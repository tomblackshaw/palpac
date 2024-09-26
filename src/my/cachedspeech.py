'''
Created on Sep 25, 2024

@author: mchobbit
'''
import os
from my.stringutils import generate_random_string, generate_random_alarm_message, generate_detokenized_message,\
    pathname_of_phrase_audio
from my.consts import farting_msgs_lst, minutes_lst, hours_lst
import random
from my.text2speech import list_phrases_to_handle, phrase_audio
from my.classes.exceptions import MissingFromCacheError
from my.tools.sound.trim import convert_audio_recordings_list_into_one_audio_recording
from my.globals import MPV_BIN

def speak_a_random_alarm_message(owner, hour, minute, voice, snoozed=False):
    # FIXME WRITE DOX
    rndstr = generate_random_string(32)
    flat_filename = '/tmp/tts{rndstr}.flat.mp3'.format(rndstr=rndstr)
    my_txt = generate_random_alarm_message(owner_of_clock=owner, time_24h=hour, time_minutes=minute, snoozed=snoozed)
    data = smart_phrase_audio(voice, my_txt)
    data.export(flat_filename, format="mp3")
    os.system("{mpv} {fnam}".format(mpv=MPV_BIN, fnam=flat_filename))
    os.unlink(flat_filename)


def just_fart(fart_vol:int=100):
    from os import listdir
    from os.path import isfile, join
    path = 'sounds/farts'
    fartfiles = [f for f in listdir(path) if isfile(join(path, f))]
    fart_mp3file = '{path}/{chx}'.format(path=path, chx=random.choice(fartfiles))
    os.system('mpv --volume={vol} {fart}'.format(vol=fart_vol, fart=fart_mp3file))
    
    
def just_apologize(voice:str, voice_vol:int=100):
    data_apologize = smart_phrase_audio(voice, random.choice(farting_msgs_lst))
    apologize_mp3file = '/tmp/tts{rnd}'.format(rnd=generate_random_string(32))
    data_apologize.export(apologize_mp3file, format="mp3")
    os.system('mpv --volume={vol} {playme}'.format(vol=voice_vol, playme=apologize_mp3file))
    os.unlink(apologize_mp3file)


def fart_and_apologize(voice:str, fart_vol:int=75,voice_vol:int=80):
    just_fart(fart_vol)
    just_apologize(voice, voice_vol)

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



def smart_phrase_audio(voice:str, smart_phrase:str, owner:str=None, time_24h:int=None, time_minutes:int=None, trim_level:int=1): # -> AudioSegment:
    # FIXME WRITE DOX
    # FIXME This is a badly written subroutine. Clean it up. Document it. Thank you.
    if owner is not None and time_24h is not None and time_minutes is not None:
        detokenized_phrase = generate_detokenized_message(owner, time_24h, time_minutes, smart_phrase)
        detokenized_phrase = detokenized_phrase.replace('12 newn', '12:00 P.M.').replace('12 midnight', '12:00 A.M.')
    else:
        detokenized_phrase = ''.join(r + ' ' for r in list_phrases_to_handle(smart_phrase)).strip(' ')
    detokenized_phrase = detokenized_phrase.lower()
    data = []
    all_words = [r.lower().strip(' ') for r in detokenized_phrase.split(' ')]
    firstwordno = 0
    while firstwordno < len(all_words):
        lastwordno = len(all_words)
        while lastwordno > firstwordno:
            searchforthis = ''.join([r + ' ' for r in all_words[firstwordno:lastwordno]]).strip()
            if not os.path.exists(pathname_of_phrase_audio(voice, searchforthis)):
                lastwordno -= 1
            elif len(searchforthis) == 0:
                break
            else:
                firstwordno = lastwordno - 1
                data.append(phrase_audio(voice, searchforthis))
                break
        if lastwordno == firstwordno:
            if searchforthis == '':
                print('Ignoring', searchforthis)
            elif ':' in searchforthis and len(searchforthis) >= 4:
                if lastwordno + 1 < len(all_words) and all_words[lastwordno + 1].lower()[:4] in ('a.m.', 'p.m.'):
                    lastwordno += 1
                    searchforthis = ''.join([r + ' ' for r in all_words[firstwordno:lastwordno + 1]]).strip()
                print("TIME <=", searchforthis)
                for s in generate_timedate_phrases_list(searchforthis):
                    outfile = pathname_of_phrase_audio(voice, s)
                    if not os.path.exists(outfile):
                        raise MissingFromCacheError("{voice} => {s} <= {outfile} => (time thingy) is missing from the cache".format(s=s, voice=voice, outfile=outfile))
                    data.append(phrase_audio(voice, s))
                firstwordno = lastwordno
            elif searchforthis in ('?', ':', '!', '.'):
                print("Ignoring", searchforthis)
            else:
                outfile = pathname_of_phrase_audio(voice, searchforthis)
                raise MissingFromCacheError("{voice} => {searchforthis} <= {outfile} => is missing from the cache".format(searchforthis=searchforthis, voice=voice, outfile=outfile))
        firstwordno += 1
    return convert_audio_recordings_list_into_one_audio_recording(data=data, trim_level=trim_level)



