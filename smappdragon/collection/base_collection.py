import csv
import abc
import json
import operator

from bson import BSON, json_util
from smappdragon.tools.tweet_parser import TweetParser

class BaseCollection(object):
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def __init__(self):
		self.limit = 0
		self.filter = {}
		self.keep_fields = []
		self.should_strip = False
		self.custom_filters = []

	'''
		returns an iterator that
		can iterate through the tweets
		in a collection
	'''
	@abc.abstractmethod
	def get_iterator(self):
		pass

	'''
		sets the fields to keep when
		the user calls strip tweets
	'''
	def strip_tweets(self, keep_fields):
		self.keep_fields = keep_fields
		self.should_strip = True
		return self

	'''
		returns the modified collection
		object with a limit on how many tweets
		it will ever output or query
	'''
	def set_limit(self, limit):
		self.limit = limit
		return self

	'''
		sets the filters you'd
		like to apply to the query
		follows mongdb query syntax
	'''
	def set_filter(self, query_filter):
		self.filter = query_filter
		return self

	'''
		takes a function as an input
		and appends it to the list of
		custom filters that need to be passed
	'''
	def set_custom_filter(self, func):
		self.custom_filters.append(func)
		return self

	'''
		takes a function as an input
		and appends it to the list of
		custom filters that need to be passed
	'''
	def set_custom_filter_list(self, functions_list):
		self.custom_filters.extend(functions_list)
		return self

	'''
		dumps the contents of a collection 
		to a bson file, this is a binary format
	'''
	def dump_to_bson(self, output_bson):
		filehandle = open(output_bson, 'ab+')

		for tweet in self.get_iterator():
			filehandle.write(BSON.encode(tweet))
		filehandle.close()

	'''
		dumps the contents of a collection
		to a json file, a json object on
		each line, this not a binary format
	'''
	def dump_to_json(self, output_json):
		filehandle = open(output_json, 'a')

		for tweet in self.get_iterator():
			filehandle.write(json_util.dumps(tweet)+'\n')
		filehandle.close()

	'''
		dumps the contents of a collection 
		csv format,not having fields is very
		unwieldy
	'''
	def dump_to_csv(self, output_csv, input_fields):

		def return_val_for_column(tweet, columns):
		    temp_tweet = {}
		    for sub_field in columns:
		        if temp_tweet == {}:
		            temp_tweet = json.loads(json_util.dumps(tweet))
		        try:
		            if sub_field.isdigit():
		                sub_field = int(sub_field)
		            val = temp_tweet[sub_field]
		            if isinstance(val,dict) or isinstance(val,list):
		                temp_tweet = val
		                continue
		            else: 
		                if isinstance(val,str):
		                    val = val.replace('\n',' ').replace('\r',' ')
		                return val
		        except (KeyError, IndexError) as e:
		            return None
		            break

		filehandle = open(output_csv, 'w', encoding='utf-8')
		writer = csv.writer(filehandle)
		writer.writerow(input_fields)

		for tweet in self.get_iterator():
		    row_to_write = []
		    for field in input_fields:
		        split_fields = field.split('.')
		        ret = return_val_for_column(tweet, split_fields)
		        if isinstance(ret,str):
		            row_to_write.append(ret)
		        else:
		            row_to_write.append(ret)
		    writer.writerow(row_to_write)
		filehandle.close()
