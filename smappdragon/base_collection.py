import abc
from smappPy.text_clean import get_cleaned_tokens

## Declare a class that inherits from object
class BaseCollection (object) :

	## declare this class to be an 
	## abstract base class (ABC)
	__metaclass__ = abc.ABCMeta

	## declare an init method that
	## will be defined in a child class
	@abc.abstractmethod
	def __init__ (self) :
		pass

	'''
	returns a list of test values for all 
	tweets, should return a dictionary
	'''
	def get_texts(self):
		return [tweet[text] for tweet in self]

	'''
	Top things is a method for getting top things
	replaces many of the top_ methods we previously
	had.
	things requested is a dictionary containing
	entries with the thing to request (hashtags)
	and the number we want to reqesut (5) hashtags
	like so: {"hashtags":5, "links":10} SO much better
	than having like 15-20 boolean inputs lol.
	'''
	def top_entities(self, requested_entities):
		returndict = {}
		for tweet in self.:

			if requested_entities['urls']:
				for url in get_urls(tweet):
					returndict['urls'][url] += 1

			if requested_entities['imageurls']:
				for imageurl in get_image_urls(tweet):
					returndict['imageurls'][imageurl] += 1

			if requested_entities['hashtags']:
				for hashtag in get_hashtags(tweet):
					returndict['hashtags'][hashtag] += 1

			if requested_entities['mentions']:
				for mention in get_users_mentioned:
					returndict['mentions'][mention] += 1

			if requested_entities['geolocations']:
				if 'place' in tweet and tweet['place'] is not None:
					returndict['geolocations'][tweet['place']['full_name']] += 1
				else:
					returndict['geolocations'][None] += 1

			if requested_entities['userlocations']:
				if 'location' in tweet['user']:
					returndict['userlocations'][tweet['user']['location']] += 1
				else:
					returndict['userlocations'][None] += 1

			if requested_entities['ngrams']:
				#each of these being fed to get_cleaned_tokens
				#is a boolean value stored in the dictionary
				tokens = get_cleaned_tokens(tweet['text']
							,keep_hashtags = requested_entities['ngrams']['hashtags']
							,keep_mentions = requested_entities['ngrams']['mentions']
							,rts = requested_entities['ngrams']['retweets']
							,mts = requested_entities['ngrams']['mentions']
							,https = requested_entities['ngrams']['urls']
							,stopwords = requested_entities['ngrams']['stopwords']
					)
				for ngram in requested_entities['ngrams']['ngrams']:
					#get the ngrams for this particular ngram level 
					#unigram, bigram, tri gram; so this will get all the
					#bigrams for example from the tokens.
					thegrams = zip(*[tokens[i:] for i in range(ngram)])
					#create a single string with all the ngrams; this 
					#would combine all the bigrams into a string delimited by ' '
					strgram = ' '.join(str(thegram) for thegram in thegrams)
					#add this ngram string to the counter array
					#this takes that ngram string and stores it
					#at the index like so 2-grams
					gramindex = '{}-grams'.format(ngram)
					returndict[gramindex] = strgram
		returnstructure = {}
		for key in returndict:
			#if the counter is empty
			#return empty series
			if len(returndict[key]) < 1:
				returnstructure[key] =  pd.Series()
			##if it's not empty
			else:
				#if the number given
				#is not empty
				if requested_entities[key]['number']:
					#set names and counts to 
					names, counts = zip(*returndict[key].most_common(requested_entities[key]['number']))
				#if the number requested is empty
				#returns everything
				else:
					names, counts = zip(*returndict[key].items())
				returnstructure[key] =  pd.Series(counts, index=names)
		return returnstructure
