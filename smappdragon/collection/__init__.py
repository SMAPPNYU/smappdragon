'''
module indicator for collection
'''
from . import mongo_collection
from . import bson_collection
from . import json_collection
from . import csv_collection
__all__ = ['mongo_collection', 'bson_collection', 'json_collection', 'csv_collection']
