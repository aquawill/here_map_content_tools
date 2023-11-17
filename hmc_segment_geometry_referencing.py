import os
import re

import geojson


def list_generator(partition_folder_path) -> list:
    topology_geometry_reference_file_path = ''
    for r, d, fs in os.walk(partition_folder_path):
        for f in fs:
            if re.match("topology-geometry_.*\.geojson$", f):
                print('topology reference: ', f)
                topology_geometry_reference_file_path = os.path.join(partition_folder_path, f)
                break
    topology_geometry_reference_file = open(topology_geometry_reference_file_path, 'r')
    topology_geometry_reference_geojson = geojson.loads(topology_geometry_reference_file.read())
    topology_geometry_reference_segment_list: geojson.FeatureCollection
    for topology_geometry_reference_geojson_feature_list in topology_geometry_reference_geojson['features']:
        if topology_geometry_reference_geojson_feature_list['properties'][0]['featureType'] == 'segment':
            topology_geometry_reference_segment_list = topology_geometry_reference_geojson_feature_list
            return topology_geometry_reference_segment_list
