import os

from bson import json_util
from smappdragon.tools.tweet_parser import TweetParser
from smappdragon.collection.base_collection import BaseCollection

class JsonCollection(BaseCollection):
	'''
		method that tells us how to
		create the JsonCollection object
	'''
	def __init__(self, filepath):
		BaseCollection.__init__(self)
		self.filepath = filepath
		if not os.path.isfile(filepath):
			raise IOError(filepath, 'JsonCollection could not find your file, it\'s mispelled or doesn\'t exist.')

	'''
		method that creates a cursor
		and yields all tweets in a particular collection
		expects a json object on each line
		no spaghetti string
	'''
	def get_iterator(self):
		count = 1
		tweet_parser = TweetParser()
		json_handle = open(self.filepath, 'r')
		for tweet in json_handle:
			tweet = json_util.loads(tweet)
			if self.limit != 0 and self.limit <= count:
				return
			elif tweet_parser.tweet_passes_filter(self.filter, tweet) \
			and tweet_parser.tweet_passes_custom_filter_list(self.custom_filters, tweet):
				count += 1
				yield tweet
		json_handle.close()
