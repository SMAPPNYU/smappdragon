import os
import unicodecsv

from smappdragon.tools.tweet_parser import TweetParser
from smappdragon.collection.base_collection import BaseCollection

class CsvCollection(BaseCollection):
    '''
        method that tells us how to
        create the CsvCollection object
    '''
    def __init__(self, filepath):
        BaseCollection.__init__(self)
        self.filepath = filepath
        if not os.path.isfile(filepath):
            raise IOError(filepath, 'CsvCollection could not find your file, it\'s mispelled or doesn\'t exist.')

    '''
        method that creates a cursor
        and yields all tweets in a particular collection
    '''
    def get_iterator(self):
        count = 1
        tweet_parser = TweetParser()
        csv_handle = open(self.filepath, 'rb')
        for tweet in unicodecsv.DictReader(csv_handle):
            if self.limit < count and self.limit != 0:
                csv_handle.close()
                return
            elif tweet_parser.tweet_passes_filter(self.filter, tweet) \
            and tweet_parser.tweet_passes_custom_filter_list(self.custom_filters, tweet):
                count += 1
                yield tweet
        csv_handle.close()
