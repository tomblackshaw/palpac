'''
'''
import copy
import datetime
import random
import string
from threading import Condition, Lock, Thread
from time import sleep
import time


def logit(s, logfile_fname='/tmp/null.txt'):
    datestr = "{:%B %d, %Y @ %H:%M:%S}".format(datetime.datetime.now())
    s = '%s  %s' % (datestr, s)
    try:
        with open(logfile_fname, 'a+') as f:
            f.write('%s\n' % s)
    except:
        pass
    print(s)


def singleton(cls):
    """
    See http://stackoverflow.com/questions/674304/pythons-use-of-new-and-init?ref=mythemeco&t=pack for explanation
    """
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return getinstance


class ReadWriteLock:
    """ A lock object that allows many simultaneous "read locks", but
    only one "write lock." """

    def __init__(self):
        self._read_ready_lck = Lock()
        self._read_ready = Condition(self._read_ready_lck)
        self._readers = 0

    def locked(self):
        return self._read_ready_lck.locked()

    def acquire_read(self):
        """ Acquire a read lock. Blocks only if a thread has
        acquired the write lock. """
        self._read_ready.acquire()
        try:
            self._readers += 1
        finally:
            self._read_ready.release()

    def release_read(self):
        """ Release a read lock. """
        self._read_ready.acquire()
        try:
            self._readers -= 1
            if not self._readers:
                self._read_ready.notifyAll()
        finally:
            self._read_ready.release()

    def acquire_write(self):
        """ Acquire a write lock. Blocks until there are no
        acquired read or write locks. """
        self._read_ready.acquire()
        while self._readers > 0:
            self._read_ready.wait()

    def release_write(self):
        """ Release a write lock. """
        self._read_ready.release()

