import os
import re

import geojson

import hmc_topology_to_geojson


def topology_geometry_file_reader(path):
    topology_geometry_reference_file_path = ''
    for r, d, fs in os.walk(path):
        for f in fs:
            if re.match("topology-geometry_.*\.geojson$", f):
                topology_geometry_reference_file_path = os.path.join(path, f)
                break
    if topology_geometry_reference_file_path != '':
        topology_geometry_reference_file = open(topology_geometry_reference_file_path, 'r')
        return geojson.loads(topology_geometry_reference_file.read())
    else:
        for r, d, fs in os.walk(path):
            for f in fs:
                if re.match("topology-geometry_.*\.json$", f):
                    hmc_topology_to_geojson.convert(os.path.join(path, f))
                    topology_geometry_reference_file = open('{}.geojson'.format(os.path.join(path, f), 'r'))
                    return geojson.loads(topology_geometry_reference_file.read())


def address_attribute_file_reader(path):
    address_attribute_reference_file_path = ''
    for r, d, fs in os.walk(path):
        for f in fs:
            if re.match("address-attributes_.*\.geojson$", f):
                address_attribute_reference_file_path = os.path.join(path, f)
                break
    if address_attribute_reference_file_path != '':
        address_attribute_reference_file = open(address_attribute_reference_file_path, 'r')
        return geojson.loads(address_attribute_reference_file.read())


def address_attribute_list_generator(partition_folder_path):
    address_attribute_reference_geojson = address_attribute_file_reader(partition_folder_path)
    return address_attribute_reference_geojson


def segment_list_generator(partition_folder_path):
    topology_geometry_reference_geojson = topology_geometry_file_reader(partition_folder_path)
    topology_geometry_reference_segment_list: geojson.FeatureCollection
    for topology_geometry_reference_geojson_feature_list in topology_geometry_reference_geojson['features']:
        if topology_geometry_reference_geojson_feature_list['properties'][0]['featureType'] == 'segment':
            topology_geometry_reference_segment_list = topology_geometry_reference_geojson_feature_list
            return topology_geometry_reference_segment_list


def node_list_generator(partition_folder_path):
    topology_geometry_reference_geojson = topology_geometry_file_reader(partition_folder_path)
    topology_geometry_reference_node_list: geojson.FeatureCollection
    for topology_geometry_reference_geojson_feature_list in topology_geometry_reference_geojson['features']:
        print(topology_geometry_reference_geojson_feature_list['properties'])
        if topology_geometry_reference_geojson_feature_list['properties'][0]['featureType'] == 'node':
            topology_geometry_reference_node_list = topology_geometry_reference_geojson_feature_list
            return topology_geometry_reference_node_list
