#!/usr/bin/env python
import json
import sys

from includes.passwordhandler.passwordHandler import PasswordHandler
from includes.requesthandler.requestHandler import RequestHandler
from includes.channelthreads.channelThread import ChannelThread

with open('config.json') as conffile:
    confdata = json.load(conffile)

dph = None
if (confdata['storageengine'] == 'redis'):
    from includes.passwordhandler.redisPasswordHandler import RedisPasswordHandler
    dph = RedisPasswordHandler(confdata)
elif(confdata['storageengine'] == 'mongo'):
    from includes.passwordhandler.mongoPasswordHandler import MongoPasswordHandler
    dph = MongoPasswordHandler(confdata)
else:
    from includes.passwordhandler.redisPasswordHandler import RedisPasswordHandler
    from includes.passwordhandler.mongoPasswordHandler import MongoPasswordHandler
    from includes.passwordhandler.redisMongoPasswordHandler import RedisMongoPasswordHandler
    dph = RedisMongoPasswordHandler(RedisPasswordHandler(confdata), MongoPasswordHandler(confdata))

pwtimeout = 0
if(len(sys.argv) > 1):
    pwtimeout = int(sys.argv[1])

ph = PasswordHandler(dph)
reqHandler = RequestHandler(ph, confdata['rabbitmq']['replyqueuename'], pwtimeout)

orderThread = ChannelThread(confdata, reqHandler, 'orderqueuename', 'order', confdata['rabbitmq']['orderqueuedurable'], 1)
controlThread = ChannelThread(confdata, reqHandler, None, 'control', False, 5)

orderThread.start()
controlThread.start()

orderThread.join()
controlThread.join()
