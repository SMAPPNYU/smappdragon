import os
import json
import pymongo
import unittest

from test.config import config
from smappdragon import JsonCollection
from smappdragon.tools.tweet_cleaner import clean_tweets

class TestTweetCleaner(unittest.TestCase):

    def setUp(self):
        if os.path.exists(os.path.dirname(os.path.abspath(__file__))+'/../test/output.json'):
            os.remove(os.path.dirname(os.path.abspath(__file__))+'/../test/output.json')

        if os.path.exists(os.path.dirname(os.path.abspath(__file__))+'/../test/output_err.json'):
            os.remove(os.path.dirname(os.path.abspath(__file__))+'/../test/output_err.json')
            
    def tearDown(self):
        if os.path.exists(os.path.dirname(os.path.abspath(__file__))+'/../test/output.json'):
            os.remove(os.path.dirname(os.path.abspath(__file__))+'/../test/output.json')

        if os.path.exists(os.path.dirname(os.path.abspath(__file__))+'/../test/output_err.json'):
            os.remove(os.path.dirname(os.path.abspath(__file__))+'/../test/output_err.json')

    def test_clean_tweets_on_dirty_data(self):
        self.setUp()
        clean_tweets('json', 
        os.path.dirname(os.path.realpath(__file__)) +'/'+ config['json']['dirty'], 
        os.path.dirname(os.path.abspath(__file__))+'/../test/output.json', 
        os.path.dirname(os.path.abspath(__file__))+'/../test/output_err.json')

        col = JsonCollection(os.path.dirname(os.path.abspath(__file__))+'/../test/output.json')

        with open(os.path.dirname(os.path.abspath(__file__))+'/../test/output.json', 'r') as f:
            for line in f:
                try:
                    json.loads(line)
                except:
                    self.assertTrue(False)

        excepted = False
        with open(os.path.dirname(os.path.abspath(__file__))+'/../test/output_err.json', 'r') as f:
            for line in f:
                try:
                    json.loads(line)
                except:
                    excepted = True
        self.assertTrue(excepted)
        self.tearDown()

    def test_clean_tweets_on_clean_data(self):
        self.setUp()
        clean_tweets('json', 
        os.path.dirname(os.path.realpath(__file__)) +'/'+ config['json']['valid'], 
        os.path.dirname(os.path.abspath(__file__))+'/../test/output.json', 
        os.path.dirname(os.path.abspath(__file__))+'/../test/output_err.json')

        col = JsonCollection(os.path.dirname(os.path.abspath(__file__))+'/../test/output.json')

        with open(os.path.dirname(os.path.abspath(__file__))+'/../test/output.json', 'r') as f:
            for line in f:
                try:
                    json.loads(line)
                except:
                    self.assertTrue(False)

        excepted = False
        with open(os.path.dirname(os.path.abspath(__file__))+'/../test/output_err.json', 'r') as f:
            for line in f:
                try:
                    json.loads(line)
                except:
                    print('blah')
                    excepted = True
        self.assertFalse(excepted)
        self.tearDown()
            

if __name__ == '__main__':
    unittest.main()

'''
author @yvan
'''