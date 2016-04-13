```
									 _
 ___ _ __ ___   __ _ _ __  _ __   __| |_ __ __ _  __ _  ___  _ __ 
/ __| '_ ` _ \ / _` | '_ \| '_ \ / _` | '__/ _` |/ _` |/ _ \| '_ \ 
\__ \ | | | | | (_| | |_) | |_) | (_| | | | (_| | (_| | (_) | | | |
|___/_| |_| |_|\__,_| .__/| .__/ \__,_|_|  \__,_|\__, |\___/|_| |_|
					|_|   |_|                    |___/
```

[![PyPI](https://img.shields.io/pypi/v/smappdragon.svg)](https://pypi.python.org/pypi/smappdragon) [![PyPI](https://img.shields.io/pypi/dm/smappdragon.svg)](https://pypi.python.org/pypi/smappdragon) [![PyPI](https://img.shields.io/pypi/l/smappdragon.svg)](https://github.com/SMAPPNYU/smappdragon/blob/master/LICENSE)

:dragon: smappdragon is a set of tools for working with twitter data. a more abstract wrapper for smappdragon can be found in [smappboa](https://github.com/SMAPPNYU/smappboa) (work in progress). [the old smapp-toolkit is here.](https://github.com/SMAPPNYU/smapp-toolkit)

- [collection](https://github.com/SMAPPNYU/smappdragon#collection)
	- [mongo_collection](https://github.com/SMAPPNYU/smappdragon#mongo_collection)
	- [bson_collection](https://github.com/SMAPPNYU/smappdragon#bson_collection)
	- [json_collection](https://github.com/SMAPPNYU/smappdragon#json_collection)
	- [csv_collection](https://github.com/SMAPPNYU/smappdragon#csv_collection)
	- [base_collection](https://github.com/SMAPPNYU/smappdragon#base_collection)
		- [get_iterator](https://github.com/SMAPPNYU/smappdragon#get_iterator)
		- [top_entities](https://github.com/SMAPPNYU/smappdragon#top_entities)
		- [set_limit](https://github.com/SMAPPNYU/smappdragon#set_limit)
		- [set_filter](https://github.com/SMAPPNYU/smappdragon#set_filter)
		- [set_custom_filter](https://github.com/SMAPPNYU/smappdragon#set_custom_filter)
		- [set_custom_filter_list](https://github.com/SMAPPNYU/smappdragon#set_custom_filter_list)
		- [dump_to_bson](https://github.com/SMAPPNYU/smappdragon#dump_to_bson)
		- [dump_to_json](https://github.com/SMAPPNYU/smappdragon#dump_to_json)
		- [dump_to_csv](https://github.com/SMAPPNYU/smappdragon#dump_to_csv)
- [tools](https://github.com/SMAPPNYU/smappdragon#tools)
	- [tweet_parser](https://github.com/SMAPPNYU/smappdragon#tweet_parser)
		- [contains_entity](https://github.com/SMAPPNYU/smappdragon#contains_entity)
		- [get_entity](https://github.com/SMAPPNYU/smappdragon#get_entity)
		- [get_entity_field](https://github.com/SMAPPNYU/smappdragon#get_entity_field)
		- [tweet_passes_filter](https://github.com/SMAPPNYU/smappdragon#tweet_passes_filter)
		- [flatten_dict](https://github.com/SMAPPNYU/smappdragon#flatten_dict)
		- [tweet_passes_custom_filter](https://github.com/SMAPPNYU/smappdragon#tweet_passes_custom_filter)
		- [tweet_passes_custom_filter_list](https://github.com/SMAPPNYU/smappdragon#tweet_passes_custom_filter_list)
		- [transform_tweet](https://github.com/SMAPPNYU/smappdragon#transform_tweet)
	- [mongo_query]()

##installation

`pip install smappdragon`

`pip install smappdragon --upgrade`

smappdragon runs in python 3. if you dont have this version of python, [install anaconda](https://www.continuum.io/downloads), [or miniconda](http://conda.pydata.org/miniconda.html), whatever you do we recommend at least python 3.0 .

(check python binary location with `which python`) 
should be `/usr/bin/python` (mac osx base install), `/usr/local/bin/python` (homebrew), `/Users/YOURNAME/miniconda3/bin/python` (miniconda), `/Users/YOURNAME/anaconda/bin/python` (anaconda)

(check with `python --version`)
if you are 2.X.X, you're out of date

##testing 

you absolutely need to write unit tests for any methods you add to smappdragon, this software needs to stay as stable as porssible as it will be the basis for other software.

this folder contains tests for smappdragon.

the `bson` folder contains two bson files on which to run tests. One if a valid.bson file with tweets that have properly formatted fields. Another is an sketchy.bson file that has tweets with strange fields, missing fields, etc.

our test covearge setup: https://github.com/coagulant/coveralls-python

##collection

classes for interfacing with a tweets from different data sources

##mongo_collection

this allows you to plug into a running live mongodb database and run smappdragon methods on the resulting collection object. 

abstract:
```python
from smappdragon import MongoCollection

collection = MongoCollection('HOST', PORT, 'USER_NAME', 'PASSWORD', 'DB_NAME', 'COLLECTION_NAME')
```

practical:
```python
from smappdragon import MongoCollection

collection = MongoCollection('superhost.bio.nyu.edu', 27574, smappReadWriteUserName, 'PASSWORD', 'GERMANY_ELECTION_2015_Nagler', 'tweet_collection_name')
```

*returns* a collection object that can have methods called on it

test: `python -m unittest tests.test_mongo_collection`

you should create a `config.py` file in the `tests` directory structured like so:

```python
config = {
	'mongo':{
		'host': 'HOSTNAME',
		'port': PORT,
		'user': 'DB_USER',
		'password': 'DB_PASS'
		'database': 'DB_NAME'
		'collection': 'COLLECTION_NAME'
	},
	'blah':{
		.
		.
		.
	}
}
```
this config is used for testing it is gitignored.

##bson_collection

this allows you to use any bson file as a data source for smappdragon

abstract:
```python
from smappdragon import BsonCollection

collection = BsonCollection('/PATH/TO/BSON/FILE.bson')
```

practical:
```python
from smappdragon import BsonCollection

collection = BsonCollection('~/Documents/file.bson')
```

*returns* a collection object can have methods called on it

test: `python -m unittest tests.test_bson_collection`

you should create a `config.py` file in the `tests` directory structured like so:

```python
config = {
	'blah':{
		.
		.
		.
	},
	'bson':{ \
        'valid': 'bson/valid.bson' \
    } \
}
```
this config is used for testing it is gitignored.

##json_collection

this allows you to use any json file (with a json object on each line) as a data source for smappdragon

abstract:
```python
from smappdragon import JsonCollection

collection = JsonCollection('/PATH/TO/JSON/FILE.json')
```

practical:
```python
from smappdragon import JsonCollection

collection = JsonCollection('~/Documents/file.json')
```

*returns* a collection object that can have methods called on it

test: `python -m unittest tests.test_json_collection`

you should create a `config.py` file in the `tests` directory structured like so:

```python
config = {
	'blah':{
		.
		.
		.
	},
	'json':{ \
        'valid': 'json/valid.json' \
    } \
}
```
this config is used for testing it is gitignored.

##csv_collection

this allows you to use any csv file (with a csv header) as a data source for smappdragon

abstract:
```python
```

practical:
```python
```

*returns* a collection object that can have methods called on it

test: `python -m unittest tests.test_csv_collection`

you should create a `config.py` file in the `tests` directory structured like so:

```python
config = {
	'blah':{
		.
		.
		.
	},
	'csv':{ \
        'valid': 'json/valid.csv' \
    } \
}
```
this config is used for testing it is gitignored.

##base_collection

this is the base class for all collection objects. methods that all collection objects use are found here. this is actually the most important class.

test: `python -m unittest tests.test_base_collection`

##get_iterator

makes an iterator that can iterate through all tweets in a particular collection

abstract / practical:
```python
collection.get_iterator()
```

*returns* an iterable object that will yield all the tweets in a particular collection

##top_entities

returns the top twitter entites from a tweet object, you can [read about twitter entities here](https://dev.twitter.com/overview/api/entities-in-twitter-objects)

abstract:
```python
collection.top_entities({'ENTITY_FIELD':NUMBER_OF_TOP_TERMS, 'ENTITY_FIELD':NUMBER_OF_TOP_TERMS, 'ENTITY_FIELD':NUMBER_OF_TOP_TERMS})
```

practical:
```python
collection.top_entities({'user_mentions':5, 'media':3, 'hashtags':5, 'urls':0, 'user_mentions':2, 'symbols':2})
# or
collection.top_entities({'hashtags':5})
```

*returns* a dictionary containing tho requested entities and the counts for each entity

input:
```python
print collection.top_entities({'user_mentions':5, 'media':3, 'hashtags':5})
```

output:
```
{
		"hashtags": {
				"JadeHelm": 118, 
				"pjnet": 26, 
				"jadehelm": 111, 
				"falseflag": 32, 
				"2a": 26
		},
		"user_mentions": {
				"1619936671": 41, 
				"27234909": 56, 
				"733417892": 121, 
				"10228272": 75, 
				"233498836": 58
		}, 
		"media": {
				"https://t.co/ORaTXOM2oX": 55, 
				"https://t.co/pAfigDPcNc": 27, 
				"https://t.co/TH8TmGuYww": 24
		}
}
```

*returns* a dictionary filled with the top terms you requested

note: passing 0 to a field like `'hashtags':0` returns all the hashtags

note: no support for extended entities, retweet entities, user entites, or direct message entities.

note: if not enough entity objects are returned they get filled into the dictionary with null like so:

```
{
	"symbols": {
			"0": null, 
			"1": null, 
			"hould": 1
	}
}
```

##set_limit

sets a limit on the number of documents a collection can return 

abstract:
```python
collection.set_limit(TWEET_LIMIT_NUMBER)
```

practical:
```python
collection.set_limit(10)
# or 
collection.set_limit(10).top_entities({'hashtags':10})
```

*returns* a collection object limited to querying / filtering only as many tweets as the limit number allows. a limit of 10 will only allow 10 tweets to be processed.

##set_filter

sets a filter to apply toa all tweets, the filter is a mongo style query dictionary

abstract:
```python
collection.set_filter(TWEET_FILTER)
```

practical:
```python
collection.set_filter({'id_str':'4576334'})
# or 
collection.set_filter({'id_str':'4576334', 'user':{'screen_name':'yvanscher'}}).top_entities({'hashtags':10})
```

*returns* a collection object that will only return tweets that match the specified filter. so if you ask for {`id_str`:`4576334`} you will only get tweets where the `id_str` field is `4576334`.

note: passing an empty filter will return all tweets in a collection, empty filters `{}` are like no filter.

##set_custom_filter

sets a method you define as a filter for tweets

abstract:
```python
collection.set_custom_filter(FUNCTION)
```

practical:
```python
def is_tweet_a_retweet(tweet):
	if 'retweeted' in tweet and tweet['retweeted']:
		return True
	else:
		return False
collection.set_custom_filter(is_tweet_a_retweet)
# or 
collection.set_custom_filter(is_tweet_a_retweet).top_entities({'hashtags':10})
```
*returns* a collection object that will only return tweets that match or pass the specified custom filter method.

##set_custom_filter_list

sets a list of methods you define as a set of filters for tweets

abstract:
```python
collection.set_custom_filter_list([FUNCTION_ONE, FUNCTION_TWO, ETC])
```

practical:
```python
def is_tweet_a_retweet(tweet):
	if 'retweeted' in tweet and tweet['retweeted']:
		return True
	else:
		return False
def screen_name_is_yvan(tweet):
	if screen_name in tweet and tweet['screen_name'] == 'yvan':
		return True
	return False
collection.set_custom_filter_list([is_tweet_a_retweet, screen_name_is_yvan])
# or 
collection.set_custom_filter_list([is_tweet_a_retweet, screen_name_is_yvan]).top_entities({'hashtags':10})
```

*returns* a collection object that will only return tweets that match or pass the specified custom filter methods.

note: passing an empty filter will return all tweets in a collection, empty filters `[]` are like no filter.

##dump_to_bson

dumps all tweets in a collection to bson.

abstract:
```python
collection.dump_to_bson('/PATH/TO/OUTPUT/FILE.bson')
```

pratical:
```python
collection.dump_to_bson('~/smappstuff/file.bson')
# or 
collection.limit(5).dump_to_bson('/Users/kevin/work/smappwork/file.bson')
```

*returns* a bson file that dumps to disk.

##dump_to_json

dumps all tweets in a collection to json formatted bson (a json object on each line of the file).

abstract:
```python
collection.dump_to_json('/PATH/TO/OUTPUT/FILE.json')
```

pratical:
```python
collection.dump_to_json('~/smappstuff/file.json')
# or 
collection.limit(5).dump_to_json('/Users/kevin/work/smappwork/file.json')
```

*returns* a json file that dumps to disk.

##dump_to_csv

dumps all tweets in a collection to csv.

abstract:
```python
collection.dump_to_csv('/PATH/TO/OUTPUT/FILE.csv', ['FIELD1', 'FIELD2', 'FIELD3.SUBFIELD', ETC])
```

pratical:
```python
collection.dump_to_csv('~/smappstuff/file.csv', ['id_str', 'entities.hashtags.0', 'entities.hashtags.1'])
# or 
collection.set_limit(5).dump_to_csv('/Users/kevin/work/smappwork/file.csv', ['id_str', 'entities.hashtags.0', 'entities.hashtags.1'])
```

*returns* a csv file that dumps to disk.

note: media and lists of objects are converted to a unicode string and put as one field in the csv.

note: this will dump in the order in which fields appear in a tweet and not the order in which you list them in your flist of fields.

note: empty lists `[]` will return nothing. you must specifyfields.

##tools

these are tools that our collection classes use ut that can also be used on their own if you have some kind of custom tweet input data source

##tweet_parser

a parser for tweets that can perform all sorts of tsansformations on tweets or extrct data from them easily.

abstract / practical:
```python
from smappdragon import TweetParser
tweet_parser = TweetParser()
```

*returns* an instance of the TweetParser class that can textract data from tweets or entities

test: `python -m unittest tests.test_tweet_parser`

##contains_entity

tells you wether or not a tweet object has a certain [twitter entity](https://dev.twitter.com/overview/api/entities-in-twitter-objects#symbols)

abstract:
```python
tweet_parser.contains_entity(ENTITY_TYPE, TWEET_OBJ)
```

practical:
```python
tweet_parser.contains_entity('media', { ... tweet object here ... })
#or
tweet_parser.contains_entity('user_mentions', { ... tweet object here ... })
#etc
```

*returns* true or false depending on whether a tweet contains the given entity

note: `entity_type` must be `'urls'` `'hashtags'` `'user_mentions'` `'media'` or `'symbols'`

##get_entity

gets a particular list of [twitter entities](https://dev.twitter.com/overview/api/entities-in-twitter-objects#symbols) for you

abstract:
```python
tweet_parser.get_entity(ENTITY_TYPE, TWEET_OBJ)
```

practical:
```python
print tweet_parser.get_entity('urls', { ... tweet object here ... })
```

output:
```python
[
	{
			"url": "https:\/\/t.co\/XdXRudPXH5",
			"expanded_url": "https:\/\/blog.twitter.com\/2013\/rich-photo-experience-now-in-embedded-tweets-3",
			"display_url": "blog.twitter.com\/2013\/rich-phot\u2026",
			"indices": [80, 103]
		},
	{
			"url": "https:\/\/t.co\/XdXRudPXH4",
			"expanded_url": "https:\/\/blog.twitter.com\/2013\/rich-photo-experience-now-in-embedded-tweets-3",
			"display_url": "blog.twitter.com\/2013\/rich-deio\u2026",
			"indices": [80, 103]
		},
]
```

*returns* a list of entity objects stored inside the tweet object's entity field.

note: `entity_type` must be `'urls'` `'hashtags'` `'user_mentions'` `'media'` or `'symbols'`

##get_entity_field

gets the field of a particular [twitter entity](https://dev.twitter.com/overview/api/entities-in-twitter-objects#symbols) object for you

abstract:
```python
tweet_parser.get_entity_field(FIELD, ENTITY)
```

practical:
```python
for entity in tweet_parser.get_entity('user_mentions', tweet):
	entity_value = tweet_parser.get_entity_field('id_str', entity)
# or
print tweet_parser.get_entity_field('url', {
			"url": "https:\/\/t.co\/XdXRudPXH5", \
			"expanded_url": "https:\/\/blog.twitter.com\/2013\/rich-photo-experience-now-in-embedded-tweets-3", \
			"display_url": "blog.twitter.com\/2013\/rich-phot\u2026", \
			"indices": [80, 103] \
	})
```

output:
```python
# the second would output
'https://t.co/XdXRudPXH5'
```

*returns* the value stored in this entity object in the field you specified

note: those urls look weird, they are just escaped, it's where you put a `\` in front of every `/`

##tweet_passes_filter

checks to see if a tweet passes a filter

abstract:
```python
tweet_parser.tweet_passes_filter(FILTER_OBJECT, TWEET_OBJECT)
```

practical:
```python
tweet_parser.tweet_passes_filter({'a':'b'}, {'a':'b', 'c':'d'})
```

output:
```python
True
```

*return* true if a tweet passes a filter or false if a tweet fails to pass a filter.

##flatten_dict

flattens a tweet into a list of key paths and values. this is a one dimensional structure. you can flatten two objects and then compare them more easily.

abstract:
```python
tweet_parser.flatten_dict(TWEET_OBJ)
```

practical:
```python
tweet_parser.flatten_dict({'key':{'key2':{'key3':'blah blah'}}, 'cat':'tab'})
```

output:
```python
[
(['key1', 'key2', 'key3'], 'blah blah'),
(['cat'], 'tab')
]
```

*returns* a list of tuples wherer each tuple contains the a list of keys to get to a value ant the value located at those nested keys.

see: http://stackoverflow.com/questions/11929904/traverse-a-nested-dictionary-and-get-the-path-in-python
see: the tweet_passes_filter method in tweet_parser.py for an example of how to use it to comapare two objects.

##tweet_passes_custom_filter

tells you wether or not a tweet passes a certain custom filter method that you define

abstract:
```python
tweet_parser.tweet_passes_custom_filter(FILTER_FUNCTION, TWEET)
```

practical:
```python
def is_tweet_a_retweet(tweet):
	if 'retweeted' in tweet and tweet['retweeted']:
		return True
	else:
		return False
tweet_parser.tweet_passes_custom_filter(is_tweet_retweet, {text: 'blah blah', retweeted: True})
```

*returns* true or false depending on whether or not a tweet passes through the filter

##tweet_passes_custom_filter_list

tells you wether or not a tweet passes a list of certain custom filter method that you define

abstract:
```python
tweet_parser.tweet_passes_custom_filter_list([FILTER_FUNCTION, ANOTHER_FILTER_FUNCTION], TWEET)
```

practical:
```python
def is_tweet_a_retweet(tweet):
	if 'retweeted' in tweet and tweet['retweeted']:
		return True
	else:
		return False
def screen_name_is_yvan(tweet):
	if screen_name in tweet and tweet['screen_name'] == 'yvan':
		return True
	return False
tweet_parser.tweet_passes_custom_filter_list([screen_name_is_yvan, is_tweet_a_retweet], {text: 'blah blah', retweeted: True})
```

*returns* true or false depending on whether or not a tweet passes through the list of filters

##transform_tweet

*not ready* - could use mongo operator support

transforms a tweet, either adding fields or removing fields

*returns*

##mongo_query

*not ready*

allows you to perform mongo queries on tweet objects (python dicts more generally)

##contributing

install the developer environment: `conda env create -f environment.yml`

run `pylint smappdragon` and fix style issues

submit your pull request on a feature branch `feature/added-language-support` to be merged with the `dev` branch

resources:

[best tutorial on python encoding/decoding](http://pythoncentral.io/encoding-and-decoding-strings-in-python-3-x/)
[csv encoding explanation](http://stackoverflow.com/questions/15420467/the-python-csv-writer-is-adding-letters-to-the-beginning-of-each-element-and-iss)

bad style:

do not write excessively long 'one-liners' these ar difficult to understand and wlll be rejected. break them up into multiple lines. posterity will thank you.

use as few dependencies as possible. if you have a choice between using a little bit of extra code or importing a dependency and using a little less code. do not import the dependecy. write the extra code.

only create an extra file with methods if those methods could be used on their own. in other words do not make pure helper classes for the sake of abstracting code. it just makes the project more confusing. if there's code that's repeated more than 3-4x make a helper method in the place where it's used not a separate file.

an example of good helper code is the [tweet_parser](https://github.com/SMAPPNYU/smappdragon/blob/master/smappdragon/tools/tweet_parser.py) in `smappdragon/tools`.

[good guide to distributing to pypi](https://packaging.python.org/en/latest/distributing/)

`python setup.py sdist upload`

##author

[yvan](https://github.com/yvan)