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

'''
	returns all tweet hashtags as a list of strings (WITHOUT the '#' char)
'''
def get_hashtags(tweet):
    if contains_hashtag(tweet):
        return [hashtag["text"] for hashtag in tweet["entities"]["hashtags"]]
    return []

'''
	returns a list of the URLs in tweet (will return multiples if multiples exist in tweet)
'''
def get_urls(tweet):
    if contains_url(tweet):
        return [url["expanded_url"] for url in tweet["entities"]["urls"]]
    else:
        return []

'''
	return all 
'''
def get_media(tweet):
    if contains_media(tweet):
    	return [media["expanded_url"] for media in tweet["entities"]["media"]]
    else:
    	return []

'''
    takes a native tweet (dict). Returns list of all mentioned users in tuple form 
    (user id_str, user screen name), or empty list if none.
'''
def get_user_mentions(tweet):
    if not contains_mention(tweet):
        return []
    users = []
    for user_mention in tweet["entities"]["user_mentions"]:
        users.append(user)
    return users

def get_symbols(tweet):
    if not contains_mention(tweet):
        return []
    symbols = []
    for symbol in tweet["entities"]["symbols"]:
        symbols.append(symbol)
    return symbols

'''
	so this says 'match everything that's not alphanumeric + underscore'
  	\w matches any alphanumeric character and underscore
   	^ inverts the meaning of the regular expression
 	\s matches any whitespace chars
    unicode flags are set with re.U
'''
def remove_all_punctuation(text):
    return re.sub(r'[^\w\s]', '', text, flags=re.U)

