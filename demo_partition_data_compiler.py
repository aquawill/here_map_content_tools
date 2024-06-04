import os

partition_path = r'decoded/hrn_here_data__olp-here_rib-2/'
overwrite = 'y'

os.system('echo running "python hmc_topology_to_geojson.py {} {}"'.format(partition_path, overwrite))
os.system('python hmc_topology_to_geojson.py {} {}"'.format(partition_path, overwrite))

os.system('echo running "python hmc_road_based_attributes_to_geojson.py {}"'.format(partition_path))
os.system('python hmc_road_based_attributes_to_geojson.py {} {}"'.format(partition_path, overwrite))

os.system('echo running "python hmc_address_locations_to_geojson.py {}"'.format(partition_path))
os.system('python hmc_address_locations_to_geojson.py {} {}"'.format(partition_path, overwrite))

os.system('echo running "python hmc_polygon_to_geojson.py {}"'.format(partition_path))
os.system('python hmc_polygon_to_geojson.py {} {}"'.format(partition_path, overwrite))

os.system('echo running "python hmc_places_to_geojson.py {}"'.format(partition_path))
os.system('python hmc_places_to_geojson.py {} {}"'.format(partition_path, overwrite))

os.system('echo running "python hmc_enhanced_buildings_to_geojson.py {}"'.format(partition_path))
os.system('python hmc_enhanced_buildings_to_geojson.py {} {}"'.format(partition_path, overwrite))

os.system('echo running "python hmc_postal_code_points_to_geojson.py {}"'.format(partition_path))
os.system('python hmc_postal_code_points_to_geojson.py {} {}"'.format(partition_path, overwrite))

os.system('echo running "python hmc_landmarks_to_geojson.py {}"'.format(partition_path))
os.system('python hmc_landmarks_to_geojson.py {} {}"'.format(partition_path, overwrite))

os.system('python hmc_parking_areas_to_geojson.py {}"'.format(partition_path))

os.system('echo running "python hmc_postal_code_points_to_geojson.py {}"'.format(partition_path))
os.system('python hmc_postal_code_points_to_geojson.py {} {}"'.format(partition_path, overwrite))

os.system('echo running "python hmc_lane_attributes_to_geojson.py {}"'.format(partition_path))
os.system('python hmc_lane_attributes_to_geojson.py {} {}"'.format(partition_path, overwrite))

os.system('echo running "python hmc_evcp_v2_to_geojson.py {}"'.format(partition_path))
os.system('python hmc_evcp_v2_to_geojson.py {} {}"'.format(partition_path, overwrite))
