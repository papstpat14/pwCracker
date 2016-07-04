import json
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import hashlib
from reply import Reply


chars = range(32, 127)
max = 100


def force(width, pos, str, hash,controlList):
    found = ""
    for c in chars:
        if pos < width-1:
            if(controlList[hash]==1):
                return found
            found = force(width, pos + 1, str + "%c" % c, hash,controlList)
            if found != "":
                break
        md5 = hashlib.md5()
        pw = str + "%c" % c
        md5.update(pw.encode("utf-8"))
        if hash == md5.hexdigest():
            found = pw
    return found


def brute_force(body,controlList):
    md5 = json.loads(body)["md5"]
    i = 0
    found = False
    pw = ""
    err = None
    while not found and i < max:
        if (controlList[md5] == 1):
            return Reply(md5, "", 'Bruteforce', "Worker aborted")
        pw = force(i, 0, "", md5, controlList)
        i += 1
        found = pw != ""
    if not found:
        err = "Hash not found by bruteforcing"
    return Reply(md5, pw, 'Bruteforce', err)


def call_api(body,controlList):
    url = "http://md5cracker.org/api/api.cracker.php?r=1140&database=md5cracker.org&hash="
    md5 = json.loads(body)["md5"]
    url += md5
    req = Request(url)
    pw = ""
    err = None
    try:
        res = urlopen(req)
        text = res.read().decode("utf-8")
        pw = json.loads(text)["result"]
        status = json.loads(text)["status"]
        if (status == False):
            err = json.loads(text)["message"]
    except HTTPError as e:
        err = e
    return Reply(md5, pw, 'Webservice', err)
