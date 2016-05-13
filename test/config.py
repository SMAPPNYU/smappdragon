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
        'valid': 'bson/valid.bson', \
        'invalid': 'bson/invalid.bson' \
    }, \
    'json':{ \
        'valid': 'bson/valid.bson.json', \
        'valid-single': 'bson/valid-single.bson.json' \
    }, \
    'csv':{ \
        'valid': 'bson/valid.csv', \
    } \
}
