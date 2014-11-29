__author__ = 'brianhoffman'

import threading


def splitArrayLike(data, length):
    length = length or 1
    retval = []

    data = bytearray(data)
    print 'arr', type(data)

    for i in range(0, len(data)):
        retval.append(data[i:i + length])

    return retval

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t
