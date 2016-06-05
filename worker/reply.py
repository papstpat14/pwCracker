from urllib.error import HTTPError


class Reply:
    def __init__(self, md5, pw, err=None):
        self.success = err is None
        self.md5 = md5
        self.pw = pw
        if err is HTTPError:
            self.err = err.reason
        else:
            self.err = ""
