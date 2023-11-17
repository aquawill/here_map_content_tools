import json
import os
import re

import geojson
import shapely.ops
from here.content.utils.hmc_external_references import HMCExternalReferences
from here.content.utils.hmc_external_references import Ref
from here.platform.adapter import Identifier
from here.platform.adapter import Partition

hmc_external_reference = HMCExternalReferences()

partition_folder_path = r"decoded\hrn_here_data__olp-here_rib-2\23599607"

topology_geometry_reference_file_path = ''

for r, d, fs in os.walk(partition_folder_path):
    for f in fs:
        if re.match("topology-geometry_.*\.geojson$", f):
            print('topology reference: ', f)
            topology_geometry_reference_file_path = os.path.join(partition_folder_path, f)
            break

road_attribute_layers = ['advanced-navigation-attributes', 'complex-road-attributes', 'navigation-attributes',
                         'road-attributes', 'traffic-patterns', 'sign-text', 'generalized-junctions-signs',
                         'bicycle-attributes', 'address-attributes']

topology_geometry_reference_file = open(topology_geometry_reference_file_path, 'r')
topology_geometry_reference_geojson = geojson.loads(topology_geometry_reference_file.read())
topology_geometry_reference_segment_list: geojson.FeatureCollection
for topology_geometry_reference_geojson_feature_list in topology_geometry_reference_geojson['features']:
    if topology_geometry_reference_geojson_feature_list['properties'][0]['featureType'] == 'segment':
        topology_geometry_reference_segment_list = topology_geometry_reference_geojson_feature_list

segment_anchor_with_attributes_list = []


def segment_anchor_attribute_mapping(attribute_name):
    attribute_list = hmc_json[attribute_name]
    for attribute in attribute_list:
        attribute_segment_anchor_indexes = attribute['segmentAnchorIndex']
        del attribute['segmentAnchorIndex']
        for attribute_segment_anchor_index in attribute_segment_anchor_indexes:
            segment_anchor_with_attributes_list[attribute_segment_anchor_index]['properties'][
                attribute_name] = attribute


for r, d, fs in os.walk(partition_folder_path):
    for f in fs:
        for road_attribute_layer in road_attribute_layers:
            if re.match('^{}_.*\.json$'.format(road_attribute_layer), f):
                hmc_decoded_json_file_path = os.path.join(partition_folder_path, f)
                output_geojson_file_path = os.path.join(partition_folder_path, '{}.geojson'.format(f))
                print('processing: ', f)
                with open(hmc_decoded_json_file_path, mode='r', encoding='utf-8') as hmc_json:
                    with open(output_geojson_file_path, mode='w', encoding='utf-8') as output_geojson:
                        hmc_json = json.loads(hmc_json.read())
                        partion_name = hmc_json['partitionName']
                        segment_anchor_with_attributes_list = hmc_json['segmentAnchor']
                        for segment_anchor in segment_anchor_with_attributes_list:
                            segment_anchor['properties'] = {}
                        for key in list(hmc_json.keys()):
                            if isinstance(hmc_json[key], list) and hmc_json[key][0].get('segmentAnchorIndex'):
                                segment_anchor_attribute_mapping(key)

                        segment_anchor_with_topology_list = []
                        for segment_anchor_with_attributes in segment_anchor_with_attributes_list:
                            oriented_segment_refs = segment_anchor_with_attributes['orientedSegmentRef']

                            for oriented_segment_ref in oriented_segment_refs:
                                segment_ref = oriented_segment_ref['segmentRef']
                                segment_ref_partition_name = segment_ref['partitionName']
                                segment_ref_identifier = segment_ref['identifier']
                                for feature in topology_geometry_reference_segment_list['features']:
                                    if segment_ref_identifier == feature['properties']['identifier']:
                                        segment_anchor_geojson_feature = geojson.Feature()
                                        segment_start_offset = 0.0
                                        segment_end_offset = 1.0
                                        if segment_anchor_with_attributes.get('firstSegmentStartOffset'):
                                            segment_start_offset = segment_anchor_with_attributes.get(
                                                'firstSegmentStartOffset')
                                        if segment_anchor_with_attributes.get('lastSegmentEndOffset'):
                                            segment_end_offset = segment_anchor_with_attributes.get(
                                                'lastSegmentEndOffset')
                                        feature_geometry_length = shapely.LineString(
                                            shapely.from_geojson(str(feature.geometry))).length
                                        feature_geometry_offset_length_start = feature_geometry_length * segment_start_offset
                                        feature_geometry_offset_length_end = feature_geometry_length * segment_end_offset
                                        feature_geometry_with_offsets = shapely.ops.substring(
                                            geom=shapely.from_geojson(str(feature.geometry)),
                                            start_dist=feature_geometry_offset_length_start,
                                            end_dist=feature_geometry_offset_length_end)
                                        segment_anchor_geojson_feature.geometry = geojson.geometry.LineString(
                                            geojson.loads(shapely.to_geojson(feature_geometry_with_offsets)))
                                        segment_anchor_geojson_feature.properties = segment_anchor_with_attributes
                                        segment_anchor_geojson_feature.properties['hmcExternalReference'] = {}
                                        segment_anchor_geojson_feature.properties['hmcExternalReference'][
                                            'pvid'] = hmc_external_reference.segment_to_pvid(
                                            partition_id=partion_name,
                                            segment_ref=Ref(partition=Partition(str(partion_name)),
                                                            identifier=Identifier(segment_ref['identifier'])))
                                        segment_anchor_geojson_feature.type = 'LingString'
                                        segment_anchor_with_topology_list.append(segment_anchor_geojson_feature)
                        segment_anchor_with_topology_feature_collection = geojson.FeatureCollection(
                            segment_anchor_with_topology_list)
                        print(segment_anchor_with_topology_feature_collection)
                        output_geojson.write(str(segment_anchor_with_topology_feature_collection))
