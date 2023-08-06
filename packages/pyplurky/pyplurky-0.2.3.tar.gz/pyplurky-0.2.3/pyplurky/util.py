# coding=utf-8
################################################
# Nazomi Plurk bot Project
# Produced by Dephilia
################################################
from datetime import datetime, timezone
from random import randrange

def randList(list):
    return list[randrange(len(list))]

def wrapExample(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        """Function here"""
        return func(*args, **kwargs)
    return wrapped

def dt2pt(time):
    """Transform datetime to plurk time"""
    return time.astimezone(tz=timezone.utc).strftime("20%y-%m-%dT%H:%M:%S")

def timestamp2datetime(stamp):
    return datetime.fromtimestamp(stamp)

def opt_para(obj,obj_name,opt_pool):
    """
    obj<string>
    opt_pool<dict>
    """
    if obj:opt_pool[obj_name]=obj


# base36 decode
alphabet = '0123456789abcdefghijklmnopqrstuvwxyz'
def encode36(number):
    if not isinstance(number, int):
        raise TypeError('Number must be an integer.')

    if number < 0:
        return '-' + encode36(-number)

    value = ''

    while number != 0:
        number, index = divmod(number, 36)
        value = alphabet[index] + value

    return value or '0'


def decode36(value):
    return int(value, 36)
