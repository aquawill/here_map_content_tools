import json
import os
import re

import geojson
import shapely.ops
from here.content.utils.hmc_external_references import HMCExternalReferences
from here.content.utils.hmc_external_references import Ref
from here.platform.adapter import Identifier
from here.platform.adapter import Partition
from progressbar import ProgressBar

import hmc_layer_cross_referencing


def topology_anchor_attribute_mapping(attribute_name):
    attribute_list = hmc_json[attribute_name]
    for attribute in attribute_list:
        if attribute.get('segmentAnchorIndex'):
            if segment_anchor_with_attributes_list:
                attribute_segment_anchor_indexes = attribute.get('segmentAnchorIndex')
                del attribute['segmentAnchorIndex']
                for attribute_segment_anchor_index in attribute_segment_anchor_indexes:
                    segment_anchor_with_attributes_list[attribute_segment_anchor_index]['properties'][
                        attribute_name] = attribute

        if attribute.get('nodeAnchorIndex'):
            if node_anchor_with_attributes_list:
                attribute_node_anchor_indexes = attribute.get('nodeAnchorIndex')
                del attribute['nodeAnchorIndex']
                for attribute_node_anchor_index in attribute_node_anchor_indexes:
                    if not node_anchor_with_attributes_list[attribute_node_anchor_index].get('properties'):
                        node_anchor_with_attributes_list[attribute_node_anchor_index]['properties'] = {}
                    node_anchor_with_attributes_list[attribute_node_anchor_index]['properties'][
                        attribute_name] = attribute


segment_anchor_with_attributes_list = []
node_anchor_with_attributes_list = []

input_layers = ['advanced-navigation-attributes', 'complex-road-attributes', 'navigation-attributes',
                'road-attributes', 'traffic-patterns', 'sign-text', 'generalized-junctions-signs',
                'bicycle-attributes', 'address-attributes', 'adas-attributes', 'truck-attributes',
                'recreational-vehicle-attributes']

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('partition_path', help='path of partition folder', type=str)
    args = parser.parse_args()
    partition_folder_path = args.partition_path

    hmc_external_reference = HMCExternalReferences()

    topology_geometry_reference_segment_list = hmc_layer_cross_referencing.segment_list_generator(partition_folder_path)
    topology_geometry_reference_node_list = hmc_layer_cross_referencing.node_list_generator(partition_folder_path)

    for r, d, fs in os.walk(partition_folder_path):
        for f in fs:
            for road_attribute_layer in input_layers:
                if re.match('^{}_.*\.json$'.format(road_attribute_layer), f):
                    hmc_decoded_json_file_path = os.path.join(partition_folder_path, f)
                    # print('processing: ', f)
                    with open(hmc_decoded_json_file_path, mode='r', encoding='utf-8') as hmc_json:

                        hmc_json = json.loads(hmc_json.read())
                        final_feature_collection = []
                        partition_name = hmc_json['partitionName']

                        segment_anchor_with_attributes_list = hmc_json.get('segmentAnchor')
                        node_anchor_with_attributes_list = hmc_json.get('nodeAnchor')

                        if segment_anchor_with_attributes_list:
                            segment_output_geojson_file_path = os.path.join(partition_folder_path,
                                                                            '{}_segments.geojson'.format(f))
                            with open(segment_output_geojson_file_path, mode='w',
                                      encoding='utf-8') as segment_output_geojson_file_path:
                                segment_anchor_with_attributes_index = 0
                                segment_process_progressbar = ProgressBar(min_value=0, max_value=len(
                                    segment_anchor_with_attributes_list), prefix='{} - processing segments:'.format(f))

                                for segment_anchor in segment_anchor_with_attributes_list:
                                    segment_anchor['properties'] = {}
                                for key in list(hmc_json.keys()):
                                    if isinstance(hmc_json[key], list) and hmc_json[key][0].get('segmentAnchorIndex'):
                                        topology_anchor_attribute_mapping(key)
                                segment_anchor_with_topology_list = []
                                for segment_anchor_with_attributes in segment_anchor_with_attributes_list:
                                    segment_process_progressbar.update(segment_anchor_with_attributes_index)
                                    segment_anchor_with_attributes_index += 1
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
                                                segment_anchor_geojson_feature.properties = segment_anchor_with_attributes
                                                feature_geometry_with_offsets_geojson = geojson.loads(
                                                    shapely.to_geojson(feature_geometry_with_offsets))
                                                if segment_start_offset == segment_end_offset:
                                                    segment_anchor_geojson_feature.type = 'Point'
                                                    segment_anchor_geojson_feature.geometry = geojson.geometry.Point(
                                                        feature_geometry_with_offsets_geojson)
                                                else:
                                                    segment_anchor_geojson_feature.type = 'LineString'
                                                    segment_anchor_geojson_feature.geometry = geojson.geometry.LineString(
                                                        feature_geometry_with_offsets_geojson)

                                                    # Get LINK PVID with HMC Segment ID
                                                    segment_anchor_geojson_feature.properties[
                                                        'hmcExternalReference'] = {}
                                                    segment_anchor_geojson_feature.properties['hmcExternalReference'][
                                                        'pvid'] = hmc_external_reference.segment_to_pvid(
                                                        partition_id=partition_name,
                                                        segment_ref=Ref(partition=Partition(str(partition_name)),
                                                                        identifier=Identifier(
                                                                            segment_ref['identifier'])))

                                                segment_anchor_with_topology_list.append(segment_anchor_geojson_feature)
                                segment_anchor_with_topology_feature_collection = geojson.FeatureCollection(
                                    segment_anchor_with_topology_list)
                                segment_process_progressbar.finish()
                                segment_output_geojson_file_path.write(
                                    json.dumps(segment_anchor_with_topology_feature_collection, indent='    '))

                        if node_anchor_with_attributes_list:
                            node_output_geojson_file_path = os.path.join(partition_folder_path,
                                                                         '{}_nodes.geojson'.format(f))
                            with open(node_output_geojson_file_path, mode='w',
                                      encoding='utf-8') as node_output_geojson_file:
                                node_anchor_with_attributes_index = 0
                                node_process_progressbar = ProgressBar(min_value=0,
                                                                       max_value=len(node_anchor_with_attributes_list),
                                                                       prefix='{} - processing nodes:'.format(f))
                                for node_anchor in node_anchor_with_attributes_list:
                                    node_anchor['properties'] = {}
                                for key in list(hmc_json.keys()):
                                    if isinstance(hmc_json[key], list):
                                        for hmc_json_element in hmc_json[key]:
                                            if hmc_json_element.get('nodeAnchorIndex'):
                                                topology_anchor_attribute_mapping(key)
                                node_anchor_with_topology_list = []
                                for node_anchor_with_attributes in node_anchor_with_attributes_list:
                                    node_process_progressbar.update(node_anchor_with_attributes_index)
                                    node_anchor_with_attributes_index += 1
                                    node_ref = node_anchor_with_attributes['nodeRef']
                                    node_ref_partition_name = node_ref['partitionName']
                                    node_ref_identifier = node_ref['identifier']
                                    for feature in topology_geometry_reference_node_list['features']:
                                        if node_ref_identifier == feature['properties']['identifier']:
                                            node_anchor_geojson_feature = geojson.Feature()
                                            node_anchor_geojson_feature.geometry = geojson.geometry.Point(
                                                feature.geometry)
                                            node_anchor_geojson_feature.properties = node_anchor_with_attributes[
                                                'properties']
                                            node_anchor_with_topology_list.append(node_anchor_geojson_feature)
                                node_process_progressbar.finish()

                                node_anchor_with_topology_feature_collection = geojson.FeatureCollection(
                                    node_anchor_with_topology_list)
                                final_feature_collection.append(node_anchor_with_topology_feature_collection)
                                node_output_geojson_file.write(
                                    json.dumps(node_anchor_with_topology_feature_collection, indent='    '))
