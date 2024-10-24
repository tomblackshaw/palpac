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
        >>> for i in range(0,10): tts.name = tts.random_voice; audiodata = tts.audio(s); tts.play(audiodata)

Section breaks are created by resuming unindented text. Section breaks
are also implicitly created anytime a new section starts.

Attributes:
    Text2SpeechSingleton (_Text2SpeechClass): The singleton

.. _Style Guide:
   https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html


"""

import os
import random
import string
import sys
from random import choice
from os import listdir
from os.path import isfile, join

from pydub.exceptions import CouldntDecodeError

from my.classes.exceptions import NoProfessionalVoicesError, MissingFromCacheError
from my.consts import hours_lst, minutes_lst, Cmaj, farting_msgs_lst
from my.stringutils import generate_random_alarm_message, generate_detokenized_message, pathname_of_phrase_audio, generate_random_string,\
    OLD_pathname_of_phrase_audio
from my.tools.sound.sing import songify_this_mp3
from my.tools.sound.trim import convert_audio_recordings_list_into_one_audio_recording,\
    convert_audio_recordings_list_into_an_mp3_file
from pydub.audio_segment import AudioSegment
from my.globals import ELEVENLABS_KEY_FILENAME, SOUNDS_FARTS_PATH 
import time
from my.tools.sound import play_audiofile, queue_oggfile, convert_one_mp3_to_ogg_file
import pygame
from shutil import copyfile

if not os.path.exists(ELEVENLABS_KEY_FILENAME) or 0 != os.system("ping -c2 -W5 www.elevenlabs.io"):
    Text2SpeechSingleton = None
    print("""We cannot use ElevenLabs. Either we're offline or there's no API key. Sorry.
Let's just hope you're using the cache & not trying to call ElevenLabs...""")
else:
    try:
        from my.classes.text2speechclass import _Text2SpeechClass
        Text2SpeechSingleton = _Text2SpeechClass()
    except (ModuleNotFoundError, ImportError) as my_e:
        if 'circular' in str(my_e):
            raise my_e
        Text2SpeechSingleton = None  # compatibility w/ Python 3.8


def get_first_prof_name(tts:Text2SpeechSingleton) -> str:
    """Get the name of the first professional-grade voice.

    On the programmer's Eleven Labs account, there may be a professional-
    grade voice available (or there may not). If there is one, return its
    name. If there are two or more, return the name of the first one. If
    there are none, raise a NoProfessionalVoicesError exception.

    Args:
        tts: The singleton by which to access
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


def speak_random_alarm(owner_name:str, time_24h:int, time_minutes:int, voice:str=None, tts=Text2SpeechSingleton):
    """Speak an alarm warning.

    In the specified voice, to the specified owner of the alarm clock, speak an alarm
    to alert the alarm clock user that a specific time has come.

    Args:
        owner_name: First name of the owner of the alarm clock.
        time_24h: The time that has come (hours).
        time_minutes: The time that has come (minutes).
        voice: The name of the voice that I am to use.

    """
    if voice is None:
        voice = tts.random_voice
    message = generate_random_alarm_message(owner_name, time_24h, time_minutes, voice)
    prof_name = get_first_prof_name(tts)  # [r for r in tts.api_voices if r.samples is not None][0].name
    if voice == prof_name:
        d = tts.audio(text=message, advanced=True, model='eleven_multilingual_v2', stability=0.30, similarity_boost=0.01, style=0.90, use_speaker_boost=True)
    else:
        d = tts.audio(text=message)
    tts.play(d)


def speak_totally_randomized_alarm_and_time(owner_of_clock:str):
    """It does what it says on the tin."""
    time_24h = random.randint(0, 24)
    time_minutes = random.randint(0, 60)
    speak_random_alarm(owner_of_clock, time_24h, time_minutes)


def play_dialogue_lst(tts, dialogue_lst:list):  # , stability=0.5, similarity_boost=0.01, style=0.5):
    """Recites dialogue.

    Using the Eleven Labs website's API, their Python module, and mpv/ffmpeg, I play
    the supplied dialogue list. 'Do' the named voices, too. FYI, the API's key is
    stored at $ELEVENLABS_KEY_FILENAME .

    Args:
        tts: Text-to-speech singleton Text2SpeechSingleton.
        dialogue_lst: List of dialogue tuples. The first item is the name of the voice
            to be used. The second item is the text to be recited.

    Example:
        $ python3
        >>> from my.text2speech import play_dialogue_lst, Text2SpeechSingleton as tts
        >>> play_dialogue_lst(tts, [('Jessie', 'Knock, knock'),('Freya', 'Get a warrant.')])

    Returns:
        n/a

    Raises:
        On its own? None. However, tts may raise various exceptions.

    """
    data_to_play = []
    from my.tools import logit
    for (name, text) in dialogue_lst:
        logit("{name}: {text}".format(name=name, text=text))
        tts.voice = name
        data_to_play.append(tts.audio(text))
    tts.play(data_to_play)



def phrase_audio(voice:str, text:str, suffix='mp3', raise_exception_if_not_cached:bool=False) -> bytes:
    # FIXME WRITE DOX
    outfile = pathname_of_phrase_audio(voice, text, suffix=suffix)
    text = text.lower().strip(' ')
    if len(text) > 1:
    # if text not in ('!', '?', '.', ','):
        while len(text) > 0 and text[0] in ' !?;:.,':
            text = text[1:]
    if not os.path.exists(outfile):
        if raise_exception_if_not_cached:
            raise MissingFromCacheError("'{text}' (for {voice}) should have been cached not hasn't been.".format(text=text, voice=voice))
        print(voice, '==>', text)
        print("Generating speech audio (spoken by {voice}) for '{text}'".format(voice=voice, text=text))
        os.system('mkdir -p "{mydir}"'.format(mydir=os.path.dirname(outfile)))
        vers = sys.version_info
        major_ver, minor_ver = vers[:2]
        if major_ver < 3 or minor_ver < 11:  # Some versions of Python can't handle Eleven Labs. Therefore, we call the bash script, will calls the correct version. Or something.
            os.system('''./_cachespeech.sh "{voice}" "{text}" "{outfile}"'''.format(voice=voice, text=text, outfile=outfile))
        else:
            with open(outfile[:-4] + '.mp3', 'wb') as f:
                print("Writing >%s<" % outfile[:-4] + '.mp3')
                old_v = Text2SpeechSingleton.voice
                Text2SpeechSingleton.voice = voice
                f.write(Text2SpeechSingleton.audio(text))
                Text2SpeechSingleton.voice = old_v
                print("Saved audio data to", outfile[:-4] + '.mp3')
                print("Converting", outfile[:-4] + '.mp3', "to", outfile[:-4] + '.ogg')
                convert_one_mp3_to_ogg_file(outfile[:-4] + '.mp3', outfile[:-4] + '.ogg')
            assert(os.path.exists(outfile[:-4] + '.mp3'))
            assert(os.path.exists(outfile[:-4] + '.ogg'))
    print("phrase_audio() output is  >>>", outfile, "<<<")
    with open(outfile, 'rb') as f:
        return f.read()
    


def list_phrases_to_handle(smart_phrase):
    # FIXME WRITE DOX
    phrases_to_handle = []
    while len(smart_phrase) > 0:
        i = smart_phrase.find('${')
        if i < 0:
            phrases_to_handle.append(smart_phrase)
            smart_phrase = ''
        else:
            phrases_to_handle.append(smart_phrase[:i])
            j = smart_phrase.find('}', i)
            smart_phrase = smart_phrase[j+1:]
    return phrases_to_handle


def decoded_token(token:str, hello_owner:str, owner:str, shorttime:str, one_minute_ago:str, one_minute_later:str, morning_or_afternoon_or_evening:str) -> str:
    # FIXME WRITE DOX
    newval = token
    for _ in range(0, 5):
        oldval = newval
        ov_template = string.Template(oldval)
        newval = ov_template.substitute(hello_owner=hello_owner, owner=owner, shorttime=shorttime, one_minute_ago=one_minute_ago, one_minute_later=one_minute_later, morning_or_afternoon_or_evening=morning_or_afternoon_or_evening)
    return newval


def deliberately_cache_a_smart_phrase(voice:str, smart_phrase:str):
    '''
    Ensure that an audio file for the supplied text exists. If it doesn't, make it happen.
    '''
    # FIXME WRITE DOX
    phrases_to_handle = list_phrases_to_handle(smart_phrase)
    for phrase in phrases_to_handle:
        print("Does", phrase, "have a cached audio file?")
        
        phrase_path = pathname_of_phrase_audio(voice, phrase)
        old_phrasepath = pathname_of_phrase_audio(voice, phrase)
        for x in ('.ogg', '.mp3'):
            try:
                copyfile(phrase_path[:-4] + x, phrase_path.replace('_.ogg', '.ogg').replace('_.mp3','.mp3'))
            except:
                pass
        if phrase_path[-5] in ('_.mp3', '_.ogg'):
            os.rename()
        if os.path.exists(old_phrasepath) and not os.path.exists(phrase_path):
            print("Moving file from old to new")
            os.rename(old_phrasepath, phrase_path)
        if 0 == os.system('file "%s" | grep Ogg' % pathname_of_phrase_audio(voice, phrase, suffix='mp3')):
            print("Moving from mp3 to ogg")
            os.rename(pathname_of_phrase_audio(voice, phrase, suffix='mp3'),
                      pathname_of_phrase_audio(voice, phrase, suffix='ogg'))
        if 0 == os.system('file "%s" | grep MPEG' % pathname_of_phrase_audio(voice, phrase, suffix='ogg')):
            print("Moving from mp3 to ogg")
            os.rename(pathname_of_phrase_audio(voice, phrase, suffix='ogg'),
                      pathname_of_phrase_audio(voice, phrase, suffix='mp3'))            
        if os.system('file "%s" | grep empty' % phrase_path) and os.path.exists(phrase_path):
            os.unlink(phrase_path)
            
        if os.path.exists(pathname_of_phrase_audio(voice, phrase, suffix="mp3")):
            print("Yes, it exists for MP3. Cool. Let's convert it to OGG, just in case.")
            try:
                convert_one_mp3_to_ogg_file(phrase_path[:-4] + '.mp3', phrase_path[:-4] + '.ogg')
            except CouldntDecodeError:
                print("Oh, dear. The source file sucks. I'll delete it and its ogg counterpart ==>", phrase_path[:-4] + '.mp3')
                os.unlink(phrase_path[:-4] + '.mp3')
                try:
                    os.unlink(phrase_path[:-4] + '.ogg')
                except FileNotFoundError:
                    pass
    
        assert(pathname_of_phrase_audio(voice, phrase, suffix="mp3") == phrase_path[:-4] + '.mp3')
        assert(pathname_of_phrase_audio(voice, phrase, suffix="ogg") == phrase_path[:-4] + '.ogg')
        if os.path.exists(pathname_of_phrase_audio(voice, phrase, suffix="mp3")) \
        and os.path.exists(pathname_of_phrase_audio(voice, phrase, suffix="ogg")):
            print("Well, we still have an OGG and an MP3. Good.")
        else:
            print("No, it does not exist. That sucks.")
            if not os.path.exists(pathname_of_phrase_audio(voice, phrase, suffix="mp3")) \
            and os.path.exists(pathname_of_phrase_audio(voice, phrase, suffix="ogg")):
                print("We have the OGG but not the MP3. That is surprising. Still, we can cope.")
            try:
                os.unlink(pathname_of_phrase_audio(voice, phrase, suffix="ogg"))
            except:
                pass
            print("The output file SHOULD BE >>>", pathname_of_phrase_audio(voice, phrase, suffix='mp3'), "<<<")
            audio_op = phrase_audio(voice, phrase, suffix='mp3')
            assert(os.path.exists(pathname_of_phrase_audio(voice, phrase, suffix='mp3')))
            print("Now, we have audio for", voice, "saying", phrase, 'in mp3')
            try:
                convert_one_mp3_to_ogg_file(phrase_path[:-4] + '.mp3', phrase_path[:-4] + '.ogg')
            except Exception as e:
                raise("Failed to convert", phrase_path[:-4] + '.mp3', "to", phrase_path[:-4] + '.ogg', "and now I have to figure out why") from e
        print('the phrase path is', phrase_path)
        assert(os.path.exists(phrase_path[:-4] + '.mp3'))
        assert(os.path.exists(phrase_path[:-4] + '.ogg'))


def smart_phrase_audio(voice:str, smart_phrase:str, owner:str=None, time_24h:int=None, time_minutes:int=None, trim_level:int=1) -> AudioSegment:
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
                if searchforthis in ('',',','.',';',':','?','!'):
                    print("Warning -- searchforthis was %s; weird" % searchforthis)
                else:
                    raise MissingFromCacheError("{voice} => {searchforthis} <= {outfile} => is missing from the cache".format(searchforthis=searchforthis, voice=voice, outfile=outfile))
        firstwordno += 1
    return convert_audio_recordings_list_into_one_audio_recording(data=data, trim_level=trim_level)



def smart_phrase_filenames(voice:str, smart_phrase:str, owner:str=None, time_24h:int=None, time_minutes:int=None, suffix:str='ogg', fail_quietly=True) -> list:
    # FIXME WRITE DOX
    # FIXME This is a badly written subroutine. Clean it up. Document it. Thank you.
    if owner is not None and time_24h is not None and time_minutes is not None:
        detokenized_phrase = generate_detokenized_message(owner, time_24h, time_minutes, smart_phrase)
        detokenized_phrase = detokenized_phrase.replace('12 newn', '12:00 P.M.').replace('12 midnight', '12:00 A.M.')
    else:
        detokenized_phrase = ''.join(r + ' ' for r in list_phrases_to_handle(smart_phrase)).strip(' ')
    detokenized_phrase = detokenized_phrase.lower()
    audiofilenames = []
    all_words = [r.lower().strip(' ') for r in detokenized_phrase.split(' ')]
    firstwordno = 0
    while firstwordno < len(all_words):
        lastwordno = len(all_words)
        while lastwordno > firstwordno:
            searchforthis = ''.join([r + ' ' for r in all_words[firstwordno:lastwordno]]).strip()
            outfile = pathname_of_phrase_audio(voice, searchforthis)
            if not os.path.exists(outfile):
                lastwordno -= 1
            elif len(searchforthis) == 0:
                break
            else:
                firstwordno = lastwordno - 1
                audiofilenames.append(outfile)
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
                        errstr="{voice} => {s} <= {outfile} => (time thingy) is missing from the cache".format(s=s, voice=voice, outfile=outfile)
                        if fail_quietly:
                            print(errstr)
                        else:
                            raise MissingFromCacheError(errstr)
                    audiofilenames.append(outfile)
                firstwordno = lastwordno
            elif searchforthis in ('?', ':', '!', '.'):
                print("Ignoring", searchforthis)
            else:
                outfile = pathname_of_phrase_audio(voice, searchforthis, suffix=suffix)
                errstr="{voice} => {searchforthis} <= {outfile} => is missing from the cache".format(searchforthis=searchforthis, voice=voice, outfile=outfile)
                if fail_quietly:
                    print(errstr)
                else:
                    raise MissingFromCacheError(errstr)
        firstwordno += 1
    return audiofilenames




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


def speak_a_random_alarm_message(owner, hour, minute, voice, snoozed=False, fail_quietly=True):
    # FIXME WRITE DOX
    my_txt = generate_random_alarm_message(owner_of_clock=owner, time_24h=hour, time_minutes=minute, snoozed=snoozed)
    fnames = smart_phrase_filenames(voice, my_txt, fail_quietly=fail_quietly)
    for f in fnames:
        queue_oggfile(f)

def get_random_fart_fname():
    path = SOUNDS_FARTS_PATH
    fartfiles = [f for f in listdir(path) if isfile(join(path, f)) and f.endswith('.ogg')]
    fart_mp3file = '{path}/{chx}'.format(path=path, chx=random.choice(fartfiles))
    return fart_mp3file

def fart_and_apologize(voice:str, fart_vol=0.5): # , voice_vol=1.0):
    phrases_fnames = [r for r in smart_phrase_filenames(voice=voice, smart_phrase=choice(farting_msgs_lst))]
    fart_fname = get_random_fart_fname()
    fart_duration = pygame.mixer.Sound(fart_fname).get_length()
    play_audiofile(fart_fname, vol=fart_vol, nowait=True)
    time.sleep(min(1.0, fart_duration*2./3.))
    for f in phrases_fnames:
        queue_oggfile(f) #, vol=voice_vol)
    

# def fart_and_apologize(voice:str, fart_vol:int=90,voice_vol:int=100):
#     apologize_audioseg = smart_phrase_audio(voice, random.choice(farting_msgs_lst))
#     fart_audioseg = AudioSegment.from_mp3(get_random_fart_fname())
#     dB_diff = fart_vol-voice_vol
#     adjusted_fart = fart_audioseg + dB_diff
#     combined = adjusted_fart + apologize_audioseg
#     _ = combined.export("/tmp/out.mp3", format="mp3")
#     play_audiofile('/tmp/out.mp3') 
#     os.unlink('/tmp/out.mp3')

    

