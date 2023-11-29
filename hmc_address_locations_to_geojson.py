import json
import os
import re

import geojson
from progressbar import ProgressBar

import hmc_layer_cross_referencing

polygon_feature_layers = ['address-locations']

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('partition_path', help='path of partition folder', type=str)
    args = parser.parse_args()
    partition_folder_path = args.partition_path

    address_attributes_reference_list = hmc_layer_cross_referencing.get_reference_geojson(partition_folder_path,
                                                                                          'address-attributes')

    for r, d, fs in os.walk(partition_folder_path):
        for f in fs:
            for polygon_feature_layer in polygon_feature_layers:
                if re.match('^{}_.*\.json$'.format(polygon_feature_layer), f):
                    hmc_decoded_json_file_path = os.path.join(partition_folder_path, f)
                    with open(hmc_decoded_json_file_path, mode='r', encoding='utf-8') as hmc_json:
                        location_output_geojson_file_path = os.path.join(partition_folder_path,
                                                                         '{}_location.geojson'.format(f))
                        with open(location_output_geojson_file_path, mode='w',
                                  encoding='utf-8') as location_output_geojson:
                            hmc_json = json.loads(hmc_json.read())
                            partition_name = hmc_json['partitionName']
                            location_list = hmc_json['location']
                            location_output_list = []
                            location_process_progressbar = ProgressBar(min_value=0, max_value=len(
                                location_list), prefix='{} - processing locations:'.format(f))
                            location_index = 0
                            for location in location_list:
                                location_process_progressbar.update(location_index)
                                location_index += 1
                                location_element_list = []
                                if location.get('displayPosition'):
                                    location_display_position_feature = geojson.Feature()
                                    location_display_position_feature_geometry = geojson.geometry.Geometry()
                                    location_display_position_feature_geometry.type = 'Point'
                                    location_display_position_feature_geometry.coordinates = [
                                        location['displayPosition']['longitude'],
                                        location['displayPosition']['latitude']]
                                    del location['displayPosition']
                                    location_display_position_feature.geometry = location_display_position_feature_geometry
                                    location_display_position_feature.properties = location
                                    location_output_list.append(location_display_position_feature)
                            location_feature_collection = geojson.FeatureCollection(location_output_list)
                            location_process_progressbar.finish()
                            location_output_geojson.write(json.dumps(location_feature_collection, indent='    '))
                        address_output_geojson_file_path = os.path.join(partition_folder_path,
                                                                        '{}_address.geojson'.format(f))
                        with open(address_output_geojson_file_path, mode='w',
                                  encoding='utf-8') as address_output_geojson:
                            postal_code_list = hmc_json.get('postalCode')
                            address_list = hmc_json['address']
                            address_process_progressbar = ProgressBar(min_value=0, max_value=len(
                                address_list), prefix='{} - processing addresses:'.format(f))
                            address_process_index = 0
                            address_feature_list = []
                            from_street_section_ref_partition_name_set = set()
                            for address in address_list:
                                address_process_progressbar.update(address_process_index)
                                address_process_index += 1
                                if address.get('fromStreetSectionRef'):
                                    from_street_section_ref = address['fromStreetSectionRef']
                                    from_street_section_ref_partition_name = from_street_section_ref['partitionName']
                                    from_street_section_ref_identifier = from_street_section_ref['identifier']
                                    from_street_section_ref_partition_name_set.add(
                                        from_street_section_ref_partition_name)
                                    for address_attribute_reference in address_attributes_reference_list.features:
                                        if address_attribute_reference.properties['properties']['streetSection'][
                                            'streetSectionRef']['identifier'] == from_street_section_ref_identifier:
                                            address_feature = geojson.Feature()
                                            address_feature_geometry = address_attribute_reference.geometry
                                            address_feature.geometry = address_feature_geometry
                                            address_feature.properties = address
                                            # address_feature.properties['house'] = address['house']
                                            if address.get('postalMapping'):
                                                address_postal_mapping_list = address['postalMapping']
                                                address_feature_postal_code_list = []
                                                for address_feature_postal_mapping in address_postal_mapping_list:
                                                    if address_feature_postal_mapping.get('postalCodeIndex'):
                                                        address_feature_postal_mapping_index = address_feature_postal_mapping.get(
                                                            'postalCodeIndex')
                                                        address_feature_postal_code_list.append(
                                                            postal_code_list[address_feature_postal_mapping_index])
                                                        address_feature_postal_mapping[
                                                            'postalCode'] = address_feature_postal_code_list
                                                address_feature.properties[
                                                    'postalMapping'] = address_feature_postal_code_list
                                            address_feature_list.append(address_feature)
                            address_feature_collection = geojson.FeatureCollection(address_feature_list)
                            address_process_progressbar.finish()
                            print('admin reference layers: ', from_street_section_ref_partition_name_set)
                            address_output_geojson.write(json.dumps(address_feature_collection, indent='    '))
