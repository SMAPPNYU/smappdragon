import os
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
		collection.dump_to_csv(output_path, ['id_str', 'entities.hashtags.0', 'entities.hashtags.1', 'source', 'user.id', 'timestamp.$date', 'text'])
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
							loaded_dict = json_util.loads(csv_row_value)
							if not all(k in loaded_dict for k in ['text', 'indices']) and loaded_dict['text'] == 'jadehelm' and loaded_dict['indices'] == [74, 83]:
								everything_in_order = False
						elif val_count == 2:
							loaded_dict = json_util.loads(csv_row_value)
							if not all(k in loaded_dict for k in ['text', 'indices']) and loaded_dict['text'] == 'newworldorder' and loaded_dict['indices'] == [84, 98]:
								everything_in_order = False
						elif val_count == 3:
							self.assertEqual(csv_row_value, '<a href="https://twitter.com/Col_Connaughton" rel="nofollow">Colin\'s Autotweeterpro5.3</a>')
						elif val_count == 4:
							self.assertEqual(csv_row_value, '379851447')
						elif val_count == 5:
							self.assertEqual(csv_row_value, '1446495359000')
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

		output_path = os.path.dirname(os.path.realpath(__file__)) + '/' + 'data/output.csv'
		collection = BsonCollection(os.path.dirname(os.path.realpath(__file__)) +'/'+ config['bson']['valid'])
		collection.dump_to_csv(output_path, ['id_str', 'entities.hashtags.0', 'entities.hashtags.1'])
		self.assertTrue(os.path.getsize(output_path) > 0)

		if os.path.exists(os.path.dirname(os.path.abspath(__file__))+'/data/output.csv'):
			os.remove(os.path.dirname(os.path.abspath(__file__))+'/data/output.csv')

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
