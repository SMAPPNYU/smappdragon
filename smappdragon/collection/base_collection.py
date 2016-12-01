import csv
import abc
import json
import sqlite3
import operator

from bson import BSON, json_util
from smappdragon.tools.tweet_parser import TweetParser

class BaseCollection(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self):
        self.limit = 0
        self.filter = {}
        self.keep_fields = []
        self.should_strip = False
        self.custom_filters = []

    '''
        returns an iterator that
        can iterate through the tweets
        in a collection
    '''
    @abc.abstractmethod
    def get_iterator(self):
        pass

    '''
        sets the fields to keep when
        the user calls strip tweets
    '''
    def strip_tweets(self, keep_fields):
        self.keep_fields = keep_fields
        self.should_strip = True
        return self

    '''
        returns the modified collection
        object with a limit on how many tweets
        it will ever output or query
    '''
    def set_limit(self, limit):
        self.limit = limit
        return self

    '''
        sets the filters you'd
        like to apply to the query
        follows mongdb query syntax
    '''
    def set_filter(self, query_filter):
        self.filter = query_filter
        return self

    '''
        takes a function as an input
        and appends it to the list of
        custom filters that need to be passed
    '''
    def set_custom_filter(self, func):
        self.custom_filters.append(func)
        return self

    '''
        takes a function as an input
        and appends it to the list of
        custom filters that need to be passed
    '''
    def set_custom_filter_list(self, functions_list):
        self.custom_filters.extend(functions_list)
        return self

    '''
        dumps the contents of a collection 
        to a bson file, this is a binary format
    '''
    def dump_to_bson(self, output_bson):
        filehandle = open(output_bson, 'ab+')

        for tweet in self.get_iterator():
            filehandle.write(BSON.encode(tweet))
        filehandle.close()

    '''
        dumps the contents of a collection
        to a json file, a json object on
        each line
    '''
    def dump_to_json(self, output_json):
        filehandle = open(output_json, 'a')

        for tweet in self.get_iterator():
            filehandle.write(json_util.dumps(tweet)+'\n')
        filehandle.close()

    '''
        dumps the contents of a collection 
        to csv format with columns specified
        by input_fields
    '''
    def dump_to_csv(self, output_csv, input_fields, write_header=True):
        filehandle = open(output_csv, 'a', encoding='utf-8')
        writer = csv.writer(filehandle)
        if write_header:
            writer.writerow(input_fields)
        tweet_parser = TweetParser()

        for tweet in self.get_iterator():
            ret = tweet_parser.parse_columns_from_tweet(tweet,input_fields)
            ret_values = [col_val[1] for col_val in ret]
            writer.writerow(ret_values)
        filehandle.close()

    '''
        dumps the contents of a collection 
        to an sqlite database with columns
        specified by input_fields
    '''
    def dump_to_sqlite_db(self, output_db, input_fields):
        def replace_none(s):
            if s is None:
                return 'NULL'
            return s

        tweet_parser = TweetParser()
        column_str = ','.join([column for column in input_fields]).replace('.','__')
        question_marks = ','.join(['?' for column in input_fields])

        con = sqlite3.connect(output_db)
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS data ({});".format(column_str))

        insert_list = []
        for count,tweet in enumerate(self.get_iterator()):
            ret = tweet_parser.parse_columns_from_tweet(tweet, input_fields)
            row = [replace_none(col_val[1]) for col_val in ret]
            insert_list.append(tuple(row))
            if (count % 10000) == 0:
                cur.executemany("INSERT INTO data ({}) VALUES ({});".format(column_str, question_marks), insert_list)
                con.commit()
                insert_list = []
        if count < 10000:
            cur.executemany("INSERT INTO data ({}) VALUES ({});".format(column_str, question_marks), insert_list)
            con.commit()
        con.close()
