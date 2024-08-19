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
            phrases_to_handle.append( smart_phrase[i:j+1])
            smart_phrase = smart_phrase[j+1:]
    return phrases_to_handle


def decoded_token(token, hello_owner, owner, shorttime, one_minute_ago, one_minute_later, morning_or_afternoon_or_evening):
    newval = token
    for _ in range(0, 5):
        oldval = newval
        ov_template = string.Template(oldval)
        newval = ov_template.substitute(hello_owner=hello_owner, owner=owner, shorttime=shorttime, one_minute_ago=one_minute_ago, one_minute_later=one_minute_later, morning_or_afternoon_or_evening=morning_or_afternoon_or_evening)
    return newval

'''
from my.text2speech import smart_phrase_audio, phrase_audio
from my.classes.text2speechclass import convert_audio_recordings_list_into_one_audio_recording, convert_audio_recordings_list_into_an_mp3_file
voice = 'Hugo'
smart_phrase="Hello ${test} there."
convert_audio_recordings_list_into_an_mp3_file(data, '/tmp/out.mp3')
s = convert_audio_recordings_list_into_one_audio_recording(data)
'''


def deliberately_cache_a_phrase(voice, smart_phrase):
    data = []
    startpos = smart_phrase.find('${')
    if startpos >= 0:
        endpos = smart_phrase.find('}', startpos) + 1
        while endpos < len(smart_phrase) and smart_phrase[endpos] in '?!;:,. ':
            endpos += 1
        s = smart_phrase[:startpos].strip()
        audio_op = phrase_audio(voice, s)
        try:
            _ = convert_audio_recordings_list_into_one_audio_recording([audio_op], trim_level=1)
            data.append(audio_op)
        except CouldntDecodeError:
            print('"%s" (for %s) failed. Ignoring.' % (s, voice))

        startpos = endpos
        return convert_audio_recordings_list_into_one_audio_recording(data, trim_level=1)


def smart_phrase_audio(voice, smart_phrase, owner=None, time_24h=None, time_minutes=None):
    if owner and time_24h and time_minutes:
        detokenized_phrase = generate_detokenized_message(owner, time_24h, time_minutes, smart_phrase)  # Decoder. FIXME. Document!
    else:
        detokenized_phrase = smart_phrase
    data = []
    all_words = [r.lower().strip(' ') for r in detokenized_phrase.split(' ')]
    firstwordno = 0
    while firstwordno < len(all_words):
        lastwordno = len(all_words)
        while lastwordno > firstwordno:
            searchforthis = ''.join([r + ' ' for r in all_words[firstwordno:lastwordno]]).strip()
            while len(searchforthis) > 0 and searchforthis[0] in (';:,.!?'):
                searchforthis = searchforthis[1:]
            if not os.path.exists(pathname_of_phrase_audio(voice, searchforthis)):
                lastwordno -= 1
            else:
                print("FOUND", searchforthis)
                firstwordno = lastwordno - 1
                data.append(phrase_audio(voice, searchforthis))
                break
        if lastwordno == firstwordno:
            if searchforthis == '' or searchforthis.startswith('${'):
                print('Ignoring', searchforthis)
            elif ':' in searchforthis:
                print("TIME <=", searchforthis)
#                data.append(phrase_audio(voice, "fish"))
            else:
                raise MissingFromCacheError("{searchforthis} is missing from the cache".format(searchforthis=searchforthis))
        firstwordno += 1
    return convert_audio_recordings_list_into_one_audio_recording(data, trim_level=1)

