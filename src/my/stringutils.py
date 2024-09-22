# -*- coding: utf-8 -*-
"""my.stringutils

Created on May 19, 2024

@author: Tom Blackshaw

This module contains string utilities that I have written for this
project.

Attributes:
    n/a

.. _Style Guide:
   https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

"""

from urllib.parse import urlparse
import os
import random
import string

import requests

from my.classes.exceptions import WebAPITimeoutError, WebAPIOutputError
from my.consts import alarm_messages_lst, postsnooze_alrm_msgs_lst
from my.tools import logit

MAX_RANDGENSTR_LEN = 99999  # used by generate_random_string()


def url_validator(url:str) -> bool:
    """Validate URL.

    Examine the supplied string. If it is a valid URL, return True. Otherwise,
    return False.

    Args:
        url: The URL to evaluate.

    Returns:
        bool: Is it a valid URL? True for yes. False for no.

    Raises:
        TypeError: The parameter is not a string.

    """
    if type(url) is not str:
        raise TypeError("{url} should have been a string. Please send a string next time.".format(url=str(url)))
    if not url.startswith('http'):
        return False
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except AttributeError:
        return False


def add_to_os_path_if_existent(a_path:str, strict:bool=True):
    """If path exists, add it to the PATH environmental variable.

    I add the specified path to the PATH environmental variable. If the
    path does not exist, I do not add it. If strict==True, I raise an
    exception.

    Args:
        a_path: path to be added.
            The path should exist. If it does not, I do not
            add it to PATH.
        strict (optional): enforce rules.
            If True *and* path 'a_path' does not exist, raise an exception.
            If False, merely write a warning w/ logit() and do not add
            the path to PATH.

    Raises:
        ValueError: If `a_path` does not exist *and* `strict` is True.

    """
    if type(a_path) is not str:
        raise TypeError("{a_path} should have been a string. Please send a string next time.".format(a_path=str(a_path)))
    if not os.path.exists(a_path):
        if strict:
            raise ValueError("{a_path} does not exist. I refuse to add a nonexistent path to the PATH environmental variable".format(a_path=a_path))
        else:
            logit("Choosing not to add a nonexistent path {a_path} to env var PATH".format(a_path=a_path))
    else:
        logit("Adding path {a_path} to env var PATH".format(a_path=a_path))
        os.environ['PATH'] += os.pathsep + a_path


def get_random_zenquote(timeout:int=10) -> str:
    """Return an uplifting quote.

    Using the API at https://zenquotes.io, I retrieve a random quote --
    something uplifting -- and return it as a string.

    Args:
        timeout (optional): Timeout before returning string (or failing).

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


def flatten(xss):
    return [x for xs in xss for x in xs]


def wind_direction_str(degrees:int) -> str:
    """Return the wind direction string, based on the degrees field.

    The supplied number of degrees will be turned into a string that describes
    the direction in human-readable form.

    Examples:
        $ python3
        >>> from my.stringutils import wind_direction_str
        >>> wind_direction_str(0)
        'North'
        >>> wind_direction_str(359)
        'North Northwest'

    Args:
        degrees (int or float): The number of degrees.

    Returns:
        str: The human-readable descriptor of that number of degrees.

    Raises:
        TypeError: Type of parameter is wrong. It should be int or float.
        ValueError: Parameter should be >=0 and <360.

    """
    if type(degrees) not in (int, float):
        raise TypeError("Wind direction must be an integer or a float, not a {t}".format(t=str(type(degrees))))
    if degrees < 0 or degrees >= 360:
        raise ValueError("Wind direction must be between 0 and 360; {degrees} is not. Please correct this.".format(degrees=degrees))
    degrees = degrees % 360
    winddirection_lst = ['North', 'North North East', 'Northeast', 'East Northeast', 'East', 'East Southeast', 'Southeast', 'South Southeast',
                         'South', 'South Southwest', 'Southwest', 'West Southwest', 'West', 'West Northwest', 'Northwest', 'North Northwest']
    degrees_entry = int(degrees / 22.5)
    if 0 <= degrees_entry < len(winddirection_lst):
        return winddirection_lst[degrees_entry]
    else:
        raise ValueError()


def generate_random_string(length:int) -> str:
    """Generate a N-chars-long random alphanumeric string.

    Generate a random string, composed of digits and lowercase letters and digits.
    The maximum length is MAX_RANDGENSTR_LEN characters. The limit is purely
    arbitrary, as far as I know.

    Note:
        Although a zero-length random string would equal '', I choose to
        raise an exception instead: no programmer will deliberately ask
        for a zero-length random string.

    Args:
        length (int): The desired length of the random string. It must be
            between 1 and MAX_RANDGENSTR_LEN, inclusive.

    Returns:
        str: The random string that I have generated.

    Raises:
        TypeError: The length field is of an invalid type.
        ValueError: The value of length is an invalid parameter.

    """
    max_len = MAX_RANDGENSTR_LEN
    if type(length) is not int:
        raise TypeError("Please specify a length of type int, not {t}".format(t=type(length)))
    if length <= 0 or length > max_len:
        raise ValueError("Please specify a length of type integer between 1 and {max_len}".format(max_len=max_len))
    x = "".join(
        random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
        for _ in range(length)
    )
    return x


def convert_24h_and_mins_to_shorttime(time_24h:int, time_minutes:int, diff:int=0) -> str:
    """Convert the supplied time to a human-readable & pronounceable string.

    Args:
        time_24h: The time that has come (hours).
        time_minutes: The time that has come (minutes).
        diff: How many minutes before/after the specified time
            should I calculate?

    Returns:
        str: Resultant simple time string.

    Raises:
        TypeError: The supplied parameters are of the wrong type.
        ValueError: The parameters are outside the valid range.

    TODO: Use datetime().

    """
    if type(time_24h) is not int:
        raise TypeError("time_24h needs to be an integer, not a %s" % str(type(time_24h)))
    if  type(time_minutes) is not int:
        raise TypeError("time_minutes needs to be an integer, not a %s" % str(type(time_minutes)))
    if  type(diff) is not int:
        raise TypeError("diff needs to be an integer, not a %s" % str(type(diff)))
    if not (0 <= time_24h <= 23):
        raise ValueError("time_24h must be >=0 and <=23")
    if not (0 <= time_minutes <= 59):
        raise ValueError("time_minutes must be >=0 and <=59")
    while diff > 0:
        diff -= 1
        time_minutes += 1
        if time_minutes >= 60:
            time_minutes -= 60
            time_24h += 1
            if time_24h >= 24:
                time_24h -= 24
    while diff < 0:
        diff += 1
        time_minutes -= 1
        if time_minutes < 0:
            time_minutes += 60
            time_24h -= 1
            if time_24h < 0:
                time_24h += 24

    if time_minutes == 0:
        if time_24h == 0:
            return '%d midnight' % (time_24h + 12)
        elif time_24h < 12:
            return '%d A.M.' % (time_24h)
        elif time_24h == 12:
            return '%d newn' % time_24h
        elif time_24h < 24:
            return '%d P.M.' % (time_24h - 12)
        else:
            return '%d hours (how is that possible)' % time_24h
    else:
        if time_24h < 12:
            return '%d:%02d A.M.' % (12 if time_24h in (0, 12, 24) else time_24h, time_minutes)
        else:
            return '%d:%02d P.M.' % (12 if time_24h in (0, 12, 24) else time_24h % 12, time_minutes)


def generate_detokenized_message(owner:str, time_24h:int, time_minutes:int, message_template:str) -> str:
    """Generate the text of an alarm or otherwise tokenized message.

    Using the specified time and template, generate a human-readable,
    pronounceable string containing a simple but pleasant alarm message.

    Example:
        $ python3
        >>> from my.consts import alarm_messages_lst
        >>> from my.stringutils import generate_alarm_message
        >>> message_template = alarm_messages_lst[0]
        >>> msg = generate_alarm_message('Chuckles', 12, 30, message_template)

    Args:
        time_24h: The time that has come (hours).
        time_minutes: The time that has come (minutes).
        voice: The name of the voice that I am to use.
        message_template: Template to be populated by the
            values from the parameters.

    Returns:
        str: The resultant alarm message.

    Raises:
        TypeError: The length field is of an invalid type.
        ValueError: The value of length is an invalid parameter.

    """
    from my.consts import hello_owner_lst
    if owner == '' or owner is None:
        raise ValueError("Owner -- the name of the human who owns this alarm clock -- needs to be a non-empty string. You supplied a duff value.")
    if type(time_24h) is not int or type(time_minutes) is not int or time_24h < 0 or time_24h >= 24 or time_minutes < 0 or time_minutes >= 60:
        raise ValueError("You supplied a duff hour and/or minute.")
    shorttime = convert_24h_and_mins_to_shorttime(time_24h, time_minutes)
    one_minute_ago = convert_24h_and_mins_to_shorttime(time_24h, time_minutes, diff=-1)
    one_minute_later = convert_24h_and_mins_to_shorttime(time_24h, time_minutes, diff=1)
    hello_owner = random.choice(hello_owner_lst)
    morning_or_afternoon_or_evening = 'morning' if time_24h < 12 else 'afternoon' if time_24h < 18 else 'evening'
    newval = message_template
    for _ in range(0, 5):
        oldval = newval
        ov_template = string.Template(oldval)
        newval = ov_template.substitute(hello_owner=hello_owner, owner=owner, shorttime=shorttime, one_minute_ago=one_minute_ago, one_minute_later=one_minute_later, morning_or_afternoon_or_evening=morning_or_afternoon_or_evening)
#        print("""{oldval} ==> {newval}""".format(oldval=oldval, newval=newval))
# s = message_template.replace('${', '').replace('}', '').replace('hello_owner', hello_owner).replace('owner', owner
#                         ).replace('shorttime', shorttime).replace('one_minute_ago', one_minute_ago
#                         ).replace("one_minute_later", one_minute_later).replace("morning_or_afternoon_or_evenin", morning_or_afternoon_or_evening)
    if '${' in newval:
        raise KeyError("Unresolved variable in {newval}. Look for the string in braces and check your source code.".format(newval=newval))
    return newval


def generate_random_alarm_message(owner_of_clock:str, time_24h:int,  time_minutes:int, snoozed:bool=False) -> str:
    """Example function with types documented in the docstring.

    `PEP 484`_ type annotations are supported. If attribute, parameter, and
    return types are annotated according to `PEP 484`_, they do not need to be
    included in the docstring:

    Args:
        owner_of_clock: The person whose alarm clock it is.
        time_24h: hour.
        time_minutes: minutes.
        snoozed: If we're snoozing or not.

    Returns:
        str: Alarm message.

    TODO: Write me

    """
    if snoozed:
        message_template = random.choice(postsnooze_alrm_msgs_lst)
    else:
        message_template = random.choice(alarm_messages_lst)
    message = generate_detokenized_message(owner_of_clock, time_24h, time_minutes, message_template)
    return message



def pathname_of_phrase_audio(voice:str, text:str) -> str:
    if len(text) > 0 and text[0] == '.':
        text = text[1:]
    return 'audio/cache/{voice}/{text}.mp3'.format(voice=voice, text=text.lower().replace(' ', '_'))

