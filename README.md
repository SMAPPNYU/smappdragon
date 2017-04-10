```
                                     _                             
 ___ _ __ ___   __ _ _ __  _ __   __| |_ __ __ _  __ _  ___  _ __  
/ __| '_ ` _ \ / _` | '_ \| '_ \ / _` | '__/ _` |/ _` |/ _ \| '_ \ 
\__ \ | | | | | (_| | |_) | |_) | (_| | | | (_| | (_| | (_) | | | |
|___/_| |_| |_|\__,_| .__/| .__/ \__,_|_|  \__,_|\__, |\___/|_| |_|
                    |_|   |_|                    |___/             
```

[![PyPI](https://img.shields.io/pypi/v/smappdragon.svg)](https://pypi.python.org/pypi/smappdragon) [![PyPI](https://img.shields.io/pypi/l/smappdragon.svg)](https://github.com/SMAPPNYU/smappdragon/blob/master/LICENSE)

:dragon: smappdragon is a set of tools for working with twitter data. a more abstract / contextual wrapper for smappdragon can be found in [pysmap](https://github.com/SMAPPNYU/pysmap) (work in progress). the old smapp-toolkit can be found on our github repositories page.

- [collection](https://github.com/SMAPPNYU/smappdragon#collection)
	- [mongo_collection](https://github.com/SMAPPNYU/smappdragon#mongo_collection)
	- [bson_collection](https://github.com/SMAPPNYU/smappdragon#bson_collection)
	- [json_collection](https://github.com/SMAPPNYU/smappdragon#json_collection)
	- [csv_collection](https://github.com/SMAPPNYU/smappdragon#csv_collection)
	- [base_collection](https://github.com/SMAPPNYU/smappdragon#base_collection)
		- [get_iterator](https://github.com/SMAPPNYU/smappdragon#get_iterator)
		- [set_limit](https://github.com/SMAPPNYU/smappdragon#set_limit)
		- [strip_tweets](https://github.com/SMAPPNYU/smappdragon#strip_tweets)
		- [set_filter](https://github.com/SMAPPNYU/smappdragon#set_filter)
		- [set_custom_filter](https://github.com/SMAPPNYU/smappdragon#set_custom_filter)
		- [set_custom_filter_list](https://github.com/SMAPPNYU/smappdragon#set_custom_filter_list)
		- [dump_to_bson](https://github.com/SMAPPNYU/smappdragon#dump_to_bson)
		- [dump_to_json](https://github.com/SMAPPNYU/smappdragon#dump_to_json)
		- [dump_to_csv](https://github.com/SMAPPNYU/smappdragon#dump_to_csv)
        - [dump_to_sqlite_db](#dump_to_sqlite_db)
- [tools](https://github.com/SMAPPNYU/smappdragon#tools)
	- [tweet_parser](https://github.com/SMAPPNYU/smappdragon#tweet_parser)
		- [contains_entity](https://github.com/SMAPPNYU/smappdragon#contains_entity)
		- [get_entity](https://github.com/SMAPPNYU/smappdragon#get_entity)
		- [get_entity_field](https://github.com/SMAPPNYU/smappdragon#get_entity_field)
		- [tweet_passes_filter](https://github.com/SMAPPNYU/smappdragon#tweet_passes_filter)
		- [flatten_dict](https://github.com/SMAPPNYU/smappdragon#flatten_dict)
		- [tweet_passes_custom_filter](https://github.com/SMAPPNYU/smappdragon#tweet_passes_custom_filter)
		- [tweet_passes_custom_filter_list](https://github.com/SMAPPNYU/smappdragon#tweet_passes_custom_filter_list)
        - [parse_columns_from_tweet](#parse_columns_from_tweet)
		- [strip_tweet](#strip_tweet)
    - [tweet_cleaner](#tweet_cleaner)
        - [clean_tweets](#clean_tweets)
        - [clean_tweets_multiple](#clean_tweets_multiple)

## installation

`pip install smappdragon`

`pip install smappdragon --upgrade`

smappdragon runs in python 3. if you dont have this version of python, [install anaconda](https://www.continuum.io/downloads), [or miniconda](http://conda.pydata.org/miniconda.html), whatever you do we recommend at least python 3.0 .

(check python binary location with `which python`) 
should be `/usr/bin/python` (mac osx base install), `/usr/local/bin/python` (homebrew), `/Users/YOURNAME/miniconda3/bin/python` (miniconda), `/Users/YOURNAME/anaconda/bin/python` (anaconda)

(check with `python --version`)
if you are 2.X.X, you're out of date

## testing 

you absolutely need to write unit tests for any methods you add to smappdragon, this software needs to stay as stable as porssible as it will be the basis for other software.

this folder contains tests for smappdragon.

the `bson` folder contains two bson files on which to run tests. One if a valid.bson file with tweets that have properly formatted fields. Another is an sketchy.bson file that has tweets with strange fields, missing fields, etc.

our test covearge setup: https://github.com/coagulant/coveralls-python

## collection

classes for interfacing with a tweets from different data sources

## mongo_collection

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

#or with a passed in mongo connection
import pymongo
mongo_to_pass = pymongo.MongoClient('superhost.bio.nyu.edu', 27574)
collection = MongoCollection('smappReadWriteUserName', 'PASSWORD', 'GERMANY_ELECTION_2015_Nagler', 'tweet_collection_name', passed_mongo=mongo_to_pass)

```

*returns* a collection object that can have methods called on it

test: `python -m unittest test.test_mongo_collection`

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

## bson_collection

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

test: `python -m unittest test.test_bson_collection`

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

## json_collection

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

test: `python -m unittest test.test_json_collection`

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

## csv_collection

this allows you to use any csv file (with a csv header) as a data source for smappdragon. we recommend using native json and not using csv collection, it's know to have a few bugs.

abstract:
```python
from smappdragon import CsvCollection

collection = CsvCollection('/PATH/TO/CSV/FILE.csv')
```

practical:
```python
from smappdragon import CsvCollection

collection = CsvCollection('~/Documents/file.csv')
```

*returns* a collection object that can have methods called on it

test: `python -m unittest test.test_csv_collection`

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

## base_collection

this is the base class for all collection objects. methods that all collection objects use are found here. this is actually the most important class.

test: `python -m unittest test.test_base_collection`

## get_iterator

makes an iterator that can iterate through all tweets in a particular collection

abstract:
```python
collection.get_iterator()
```

practical:
```python
for tweet in collection.get_iterator():
	print(tweet)
```

*returns* an iterable object that will yield all the tweets in a particular collection

## set_limit

sets a limit on the number of documents a collection can return 

abstract:
```python
collection.set_limit(TWEET_LIMIT_NUMBER)
```

practical:
```python
collection.set_limit(10)
# or 
collection.set_limit(10)
```

*returns* a collection object limited to querying / filtering only as many tweets as the limit number allows. a limit of 10 will only allow 10 tweets to be processed.

## strip_tweets

abstract:
```python
collection.strip_tweets(FIELDS_TO_KEEP)
```

practical:
```python
collection.strip_tweets(['id', 'user.id', 'entities.user_mentions'])
```

*returns* a collection object that will return reduced tweet objects where all the fields but the specified ones are filtered away.

*note* you cannot use strip_tweets with [csv_collection](#csv_collection)

## set_filter

sets a filter to apply toa all tweets, the filter is a mongo style query dictionary

abstract:
```python
collection.set_filter(TWEET_FILTER)
```

practical:
```python
collection.set_filter({'id_str':'4576334'})
# or 
collection.set_filter({'id_str':'4576334', 'user':{'screen_name':'yvanscher'}})
```

*returns* a collection object that will only return tweets that match the specified filter. so if you ask for {`id_str`:`4576334`} you will only get tweets where the `id_str` field is `4576334`.

note: passing an empty filter will return all tweets in a collection, empty filters `{}` are like no filter.

note: to make sure you are querying what you really want you should examine the twitter docs on [tweet](https://dev.twitter.com/overview/api/tweets) and [user](https://dev.twitter.com/overview/api/users) objects. some field names are shared between objects (example `id_str` is part of both user and tweet objects, even when a user object is nested inside a tweet object)

## set_custom_filter

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
collection.set_custom_filter(is_tweet_a_retweet)
```
*returns* a collection object that will only return tweets that match or pass the specified custom filter method.

## set_custom_filter_list

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
	if 'screen_name' in tweet['user'] and tweet['user']['screen_name'] == 'yvan':
		return True
	return False
collection.set_custom_filter_list([is_tweet_a_retweet, screen_name_is_yvan])
# or 
collection.set_custom_filter_list([is_tweet_a_retweet, screen_name_is_yvan])
```

*returns* a collection object that will only return tweets that match or pass the specified custom filter methods.

note: passing an empty filter will return all tweets in a collection, empty filters `[]` are like no filter.

## dump_to_bson

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

## dump_to_json

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

## dump_to_csv

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
# or if you want to omit the header
collection.dump_to_csv('out_file.csv', ['id_str'], write_header=False)
```

input:
```
[
    'id_str',
    'coordinates.coordinates.0',
    'coordinates.coordinates.1',
    'user.id_str',
    'user.lang',
    'lang',
    'text',
    'user.screen_name',
    'user.location',
    'user.description',
    'created_at',
    'user.friends_count',
    'user.followers_count',
    'retweet_count',
    'entities.urls.0.expanded_url',
    'entities.urls.1.expanded_url',
    'entities.urls.2.expanded_url',
    'entities.urls.3.expanded_url',
    'entities.urls.4.expanded_url'
]
```

output:
```csv
id_str,coordinates.coordinates.0,coordinates.coordinates.1,user.id_str,user.lang,lang,text,user.screen_name,user.location,user.description,created_at,user.friends_count,user.followers_count,retweet_count,entities.urls.0.expanded_url,entities.urls.1.expanded_url,entities.urls.2.expanded_url,entities.urls.3.expanded_url,entities.urls.4.expanded_url

788556059375874048,50,50,2240756971,en,en,RT @dailypenn: The DP and @WellesleyNews are jointly endorsing Wellesley alum @HillaryClinton over Wharton ’68 @realDonaldTrump.… ,CorrectRecord,,Correct The Record is a strategic research and rapid response team designed to defend Hillary Clinton from baseless attacks.,Wed Oct 19 01:43:09 +0000 2016,224,23080,0,http://www.metrodakar.net/barack-obama-conseille-a-donald-trump-darreter-de-pleurnicher/,http://www.metrodakar.net/barack-obama-conseille-a-donald-trump-darreter-de-pleurnicher/,http://www.metrodakar.net/barack-obama-conseille-a-donald-trump-darreter-de-pleurnicher/,http://www.metrodakar.net/barack-obama-conseille-a-donald-trump-darreter-de-pleurnicher/,http://www.metrodakar.net/barack-obama-conseille-a-donald-trump-darreter-de-pleurnicher/

788556059317186560,,,4655522325,fr,fr,Barack Obama conseille à Donald Trump « d’arrêter de pleurnicher » -  https://t.co/eEl1mOnIwp https://t.co/8EeOGya28r,metrodakar_net,Senegal,,Wed Oct 19 01:43:09 +0000 2016,110,657,0,http://www.metrodakar.net/barack-obama-conseille-a-donald-trump-darreter-de-pleurnicher/,,,,
```

*returns* a csv file that dumps to disk.

`write_header` - the 'write_header' optional variable tellls the csv dump to write or not write its header, the use purpose is to give the user this option, the technical purposes it to make it easier to
not dump the header more than 1 time in the middle of a file when dumping a pysmap dataset to csv.

`top_level` - tells this dump method to split input columns based on dots or not, this is complicated and has to do with the way we automatically assume a '.' character in a input_field indicates a nested field. `top_level` tells the method to treat dots as normal cahracters and will not try to look for nested values. it  will just grab the top level values from each tweet dict in the method. if your input is a csv collection or tabular format you should always set this to `False` as you will only ever need to get things the top level (as tabular data cannot be nested). if you do not set it to true and your column names have '.' in them the dump will fail as it will try to look for nested data. for examplenormally `extended_entites.media` would look for `{... 'extended_entites':{'media':'some_url'} ...}` if you set `top_level = True` then input field `extended_entites.media` looks for `{... 'extended_entites.media':'some_other_thing' ...}`

note: to get things inside a list you need to refer to their list index. its better to overshoot (so if you want to get 5 entites urls where there are 5) you would use `['entities.urls.0.expanded_url','entities.urls.1.expanded_url','entities.urls.2.expanded_url','entities.urls.3.expanded_url','entities.urls.4.expanded_url']`, for tweet objects with less than 5 `urls` entities this will fill out urls up to 5 urls, if there are less than 5 the extra ones will be empty `,,` fields

note: empty lists `[]` will return nothing. you must specify fields.

note: fields that have no value will appear empty `,,`

dev note: you will note that if called on a csv collection we do not use the parse_columns_from_tweet method as it splits the '.' character and treats it as a nesting operator which applies to non tabular bson, json, or mongo but not to csv data sources which might have '.' in column names and still need to dump back to csv or sqlite. you will see in dump_to_csv or dump_to_sqlite_db that in case the input datasource is a columnar/tabular format we just take the twet dict values (as this dict is guaruanteed to be a flat dict in cases of csv input)

## dump_to_sqlite_db

dumps all tweets (only the fields you specify) to an sqlite database file

abstract:
```python
collection.dump_to_sqlite_db('/PATH/TO/OUTPUT/FILE.db', ['FIELD1', 'FIELD2', 'FIELD3.SUBFIELD', ETC])
```

pratical:
```python
collection.dump_to_sqlite_db('~/smappstuff/file.db', ['id_str', 'entities.hashtags.0', 'entities.hashtags.1'])
# or 
collection.set_limit(5).dump_to_sqlite_db('/Users/kevin/work/smappwork/file.db', ['id_str', 'entities.hashtags.0', 'entities.hashtags.1'])
```

*input* a collection object and a list of fields/subfields
```
[
    'id_str',
    'coordinates.coordinates.0',
    'coordinates.coordinates.1',
    'user.id_str',
    'user.lang',
    'lang',
    'text',
    'user.screen_name',
    'user.location',
    'user.description',
    'created_at',
    'user.friends_count',
    'user.followers_count',
    'retweet_count',
    'entities.urls.0.expanded_url',
    'entities.urls.1.expanded_url',
    'entities.urls.2.expanded_url',
    'entities.urls.3.expanded_url',
    'entities.urls.4.expanded_url'
]
```

*output* an sqlite db that looks like so:
```
sqlite> .schema
CREATE TABLE data (id_str,user__id_str,text,entities__urls__0__expanded_url,entities__urls__1__expanded_url,entities__media__0__expanded_url,entities__media__1__expanded_url);
sqlite> .tables
data
sqlite> select * from data;
686799531875405824|491074580|@_tessr @ProductHunt No one has stolen me yet. Security through obscurity.|NULL|NULL|NULL|NULL
686661056115175425|491074580|Predictions of peach's demise already starting. Nice.|NULL|NULL|NULL|NULL
686956278099349506|491074580|When was the state of the union first started? Ok wow since the office has existed. https://t.co/Cqgjkhr3Aa|https://en.wikipedia.org/wiki/State_of_the_Union#History|NULL|NULL|NULL
687115788487122944|491074580|RT @lessig: Looks like the @citizenequality act got a supporter tonight. Thank you @POTUS|NULL|NULL|NULL|NULL
686661056115175425|491074580|Predictions of peach's demise already starting. Nice.|NULL|NULL|NULL|NULL
687008713039835136|491074580|#GOPDebate approaching. Can't wait to observer a trump in its natural habitat!|NULL|NULL|NULL|NULL
687208777561448448|18673945|@yvanscher hey! saw u upvoted Cubeit on ProductHunt. Any feedback on how we can make Cubeit better for you? :) Thanks!|NULL|NULL|NULL|NULL
686662539913084928|491074580|RT @PopSci: iOS 9.3 update will tint your screen at night, for your health https://t.co/zrDt4TsoXB https://t.co/yXCEGQPHWp|http://pops.ci/cJWqhM|NULL|http://twitter.com/PopSci/status/686661925267206144/photo/1|NULL
```

`top_level` - tells this dump method to split input columns based on dots or not, this is complicated and has to do with the way we automatically assume a '.' character in a input_field indicates a nested field. `top_level` tells the method to treat dots as normal cahracters and will not try to look for nested values. it  will just grab the top level values from each tweet dict in the method. if your input is a csv collection or tabular format you should always set this to `False` as you will only ever need to get things the top level (as tabular data cannot be nested). if you do not set it to true and your column names have '.' in them the dump will fail as it will try to look for nested data. for examplenormally `extended_entites.media` would look for `{... 'extended_entites':{'media':'some_url'} ...}` if you set `top_level = True` then input field `extended_entites.media` looks for `{... 'extended_entites.media':'some_other_thing' ...}`

dev note: you will note that if called on a csv collection we do not use the parse_columns_from_tweet method as it splits the '.' character and treats it as a nesting operator which applies to non tabular bson, json, or mongo but not to csv data sources which might have '.' in column names and still need to dump back to csv or sqlite. you will see in dump_to_csv or dump_to_sqlite_db that in case the input datasource is a columnar/tabular format we just take the twet dict values (as this dict is guaruanteed to be a flat dict in cases of csv input)

# tools

these are tools that our collection classes use ut that can also be used on their own if you have some kind of custom tweet input data source

## tweet_parser

a parser for tweets that can perform all sorts of tsansformations on tweets or extrct data from them easily.

abstract / practical:
```python
from smappdragon import TweetParser
tweet_parser = TweetParser()
```

*returns* an instance of the TweetParser class that can textract data from tweets or entities

test: `python -m unittest test.test_tweet_parser`

## contains_entity

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

## get_entity

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

## get_entity_field

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

## tweet_passes_filter

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

## flatten_dict

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

## tweet_passes_custom_filter

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

## tweet_passes_custom_filter_list

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

## parse_columns_from_tweet

takes a tweet and returns the values for the fields you give it

abstract:
```python
tweet_parser.parse_columns_from_tweet(TWEET, INPUT_FIELDS)
```

practical:
```python
for tweet in self.get_iterator():
    tweet_parser = TweetParser()
    ret = tweet_parser.parse_columns_from_tweet(tweet,input_fields)
    print(ret)
```

*input* a tweet and the fields you'd like to extract out of the tweet
```
#tweet
{"name":"sam", "age":25, "fav_count":36, siblings:[{"name":"bob"},{"name":"jo"},{"name":"yako"}]}
#fields to get
['name', 'age', 'siblings.0.name',siblings.2.name]
```

*output* a list of tuple pairs where each pair is `(INPUT_FIELD, VALUE)`
```
[
('name','sam'),
('age',25),
('siblings.0.name','bob'),
('siblings.2.name','yako')
]
```

## strip_tweet

strips a tweet of all its fields except the ones specified

abstract:
```python
tweet_parser.strip_tweet(KEEP_FIELDS, TWEET)
```

practical:
```python
tweet_parser.strip_tweet(['id', 'user.id', 'entities.user_mentions'], tweet)
```

*returns* a tweet stripped down to the fields you want, retaining only specified fields

# contributing

install the developer environment: `conda env create -f environment.yml`

run `pylint smappdragon` and fix style issues

submit your pull request on a feature branch `feature/added-language-support` to be merged with the `dev` branch

# tweet_cleaner

functions for cleaning tweets

## clean_tweets

a catch all tweet cleaner that excepts all errors and writes clean tweets to a file and unclean tweets to a 
separate file

abstract:
```python
clean_tweets(YOUR_DIRTY_INPUT_FILE, YOUR_CLEAN_OUTPUT_FILE, YOUR_DIRTY_OUTPUT_FILE)
```

practical:
```python
from smappdragon.tools.tweet_cleaner import clean_tweets

clean_tweets('~/smappwork/my_dirty_file.json', '~/smappwork/clean_tweets.json', '~/smappwork/dirty_tweets.json')
```

*input* a json file and the names of your dirty/clean output files.

*return* a file with clean tweets and a file with dirty tweets.

note: this assumes that the correct underlying format/encoding will be utf8 unicode. if you want your file to be something else you are on your own.

note: only does json cleaning for now.

## clean_tweets_multiple

a catch all tweet cleaner that excepts all errors and writes clean tweets to a file and unclean tweets to a separate file. same as (clean_tweets except it can clean multiple files).

abstract:
```python
clean_tweets_multiple(DIRTY_FILE_PATTERN, YOUR_CLEAN_OUTPUT_FILE, YOUR_DIRTY_OUTPUT_FILE)
```

practical:
```python
from smappdragon.tools.tweet_cleaner import clean_tweets_multiple

clean_tweets_multiple('~/smappwork/my_dirty_file_pattern_*.json', '~/smappwork/clean_tweets.json', '~/smappwork/dirty_tweets.json')
```

*input* a json file and the names of your dirty/clean output files.

*return* a file with clean tweets and a file with dirty tweets.

note: this assumes that the correct underlying format/encoding will be utf8 unicode. if you want your file to be something else you are on your own.

note: only does json cleaning for now.

# resources:

[best tutorial on python encoding/decoding](http://pythoncentral.io/encoding-and-decoding-strings-in-python-3-x/)
[csv encoding explanation](http://stackoverflow.com/questions/15420467/the-python-csv-writer-is-adding-letters-to-the-beginning-of-each-element-and-iss)

# bad style:

do not write excessively long 'one-liners' these ar difficult to understand and wlll be rejected. break them up into multiple lines. posterity will thank you.

use as few dependencies as possible. if you have a choice between using a little bit of extra code or importing a dependency and using a little less code. do not import the dependecy. write the extra code.

only create an extra file with methods if those methods could be used on their own. in other words do not make pure helper classes for the sake of abstracting code. it just makes the project more confusing. if there's code that's repeated more than 3-4x make a helper method in the place where it's used not a separate file.

an example of good helper code is the [tweet_parser](https://github.com/SMAPPNYU/smappdragon/blob/master/smappdragon/tools/tweet_parser.py) in `smappdragon/tools`.

[good guide to distributing to pypi](https://packaging.python.org/en/latest/distributing/)

`python setup.py sdist upload`

##author

[yvan](https://github.com/yvan)