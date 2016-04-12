import os
import unittest
import unicodecsv

from tests.config import config
from smappdragon import BsonCollection
from smappdragon import MongoCollection
from smappdragon import JsonCollection

class TestBaseCollection(unittest.TestCase):

	def test_base_top_entities_returns_dict(self):
		collection = BsonCollection(os.path.dirname(os.path.realpath(__file__)) +'/'+ config['bson']['valid'])
		returndict = collection.top_entities({'hashtags':5})
		self.assertTrue(isinstance(returndict, dict))

	def test_base_top_entities_returns_hashtags(self):
		collection = BsonCollection(os.path.dirname(os.path.realpath(__file__)) +'/'+ config['bson']['valid'])
		returndict = collection.top_entities({'hashtags':5})
		self.assertTrue('hashtags' in returndict)

	def test_base_top_entities_returns_hashtags_and_media(self):
		collection = BsonCollection(os.path.dirname(os.path.realpath(__file__)) +'/'+ config['bson']['valid'])
		returndict = collection.top_entities({'user_mentions':5, 'media':3})
		self.assertTrue('user_mentions' in returndict and 'media' in returndict)

	def test_base_top_entities_returns_counts(self):
		collection = BsonCollection(os.path.dirname(os.path.realpath(__file__)) +'/'+ config['bson']['valid'])
		returndict = collection.top_entities({'urls':5, 'symbols':3})
		if len(returndict['urls']) > 0:
			self.assertTrue(len(returndict['urls']) == 5)
		if len(returndict['symbols']) > 0:
			self.assertTrue(len(returndict['symbols']) == 3)

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
		if os.path.exists(os.path.dirname(os.path.abspath(__file__))+'/bson/output.bson'):
			os.remove(os.path.dirname(os.path.abspath(__file__))+'/bson/output.bson')

		output_path = os.path.dirname(os.path.realpath(__file__)) + '/' + 'bson/output.bson'
		collection = BsonCollection(os.path.dirname(os.path.realpath(__file__)) +'/'+ config['bson']['valid'])
		collection.dump_to_bson(output_path)
		self.assertTrue(os.path.getsize(output_path) > 0)

		if os.path.exists(os.path.dirname(os.path.abspath(__file__))+'/bson/output.bson'):
			os.remove(os.path.dirname(os.path.abspath(__file__))+'/bson/output.bson')

	def test_dump_to_json_dumps(self):
		if os.path.exists(os.path.dirname(os.path.abspath(__file__))+'/bson/output.bson.json'):
			os.remove(os.path.dirname(os.path.abspath(__file__))+'/bson/output.bson.json')

		output_path = os.path.dirname(os.path.realpath(__file__)) + '/' + 'bson/output.bson.json'
		collection = BsonCollection(os.path.dirname(os.path.realpath(__file__)) +'/'+ config['bson']['valid'])
		collection.dump_to_json(output_path)
		self.assertTrue(os.path.getsize(output_path) > 0)

		if os.path.exists(os.path.dirname(os.path.abspath(__file__))+'/bson/output.bson.json'):
			os.remove(os.path.dirname(os.path.abspath(__file__))+'/bson/output.bson.json')

	def test_dump_to_csv_orders_properly(self):
		if os.path.exists(os.path.dirname(os.path.abspath(__file__))+'/bson/output.csv'):
			os.remove(os.path.dirname(os.path.abspath(__file__))+'/bson/output.csv')

		output_path = os.path.dirname(os.path.realpath(__file__)) + '/' + 'bson/output.csv'
		collection = JsonCollection(os.path.dirname(os.path.realpath(__file__)) +'/'+ config['json']['valid-single'])
		collection.dump_to_csv(output_path, ['id_str', 'entities.hashtags.0', 'entities.hashtags.1'])
		with open(os.path.dirname(os.path.abspath(__file__))+'/bson/output.csv', 'rb') as filehandle:
			count = 0
			for line in unicodecsv.reader(filehandle):
				if count != 0:
					self.assertEqual(line, ['661275583813431296', "{'text': 'jadehelm', 'indices': [74, 83]}", "{'text': 'newworldorder', 'indices': [84, 98]}"])
				else:
					count += 1
		filehandle.close()
		
		if os.path.exists(os.path.dirname(os.path.abspath(__file__))+'/bson/output.csv'):
			os.remove(os.path.dirname(os.path.abspath(__file__))+'/bson/output.csv')

	def test_dump_to_csv_dumps(self):
		if os.path.exists(os.path.dirname(os.path.abspath(__file__))+'/bson/output.csv'):
			os.remove(os.path.dirname(os.path.abspath(__file__))+'/bson/output.csv')

		output_path = os.path.dirname(os.path.realpath(__file__)) + '/' + 'bson/output.csv'
		collection = BsonCollection(os.path.dirname(os.path.realpath(__file__)) +'/'+ config['bson']['valid'])
		collection.dump_to_csv(output_path, ['id_str', 'entities.hashtags.0', 'entities.hashtags.1'])
		self.assertTrue(os.path.getsize(output_path) > 0)

		if os.path.exists(os.path.dirname(os.path.abspath(__file__))+'/bson/output.csv'):
			os.remove(os.path.dirname(os.path.abspath(__file__))+'/bson/output.csv')

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

if __name__ == '__main__':
	unittest.main()
