# -*- coding: utf-8 -*-
"""Executable to regenerate the audio cache for text-to-speech.

Created on Aug 19, 2024

@author: Tom Blackshaw

This code takes the list of acceptable names (Charlie, Liam, etc.) – names of
voices available from ElevenLabs, under the user's current subscription - and
generates audio for each of the common phrases. These phrases include greetings,
apologies, hours, minutes, days, etc.

The audio files are saved in ./sounds/cache/{voice name}/

Todo:
    * For module TODOs
    * You have to also use ``sphinx.ext.todo`` extension

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

from my.consts import hello_owner_lst, alarm_messages_lst, hours_lst, minutes_lst, postsnooze_alrm_msgs_lst, \
                                    farting_msgs_lst, OWNER_NAME
from my.text2speech import smart_phrase_audio, deliberately_cache_a_smart_phrase, look_for_dupes, smart_phrase_filenames

from os import listdir
from os.path import isfile, join
from my.tools.sound.trim import trim_my_audio
import os
from my.text2speech import Text2SpeechSingleton as tts
from my.globals import SOUNDS_CACHE_PATH, SOUNDS_ALARMS_PATH, SOUNDS_FARTS_PATH
from my.tools.sound import convert_one_mp3_to_ogg_file, mp3_to_ogg_conversions, mp3_to_ogg_voice_conversions
from pydub.exceptions import CouldntDecodeError
import sys

def cache_this_smart_phrase(voice:str, smart_phrase:str):
    """With this voice, generate the audio for speaking this phrase.

    Args:
        param1 (int): The first parameter.
        param2 (str): The second parameter.

    Returns:
        bool: The return value. True for success, False otherwise.

    .. _PEP 484:
        https://www.python.org/dev/peps/pep-0484/

    """
    look_for_dupes()
    deliberately_cache_a_smart_phrase(voice, smart_phrase)
    for suffix in ('mp3', 'ogg'):
        look_for_dupes()
        try:
            _ = smart_phrase_audio(voice, smart_phrase, suffix)
        except CouldntDecodeError as e:
            raise CouldntDecodeError("Unable to cache the %s of >>>%s<<<" % (suffix, smart_phrase)) from e
        look_for_dupes()


def cache_this_list_of_smart_phrases_for_voice(voice:str, lst, minimum_len_for_punc=2, maximum_len_for_punc=20):
    pronounceable_punctuation = '?!,.'
    for smart_phrase in lst:
        assert('{owner}' not in smart_phrase)
        assert(not smart_phrase.endswith(' '))
        cache_this_smart_phrase(voice, smart_phrase)
        if len(smart_phrase) == 0:
            print("IGNORING >><< because it's empty")
            continue
        elif len(smart_phrase) >= minimum_len_for_punc and len(smart_phrase) < maximum_len_for_punc:
            # I'll not do all the punctuation: why bother? It's a LOOONNNNGGG sentence.
            cache_this_smart_phrase(voice, smart_phrase)
        else:
            if smart_phrase[-1] in pronounceable_punctuation:
                smart_phrase = smart_phrase[:-1]
            cache_this_smart_phrase(voice, smart_phrase)
            for extra_char in  pronounceable_punctuation:
                cache_this_smart_phrase(voice, smart_phrase + extra_char)


def cache_phrases_for_voice(voice:str):
    cache_this_smart_phrase(voice, OWNER_NAME)
    cache_this_list_of_smart_phrases_for_voice(voice, hello_owner_lst)
    cache_this_list_of_smart_phrases_for_voice(voice, ["Good morning, %s" % OWNER_NAME,
                                                       "Good afternoon, %s" % OWNER_NAME,
                                                       "Good evening, %s" % OWNER_NAME,
                                                       "Hello %s" % OWNER_NAME,
                                                       "Hello, %s" % OWNER_NAME,
                                                       "Hi %s" % OWNER_NAME,
                                                       "Hi, %s" % OWNER_NAME,
                                                       "Hey %s" % OWNER_NAME,
                                                       "Hey, %s" % OWNER_NAME,
                                                       "Greetings %s" % OWNER_NAME
                                                       ])
    cache_this_list_of_smart_phrases_for_voice(voice, ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    cache_this_list_of_smart_phrases_for_voice(voice, ["o'clock", "A.M.", "P.M.",
                                                       "twelve newn",
                                                       "twelve newn", "twelve midnight",
                                                       "12 newn", "12 midnight",
                                                       "time", 'date',
                                                       "morning", "afternoon", "evening",
                                                       "good morning", "good afternoon", "good evening",
                                                       "midnight", "hours", "in the afternoon", "in the morning",
                                                       "in the evening",])
    cache_this_list_of_smart_phrases_for_voice(voice, postsnooze_alrm_msgs_lst)
    cache_this_list_of_smart_phrases_for_voice(voice, alarm_messages_lst)
    cache_this_list_of_smart_phrases_for_voice(voice, hours_lst)
    cache_this_list_of_smart_phrases_for_voice(voice, minutes_lst)
    cache_this_list_of_smart_phrases_for_voice(voice, farting_msgs_lst)




if __name__ == '__main__':
    mp3_to_ogg_conversions(SOUNDS_ALARMS_PATH)
    mp3_to_ogg_conversions(SOUNDS_FARTS_PATH)
    the_voices_i_care_about = tts.all_voices if len(sys.argv) == 1 else (sys.argv[1],)
    for this_voice in the_voices_i_care_about:
        print("Working on", this_voice)
        cache_phrases_for_voice(this_voice) # ...which generates mp3 and ogg files

