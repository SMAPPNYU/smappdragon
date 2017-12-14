import os
import gzip
import bz2

from bson import json_util
from smappdragon.tools.tweet_parser import TweetParser
from smappdragon.collection.base_collection import BaseCollection, binary_mode

class JsonCollection(BaseCollection):
	'''
		method that tells us how to
		create the JsonCollection object
	'''
	def __init__(self, filepath, compression=None, encoding='utf-8', throw_error=1, 
                 mode='r', verbose=1):
		BaseCollection.__init__(self)
		self.filepath = filepath
		self.compression = compression
		self.encoding = encoding
		self.throw_error = throw_error
		self.verbose = verbose
		self.mode = mode

		if not os.path.isfile(filepath):
			raise IOError(filepath, 'JsonCollection could not find your file, it\'s mispelled or doesn\'t exist.')

	'''
		method that creates a cursor
		and yields all tweets in a particular collection
		expects a json object on each line
		no spaghetti string
	'''
	def get_iterator(self):
		tweet_parser = TweetParser()
<<<<<<< HEAD
		if self.compression == 'bz2':
			self.mode = binary_mode(self.mode)
			json_handle = bz2.open(self.filepath, self.mode, encoding=self.encoding)
		elif self.compression == 'gzip':
			self.mode = binary_mode(self.mode)
			json_handle = gzip.open(self.filepath, self.mode, encoding=self.encoding)
=======
		file_extension = self.filepath.split('.')[-1]
		if file_extension == 'bz2':
			json_handle = bzopen(self.filepath, 'r', encoding='utf-8')
		elif file_extension == 'gz':
			json_handle = gzip.open(self.filepath,'r', encoding='utf-8')
>>>>>>> f8e4d25f468a6a974d3d27f2ff40413918756b57
		else:       
			json_handle = open(self.filepath, self.mode, encoding=self.encoding)
		bad_lines = 0
		for count, tweet in enumerate(json_handle):
			if not self.throw_error:
				try:
					tweet = json_util.loads(tweet)
				except: # records 
					bad_lines += 1
					pass
			else:
				tweet = json_util.loads(tweet)
			if self.limit != 0 and self.limit <= count:
				return
			elif tweet_parser.tweet_passes_filter(self.filter, tweet) \
			and tweet_parser.tweet_passes_custom_filter_list(self.custom_filters, tweet):
				if self.should_strip:
					yield tweet_parser.strip_tweet(self.keep_fields, tweet) 
				else: 
					yield tweet
		if self.verbose and not self.throw_error:
			print("{} rows are corrupt.".format(bad_lines))
		json_handle.close()
