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

	def test_strip_tweets_totally_strips_tweet(self):
		tweet_object = { \
			'blah':1, \
			'retweeted':False,
			'created_at': 'time',
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

		self.assertEqual(self.tweet_parser.strip_tweet([], tweet_object), {})

	def test_strip_tweets_keeps_fields(self):
		tweet_object = { \
			'blah':1, \
			'retweeted':False,
			'created_at': 'time',
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
		  	}, \
		  	"user" : {
				"follow_request_sent" : None,
				"profile_use_background_image" : True,
				"default_profile_image" : False,
				"geo_enabled" : False,
				"verified" : False,
				"profile_image_url_https" : "https://pbs.twimg.com/profile_images/496694241536397313/zQY6Kebr_normal.jpeg",
				"profile_sidebar_fill_color" : "DDEEF6",
				"id" : 379851447,
				"profile_text_color" : "333333",
				"followers_count" : 3159,
				"profile_sidebar_border_color" : "C0DEED",
				"id_str" : "379851447",
				"profile_background_color" : "C0DEED",
				"listed_count" : 401,
				"utc_offset" : 0,
				"statuses_count" : 477638,
				"description" : "#gaza #palestine #israel #BDS MAD EVIL ISRAEL MURDERS BABIES CIVILIANS to STEAL PALESTINIAN LAND RESOURCES with USA UK HELP. To stop my tweets, BLOCK or MUTE me",
				"friends_count" : 2019,
				"profile_link_color" : "0084B4",
				"profile_image_url" : "http://pbs.twimg.com/profile_images/496694241536397313/zQY6Kebr_normal.jpeg",
				"following" : None,
				"time_zone" : "London",
				"profile_background_image_url_https" : "https://abs.twimg.com/images/themes/theme1/bg.png",
				"profile_banner_url" : "https://pbs.twimg.com/profile_banners/379851447/1416509762",
				"profile_background_image_url" : "http://abs.twimg.com/images/themes/theme1/bg.png",
				"name" : "ISRAEL BOMBS BABIES",
				"lang" : "en",
				"profile_background_tile" : False,
				"favourites_count" : 15917,
				"screen_name" : "Col_Connaughton",
				"notifications" : None,
				"url" : None,
				"created_at" : "Sun Sep 25 17:29:09 +0000 2011",
				"contributors_enabled" : False,
				"location" : "London UK",
				"protected" : False,
				"default_profile" : True,
				"is_translator" : False
			}
		}
		stripped_obj = {
			'blah':1,
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
		  	}, \
		  	"user": {
		  		"profile_image_url_https" : "https://pbs.twimg.com/profile_images/496694241536397313/zQY6Kebr_normal.jpeg"
		  	}
		}

		self.maxDiff = None
		self.assertEqual(self.tweet_parser.strip_tweet(['blah', 'entities.user_mentions', 'user.profile_image_url_https'], tweet_object), stripped_obj)

	def test_parses_columns_from_tweet(self):
		tweet_object = { \
			'blah':1, \
			'retweeted':False,
			'created_at': 'time',
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
		  	}, \
		  	"user" : {
				"follow_request_sent" : None,
				"profile_use_background_image" : True,
				"default_profile_image" : False,
				"geo_enabled" : False,
				"verified" : False,
				"profile_image_url_https" : "https://pbs.twimg.com/profile_images/496694241536397313/zQY6Kebr_normal.jpeg",
				"profile_sidebar_fill_color" : "DDEEF6",
				"id" : 379851447,
				"profile_text_color" : "333333",
				"followers_count" : 3159,
				"profile_sidebar_border_color" : "C0DEED",
				"id_str" : "379851447",
				"profile_background_color" : "C0DEED",
				"listed_count" : 401,
				"utc_offset" : 0,
				"statuses_count" : 477638,
				"description" : "#gaza #palestine #israel #BDS MAD EVIL ISRAEL MURDERS BABIES CIVILIANS to STEAL PALESTINIAN LAND RESOURCES with USA UK HELP. To stop my tweets, BLOCK or MUTE me",
				"friends_count" : 2019,
				"profile_link_color" : "0084B4",
				"profile_image_url" : "http://pbs.twimg.com/profile_images/496694241536397313/zQY6Kebr_normal.jpeg",
				"following" : None,
				"time_zone" : "London",
				"profile_background_image_url_https" : "https://abs.twimg.com/images/themes/theme1/bg.png",
				"profile_banner_url" : "https://pbs.twimg.com/profile_banners/379851447/1416509762",
				"profile_background_image_url" : "http://abs.twimg.com/images/themes/theme1/bg.png",
				"name" : "ISRAEL BOMBS BABIES",
				"lang" : "en",
				"profile_background_tile" : False,
				"favourites_count" : 15917,
				"screen_name" : "Col_Connaughton",
				"notifications" : None,
				"url" : None,
				"created_at" : "Sun Sep 25 17:29:09 +0000 2011",
				"contributors_enabled" : False,
				"location" : "London UK",
				"protected" : False,
				"default_profile" : True,
				"is_translator" : False
			}
		}
		ret = self.tweet_parser.parse_columns_from_tweet(tweet_object, ['blah', 'entities.user_mentions.0.id_str', 'entities.user_mentions.1.id_str', 'user.wrong_ass_index', 'user.profile_sidebar_fill_color', 'user.profile_background_tile'])
		ret_values = [col_val[1] for col_val in ret]
		self.assertEqual(ret_values, [1, '6844292', '376825877', None, 'DDEEF6', False])


if __name__ == '__main__':
	unittest.main()

'''
read about twitter entities here:
https://dev.twitter.com/overview/api/entities-in-twitter-objects
'''
