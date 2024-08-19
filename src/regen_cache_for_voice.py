'''
Created on Aug 19, 2024

@author: Tom Blackshaw
'''


from  my.consts import hello_owner_lst, alarm_messages_lst, default_speaker_alarm_message_dct
from my.text2speech import phrase_audio


def cache_this_smart_phrase(voice, smart_phrase):
    startpos = smart_phrase.find('${')
    if startpos >= 0:
        endpos = smart_phrase.find('}', startpos)+1
        while endpos < len(smart_phrase) and smart_phrase[endpos] in '?!;:,. ':
            endpos += 1
        cache_this_smart_phrase(voice, smart_phrase[:startpos])
        cache_this_smart_phrase(voice, smart_phrase[endpos:])
    elif smart_phrase == '':
        pass
    else:
        _ = phrase_audio(voice, smart_phrase)


def cache_this_list_of_smart_phrases_for_voice(voice, lst):
    for smart_phrase in lst:
        cache_this_smart_phrase(voice, smart_phrase)

def cache_phrases_for_voice(voice):
    cache_this_list_of_smart_phrases_for_voice(voice, hello_owner_lst)
    cache_this_list_of_smart_phrases_for_voice(voice, alarm_messages_lst)
    cache_this_list_of_smart_phrases_for_voice(voice, ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    cache_this_list_of_smart_phrases_for_voice(voice, [str(r) + "?" for r in range(0, 60)])
    cache_this_list_of_smart_phrases_for_voice(voice, [str(r) + "!" for r in range(0, 60)])
    cache_this_list_of_smart_phrases_for_voice(voice, [str(r) + "," for r in range(0, 60)])
    cache_this_list_of_smart_phrases_for_voice(voice, [str(r) for r in range(0, 60)])
    cache_this_list_of_smart_phrases_for_voice(voice, ["o'clock", "A.M.", "P.M.", "noon",
                                                       "morning", "afternoon", "evening",
                                                       "midnight", "hours", "in the afternoon", "in the morning",
                                                       "in the evening"])
    if voice in default_speaker_alarm_message_dct.keys():
        cache_this_smart_phrase(voice, default_speaker_alarm_message_dct[voice])



if __name__ == '__main__':
    from my.text2speech import Text2SpeechSingleton as tts
    for this_voice in tts.all_voices:
        cache_phrases_for_voice(this_voice)
