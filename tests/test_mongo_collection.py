import unittest
from tests.config import config
from smappdragon import MongoCollection

class TestMongoCollection(unittest.TestCase):
	collection = MongoCollection( \
							config['mongo']['host'], \
							config['mongo']['port'], \
							config['mongo']['user'], \
							config['mongo']['password'], \
							config['mongo']['database'], \
							config['mongo']['collection'] \
							)

	def test_mongo_top_entities_returns_dict(self):
		returndict = self.collection.top_entities({'hashtags':5})
		self.assertTrue(isinstance(returndict, dict))

	def test_mongo_top_entities_returns_hashtags(self):
		returndict = self.collection.top_entities({'hashtags':5})
		self.assertTrue('hashtags' in returndict)

	def test_mongo_top_entities_returns_hashtags_and_media(self):
		returndict = self.collection.top_entities({'user_mentions':5, 'media':3})
		self.assertTrue('user_mentions' in returndict and 'media' in returndict)

	def test_mongo_top_entities_returns_counts(self):
		returndict = self.collection.top_entities({'urls':5, 'symbols':3})
		if len(returndict['urls']) > 0:
			self.assertTrue(len(returndict['urls']) == 5)
		if len(returndict['symbols']) > 0:
			self.assertTrue(len(returndict['symbols']) == 3)

	def test_limit_is_set(self):
		self.collection.set_limit(5)
		self.assertEqual(5, self.collection.limit)

	def test_limit_actually_limits(self):
		count = len(list(self.collection.set_limit(5).get_iterator()))
		self.assertEqual(5, count)

if __name__ == '__main__':
	unittest.main()

'''
read about twitter entities here:
https://dev.twitter.com/overview/api/entities-in-twitter-objects
'''

