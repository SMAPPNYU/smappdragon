import os
import sqlite3
import unittest
import unicodecsv

from bson import json_util
from test.config import config
from smappdragon import BsonCollection
from smappdragon import MongoCollection
from smappdragon import JsonCollection

class TestBaseCollection(unittest.TestCase):

    def test_limit_is_set(self):
        collection = BsonCollection(os.path.dirname(os.path.realpath(__file__)) +'/'+ config['bson']['valid'])
        collection.set_limit(5)
        self.assertEqual(5, collection.limit)
        collection.set_limit(0)

    def test_limit_actually_limits(self):
        collection = BsonCollection(os.path.dirname(os.path.realpath(__file__)) +'/'+ config['bson']['valid'])
        collection.get_iterator()
        count = len(list(tweet for tweet in collection.set_limit(5).get_iterator()))
        self.assertEqual(5, count)

    def test_filter_is_set(self):
        collection = BsonCollection(os.path.dirname(os.path.realpath(__file__)) +'/'+ config['bson']['valid'])
        collection.set_filter({'a':'b', 'c':'d', 'e':{'f':'g', 'h':'i'}})
        self.assertEqual(collection.filter, {'a':'b', 'c':'d', 'e':{'f':'g', 'h':'i'}})

    def test_dump_to_bson_dumps(self):
        if os.path.exists(os.path.dirname(os.path.abspath(__file__))+'/data/output.bson'):
            os.remove(os.path.dirname(os.path.abspath(__file__))+'/data/output.bson')

        output_path = os.path.dirname(os.path.realpath(__file__)) + '/' + 'data/output.bson'
        collection = BsonCollection(os.path.dirname(os.path.realpath(__file__)) +'/'+ config['bson']['valid'])
        collection.dump_to_bson(output_path)
        self.assertTrue(os.path.getsize(output_path) > 0)

        if os.path.exists(os.path.dirname(os.path.abspath(__file__))+'/data/output.bson'):
            os.remove(os.path.dirname(os.path.abspath(__file__))+'/data/output.bson')

    def test_dump_to_json_dumps(self):
        if os.path.exists(os.path.dirname(os.path.abspath(__file__))+'/data/output.bson.json'):
            os.remove(os.path.dirname(os.path.abspath(__file__))+'/data/output.bson.json')

        output_path = os.path.dirname(os.path.realpath(__file__)) + '/' + 'data/output.bson.json'
        collection = BsonCollection(os.path.dirname(os.path.realpath(__file__)) +'/'+ config['bson']['valid'])
        collection.dump_to_json(output_path)
        self.assertTrue(os.path.getsize(output_path) > 0)

        if os.path.exists(os.path.dirname(os.path.abspath(__file__))+'/data/output.bson.json'):
            os.remove(os.path.dirname(os.path.abspath(__file__))+'/data/output.bson.json')

    def test_dump_to_csv_orders_and_encodes_properly(self):
        if os.path.exists(os.path.dirname(os.path.abspath(__file__))+'/data/output.csv'):
            os.remove(os.path.dirname(os.path.abspath(__file__))+'/data/output.csv')

        output_path = os.path.dirname(os.path.realpath(__file__)) + '/' + 'data/output.csv'
        collection = JsonCollection(os.path.dirname(os.path.realpath(__file__)) +'/'+ config['json']['valid-single'])
        collection.dump_to_csv(output_path, ['id_str', 'entities.hashtags.0.text', 'entities.hashtags.1.text', 'source', 'user.id', 'timestamp.$date', 'text'])
        with open(os.path.dirname(os.path.abspath(__file__))+'/data/output.csv', 'rb') as filehandle:
            count = 0
            for line in unicodecsv.reader(filehandle):
                if count != 0:
                    val_count = 0
                    for csv_row_value in line:
                        everything_in_order = True
                        if val_count == 0:
                            self.assertEqual(csv_row_value, '661275583813431296')
                        elif val_count == 1:
                            if csv_row_value != 'jadehelm':
                                everything_in_order = False
                        elif val_count == 2:
                            if csv_row_value != 'newworldorder':
                                everything_in_order = False
                        elif val_count == 3:
                            self.assertEqual(csv_row_value, '<a href="https://twitter.com/Col_Connaughton" rel="nofollow">Colin\'s Autotweeterpro5.3</a>')
                        elif val_count == 4:
                            self.assertEqual(csv_row_value, '379851447')
                        elif val_count == 5:
                            self.assertEqual(csv_row_value, '2015-11-02 20:15:59+00:00')
                        elif val_count == 6:
                            self.assertEqual(csv_row_value, 'Susan Lindauer, Rtd US Army LTC Potter: Jade Helm https://t.co/VA4bQRudLt #jadehelm #newworldorder #usa #tyranny #threat')
                        if everything_in_order:
                            self.assertTrue(True)
                        val_count += 1
                else:
                    count += 1
        filehandle.close()
        
        if os.path.exists(os.path.dirname(os.path.abspath(__file__))+'/data/output.csv'):
            os.remove(os.path.dirname(os.path.abspath(__file__))+'/data/output.csv')

    def test_dump_to_csv_dumps(self):
        if os.path.exists(os.path.dirname(os.path.abspath(__file__))+'/data/output.csv'):
            os.remove(os.path.dirname(os.path.abspath(__file__))+'/data/output.csv')

        field_list = ['id_str',
        'coordinates.coordinates.0',
        'coordinates.coordinates.1',
        'user.id_str',
        'user.lang',
        'lang',
        'text',
        'user.screen_name',
        'user.location',
        'user.description',
        'created_at',
        'user.friends_count',
        'user.followers_count',
        'retweet_count',
        'entities.urls.0.expanded_url',
        'entities.urls.1.expanded_url',
        'entities.urls.2.expanded_url',
        'entities.urls.3.expanded_url',
        'entities.urls.4.expanded_url',
        'entities.hashtags.0.text',
        'entities.hashtags.1.text']

        output_path = os.path.dirname(os.path.realpath(__file__)) + '/' + 'data/output.csv'
        collection = BsonCollection(os.path.dirname(os.path.realpath(__file__)) +'/'+ config['bson']['valid'])
        collection.dump_to_csv(output_path, field_list)
        self.assertTrue(os.path.getsize(output_path) > 0)

        if os.path.exists(os.path.dirname(os.path.abspath(__file__))+'/data/output.csv'):
            os.remove(os.path.dirname(os.path.abspath(__file__))+'/data/output.csv')

    def test_dump_to_sqlite_db_dumps(self):
        if os.path.exists(os.path.dirname(os.path.abspath(__file__))+'/data/output.db'):
            os.remove(os.path.dirname(os.path.abspath(__file__))+'/data/output.db')

        field_list = ['id_str',
        'coordinates.coordinates.0',
        'coordinates.coordinates.1',
        'user.id_str',
        'user.lang',
        'lang',
        'text',
        'user.screen_name',
        'user.location',
        'user.description',
        'created_at',
        'user.friends_count',
        'user.followers_count',
        'retweet_count',
        'entities.urls.0.expanded_url',
        'entities.urls.1.expanded_url',
        'entities.urls.2.expanded_url',
        'entities.urls.3.expanded_url',
        'entities.urls.4.expanded_url',
        'entities.hashtags.0.text',
        'entities.hashtags.1.text']

        output_path = os.path.dirname(os.path.realpath(__file__)) + '/' + 'data/output.db'
        collection = BsonCollection(os.path.dirname(os.path.realpath(__file__)) +'/'+ config['bson']['valid'])
        collection.dump_to_sqlite_db(output_path, field_list)

        self.assertTrue(os.path.getsize(output_path) > 0)

        if os.path.exists(os.path.dirname(os.path.abspath(__file__))+'/data/output.db'):
            os.remove(os.path.dirname(os.path.abspath(__file__))+'/data/output.db')

    def test_dump_to_sqlite_db_dumps_the_right_stuff(self):
        if os.path.exists(os.path.dirname(os.path.abspath(__file__))+'/data/output.db'):
            os.remove(os.path.dirname(os.path.abspath(__file__))+'/data/output.db')

        field_list = ['id_str',
        'coordinates.coordinates.0',
        'coordinates.coordinates.1',
        'user.id_str',
        'user.lang',
        'lang',
        'text',
        'user.screen_name',
        'user.location',
        'user.description',
        'created_at',
        'user.friends_count',
        'user.followers_count',
        'retweet_count',
        'entities.urls.0.expanded_url',
        'entities.urls.1.expanded_url',
        'entities.urls.2.expanded_url',
        'entities.urls.3.expanded_url',
        'entities.urls.4.expanded_url',
        'entities.hashtags.0.text',
        'entities.hashtags.1.text']

        output_path = os.path.dirname(os.path.realpath(__file__)) + '/' + 'data/output.db'
        collection = BsonCollection(os.path.dirname(os.path.realpath(__file__)) +'/'+ config['bson']['valid'])
        collection.dump_to_sqlite_db(output_path, field_list)

        con = sqlite3.connect(output_path)
        cur = con.cursor()
        row = [elem for row in cur.execute("SELECT * FROM data LIMIT 1;") for elem in row ]
        con.close()
        self.assertTrue(len(row) > 0)
        self.assertEqual(set(row), set(['661275583813431296', 'NULL', 'NULL', '379851447', 'en', 'de', 'Susan Lindauer, Rtd US Army LTC Potter: Jade Helm https://t.co/VA4bQRudLt #jadehelm #newworldorder #usa #tyranny #threat', 'Col_Connaughton', 'London UK', '#gaza #palestine #israel #BDS MAD EVIL ISRAEL MURDERS BABIES CIVILIANS to STEAL PALESTINIAN LAND RESOURCES with USA UK HELP. To stop my tweets, BLOCK or MUTE me', 'Mon Nov 02 20:15:59 +0000 2015', 2019, 3159, 0, 'https://www.youtube.com/watch?v=0nJqymxVpwc', 'NULL', 'NULL', 'NULL', 'NULL', 'jadehelm', 'newworldorder']))

        if os.path.exists(os.path.dirname(os.path.abspath(__file__))+'/data/output.db'):
            os.remove(os.path.dirname(os.path.abspath(__file__))+'/data/output.db')

    def test_set_custom_filter_is_set(self):
        collection = BsonCollection(os.path.dirname(os.path.realpath(__file__)) +'/'+ config['bson']['valid'])
        def is_tweet_a_retweet(tweet):
            if 'retweeted' in tweet and tweet['retweeted']:
                return True
            else:
                return False
        collection.set_custom_filter(is_tweet_a_retweet)
        self.assertTrue(len(collection.custom_filters) == 1)

    def test_set_custom_filter_is_not_double_set(self):
        collection = BsonCollection(os.path.dirname(os.path.realpath(__file__)) +'/'+ config['bson']['valid'])
        def is_tweet_a_retweet(tweet):
            if 'retweeted' in tweet and tweet['retweeted']:
                return True
            else:
                return False
        collection.set_custom_filter(is_tweet_a_retweet)
        self.assertFalse(len(collection.custom_filters) > 1)

    def test_collection_filters_custom_filter_filters_something(self):
        collection = BsonCollection(os.path.dirname(os.path.realpath(__file__)) +'/'+ config['bson']['valid'])
        long_len = len(list(collection.get_iterator()))
        def is_tweet_a_retweet(tweet):
            if 'retweeted' in tweet and tweet['retweeted']:
                return True
            else:
                return False
        collection.set_custom_filter(is_tweet_a_retweet)
        shorter_len = len(list(collection.get_iterator()))

        #there should be fewer retweets than all tweets.
        self.assertTrue(long_len > shorter_len)

    def test_collection_filters_custom_filter_properly_applies_filter(self):
        collectionone = BsonCollection(os.path.dirname(os.path.realpath(__file__)) +'/'+ config['bson']['valid'])
        full_collection_len = len(list(collectionone.get_iterator()))
        def is_tweet_a_retweet(tweet):
            if 'retweeted' in tweet and tweet['retweeted']:
                return True
            else:
                return False
        num_retweets = len(list(collectionone.set_custom_filter(is_tweet_a_retweet).get_iterator()))


        collectiontwo = BsonCollection(os.path.dirname(os.path.realpath(__file__)) +'/'+ config['bson']['valid'])
        def is_not_a_retweet(tweet):
            if 'retweeted' in tweet and tweet['retweeted']:
                return False
            else:
                return True
        num_non_retweets = len(list(collectiontwo.set_custom_filter(is_not_a_retweet).get_iterator()))

        #the numbes of retweets and non retweets should add up to the whole collection
        self.assertEqual(num_retweets + num_non_retweets, full_collection_len)

    def test_strip_tweets_strips_many_tweets_totally(self):
        collectionone = BsonCollection(os.path.dirname(os.path.realpath(__file__)) +'/'+ config['bson']['valid'])
        iterator = collectionone.strip_tweets([]).get_iterator()
        first_tweet = next(iterator)
        second_tweet = next(iterator)
        #exhaust the iterator
        len(list(iterator))
        self.assertTrue(first_tweet == {} and second_tweet == {})

if __name__ == '__main__':
    unittest.main()
