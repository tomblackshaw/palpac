#!/usr/bin/python3

'''
Created on May 19, 2024

@author: Tom Blackshaw

tools

import os

from tools.selfcachingcall import SelfCachingCall

GVAR = 5
def myfunc(addme):
    global GVAR
    GVAR += addme
    return GVAR

c = SelfCachingCall(2, myfunc, 100)
d = SelfCachingCall(5, os.system, "ping -W2 -c1 cinqcent.local > /dev/null 2> /dev/null")
[all_mac_addresses_dct[k]['pinger'].result for k in all_mac_addresses_dct.keys()]
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


class Error(Exception):
    """Base class for other exceptions"""

    def __init__(self, message):
        super().__init__(message)


class CachingError(Error):
    """Class for all caching errors"""

    def __init__(self, message):
        super().__init__(message)


class StillAwaitingCachedValue(CachingError):
    """If we're trying to access a cached value that hasn't been cached yet.

    The class SelfCachingCall() calls the supplied function every N seconds
    and stores the result. If the result is an exception, it stores that.
    Either way, it replies with the result (or the exception) when the
    programmer asks for it. In this way, the programmer can receive
    instantaneously the result of a function call without having to wait
    for it to run.

    Of course, this means that there won't be a result at first. Otherwise,
    the programmer would have to wait until the first result had been cached:
    the opposite of the intended purpose of this class. Granted, the programmer
    would have to wait only once; still, I don't like that. I would rather
    raise an exception and say, "We haven't cached the first value yet."

    Example:
        >>> from my.classes import SelfCachingCall
        >>> c = SelfCachingCall(2, myfunc, 100)
        >>> c.result
        my.globals.exceptions.StillAwaitingCachedValue: We have not cached the first result yet
        >>> sleep(1); c.result
        605

    Args:
        msg (str): Human readable string describing the exception.
        code (:obj:`int`, optional): Error code.

    Attributes:
        msg (str): Human readable string describing the exception.
        code (int): Exception error code.

    """

    def __init__(self, message):
        super().__init__(message)


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


class SelfCachingCall:
    """Self-repeating call to function; saves result; caches it.

    SelfCachingCall() is a class instance that calls a specific function (with specified parameters)
    every N seconds. The result, including any error, is cached and is made available to the
    programmer. The call happens in the background. An instance of SelfCachingCall() encapsulates that
    functionality and caches the result of the call.

    e.g.
        >>> GVAR = 5
        >>> def myfunc(addme):
                global GVAR
                GVAR += addme
                return GVAR
        >>> from my.classes import SelfCachingCall
        >>> #................freq, func, paramsForfunc
        >>> c = SelfCachingCall(2, myfunc, 100)
        >>> c.result
        my.globals.exceptions.StillAwaitingCachedValue: We have not cached the first result yet
        >>> sleep(1); c.result
        605

    Note:
        If the programmer tries to read the cached value before the first call to the function,
        an exception will be thrown.

    Args:
        refreshfrequency (int): How often should I call the function
        func: What is the function?
        args,kwargs: Pass these parameters to the function

    Methods:
        _update_me(): Force a new call to the function; save the result in our cache.

    Attributes:
        result (int): result of most recent (cached) call to the function that's being cached
            FYI, if the most recent call threw an exception, then the act of getting the result
            attribute will throw that exception. I guess you could say the subroutine didn't
            only catch it; it cached it.

    Exceptions:
        StillAwaitingCachedValue: If we don't have a cached value yet, this exception is raised.

    """

    def __init__(self, refreshfrequency, func, *args, **kwargs):
        assert (isinstance(refreshfrequency, int)
                or isinstance(refreshfrequency, float))
        self.__args = args
        self.__kwargs = kwargs
        self.__func = func
        self.__refreshfrequency = refreshfrequency
        self.__refreshfreq_lock = ReadWriteLock()
        self.__update_lock = ReadWriteLock()
        self.__result = None
        self.__error = StillAwaitingCachedValue(
            'We have not cached the first result yet')
        self.__result_and_error_lock = ReadWriteLock()
        self.__time_to_join = False
        self.__keepupdating_thread = Thread(target=self._keep_updating)
        self.__keepupdating_thread.daemon = True
        self.__keepupdating_thread.start()
        super().__init__()

    def _keep_updating(self):
        time_left_before_update = 0
        while not self.__time_to_join:
            if time_left_before_update <= 0:
                self._update_me()
                time_left_before_update = self.__refreshfrequency
            else:
                sleep_for_how_long = min(1, time_left_before_update)
                time_left_before_update -= sleep_for_how_long
                sleep(sleep_for_how_long)
        logit('No more soup for you')
#         self.join() # FIXME: Why was this commented out?!

    def _update_me(self):
        try:
            self.__update_lock.acquire_write()
            the_new_result = self.__func(*self.__args, **self.__kwargs)
            the_new_error = None
        except Exception as e:
            the_new_result = None
            the_new_error = e
        finally:
            self.__update_lock.release_write()
        try:
            self.__result_and_error_lock.acquire_write()
            self.__error = the_new_error
            self.__result = the_new_result
        finally:
            self.__result_and_error_lock.release_write()

    @property
    def result(self):
        try:
            self.__result_and_error_lock.acquire_write()
            while True:
                try:
                    retval = copy.deepcopy(self.__result)
                except RuntimeError:
                    logit('value changed while iterating, or something; probably a race condition; retrying...')
                    sleep(1)
                else:
                    reterr = self.__error
                    break
        except Exception as e:
            #             from my.globals.logging import Logger
            logit('SelfCachingCall.result reported this ==> %s' % str(e))
            retval = None
            reterr = e
        finally:
            self.__result_and_error_lock.release_write()
        if reterr is not None:
            raise reterr
        else:
            return retval

    def join(self):
        self.__time_to_join = True
        self.__keepupdating_thread.join()

    @property
    def refreshfrequency(self):
        self.__refreshfreq_lock.acquire_read()
        retval = self.__refreshfrequency
        self.__refreshfreq_lock.release_read()
        return retval

    @refreshfrequency.setter
    def refreshfrequency(self, value):
        self.__refreshfreq_lock.acquire_write()
        self.__refreshfrequency = value
        self.__refreshfreq_lock.release_write()


def timeit(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%r  %2.2f ms' %
                  (method.__name__, (te - ts) * 1000))
        return result

    return timed


def generate_random_string(length):
    """Generate a N-chars-long random alphanumeric string"""
    x = "".join(
        random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
        for _ in range(length)
    )
    return x
