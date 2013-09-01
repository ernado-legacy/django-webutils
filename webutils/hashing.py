import hashlib

from django.utils.encoding import smart_str


def hexHash(s):
    encoded_str = smart_str(s)
    return hashlib.md5(encoded_str).hexdigest()