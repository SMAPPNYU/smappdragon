import json
import unittest
from config import *
from smappdragon import MongoCollection

class TestMongoMethods(unittest.TestCase):

	def test_mongo_top_entities(self):
		print config
		collection = MongoCollection(config['mongo']['host'], config['mongo']['port'], config['mongo']['user'], config['mongo']['password'], config['mongo']['database'], config['mongo']['collection'])
		returnst = collection.top_entities({'hashtags':5})
		print json.dumps(returnst, indent=4)

if __name__ == '__main__':
	unittest.main()
