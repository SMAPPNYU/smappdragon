import pymongo

from smappdragon.tools.tweet_parser import TweetParser
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
		tweet_parser = TweetParser()
		mongo_cursor = self.mongo_collection.find( \
			filter=self.filter, \
			no_cursor_timeout=False, \
			limit=self.limit \
		)
		for tweet in mongo_cursor:
			if tweet_parser.tweet_passes_custom_filter_list(self.custom_filters, tweet):
				if self.should_strip:
					yield tweet_parser.strip_tweet(self.keep_fields, tweet) 
				else: 
					yield tweet
		mongo_cursor.close()
