import json
import os
import re

import geojson

partition_folder_path = r"decoded/hrn_here_data__olp-here_rib-2/24318368"

point_feature_layers = ['landmarks-3d']

feature_list = []

for r, d, fs in os.walk(partition_folder_path):
    for f in fs:
        for point_feature_layer in point_feature_layers:
            if re.match('^{}_.*\.json$'.format(point_feature_layer), f):
                hmc_decoded_json_file_path = os.path.join(partition_folder_path, f)
                output_geojson_file_path = os.path.join(partition_folder_path, '{}.geojson'.format(f))
                print('processing: ', f)
                feature_list = []
                with open(hmc_decoded_json_file_path, mode='r', encoding='utf-8') as hmc_json:
                    with open(output_geojson_file_path, mode='w', encoding='utf-8') as output_geojson:
                        hmc_json = json.loads(hmc_json.read())
                        del hmc_json['partitionName']
                        landmark_list = hmc_json['landmark']
                        landmark_feature_list = []
                        for landmark in landmark_list:
                            landmark_feature = geojson.Feature()
                            landmark_feature.geometry = geojson.geometry.Geometry()
                            landmark_feature.geometry.type = 'Point'
                            landmark_feature_geometry_geometry_coordinates = [landmark['anchorPoint']['longitude'],
                                                                              landmark['anchorPoint']['latitude']]
                            landmark_feature.geometry.coordinates = landmark_feature_geometry_geometry_coordinates
                            del landmark['anchorPoint']
                            for key in list(landmark.keys()):
                                landmark_feature.properties[key] = landmark[key]
                            landmark_feature_list.append(landmark_feature)
                        landmark_feature_collection = geojson.FeatureCollection(landmark_feature_list)
                        output_geojson.write(str(landmark_feature_collection))
