import os
import re

import geojson

def file_reader(path):
    topology_geometry_reference_file_path = ''
    for r, d, fs in os.walk(path):
        for f in fs:
            if re.match("topology-geometry_.*\.geojson$", f):
                topology_geometry_reference_file_path = os.path.join(path, f)
                break
    topology_geometry_reference_file = open(topology_geometry_reference_file_path, 'r')
    return geojson.loads(topology_geometry_reference_file.read())


def segment_list_generator(partition_folder_path) -> list:
    topology_geometry_reference_geojson = file_reader(partition_folder_path)
    topology_geometry_reference_segment_list: geojson.FeatureCollection
    for topology_geometry_reference_geojson_feature_list in topology_geometry_reference_geojson['features']:
        if topology_geometry_reference_geojson_feature_list['properties'][0]['featureType'] == 'segment':
            topology_geometry_reference_segment_list = topology_geometry_reference_geojson_feature_list
            return topology_geometry_reference_segment_list

def node_list_generator(partition_folder_path) -> list:
    topology_geometry_reference_geojson = file_reader(partition_folder_path)
    topology_geometry_reference_node_list: geojson.FeatureCollection
    for topology_geometry_reference_geojson_feature_list in topology_geometry_reference_geojson['features']:
        if topology_geometry_reference_geojson_feature_list['properties'][0]['featureType'] == 'node':
            topology_geometry_reference_segment_list = topology_geometry_reference_geojson_feature_list
            return topology_geometry_reference_segment_list

