config = \
{ \
    'mongo':{ \
            'host': 'localhost', \
            'port': 49999, \
            'user': 'smapp_readOnly_Db', \
            'password': 'winter!is*coming^ppams', \
            'database': 'JebCanFixIt', \
            'collection': 'tweets_1' \
    }, \
    'bson':{ \
        'valid': 'data/valid.bson', \
        'invalid': 'data/invalid.bson' \
    }, \
    'json':{ \
        'valid': 'data/valid.bson.json', \
        'valid-single': 'data/valid-single.bson.json' \
    }, \
    'csv':{ \
        'valid': 'data/valid.csv', \
    } \
}
