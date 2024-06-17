import json

import here.geotiles.heretile as heretile
from here.geotiles.heretile import BoundingBox, GeoCoordinate
from here.platform import Platform

from download_options import FileFormat, HerePlatformCatalog
from hmc_downloader import HmcDownloader


def layer_queueing(layer_id, layer_partitioning_scheme):
    if catalog_layer['partitioningScheme'] == 'heretile':  # Check if the partitioning scheme is 'heretile'
        layers.append(
            {'layer_id': layer_id, 'tiling_scheme': layer_partitioning_scheme})  # Add the layer ID to the layers list
    # else:
    #     print(layer_id, layer_partitioning_scheme)  # Print the layer ID and partitioning scheme
    #     HmcDownloader(catalog=platform_catalog, layer=layer_id,
    #                   file_format=FileFormat.JSON).download_generic_layer()


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

    ### Option: Query by GeoCoordinate
    download_center = GeoCoordinate(lng=119.51073474245146,
                                    lat=23.626448493372244)  # Define the center for geo-coordinate query

    ### Option: Query by bounding box
    south_west = (9.591465308256108, 97.73522936323553)
    north_east = (20.981253503936394, 106.08727704044883)
    download_bounding_box = BoundingBox(west=south_west[1], south=south_west[0], east=north_east[1],
                                        north=north_east[0])  # Define the bounding box for query

    ### Option: Query by tile/partition ID list
    download_quad_id_list = [24134137]  # Define the list of tile/partition IDs for query

    ### Option: Download by ISO COUNTRY CODE (all CAPITAL!)
    country_list_tuple = ('TWN',)  # Define the country code for query

    ### Select one of options above
    download_target = download_center  # Choose the query input (center, bounding box, or tile/partition ID list)

    ### Catalog selection
    catalog = HerePlatformCatalog.HMC_RIB_2  # Choose the catalog for query

    ### List of HERE Tile/Partition ID
    here_quad_longkey_list = []  # Initialize the list to store HERE Tile/Partition IDs

    ### Download Layers (Empty: all layers)
    layers = []  # Initialize the list to store layers for download

    '''
    HMC_RIB_2 layers
    {'layer_id': 'address-locations', 'tiling_scheme': 'heretile'}
    {'layer_id': 'building-footprints', 'tiling_scheme': 'heretile'}
    {'layer_id': '3d-buildings', 'tiling_scheme': 'heretile'}
    {'layer_id': 'cartography', 'tiling_scheme': 'heretile'}
    {'layer_id': 'traffic-patterns', 'tiling_scheme': 'heretile'}
    {'layer_id': 'lane-attributes', 'tiling_scheme': 'heretile'}
    {'layer_id': 'address-attributes', 'tiling_scheme': 'heretile'}
    {'layer_id': 'adas-attributes', 'tiling_scheme': 'heretile'}
    {'layer_id': 'road-attributes', 'tiling_scheme': 'heretile'}
    {'layer_id': 'topology-geometry', 'tiling_scheme': 'heretile'}
    {'layer_id': 'navigation-attributes', 'tiling_scheme': 'heretile'}
    {'layer_id': 'advanced-navigation-attributes', 'tiling_scheme': 'heretile'}
    {'layer_id': 'truck-attributes', 'tiling_scheme': 'heretile'}
    {'layer_id': 'here-places', 'tiling_scheme': 'heretile'}
    {'layer_id': 'distance-markers', 'tiling_scheme': 'heretile'}
    {'layer_id': 'sign-text', 'tiling_scheme': 'heretile'}
    {'layer_id': 'here-places-essential-map', 'tiling_scheme': 'heretile'}
    {'layer_id': 'landmarks-3d', 'tiling_scheme': 'heretile'}
    {'layer_id': 'landmarks-2d', 'tiling_scheme': 'heretile'}
    {'layer_id': 'postal-code-points', 'tiling_scheme': 'heretile'}
    {'layer_id': 'postal-area-boundaries', 'tiling_scheme': 'heretile'}
    {'layer_id': 'electric-vehicle-charging-stations', 'tiling_scheme': 'heretile'}
    {'layer_id': 'electric-vehicle-charging-locations', 'tiling_scheme': 'heretile'}
    {'layer_id': 'here-truck-service-locations', 'tiling_scheme': 'heretile'}
    {'layer_id': 'here-fueling-stations', 'tiling_scheme': 'heretile'}
    {'layer_id': 'generalized-junctions-signs', 'tiling_scheme': 'heretile'}
    {'layer_id': 'enhanced-buildings', 'tiling_scheme': 'heretile'}
    {'layer_id': 'parking-areas', 'tiling_scheme': 'heretile'}
    {'layer_id': 'annotations', 'tiling_scheme': 'heretile'}
    {'layer_id': 'bicycle-attributes', 'tiling_scheme': 'heretile'}
    {'layer_id': 'warning-locations', 'tiling_scheme': 'heretile'}
    {'layer_id': 'complex-road-attributes', 'tiling_scheme': 'heretile'}
    {'layer_id': 'recreational-vehicle-attributes', 'tiling_scheme': 'heretile'}
    '''

    ### Main runner

    level: int  # Initialize the level variable
    hrn: str  # Initialize the hrn variable

    if catalog == HerePlatformCatalog.HMC_RIB_2:
        hrn = 'hrn:here:data::olp-here:rib-2'
        level = 12
    elif catalog == HerePlatformCatalog.HDLM_WEU_2:
        hrn = 'hrn:here:data::olp-here-had:here-hdlm-protobuf-weu-2'
        level = 14
    elif catalog == HerePlatformCatalog.HMC_EXT_REF_2:
        hrn = 'hrn:here:data::olp-here:rib-external-references-2'
        level = 12

    platform_catalog = platform.get_catalog(hrn=hrn)  # Get the platform catalog based on hrn
    if isinstance(download_target, GeoCoordinate):  # Check if the search input is a GeoCoordinate
        here_quad_longkey_list = [heretile.from_coordinates(download_target.lng, download_target.lat,
                                                            level)]  # Get HERE Tile/Partition ID from coordinates
    elif isinstance(download_target, BoundingBox):  # Check if the search input is a BoundingBox
        here_quad_longkey_list = list(
            heretile.in_bounding_box(download_target.west, download_target.south, download_target.east,
                                     download_target.north,
                                     level))  # Get HERE Tile/Partition IDs from bounding box
    elif isinstance(download_target, list):  # Check if the search input is a list
        here_quad_longkey_list = download_quad_id_list  # Use the provided tile/partition ID list
    elif isinstance(download_target, tuple):  # Check if the search input is a tuple
        indexed_locations_layer = 'indexed-locations'  # Define the indexed locations layer
        tile_id_list_per_country = HmcDownloader(catalog=platform_catalog, layer=indexed_locations_layer,
                                                 file_format=FileFormat.JSON).get_country_tile_indexes(
            country_list_tuple)  # Get tile indexes for the specified country
        for tile_id_list in tile_id_list_per_country:  # Iterate through the tile ID lists
            here_quad_longkey_list.append(tile_id_list)  # Add the tile ID lists to the HERE Quad Longkey list

        # HmcDownloader(catalog=platform_catalog, layer=indexed_locations_layer,
        #               file_format=FileFormat.JSON).get_country_admin_indexes(country_list_tuple)

    if len(here_quad_longkey_list) == 0:  # Check if no tile/partition IDs are presented
        print('No tile/partition ID presented, quit.')  # Print message and quit if no tile/partition IDs are presented
    else:
        catalog_detail = json.loads(json.dumps(platform_catalog.get_details()))  # Get and parse catalog details
        catalog_layers = catalog_detail['layers']  # Get the catalog layers
        print('Available layers: ')
        for catalog_layer in catalog_layers:  # Iterate through the catalog layers
            print('* {} | {} | {} | {}'.format(catalog_layer['id'], catalog_layer['name'], catalog_layer['hrn'],
                                               catalog_layer['tags']))

        if len(layers) == 0:  # Check if no layers are specified
            for catalog_layer in catalog_layers:  # Iterate through the catalog layers
                if catalog_layer['partitioningScheme'] == 'heretile':  # Check if the partitioning scheme is 'heretile'
                    layer_queueing(catalog_layer['id'], catalog_layer['partitioningScheme'])

        print('download layers:', layers)  # Print the layers for download
        for layer in layers:  # Iterate through the layers for download
            print('* Downloading {}'.format(layer['layer_id']))
            HmcDownloader(catalog=platform_catalog, layer=layer['layer_id'],
                          file_format=FileFormat.JSON).download_partitioned_layer(
                quad_ids=here_quad_longkey_list)  # Download the data for the specified layer and HERE Quad Longkey list
