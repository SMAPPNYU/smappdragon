import os
import csv

from smappdragon.tools.tweet_parser import TweetParser
from smappdragon.collection.base_collection import BaseCollection

class CsvCollection(BaseCollection):
	'''
		method that tells us how to
		create the CsvCollection object
	'''
	def __init__(self, filepath):
		BaseCollection.__init__(self)
		self.filepath = filepath
		if not os.path.isfile(filepath):
			raise IOError(filepath, 'CsvCollection could not find your file, it\'s mispelled or doesn\'t exist.')

	'''
		method that creates a cursor
		and yields all tweets in a particular collection
	'''
	def get_iterator(self):
		tweet_parser = TweetParser()
		csv_handle = open(self.filepath, 'r', encoding='utf-8')
		for count, tweet in enumerate(csv.DictReader(csv_handle)):
			if self.limit < count+1 and self.limit != 0:
				csv_handle.close()
				return
			elif tweet_parser.tweet_passes_filter(self.filter, tweet) \
			and tweet_parser.tweet_passes_custom_filter_list(self.custom_filters, tweet):
				if self.should_strip:
					yield tweet_parser.strip_tweet(self.keep_fields, tweet) 
				else: 
					yield tweet
		csv_handle.close()
