"""
This code defines a class HmcDownloader that is responsible for downloading
and processing data from the HERE platform. It provides methods to retrieve
schema, download data, and extract country tile and admin indexes.
"""
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
        super().__init__()  # Initialize the class with the provided catalog, layer, and file format
        self.catalog = catalog
        self.layer = layer
        self.file_format = file_format

    def get_schema(self):
        return self.catalog.get_layer(self.layer).get_schema()  # Retrieve the schema for the specified layer

    def download(self, quad_ids: list) -> dict:
        versioned_layer = self.catalog.get_layer(self.layer)  # Get the versioned layer for the specified layer
        partitions = versioned_layer.read_partitions(quad_ids)  # Read partitions for the specified quad IDs
        for p in partitions:
            versioned_partition, partition_content = p  # Unpack the versioned partition and partition content
            hrn_folder_name = self.catalog.hrn.replace(':', '_')  # Replace ':' with '_' in the catalog HRN
            extension: str
            if self.file_format == FileFormat.TXTBP:  # Check the file format and set the extension accordingly
                extension = 'txtbp'
            elif self.file_format == FileFormat.JSON:
                extension = 'json'
            filename = os.path.join('decoded', hrn_folder_name, str(versioned_partition.id),  # Construct the filename
                                    '{}_{}_v{}.{}'.format(self.layer, versioned_partition.id,
                                                          versioned_partition.version, extension))
            if not os.path.exists(filename):  # Check if the file already exists
                if not os.path.exists('decoded'):  # Create 'decoded' directory if it doesn't exist
                    os.mkdir('decoded')
                if not os.path.exists(
                        os.path.join('decoded', hrn_folder_name)):  # Create HRN directory if it doesn't exist
                    os.mkdir(os.path.join('decoded', hrn_folder_name))
                if not os.path.exists(os.path.join('decoded', hrn_folder_name,
                                                   str(versioned_partition.id))):  # Create partition directory if it doesn't exist
                    os.mkdir(os.path.join('decoded', hrn_folder_name, str(versioned_partition.id)))
                print('layer: {} | partition: {} | version: {} | size: {} bytes'.format(self.layer,
                                                                                        # Print information about the layer, partition, version, and size
                                                                                        versioned_partition.id,
                                                                                        versioned_partition.version,
                                                                                        versioned_partition.data_size))
                decoded_content = DecodedMessage(partition_content)  # Decode the partition content
                with open(filename, mode='w', encoding='utf-8') as output:  # Open the file for writing
                    content_to_write: str
                    if self.file_format == FileFormat.TXTBP:  # Check the file format and set the content to write accordingly
                        content_to_write = str(decoded_content)
                    elif self.file_format == FileFormat.JSON:
                        content_to_write = MessageToJson(decoded_content)
                    output.write(content_to_write)  # Write the content to the file
                    return {'filename': filename, 'result': 'created'}  # Return the filename and result as 'created'
            else:
                return {'filename': filename, 'result': 'skipped'}  # Return the filename and result as 'skipped'

    def get_country_tile_indexes(self, iso_country_code_tuple: tuple):
        layer = self.catalog.get_layer(self.layer)  # Get the layer for the specified layer
        partitions = layer.read_partitions(
            iso_country_code_tuple)  # Read partitions for the specified ISO country code tuple
        results = []
        for p in partitions:
            versioned_partition, partition_content = p  # Unpack the versioned partition and partition content
            decoded_content_json = json.loads(
                MessageToJson(DecodedMessage(partition_content)))  # Decode the partition content to JSON
            results.append({decoded_content_json['partitionName']: decoded_content_json[
                'tileId']})  # Append partition name and tile ID to results
        return results  # Return the results

    def get_country_admin_indexes(self, iso_country_code_tuple: tuple):
        layer = self.catalog.get_layer(self.layer)  # Get the layer for the specified layer
        partitions = layer.read_partitions(
            iso_country_code_tuple)  # Read partitions for the specified ISO country code tuple
        results = []
        for p in partitions:
            versioned_partition, partition_content = p  # Unpack the versioned partition and partition content
            hmc_json = json.loads(
                MessageToJson(DecodedMessage(partition_content)))  # Decode the partition content to JSON
            tile_id_list = hmc_json['tileId']  # Get the tile ID list from the JSON
            indexed_location_list = hmc_json['indexedLocation']  # Get the indexed location list from the JSON
            for indexed_location in indexed_location_list:
                indexed_location_tile_index_list = indexed_location[
                    'tileIndex']  # Get the tile index list from the indexed location
                indexed_location_boundary_tile_index_list = indexed_location[
                    'boundaryTileIndex']  # Get the boundary tile index list from the indexed location
                del indexed_location['tileIndex']  # Delete the tile index from the indexed location
                del indexed_location['boundaryTileIndex']  # Delete the boundary tile index from the indexed location
                indexed_location['partitionIdList'] = []  # Initialize the partition ID list in the indexed location
                indexed_location[
                    'boundaryPartitionIdList'] = []  # Initialize the boundary partition ID list in the indexed location
                for indexed_location_tile_index in indexed_location_tile_index_list:
                    indexed_location['partitionIdList'].append(
                        tile_id_list[indexed_location_tile_index])  # Append partition ID to the partition ID list
                for indexed_location_boundary_tile_index in indexed_location_boundary_tile_index_list:
                    indexed_location['boundaryPartitionIdList'].append(
                        # Append boundary partition ID to the boundary partition ID list
                        tile_id_list[indexed_location_boundary_tile_index])
            hmc_json['indexedLocation'] = indexed_location_list  # Update the indexed location list in the HMC JSON
            print(json.dumps(hmc_json, indent='    '))  # Print the formatted HMC JSON
        return results  # Return the results
