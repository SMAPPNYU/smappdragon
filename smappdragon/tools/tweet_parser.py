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
        for tweet_tuple in self.flatten_dict(tweet):
            flat_tweet_list.append(tweet_tuple)
        for filter_tuple in self.flatten_dict(filter_obj):
            if filter_tuple not in flat_tweet_list:
                return False
        return True

    '''
        get a list where each element in the list
        is a tuple that contains, (['path','to','value'], value_at_path)
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

    '''
        pulls out the columns from a tweet, usually used for making
        tweets into a fixed schema/csv/sql table/columnd based data
        structure, used for csv dump and sqlite db generation
    '''
    def parse_columns_from_tweet(self, tweet, columns):
        def return_val_for_column(tweet, columns):
            temp_tweet = {}
            for sub_field in columns:
                if temp_tweet == {}:
                    temp_tweet = tweet
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
        ret_columns = []
        for field in columns:
            split_field = field.split('.')
            ret_columns.append((field,return_val_for_column(tweet, split_field)))
        return ret_columns

'''
author @yvan
tweet parser is a tool for making tweet filters
'''