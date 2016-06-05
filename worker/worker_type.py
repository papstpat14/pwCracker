import json
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import hashlib
from reply import Reply


chars = range(32, 127)
max = 10


def force(width, pos, str, hash):
    found = ""
    for c in chars:
        if pos < width-1:
            found = force(width, pos + 1, str + "%c" % c, hash)
            if found != "":
                break;
        md5 = hashlib.md5()
        pw = str + "%c" % c
        md5.update(pw.encode("utf-8"))
        if hash == md5.hexdigest():
            found = pw
    return found;


def brute_force(body):
    md5 = json.loads(body)["md5"]
    i = 0
    found = False
    pw = ""
    while not found or i == max:
        pw = force(i, 0, "", md5)
        i += 1
        found = pw != ""
    return Reply(md5, pw, None)


def call_api(body):
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
    except HTTPError as e:
        err = e
    return Reply(md5, pw, err)
