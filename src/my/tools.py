#!/usr/bin/python3

'''
Created on May 19, 2024

@author: Tom Blackshaw
'''

import time


def timeit(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            from my.classes import logit
            logit('%r  %2.2f ms' %
                  (method.__name__, (te - ts) * 1000))
        return result

    return timed
