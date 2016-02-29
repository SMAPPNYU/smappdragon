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


if __name__ == '__main__':
	unittest.main()

'''
read about twitter entities here:
https://dev.twitter.com/overview/api/entities-in-twitter-objects
'''
