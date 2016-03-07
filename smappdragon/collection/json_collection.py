import os
import json

from smappdragon.tools.tweet_parser import TweetParser
from smappdragon.collection.base_collection import BaseCollection

class JsonCollection(BaseCollection):
    '''
        method that tells us how to
        create the JsonCollection object
    '''
    def __init__(self, filepath):
        BaseCollection.__init__(self)
        self.filepath = filepath
        if not os.path.isfile(filepath):
            raise IOError(filepath, 'JsonCollection could not find your file, it\'s mispelled or doesn\'t exist.')

    '''
        method that creates a cursor
        and yields all tweets in a particular collection
    '''
    def get_iterator(self):
        count = 0
        tweet_parser = TweetParser()
        json_handle = open(self.filepath, 'rb')
        for tweet in bson.decode_file_iter(bson_handle):
            if self.limit < count and not self.limit == 0:
                raise StopIteration
            elif tweet_parser.tweet_passes_filter(self.filter, tweet):
                count += 1
                yield tweet
        bson_handle.close()
