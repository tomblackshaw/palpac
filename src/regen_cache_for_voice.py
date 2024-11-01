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
from my.text2speech import smart_phrase_audio, deliberately_cache_a_smart_phrase, look_for_dupes

from my.text2speech import Text2SpeechSingleton as tts
from my.globals import SOUNDS_ALARMS_PATH, SOUNDS_FARTS_PATH
from my.tools.sound import mp3_to_ogg_conversions
import sys

def cache_this_smart_phrase(voice:str, smart_phrase:str, owner:str):
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
    deliberately_cache_a_smart_phrase(voice, smart_phrase.replace('${owner}', owner))
    for suffix in ('mp3', 'ogg'):
        look_for_dupes()
#        try:
        _ = smart_phrase_audio(voice=voice, smart_phrase=smart_phrase, owner=owner, suffix=suffix)
        # except CouldntDecodeError as e:
        #     raise CouldntDecodeError("Unable to cache the %s of >>>%s<<<" % (suffix, smart_phrase)) from e
        look_for_dupes()


def cache_this_list_of_smart_phrases_for_voice(voice:str, lst, owner, minimum_len_for_punc=2, maximum_len_for_punc=20):
    pronounceable_punctuation = '?!,.'
    for smart_phrase in lst:
        assert(not smart_phrase.endswith(' '))
        cache_this_smart_phrase(voice=voice, smart_phrase=smart_phrase.replace('${owner}', owner), owner=owner)
        if len(smart_phrase) == 0:
            print("IGNORING >><< because it's empty")
            continue
        elif len(smart_phrase) >= minimum_len_for_punc and len(smart_phrase) < maximum_len_for_punc:
            # I'll not do all the punctuation: why bother? It's a LOOONNNNGGG sentence.
            cache_this_smart_phrase(voice, smart_phrase, owner)
        else:
            if smart_phrase[-1] in pronounceable_punctuation:
                smart_phrase = smart_phrase[:-1]
            cache_this_smart_phrase(voice, smart_phrase, owner)
            for extra_char in  pronounceable_punctuation:
                cache_this_smart_phrase(voice, smart_phrase + extra_char, owner)


def cache_phrases_for_voice(voice:str, owner:str):
    cache_this_smart_phrase(voice=voice, smart_phrase=owner, owner=owner)
    cache_this_smart_phrase(voice=voice, smart_phrase=owner + ',', owner=owner)
    cache_this_smart_phrase(voice=voice, smart_phrase=owner + '.', owner=owner)
    cache_this_smart_phrase(voice=voice, smart_phrase=owner + '?', owner=owner)
    cache_this_smart_phrase(voice=voice, smart_phrase=owner + '!', owner=owner)
    cache_this_list_of_smart_phrases_for_voice(voice, hello_owner_lst, owner)
    cache_this_list_of_smart_phrases_for_voice(voice, ["Good morning, %s" % owner,
                                                       "Good afternoon, %s" % owner,
                                                       "Good evening, %s" % owner,
                                                       "Good morning",
                                                       "Good afternoon",
                                                       "Good evening",
                                                       "Good morning!",
                                                       "Good afternoon!",
                                                       "Good evening!",
                                                       "Good morning.",
                                                       "Good afternoon.",
                                                       "Good evening.",
                                                       "Hello %s" % owner,
                                                       "Hello, %s" % owner,
                                                       "Hi %s" % owner,
                                                       "Hi, %s" % owner,
                                                       "Hey %s" % owner,
                                                       "Hey, %s" % owner,
                                                       "Greetings %s" % owner
                                                       ], owner)
    cache_this_list_of_smart_phrases_for_voice(voice, ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], owner=owner)
    cache_this_list_of_smart_phrases_for_voice(voice, ["o'clock", "A.M.", "P.M.",
                                                       "twelve newn",
                                                       "twelve newn", "twelve midnight",
                                                       "12 newn", "12 midnight",
                                                       "time", 'date',
                                                       "morning", "afternoon", "evening",
                                                       "good morning", "good afternoon", "good evening",
                                                       "midnight", "hours", "in the afternoon", "in the morning",
                                                       "in the evening",], owner=owner)
    cache_this_list_of_smart_phrases_for_voice(voice, postsnooze_alrm_msgs_lst, owner=owner)
    cache_this_list_of_smart_phrases_for_voice(voice, alarm_messages_lst, owner=owner)
    cache_this_list_of_smart_phrases_for_voice(voice, hours_lst, owner=owner)
    cache_this_list_of_smart_phrases_for_voice(voice, minutes_lst, owner=owner)
    cache_this_list_of_smart_phrases_for_voice(voice, farting_msgs_lst, owner=owner)




if __name__ == '__main__':
    mp3_to_ogg_conversions(SOUNDS_ALARMS_PATH)
    mp3_to_ogg_conversions(SOUNDS_FARTS_PATH)
    the_voices_i_care_about = tts.all_voices if len(sys.argv) == 1 else (sys.argv[1],)
    cache_this_smart_phrase('Aria', 'Charlie.', 'Charlie')
    for this_voice in the_voices_i_care_about:
        print("Working on", this_voice)
        cache_phrases_for_voice(this_voice, OWNER_NAME) # ...which generates mp3 and ogg files

