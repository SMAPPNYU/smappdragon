import unittest
from tests.config import config
from smappdragon import MongoCollection

class TestMongoCollection(unittest.TestCase):

	def test_iterator_returns_tweets(self):
        collection = MongoCollection(     \
            config['mongo']['host'],      \
            config['mongo']['port'],      \
            config['mongo']['user'],      \
            config['mongo']['password'],  \
            config['mongo']['database'],  \
            config['mongo']['collection'] \
        )
		self.assertTrue(len(list(collection.set_limit(10).get_iterator())) > 0)

if __name__ == '__main__':
	unittest.main()

'''
read about twitter entities here:
https://dev.twitter.com/overview/api/entities-in-twitter-objects
'''

