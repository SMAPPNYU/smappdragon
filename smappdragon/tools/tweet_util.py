"""
Utility functions for tweets
"""

import random
from smappPy.date import mongodate_to_datetime

ID_FIELD = "id"
RANDOM_FIELD = "random_number"
TIMESTAMP_FIELD = "timestamp"

def add_random_to_tweet(tweet):
    """Takes a tweet dict, adds a random number field to it via python random module"""
    # If already defined, do nothing
    if RANDOM_FIELD in tweet and tweet[RANDOM_FIELD] != None:
        return
    tweet[RANDOM_FIELD] = random.random()

def add_timestamp_to_tweet(tweet):
    """Takes a tweet dict, adds a native datetime object corresponding to tweet's 'created_at' field"""
    # If already defined, do nothing
    if TIMESTAMP_FIELD in tweet and tweet[TIMESTAMP_FIELD] != None:
        return
    if 'created_at' not in tweet:
        raise Exception("Tweet (id_str: {0}) has no 'created_at' field".format(tweet['id_str']))
    tweet[TIMESTAMP_FIELD] = mongodate_to_datetime(tweet['created_at'])

def contains_place(tweet):
    """
    Returns True if tweet contains a populated 'place' field
    """
    if "place" in tweet and tweet["place"]:
        return True
    return False
