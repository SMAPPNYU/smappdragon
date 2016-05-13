import os
import unittest

from test.config import config
from smappdragon import JsonCollection
from smappdragon.tools.tweet_parser import TweetParser

class TestJsonCollection(unittest.TestCase):

	def test_iterator_returns_tweets(self):
		collection = JsonCollection(os.path.dirname(os.path.realpath(__file__)) +'/'+ config['json']['valid'])
		self.assertTrue(len(list(collection.get_iterator())) > 0)

	# special test because custom logic is different on mongo
	def test_json_collection_custom_filter_filters(self):
		collectionone = JsonCollection(os.path.dirname(os.path.realpath(__file__)) +'/'+ config['json']['valid'])
		full_collection_len = len(list(collectionone.get_iterator()))
		def is_tweet_a_retweet(tweet):
			if 'retweeted' in tweet and tweet['retweeted']:
				return True
			else:
				return False
		num_retweets = len(list(collectionone.set_custom_filter(is_tweet_a_retweet).get_iterator()))

		collectiontwo = JsonCollection(os.path.dirname(os.path.realpath(__file__)) +'/'+ config['json']['valid'])
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
		collection = JsonCollection(os.path.dirname(os.path.realpath(__file__)) +'/'+ config['json']['valid'])
		self.maxDiff = None
		it = collection.strip_tweets(['id', 'entities.user_mentions', 'user.profile_image_url_https']).get_iterator()
		def tweets_have_right_keys(iterator, fields):
			for tweet in iterator:
				keys = [key for key,value in tweet_parser.flatten_dict(tweet)]
				for elem in fields:
					if elem not in keys:
						return False
			return True		
		self.assertTrue(tweets_have_right_keys(it, [['id'], ['entities', 'user_mentions'], ['user', 'profile_image_url_https']]))

if __name__ == '__main__':
	unittest.main()
