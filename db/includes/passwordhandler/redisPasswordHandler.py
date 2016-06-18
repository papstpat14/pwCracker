#!/usr/bin/env python3

class RedisPasswordHandler:
    def __init__(self, confdata):
        self.confdata = confdata
        self.r = None

    def getRedisDbObj(self):
        if (self.r is not None):
            return self.r
        else:
            from redis import StrictRedis
            self.r = StrictRedis(host=self.confdata['redis']['host'], port=int(self.confdata['redis']['port']),
                                  db=int(self.confdata['redis']['db']), password=self.confdata['redis']['password'])
        return self.r

    def getPassword(self, hashvalue):
        db = self.getRedisDbObj()
        pw = db.get(hashvalue)
        if (pw is not None):
            pw = str(pw.decode('utf-8'))
        return pw

    def putPassword(self, hashvalue, password):
        db = self.getRedisDbObj()
        updateresult = db.set(hashvalue, password.encode('utf-8'))
        return updateresult
