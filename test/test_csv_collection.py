import os
import unittest

from test.config import config
from smappdragon import CsvCollection
from smappdragon.tools.tweet_parser import TweetParser

class TestCsvCollection(unittest.TestCase):

    def test_iterator_returns_tweets(self):
        collection = CsvCollection(os.path.dirname(os.path.realpath(__file__)) +'/'+ config['csv']['valid'])
        self.assertTrue(len(list(collection.get_iterator())) > 0)

    # special test because custom logic is different on mongo
    def test_json_collection_custom_filter_filters(self):
        collectionone = CsvCollection(os.path.dirname(os.path.realpath(__file__)) +'/'+ config['csv']['valid'])
        full_collection_len = len(list(collectionone.get_iterator()))
        def is_tweet_a_retweet(tweet):
            if 'retweeted' in tweet and tweet['retweeted']:
                return True
            else:
                return False
        num_retweets = len(list(collectionone.set_custom_filter(is_tweet_a_retweet).get_iterator()))

        collectiontwo = CsvCollection(os.path.dirname(os.path.realpath(__file__)) +'/'+ config['csv']['valid'])
        def is_not_a_retweet(tweet):
            if 'retweeted' in tweet and tweet['retweeted']:
                return False
            else:
                return True
        num_non_retweets = len(list(collectiontwo.set_custom_filter(is_not_a_retweet).get_iterator()))

        #the numbes of retweets and non retweets should add up to the whole collection
        self.assertEqual(num_retweets + num_non_retweets, full_collection_len)
        
    def test_strip_tweets_keeps_fields(self):
        tweet_parser = TweetParser()
        collection = CsvCollection(os.path.dirname(os.path.realpath(__file__)) +'/'+ config['csv']['valid'])
        self.maxDiff = None
        it = collection.strip_tweets(['source', 'text', 'id_str']).get_iterator()
        def tweets_have_right_keys(iterator, fields):
            for tweet in iterator:
                keys = [key for key,value in tweet_parser.flatten_dict(tweet)]
                for elem in fields:
                    if elem not in keys:
                        return False
            return True     
        self.assertTrue(tweets_have_right_keys(it, [['source'], ['text'], ['id_str']]))


if __name__ == '__main__':
    unittest.main()
