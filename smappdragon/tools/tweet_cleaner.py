import os
import csv
import glob
import bson
import json

def clean_tweets(input_file_path, output_file_path, error_file_path):
    json_handle = open(input_file_path, 'r', encoding='utf-8')
    with open(output_file_path, 'w', encoding='utf-8') as fo:
        with open(error_file_path, 'w', encoding='utf-8') as f:
            for count, line in enumerate(json_handle):
                try:
                    tweet = json.loads(line)
                    fo.write(json.dumps(tweet))
                    fo.write('\n')
                except:
                    f.write(line)
    json_handle.close()

def clean_tweets_multiple(input_file_pattern, output_file_path, error_file_path):
    for path in glob.glob(os.path.expanduser(input_file_pattern)):
        json_handle = open(path, 'r', encoding='utf-8')
        with open(output_file_path, 'a', encoding='utf-8') as fo:
            with open(error_file_path, 'a', encoding='utf-8') as f:
                for count, line in enumerate(json_handle):
                    try:
                        tweet = json.loads(line)
                        fo.write(json.dumps(tweet))
                        fo.write('\n')
                    except:
                        f.write(line)
        json_handle.close()

class SmappError(Exception):
    pass


'''
@yvan
can be used to clean tweets in a general catch all sense
kept separate from the data sources bson_collection, etc
to keep datasource implementation simple, its also not
a core function, its really more of an extra, how you clean
your data is up to you, we jsut offer this way. 
methods can get big and out of hand very quickly for cleaning
data. so im putting this here in an attempt to keep other parts
of the code from getting too crazy and unmaintainable.
'''