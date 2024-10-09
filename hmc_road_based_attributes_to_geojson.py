import json
import os
import re
import geojson
import shapely
from here.content.utils.hmc_external_references import HMCExternalReferences, Ref
from here.platform.adapter import Identifier, Partition
from here.platform import Platform
# from progressbar import ProgressBar  # 註釋掉進度條的導入
from hmc_downloader import HmcDownloader
from download_options import FileFormat
import hmc_layer_cross_referencing
import multiprocessing

class HMCAttributeProcessor:
    def __init__(self, partition_folder_path, overwrite_result='n'):
        self.partition_folder_path = partition_folder_path
        self.overwrite_result = overwrite_result.lower()
        self.hmc_external_reference = HMCExternalReferences()
        self.input_layers = [
            'advanced-navigation-attributes', 'complex-road-attributes', 'navigation-attributes',
            'road-attributes', 'traffic-patterns', 'sign-text', 'generalized-junctions-signs',
            'bicycle-attributes', 'address-attributes', 'adas-attributes', 'truck-attributes',
            'recreational-vehicle-attributes'
        ]

    def process_attributes(self):
        file_list = []
        for r, d, fs in os.walk(self.partition_folder_path):
            for f in fs:
                for road_attribute_layer in self.input_layers:
                    if re.match(f'^{road_attribute_layer}_.*\.json$', f):
                        file_list.append((r, f))
        
        with multiprocessing.Pool() as pool:
            results = pool.starmap(self._process_file, file_list)
        
        # 合併所有進程的結果
        all_street_section_refs = set()
        for result in results:
            if result:
                all_street_section_refs.update(result)
        
        self._download_street_name_references(all_street_section_refs)

    def _process_file(self, r, f):
        hmc_decoded_json_file_path = os.path.join(r, f)
        print(hmc_decoded_json_file_path)
        with open(hmc_decoded_json_file_path, mode='r', encoding='utf-8') as hmc_json_file:
            hmc_json = json.load(hmc_json_file)
            partition_name = hmc_json['partitionName']
            
            segment_processor = SegmentProcessor(hmc_json, r, f, partition_name, self.hmc_external_reference, self.overwrite_result)
            segment_processor.process()
            
            node_processor = NodeProcessor(hmc_json, r, f, self.overwrite_result)
            node_processor.process()
            
            return self._process_street_sections(hmc_json)

    def _process_street_sections(self, hmc_json):
        street_section_refs = set()
        if 'streetSection' in hmc_json:
            for street_section in hmc_json['streetSection']:
                street_section_ref = street_section.get('streetSectionRef')
                if street_section_ref:
                    street_section_refs.add(street_section_ref.get('partitionName'))
        return street_section_refs

    def _download_street_name_references(self, street_section_refs):
        print('street-name reference partitions: ', list(street_section_refs))
        street_name_reference_layers = ['street-names']
        print('download street-name reference layers: {}'.format(', '.join(street_name_reference_layers)))
        
        platform = Platform()
        print('HERE Platform Status: ', platform.get_status())
        platform_catalog = platform.get_catalog(hrn='hrn:here:data::olp-here:rib-2')
        
        for street_name_partition in street_section_refs:
            for street_name_reference_layer in street_name_reference_layers:
                HmcDownloader(catalog=platform_catalog, layer=street_name_reference_layer,
                              file_format=FileFormat.JSON).download_generic_layer(
                    quad_ids=[street_name_partition])

class SegmentProcessor:
    def __init__(self, hmc_json, r, f, partition_name, hmc_external_reference, overwrite_result):
        self.hmc_json = hmc_json
        self.r = r
        self.f = f
        self.partition_name = partition_name
        self.hmc_external_reference = hmc_external_reference
        self.overwrite_result = overwrite_result
        self.segment_anchor_with_attributes_list = hmc_json.get('segmentAnchor', [])
        self.topology_geometry_reference_segment_list = hmc_layer_cross_referencing.segment_list_generator(r)

    def process(self):
        if not self.segment_anchor_with_attributes_list:
            return

        segment_output_geojson_file_path = os.path.join(self.r, f'{self.f}_segments.geojson')
        if os.path.exists(segment_output_geojson_file_path) and self.overwrite_result != 'y':
            print(f'{segment_output_geojson_file_path} --> existing already.')
            return

        with open(segment_output_geojson_file_path, mode='w', encoding='utf-8') as output_file:
            self._process_segments(output_file)

    def _process_segments(self, output_file):
        for segment_anchor in self.segment_anchor_with_attributes_list:
            segment_anchor['properties'] = {}
        
        self._map_attributes()
        
        segment_anchor_with_topology_list = []
        # progress_bar = ProgressBar(max_value=len(self.segment_anchor_with_attributes_list), 
        #                            prefix=f'{self.f} - processing segments:')  # 註釋掉進度條

        for index, segment_anchor_with_attributes in enumerate(self.segment_anchor_with_attributes_list):
            # progress_bar.update(index)  # 註釋掉進度條更新
            self._process_segment(segment_anchor_with_attributes, segment_anchor_with_topology_list)

        # progress_bar.finish()  # 註釋掉進度條結束
        
        segment_anchor_with_topology_feature_collection = geojson.FeatureCollection(segment_anchor_with_topology_list)
        json.dump(segment_anchor_with_topology_feature_collection, output_file, indent=4)

    def _map_attributes(self):
        for key, value in self.hmc_json.items():
            if isinstance(value, list):
                if value and isinstance(value[0], dict):
                    if 'segmentAnchorIndex' in value[0]:
                        self._map_attribute(key, 'segmentAnchorIndex')
                    elif 'originSegmentAnchorIndex' in value[0]:
                        self._map_attribute(key, 'originSegmentAnchorIndex')

    def _map_attribute(self, attribute_name, index_name):
        attribute_list = self.hmc_json[attribute_name]
        for attribute in attribute_list:
            if index_name in attribute:
                indexes = attribute[index_name]
                del attribute[index_name]
                if attribute:
                    if isinstance(indexes, list):
                        for index in indexes:
                            self.segment_anchor_with_attributes_list[index]['properties'][attribute_name] = attribute
                    elif isinstance(indexes, int):
                        self.segment_anchor_with_attributes_list[indexes]['properties'][attribute_name] = attribute

    def _process_segment(self, segment_anchor_with_attributes, segment_anchor_with_topology_list):
        for oriented_segment_ref in segment_anchor_with_attributes['orientedSegmentRef']:
            segment_ref = oriented_segment_ref['segmentRef']
            segment_ref_identifier = segment_ref['identifier']
            
            for feature in self.topology_geometry_reference_segment_list['features']:
                if segment_ref_identifier == feature['properties']['identifier']:
                    segment_anchor_geojson_feature = self._create_segment_feature(segment_anchor_with_attributes, feature)
                    segment_anchor_with_topology_list.append(segment_anchor_geojson_feature)

    def _create_segment_feature(self, segment_anchor_with_attributes, feature):
        segment_anchor_geojson_feature = geojson.Feature()
        segment_start_offset = segment_anchor_with_attributes.get('firstSegmentStartOffset', 0.0)
        segment_end_offset = segment_anchor_with_attributes.get('lastSegmentEndOffset', 1.0)
        
        feature_geometry = self._create_feature_geometry(feature, segment_start_offset, segment_end_offset)
        
        segment_anchor_geojson_feature.properties = segment_anchor_with_attributes
        segment_anchor_geojson_feature.geometry = feature_geometry
        
        if segment_start_offset != segment_end_offset:
            self._add_external_reference(segment_anchor_geojson_feature, segment_anchor_with_attributes)
        
        return segment_anchor_geojson_feature

    def _create_feature_geometry(self, feature, start_offset, end_offset):
        feature_geometry = shapely.geometry.shape(feature.geometry)
        feature_geometry_length = feature_geometry.length
        start_dist = feature_geometry_length * start_offset
        end_dist = feature_geometry_length * end_offset
        
        feature_geometry_with_offsets = shapely.ops.substring(feature_geometry, start_dist, end_dist)
        feature_geometry_with_offsets_geojson = geojson.loads(shapely.to_geojson(feature_geometry_with_offsets))
        
        if start_offset == end_offset:
            return geojson.geometry.Point(feature_geometry_with_offsets_geojson)
        else:
            return geojson.geometry.LineString(feature_geometry_with_offsets_geojson)

    def _add_external_reference(self, feature, segment_anchor_with_attributes):
        segment_ref = segment_anchor_with_attributes['orientedSegmentRef'][0]['segmentRef']
        feature.properties['hmcExternalReference'] = {
            'pvid': self.hmc_external_reference.segment_to_pvid(
                partition_id=self.partition_name,
                segment_ref=Ref(partition=Partition(str(self.partition_name)),
                                identifier=Identifier(segment_ref['identifier']))
            )
        }

class NodeProcessor:
    def __init__(self, hmc_json, r, f, overwrite_result):
        self.hmc_json = hmc_json
        self.r = r
        self.f = f
        self.overwrite_result = overwrite_result
        self.node_anchor_with_attributes_list = hmc_json.get('nodeAnchor', [])
        self.topology_geometry_reference_node_list = hmc_layer_cross_referencing.node_list_generator(r)

    def process(self):
        if not self.node_anchor_with_attributes_list:
            return

        node_output_geojson_file_path = os.path.join(self.r, f'{self.f}_nodes.geojson')
        if os.path.exists(node_output_geojson_file_path) and self.overwrite_result != 'y':
            print(f'{node_output_geojson_file_path} --> existing already.')
            return

        with open(node_output_geojson_file_path, mode='w', encoding='utf-8') as output_file:
            self._process_nodes(output_file)

    def _process_nodes(self, output_file):
        for node_anchor in self.node_anchor_with_attributes_list:
            node_anchor['properties'] = {}
        
        self._map_attributes()
        
        node_anchor_with_topology_list = []
        # progress_bar = ProgressBar(max_value=len(self.node_anchor_with_attributes_list), 
        #                            prefix=f'{self.f} - processing nodes:')  # 註釋掉進度條

        for index, node_anchor_with_attributes in enumerate(self.node_anchor_with_attributes_list):
            # progress_bar.update(index)  # 註釋掉進度條更新
            self._process_node(node_anchor_with_attributes, node_anchor_with_topology_list)

        # progress_bar.finish()  # 註釋掉進度條結束
        
        node_anchor_with_topology_feature_collection = geojson.FeatureCollection(node_anchor_with_topology_list)
        json.dump(node_anchor_with_topology_feature_collection, output_file, indent=4)

    def _map_attributes(self):
        for key, value in self.hmc_json.items():
            if isinstance(value, list):
                for element in value:
                    if isinstance(element, dict) and 'nodeAnchorIndex' in element:
                        self._map_attribute(key, 'nodeAnchorIndex')
                        break

    def _map_attribute(self, attribute_name, index_name):
        attribute_list = self.hmc_json[attribute_name]
        for attribute in attribute_list:
            if index_name in attribute:
                indexes = attribute[index_name]
                del attribute[index_name]
                if attribute:
                    for index in indexes:
                        if 'properties' not in self.node_anchor_with_attributes_list[index]:
                            self.node_anchor_with_attributes_list[index]['properties'] = {}
                        self.node_anchor_with_attributes_list[index]['properties'][attribute_name] = attribute

    def _process_node(self, node_anchor_with_attributes, node_anchor_with_topology_list):
        node_ref = node_anchor_with_attributes['nodeRef']
        node_ref_identifier = node_ref['identifier']
        
        for feature in self.topology_geometry_reference_node_list['features']:
            if node_ref_identifier == feature['properties']['identifier']:
                node_anchor_geojson_feature = geojson.Feature()
                node_anchor_geojson_feature.geometry = geojson.geometry.Point(feature.geometry)
                node_anchor_geojson_feature.properties = node_anchor_with_attributes['properties']
                node_anchor_with_topology_list.append(node_anchor_geojson_feature)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('partition_path', help='path of partition folder', type=str)
    parser.add_argument('overwrite_result', help='overwrite geojson result file (y/N)', nargs='?', default='n', type=str)
    args = parser.parse_args()

    processor = HMCAttributeProcessor(args.partition_path, args.overwrite_result)
    processor.process_attributes()