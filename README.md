# HERE Map Content (HMC) Tools
## Developed with [HERE Data SDK Python V2](https://www.here.com/docs/bundle/data-sdk-for-python-developer-guide-v2/page/README.html)

### Prerequisites:

You will need a complete set of configuration to access HERE Map Content: Account, App, Project, credential and SDK.

1. Create account of HERE Platform https://platform.here.com/portal/.
2. Create new project in https://platform.here.com/management/projects/.
3. Create new app in https://platform.here.com/admin/apps.
4. Grant access of project to app to project created at step 3.
5. Link catalogs you need to project created at step 2.
   * hrn:here:data::olp-here:rib-2
   * hrn:here:data::olp-here:rib-external-references-2
6. Obtain OAuth credential of App, download credentials.properties file.
7. Follow the [instruction](https://www.here.com/docs/bundle/data-sdk-for-python-developer-guide-v2/page/topics/install.html) to install HERE Data SDK for Python V2.
8. Make sure credentials.properties has been placed to correct path.

### Main programs:

* **demo_download_hmc_tiles.py**: downloading HMC partitions from HERE Platform.
* **demo_partition_data_compiler.py**: convert all layers of partition to geojson.
* **hmc_downloader.py**: HmcDownloader class

### Misc. tools:

* **here_quad_list_from_geojson.py**: get list of tile and wkt from geojson geometries.
* **lat_lng_to_quad.py**: get tile quadkey from latitude and longitude.
* **proto_schema_compiler.py**: compile protocol buffer schema documents.
* **hdlm_coord_converter.py**: convert between HDLM coordinates and WGS84 lat/lng.

## Screenshots

![](https://i.imgur.com/dtDWMHl.png)

![](https://i.imgur.com/zolDmWJ.png)

![](https://i.imgur.com/PRP23vk.png)

![](https://i.imgur.com/MmmZtOv.png)

![](https://i.imgur.com/vPvITdB.png)

![](https://i.imgur.com/7EFdYm6.jpeg)

![](https://i.imgur.com/99KpolE.jpeg)

![](https://i.imgur.com/1L8Z2oi.png)

![](https://i.imgur.com/zmDPu7v.jpeg)

![](https://i.imgur.com/C5pZHrY.jpeg)

![](https://i.imgur.com/N9cNU7o.jpeg)

![](https://i.imgur.com/VY7Wj1t.jpeg)

![](https://i.imgur.com/rWWKf5l.jpeg)

![](https://i.imgur.com/1R4JuJS.jpeg)

![](https://i.imgur.com/bWKH77R.jpeg)

![](https://i.imgur.com/1wmeRuj.jpeg)

![](https://i.imgur.com/3fFwMQx.jpeg)

