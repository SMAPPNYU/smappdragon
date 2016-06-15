config = { \
	'mongo':{ \
		'host': 'localhost', \
		'port': 49999,\
		'user': 'smapp_readOnly_Db', \
		'password': 'winter!is*coming^ppams', \
		'database': 'JadeHelm', \
		'collection': 'tweets_1' \
	}, \
	'bson':{ \
		'valid':'data/valid.bson', \
		'sketchy':'data/sketchy.bson' \
	}, \
	'json':{ \
		'valid': 'data/valid.bson.json', \
		'valid-single': 'data/valid-single.bson.json' \
	}, \
	'csv':{
		'valid': 'data/valid.csv'
	}
}
