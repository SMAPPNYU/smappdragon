import unittest
from smappdragon import TweetParser

class TestTweetParser(unittest.TestCase):
	tweet_parser = TweetParser()

	def test_contains_entity_empty(self):
		self.assertFalse( \
						self.tweet_parser.contains_entity( \
							'user_mentions', \
							{'blah':1, 'entities':{'user_mentions':[]}} \
						) \
		)

	def test_contains_entity(self):
		tweet_object = { \
			'blah':1, \
			'entities':{ \
				'user_mentions':[ \
					{ \
				      "screen_name": "TwitterEng", \
				      "name": "Twitter Engineering", \
				      "id": 6844292, \
				      "id_str": "6844292", \
				      "indices": [81, 92] \
				    }, { \
				      "screen_name": "TwitterOSS", \
				      "name": "Twitter Open Source", \
				      "id": 376825877, \
				      "id_str": "376825877", \
				      "indices": [121, 132] \
				    } \
				] \
		  	} \
		}
		self.assertTrue(self.tweet_parser.contains_entity('user_mentions', tweet_object))

	def test_get_entity_empty(self):
		self.assertEqual([], self.tweet_parser.get_entity('urls', {'blah':1, 'user_mentions':[]}))

	def test_get_entity(self):
		url_entity_objects = [ \
			{ \
		      "url": "https://t.co/XdXRudPXH5", \
		      "expanded_url": "https://blog.twitter.com/2013/rich-photo-experience-now-in-embedded-tweets-3", \
		      "display_url": "blog.twitter.com/2013/rich-phot", \
		      "indices": [80, 103] \
		    }, \
			{ \
		      "url": "https://t.co/XdXRudPXH4", \
		      "expanded_url": "https://blog.twitter.com/2013/rich-photo-experience-now-in-embedded-tweets-3", \
		      "display_url": "blog.twitter.com/2013/rich-deio", \
		      "indices": [80, 103] \
		    } \
		]
		self.assertEqual(url_entity_objects, self.tweet_parser.get_entity('urls', {'blah':1, 'entities':{'urls':url_entity_objects}}))

	def test_get_entity_field(self):
		url_entity_object = { \
		      "url": "https://t.co/XdXRudPXH5", \
		      "expanded_url": "https://blog.twitter.com/2013/rich-photo-experience-now-in-embedded-tweets-3", \
		      "display_url": "blog.twitter.com/2013/rich-phot", \
		      "indices": [80, 103] \
		    }
		self.assertEqual('blog.twitter.com/2013/rich-phot', self.tweet_parser.get_entity_field('display_url', url_entity_object))

	def test_flatten_dict_flattens(self):
		dict_to_flatten = {'a':'b', 'c':{'d':'e', 'f':{'g':'h', 'i':'j'}}}
		actual_flat_dict = [(['a'], 'b'), (['c', 'd'], 'e'), (['c', 'f', 'i'], 'j'), (['c', 'f', 'g'], 'h')]
		dict_was_flattened = True
		for entry in self.tweet_parser.flatten_dict(dict_to_flatten):
			if entry not in actual_flat_dict:
				dict_was_flattened = False
		self.assertTrue(dict_was_flattened)

	def tests_tweet_passes_empty_filter(self):
		tweet_to_test = {'a':'b', 'c':{'d':'e', 'f':{'g':'h', 'i':'j'}}}
		self.assertTrue(self.tweet_parser.tweet_passes_filter({}, tweet_to_test))

	def test_tweet_passes_filter_of_itself(self):
		tweet_to_test = {'a':'b', 'c':{'d':'e', 'f':{'g':'h', 'i':'j'}}}
		filter_obj = {'a':'b', 'c':{'d':'e', 'f':{'g':'h', 'i':'j'}}}
		self.assertTrue(self.tweet_parser.tweet_passes_filter(filter_obj, tweet_to_test))

	def test_tweet_passes_filter(self):
		tweet_to_test = {'a':'b', 'c':{'d':'e', 'f':{'g':'h', 'i':'j'}}}
		filter_obj = {'a':'b'}
		self.assertTrue(self.tweet_parser.tweet_passes_filter(filter_obj, tweet_to_test))

	def tests_tweet_fails_on_bad_filter(self):
		tweet_to_test = {'a':'b', 'c':{'d':'e', 'f':{'g':'h', 'i':'j'}}}
		filter_obj = {'t':'m'}
		self.assertFalse(self.tweet_parser.tweet_passes_filter(filter_obj, tweet_to_test))

	def test_tweet_passes_good_custom_filter(self):
		tweet_object = { \
			'blah':1, \
			'retweeted':True,
			'entities':{ \
				'user_mentions':[ \
					{ \
				      "screen_name": "TwitterEng", \
				      "name": "Twitter Engineering", \
				      "id": 6844292, \
				      "id_str": "6844292", \
				      "indices": [81, 92] \
				    }, { \
				      "screen_name": "TwitterOSS", \
				      "name": "Twitter Open Source", \
				      "id": 376825877, \
				      "id_str": "376825877", \
				      "indices": [121, 132] \
				    } \
				] \
		  	} \
		}
		def is_tweet_a_retweet(tweet):
			if 'retweeted' in tweet and tweet['retweeted']:
				return True
			else:
				return False
		self.assertTrue(self.tweet_parser.tweet_passes_custom_filter(is_tweet_a_retweet, tweet_object))

	def test_tweet_does_not_pass_incorrect_custom_filter(self):
		tweet_object = { \
			'blah':1, \
			'retweeted':False,
			'entities':{ \
				'user_mentions':[ \
					{ \
				      "screen_name": "TwitterEng", \
				      "name": "Twitter Engineering", \
				      "id": 6844292, \
				      "id_str": "6844292", \
				      "indices": [81, 92] \
				    }, { \
				      "screen_name": "TwitterOSS", \
				      "name": "Twitter Open Source", \
				      "id": 376825877, \
				      "id_str": "376825877", \
				      "indices": [121, 132] \
				    } \
				] \
		  	} \
		}
		def is_tweet_a_retweet(tweet):
			if 'retweeted' in tweet and tweet['retweeted']:
				return True
			else:
				return False
		self.assertFalse(self.tweet_parser.tweet_passes_custom_filter(is_tweet_a_retweet, tweet_object))

	def test_tweet_passes_good_custom_filter_list(self):
		tweet_object = { \
			'blah':1, \
			'retweeted':True,
			'entities':{ \
				'user_mentions':[ \
					{ \
				      "screen_name": "TwitterEng", \
				      "name": "Twitter Engineering", \
				      "id": 6844292, \
				      "id_str": "6844292", \
				      "indices": [81, 92] \
				    }, { \
				      "screen_name": "TwitterOSS", \
				      "name": "Twitter Open Source", \
				      "id": 376825877, \
				      "id_str": "376825877", \
				      "indices": [121, 132] \
				    } \
				] \
		  	} \
		}
		def is_tweet_a_retweet(tweet):
			if 'retweeted' in tweet and tweet['retweeted']:
				return True
			else:
				return False
		def tweet_has_blah(tweet):
			if 'blah' in tweet and tweet['blah'] == 1:
				return True
			else:
				return False
		self.assertTrue(self.tweet_parser.tweet_passes_custom_filter_list([is_tweet_a_retweet, tweet_has_blah], tweet_object))

	def test_tweet_does_not_pass_incorrect_custom_filter_list(self):
		tweet_object = { \
			'blah':1, \
			'retweeted':False,
			'entities':{ \
				'user_mentions':[ \
					{ \
				      "screen_name": "TwitterEng", \
				      "name": "Twitter Engineering", \
				      "id": 6844292, \
				      "id_str": "6844292", \
				      "indices": [81, 92] \
				    }, { \
				      "screen_name": "TwitterOSS", \
				      "name": "Twitter Open Source", \
				      "id": 376825877, \
				      "id_str": "376825877", \
				      "indices": [121, 132] \
				    } \
				] \
		  	} \
		}
		def is_tweet_a_retweet(tweet):
			if 'retweeted' in tweet and tweet['retweeted']:
				return True
			else:
				return False
		def tweet_has_blah(tweet):
			if 'blah' in tweet and tweet['blah'] == 1:
				return True
			else:
				return False
		self.assertFalse(self.tweet_parser.tweet_passes_custom_filter_list([is_tweet_a_retweet, tweet_has_blah], tweet_object))

	def test_transform_transforms_tweet(self):
		tweet_object = { \
			'blah':1, \
			'retweeted':False,
			'entities':{ \
				'user_mentions':[ \
					{ \
				      "screen_name": "TwitterEng", \
				      "name": "Twitter Engineering", \
				      "id": 6844292, \
				      "id_str": "6844292", \
				      "indices": [81, 92] \
				    }, { \
				      "screen_name": "TwitterOSS", \
				      "name": "Twitter Open Source", \
				      "id": 376825877, \
				      "id_str": "376825877", \
				      "indices": [121, 132] \
				    } \
				] \
		  	} \
		}
		



if __name__ == '__main__':
	unittest.main()

'''
read about twitter entities here:
https://dev.twitter.com/overview/api/entities-in-twitter-objects
'''
