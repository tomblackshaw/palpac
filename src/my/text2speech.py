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
from datetime import datetime
from os import listdir
from os.path import isfile, join

from pydub.exceptions import CouldntDecodeError

from my.classes.exceptions import NoProfessionalVoicesError, MissingFromCacheError
from my.consts import hours_lst, minutes_lst, farting_msgs_lst, OWNER_NAME, hello_owner_lst, wannasnooze_msgs_lst, \
    postsnooze_alrm_msgs_lst, alarm_messages_lst, motivational_comments_lst
from my.stringutils import generate_detokenized_message, pathname_of_phrase_audio
from my.tools.sound.trim import convert_audio_recordings_list_into_one_audio_recording
from pydub.audio_segment import AudioSegment
from my.globals import ELEVENLABS_KEY_FILENAME, SOUNDS_FARTS_PATH
import time
from my.tools.sound import play_audiofile, queue_oggfile, convert_one_mp3_to_ogg_file
import pygame

print("my.text2speech -- importing/creating text2speech singleton")
Text2SpeechSingleton = None
if os.path.exists(ELEVENLABS_KEY_FILENAME):
    if 0 == os.system("ping -c2 -W5 www.elevenlabs.io"):
        try:
            from my.classes.text2speechclass import _Text2SpeechClass
            Text2SpeechSingleton = _Text2SpeechClass()
            print("Yay. Online? Check. Elevenlabs OK? Check. Key? Check. Woohoo!")
        except (ModuleNotFoundError, ImportError) as my_e:
            if 'circular' in str(my_e):
                raise my_e
            Text2SpeechSingleton = None  # compatibility w/ Python 3.8
    else:
        print("""We cannot use ElevenLabs: we're offline! Sorry. Let's just
        hope you're using the cache & not trying to call ElevenLabs...""")
else:
    print("""We cannot use ElevenLabs: there's no API key. Sorry. Let's
    just hope you're using the cache & not trying to call ElevenLabs...""")


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


def look_for_dupes():
    if 0 == os.system("""ls sounds/cache/*/*\\ * 2> /dev/null"""):
        os.system("""rm sounds/cache/*/*\\ *""")  #        raise SystemError("Somehow, I ended up with spare files for audio cache")

# def speak_random_alarm(owner_name:str, time_24h:int, time_minutes:int, voice:str=None, tts=Text2SpeechSingleton):
#     """Speak an alarm warning.
#
#     In the specified voice, to the specified owner of the alarm clock, speak an alarm
#     to alert the alarm clock user that a specific time has come.
#
#     Args:
#         owner_name: First name of the owner of the alarm clock.
#         time_24h: The time that has come (hours).
#         time_minutes: The time that has come (minutes).
#         voice: The name of the voice that I am to use.
#
#     """
#     if voice is None:
#         voice = tts.random_voice
#     message = generate_random_alarm_message(owner_name, time_24h, time_minutes, voice)
#     prof_name = get_first_prof_name(tts)  # [r for r in tts.api_voices if r.samples is not None][0].name
#     if voice == prof_name:
#         d = tts.audio(text=message, advanced=True, model='eleven_multilingual_v2', stability=0.30, similarity_boost=0.01, style=0.90, use_speaker_boost=True)
#     else:
#         d = tts.audio(text=message)
#     tts.play(d)

# def speak_totally_randomized_alarm_and_time(owner_of_clock:str):
#     """It does what it says on the tin."""
#     time_24h = random.randint(0, 24)
#     time_minutes = random.randint(0, 60)
#     speak_random_alarm(owner_of_clock, time_24h, time_minutes)


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


def phrase_audio(voice:str, text:str, suffix, raise_exception_if_not_cached:bool=False) -> bytes:
    alnums = sum(c.isdigit() for c in text) + sum(c.isalpha() for c in text)
    if alnums == 0:
#        print("Ignoring >>>%s<<< because it has no letters or numbers in it & is therefore unpronounceable." % text)
        return None
    if '{' in text or '}' in text:
        raise ValueError("{ or } is in >>>%s<<<" % text)
    # FIXME WRITE DOX
    outfile = pathname_of_phrase_audio(voice, text, suffix=suffix)
    text = text.lower().strip(' ')
    if len(text) > 1:
    # if text not in ('!', '?', '.', ','):
        while len(text) > 0 and text[0] in ' !?;:.,':
            text = text[1:]
    if len(text) == 0:
#        print("An empty phrase HAS no audio file associated with it.")
        return None
    elif not os.path.exists(outfile):
        if raise_exception_if_not_cached:
            raise MissingFromCacheError("'{text}' (for {voice}) should have been cached not hasn't been.".format(text=text, voice=voice))
#        print(voice, '==>', text)
        print("Generating speech audio (spoken by {voice}) for '{text}'".format(voice=voice, text=text))
        vers = sys.version_info
        look_for_dupes()
        major_ver, minor_ver = vers[:2]
        if major_ver < 3 or minor_ver < 11:  # Some versions of Python can't handle Eleven Labs. Therefore, we call the bash script, will calls the correct version. Or something.
            os.system('''./_cachespeech.sh "{voice}" "{text}" "{outfile}"'''.format(voice=voice, text=text, outfile=outfile))
        else:
            print("Writing >>>%s<<<" % (outfile[:-4] + '.mp3'))
            old_v = Text2SpeechSingleton.voice
            Text2SpeechSingleton.voice = voice
            look_for_dupes()
            os.system('mkdir -p "{mydir}"'.format(mydir=os.path.dirname(outfile)))
            try:
                assert(text[0] not in ('?!;:,. (){}'))
            except AssertionError as e:
                raise ValueError(">>>%s<<< is invalid. Its starting character sucks ass." % text) from e
            try:
                os.unlink(outfile[:-4] + '.mp3')
            except FileNotFoundError:
                pass
            with open(outfile[:-4] + '.mp3', 'wb') as f:
                f.write(Text2SpeechSingleton.audio(text))
            Text2SpeechSingleton.voice = old_v
            look_for_dupes()
            print("Saved audio data to", outfile[:-4] + '.mp3')
            print("Converting", outfile[:-4] + '.mp3', "to", outfile[:-4] + '.ogg')
            convert_one_mp3_to_ogg_file(outfile[:-4] + '.mp3', outfile[:-4] + '.ogg')
            assert(os.path.exists(outfile[:-4] + '.mp3'))
            assert(os.path.exists(outfile[:-4] + '.ogg'))
            look_for_dupes()
            print("phrase_audio() output is  >>>%s<<< (and we just created it)" % outfile)
#    else:
#        print("phrase_audio() output is  >>>%s<<< (and it already exists)" % outfile)
    look_for_dupes()
    with open(outfile, 'rb') as f:
        return f.read()


def list_phrases_to_handle(smart_phrase):
    # FIXME WRITE DOX
    phrases_to_handle = []
    while len(smart_phrase) > 0:
        i = smart_phrase.find('${')
        if i < 0:
            phrase_to_append = smart_phrase.strip(' ')
            smart_phrase = ''
        else:
            phrase_to_append = smart_phrase[:i].strip(' ')
            j = smart_phrase.find('}', i)
            smart_phrase = smart_phrase[j + 1:]
        while len(smart_phrase) > 0 and smart_phrase[0] in "!?;:,. ":
#            print("Skipping the first character of >>>%s<<<" % (smart_phrase))
            smart_phrase = smart_phrase[1:]
        alnums = sum(c.isdigit() for c in phrase_to_append) + sum(c.isalpha() for c in phrase_to_append)
        if alnums == 0:
#            print("Ignoring >>>%s<<< because it has no nutritional value" % phrase_to_append)
            pass
        elif phrase_to_append[0] in "!?;:,. ":
            raise ValueError("The phrase >>>%s<<< contains punctuation." % phrase_to_append)
        else:
            phrases_to_handle.append(phrase_to_append)
    return phrases_to_handle


def decoded_token(token:str, hello_owner:str, owner:str, shorttime:str, one_minute_ago:str, one_minute_later:str, morning_or_afternoon_or_evening:str) -> str:
    # FIXME WRITE DOX
    newval = token
    for _ in range(0, 5):
        oldval = newval
        ov_template = string.Template(oldval)
        newval = ov_template.substitute(hello_owner=hello_owner, owner=owner, shorttime=shorttime, one_minute_ago=one_minute_ago, one_minute_later=one_minute_later, morning_or_afternoon_or_evening=morning_or_afternoon_or_evening)
    return newval


def deliberately_cache_a_smart_sentence(voice:str, smart_phrase:str):
    '''
    Ensure that an audio file for the supplied text exists. If it doesn't, make it happen.
    '''
    assert('${owner}' not in smart_phrase)
    print("Does %s's >>>%s<<< smart phrase have a cached audio set?" % (voice, smart_phrase))
    phrases_to_handle = list_phrases_to_handle(smart_phrase)
    if phrases_to_handle in (None, []):
        raise ValueError(">>>%s<<< contained nothing of value. WTF." % smart_phrase)
    for phrase in phrases_to_handle:
        cache_one_phrase(voice, phrase)  # ...unless it has already been cached.
        try:
            check_that_files_are_mp3_and_ogg(voice, phrase)
        except SystemError:
            print("Failed to cache >>>%s<<< for >>>%s<<<; retrying..." % (phrase, voice))
            for suffix in ('mp3', 'ogg'):
                try:
                    os.unlink(pathname_of_phrase_audio(voice, phrase, suffix=suffix))
                except FileNotFoundError:
                    pass
            deliberately_cache_a_smart_sentence(voice, phrase)


def cache_one_phrase(voice:str, phrase:str):
    print("Does %s's >>>%s<<< have a cached audio file?" % (voice, phrase))
    if len(phrase) == 0:
        raise ValueError("Why ask me to cache a string of zero length?")
    if phrase[0] in "!?;:,. ":
        raise ValueError("Do not ask me to cache a phrase that starts with punctuation or a space.")
    if phrase[-1] == ' ':
        raise ValueError("Do not ask me to cache a phrase that ends with a space.")
    if 0 == sum(c.isdigit() for c in phrase) + sum(c.isalpha() for c in phrase):
        raise ValueError("Rejecting >>>%s<<< because it has no letters or numbers in it & is therefore unpronounceable." % phrase)
    phrase_path = pathname_of_phrase_audio(voice, phrase)
    if 0 == os.system('file "%s" | grep Ogg' % pathname_of_phrase_audio(voice, phrase, suffix='mp3')):
        print("This mp3 file is actually ogg. So, I'm renaming it.")
        os.rename(pathname_of_phrase_audio(voice, phrase, suffix='mp3'),
                  pathname_of_phrase_audio(voice, phrase, suffix='ogg'))
    if 0 == os.system('file "%s" | grep MPEG' % pathname_of_phrase_audio(voice, phrase, suffix='ogg')):
        print("This ogg file is actually mp3. So, I'm renaming it.")
        os.rename(pathname_of_phrase_audio(voice, phrase, suffix='ogg'),
                  pathname_of_phrase_audio(voice, phrase, suffix='mp3'))
    if 0 == os.system('file "%s" | fgrep ": empty"' % phrase_path) and os.path.exists(phrase_path):
        print("FYI, >>>%s<<< was empty. I'll delete it now." % phrase_path)
        os.unlink(phrase_path)
    if os.path.exists(pathname_of_phrase_audio(voice, phrase, suffix="mp3")) \
    and not os.path.exists(pathname_of_phrase_audio(voice, phrase, suffix="ogg")):
        print("Does %s's >>>%s<<< have a cached audio file? Yes, MP3; no, OGG. Let's convert MP3 to OGG, just in case." % (voice, phrase))
        try:
            convert_one_mp3_to_ogg_file(phrase_path[:-4] + '.mp3', phrase_path[:-4] + '.ogg')
            assert(os.path.exists(pathname_of_phrase_audio(voice, phrase, suffix="ogg")))
            assert(os.path.exists(pathname_of_phrase_audio(voice, phrase, suffix="mp3")))
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
        print("Does {voice}'s >>>{phrase}<<< have a cached audio file? YES (mp3+ogg)".format(voice=voice, phrase=phrase))
    else:
        print("Does {voice}'s >>>{phrase}<<< have a cached audio file? NO. So, I'll create a pair (mp3+ogg).".format(voice=voice, phrase=phrase))
        if not os.path.exists(pathname_of_phrase_audio(voice, phrase, suffix="mp3")) \
        and os.path.exists(pathname_of_phrase_audio(voice, phrase, suffix="ogg")):
            print("We have the OGG but not the MP3. That is surprising. Still, we can cope.")
        try:
            os.unlink(pathname_of_phrase_audio(voice, phrase, suffix="ogg"))
        except FileNotFoundError as _:
            pass
        _ = phrase_audio(voice, phrase, suffix='mp3')
        assert(os.path.exists(pathname_of_phrase_audio(voice, phrase, suffix='mp3')))
        try:
            convert_one_mp3_to_ogg_file(phrase_path[:-4] + '.mp3', phrase_path[:-4] + '.ogg')
        except Exception as e:
            errstr = "Failed to convert", phrase_path[:-4] + '.mp3', "to", phrase_path[:-4] + '.ogg', "and now I have to figure out why"
            raise SystemError(errstr) from e
        assert(os.path.exists(phrase_path[:-4] + '.mp3'))
        assert(os.path.exists(phrase_path[:-4] + '.ogg'))
        print("Does {voice}'s >>>{phrase}<<< have a cached audio file? YES (mp3+ogg) ...now.".format(voice=voice, phrase=phrase))


def check_that_files_are_mp3_and_ogg(voice, phrase):
    if 0 != os.system('file "%s" | grep MPEG > /dev/null' % pathname_of_phrase_audio(voice, phrase, suffix='mp3')):
        raise SystemError(">>>%s<<< should be an MP3 but it's not." % pathname_of_phrase_audio(voice, phrase, suffix='mp3'))
    if 0 != os.system('file "%s" | grep Ogg > /dev/null' % pathname_of_phrase_audio(voice, phrase, suffix='ogg')):
        raise SystemError(">>>%s<<< should be an OGG but it's not." % pathname_of_phrase_audio(voice, phrase, suffix='ogg'))


def smart_phrase_audio(voice:str, smart_phrase:str, owner:str, time_24h:int=None, time_minutes:int=None, trim_level:int=1, suffix='ogg') -> AudioSegment:
    assert(suffix in ('mp3', 'ogg'))
    assert(owner == OWNER_NAME)  #     assert(owner not in (None, '', 'mp3', 'ogg'))
    # FIXME This is a badly written subroutine. Clean it up. Document it. Thank you.
    smart_phrase = smart_phrase.replace('${owner}', owner)  # This way, 'Hello ${owner}' is stored as 'Hello, Charlie' or whatever.
    look_for_dupes()
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
                look_for_dupes()
                the_new_audio_data = phrase_audio(voice, searchforthis, suffix=suffix)
                if the_new_audio_data is not None:
                    data.append(the_new_audio_data)
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
                    look_for_dupes()
                    outfile = pathname_of_phrase_audio(voice, s)
                    if not os.path.exists(outfile):
                        raise MissingFromCacheError("{voice} => {s} <= {outfile} => (time thingy) is missing from the cache".format(s=s, voice=voice, outfile=outfile))
                    the_new_audio_data = phrase_audio(voice, s, suffix=suffix)
                    if the_new_audio_data is not None:
                        data.append(the_new_audio_data)
                    look_for_dupes()
                firstwordno = lastwordno
            elif sum(c.isdigit() for c in searchforthis) + sum(c.isalpha() for c in searchforthis) == 0:
                print("Ignoring", searchforthis)
            else:
                outfile = pathname_of_phrase_audio(voice, searchforthis)
                if searchforthis in ('', ',', '.', ';', ':', '?', '!', " "):
                    print("Warning -- searchforthis was %s; weird" % searchforthis)
                else:
                    raise MissingFromCacheError("{voice} => {searchforthis} <= {outfile} => is missing from the cache".format(searchforthis=searchforthis, voice=voice, outfile=outfile))
        firstwordno += 1
    return convert_audio_recordings_list_into_one_audio_recording(data=data, trim_level=trim_level, suffix=suffix)


def smart_phrase_filenames(voice:str, smart_phrase:str, owner:str=None, time_24h:int=None, time_minutes:int=None, suffix:str='ogg', fail_quietly=True) -> list:
    # FIXME WRITE DOX
    # FIXME This is a badly written subroutine. Clean it up. Document it. Thank you.
    if owner is not None and time_24h is not None and time_minutes is not None:
        detokenized_phrase = generate_detokenized_message(owner, time_24h, time_minutes, smart_phrase)
        detokenized_phrase = detokenized_phrase.replace('12 newn', '12:00 P.M.').replace('12 midnight', '12:00 A.M.')
    else:
        detokenized_phrase = ''.join(r + ' ' for r in list_phrases_to_handle(smart_phrase)).strip(' ')
    detokenized_phrase = detokenized_phrase.lower().replace('..', '.!')  # e.g. a.m.., p.m..
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
                        errstr = "{voice} => {s} <= {outfile} => (time thingy) is missing from the cache".format(s=s, voice=voice, outfile=outfile)
                        if fail_quietly:
                            print(errstr)
                        else:
                            raise MissingFromCacheError(errstr)
                    audiofilenames.append(outfile)
                firstwordno = lastwordno
            elif searchforthis in ('?', ':', '!', '.'):
                print("Ignoring >>>%s<<<" % searchforthis)
            else:
                outfile = pathname_of_phrase_audio(voice, searchforthis, suffix=suffix)
                errstr = "{voice} => {searchforthis} <= {outfile} => is missing from the cache".format(searchforthis=searchforthis, voice=voice, outfile=outfile)
                if fail_quietly:
                    print(errstr)
                else:
                    raise MissingFromCacheError(errstr)
        firstwordno += 1
    return audiofilenames


def generate_timedate_phrases_list(timedate_str:str) -> list:
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
        return (hours_lst[int(the_hr)] + '?',
                minutes_lst[int(the_min)],
                )
    else:
        return (
            hours_lst[int(the_hr)] + '?',
            minutes_lst[int(the_min)] + '?',
            the_ampm + ',',
            )


def speak_a_randomly_chosen_smart_sentence(owner, voice, message_template_list, fail_quietly=True, time_24h=None, time_minute=None):
    """Speak a randomly chosen sentence, using snippets from our cache.

    Owner: e.g. Charlie
    Voice: Name of ElevenLabs voice to use
    message_template_list: List [] of templates that I could use. I'll pick one at random.
    fail_quietly: If a sample is missing, should I fail quietly (by ignoring it) or raise an exception?
    time_24h: Self-explanatory.
    time_minute: See above.

    """
    message_template = random.choice(message_template_list)
    speak_this_smart_sentence(owner, voice, message_template, fail_quietly, time_24h, time_minute)


def speak_this_smart_sentence(owner, voice, message_template, fail_quietly=True, time_24h=None, time_minute=None):
    if time_24h is None or time_minute is None:
        t = datetime.now()
        time_24h = t.hour
        time_minute = t.minute
    message = generate_detokenized_message(owner=owner, time_24h=time_24h, time_minutes=time_minute, message_template=message_template)
    fnames = smart_phrase_filenames(voice, message, fail_quietly=fail_quietly)
    for f in fnames:
        print("Playing", f)
        queue_oggfile(f)


def speak_a_random_alarm_message(owner, voice, alarm_time=None, snoozed=False, fail_quietly=True):
    if alarm_time is None:
        t = datetime.now()
        hour = t.hour
        minute = t.minute
    else:
        hour = int(alarm_time[:2])
        minute = int(alarm_time[3:])
    message_template_lst = postsnooze_alrm_msgs_lst if snoozed else alarm_messages_lst
    speak_a_randomly_chosen_smart_sentence(owner=owner, voice=voice, message_template_list=message_template_lst,
                                           fail_quietly=fail_quietly, time_24h=hour, time_minute=minute)


def speak_a_random_hello_message(owner, voice, fail_quietly=True):
    speak_a_randomly_chosen_smart_sentence(owner, voice, hello_owner_lst, fail_quietly)


def speak_a_random_motivational_comment(owner, voice, fail_quietly=True):
    speak_a_randomly_chosen_smart_sentence(owner, voice, motivational_comments_lst, fail_quietly)


def speak_a_random_wannasnooze_message(owner, voice, fail_quietly=True):
    speak_a_randomly_chosen_smart_sentence(owner, voice, wannasnooze_msgs_lst, fail_quietly)


def get_random_fart_fname():
    path = SOUNDS_FARTS_PATH
    fartfiles = [f for f in listdir(path) if isfile(join(path, f)) and f.endswith('.ogg')]
    fart_mp3file = '{path}/{chx}'.format(path=path, chx=random.choice(fartfiles))
    return fart_mp3file


def fart_and_apologize(voice:str, fart_vol=0.5):
    phrases_fnames = [r for r in smart_phrase_filenames(voice=voice, smart_phrase=choice(farting_msgs_lst))]
    fart_fname = get_random_fart_fname()
    fart_duration = pygame.mixer.Sound(fart_fname).get_length()
    play_audiofile(fart_fname, vol=fart_vol, nowait=True)
    time.sleep(min(1.0, fart_duration * 2. / 3.))
    for f in phrases_fnames:
        queue_oggfile(f)

