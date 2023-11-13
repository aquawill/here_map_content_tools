import json

import here.geotiles.heretile as heretile
from here.platform import Platform

from download_options import FileFormat, HerePlatformCatalog, QueryType
from hmc_tile_downloader import HmcTileDownloader

if __name__ == '__main__':
    ### Customized configurations
    # home_path = os.path.expanduser(os.getenv('USERPROFILE'))
    # platform_cred = PlatformCredentials.from_credentials_file(os.path.join(home_path, '.here', 'credentials.properties'))
    # platform_obj = Platform(platform_cred)
    # platform = Platform(credentials=platform_cred, environment=Environment.DEFAULT)

    ### Platform SDK initialization
    platform = Platform()
    env = platform.environment
    config = platform.platform_config
    print('HERE Platform Status: ', platform.get_status())

    ### Query by Lat/Lng or Tile/Partition LONGKEY ID
    query_type = QueryType.LAT_LNG

    search_location = {'lat': 49.00839, 'lng': 8.41036}

    ### Catalog selection
    catalog = HerePlatformCatalog.RIB2

    ### List of HERE Tile/Partition ID
    here_quad_longkey_list = []

    ### Download Layers (Empty: all layers)
    layers = ['topology-geometry']

    ### Main runner
    if query_type == QueryType.LAT_LNG:
        if catalog == HerePlatformCatalog.RIB2:
            hrn = 'hrn:here:data::olp-here:rib-2'
            zoom = 12
            partition_id = heretile.from_coordinates(search_location['lng'], search_location['lat'], zoom)
            here_quad_longkey_list.append(partition_id)
        elif catalog == HerePlatformCatalog.HDLM:
            hrn = 'hrn:here:data::olp-here-had:here-hdlm-protobuf-weu-2'
            zoom = 14
            tile_id = heretile.from_lat_lng_level(search_location['lng'], search_location['lat'], zoom)
            here_quad_longkey_list.append(tile_id)

    if len(here_quad_longkey_list) == 0:
        print('No tile/partition ID presented, quit.')
    else:
        catalog = platform.get_catalog(hrn=hrn)
        catalog_detail = json.loads(json.dumps(catalog.get_details()))
        catalog_layers = catalog_detail['layers']
        if len(layers) == 0:
            for catalog_layer in catalog_layers:
                if catalog_layer['partitioningScheme'] == 'heretile':
                    layers.append(catalog_layer['id'])
        print('layers', layers)
        for layer in layers:
            HmcTileDownloader(catalog=catalog, layer=layer, tile_ids=here_quad_longkey_list,
                              file_format=FileFormat.JSON).download()
