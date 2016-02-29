```
                                     _                             
 ___ _ __ ___   __ _ _ __  _ __   __| |_ __ __ _  __ _  ___  _ __  
/ __| '_ ` _ \ / _` | '_ \| '_ \ / _` | '__/ _` |/ _` |/ _ \| '_ \ 
\__ \ | | | | | (_| | |_) | |_) | (_| | | | (_| | (_| | (_) | | | |
|___/_| |_| |_|\__,_| .__/| .__/ \__,_|_|  \__,_|\__, |\___/|_| |_|
                    |_|   |_|                    |___/             
```

:dragon: smappdragon is a set of tools for working with twitter data. check us out on [pypi](https://pypi.python.org/pypi/smappdragon). a more abstract wrapper for smappdragon can be found in [smappboa](https://github.com/SMAPPNYU/smappboa) (work in progress).

- [collection](https://github.com/SMAPPNYU/smappdragon#collection)
	- [mongo_collection](https://github.com/SMAPPNYU/smappdragon#mongo_collection)
	- [base_collection](https://github.com/SMAPPNYU/smappdragon#base_collection)
		- [top_entities](https://github.com/SMAPPNYU/smappdragon#top_entities)
    - [set_limit]()
- [tools](https://github.com/SMAPPNYU/smappdragon#tools)
	- [tweet_parser](https://github.com/SMAPPNYU/smappdragon#tweet_parser)
		- [contains_entity](https://github.com/SMAPPNYU/smappdragon#contains_entity)
		- [get_entity](https://github.com/SMAPPNYU/smappdragon#get_entity)
		- [get_entity_field](https://github.com/SMAPPNYU/smappdragon#get_entity_field)

##contributing

TODO:

combining multiple collections.(give a list of the collections in a mongo database)

add bson collection.

process:

install pylint: `pip install pylint`

write your code

run `pylint smappdragon`

fix style issues

submit your pull request to the `dev` branch

some pointers:

do not write excessively long 'one-liners' these ar difficult to understand and wlll be rejected. break them up into multiple lines. posterity will thank you.

use as few dependencies as possible. if you have a choice between using a little bit of extra code or importing a dependency and using a little less code. do not import the dependecy. write the extra code.

only create an extra file with methods if those methods could be used on their own. in other words do not make pure helper classes for the sake of abstracting code. it just makes the project more confusing. if there's code that's repeated more than 3-4x make a helper method in the place where it's used not a separatae file.

an example of good helper code is the [tweet_parser](https://github.com/SMAPPNYU/smappdragon/blob/master/smappdragon/tools/tweet_parser.py) in `smappdragon/tools`.

be nice.

[good guide to distributing to pypi](https://packaging.python.org/en/latest/distributing/)    

##testing 

You absolutely need to write unit tests for any methods you add to smappdragon, this software needs to stay as stable as porssible as it will be the basis for other software.

This folder contains tests for smappdragon.

The `bson` folder contains two bson files on which to run tests. One if a valid.bson file with tweets that have properly formatted fields. Another is an sketchy.bson file that has tweets with strange fields, missing fields, etc.

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

##base_collection

this is the base class for all collection objects. methods that all collection objects use are found here. this is actually the most important class.

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

#set_limit

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
tweet_parser.contains_entity(entity_type, tweet)
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
tweet_parser.get_entity(entity_type, tweet)
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
tweet_parser.get_entity_field(field, entity)
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
# the second would output
'https://t.co/XdXRudPXH5'
```

*returns* the value stored in this entity object in the field you specified

note: those urls look weird, they are just escaped, it's where you put a `\` in front of every `/`
