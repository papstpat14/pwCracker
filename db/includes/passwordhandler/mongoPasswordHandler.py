#!/usr/bin/env python3

class MongoPasswordHandler:
    def __init__(self, confdata):
        self.confdata = confdata
        self.db = None

    def getMongoDbObj(self):
        if (self.db is not None):
            return self.db
        else:
            authstring = ''
            if (self.confdata['mongo']['username'] is not None) and (self.confdata['mongo']['password'] is not None):
                authstring = self.confdata['mongo']['username'] + ':' + self.confdata['mongo']['password'] + '@'

            from pymongo import MongoClient
            client = MongoClient(
                'mongodb://' + authstring + self.confdata['mongo']['host'] + ':' + self.confdata['mongo']['port'] + '/' + self.confdata['mongo']['db'])

            self.db = client.get_default_database()

        return self.db

    def getPassword(self, hashvalue):
        db = self.getMongoDbObj()
        pw = db[self.confdata['mongo']['table']].find_one({"_id": hashvalue})
        if (pw is not None):
            pw = pw['pw']
        return pw

    def putPassword(self, hashvalue, password):
        db = self.getMongoDbObj()
        hash = {"_id": hashvalue, "pw": password}
        updateresult = db[self.confdata['mongo']['table']].update_one({"_id": hashvalue}, {'$set': hash}, True)

        if (updateresult is not None) and ('ok' in updateresult.raw_result and updateresult.raw_result['ok'] == 1):
            return True

        return False
