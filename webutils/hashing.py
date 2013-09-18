import hashlib

from django.utils.encoding import smart_str
from encode import baseEncode


def hexHash(s):
    encoded_str = smart_str(s)
    int_hash = int(hashlib.md5(encoded_str).hexdigest(), 16)
    return baseEncode(int_hash)
