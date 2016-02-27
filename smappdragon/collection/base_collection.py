import abc
import operator
from ..tools.tweet_parser import TweetParser

class BaseCollection(object):
	__metaclass__ = abc.ABCMeta

	@abc.abstractmethod
	def __init__(self):
		pass

	'''
		returns a list of test values for all 
		tweets, should return a dictionary
	'''
	def get_texts(self):
		return [tweet[text] for tweet in self]

	'''
		returns a dictionary with
		counts for the number of 
		top entities requested
	'''
	def top_entities(self, requested_entities):
		returndict = {}
		returnstructure = {}
		tweet_parser = TweetParser()
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
			if len(returndict[entity_type]) < 1:
				returnstructure[entity_type] = {}
			else:
				sorted_list = sorted(returndict[entity_type].items(), key=operator.itemgetter(1), reverse=True)
				# if the user put in 0 return all entites
				# otherwise slice the array and return the
				# number of top things they asked for
				if requested_entities[entity_type] == 0:
					returnstructure[entity_type] = {name: count for name, count in sorted_list}
				else:
					returnstructure[entity_type] = {name: count for name, count in sorted_list[0:requested_entities[entity_type]]}
		return returnstructure


	def get_ngrams(self, tweet, requested_ngrams):
		returndict = {}
		#each of these being fed to get_cleaned_tokens
		#is a boolean value stored in the dictionary
		tokens = TweetParser.tokenize_tweet(tweet)
		for ngram in requested_ngrams:
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
		return returndict
