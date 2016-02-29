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
	'''
	def tweet_passes_filter(filter, tweet):
		# iterate through all our filters
		# and build out index paths
		list_of_nested_indexes = []
		self.get_key_list(filter, list_of_nested_indexes)
		if self.filter == {}:
			return true

	'''
		get a list of lists that contains the 
		keys that are in our filter.
	'''
	def get_key_list(filter_obj, global_list, sublist=[]):
	    if isinstance(filter_obj, dict):
	        for k, v2 in filter_obj.items():
	            sublist.append(k)
	            get_key_list(v2, sublist)
	    else:
	    	global_list.append(sublist)
