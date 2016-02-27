```
                                     _                             
 ___ _ __ ___   __ _ _ __  _ __   __| |_ __ __ _  __ _  ___  _ __  
/ __| '_ ` _ \ / _` | '_ \| '_ \ / _` | '__/ _` |/ _` |/ _ \| '_ \ 
\__ \ | | | | | (_| | |_) | |_) | ( :dragon:_| | | | (_| | (_| | (_) | | | |
|___/_| |_| |_|\__,_| .__/| .__/ \__,_|_|  \__,_|\__, |\___/|_| |_|
                    |_|   |_|                    |___/             
```

smappdragon is a rebuild of the old [smapp-toolkit](https://github.com/SMAPPNYU/smapp-toolkit). It is a low level set of tools for programmers to use, it’s the low level part of the toolkit. There will be a separate piece of software called `smapptoolbox` that will import smapp dragon and buid the high level interface. Plotting figures, aggregating, and other non standard data operations will be in the new `smapptoolbox`.

##testing 

You absolutely need to write unit tests for any methods you add to smappdragon, this software needs to stay as stable as porssible as it will be the basis for other software.

This folder contains tests for smappdragon.

The `bson` folder contains two bson files on which to run tests. One if a valid.bson file with tweets that have properly formatted fields. Another is an sketchy.bson file that has tweets with strange fields, missing fields, etc.

##test_mongo_collection.py

Tests the MongoCollection class. Tests the count, containing, since, until, and a daterange query.

##collection

classes for interfacing with a mongodb database of tweets

##basecollection

this is the base class for all collection objects. methods taht all collection objects use are found here. this is actually the most important class.

##top_entities

returns the top twitter entites from a tweet object

##get_ngrams

##mongocollection

this allows you to plug into a running live mongodb database and run smappdragon methods on the resulting collection object. 

test:

you should create a `config.py` file in the `tests` directory structured like so:

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

only put a thing you want to test in there.





