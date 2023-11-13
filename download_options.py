from enum import Enum


class FileFormat(Enum):
    JSON = 1
    TXTBP = 2


class QueryType(Enum):
    LAT_LNG = 1  # Latitude and Longitude
    QUAD_ID = 2  # ID of RIB2 Partition or HDLM Tile
    QUAD_LIST = 3


class HerePlatformCatalog(Enum):
    HDLM = 1
    RIB2 = 2
