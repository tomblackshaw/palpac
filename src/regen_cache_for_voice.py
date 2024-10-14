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
from my.text2speech import smart_phrase_audio, deliberately_cache_a_smart_phrase

from os import listdir
from os.path import isfile, join
from my.tools.sound.trim import trim_my_audio
from pydub.audio_segment import AudioSegment
from pydub.exceptions import CouldntDecodeError
import os

def cache_this_smart_phrase(voice:str, smart_phrase:str, add_punctuation:bool=True):
    """With this voice, generate the audio for speaking this phrase.

    
    
    Args:
        param1 (int): The first parameter.
        param2 (str): The second parameter.

    Returns:
        bool: The return value. True for success, False otherwise.

    .. _PEP 484:
        https://www.python.org/dev/peps/pep-0484/

    """
    deliberately_cache_a_smart_phrase(voice, smart_phrase)
    if add_punctuation:
        for x in ('.', ',', '?', '!'):
            if len(smart_phrase) > 0 and smart_phrase[-1] not in ('.,?!'):
                y = smart_phrase + x
                deliberately_cache_a_smart_phrase(voice, y)
                _ = smart_phrase_audio(voice, y)
    _ = smart_phrase_audio(voice, smart_phrase)


def cache_this_list_of_smart_phrases_for_voice(voice:str, lst, add_punctuation=True):
    for smart_phrase in lst:
        assert('{owner}' not in smart_phrase)
        cache_this_smart_phrase(voice, smart_phrase, add_punctuation=add_punctuation)


def cache_phrases_for_voice(voice:str):
    cache_this_smart_phrase(voice, OWNER_NAME)
    cache_this_list_of_smart_phrases_for_voice(voice, hours_lst)
    cache_this_list_of_smart_phrases_for_voice(voice, minutes_lst, add_punctuation=False)
    cache_this_list_of_smart_phrases_for_voice(voice, hello_owner_lst)
    cache_this_list_of_smart_phrases_for_voice(voice, postsnooze_alrm_msgs_lst)
    cache_this_list_of_smart_phrases_for_voice(voice, alarm_messages_lst)
    cache_this_list_of_smart_phrases_for_voice(voice, farting_msgs_lst)
    cache_this_list_of_smart_phrases_for_voice(voice, ["Good morning, %s" % OWNER_NAME,
                                                       "Good afternoon, %s" % OWNER_NAME,
                                                       "Good evening, %s" % OWNER_NAME,
                                                       "Hello %s" % OWNER_NAME,
                                                       "Hi %s" % OWNER_NAME,
                                                       "Greetings %s" % OWNER_NAME
                                                       ])
    cache_this_list_of_smart_phrases_for_voice(voice, ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    cache_this_list_of_smart_phrases_for_voice(voice, ["?", "!", "o'clock", "A.M.", "P.M.",
                                                       "twelve newn",
                                                       "twelve newn", "twelve midnight",
                                                       "12 new", "12 newn", "12 midnight",
                                                       "time", '',
                                                       "morning", "afternoon", "evening",
                                                       "good morning", "good afternoon", "good evening",
                                                       "midnight", "hours", "in the afternoon", "in the morning",
                                                       "in the evening",])



def convert_one_mp3_to_ogg_file(mp3fname, oggfname):
    untrimmed_audio = AudioSegment.from_mp3(mp3fname)
    trimmed_aud = trim_my_audio(untrimmed_audio, trim_level=1)
    trimmed_aud.export(oggfname, format="ogg")


def mp3_to_ogg_conversions(path):
    errors = 0
    mp3files = [f for f in listdir(path) if isfile(join(path, f)) and f.endswith('.mp3')]
    for f in mp3files:
        mp3fname = '%s/%s' % (path, f)
        oggfname = mp3fname.replace('.mp3', '.ogg')
        if not os.path.exists(oggfname):
            try:
                convert_one_mp3_to_ogg_file(mp3fname, oggfname)
            except CouldntDecodeError:
                print("WARNING - could not decode %s; so, I'll delete it." % mp3fname)
                os.unlink(mp3fname)
                errors = errors + 1
    return errors


def mp3_to_ogg_voice_conversions(voice:str):
    path = 'sounds/cache/%s' % voice
    mp3_to_ogg_conversions(path)


if __name__ == '__main__':
    from my.text2speech import Text2SpeechSingleton as tts
    mp3_to_ogg_conversions('sounds/alarms')
    mp3_to_ogg_conversions('sounds/farts')
    for this_voice in tts.all_voices:
        print("Working on", this_voice)
        cache_phrases_for_voice(this_voice)
        mp3_to_ogg_voice_conversions(this_voice)

