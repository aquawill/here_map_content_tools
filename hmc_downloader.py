import json
import os

from google.protobuf.json_format import MessageToJson
from here.platform.adapter import DecodedMessage
from here.platform.catalog import Catalog
from here.content.hmc2.hmc import HMC

from download_options import FileFormat


class HmcDownloader:
    catalog: Catalog
    layer: str = ''
    quad_ids: list
    file_format: FileFormat

    def __init__(self, catalog: Catalog, layer: str, file_format: FileFormat) -> None:
        super().__init__()
        self.catalog = catalog
        self.layer = layer
        self.file_format = file_format

    def get_schema(self):
        versioned_layer = self.catalog.get_layer(self.layer).get_schema()

    def download(self, quad_ids: list) -> dict:
        versioned_layer = self.catalog.get_layer(self.layer)
        partitions = versioned_layer.read_partitions(quad_ids)
        for p in partitions:
            versioned_partition, partition_content = p
            hrn_folder_name = self.catalog.hrn.replace(':', '_')
            extension: str
            if self.file_format == FileFormat.TXTBP:
                extension = 'txtbp'
            elif self.file_format == FileFormat.JSON:
                extension = 'json'
            filename = os.path.join('decoded', hrn_folder_name, str(versioned_partition.id),
                                    '{}_{}_v{}.{}'.format(self.layer, versioned_partition.id,
                                                          versioned_partition.version, extension))
            if not os.path.exists(filename):
                if not os.path.exists('decoded'):
                    os.mkdir('decoded')
                if not os.path.exists(os.path.join('decoded', hrn_folder_name)):
                    os.mkdir(os.path.join('decoded', hrn_folder_name))
                if not os.path.exists(os.path.join('decoded', hrn_folder_name, str(versioned_partition.id))):
                    os.mkdir(os.path.join('decoded', hrn_folder_name, str(versioned_partition.id)))
                print('layer: {} | partition: {} | version: {} | size: {} bytes'.format(self.layer,
                                                                                        versioned_partition.id,
                                                                                        versioned_partition.version,
                                                                                        versioned_partition.data_size))
                decoded_content = DecodedMessage(partition_content)
                with open(filename, mode='w', encoding='utf-8') as output:
                    content_to_write: str
                    if self.file_format == FileFormat.TXTBP:
                        content_to_write = str(decoded_content)
                    elif self.file_format == FileFormat.JSON:
                        content_to_write = MessageToJson(decoded_content)
                    output.write(content_to_write)
                    return {'filename': filename, 'result': 'created'}
            else:
                return {'filename': filename, 'result': 'skipped'}

    def get_country_tile_indexes(self, iso_country_code_tuple: tuple):
        layer = self.catalog.get_layer(self.layer)
        partitions = layer.read_partitions(iso_country_code_tuple)
        results = []
        for p in partitions:
            versioned_partition, partition_content = p
            decoded_content_json = json.loads(MessageToJson(DecodedMessage(partition_content)))
            results.append({decoded_content_json['partitionName']: decoded_content_json['tileId']})
        return results

    def get_country_admin_indexes(self, iso_country_code_tuple: tuple):
        layer = self.catalog.get_layer(self.layer)
        partitions = layer.read_partitions(iso_country_code_tuple)
        results = []
        for p in partitions:
            versioned_partition, partition_content = p
            hmc_json = json.loads(MessageToJson(DecodedMessage(partition_content)))
            tile_id_list = hmc_json['tileId']
            indexed_location_list = hmc_json['indexedLocation']
            for indexed_location in indexed_location_list:
                indexed_location_tile_index_list = indexed_location['tileIndex']
                indexed_location_boundary_tile_index_list = indexed_location['boundaryTileIndex']
                del indexed_location['tileIndex']
                del indexed_location['boundaryTileIndex']
                indexed_location['partitionIdList'] = []
                indexed_location['boundaryPartitionIdList'] = []
                for indexed_location_tile_index in indexed_location_tile_index_list:
                    indexed_location['partitionIdList'].append(tile_id_list[indexed_location_tile_index])
                for indexed_location_boundary_tile_index in indexed_location_boundary_tile_index_list:
                    indexed_location['boundaryPartitionIdList'].append(
                        tile_id_list[indexed_location_boundary_tile_index])
            hmc_json['indexedLocation'] = indexed_location_list
            print(json.dumps(hmc_json, indent='    '))
        return results
