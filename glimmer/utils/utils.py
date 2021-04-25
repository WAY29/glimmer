import errno
import hashlib
import os
import re
import sys
from base64 import b64decode, b64encode

ERROR_INVALID_NAME = 123
__version__ = "1.4.0"


def banner():
    msg = r"""
 _____ _ _
|  __ \ (_)
| |  \/ |_ _ __ ___  _ __ ___   ___ _ __
| | __| | | '_ ` _ \| '_ ` _ \ / _ \ '__|
| |_\ \ | | | | | | | | | | | |  __/ |
 \____/_|_|_| |_| |_|_| |_| |_|\___|_|
                                    v%s
""" % __version__
    print(msg)


def get_md5(value):
    if isinstance(value, str):
        value = value.encode(encoding='UTF-8')
    return hashlib.md5(value).hexdigest()


def base64_encode(s: str, encoding='utf-8') -> str:
    return b64encode(s.encode()).decode(encoding=encoding)


def base64_decode(s: str, encoding='utf-8') -> str:
    return b64decode(s.encode()).decode(encoding=encoding)


def get_full_exception_name(exc):
    name = ""
    exc_class = exc.__class__
    while exc_class != Exception:
        name = exc_class.__name__ + "." + name
        exc_class = exc_class.__base__
    name = name.rstrip(".")
    return name


def is_valid_pathname(pathname: str) -> bool:
    '''
    `True` if the passed pathname is a valid pathname for the current OS;
    `False` otherwise.

    Reference: https://stackoverflow.com/questions/9532499/check-whether-a-path-is-valid-in-python-without-creating-a-file-at-the-paths-ta
    '''
    try:
        if not isinstance(pathname, str) or not pathname:
            return False

        _, pathname = os.path.splitdrive(pathname)

        root_dirname = os.environ.get('HOMEDRIVE', 'C:') \
            if sys.platform == 'win32' else os.path.sep
        if not os.path.isdir(root_dirname):
            return False
        root_dirname = root_dirname.rstrip(os.path.sep) + os.path.sep
        for pathname_part in pathname.split(os.path.sep):
            try:
                os.lstat(root_dirname + pathname_part)
            except OSError as exc:
                if hasattr(exc, 'winerror'):
                    if exc.winerror == ERROR_INVALID_NAME:
                        return False
                elif exc.errno in {errno.ENAMETOOLONG, errno.ERANGE}:
                    return False
    except TypeError:
        return False
    else:
        return True


def is_valid_url(url):
    return re.match("(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]", url)
