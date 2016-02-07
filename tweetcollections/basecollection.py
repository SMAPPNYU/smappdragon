import gzip
from bson import BSON
from abc import ABCMeta, abstractmethod
from collections import Counter, defaultdict
from smappPy.text_clean import get_cleaned_tokens
from smappPy.entities import get_urls, get_links, get_image_urls, get_users_mentioned, get_hashtags

'''
THE REASON EVERYTHING USES A pd.Series is so it can be graphed. That is so kind of dumb. Like the graph software should be the part
of the code that takes a standard input and makes it into a pd.Series. The rest of the code shouldn't confrorm to makeing pd.Series 
just for the graph component. This is so backwards.

count_by needs to be offered in more breakdowns that days hours minutes, weeks, months, years need to be added.

this is so retarded. the aggregator object is an iterator. and it's not JSON serializable. ok seriously. 
groups need to be serailizable, streamable, everythingable. this is broken in my opinion.

ok serously. you can't stream groups to count()? this is ridiculous. you have to calculate the lenth of the list of tweets. 
you need to be able to stream everu function into other functions. this is bad.

non of the formats of anything being returned by the toolkit is documented. if you do:

for timeslice, tweetlist in bsoncollection.since(datetime(2015, 8, 31)).until(datetime(2015, 9, 28)).containing('Benghazi', 'benghazi', 'BENGHAZI').group_by('days'):

	you have no idea what format the time slice is in. it's just not documented and it causes crashes. everything returned by 
	the toolkit should be a streamble form of JSON thing that can be converted to a stanard return dictionary

yeah like everyhting needs to export a dictionary or have a method for proper exporting. right now i make groups and then there is no easy
way to export them as a json, i have to write all that logic myself and it's really dumb. each method should export a json and that JSON should
be easily writable to a file with appednable method.

There's a crash / bug in the aggregator 

"start_time referenced before assignment. great.  in teh aggregator file."
cant see line or rest of stack because TMUX

everything needs to return the same datatype in the smapp-toolkit. a dictionary or an iterator or a dictionary or something.

apply_labels needs to be streamble into the next section. apply_labels should not direclty dump the stuff.

whether or not inputs to a method are case sensitive, emoji sensitive, punctuation sensitive, should be in the docs

a use for the filter function could be to log data as it's streaming. like function(){print tweet return tweet}, print it out and stream on through.

I think we should stay away from all iterators. group_by returns an iterator and it's SUPER slow.
term_counts does the same thing but has no iterator and it's fast as shit? mhhhhm...this doesn't seem to make any sense.

Ability to create a BSONTweetCollection from more than one bson file. Like just auto merge them instead of having
to run a script like 5 times.

instead of cloning filters and then applying one pass throug the object like 'for tweet in self:'

EACH method applies 'for tweet in self:' changes each tweet. then returns self again or it returns
a brand new iterator with all the new tweets /objects(instead of a new iterator with just a new filter stored in it).

now to accomplish this we either write it back to disk over the old file (eh) or.... uh...

this will make everything streamable if eveyr function does this.

Ok everything needs a log that prints what's happening for each operation so flow can be tracked.

without logs we can't tell where something breaks, if something breaks, or if the query is just not returning any results.

if queries return totally empty that should issue a logger warning or something.

the reason i say this is because if you launch a query for a date range...one some functions the toolkit doesn't work (group_by) on other
functions it might just return nothing (term_counts) this gets confusing and causes us to waste lots of time.

The other thing is that the person running the software shouldn't need to know any gritty details about the underlying data.
like i should need to know that tweets_1 wouldn't contain anything from the last week because it was 4 months ago. like I should query the 
data and the toolkit should tell me what is happening. instead of being a black box that sometiems works, sometimes breaks and sometimes says nothing.

so the previous toolkit held that we need to use iterators to be "efficient" but like half the time we're returning a large list comprehension of all tweets
that's gonna cause them to be stored in memory.

unit tests for 5 most common functions. count, containing, since, until, 

one of the only reasons an iterator file was use was to be able to return copied iterator objects with
new filters in them. decode file iter just returns an iterator that reads a thing line by line.

ability to take more than one BSON file is just multiple calls to decode_file_iter

on old toolkit:

sorting doesn't work on a BSON collection.

sample may not work

term counts is screwed up, returns different data formats (and a messed up _total field) 

completely annihilate __getattr__ it's horrible. It's a rewrite/abuse of a feature of pyhton.

google doc with stuff to keep in mind for toolkit: 

https://docs.google.com/document/d/1_u5skWVK9nRFHdiUhsZ_CIH56r3XveQn9BfO5WSrjvU/edit

we desperately need a function that will allow us to "Trim" down a tweet object and only
retain certain field in the tweet object and then output those tweet objects to CSV or wtvr.
BAsically a trim function.

sampling based on random #s in the DB doesn't work. You sample 0.33 on a DB with millions of tweets
and expect to get tons of stuff back and you get 7000 things back. That clearly means the random #
method is not returning the appropriate # of things. To be fair I used this in conjunction with the limit
filter which might affect something. 

The limit filter doesn't fucking work. You tell it to get you 30,000 things and it actually gets you 45,000 things.

replacement for
https://github.com/SMAPPNYU/smapp-toolkit/blob/master/smapp_toolkit/twitter/base_tweet_collection.py
'''

## Declare a class that inherits from object
class BaseCollection (object) :

	## declare this class to be an 
	## abstract base class (ABC)
	__metaclass__ = ABCMeta

	## declare an init method that
	## will be defined in a child class
	@abstractmethod
	def __init__ (self) :
		pass

	'''
	this is a very basic map function that will allow us
	to apply any function to the tweet data.
	Everything else in here is like a more specific
	map function.

	perform ref: http://stackoverflow.com/questions/803616/passing-functions-with-arguments-to-another-function-in-python
	'''
	def map(function, *args):
		function(*args)

	'''
	returns a list of test values for all 
	tweets, should return a dictionary
	'''
	def get_texts(self):
		return [tweet[text] for tweet in self]

	'''
	method that takes in a bsoncollection or mongocollection and outputs a bson file.
	yes the method lacks any back propagation to the database. I really don't see this 
	as a problem given that the entire structure of the original toolkit was a one way 
	data dump from the database to local machine, should take a dictionary input.
	'''
	def apply_labels(self, list_of_labels, list_of_fields, list_for_values, bsonoutputpath) :
		'''
		This method applies labels chosen by the user to collection objects.
		Read the docs in the README.md to see how it works
		'''

		for tweet in self:
			tweet_should_be_labeled = 0
			##for each field in the list of fields we're looking for
			for i, each_field in enumerate(list_of_fields):
				##split the field names so that user.id becomes user id
				split_field = each_field.split('.')
				tweet_ref = tweet
				## take "user" and "id" and navigate into the structure of the tweet
				for field_level in split_field: 
					tweet_ref = tweet_ref[field_level]
				## if the value we want to match is equal to the field or a substring of the field
				## (text and user description) match it
				try:
					for list_value in list_for_values[i]:
						if tweet_ref and list_value in tweet_ref: 
							tweet_should_be_labeled = 1
				except Exception as e:
					print "tweet_ref that threw error {}".format(tweet_ref)
					print "Error for a certain field {}, trying non iterable...".format(e)
					try:
						if tweet_ref in list_for_values[i]:
							tweet_should_be_labeled = 1
					except Exception as e:
						print "Non iterable method also failed, this one can't be labeled. Error: {}".format(e)
			if tweet_should_be_labeled:
				tweet['labels']= {}
				##add the labels to the tweet objects##
				for i, label_name in enumerate(list_of_labels[0]):
					tweet['labels'][str(i)] = {}
					tweet['labels'][str(i)]['name'] = list_of_labels[0][i]
					tweet['labels'][str(i)]['type']= list_of_labels[1][i]

	'''
	replacement for all ngrams methods
	the idea is to simplify this down.
	so that there are no special methods
	for certain numbers of ngrams

	CHANGE METHOD TO TAKE ONE DICTIONARY INPUT
	REQUESTED ENTITIES
	'''
	def top_ngrams(self, ngram, n, hashtags, mentions, rts, mts, https):
		#create a counter
		counts = Counter()
		#go through each tweet
		for tweet in self:
			#get tokens 
			tokens = get_cleaned_tokens(
				tweet['text']
				,keep_hashtags=hashtags
				,keep_mentions=mentions
				,rts=rts
				,mts=mts
				,https=https
				,stopwords=stopwords
				)
			#get the ngrams
			ngrams = zip(*[tokens[i:] for i in range(ngram)])
			strgram = ' '.join(str(ngram) for ngram in ngrams)
			gramindex = '{}-grams'.format(ngram)
			#get the counts
			counts[gramindex] = strgram
		#if the counter is empty
		#return empty series
		if len(counter) < 1:
			return pd.Series()
		#if the number given
		#is not empty
		if n:
			#set names and counts to 
			names, counts = zip(*counter.most_common(n))
		else:
			names, counts = zip(*counter.items())
		return pd.Series(counts, index=names)

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
		for tweet in self:

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

	'''
	counts the # of languages on a tweet object.
	'''
	def languagecounts(self, languages=['en', 'other']):
		languagecounts = Counter()
		for tweet in self:
			languagecounts[tweet['lang']] += 1
		if 'other' in languages:
			sumvar = 0
			for language in languagecounts:
				if language not in languages:
					sumvar += languagecounts[language]
			languagecounts['other'] = sumvar
		finalcount = []
		for language in languages:
			finalcount.extend(languagecounts[language])
		return pd.Series(finalcount, index=languages)

	'''
	counts the # of unique users in a collection
	'''
	def uniqueusers(self):
		uids = set()
		for tweet in self:
			uids.add(tweet['user']['id'])
		return pd.Series([len(uids)], index=['uniqueusers'])

	'''
	END POINT FUNCTIONS
	results cannot be streamed
	into another function call
	'''

	def dumpjson(self, filename, append=False, pretty=False):
		if append:
			handle = open(filename, "a")
		else:
			handle = open(filename, "w")
		if pretty:
			for tweet in tweets:
				handle.write(json_dumps(tweet, indent=4, separators=(',', ': ')) + "\n")
		else:
			for tweet in tweets:
				handle.write(json_dumps(tweet) + "\n")
		handle.close()

	def dumpbson(self, filename, append=False):
		if append:
			handle = open(filename, "ab")
		else:
			handle = open(filename, "wb")
		for tweet in tweets:
			handle.write(BSON.encode(tweet))
		handle.close()

	def dumpcsv(self, filename, columns=['id_str', 'user.screen_name', 'timestamp', 'text']):
		if(filename.endswith('.gz')):
			outfile = gzip.open(filename, 'w')
		else:
			outfile = open(filename, 'w')
		try:
			writer = UnicodeWriter(outfile)
			writer.writerow(columns)
			for tweet in self:
				row = list()
				for col_name in columns:
					path = col_name.split('.')
					try:
						value = tweet[path.pop(0)]
						for p in path:
							if isinstance(value, list):
								value = value[int(p)]
							else:
								value = value[p]
					except:
						value = ''
					value = unicode(value)
					row.append(u','.join(unicode(v) for v in value) if isinstance(value, list) else unicode(value))
				writer.writerow(row)
		finally:
			outfile.close()
