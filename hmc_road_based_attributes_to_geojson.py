import json
import os

import geojson

hmc_decoded_json_file_path = r'C:\Users\guanlwu\PycharmProjects\here_python_sdk_test_project\decoded\hrn_here_data__olp-here_rib-2\23599607\traffic-patterns_23599607_v5570.json'
dir_name = os.path.dirname(hmc_decoded_json_file_path)
file_name = os.path.basename(hmc_decoded_json_file_path)

topology_geometry_reference_file_path = r'C:\Users\guanlwu\PycharmProjects\here_python_sdk_test_project\decoded\hrn_here_data__olp-here_rib-2\23599607\topology-geometry_23599607_v5570.json.geojson'
topology_geometry_reference_file = open(topology_geometry_reference_file_path, 'r')
topology_geometry_reference_geojson = geojson.loads(topology_geometry_reference_file.read())
topology_geometry_reference_segment_list: geojson.FeatureCollection
for topology_geometry_reference_geojson_feature_list in topology_geometry_reference_geojson['features']:
    if topology_geometry_reference_geojson_feature_list['properties'][0]['featureType'] == 'segment':
        topology_geometry_reference_segment_list = topology_geometry_reference_geojson_feature_list

output_geojson_file_path = os.path.join(dir_name, '{}.geojson'.format(file_name))

segment_anchor_with_attributes_list = []


def segment_anchor_attribute_mapping(attribute_name):
    attribute_list = hmc_json[attribute_name]
    for attribute in attribute_list:
        attribute_segment_anchor_indexes = attribute['segmentAnchorIndex']
        del attribute['segmentAnchorIndex']
        for attribute_segment_anchor_index in attribute_segment_anchor_indexes:
            segment_anchor_with_attributes_list[attribute_segment_anchor_index]['properties'][
                attribute_name] = attribute


# hmc_external_reference = HMCExternalReferences()

with open(hmc_decoded_json_file_path, mode='r', encoding='utf-8') as hmc_json:
    with open(output_geojson_file_path, mode='w', encoding='utf-8') as output_geojson:
        hmc_json = json.loads(hmc_json.read())
        partion_name = hmc_json['partitionName']
        segment_anchor_with_attributes_list = hmc_json['segmentAnchor']
        # segment_anchor_feature_list = []
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
                        segment_anchor_geojson_feature.geometry = feature.geometry
                        segment_anchor_geojson_feature.properties = segment_anchor_with_attributes
                        segment_anchor_geojson_feature.type = 'LingString'
                        segment_anchor_with_topology_list.append(segment_anchor_geojson_feature)
        segment_anchor_with_topology_feature_collection = geojson.FeatureCollection(segment_anchor_with_topology_list)
        print(segment_anchor_with_topology_feature_collection)
        output_geojson.write(str(segment_anchor_with_topology_feature_collection))
