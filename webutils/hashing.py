import hashlib


def hexHash(s):
    if not isinstance(s, str):
        s = s.encode('utf8')
    return hashlib.md5(s).hexdigest()