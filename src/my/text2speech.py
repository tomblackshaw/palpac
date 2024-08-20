# -*- coding: utf-8 -*-
"""my.text2speech

Created on May 19, 2024

@author: Tom Blackshaw

Module for interacting with the ElevenLabs text-to-speech API. There is a
lot of cool stuff in here.

Example:
    Here is one::

        $ python3
        >>> from my.text2speech import Text2SpeechSingleton as tts
        >>> s = "Hello there. There's a car in the bar, by the farm."
        >>> tts.say(s)
        >>> for i in range(0,10): tts.name = tts.random_voice; audiodata = tts.audio(s); tts.play(audiodata)

Section breaks are created by resuming unindented text. Section breaks
are also implicitly created anytime a new section starts.

Attributes:
    Text2SpeechSingleton (_Text2SpeechClass): The singleton

.. _Style Guide:
   https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html


"""

import os
import random
import string
import sys

from pydub.exceptions import CouldntDecodeError

from my.classes.exceptions import NoProfessionalVoicesError, MissingFromCacheError
from my.classes.text2speechclass import convert_audio_recordings_list_into_one_audio_recording, convert_audio_recordings_list_into_an_mp3_file
from my.consts import hours_lst, minutes_lst
from my.stringutils import generate_random_alarm_message, convert_24h_and_mins_to_shorttime, generate_detokenized_message, pathname_of_phrase_audio

try:
    from my.classes.text2speechclass import _Text2SpeechClass
    Text2SpeechSingleton = _Text2SpeechClass()
except ModuleNotFoundError:
    Text2SpeechSingleton = None  # compatibility w/ Python 3.8


def get_first_prof_name(tts):
    """Get the name of the first professional-grade voice.

    On the programmer's Eleven Labs account, there may be a professional-
    grade voice available (or there may not). If there is one, return its
    name. If there are two or more, return the name of the first one. If
    there are none, raise a NoProfessionalVoicesError exception.

    Args:
        tts (Text2SpeechSingleton): The singleton by which to access
            the Eleven Labs API.

    Returns:
        str: The name of the first available professional-grade voice.

    Raises:
        NoProfessionalVoicesError: There is no professional-grade voice
            available via the configured Eleven Labs account.

    """
    try:
        return [r for r in tts.api_voices if r.samples is not None][0].name
    except (IndexError, KeyError, ValueError) as e:
        raise NoProfessionalVoicesError("There are no professional-grade voices available from your Eleven Labs account.") from e


def speak_random_alarm(owner_name, time_24h, time_minutes, voice=None, tts=Text2SpeechSingleton):
    """Speak an alarm warning.

    In the specified voice, to the specified owner of the alarm clock, speak an alarm
    to alert the alarm clock user that a specific time has come.

    Args:
        owner_name (str): First name of the owner of the alarm clock.
        time_24h (int): The time that has come (hours).
        time_minutes (int): The time that has come (minutes).
        voice (str): The name of the voice that I am to use.

    """
    if voice is None:
        voice = tts.random_voice
#    tts.voice = voice
#    del voice
    message = generate_random_alarm_message(owner_name, time_24h, time_minutes, voice)
    prof_name = get_first_prof_name(tts)  # [r for r in tts.api_voices if r.samples is not None][0].name
    if voice == prof_name:
        d = tts.audio(text=message, advanced=True, model='eleven_multilingual_v2', stability=0.30, similarity_boost=0.01, style=0.90, use_speaker_boost=True)
    else:
        d = tts.audio(text=message)
    tts.play(d)


def speak_totally_randomized_alarm_and_time(owner_of_clock):
    """It does what it says on the tin."""
    time_24h = random.randint(0, 24)
    time_minutes = random.randint(0, 60)
    speak_random_alarm(owner_of_clock, time_24h, time_minutes)


def play_dialogue_lst(tts, dialogue_lst):  # , stability=0.5, similarity_boost=0.01, style=0.5):
    """Recites dialogue.

    Using the Eleven Labs website's API, their Python module, and mpv/ffmpeg, I play
    the supplied dialogue list. 'Do' the named voices, too. FYI, the API's key is
    stored at ~/$ELEVENLABS_KEY_BASENAME.

    Args:
        tts: Text-to-speech singleton Text2SpeechSingleton.
        dialogue_lst: List of dialogue tuples. The first item is the name of the voice
            to be used. The second item is the text to be recited.
        stability: The stability level (between 0.3 and 1.0 recommended).
        similarity_boost: The similarity level (between 0.01 and 1.0 recommended).
        style: The similarity level (between 0.0 and 0.5 recommended).

    Example:
        $ python3
        >>> from my.text2speech import play_dialogue_lst, Text2SpeechSingleton as tts
        >>> play_dialogue_lst(tts, [('Jessie', 'Knock, knock'),('Freya', 'Get a warrant.')])

    Returns:
        n/a

    Raises:
        unknown. FIXME: list the potential exceptions

    """
    data_to_play = []
    from my.tools import logit
    for (name, text) in dialogue_lst:
        logit("{name}: {text}".format(name=name, text=text))
        tts.voice = name
        data_to_play.append(tts.audio(text))
    tts.play(data_to_play)
    # for d in data_to_play:
    #     tts.play(d)



def phrase_audio(voice, text, raise_exception_if_not_cached=False):
    text = text.lower().strip(' ')
    if len(text) > 1:
    # if text not in ('!', '?', '.', ','):
        while len(text) > 0 and text[0] in ' !?;:.,':
            text = text[1:]
    outfile =pathname_of_phrase_audio(voice, text)
    if not os.path.exists(outfile):
        if raise_exception_if_not_cached:
            raise MissingFromCacheError("'{text}' (for {voice}) should have been cached not hasn't been.".format(text=text, voice=voice))
        print(voice, '==>', text)
        print("Generating speech audio (spoken by {voice}) for '{text}'".format(voice=voice, text=text))
        os.system('mkdir -p "{mydir}"'.format(mydir=os.path.dirname(outfile)))
#        try:
#            os.mkdir(os.path.dirname(outfile))
#        except FileExistsError:
#            pass
        vers = sys.version_info
        major_ver, minor_ver = vers[:2]
        if major_ver < 3 or minor_ver < 11:
            os.system('''./_cachespeech.sh "{voice}" "{text}" "{outfile}"'''.format(voice=voice, text=text, outfile=outfile))
        else:
            with open(outfile, 'wb') as f:
                print("Writing >%s<" % outfile)
                old_v = Text2SpeechSingleton.voice
                Text2SpeechSingleton.voice = voice
                f.write(Text2SpeechSingleton.audio(text))
                Text2SpeechSingleton.voice = old_v
    with open(outfile, 'rb') as f:
        return f.read()


def list_phrases_to_handle(smart_phrase):
    phrases_to_handle = []
    while len(smart_phrase) > 0:
        i = smart_phrase.find('${')
        if i < 0:
            phrases_to_handle.append(smart_phrase)
            smart_phrase = ''
        else:
            phrases_to_handle.append(smart_phrase[:i])
            j = smart_phrase.find('}', i)
            smart_phrase = smart_phrase[j+1:]
    return phrases_to_handle


def decoded_token(token, hello_owner, owner, shorttime, one_minute_ago, one_minute_later, morning_or_afternoon_or_evening):
    newval = token
    for _ in range(0, 5):
        oldval = newval
        ov_template = string.Template(oldval)
        newval = ov_template.substitute(hello_owner=hello_owner, owner=owner, shorttime=shorttime, one_minute_ago=one_minute_ago, one_minute_later=one_minute_later, morning_or_afternoon_or_evening=morning_or_afternoon_or_evening)
    return newval


def deliberately_cache_a_smart_phrase(voice, smart_phrase):
    phrases_to_handle = list_phrases_to_handle(smart_phrase)
    for phrase in phrases_to_handle:
        audio_op = phrase_audio(voice, phrase)
        try:
            _ = convert_audio_recordings_list_into_one_audio_recording([audio_op], trim_level=1)

        except CouldntDecodeError:
            print('"%s" (%s) failed. Retrying.' % (phrase, voice))
            os.unlink(pathname_of_phrase_audio(voice, phrase))
            deliberately_cache_a_smart_phrase(voice, phrase)
            print('"%s" (%s) regenerated successfully.' % (phrase, voice))


def smart_phrase_audio(voice, smart_phrase, owner=None, time_24h=None, time_minutes=None, trim_level=1):
    if owner is not None and time_24h is not None and time_minutes is not None:
        detokenized_phrase = generate_detokenized_message(owner, time_24h, time_minutes, smart_phrase)  # Decoder. FIXME. Document!
        detokenized_phrase = detokenized_phrase.replace('12 noon', '12:00 P.M.').replace('12 midnight', '12:00 A.M.')  # FIXME hack hack hack
    else:
#        print('No detokenizing possible')
        detokenized_phrase = ''.join(r + ' ' for r in list_phrases_to_handle(smart_phrase)).strip(' ')
    detokenized_phrase = detokenized_phrase.lower()
    data = []
    all_words = [r.lower().strip(' ') for r in detokenized_phrase.split(' ')]
    firstwordno = 0
    while firstwordno < len(all_words):
        lastwordno = len(all_words)
        while lastwordno > firstwordno:
            searchforthis = ''.join([r + ' ' for r in all_words[firstwordno:lastwordno]]).strip()
#            while len(searchforthis) > 0 and searchforthis[0] in (';:,.!?'):
#                searchforthis = searchforthis[1:]
#            print('looking for >>%s<<' % searchforthis)
            if not os.path.exists(pathname_of_phrase_audio(voice, searchforthis)):
                lastwordno -= 1
            elif len(searchforthis) == 0:
                break
            else:
                firstwordno = lastwordno - 1
                print("GOT IT (%s) >>%s<<" % (voice, searchforthis))
                data.append(phrase_audio(voice, searchforthis))
                break
        if lastwordno == firstwordno:
            if searchforthis == '':
                pass
                print('Ignoring', searchforthis)
            elif ':' in searchforthis and len(searchforthis) >= 4:
                if lastwordno + 1 < len(all_words) and all_words[lastwordno + 1].lower()[:4] in ('a.m.', 'p.m.'):
                    lastwordno += 1
                    searchforthis = ''.join([r + ' ' for r in all_words[firstwordno:lastwordno + 1]]).strip()
                print("TIME <=", searchforthis)
                for s in generate_timedate_phrases_list(voice, searchforthis):
                    print("s =", s)
                    outfile = pathname_of_phrase_audio(voice, s)
                    if not os.path.exists(outfile):
                        raise MissingFromCacheError("{voice} => {s} <= {outfile} => (time thingy) is missing from the cache".format(s=s, voice=voice, outfile=outfile))
                    data.append(phrase_audio(voice, s))
                firstwordno = lastwordno
#                data.append(phrase_audio(voice, searchforthis))
            elif searchforthis in ('?', ':', '!', '.'):
                print("Ignoring", searchforthis)
            else:
                outfile = pathname_of_phrase_audio(voice, searchforthis)
                raise MissingFromCacheError("{voice} => {searchforthis} <= {outfile} => is missing from the cache".format(searchforthis=searchforthis, voice=voice, outfile=outfile))
        firstwordno += 1
    return convert_audio_recordings_list_into_one_audio_recording(data=data, trim_level=trim_level)


def generate_timedate_phrases_list(voice, timedate_str):
    the_hr, the_min = timedate_str.split(':')
    the_hr = the_hr.strip('.')
    the_min = the_min.strip('.')
    the_ampm = ''
    if ' ' in the_min:
        the_min, the_ampm = the_min.split(' ')
    the_ampm = the_ampm[:4].strip(' . ')
    print('the_hr={the_hr}; the_min={the_min}; the_ampm={the_ampm}'.format(the_hr=the_hr, the_min=the_min, the_ampm=the_ampm))
    if the_hr not in (12, '12'):
        print("the_hr is neither 12 nor '12'")
        print(type(the_hr))
    if the_hr in (0, '0') and the_min in (0, '0', '00'):
        return ("twelve midnight",)
    elif the_hr in (12, '12') and the_min in (0, '0', '00'):
        return ("twelve noon",)
    elif the_ampm == '':
        return (hours_lst[int(the_hr)] + '?', minutes_lst[int(the_min)])
    else:
        return (hours_lst[int(the_hr)] + '?', minutes_lst[int(the_min)], the_ampm + '.')
