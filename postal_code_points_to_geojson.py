import json
import os
import re

import geojson
from progressbar import ProgressBar

import hmc_layer_cross_referencing

partition_folder_path = r"decoded/hrn_here_data__olp-here_rib-2/17446627"

polygon_feature_layers = ['postal-code-points']

for r, d, fs in os.walk(partition_folder_path):
    for f in fs:
        for polygon_feature_layer in polygon_feature_layers:
            if re.match('^{}_.*\.json$'.format(polygon_feature_layer), f):
                hmc_decoded_json_file_path = os.path.join(partition_folder_path, f)
                with open(hmc_decoded_json_file_path, mode='r', encoding='utf-8') as hmc_json:
                    output_geojson_file_path = os.path.join(partition_folder_path,
                                                                     '{}.geojson'.format(f))
                    with open(output_geojson_file_path, mode='w', encoding='utf-8') as output_geojson:
                        hmc_json = json.loads(hmc_json.read())
                        partition_name = hmc_json['partitionName']
                        postal_code_point_list = hmc_json['postalCodePoints']
                        feature_list = []
                        for postal_code_point in postal_code_point_list:
                            postal_code_point_feature = geojson.Feature()
                            feature = geojson.Feature()
                            geometry = geojson.geometry.Geometry()
                            geometry.type = 'Point'
                            geometry.coordinates = [postal_code_point['postalCodeCentroid']['longitude'],
                                                    postal_code_point['postalCodeCentroid']['latitude']]
                            feature.geometry = geometry
                            del postal_code_point['postalCodeCentroid']
                            feature.properties = postal_code_point
                            feature_list.append(feature)
                        output_geojson.write(json.dumps(geojson.FeatureCollection(feature_list), indent='    '))
