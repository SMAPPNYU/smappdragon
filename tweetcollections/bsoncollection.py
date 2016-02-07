from bson import decode_file_iter
from basecollection import BaseCollection

'''
replacement for
https://github.com/SMAPPNYU/smapp-toolkit/blob/master/smapp_toolkit/twitter/bson_tweet_collection.py
'''
class BSONCollection(BaseCollection):

	'''
	method that tells us how to 
	create the BSONCollection object
	'''
	def __init__(self, filename):
		self.filename = filename
		if not os.path.isfile(filename):
			raise IOError('Your input BSON doesn\'t exist or your path is wrong. Fix it.')
		self.tweetlimit = None
		#don't grab one tweet to check for a timestamp
		#what we should do instead is on the 'since' and
		#'until' methods only count tweets that have it
		#and discard tweets with no timestamp if they
		#both appear in the same collection

	'''
	method that tells us that a BSONCollection
	should behave as an iterable object and
	describes its iterable behavior
	'''
	def __iter__(self):
		with open(self.filename, 'rb') as bson:
			for tweet in decode_file_iter(bson):
				yield tweet


	'''
	method that prints a representation of
	a BSONCollection object (kind of like toString())
	'''
	def __repr__(self):
