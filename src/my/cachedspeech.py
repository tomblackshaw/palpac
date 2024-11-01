'''
Created on Sep 25, 2024

@author: mchobbit
'''
import os
from my.stringutils import generate_random_string, generate_random_alarm_message, generate_detokenized_message,\
    pathname_of_phrase_audio
from my.consts import farting_msgs_lst, minutes_lst, hours_lst
import random
from my.text2speech import list_phrases_to_handle, phrase_audio, smart_phrase_audio
from my.classes.exceptions import MissingFromCacheError
from my.tools.sound.trim import convert_audio_recordings_list_into_one_audio_recording
from my.tools.sound import play_audiofile
from my.globals import SOUNDS_FARTS_PATH


def speak_a_random_alarm_message(owner, hour, minute, voice, snoozed=False):
    # FIXME WRITE DOX
    rndstr = generate_random_string(32)
    flat_filename = '/tmp/tts{rndstr}.flat.ogg'.format(rndstr=rndstr)
    my_txt = generate_random_alarm_message(owner_of_clock=owner, time_24h=hour, time_minutes=minute, snoozed=snoozed)
    data = smart_phrase_audio(voice=voice, my_txt=my_txt, owner=owner)
    data.export(flat_filename, format="ogg")
    play_audiofile(flat_filename) 
    os.unlink(flat_filename)


def just_fart(fart_vol:int=100):
    from os import listdir
    from os.path import isfile, join
    path = SOUNDS_FARTS_PATH
    fartfiles = [f for f in listdir(path) if isfile(join(path, f))]
    fart_mp3file = '{path}/{chx}'.format(path=path, chx=random.choice(fartfiles))
    os.system('mpv --volume={vol} {fart}'.format(vol=fart_vol, fart=fart_mp3file))
    
    
def just_apologize(voice:str, owner:str, voice_vol:int=100):
    data_apologize = smart_phrase_audio(voice=voice, smart_phrase=random.choice(farting_msgs_lst), owner=owner)
    apologize_mp3file = '/tmp/tts{rnd}'.format(rnd=generate_random_string(32))
    data_apologize.export(apologize_mp3file, format="mp3")
    os.system('mpv --volume={vol} {playme}'.format(vol=voice_vol, playme=apologize_mp3file))
    os.unlink(apologize_mp3file)


def fart_and_apologize(voice:str, owner:str, fart_vol:int=75,voice_vol:int=80):
    just_fart(fart_vol)
    just_apologize(voice, owner, voice_vol)

def generate_timedate_phrases_list(timedate_str:str) -> str:
    # FIXME WRITE DOX
    the_hr, the_min = timedate_str.split(':')
    the_hr = the_hr.strip('.')
    the_min = the_min.strip('.')
    the_ampm = ''
    if ' ' in the_min:
        the_min, the_ampm = the_min.split(' ')
    the_ampm = the_ampm[:4].strip(' . ')
    print('the_hr={the_hr}; the_min={the_min}; the_ampm={the_ampm}'.format(the_hr=the_hr, the_min=the_min, the_ampm=the_ampm))
    if the_hr in (0, '0') and the_min in (0, '0', '00'):
        return ("twelve midnight",)
    elif the_hr in (12, '12') and the_min in (0, '0', '00'):
        return ("twelve newn",)  # UGH! Necessary, because ElevenLabs can't pronounce 'noon' properly.
    elif the_ampm == '':
        return (hours_lst[int(the_hr)] + '?', minutes_lst[int(the_min)])
    else:
        return (hours_lst[int(the_hr)] + '?', minutes_lst[int(the_min)], the_ampm + '.')




