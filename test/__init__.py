'''
module indicator for tests directory
'''

from . import test_base_collection
from . import test_bson_collection
from . import test_json_collection
from . import test_mongo_collection
from . import test_tweet_parser
__all__ = ['test_base_collection', 'test_bson_collection', 'test_json_collection', 'test_mongo_collection', 'test_tweet_parser']
