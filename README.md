# HERE Map Content (HMC) Tools
## Developed with [HERE Data SDK Python V2](https://www.here.com/docs/bundle/data-sdk-for-python-developer-guide-v2/page/README.html)

### Prerequisites:

You will need a complete set of configuration to access HERE Map Content: Account, App, Project, credential and SDK.

1. Create account of HERE Platform https://platform.here.com/portal/.
2. Create new project in https://platform.here.com/management/projects/.
3. Create new app in https://platform.here.com/admin/apps.
4. Grant access of project to app to project created at step 3.
5. Link catalogs you need to project created at step 2.
   * `hrn:here:data::olp-here:rib-2`
   * `hrn:here:data::olp-here:rib-external-references-2`
6. Obtain OAuth credential of App, download credentials.properties file.
7. Follow the [instruction](https://www.here.com/docs/bundle/data-sdk-for-python-developer-guide-v2/page/topics/install.html) to install HERE Data SDK for Python V2.
8. Make sure credentials.properties has been placed to correct path.

### 先決條件：

在使用 HERE Map Content 之前，您需要一套完整的設定：帳戶、應用程式、專案、憑證和軟體開發工具（SDK）。

1. 在 [HERE平台](https://platform.here.com/portal/) 上建立帳戶。
2. 在 [HERE平台專案管理](https://platform.here.com/management/projects/) 中建立新專案。
3. 在 [HERE平台應用管理](https://platform.here.com/admin/apps) 中建立新應用程式。
4. 將專案的存取權授予在第 3 步中建立的應用程式。
5. 將您需要的目錄連結到在第 2 步中建立的專案。
   - `hrn:here:data::olp-here:rib-2`
   - `hrn:here:data::olp-here:rib-external-references-2`
6. 獲取應用程式的 OAuth憑 證，並下載`credentials.properties`檔案。
7. 按照 [此說明](https://www.here.com/docs/bundle/data-sdk-for-python-developer-guide-v2/page/topics/install.html) 安裝HERE Data SDK for Python V2。
8. 確保`credentials.properties`已放置在正確的路徑下。

### Main programs:

* **`demo_download_hmc_tiles.py`**: downloading HMC partitions from HERE Platform.
* **`demo_partition_data_compiler.py / demo_partition_data_compiler.bat`**: convert all layers of partition to geojson.
* **`hmc_downloader.py`**: HmcDownloader class

### 主程式：

- **`demo_download_hmc_tiles.py`**：從 HERE 平台下載 HMC 分區。
- **`demo_partition_data_compiler.py` / `demo_partition_data_compiler.bat`**：將分區的所有圖層轉換為geojson格式。
- **`hmc_downloader.py`**：`HmcDownloader`類別。

### Misc. tools:

* **`here_quad_list_from_geojson.py`**: get list of tile and wkt from geojson geometries.
* **`lat_lng_to_quad.py`**: get tile quadkey from latitude and longitude.
* **`proto_schema_compiler.py`**: compile protocol buffer schema documents.
* **`hdlm_coord_converter.py`**: convert between HDLM coordinates and WGS84 lat/lng.

### 其他工具：

* **`here_quad_list_from_geojson.py`**：從 geojson 幾何圖形中獲取 Partition/Tile 和 WKT 列表。
* **`lat_lng_to_quad.py`**：從緯度和經度中算出 Partition/tile QuadKey。
* **`proto_schema_compiler.py`**：編譯 PROTOCOL BUFFER 文件。
* **`hdlm_coord_converter.py`**：在 HDLM 座標和 WGS84 緯度/經度之間進行轉換。

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

![](https://i.imgur.com/Ers08wq.jpeg)