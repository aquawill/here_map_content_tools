import json

import here.geotiles.heretile as heretile
from here.geotiles.heretile import BoundingBox, GeoCoordinate
from here.platform import Platform

from download_options import FileFormat, HerePlatformCatalog
from hmc_downloader import HmcDownloader

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
    download_center = GeoCoordinate(lng=9.529149391682209, lat=51.27567430514518)  # Define the center for geo-coordinate query

    ### Option: Query by bounding box
    south_west = (9.591465308256108, 97.73522936323553)
    north_east = (20.981253503936394, 106.08727704044883)
    download_bounding_box = BoundingBox(west=south_west[1], south=south_west[0], east=north_east[1],
                                        north=north_east[0])  # Define the bounding box for query

    ### Option: Query by tile/partition ID list
    download_quad_id_list = [24318368]  # Define the list of tile/partition IDs for query

    ### Option: Download by ISO COUNTRY CODE (all CAPITAL!)
    country_list_tuple = ('TWN',)  # Define the country code for query

    ### Select one of options above
    search_input = download_center  # Choose the query input (center, bounding box, or tile/partition ID list)

    ### Catalog selection
    catalog = HerePlatformCatalog.RIB2  # Choose the catalog for query

    ### List of HERE Tile/Partition ID
    here_quad_longkey_list = []  # Initialize the list to store HERE Tile/Partition IDs

    ### Download Layers (Empty: all layers)
    layers = []  # Initialize the list to store layers for download

    ### Main runner

    level: int  # Initialize the level variable
    hrn: str  # Initialize the hrn variable

    if catalog == HerePlatformCatalog.RIB2:  # Check if the catalog is RIB2
        hrn = 'hrn:here:data::olp-here:rib-2'  # Set the hrn for RIB2
        level = 12  # Set the level for RIB2
    elif catalog == HerePlatformCatalog.HDLM:  # Check if the catalog is HDLM
        hrn = 'hrn:here:data::olp-here-had:here-hdlm-protobuf-weu-2'  # Set the hrn for HDLM
        level = 14  # Set the level for HDLM

    platform_catalog = platform.get_catalog(hrn=hrn)  # Get the platform catalog based on hrn
    if isinstance(search_input, GeoCoordinate):  # Check if the search input is a GeoCoordinate
        here_quad_longkey_list = [heretile.from_coordinates(search_input.lng, search_input.lat, level)]  # Get HERE Tile/Partition ID from coordinates
    elif isinstance(search_input, BoundingBox):  # Check if the search input is a BoundingBox
        here_quad_longkey_list = list(heretile.in_bounding_box(search_input.west, search_input.south, search_input.east,
                                                               search_input.north, level))  # Get HERE Tile/Partition IDs from bounding box
    elif isinstance(search_input, list):  # Check if the search input is a list
        here_quad_longkey_list = download_quad_id_list  # Use the provided tile/partition ID list
    elif isinstance(search_input, tuple):  # Check if the search input is a tuple
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
        print('Available layers: ')  # Print message
        for catalog_layer in catalog_layers:  # Iterate through the catalog layers
            print('\t', catalog_layer['id'])  # Print the catalog layer ID

        if len(layers) == 0:  # Check if no layers are specified
            for catalog_layer in catalog_layers:  # Iterate through the catalog layers
                if catalog_layer['partitioningScheme'] == 'heretile':  # Check if the partitioning scheme is 'heretile'
                    layers.append(catalog_layer['id'])  # Add the layer ID to the layers list
                else:
                    print('\t', catalog_layer['id'], catalog_layer['partitioningScheme'])  # Print the layer ID and partitioning scheme
        print('download layers:', layers)  # Print the layers for download
        for layer in layers:  # Iterate through the layers for download
            result = HmcDownloader(catalog=platform_catalog, layer=layer,
                                   file_format=FileFormat.JSON).download(quad_ids=here_quad_longkey_list)  # Download the data for the specified layer and HERE Quad Longkey list
            if not result:  # Check if the download result is empty
                print('* {} --> layer unavailable'.format(layer))  # Print message for unavailable layer
            else:
                print('* {} --> {}'.format(layer, result))  # Print the layer and download result
