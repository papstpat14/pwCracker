DB Worker for MD5 Cracker
=========================
TOC
---
[TOC]

Summary
--------
This is an implementation of DB Workers providing functionality for the MD5 Cracker project in Distributed Computing.

- worker.py starts a DB worker with the config of config.json
Each DB worker has an exclusive control queue and all DB workers share one order queue
- init.py starts the initial filling of the DB

Pre-requisites
---------------
For worker.py and init.py following python packages are required (install via pip):
- pika==0.10.0
- pymongo==3.2.2 or redis==2.10.0

In addition redis (or mongo-db) and rabbitmq must be installed.

If you want to use the .bat files, the redis path and mongo/bin path has to be present in PATH.

Usage
------
Configure via config.json
Then start DB Worker via CMD or via bin/.bat Files

bin/.bat files
--------------

| file | action |
|--------|--------|
| flushall_mongo.bat | CAUTION! Flushes all DBs in mongo! |
| flushall_redis.bat | CAUTION! Flushes all DBs in redis! |
| start_dbworker.bat 12 0 | starts 12 dbworker with 0 sleep before getting the password (sleep for stopping test purposes only) |
| start_dbworker_5.bat | runs start_dbworker.bat 5 0 |
| start_dbworker_5_sleep5.bat | runs start_dbworker.bat 5 5 |
| start_default_mongo.bat | starts up mongo using mongod.conf and 5 dbworker |
| start_default_and_init_mongo.bat | starts up mongo using mongod.conf and 5 dbworker and runs init.py |
| start_mongo.bat | starts up mongo using mongod.conf |
| start_default_redis.bat | starts up redis and 5 dbworker |
| start_default_and_init_redis.bat | starts up redis and 5 dbworker and runs init.py |
| start_redis.bat | starts up redis |

Messageformats Used by Workers
------------------------------

##### Messageformat for the DB Worker to react on must be the following json
```
{
	'md5': 'hash',					//non-optional; the hash to get the password from or to write
	'action': 'put'|'get'|'stop',	//non-optional; 'put' or 'get'; get to query worker, put to let worker save, stop to signal to stop worker
	'pw': 'clear password'			//optional when action == get or action == stop, otherwise non-optional; the password corresponding to the hash under 'md5'
}
```


Returns a JSON-String as follows to the given reply_to queue
```
{
	'md5': 'hash',					//non-optional; the hash of the request
	'action': 'put'|'get'|'stop',	//non-optional; the original action that led to this response
	'success': true|false|null,		//non-optional; true if action successful, false if action not successful, None if action not complete
	'status': 100					//non-optional; status 0-100% of worker; if 100, then final answer
	'pw': 'clear password',			//non-optional; the clear text password to the md5 hash or null if not successful
	'err': []						//non-optional; array of errormessages; if no errors, empty array
}
```

Usage testserver
-----------------
- node server.js test get [100] --> Send get Requests [100 times]
- node server.js test put [100] --> send put Requests [100 times]
- node server.js test stop [100] --> send stop Requests [100 times]

Wordlists
---------
Wordlists for init.py from: [http://www.md5this.com/tools/wordlists.html](http://www.md5this.com/tools/wordlists.html)

Authors
-------
- Patrick Kager ([patrickaugustjosef.kager@edu.fh-joanneum.at](mailto:patrickaugustjosef.kager@edu.fh-joanneum.at))
- Alb Pellumbi ([alb.pellumbi@edu.fh-joanneum.at](mailto:alb.pellumbi@edu.fh-joanneum.at))