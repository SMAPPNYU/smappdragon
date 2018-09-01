import sys
from setuptools import setup

setup(name='smappdragon',
	packages=['smappdragon', 'smappdragon.collection', 'smappdragon.tools'],
	version='0.0.47',
	description='smappdragon is a set of tools for working with twitter data',
	author='yvan, leon yin',
	author_email='whereisleon@gmail.com',
	url='https://github.com/SMAPPNYU/smappdragon',
	keywords='twitter parse smappdragon',
	license='MIT',
	install_requires=[
		'pymongo>=3.2.1'
	]
)
