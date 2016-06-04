#!/usr/bin/env python

class PasswordHandler:
    def __init__(self, ph):
        self.ph = ph

    def putPassword(self, hashvalue, password):
        updateresult = self.ph.putPassword(hashvalue, password)

        result = {'success': None, 'err': []}

        if (updateresult):
            result['success'] = True
        else:
            result['success'] = False
            result['err'].extend(["Hash " + hashvalue + " could not be saved to DB"])

        return result

    def getPassword(self, hashvalue):
        result = {'success': None, 'pw': None, 'err': []}

        pw = self.ph.getPassword(hashvalue)

        if pw is not None:
            result['success'] = True
            result['pw'] = pw
        else:
            result['success'] = False
            result['err'].extend(["Hash " + hashvalue + " not found in DB"])

        return result
