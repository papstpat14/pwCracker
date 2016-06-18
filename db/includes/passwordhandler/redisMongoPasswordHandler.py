#!/usr/bin/env python3

class RedisMongoPasswordHandler:
    def __init__(self, redisPasswordHdl, mongoPasswordHdl):
        self.redisPasswordHdl = redisPasswordHdl
        self.mongoPasswordHdl = mongoPasswordHdl

    def getPassword(self, hashvalue):
        pw = self.redisPasswordHdl.getPassword(hashvalue)
        if (pw is not None):
            return pw
        pw = self.mongoPasswordHdl.getPassword(hashvalue)
        if (pw is not None):
            self.redisPasswordHdl.putPassword(hashvalue, pw)
            return pw

    def putPassword(self, hashvalue, password):
        updateresult1 = self.redisPasswordHdl.putPassword(hashvalue, password)
        updateresult2 = self.mongoPasswordHdl.putPassword(hashvalue, password)
        return (updateresult1 and updateresult2)
