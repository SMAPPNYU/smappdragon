```
                                     _                             
 ___ _ __ ___   __ _ _ __  _ __   __| |_ __ __ _  __ _  ___  _ __  
/ __| '_ ` _ \ / _` | '_ \| '_ \ / _` | '__/ _` |/ _` |/ _ \| '_ \ 
\__ \ | | | | | (_| | |_) | |_) | (_| | | | (_| | (_| | (_) | | | |
|___/_| |_| |_|\__,_| .__/| .__/ \__,_|_|  \__,_|\__, |\___/|_| |_|
                    |_|   |_|                    |___/             
```

smappdragon is a rebuild of the old [smapp-toolkit](https://github.com/SMAPPNYU/smapp-toolkit). It is a low level set of tools for programmers to use, it’s the low level part of the toolkit. There will be a separate piece of software called `smapptoolkit` that will import smapp dragon and buid the high level interface.

##testing 

You absolutely need to write unit tests for any methods you add to smappdragon, this software needs to stay as stable as porssible as it will be the basis for other software.

This folder contains tests for smappdragon.

The `bson` folder contains two bson files on which to run tests. One if a valid.bson file with tweets that have properly formatted fields. Another is an sketchy.bson file that has tweets with strange fields, missing fields, etc.

##testbsoncollection.py

Tests the BSONCollection class. Tests the count, containing, since, until, and a daterange query.

##testmongocollection.py

Tests the MongoCollection class. Tests the count, containing, since, until, and a daterange query.


