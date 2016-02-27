import pymongo
from base_collection import BaseCollection

'''
replacement for: 
https://github.com/SMAPPNYU/smapp-toolkit/blob/master/smapp_toolkit/twitter/mongo_tweet_collection.py
'''

class MongoCollection(BaseCollection):
	'''
		method that tells us how to 
		create the MongoCollection object
	'''
	def __init__(self, address, port, username, password, database_name, collection_name):
		self.limit = 0
		self.mongo = pymongo.MongoClient(address, int(port))
		self.mongo_database = self.mongo[database_name]
		self.mongo_collection = self.mongo_database[collection_name]
		if username and password:
			self.mongo_database.authenticate(username, password)

	'''
		method that creates a cursor
		and yields all tweets in a particular collection
	'''
	def get_iterator(self):
		mongo_cursor = pymongo.cursor.Cursor(self.mongo_collection, self.filters(), no_cursor_timeout=True, limit=self.limit)
		try:
			for tweet in mongo_cursor:
				yield tweet
		finally:
			mongo_cursor.close()
	'''
	    Only return `count` tweets from the collection. Note: this takes tweets from the
	    beginning of the collection(s)
	    Example:
	    ########
	    collection.limit(5).texts()
	'''
	def limit(self, tweet_limit):
		self.limit = tweet_limit
		return self

	def filters(self):
		return {}
