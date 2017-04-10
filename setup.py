import sys
from setuptools import setup

setup(name='smappdragon',
	packages=['smappdragon', 'smappdragon.collection', 'smappdragon.tools'],
	version='0.0.44',
	description='smappdragon is a set of tools for working with twitter data',
	author='yvan',
	author_email='yns207@nyu.edu',
	url='https://github.com/SMAPPNYU/smappdragon',
	keywords='twitter parse smappdragon',
	license='MIT',
	install_requires=[
	  'pymongo>=3.2.1'
	]
)