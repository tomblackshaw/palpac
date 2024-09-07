'''
Created on Aug 19, 2024

@author: Tom Blackshaw

from my.text2speech import smart_phrase_audio, phrase_audio
generate_random_alarm_message(owner_of_clock, time_24h, time_minutes)

import os
from my.stringutils import *
from my.text2speech import *
import random
from my.classes.text2speechclass import *
from my.text2speech import Text2SpeechSingleton as tts
owner = 'Charlie'
voice = 'Sarah'
time_24h = 12
time_minutes = 0
smart_phrase = random.choice(alarm_messages_lst)
os.system('rm -f /tmp/out.mp3')
data = smart_phrase_audio(voice, smart_phrase, owner='Charlie', time_24h=time_24h, time_minutes=time_minutes); file_handle = data.export("/tmp/out.mp3", format="mp3")
file_handle = data.export("/tmp/out.mp3", format="mp3")
os.system("mpv /tmp/out.mp3")

for voice in ('Sarah',): # tts.all_voices:
    for smart_phrase in alarm_messages_lst:
        time_24h=random.randint(0,24)
        time_minutes=random.randint(0,60)
        os.system('rm -f /tmp/out.mp3')
        data = smart_phrase_audio(voice, smart_phrase, owner='Charlie', time_24h=time_24h, time_minutes=time_minutes); file_handle = data.export("/tmp/out.mp3", format="mp3")
        file_handle = data.export("/tmp/out.mp3", format="mp3")
        os.system("mpv /tmp/out.mp3")


from my.text2speech import Text2SpeechSingleton as tts
tts.voice = voice
message = generate_detokenized_message(owner, time_24h, time_minutes, smart_phrase)
tts.say('09')

'''

from my.consts import hello_owner_lst, alarm_messages_lst, hours_lst, minutes_lst, postsnooze_alrm_msgs_lst
from my.text2speech import smart_phrase_audio, deliberately_cache_a_smart_phrase


def cache_this_smart_phrase(voice, smart_phrase, add_punctuation=True):
    deliberately_cache_a_smart_phrase(voice, smart_phrase)
    if add_punctuation:
        for x in ('.', ',', '?', '!'):
            if len(smart_phrase) > 0 and smart_phrase[-1] not in ('.,?!'):
                y = smart_phrase + x
                deliberately_cache_a_smart_phrase(voice, y)
                _ = smart_phrase_audio(voice, y)
    _ = smart_phrase_audio(voice, smart_phrase)


def cache_this_list_of_smart_phrases_for_voice(voice, lst, add_punctuation=True):
    for smart_phrase in lst:
        cache_this_smart_phrase(voice, smart_phrase, add_punctuation=add_punctuation)


def cache_phrases_for_voice(voice):
    cache_this_list_of_smart_phrases_for_voice(voice, hours_lst)
    cache_this_list_of_smart_phrases_for_voice(voice, minutes_lst, add_punctuation=False)
    cache_this_list_of_smart_phrases_for_voice(voice, hello_owner_lst)
    cache_this_list_of_smart_phrases_for_voice(voice, postsnooze_alrm_msgs_lst)
    cache_this_list_of_smart_phrases_for_voice(voice, alarm_messages_lst)
    cache_this_list_of_smart_phrases_for_voice(voice, ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
#    cache_this_list_of_smart_phrases_for_voice(voice, [str(r) + " P.M." for r in range(1, 13)])
#    cache_this_list_of_smart_phrases_for_voice(voice, [str(r) + " A.M." for r in range(1, 13)])
#    cache_this_list_of_smart_phrases_for_voice(voice, [str(r) for r in range(0, 60)])
    cache_this_list_of_smart_phrases_for_voice(voice, ["?", "!", "o'clock", "A.M.", "P.M.",
                                                       "twelve newn",
                                                       "twelve newn", "twelve midnight",
                                                       "12 new", "12 newn", "12 midnight",
                                                       "time", '',
                                                       "morning", "afternoon", "evening",
                                                       "good morning", "good afternoon", "good evening",
                                                       "midnight", "hours", "in the afternoon", "in the morning",
                                                       "in the evening"])

if __name__ == '__main__':
    potential_owner_names = ["Charlie", "Chief", "Dumbass", "Charles", "Killer"]
    from my.text2speech import Text2SpeechSingleton as tts
    for this_voice in tts.all_voices:
        print("Working on", this_voice)
        cache_phrases_for_voice(this_voice)
        cache_this_list_of_smart_phrases_for_voice(this_voice, potential_owner_names)
