import json
import os
from enum import Enum

from google.protobuf.json_format import MessageToJson
from here.platform import Platform
from here.platform.adapter import DecodedMessage
from mapquadlib.herequad import HereQuad


class QueryType(Enum):
    LAT_LNG = 1  # Latitude and Longitude
    QUAD_LONGKEY_ID = 2  # ID of RIB2 Partition or HDLM Tile


class HerePlatformCatalog(Enum):
    HDLM = 1
    RIB2 = 2


def get_layer_partition_contents(layer):
    versioned_layer = catalog.get_layer(layer)
    partitions = versioned_layer.read_partitions(partition_ids=here_quad_longkey_list)
    for p in partitions:
        versioned_partition, partition_content = p
        hrn_folder_name = catalog.hrn.replace(':', '_')
        filename = os.path.join('decoded', hrn_folder_name, str(versioned_partition.id),
                                '{}_{}_v{}.json'.format(layer, versioned_partition.id,
                                                        versioned_partition.version))
        if not os.path.exists(filename):
            if not os.path.exists('decoded'):
                os.mkdir('decoded')
            if not os.path.exists(os.path.join('decoded', hrn_folder_name)):
                os.mkdir(os.path.join('decoded', hrn_folder_name))
            if not os.path.exists(os.path.join('decoded', hrn_folder_name, str(versioned_partition.id))):
                os.mkdir(os.path.join('decoded', hrn_folder_name, str(versioned_partition.id)))
            print('layer: {} | partition: {} | version: {} | size: {} bytes'.format(layer,
                                                                                    versioned_partition.id,
                                                                                    versioned_partition.version,
                                                                                    versioned_partition.data_size))
            decoded_content = DecodedMessage(partition_content)
            decoded_content_json = MessageToJson(decoded_content)
            with open(filename, mode='w', encoding='utf-8') as output:
                output.write(decoded_content_json)
        else:
            print(filename, '--> skipped')


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

    ### Query by Lat/Lng or Tile/Partiion LONGKEY ID
    query_type = QueryType.LAT_LNG

    search_location = {'lat': 52.52507, 'lng': 13.36937}

    ### Catalog selection
    catalog = HerePlatformCatalog.RIB2

    ### List of HERE Tile/Partition ID
    here_quad_longkey_list = []

    ### Download Layers (Empty: all layers)
    layers = []
    if query_type == QueryType.LAT_LNG:
        if catalog == HerePlatformCatalog.RIB2:
            hrn = 'hrn:here:data::olp-here:rib-2'
            zoom = 12
            partition_id = HereQuad.from_lat_lng_level(search_location['lat'], search_location['lng'], zoom).long_key
            here_quad_longkey_list.append(partition_id)
        elif catalog == HerePlatformCatalog.HDLM:
            hrn = 'hrn:here:data::olp-here-had:here-hdlm-protobuf-weu-2'
            zoom = 14
            tile_id = HereQuad.from_lat_lng_level(search_location['lat'], search_location['lng'], zoom).long_key
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
            get_layer_partition_contents(layer)
