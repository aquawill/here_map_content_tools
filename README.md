# HERE Map Content (HMC) Downloader
## Developed with [HERE Data SDK Python V2](https://www.here.com/docs/bundle/data-sdk-for-python-developer-guide-v2/page/README.html)

### Executables:
* demo.py: demonstration of downloading HMC from HERE Platform.
* here_quad_list_from_geojson.py: get list of tile and wkt from geojson geometries.
* here_quad_list_generator.py: get list of tlie and wkt from bounding box.
* hmc_downloader.py: HmcDownloader class to download HMC and write raw or decoded contents.
* lat_lng_to_quad.py: get tile quadkey from latitude and longitude.
* proto_schema_compiler.py: compile protocal buffer schema documents.
* hdlm_coord_converter.py: convert between HDLM coordinates and lat/lng.
* hmc_places_to_geojson.py: convert HMC places to geojson.
* hmc_topology_to_geojson.py: convert HMC topology geometry to geojson.
* more to come...

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

### Convert HMC attributes to GeoJSON.
* advanced-navigation-attributes
* complex-road-attributes
* navigation-attributes
* road-attributes
* traffic-patterns

![](https://i.imgur.com/vhn0pyS.jpeg)