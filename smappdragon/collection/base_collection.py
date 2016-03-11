import abc
import json
import operator
import unicodecsv

from bson import BSON, json_util
from smappdragon.tools.tweet_parser import TweetParser

class BaseCollection(object):
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def __init__(self):
		self.limit = 0
		self.filter = {}
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
		filehandle = open(output_json, 'ab+')

		for tweet in self.get_iterator():
			filehandle.write(json.dumps(tweet, default=json_util.default)+'\n')
		filehandle.close()

	'''
		dumps the contents of a collection 
		csv format
	'''
	def dump_to_csv(self, output_csv):
		count = 0
		tweet_parser = TweetParser()
		filehandle = open(output_csv, 'ab+')
		writer = unicodecsv.writer(filehandle)

		for tweet in self.get_iterator():
			row_to_write = []
			flat_tweet_list = []

			for flat_entry in tweet_parser.flatten_dict(tweet):
				flat_tweet_list.append(flat_entry)

			# split list of tuples into
			# two lists and grab the first list
			key_paths = zip(*flat_tweet_list)[0]

			if count == 0:
				writer.writerow(['.'.join(key_path) for key_path in key_paths])
				count += 1

			for tweet_tuple in flat_tweet_list:
				row_to_write.append(unicode(tweet_tuple[1]))
			row_to_write = [column or u'' for column in row_to_write]
			writer.writerow(row_to_write)
		filehandle.close()

	'''
		returns a dictionary with
		counts for the number of
		top entities requested
	'''
	def top_entities(self, requested_entities):
		returndict = {}
		returnstructure = {}
		tweet_parser = TweetParser()
		#init dempty dict for all entity types
		for entity_type in requested_entities:
			returndict[entity_type] = {}

		for tweet in self.get_iterator():
			for entity_type in requested_entities:
				for entity in tweet_parser.get_entity(entity_type, tweet):
					if entity_type == 'user_mentions':
						entity_value = tweet_parser.get_entity_field('id_str', entity)
					elif entity_type == 'hashtags' or entity_type == 'symbols':
						entity_value = tweet_parser.get_entity_field('text', entity)
					else:
						entity_value = tweet_parser.get_entity_field('url', entity)

					if entity_value in returndict[entity_type]:
						returndict[entity_type][entity_value] += 1
					else:
						returndict[entity_type][entity_value] = 1

		for entity_type in returndict:
			returnstructure[entity_type] = {}
			if len(returndict[entity_type]) > 0:
				sorted_list = sorted(returndict[entity_type].items(), key=operator.itemgetter(1), reverse=True)
				# if the user put in 0 return all entites
				# otherwise slice the array and return the
				# number of top things they asked for
				# if the list is too short throw in None
				if requested_entities[entity_type] == 0:
					returnstructure[entity_type] = {name: count for name, count in sorted_list}
				elif len(sorted_list) < requested_entities[entity_type]:
					returnstructure[entity_type] = {name: count for name, count in sorted_list}
					for i in range(0, requested_entities[entity_type]-len(sorted_list)):
						returnstructure[entity_type][i] = None
				else:
					returnstructure[entity_type] = { \
						name: count for name, count in sorted_list[0:requested_entities[entity_type]] \
					}
		return returnstructure
