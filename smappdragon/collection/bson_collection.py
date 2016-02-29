import os
import bson
from smappdragon.tools.tweet_parser import TweetParser
from smappdragon.collection.base_collection import BaseCollection

class BsonCollection(BaseCollection):
	'''
		method that tells us how to
		create the BsonCollection object
	'''
	def __init__(self, filepath):
		self.filepath = filepath
		if not os.path.isfile(filepath):
			raise IOError(filepath, 'BsonCollection could not find your file, it\'s mispelled or doesn\'t exist.')

	'''
		method that creates a cursor
		and yields all tweets in a particular collection
	'''
	def get_iterator(self):
		count = 0
		tweet_parser = TweetParser()
		bson_handle = open(self.filepath, 'rb')
		for tweet in bson.decode_file_iter(bson_handle):
			if self.limit > count:
				raise StopIteration
			elif self.tweet_parser.tweet_passes_filter(self.filter, tweet):
				count += 1
				yield tweet
		bson_handle.close()
