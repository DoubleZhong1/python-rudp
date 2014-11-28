__author__ = 'brianhoffman'

import threading


def splitArrayLike(arr, length):
    length = length or 1
    retval = []

    for i in range(0, len(arr)):
        retval.append(arr[i:i + length])

    return retval

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t
