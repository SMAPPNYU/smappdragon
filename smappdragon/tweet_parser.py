'''
read about twitter entities here
https://dev.twitter.com/overview/api/entities-in-twitter-objects
'''

'''
    returns True if tweet contains one or more entities (hashtag, url, or media)
'''
def contains_entity(entity_type, tweet):

    if "entities" not in tweet:
        return False
    elif entity_type in tweet["entities"] and len(tweet["entities"][entity_type]) > 0:
    	return True
    else:
    	return False
'''
    returns True if tweet contains one or more entities (hashtag, url, or media)
'''
def get_entity(entity_type, tweet):
    if contains_entity(entity_type, tweet):
        return [entity for entity in tweet["entities"][entity_type]]
    return []

def get_entity_field(field, entity):
	if field in entity:
		return entity[field]
	else:
		return None

'''
	so this says 'match everything that's not alphanumeric + underscore'
  	\w matches any alphanumeric character and underscore
   	^ inverts the meaning of the regular expression
 	\s matches any whitespace chars
    unicode flags are set with re.U
'''
def remove_all_punctuation(text):
    return re.sub(r'[^\w\s]', '', text, flags=re.U)

