import os

partition_id = 24125363
partition_path = r'decoded/hrn_here_data__olp-here_rib-2/{}'.format(partition_id)

os.system('python hmc_topology_to_geojson.py {}'.format(partition_path))
os.system('python hmc_road_based_attributes_to_geojson.py {}'.format(partition_path))
os.system('python hmc_polygon_to_geojson.py {}'.format(partition_path))
os.system('python hmc_places_to_geojson.py {}'.format(partition_path))
os.system('python hmc_address_locations_to_geojson.py {}'.format(partition_path))
os.system('python hmc_enhanced_buildings_to_geojson.py {}'.format(partition_path))
os.system('python hmc_postal_code_points_to_geojson.py {}'.format(partition_path))
os.system('python hmc_landmarks_to_geojson.py {}'.format(partition_path))
os.system('python hmc_parking_areas_to_geojson.py {}'.format(partition_path))
os.system('python hmc_postal_code_points_to_geojson.py {}'.format(partition_path))
os.system('python hmc_lane_attributes_to_geojson.py {}'.format(partition_path))
