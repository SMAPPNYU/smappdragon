import pymongo

from smappdragon.tools.tweet_parser import TweetParser
from smappdragon.collection.base_collection import BaseCollection

class MongoCollection(BaseCollection):
	'''
		method that tells us how to
		create the MongoCollection object
		*args -> address, port, username, password, database_name, collection_name
	'''
	def __init__(self, *args, **kwargs):
		BaseCollection.__init__(self)
		if 'passed_mongo' in kwargs:
			self.mongo = kwargs['passed_mongo']
			self.mongo_database = self.mongo[args[2]]
			if args[0] and args[1]:
				self.mongo_database.authenticate(args[0], args[1])
			self.mongo_collection = self.mongo_database[args[3]]
		else:
			self.mongo = pymongo.MongoClient(args[0], int(args[1]))
			self.mongo_database = self.mongo[args[4]]
			if args[2] and args[3]:
				self.mongo_database.authenticate(args[2], args[3])
			self.mongo_collection = self.mongo_database[args[5]]

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
