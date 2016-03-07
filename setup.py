import sys
from setuptools import setup

# if python version is above 3 then throw a message and exit
if not sys.version_info.major < 3:
    print "Hello python pirate! smappdragon is only for python versions below version 3.0!"
    print "You appear to have python version:"
    print "{}".format(sys.version_info.major)
    sys.exit(1)

setup(name='smappdragon',
	packages=['smappdragon', 'smappdragon.collection', 'smappdragon.tools'],
	version='0.0.9',
	description='smappdragon is a set of tools for working with twitter data',
	author='yvan',
	author_email='yns207@nyu.edu',
	url='https://github.com/SMAPPNYU/smappdragon',
	keywords='twitter parse smappdragon',
	license='MIT',
	install_requires=[
	  'pymongo>=3.2.1',
      'unicodecsv>=0.14.1'
	]
)