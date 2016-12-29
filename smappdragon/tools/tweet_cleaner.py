import os
import bson
import csv
import json

def clean_tweets(input_type, input_file_path, output_file_path, error_file_path):
    if input_type == 'bson':
        bson_handle = open(input_file_path, 'rb')
        for count, line in enumerate(bson.decode_file_iter(bson_handle)):
            try:
                pass
            except:
                pass
    elif input_type == 'json':
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
    elif input_type == 'csv':
        csv_handle = open(input_file_path, 'r', encoding='utf-8')
        for count, line in enumerate(csv.DictReader(csv_handle)):
            try:
                pass
            except:
                pass

class SmappError(Exception):
    pass


'''
@yvan
can be used to clean tweets in a general catch all sense
kept separate from the data sources bson_collection, etc
to keep datasource implementation simple, its also not
a core function, its really more of an extra, how you clean
your data is up to you, we jsut offer this way. because 
methods can get big and out of hand very quickly for cleaning
data. so im putting this here in an attempt to keep other parts
of the code from getting too crazy and unmaintainable.
'''