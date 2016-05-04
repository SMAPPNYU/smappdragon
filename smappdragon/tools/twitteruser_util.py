"""
General utility functions for twitter user documents/objects

@auth dpb
@date 5/30/2014
"""

import random
from smappPy.date import mongodate_to_datetime

USER_ID = "id"
USER_RANDOM = "random_number"
ACCOUNT_CREATED_TIMESTAMP = "created_timestamp"

def add_random_to_user(user, field=USER_RANDOM):
    """Takes a user dict, adds a random number field to it via python random module"""
    # If already defined, do nothing
    if field in user and user[field] != None:
        return
    user[field] = random.random()

def add_created_timestamp(user, field=ACCOUNT_CREATED_TIMESTAMP):
    """
    Takes a user dict, adds a native datetime object corresponding to user's 'created_at' field
    (the time the user created the account)
    """
    # If already defined, do nothing
    if field in user and user[field] != None:
        return
    if 'created_at' not in user:
        raise Exception("User ({0}) has no 'created_at' field".format(user))
    user[field] = mongodate_to_datetime(user['created_at'])