import os

from google.protobuf.json_format import MessageToJson
from here.platform.adapter import DecodedMessage
from here.platform.catalog import Catalog

from download_options import FileFormat


class HmcDownloader:
    catalog: Catalog
    layer: str = ''
    quad_ids: list
    file_format: FileFormat

    def __init__(self, catalog: Catalog, layer: str, quad_ids: list, file_format: FileFormat) -> None:
        super().__init__()
        self.catalog = catalog
        self.layer = layer
        self.quad_ids = quad_ids
        self.file_format = file_format

    def get_schema(self):
        versioned_layer = self.catalog.get_layer(self.layer).get_schema()

    def download(self) -> dict:
        versioned_layer = self.catalog.get_layer(self.layer)
        partitions = versioned_layer.read_partitions(partition_ids=self.quad_ids)
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
