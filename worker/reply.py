#Authors: Kainz Patrick and Schalk Markus
from urllib.error import HTTPError


class Reply:
    def __init__(self, md5, pw, workertype, err=None):
        self.success = err is None
        self.workertype = workertype
        self.md5 = md5
        self.pw = pw
        self.err = []
        if err is HTTPError:
            self.err.extend([err.reason])
        elif err != None:
            self.err.extend([err])