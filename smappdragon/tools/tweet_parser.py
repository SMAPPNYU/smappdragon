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
		tests a tweet to see if it passes a 
		custom filter method, this just returns the
		value of the filter method passed in
	'''
	@staticmethod
	def tweet_passes_custom_filter(function, tweet):
		return function(tweet)

	'''
		removes all the the specified field from a tweet
	'''
	@staticmethod
	def strip_tweet(keep_fields, tweet):
		stripped_tweet = {}
		expanded_fields = [field_path.split('.') for field_path in keep_fields]
		for expanded_field in expanded_fields:
			prev = {}
			prev_tweet = {}
			temp_iteration_dict = {}
			for count, field in enumerate(expanded_field):
				#if its a top level field
				if field in tweet:
					if count+1 == len(expanded_field):
						temp_iteration_dict[field] = tweet[field]
					else: 
						temp_iteration_dict[field] = {}
					prev_tweet = tweet[field]
					prev = temp_iteration_dict[field]
				# if its a mid level field
				elif field in prev_tweet:
					if count+1 == len(expanded_field):
						prev[field] = prev_tweet[field]
					else: 
						prev[field] = {}
					prev_tweet = prev_tweet[field]
					prev = prev[field]
			# merge into main dict
			c = temp_iteration_dict.copy()
			stripped_tweet.update(c)
		return stripped_tweet

	'''
		just tests multiple custom filters
		see, tweet_passes_custom_filter
	'''
	def tweet_passes_custom_filter_list(self, function_list, tweet):
		for function in function_list:
			if not self.tweet_passes_custom_filter(function, tweet):
				return False
		return True

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
		for tweet_tuple in self.list_flat_json(tweet):
			flat_tweet_list.append(tweet_tuple)
		for filter_tuple in self.list_flat_json(filter_obj):
			if filter_tuple not in flat_tweet_list:
				return False
		return True

	'''
		flattens json {"blah": {"txt":"t"} , "z": [5, "g", "5.6"]} -> 
		kudos: https://medium.com/@amirziai/flattening-json-objects-in-python-f5343c794b10#.hgkmqsawh
	'''
	@staticmethod
	def flatten_json(y):
	    out = {}
	    def flatten(x, name=''):
	        if type(x) is dict:
	            for a in x:
	                flatten(x[a], name + a + '.')
	        elif type(x) is list:
	            i = 0
	            for a in x:
	                flatten(a, name + str(i) + '.')
	                i += 1
	        else:
	            out[name[:-1]] = x
	    flatten(y)
	    return out

	'''
		get a list of tuples of flattened json
		better for searching
	'''
	@staticmethod
	def list_flat_json(flat_dict_obj):
		for key, value in flat_dict_obj.items():
			out = ()
			out[0] = key.split('.')
			out[1] = value
			yield out
