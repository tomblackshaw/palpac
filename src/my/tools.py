# -*- coding: utf-8 -*-
"""my.tools

Created on May 19, 2024

@author: Tom Blackshaw

This module demonstrates documentation. Docstrings may extend over multiple lines. Sections are created
with a section header and a colon followed by a block of indented text.

Example:
    Examples can be given using either the ``Example`` or ``Examples``
    sections. Sections support any reStructuredText formatting, including
    literal blocks::

        $ python example_google.py

Section breaks are created by resuming unindented text. Section breaks
are also implicitly created anytime a new section starts.

Attributes:
    module_level_variable1 (int): Module level variables may be documented in
        either the ``Attributes`` section of the module docstring, or in an
        inline docstring immediately following the variable.

        Either form is acceptable, but the two should not be mixed. Choose
        one convention to document module level variables and be consistent
        with it.

Todo:
    * For module TODOs
    * You have to also use ``sphinx.ext.todo`` extension

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
    """Example function with types documented in the docstring.

    `PEP 484`_ type annotations are supported. If attribute, parameter, and
    return types are annotated according to `PEP 484`_, they do not need to be
    included in the docstring:

    Args:
        param1 (int): The first parameter.
        param2 (str): The second parameter.

    Returns:
        bool: The return value. True for success, False otherwise.

    .. _PEP 484:
        https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

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
    """Example function with types documented in the docstring.

    `PEP 484`_ type annotations are supported. If attribute, parameter, and
    return types are annotated according to `PEP 484`_, they do not need to be
    included in the docstring:

    Args:
        param1 (int): The first parameter.
        param2 (str): The second parameter.

    Returns:
        bool: The return value. True for success, False otherwise.

    .. _Style Guide:
        https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

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

