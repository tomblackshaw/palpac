'''
Created on May 19, 2024

@author: Tom Blackshaw

stringstuff
'''

import os
import random
import string
from urllib.parse import urlparse

import requests

from my.classes import logit
from my.tools import SelfCachingCall, StillAwaitingCachedValue

MAX_RANDGENSTR_LEN = 99999  # used by generate_random_string()


def url_validator(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except AttributeError:
        return False


def add_to_os_path_if_existent(a_path, strict=True):
    """If path exists, add it to the PATH environmental variable.

    I add the specified path to the PATH environmental variable. If the
    path does not exist, I do not add it. If strict==True, I raise an
    exception.

    Args:
        a_path (str): path to be added.
            The path should exist. If it does not, I do not
            add it to PATH.
        strict (bool, optional): enforce rules.
            If True *and* path 'a_path' does not exist, raise an exception.
            If False, merely write a warning w/ logit() and do not add
            the path to PATH.

    Returns:
        n/a

    Raises:
        ValueError: If `a_path` does not exist *and* `strict` is True.

    """
    if not os.path.exists(a_path):
        if strict:
            raise ValueError("{a_path} does not exist. I refuse to add a nonexistent path to the PATH environmental variable".format(a_path=a_path))
        else:
            logit("Choosing not to add a nonexistent path {a_path} to env var PATH".format(a_path=a_path))
    else:
        logit("Adding path {a_path} to env var PATH".format(a_path=a_path))
        os.environ['PATH'] += os.pathsep + a_path


def get_random_zenquote_SUB():
    """Return an uplifting quote.

    Using the API at https://zenquotes.io, I retrieve a random quote --
    something uplifting -- and return it as a string.

    Args:
        n/a

    Returns:
        str: Random uplifting message string.

    Raises:
        TimeoutError: Timed out while attempting to access ZenQuotes.
        ConnectionError: ZenQuotes is refusing connections.
        KeyError, IndexError: ZenQuotes generated a mangled output.

    """
    response = requests.get('https://zenquotes.io/api/random')
    data = response.json()[0]
    quote = data['q'] + ' - ' + data['a']
    return quote


our_randomquote_caching_call = None


def get_random_quote(force_update=False):
    """Obtain a (locally cached) uplifting quote from ZenQuote.

    Using a locally cached copy of the most recent

    Args:
        force_update (bool): If True, force the cache to update.

    Returns:
        str: The resultant quote.

    Raises:
        StillAwaitingCachedValue: Unable to get cached quote.

    """
    global our_randomquote_caching_call
    if our_randomquote_caching_call is None:
        our_randomquote_caching_call = SelfCachingCall(300, get_random_zenquote_SUB)
        force_update = True
    try:
        if force_update:
            our_randomquote_caching_call._update_me()
        return our_randomquote_caching_call.result
    except (TimeoutError, ConnectionError, KeyError, IndexError, StillAwaitingCachedValue):
        raise StillAwaitingCachedValue("Still trying to get inspirational quote from ZenQuote")


def flatten(xss):
    return [x for xs in xss for x in xs]


def wind_direction_str(degrees):
    degrees = degrees % 360
    winddirection_lst = ['North', 'North North East', 'Northeast', 'East Northeast', 'East', 'East Southeast', 'Southeast', 'South Southeast',
                         'South', 'South Southwest', 'Southwest', 'West Southwest', 'West', 'West Northwest', 'Northwest', 'North Northwest']
    degrees_entry = int(degrees / 22.5)
    if 0 <= degrees_entry < len(winddirection_lst):
        return winddirection_lst[degrees_entry]
    else:
        return "unknown"


def generate_random_string(length):
    """Generate a N-chars-long random alphanumeric string. Max length: 99999 chars. Purely arbitrary."""
    max_len = MAX_RANDGENSTR_LEN
    if type(length) is not int or length < 0 or length > max_len:
        raise TypeError("Please specify a length of type integer between 0 and {max_len}".format(max_len=max_len))
    x = "".join(
        random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
        for _ in range(length)
    )
    return x

