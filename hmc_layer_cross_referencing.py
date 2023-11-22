import os
import re

import geojson


def geojson_file_reader(path, layer_name):
    file_path = ''
    for r, d, fs in os.walk(path):
        for f in fs:
            if re.match("{}_.*\.geojson$".format(layer_name), f):
                file_path = os.path.join(path, f)
                break
    if file_path != '':
        attribute_reference_file = open(file_path, 'r', encoding='utf-8')
        return geojson.loads(attribute_reference_file.read())


def get_reference_geojson(partition_folder_path, layer_name):
    reference_geojson = geojson_file_reader(partition_folder_path, layer_name)
    return reference_geojson


def segment_list_generator(partition_folder_path):
    topology_geometry_reference_geojson = geojson_file_reader(partition_folder_path, 'topology-geometry')
    topology_geometry_reference_segment_list: geojson.FeatureCollection
    for topology_geometry_reference_geojson_feature_list in topology_geometry_reference_geojson['features']:
        if topology_geometry_reference_geojson_feature_list['properties'][0]['featureType'] == 'segment':
            topology_geometry_reference_segment_list = topology_geometry_reference_geojson_feature_list
            return topology_geometry_reference_segment_list


def node_list_generator(partition_folder_path):
    topology_geometry_reference_geojson = geojson_file_reader(partition_folder_path, 'topology-geometry')
    topology_geometry_reference_node_list: geojson.FeatureCollection
    for topology_geometry_reference_geojson_feature_list in topology_geometry_reference_geojson['features']:
        if topology_geometry_reference_geojson_feature_list['properties'][0]['featureType'] == 'node':
            topology_geometry_reference_node_list = topology_geometry_reference_geojson_feature_list
            return topology_geometry_reference_node_list


