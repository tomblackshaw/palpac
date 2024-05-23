# -*- coding: utf-8 -*-
"""my.tools

Created on May 19, 2024

@author: Tom Blackshaw

This module contains miscellaneous tools.

.. _Style Guide:
   https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

"""

import datetime
import os
import time

from my.exceptions import PyQtUICompilerError


def timeit(method):

    # TODO: Write me.
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


def compile_all_uic_files(a_path):
    """Compile the UIC files in the supplied path.

    Using the PyQt-supplied UIC file compiler, turn the path's every UIC file
    into a set of importable Python modules/wrappers.

    Args:
        a_path (str): Path to the directory.

    Returns:
        n/a

    """
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f for f in listdir(a_path) if isfile(join(a_path, f))]
    for f in onlyfiles:
        if f.endswith('.ui'):
            cmd = '''pyuic6 -o "{a_path}/{pyfile}" "{a_path}/{uifile}"'''.format(
                a_path=a_path,
                uifile=f,
                pyfile=f[:-2] + 'py')
            if 0 != os.system(cmd):
                raise PyQtUICompilerError("{cmd} failed".format(cmd=cmd))

