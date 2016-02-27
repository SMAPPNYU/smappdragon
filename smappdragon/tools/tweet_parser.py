'''
read about twitter entities here
https://dev.twitter.com/overview/api/entities-in-twitter-objects
'''

class TweetParser(object):
	def __init__(self):
		pass
	'''
    	returns True if tweet contains one or more entities (hashtag, url, or media)
	'''
	def contains_entity(self, entity_type, tweet):

	    if "entities" not in tweet:
	        return False
	    elif entity_type in tweet["entities"] and len(tweet["entities"][entity_type]) > 0:
	    	return True
	    return False

	'''
	    get an entity from a tweet if it exists
	'''
	def get_entity(self, entity_type, tweet):
	    if self.contains_entity(entity_type, tweet):
	        return [entity for entity in tweet["entities"][entity_type]]
	    return []

	'''
		gets a particular field for an entity if it exists
	'''
	def get_entity_field(self, field, entity):
		# beacuse all entities are actually lists
		# of entity objects
		for entity_object in entity:
			if field in entity_object:
				return entity[field]
		return None
