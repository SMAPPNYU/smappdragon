'''
see mongo operator here:
https://docs.mongodb.org/manual/reference/operator/query/
'''

MONGO_OPERATORS = [
    '$eq',
    '$gt',
    '$gte',
    '$lt',
    '$lte',
    '$ne',
    '$in',
    '$nin',
    '$or',
    '$and',
    '$not',
    '$nor',
    '$exists',
    '$type',
    '$mod',
    '$regex',
    '$text',
    '$where',
    '$all',
    '$elemMatch',
    '$size'
]

class MongoQuery(object):
    def __init__(self):
        pass

    def process_operators(self, filter_object):
        pass


