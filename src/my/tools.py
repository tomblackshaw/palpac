#!/usr/bin/python3

'''
Created on May 19, 2024

@author: Tom Blackshaw
'''

import datetime
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
            logit('%r  %2.2f ms' %
                  (method.__name__, (te - ts) * 1000))
        return result

    return timed


def logit(s, logfile_fname='/tmp/null.txt'):
    datestr = "{:%B %d, %Y @ %H:%M:%S}".format(datetime.datetime.now())
    s = '%s  %s' % (datestr, s)
    try:
        with open(logfile_fname, 'a+') as f:
            f.write('%s\n' % s)
    except:
        pass
    print(s)
