import os
import unittest

from tests.config import config
from smappdragon import BsonCollection
from smappdragon import MongoCollection

class TestBaseCollection(unittest.TestCase):

	def test_base_top_entities_returns_dict(self):
		collection = MongoCollection(     \
			config['mongo']['host'],      \
			config['mongo']['port'],      \
			config['mongo']['user'],      \
			config['mongo']['password'],  \
			config['mongo']['database'],  \
			config['mongo']['collection'] \
		)
		returndict = collection.top_entities({'hashtags':5})
		self.assertTrue(isinstance(returndict, dict))

	def test_base_top_entities_returns_hashtags(self):
		collection = MongoCollection(     \
			config['mongo']['host'],      \
			config['mongo']['port'],      \
			config['mongo']['user'],      \
			config['mongo']['password'],  \
			config['mongo']['database'],  \
			config['mongo']['collection'] \
		)
		returndict = collection.top_entities({'hashtags':5})
		self.assertTrue('hashtags' in returndict)

	def test_base_top_entities_returns_hashtags_and_media(self):
		collection = MongoCollection(     \
			config['mongo']['host'],      \
			config['mongo']['port'],      \
			config['mongo']['user'],      \
			config['mongo']['password'],  \
			config['mongo']['database'],  \
			config['mongo']['collection'] \
		)
		returndict = collection.top_entities({'user_mentions':5, 'media':3})
		self.assertTrue('user_mentions' in returndict and 'media' in returndict)

	def test_base_top_entities_returns_counts(self):
		collection = MongoCollection(     \
			config['mongo']['host'],      \
			config['mongo']['port'],      \
			config['mongo']['user'],      \
			config['mongo']['password'],  \
			config['mongo']['database'],  \
			config['mongo']['collection'] \
		)
		returndict = collection.top_entities({'urls':5, 'symbols':3})
		if len(returndict['urls']) > 0:
			self.assertTrue(len(returndict['urls']) == 5)
		if len(returndict['symbols']) > 0:
			self.assertTrue(len(returndict['symbols']) == 3)

	def test_limit_is_set(self):
		collection = MongoCollection(     \
			config['mongo']['host'],      \
			config['mongo']['port'],      \
			config['mongo']['user'],      \
			config['mongo']['password'],  \
			config['mongo']['database'],  \
			config['mongo']['collection'] \
		)
		collection.set_limit(5)
		self.assertEqual(5, collection.limit)
		collection.set_limit(0)

	def test_limit_actually_limits(self):
		collection = MongoCollection(     \
			config['mongo']['host'],      \
			config['mongo']['port'],      \
			config['mongo']['user'],      \
			config['mongo']['password'],  \
			config['mongo']['database'],  \
			config['mongo']['collection'] \
		)
		collection.get_iterator()
		count = len([tweet for tweet in collection.set_limit(5).get_iterator()])
		self.assertEqual(5, count)

	def test_filter_is_set(self):
		collection = MongoCollection(     \
			config['mongo']['host'],      \
			config['mongo']['port'],      \
			config['mongo']['user'],      \
			config['mongo']['password'],  \
			config['mongo']['database'],  \
			config['mongo']['collection'] \
		)
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
