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
from my.consts import default_speaker_alarm_message_dct, alarm_messages_lst
from my.tools import logit

MAX_RANDGENSTR_LEN = 99999  # used by generate_random_string()


def generate_triggerphrase_permutations(listA, listB):
    if type(listA) not in (tuple, list) or type(listB) not in (tuple, list):
        raise TypeError("Both parameters must be either lists or tuples")
    if [] != list(set([type(r) for r in listA if type(r) is not str])) or [] != list(set([type(r) for r in listB if type(r) is not str])):
        raise TypeError("All values within the lists (the parameters) must be strings")
    if [] != list(set([type(r) for r in listA if type(r) is not str or r == ''])) or [] != list(set([type(r) for r in listB if type(r) is not str or r == ''])):
        raise ValueError("All values within the lists (the parameters) must be NON-EMPTY strings")
    if listA in ([], ()) or listB in ([], ()):
        raise ValueError("Both lists must be non-empty")
    lst = []
    for wordA in listA:
        for wordB in listB:
            s = wordA + ' ' + wordB
            lst.append(s)
    return lst


def url_validator(url):
    """Validate URL.

    Examine the supplied string. If it is a valid URL, return True. Otherwise,
    return False.

    Args:
        url (str): The URL to evaluate.

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


def flatten(xss):
    return [x for xs in xss for x in xs]


def wind_direction_str(degrees):
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


def generate_random_string(length):
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


def convert_24h_and_mins_to_shorttime(time_24h, time_minutes, diff=0):
    """Convert the supplied time to a human-readable & pronounceable string.

    Args:
        time_24h (int): The time that has come (hours).
        time_minutes (int): The time that has come (minutes).
        diff (int): How many minutes before/after the specified time
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


def generate_alarm_message(owner, time_24h, time_minutes, message_template):
    """Generate the text of an alarm message.

    Using the specified time and template, generate a human-readable,
    pronounceable string containing a simple but pleasant alarm message.

    Example:
        $ python3
        >>> from my.consts import alarm_messages_lst
        >>> from my.stringutils import generate_alarm_message
        >>> message_template = alarm_messages_lst[0]
        >>> msg = generate_alarm_message('Chuckles', 12, 30, message_template)

    Args:
        time_24h (int): The time that has come (hours).
        time_minutes (int): The time that has come (minutes).
        voice (str): The name of the voice that I am to use.
        message_template (str): Template to be populated by the
            values from the parameters.

    Returns:
        str: The resultant alarm message.

    Raises:
        TypeError: The length field is of an invalid type.
        ValueError: The value of length is an invalid parameter.

    """
    # TODO: Write me
    '''

    '''
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




def generate_random_alarm_message(owner_of_clock, time_24h, time_minutes, voice=None):
    """Example function with types documented in the docstring.

    `PEP 484`_ type annotations are supported. If attribute, parameter, and
    return types are annotated according to `PEP 484`_, they do not need to be
    included in the docstring:

    Args:
        param1 (int): The first parameter.
        param2 (str): The second parameter.

    Returns:
        bool: The return value. True for success, False otherwise.

    TODO: Write me

    """
    if voice in default_speaker_alarm_message_dct.keys():
        message_template = random.choice([default_speaker_alarm_message_dct[voice]] + alarm_messages_lst)
    else:
        message_template = random.choice(alarm_messages_lst)
    message = generate_alarm_message(owner_of_clock, time_24h, time_minutes, message_template)
    return message


def find_trigger_phrase_in_sentence(sentence, triggerphrase):
    """Find trigger phrase in sentence, if it's there.

    Scan the supplied sentence (a string) for the supplied trigger phrase
    (also a string). If the trigger phrase starts at the first or second word
    of the sentence, return its position (an int). Otherwise, return -1.

    Note:
        If the sentence is an empty string (""), that is *not* grounds
        to throw an exception. However, an empty triggerphrase ("")
        *is* grounds for an exception.

    Example:
        $ python3
        >>> from my.stringutils import find_trigger_phrase_in_sentence
        >>> find_trigger_phrase_in_sentence("

    Args:
        sentence (str): The sentence to be scanned.
        triggerphrase (str): The trigger word for which we are searching.

    Returns:
        int: Location of the trigger phrase, if found. Otherwise, -1.

    Raises:
        TypeError: A supplied parameter isn't a string.
        ValueError: A supplied parameter isn't a non-empty string,
            or there are spaces at the start/end of the strings.

    TODO: Write me

    """
    if type(sentence) is not str or type(triggerphrase) is not str:
        raise TypeError("sentence and triggerphrase must be strings")
    if sentence == '':
        return -1
    sentence = sentence.lower()
    triggerphrase = triggerphrase.lower()
    if sentence != sentence.strip() or triggerphrase != triggerphrase.strip():
#        print("Sentence: ==>{sentence}<==".format(sentence=sentence))
#        print("Triggerp: ==>{triggerp}<==".format(triggerp=triggerphrase))
        raise ValueError("sentence and triggerphrase must be strings WITHOUT spaces at start or end")
    if triggerphrase == '':
        raise ValueError("I need a triggerphrase that is at least one character long")
    i = sentence.find(triggerphrase)
    if i >= 0:
#        print("Found triggerphrase in sentence")
        if i == 0 or sentence[i - 1] == ' ':
#            print("Triggerphrase begins at the start of the sentence *or* in front of a space")
            j = i + len(triggerphrase)
            if j >= len(sentence) or sentence[j] == ' ':
#                print("Triggerphrase ends at the end of the sentence *or* at a space")
                return i
    # words_lst = sentence.split(' ')
    # noof_words = len(words_lst)
    # upperlimit = noof_words if scan_first_N_words is None else min(noof_words, scan_first_N_words)
    # for wordnum in range(0, upperlimit):
    #     if words_lst[wordnum] == triggerphrase:
    #         return sentence.index(' ' + triggerphrase) + 1 if wordnum > 0 else 0
    return -1


def scan_sentence_for_any_one_of_these_trigger_phrases(sentence, triggerphrases):
    if sentence == '':
        return -1
    for tp in triggerphrases:
        cutoff_point = find_trigger_phrase_in_sentence(sentence, tp)
        if cutoff_point >= 0:
            cutoff_point += len(tp)
            return min(cutoff_point + 1, len(sentence))  # to allow for a trailing space
    return -1


def trim_away_the_trigger_and_locate_the_command_if_there_is_one(sentence, triggerphrases):
    cutoff_point = scan_sentence_for_any_one_of_these_trigger_phrases(sentence, triggerphrases)
    limiter = 16
    if cutoff_point >= 0:
        while True:
            another_cup = cutoff_point + scan_sentence_for_any_one_of_these_trigger_phrases(sentence[cutoff_point:cutoff_point + limiter].rstrip(), triggerphrases)
#            print("another cup =", another_cup)
            if another_cup >= cutoff_point:
#                print("Why'd you say it twice?", sentence[cutoff_point:], "...becomes...", sentence[cutoff_point + another_cup:])
                cutoff_point = another_cup
            else:
                break
    return cutoff_point


def text2time(incoming_time_text):
    dct = {'midnight':(0, 0), 'noon':(12, 0), 'midday':(12, 0), 'twelve noon':(12, 0), 'twelve midnight':(0, 0), 'twelve midnight':(0, 0)}
    if incoming_time_text in dct.keys():
        return dct[incoming_time_text]
    pot_values_lst = ['0', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten',
                             'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty', 'twenty one', 'twenty two', 'twenty three', 'twenty four']
    sortedbylength_pot_values = ['twenty three', 'twenty four', 'twenty one', 'twenty two', 'seventeen', 'thirteen', 'fourteen', 'eighteen', 'nineteen', 'fifteen', 'sixteen', 'eleven', 'twelve', 'twenty', 'three', 'seven', 'eight', 'four', 'five', 'nine', 'one', 'two', 'six', 'ten', '0']
    tens_lst = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    txt = (' ' + incoming_time_text + ' '
           ).replace(' twenty four hundred ', ' zero hundred '
           ).replace(' oh ', ' 0 ').replace(' zero ', ' 0 ').replace(' hundred hours ', ' hundred ').replace(' hundred ', ' 00 '
           )

    am_or_pm = ''
    if txt[-3:] in ('am ', 'pm '):
        am_or_pm = txt[-3:-1]
        txt = txt[:-3]

    hr_mn_split = -1
    for s in sortedbylength_pot_values:
        hr_mn_split = txt.find(s + ' ')
        if s != '' and hr_mn_split in (0, 1):
            hrs_str = txt[:hr_mn_split+len(s)] + ' '
            mns_str = ' ' + txt[hr_mn_split+len(s)+1:]
            break
    if hr_mn_split < 0:
        raise ValueError( "Unable to decode {incoming_time_text}. I made it as far as {txt} and failed to find the hour string.".format(incoming_time_text=incoming_time_text,txt=txt))

    for i in range(0, len(pot_values_lst)):
        hrs_str = hrs_str.replace(' {t} '.format(t=pot_values_lst[i]), ' {i} '.format(i=i))
        mns_str = mns_str.replace(' {t} '.format(t=pot_values_lst[i]), ' {i} '.format(i=i))

    for i in range(0, len(tens_lst)):
        mns_str = mns_str.replace(' {t} '.format(t=tens_lst[i]), ' {i} '.format(i=i * 10))

    hrs_str = hrs_str.strip().replace('0 ', '')
    mns_str = mns_str.strip().replace('0 ', '')
    try:
        hrs = 0 if hrs_str == '' else int(hrs_str.replace(' ', ''))
        mns = 0 if mns_str == '' else int(mns_str.replace(' ', ''))
    except ValueError as e:
        raise ValueError("Unable to decode {incoming_time_text}. I made it as far as {txt} ==> {hrs_str}:{mns_str} and I failed to decode the hr&mn.".format(
                                    incoming_time_text=incoming_time_text, txt=txt, hrs_str=hrs_str, mns_str=mns_str)) from e
    #
    # our_int = int(txt)
    # if our_int >= 24 and our_int < 100:
    #     raise ValueError("Unable to decode {incoming_time_text}. I made it as far as {txt} but I can't figure out how many hours we want.".format(incoming_time_text=incoming_time_text, txt=txt))
    #
    # our_int = (our_int % 2400)
    # if our_int < 24:
    #     our_hours = our_int
    #     our_minutes = 0
    # else:
    #     assert(our_int >= 100)
    #     our_hours = our_int // 100
    #     our_minutes = our_int % 100
    if am_or_pm == 'pm' and hrs < 12:
        hrs += 12
    if am_or_pm == 'am' and hrs == 12:
        hrs -= 12
    if hrs >= 24 or mns >= 60:
        raise ValueError("Unable to decode {incoming_time_text}. I made it as far as {txt} but hours={hours} and minutes={minutes}...? Really?".format(
            incoming_time_text=incoming_time_text, txt=txt, hours=hrs, minutes=mns))
    return (hrs, mns)

