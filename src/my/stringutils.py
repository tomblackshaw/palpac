'''
Created on May 19, 2024

@author: Tom Blackshaw

stringstuff
'''

from urllib.parse import urlparse
import os
import random
import string

import requests

from my.exceptions import WebAPITimeoutError, WebAPIOutputError
from my.tools import logit

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


def get_random_zenquote(timeout=10):
    """Return an uplifting quote.

    Using the API at https://zenquotes.io, I retrieve a random quote --
    something uplifting -- and return it as a string.

    Args:
        n/a

    Returns:
        str: Random uplifting message string.

    Raises:
        WebAPITimeoutError: Unable to access website to get quote.
        WebAPIOutputError: Website's output was incomprehensible.

    """
    response = requests.get('https://zenquotes.io/api/random', timeout=timeout)
    try:
        data = response.json()[0]
        quote = data['q'] + ' - ' + data['a']
    except (TimeoutError, ConnectionError) as e:
        raise WebAPITimeoutError("The ZenQuotes website timed out") from e
    except (KeyError, IndexError) as e:
        raise WebAPIOutputError("The output from the ZenQuotes website was incomprehensible") from e
    else:
        return quote


__our_randomquote_caching_call = None


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


def convert_24h_and_mins_to_shorttime(time_24h, time_minutes, diff=0):
    # TODO: write me
    if diff != 0:
        time_minutes += diff
        while time_minutes < 0:
            time_minutes += 60
            time_24h -= (diff // 60)
        while time_minutes >= 60:
            time_minutes -= 60
            time_24h += (diff // 60)

    if time_minutes == 0:
        if time_24h == 0:
            return '%d midnight' % (time_24h + 12)
        if time_24h < 12:
            return '%dAM' % (time_24h + 12)
        elif time_24h == 12:
            return '%d noon' % time_24h
        elif time_24h < 24:
            return '%dPM' % (time_24h - 12)
        else:
            return '%d hours (how is that possible)' % time_24h
    else:
        if time_24h < 12:
            return '%d:%02dAM' % (time_24h + 12, time_minutes)
        else:
            return '%d:%02dAM' % (time_24h - 12, time_minutes)
