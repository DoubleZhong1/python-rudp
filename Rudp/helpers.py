__author__ = 'brianhoffman'

import threading
import math

def splitArrayLike(data, length):
    length = length or 1
    retval = []

    blocks = int(math.ceil(len(data) / length))
    blocks += 1

    for i in range(0, blocks):
        retval.append(data[i:i + length])

    return retval

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t
