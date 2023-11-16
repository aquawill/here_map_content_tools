import json
import os

import geojson

hmc_decoded_json_file_path = r'C:\Users\guanlwu\PycharmProjects\here_python_sdk_test_project\decoded\hrn_here_data__olp-here_rib-2\23599607\here-fueling-stations_23599607_v5571.json'
dirname = os.path.dirname(hmc_decoded_json_file_path)
file_name = os.path.basename(hmc_decoded_json_file_path)

output_geojson_file_path = os.path.join(dirname, '{}.geojson'.format(file_name))

feature_list = []


def place_index_attribute_mapping(attribute_name):
    attribute_list = hmc_json[attribute_name]
    for attribute in attribute_list:
        attribute_place_index = attribute['placeIndex']
        del attribute['placeIndex']
        for attribute_place_index in attribute_place_index:
            feature_list[attribute_place_index].properties[attribute_name] = attribute
    del hmc_json[attribute_name]


def attribute_list_mapping(attribute_name):
    attribute_list = hmc_json[attribute_name]
    attribute_list_size = len(attribute_list)
    for i in range(attribute_list_size):
        feature_list[i].properties[attribute_name] = attribute_list[i]
    del hmc_json[attribute_name]


with open(hmc_decoded_json_file_path, mode='r', encoding='utf-8') as hmc_json:
    with open(output_geojson_file_path, mode='w', encoding='utf-8') as output_geojson:
        hmc_json = json.loads(hmc_json.read())
        del hmc_json['partitionName']

        place_list = hmc_json['place']

        # parse locations to geojson points
        location_list = hmc_json['location']

        # create basic geojson feature collection
        for location in location_list:
            point = geojson.Point()
            feature = geojson.Feature()
            geometry = geojson.geometry.Geometry()
            geometry.type = str(location['locationType']).capitalize()
            if location.get('displayPosition') is not None:
                geometry.coordinates = [location['displayPosition']['longitude'],
                                        location['displayPosition']['latitude']]
            elif location.get('geometry').get('point') is not None:
                geometry.coordinates = [location['geometry']['point']['longitude'],
                                        location['geometry']['point']['latitude']]
            feature.geometry = geometry
            feature.properties['location'] = location
            feature_list.append(feature)
        del hmc_json['location']

        hmc_json_keys = list(hmc_json.keys())

        for key in hmc_json_keys:
            if hmc_json[key][0].get('placeIndex') is not None:
                place_index_attribute_mapping(key)
            else:
                attribute_list_mapping(key)

        feature_collection = geojson.FeatureCollection(feature_list)
        output_geojson.write(str(feature_collection))
        print(feature_collection)
