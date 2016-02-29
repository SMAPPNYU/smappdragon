import os
import unittest
from tests.config import config
from smappdragon import BsonCollection

class TestBsonCollection(unittest.TestCase):

	def test_iterator_returns_tweets(self):
		collection = BsonCollection(os.path.dirname(os.path.realpath(__file__)) +'/'+ config['bson']['valid'])
		for tweet in collection.get_iterator():
			print tweet

	# def test_mongo_top_entities_returns_dict(self):
	# 	collection = BsonCollection(config['bson']['valid'])
	# 	returndict = collection.top_entities({'hashtags':5})
	# 	self.assertTrue(isinstance(returndict, dict))
	