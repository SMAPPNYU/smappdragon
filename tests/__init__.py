'''
module indicator for tests directory
'''

from . import test_mongo_collection
from . import test_tweet_parser
__all__ = ['test_tweet_parser', 'test_mongo_collection']
