# -*- coding: utf-8 -*-
"""Executable to regenerate the audio cache for text-to-speech.

Created on Aug 19, 2024
Updated on Nov 05, 2024

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

from my.consts import OWNER_NAME, alarm_messages_lst, postsnooze_alrm_msgs_lst, hours_lst, minutes_lst, hello_owner_lst, \
    wannasnooze_msgs_lst, farting_msgs_lst, motivational_comments_lst
from my.text2speech import smart_phrase_audio, deliberately_cache_a_smart_sentence, \
                    look_for_dupes, smart_phrase_filenames, speak_a_random_motivational_comment
from my.text2speech import Text2SpeechSingleton as tts
from my.globals import SOUNDS_ALARMS_PATH, SOUNDS_FARTS_PATH
from my.tools.sound import mp3_to_ogg_conversions
import sys
from my.stringutils import generate_detokenized_message
import random


def cache_and_check_smart_sentence(voice:str, smart_phrase:str, owner:str):
    """With this voice, generate the audio for speaking this phrase.

    Args:
        voice (str): The name of the voice to be speaking.
        smart_phrase (str): The smart phrase to be cached.

    Returns:
        bool: The return value. True for success, False otherwise.

    .. _PEP 484:
        https://www.python.org/dev/peps/pep-0484/

    """
    look_for_dupes()
    deliberately_cache_a_smart_sentence(voice, smart_phrase.replace('${owner}', owner))
    for suffix in ('mp3', 'ogg'):
        look_for_dupes()
#        try:
        _ = smart_phrase_audio(voice=voice, smart_phrase=smart_phrase, owner=owner, suffix=suffix)
        # except CouldntDecodeError as e:
        #     raise CouldntDecodeError("Unable to cache the %s of >>>%s<<<" % (suffix, smart_phrase)) from e
        look_for_dupes()


def cache_and_check_list_of_smart_sentences(voice:str, lst, owner:str, do_punctuation=True):
    pronounceable_punctuation = '?!,.'
    for smart_phrase in lst:
        assert(not smart_phrase.endswith(' '))
        if len(smart_phrase) == 0:
            print("IGNORING >><< because it's empty")
        else:
            smart_phrase = smart_phrase.replace('${owner}', owner)
            if not do_punctuation:
                cache_and_check_smart_sentence(voice=voice, smart_phrase=smart_phrase, owner=owner)
            else:
                if smart_phrase[-1] in pronounceable_punctuation and not smart_phrase.endswith('.m.'):
                    smart_phrase = smart_phrase[:-1]
                cache_and_check_smart_sentence(voice, smart_phrase, owner)
                for extra_char in pronounceable_punctuation:
                    cache_and_check_smart_sentence(voice, smart_phrase=smart_phrase + extra_char, owner=owner)


def cache_phrases_for_voice(voice:str, owner:str):
    # Cache the most common "HELLO OWNER" messages
    for time_24h in (0, 4, 8, 12, 16, 20):
        cache_and_check_list_of_smart_sentences(voice=voice, owner=owner, lst=[
             generate_detokenized_message(owner=owner, time_24h=time_24h, time_minutes=0, message_template=m) for m in hello_owner_lst
             ])
    cache_and_check_smart_sentence(voice=voice, smart_phrase=owner, owner=owner)
    cache_and_check_list_of_smart_sentences(voice, hello_owner_lst, owner, do_punctuation=False)
    cache_and_check_list_of_smart_sentences(voice, ["Good morning, %s" % owner,
                                                       "Good afternoon, %s" % owner,
                                                       "Good evening, %s" % owner,
                                                       ], owner)
    cache_and_check_list_of_smart_sentences(voice, ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], owner=owner)
    cache_and_check_list_of_smart_sentences(voice, ["o'clock", "A.M.", "P.M.",
                                                       "twelve newn",
                                                       "twelve newn", "twelve midnight",
                                                       "12 newn", "12 midnight",
                                                       "time", 'date',
                                                       "morning", "afternoon", "evening",
                                                       "good morning", "good afternoon", "good evening",
                                                       "midnight", "hours", "minutes", "in the afternoon", "in the morning",
                                                       "in the evening", ], owner=owner)
    cache_and_check_list_of_smart_sentences(voice, postsnooze_alrm_msgs_lst, owner=owner, do_punctuation=False)
    cache_and_check_list_of_smart_sentences(voice, alarm_messages_lst, owner=owner, do_punctuation=False)
    cache_and_check_list_of_smart_sentences(voice, hours_lst, owner=owner)
    cache_and_check_list_of_smart_sentences(voice, minutes_lst, owner=owner)
    cache_and_check_list_of_smart_sentences(voice, farting_msgs_lst, owner, do_punctuation=False)

# def do_stuff(q):
#     while True:
#         cache_phrases_for_voice(q.get(), OWNER_NAME)
#         q.task_done()


if __name__ == '__main__':
    mp3_to_ogg_conversions(SOUNDS_ALARMS_PATH)
    mp3_to_ogg_conversions(SOUNDS_FARTS_PATH)
    the_voices_i_care_about = (sys.argv[1],) if len(sys.argv) > 1 else tts.all_voices  # [:20]
    for my_voice in the_voices_i_care_about:
        print("Working on", my_voice)
        if my_voice == 'Brian':
            print("Nope. Brian sucks.")
            continue
        cache_and_check_list_of_smart_sentences(voice=my_voice, owner=OWNER_NAME, lst=motivational_comments_lst, do_punctuation=False)
        cache_and_check_list_of_smart_sentences(voice=my_voice, owner=OWNER_NAME, lst=farting_msgs_lst, do_punctuation=False)
        cache_and_check_list_of_smart_sentences(voice=my_voice, owner=OWNER_NAME, lst=wannasnooze_msgs_lst, do_punctuation=False)
        cache_phrases_for_voice(my_voice, OWNER_NAME)  # ...which generates mp3 and ogg files
    sys.exit(0)
    # q = Queue(maxsize=0)
    # workers = []
    # num_threads = 8
    # for i in range(num_threads):
    #     worker = Thread(target=do_stuff, args=(q,))
    #     worker.setDaemon(True)
    #     worker.start()
    # for this_voice in tts.all_voices:
    #     q.put(this_voice)
    # q.join()

