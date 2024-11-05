# -*- coding: utf-8 -*-
"""my.tools

Created on May 19, 2024
Updated on Nov 05, 2024

@author: Tom Blackshaw

This module contains miscellaneous tools. For example:-
    timeit
    logit
    object_from_dictionary (turns a dictionary{'x':1, 'y':2', etc.} into an object(x=1,y=2,etc.)

.. _Style Guide:
   https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

"""

import datetime
import os
import time
from my.classes.exceptions import PyQtUICompilerError


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


def logit(s:str, logfile_fname:str='/tmp/null.txt'):
    """Log the supplied text to the specified logfile.

    Append the supplied text to the logfile whose pathname is supplied to this
    very function. Add the date to the front of the string first.

    Args:
        s (str): Text to be logged.
        logfile_fname (str): Logfile pathname.

    Returns:
        n/a

    """
    datestr = "{:%B %d, %Y @ %H:%M:%S}".format(datetime.datetime.now())
    s = '%s  %s' % (datestr, s)
    try:
        with open(logfile_fname, mode='a+', encoding="utf-8") as f:
            f.write('%s\n' % s)
    except Exception as e:  # pylint: disable=broad-exception-caught
        print("WARNING -- unable to log ===> {s} <=== {e}".format(s=s, e=str(e)))
    print(s)



def object_from_dictionary(dct:dict):
    '''Turn a dictionary into a simple object'''

    class MySimpleObject:
        pass

    o = MySimpleObject()
    for k in dct.keys():
        setattr(o, k, dct[k])
    return o


