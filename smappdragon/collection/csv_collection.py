import os
import csv
import gzip
from bz2 import BZ2File as bzopen

from smappdragon.tools.tweet_parser import TweetParser
from smappdragon.collection.base_collection import BaseCollection

class CsvCollection(BaseCollection):
	'''
		method that tells us how to
		create the CsvCollection object
	'''
	def __init__(self, filepath):
		BaseCollection.__init__(self, compression=None, encoding='utf-8', on_error='throw', 
                                mode='r', verbose=0)
		self.filepath = filepath
		self.compression = compression
		self.encoding = encoding
		self.on_error = on_error
		self.verbose = verbose
		self.mode = mode
		if not os.path.isfile(filepath):
			raise IOError(filepath, 'CsvCollection could not find your file, it\'s mispelled or doesn\'t exist.')

	'''
		method that creates a cursor
		and yields all tweets in a particular collection
	'''
	def get_iterator(self):
		tweet_parser = TweetParser()
<<<<<<< HEAD
		if self.compression == 'bz2':
			self.mode = binary_mode(self.mode)
			csv_handle = bz2.open(self.filepath, self.mode, encoding=self.encoding)
		elif self.compression == 'gzip':
			self.mode = binary_mode(self.mode)
			csv_handle = gzip.open(self.filepath, self.mode, encoding=self.encoding)
		else:       
			csv_handle = open(self.filepath, self.mode, encoding=self.encoding)
=======
		file_extension = self.filepath.split('.')[-1]
		if file_extension == 'bz2':
			csv_handle = bzopen(self.filepath, 'r', encoding='utf-8')
		elif file_extension == 'gz':
			csv_handle = gzip.open(self.filepath,'r', encoding='utf-8')
		else:
			csv_handle = open(self.filepath, 'r', encoding='utf-8')
>>>>>>> f8e4d25f468a6a974d3d27f2ff40413918756b57
		for count, tweet in enumerate(csv.DictReader(csv_handle)):
			if self.limit < count+1 and self.limit != 0:
				csv_handle.close()
				return
			elif tweet_parser.tweet_passes_filter(self.filter, tweet) \
			and tweet_parser.tweet_passes_custom_filter_list(self.custom_filters, tweet):
				if self.should_strip:
					yield tweet_parser.strip_tweet(self.keep_fields, tweet) 
				else: 
					yield dict(tweet)
		csv_handle.close()
