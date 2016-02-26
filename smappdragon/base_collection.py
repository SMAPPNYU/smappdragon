import abc
import tweet_parser import TweetParser

## Declare a class that inherits from object
class BaseCollection(object):

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
		for tweet in self.get_iterator():

			for entity_type in requested_entities:
				for entity in TweetParser.get_entity(entity_type, tweet):
					if entity_type == 'user_mentions':
						returndict[entity_type][TweetParser.get_entity_field('id_str', entity)] += 1
					elif entity_type == 'hashtags' or entity_type == 'symbols':
						returndict[entity_type][TweetParser.get_entity_field('text', entity)] += 1
					else:
						returndict[entity_type][TweetParser.get_entity_field('url', entity)] += 1

			if requested_entities['ngrams']:
				#each of these being fed to get_cleaned_tokens
				#is a boolean value stored in the dictionary
				tokens = TweetParser.tokenize_tweet(tweet)
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
