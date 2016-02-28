import pymongo
from smappdragon.collection.base_collection import BaseCollection

class MongoCollection(BaseCollection):
	'''
		method that tells us how to
		create the MongoCollection object
	'''
	def __init__(self, address, port, username, password, database_name, collection_name):
		BaseCollection.__init__(self)
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
		mongo_cursor = pymongo.cursor.Cursor( \
											self.mongo_collection, \
										 	self.get_filters(), \
											no_cursor_timeout=True, \
											limit=self.limit \
											)
		try:
			for tweet in mongo_cursor:
				yield tweet
		finally:
			mongo_cursor.close()
