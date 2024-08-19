'''
Created on Aug 19, 2024

@author: Tom Blackshaw

from my.text2speech import smart_phrase_audio, phrase_audio
generate_random_alarm_message(owner_of_clock, time_24h, time_minutes, for_voice=None)

'''

from my.consts import hello_owner_lst, alarm_messages_lst, default_speaker_alarm_message_dct
from my.text2speech import smart_phrase_audio, deliberately_cache_a_phrase


def cache_this_smart_phrase(voice, smart_phrase):
    _ = deliberately_cache_a_phrase(voice, smart_phrase)
    _ = smart_phrase_audio(voice, smart_phrase)


def cache_this_list_of_smart_phrases_for_voice(voice, lst):
    for smart_phrase in lst:
        for i in ('', '.', ',', '?', '!'):
            deliberately_cache_a_phrase(voice, smart_phrase)
            if not smart_phrase.endswith(i):
                deliberately_cache_a_phrase(voice, (smart_phrase + i))


def cache_phrases_for_voice(voice):
    cache_this_list_of_smart_phrases_for_voice(voice, hello_owner_lst)
    cache_this_list_of_smart_phrases_for_voice(voice, alarm_messages_lst)
    cache_this_list_of_smart_phrases_for_voice(voice, ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    cache_this_list_of_smart_phrases_for_voice(voice, [str(r) + "?" for r in range(0, 60)])
    cache_this_list_of_smart_phrases_for_voice(voice, [str(r) + "!" for r in range(0, 60)])
    cache_this_list_of_smart_phrases_for_voice(voice, [str(r) + "," for r in range(0, 60)])
    cache_this_list_of_smart_phrases_for_voice(voice, [str(r) for r in range(0, 60)])
    cache_this_list_of_smart_phrases_for_voice(voice, ["o'clock", "A.M.", "P.M.", "noon",
                                                       "time",
                                                       "morning", "afternoon", "evening",
                                                       "good morning", "good afternoon", "good evening",
                                                       "midnight", "hours", "in the afternoon", "in the morning",
                                                       "in the evening"])
    if voice in default_speaker_alarm_message_dct.keys():
        cache_this_smart_phrase(voice, default_speaker_alarm_message_dct[voice])



if __name__ == '__main__':
    from my.text2speech import Text2SpeechSingleton as tts
    for this_voice in tts.all_voices:
        print("Working on", this_voice)
        cache_phrases_for_voice(this_voice)
        cache_this_list_of_smart_phrases_for_voice(this_voice, ['Charlie', 'Charlie?', 'Charlie!', 'Charlie.'])
