@echo on
set python=%cd%\venv\Scripts\python.exe

%python% hmc_topology_to_geojson.py decoded/hrn_here_data__olp-here_rib-2/
%python% hmc_road_based_attributes_to_geojson.py decoded/hrn_here_data__olp-here_rib-2/
%python% hmc_places_to_geojson.py decoded/hrn_here_data__olp-here_rib-2/
%python% hmc_address_locations_to_geojson.py decoded/hrn_here_data__olp-here_rib-2/
%python% hmc_polygon_to_geojson.py decoded/hrn_here_data__olp-here_rib-2/
%python% hmc_enhanced_buildings_to_geojson.py decoded/hrn_here_data__olp-here_rib-2/
%python% hmc_postal_code_points_to_geojson.py decoded/hrn_here_data__olp-here_rib-2/
%python% hmc_landmarks_to_geojson.py decoded/hrn_here_data__olp-here_rib-2/
%python% hmc_parking_areas_to_geojson.py decoded/hrn_here_data__olp-here_rib-2/
%python% hmc_postal_code_points_to_geojson.py decoded/hrn_here_data__olp-here_rib-2/
%python% hmc_lane_attributes_to_geojson.py decoded/hrn_here_data__olp-here_rib-2/
