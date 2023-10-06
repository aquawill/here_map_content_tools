import json
import os
from google.protobuf.json_format import MessageToJson

from here.platform import Platform
from here.platform import adapter

# home_path = os.path.expanduser(os.getenv('USERPROFILE'))
#
# platform_cred = PlatformCredentials.from_credentials_file(os.path.join(home_path, '.here', 'credentials.properties'))
# platform_obj = Platform(platform_cred)

# platform = Platform(credentials=platform_cred, environment=Environment.DEFAULT)

platform = Platform()
env = platform.environment
config = platform.platform_config
status = platform.get_status()
print(status)
hrn = 'hrn:here:data::olp-here-had:here-hdlm-protobuf-weu-2'
catalog = platform.get_catalog(hrn=hrn)
catalog_detail = json.loads(json.dumps(catalog.get_details()))

partition_ids = [377893071]

layers = catalog_detail['layers']
for layer in layers:
    if layer['partitioningScheme'] == 'heretile' and layer['layerType'] == 'versioned':
        print(layer['id'])
        versioned_layer = catalog.get_layer(layer['id'])
        partitions = versioned_layer.read_partitions(partition_ids=partition_ids)
        for p in partitions:
            versioned_partition, partition_content = p
            print(f"{versioned_partition.id}: {type(partition_content)}")
            decoded_content = adapter.DecodedMessage(partition_content)
            decoded_content_json = MessageToJson(decoded_content)
            if not os.path.exists('decoded_tile'):
                os.mkdir('decoded_tile')
            if not os.path.exists(os.path.join('decoded_tile', str(versioned_partition.id))):
                os.mkdir(os.path.join('decoded_tile', str(versioned_partition.id)))
            with open(os.path.join('decoded_tile', str(versioned_partition.id),
                                   f"{versioned_partition.id}_{layer['id']}.json"), mode='w',
                      encoding='utf-8') as output:
                output.write(decoded_content_json)
