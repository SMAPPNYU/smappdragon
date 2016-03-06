'''
read about twitter entities here
https://dev.twitter.com/overview/api/entities-in-twitter-objects
'''

class TweetParser(object):
	def __init__(self):
		pass
	'''
		get an entity from a tweet if it exists
	'''
	def get_entity(self, entity_type, tweet):
		if self.contains_entity(entity_type, tweet):
			return [entity for entity in tweet["entities"][entity_type]]
		return []

	'''
		returns True if tweet contains one or more entities (hashtag, url, or media)
	'''
	@staticmethod
	def contains_entity(entity_type, tweet):
		if "entities" not in tweet:
			return False
		elif entity_type in tweet["entities"] and len(tweet["entities"][entity_type]) > 0:
			return True
		return False

	'''
		gets a particular field for an entity if it exists
	'''
	@staticmethod
	def get_entity_field(field, entity):
		# beacuse all entities are actually lists
		# of entity objects
		for entity_object in entity:
			if field in entity_object:
				return entity[field]
		return None

	'''
		return true or false depends if
		tweet passes through the filter
		filters are just dictionaries.
		filter = mongo style query dict
	'''
	def tweet_passes_filter(self, filter_obj, tweet):
		if filter_obj == {}:
			return True
		# lists of tuples that
		# come from our dicts
		flat_tweet_list = []
		for tweet_tuple in self.flatten_dict(tweet):
			flat_tweet_list.append(tweet_tuple)
		for filter_tuple in self.flatten_dict(filter_obj):
			if filter_tuple not in flat_tweet_list:
				return False
		return True

	'''
		get a list of lists that contains the 
		keys that are in our filter and the value
		at the end of those keys. makes a list of tuples.
	'''
	def flatten_dict(self, dict_obj, path=None):
		if path is None:
			path = []
		if isinstance(dict_obj, dict):
			for key in dict_obj.keys():
				local_path = path[:]
				local_path.append(key)
				for val in self.flatten_dict(dict_obj[key], local_path):
					yield val
		else:
			yield path, dict_obj
