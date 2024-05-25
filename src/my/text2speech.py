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
        >>> for i in range(0,10): tts.name = tts.random_name; audiodata = tts.audio(s); tts.play(audiodata)

Section breaks are created by resuming unindented text. Section breaks
are also implicitly created anytime a new section starts.

Attributes:
    Text2SpeechSingleton (_Text2SpeechClass): The singleton

.. _Style Guide:
   https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

"""

import os
import random

from my.classes.exceptions import NoProfessionalVoicesError
from my.classes.text2speechclass import _Text2SpeechClass
from my.stringutils import generate_random_alarm_message

Text2SpeechSingleton = _Text2SpeechClass()


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


def speak_random_alarm(owner_of_clock, time_24h, time_minutes, voice=None, tts=Text2SpeechSingleton):
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
    if voice is None:
        voice = tts.random_name
    message = generate_random_alarm_message(owner_of_clock, time_24h, time_minutes, voice)
    prof_name = get_first_prof_name(tts)  # [r for r in tts.api_voices if r.samples is not None][0].name
    if voice == prof_name:
        d = tts.audio(voice=voice, text=message, advanced=True, model='eleven_multilingual_v2', stability=0.30, similarity_boost=0.01, style=0.90, use_speaker_boost=True)
    else:
        d = tts.audio(voice=voice, text=message)
    tts.play(d)


def speak_totally_randomized_alarm_and_time(owner_of_clock):
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
        >>> from my.text2speech import play_dialogue_lst
        >>> play_dialogue_lst(Text2SpeechSingleton, [('Jessie', 'Knock, knock'),('Freya', 'Get a warrant.')])

    Returns:
        n/a

    Raises:
        unknown. FIXME: list the potential exceptions

    """
    from elevenlabs import play
    data_to_play = []
    from my.tools import logit
    for (name, text) in dialogue_lst:
        logit("{name}: {text}".format(name=name, text=text))
        tts.voice = name
        data_to_play.append(tts.audio(text))
    for d in data_to_play:
        play(d)
