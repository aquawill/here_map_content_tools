import json
import os

import geojson
from here.content.utils.hmc_external_references import HMCExternalReferences
from here.content.utils.hmc_external_references import Ref
from here.platform.adapter import Identifier
from here.platform.adapter import Partition

hmc_decoded_json_file_path = r'C:\Users\guanlwu\PycharmProjects\here_python_sdk_test_project\decoded\hrn_here_data__olp-here_rib-2\23599607\topology-geometry_23599607_v5570.json'
dirname = os.path.dirname(hmc_decoded_json_file_path)
file_name = os.path.basename(hmc_decoded_json_file_path)

output_geojson_file_path = os.path.join(dirname, '{}.geojson'.format(file_name))

node_feature_list = []
segment_feature_list = []

hmc_external_reference = HMCExternalReferences()

with open(hmc_decoded_json_file_path, mode='r', encoding='utf-8') as hmc_json:
    with open(output_geojson_file_path, mode='w', encoding='utf-8') as output_geojson:
        hmc_json = json.loads(hmc_json.read())
        partion_name = hmc_json['partitionName']
        node_list = hmc_json['node']
        segment_list = hmc_json['segment']
        for node in node_list:
            node_feature = geojson.Feature()
            node_geometry = geojson.geometry.Geometry()
            node_geometry.type = 'Point'
            node_geometry.coordinates = [node['geometry']['longitude'], node['geometry']['latitude']]
            node_feature.geometry = node_geometry
            for node_key in list(node.keys()):
                node_feature.properties[node_key] = node[node_key]
            node_feature_list.append(node_feature)

        for segment in segment_list:
            segment_keys = list(segment.keys())
            segment_feature = geojson.Feature()
            segment_geometry = geojson.geometry.Geometry()
            segment_geometry.type = 'LineString'
            coordinates = []
            for latlng_pair in segment['geometry']['point']:
                lat = latlng_pair['latitude']
                lng = latlng_pair['longitude']
                coordinates.append([lng, lat])
            segment_geometry.coordinates = coordinates
            segment_feature.geometry = segment_geometry
            for key in segment_keys:
                segment_feature.properties[key] = segment[key]
            segment_feature.properties['hmcExternalReference'] = {}
            segment_feature.properties['hmcExternalReference']['pvid'] = hmc_external_reference.segment_to_pvid(
                partition_id=partion_name,
                segment_ref=Ref(partition=Partition(str(partion_name)), identifier=Identifier(segment['identifier'])))
            segment_feature_list.append(segment_feature)
        topology_feature_collection = geojson.FeatureCollection([node_feature_list, segment_feature_list])

        output_geojson.write(str(topology_feature_collection))
        print(topology_feature_collection)