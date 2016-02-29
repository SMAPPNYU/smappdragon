import unittest
from tests.config import config
from smappdragon import MongoCollection

class TestMongoCollection(unittest.TestCase):
	# collection repeated a lot
	# for some reason when i make a shared var
	# the generator function deosn't init properly

	# def test_iterator_returns_tweets(self):

	def test_mongo_top_entities_returns_dict(self):
		collection = MongoCollection( \
							config['mongo']['host'], \
							config['mongo']['port'], \
							config['mongo']['user'], \
							config['mongo']['password'], \
							config['mongo']['database'], \
							config['mongo']['collection'] \
							)
		returndict = collection.top_entities({'hashtags':5})
		self.assertTrue(isinstance(returndict, dict))

	def test_mongo_top_entities_returns_hashtags(self):
		collection = MongoCollection( \
							config['mongo']['host'], \
							config['mongo']['port'], \
							config['mongo']['user'], \
							config['mongo']['password'], \
							config['mongo']['database'], \
							config['mongo']['collection'] \
							)
		returndict = collection.top_entities({'hashtags':5})
		self.assertTrue('hashtags' in returndict)

	def test_mongo_top_entities_returns_hashtags_and_media(self):
		collection = MongoCollection( \
							config['mongo']['host'], \
							config['mongo']['port'], \
							config['mongo']['user'], \
							config['mongo']['password'], \
							config['mongo']['database'], \
							config['mongo']['collection'] \
							)
		returndict = collection.top_entities({'user_mentions':5, 'media':3})
		self.assertTrue('user_mentions' in returndict and 'media' in returndict)

	def test_mongo_top_entities_returns_counts(self):
		collection = MongoCollection( \
							config['mongo']['host'], \
							config['mongo']['port'], \
							config['mongo']['user'], \
							config['mongo']['password'], \
							config['mongo']['database'], \
							config['mongo']['collection'] \
							)
		returndict = collection.top_entities({'urls':5, 'symbols':3})
		if len(returndict['urls']) > 0:
			self.assertTrue(len(returndict['urls']) == 5)
		if len(returndict['symbols']) > 0:
			self.assertTrue(len(returndict['symbols']) == 3)

	def test_limit_is_set(self):
		collection = MongoCollection( \
							config['mongo']['host'], \
							config['mongo']['port'], \
							config['mongo']['user'], \
							config['mongo']['password'], \
							config['mongo']['database'], \
							config['mongo']['collection'] \
							)
		collection.set_limit(5)
		self.assertEqual(5, collection.limit)
		collection.set_limit(0)

	def test_limit_actually_limits(self):
		collection = MongoCollection( \
							config['mongo']['host'], \
							config['mongo']['port'], \
							config['mongo']['user'], \
							config['mongo']['password'], \
							config['mongo']['database'], \
							config['mongo']['collection'] \
							)
		collection.get_iterator()
		count = len([tweet for tweet in collection.set_limit(5).get_iterator()])
		self.assertEqual(5, count)

	def test_filter_is_set(self):
		collection = MongoCollection( \
							config['mongo']['host'], \
							config['mongo']['port'], \
							config['mongo']['user'], \
							config['mongo']['password'], \
							config['mongo']['database'], \
							config['mongo']['collection'] \
							)
		collection.set_filter({'a':'b', 'c':'d', 'e':{ 'f':'g', 'h':'i' }})
		self.assertEqual(collection.filter, {'a':'b', 'c':'d', 'e':{ 'f':'g', 'h':'i' }})

	# def test_filter_actually_filters(self):

if __name__ == '__main__':
	unittest.main()

'''
read about twitter entities here:
https://dev.twitter.com/overview/api/entities-in-twitter-objects
'''

