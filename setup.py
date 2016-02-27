import sys
from setuptools import setup

# if python version is above 3 then throw a message and exit
if not sys.version_info.major < 3:
    print "Hello python pirate! smappdragon is only for python versions below version 3.0!"
    print "You appear to have python version:"
    print "{}".format(sys.version_info.major)
    sys.exit(1)

setup(name='smappdragon',
	version='0.0.1',
	description='smappdragon is a set of tools for working with twitter data',
	author='yvan',
	license='MIT',
	author_email='yns207@nyu.edu',
	url='https://github.com/SMAPPNYU/smappdragon',
	packages=['smappdragon'],
	install_requires=[
	  'pymongo>=3.2.1'
	]
)