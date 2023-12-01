import json
import os
import re

import geojson
from progressbar import ProgressBar

polygon_feature_layers = ['3d-buildings', 'building-footprints', 'cartography', 'postal-area-boundaries']


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('partition_path', help='path of partition folder', type=str)
    args = parser.parse_args()
    partition_folder_path = args.partition_path

    for r, d, fs in os.walk(partition_folder_path):
        for f in fs:
            for polygon_feature_layer in polygon_feature_layers:
                if re.match('^{}_.*\.json$'.format(polygon_feature_layer), f):
                    hmc_decoded_json_file_path = os.path.join(partition_folder_path, f)
                    with open(hmc_decoded_json_file_path, mode='r', encoding='utf-8') as hmc_json:
                        output_geojson_file_path = os.path.join(partition_folder_path, '{}.geojson'.format(f))
                        with open(output_geojson_file_path, mode='w', encoding='utf-8') as output_geojson:
                            hmc_json = json.loads(hmc_json.read())
                            partion_name = hmc_json['partitionName']
                            location_list = hmc_json['location']
                            location_output_list = []
                            location_process_progressbar = ProgressBar(min_value=0, max_value=len(
                                location_list), prefix='{} - processing locations:'.format(f))
                            location_index = 0
                            for location in location_list:
                                location_process_progressbar.update(location_index)
                                location_element_list = []

                                if location.get('alternateGeometry'):
                                    del location['alternateGeometry']

                                if location.get('displayPosition'):
                                    location_display_position_feature = geojson.Feature()
                                    location_display_position_feature_geometry = geojson.geometry.Geometry()
                                    location_display_position_feature_geometry.type = 'Point'
                                    location_display_position_feature_geometry.coordinates = [
                                        location['displayPosition']['longitude'],
                                        location['displayPosition']['latitude']]
                                    location_display_position_feature.geometry = location_display_position_feature_geometry
                                    location_element_list.append(location_display_position_feature)
                                    del location['displayPosition']

                                if location.get('boundingBox'):
                                    bounding_box_feature = geojson.Feature()
                                    bounding_box_feature_geometry = geojson.geometry.Geometry()
                                    bounding_box_feature_geometry.type = 'Polygon'
                                    bounding_box_feature_geometry_nw = [location['boundingBox']['westLongitude'],
                                                                        location['boundingBox']['northLatitude']]
                                    bounding_box_feature_geometry_sw = [location['boundingBox']['westLongitude'],
                                                                        location['boundingBox']['southLatitude']]
                                    bounding_box_feature_geometry_se = [location['boundingBox']['eastLongitude'],
                                                                        location['boundingBox']['southLatitude']]
                                    bounding_box_feature_geometry_ne = [location['boundingBox']['eastLongitude'],
                                                                        location['boundingBox']['northLatitude']]
                                    bounding_box_feature_geometry.coordinates = [[bounding_box_feature_geometry_nw,
                                                                                  bounding_box_feature_geometry_sw,
                                                                                  bounding_box_feature_geometry_se,
                                                                                  bounding_box_feature_geometry_ne,
                                                                                  bounding_box_feature_geometry_nw]]
                                    bounding_box_feature.geometry = bounding_box_feature_geometry
                                    bounding_box_feature.properties = {'polygonType': 'boundingBox'}
                                    location_element_list.append(bounding_box_feature)
                                    del location['boundingBox']

                                if location.get('geometry'):
                                    geometry_level_2_name = list(location['geometry'].keys())[0]
                                    geometry_level_3_name = list(location['geometry'][geometry_level_2_name].keys())[0]
                                    location_geometry_multi_component_list = \
                                        location['geometry'][geometry_level_2_name][
                                            geometry_level_3_name]
                                    for location_geometry_multi_component in location_geometry_multi_component_list:

                                        polygon_exteriorRing_feature = geojson.Feature()
                                        polygon_exteriorRing_feature_geometry = geojson.geometry.Geometry()
                                        polygon_exteriorRing_feature_geometry.type = ''
                                        polygon_exteriorRing_feature_geometry_list = []
                                        if location_geometry_multi_component.get('polygon'):
                                            # 3d-buildings
                                            polygon_exteriorRing_point_list = \
                                                location_geometry_multi_component['polygon']['exteriorRing']['point']
                                            polygon_exteriorRing_feature_geometry.type = 'Polygon'
                                        elif location_geometry_multi_component.get('exteriorRing'):
                                            # building-footprints
                                            polygon_exteriorRing_point_list = \
                                                location_geometry_multi_component['exteriorRing']['point']
                                            polygon_exteriorRing_feature_geometry.type = 'Polygon'
                                        else:
                                            polygon_exteriorRing_point_list = location_geometry_multi_component
                                            polygon_exteriorRing_feature_geometry.type = 'LineString'
                                        if location_geometry_multi_component.get('heightClearance'):
                                            location['heightClearance'] = location_geometry_multi_component.get(
                                                'heightClearance')
                                        if not isinstance(polygon_exteriorRing_point_list, list):
                                            polygon_exteriorRing_point_list = polygon_exteriorRing_point_list.get(
                                                'point')
                                        for polygon_exteriorRing_point in polygon_exteriorRing_point_list:
                                            polygon_exteriorRing_point_lat = polygon_exteriorRing_point['latitude']
                                            polygon_exteriorRing_point_lng = polygon_exteriorRing_point['longitude']
                                            polygon_exteriorRing_feature_geometry_list.append(
                                                [polygon_exteriorRing_point_lng, polygon_exteriorRing_point_lat])
                                        polygon_exteriorRing_feature_geometry.coordinates = [
                                            polygon_exteriorRing_feature_geometry_list]
                                        polygon_exteriorRing_feature.geometry = polygon_exteriorRing_feature_geometry
                                        polygon_exteriorRing_feature.properties = {'polygonType': 'boundary'}
                                        location_element_list.append(polygon_exteriorRing_feature)

                                    del location['geometry']
                                for location_element in location_element_list:
                                    location_element.properties['location'] = location

                                place_list = hmc_json['place']
                                for place in place_list:
                                    place_building_location_identifier = place['locationRef']['identifier']
                                    for location_element in location_element_list:
                                        if location_element.properties['location'][
                                            'identifier'] == place_building_location_identifier:
                                            location_element.properties['place'] = place
                                location_index += 1
                                location_output_list.append(geojson.FeatureCollection(location_element_list))
                            location_process_progressbar.finish()
                            output_geojson.write(
                                json.dumps((geojson.FeatureCollection(location_output_list)), indent='    '))
