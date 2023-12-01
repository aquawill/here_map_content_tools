# HERE Map Content (HMC) Tools
## Developed with [HERE Data SDK Python V2](https://www.here.com/docs/bundle/data-sdk-for-python-developer-guide-v2/page/README.html)

### Main programs:

* **demo_download_hmc_tiles.py**: downloading HMC partitions from HERE Platform.
* **demo_partition_data_compiler.py**: convert all layers of partition to geojson.
* **hmc_downloader.py**: HmcDownloader class

### Misc. tools:

* **here_quad_list_from_geojson.py**: get list of tile and wkt from geojson geometries.
* **lat_lng_to_quad.py**: get tile quadkey from latitude and longitude.
* **proto_schema_compiler.py**: compile protocal buffer schema documents.
* **hdlm_coord_converter.py**: convert between HDLM coordinates and lat/lng.

## Screenshots

### Get partition/tile of specific geometries.
![](https://i.imgur.com/dtDWMHl.png)

### HMC schema in JSON.
![](https://i.imgur.com/zolDmWJ.png)

### Download HMC partition/tile.
![](https://i.imgur.com/PRP23vk.png)

### Convert HMC Places (here-places) to GeoJSON.
![](https://i.imgur.com/vPvITdB.png)

### Convert HMC Topology Geometry (topology-geometry) to GeoJSON.
![](https://i.imgur.com/7EFdYm6.jpeg)

### Convert HMC Polygonal Geometry (topology-geometry) to GeoJSON.
![](https://i.imgur.com/99KpolE.jpeg)

### Convert HMC Address Locations to GeoJSON.
![](https://i.imgur.com/1L8Z2oi.png)

### Convert HMC Enhanced Buildings to geoJSON.

![](https://i.imgur.com/zmDPu7v.jpeg)

### Convert HMC attributes to GeoJSON.
* hmc_lane_attributes_to_geojson.py
* hmc_enhanced_buildings_to_geojson.py
* hmc_address_locations_to_geojson.py
* hmc_landmarks_to_geojson.py
* hmc_parking_areas_to_geojson.py
* hmc_places_to_geojson.py
* hmc_polygon_to_geojson.py
* hmc_postal_code_points_to_geojson.py
* hmc_road_based_attributes_to_geojson.py
* hmc_topology_to_geojson.py

![](https://i.imgur.com/C5pZHrY.jpeg)

![](https://i.imgur.com/N9cNU7o.jpeg)

![](https://i.imgur.com/VY7Wj1t.jpeg)

![](https://i.imgur.com/rWWKf5l.jpeg)

![](https://i.imgur.com/1R4JuJS.jpeg)

![](https://i.imgur.com/bWKH77R.jpeg)

![](https://i.imgur.com/1wmeRuj.jpeg)

