# -*- coding: utf-8 -*-
""" sheepdip

Created on May 21, 2024

@author: Tom Blackshaw



EXAMPLE

from ast import literal_eval
from my.speechrecognition import SpeechRecognitionSingleton as s2t
s2t.always_adjust = True
s2t.max_recording_time = 3
s2t.pause_threshold = 0.8

mic = s2t.microphone

mic = s2t.api.Microphone()
with mic as source:
    recog = s2t.api.Recognizer()
#    recog.adjust_for_ambient_noise(source)
    audio =recog.listen(source)
s2t.recognize(audio)

from sheepdip import *
audio = s2t.listen()
s2t.recognize(audio)
from my.text2speech import Text2SpeechSingleton as tts
tts.voice = 'Freya'
tts.say("In the beginning was the word, and the word was with God, and the word was God.")
"""

from _queue import Empty
from queue import Queue
from threading import Thread
import datetime
import os
import sys
import time
from speech_recognition import AudioSource

from my.classes.exceptions import StillAwaitingCachedValue, MutedMicrophoneError, UnknownCommandError, MicrophoneTimeoutError
from my.classes.selfcachingcall import SelfCachingCall
from my.stringutils import find_trigger_phrase_in_sentence, scan_sentence_for_any_one_of_these_trigger_phrases, generate_triggerphrase_permutations, \
    trim_away_the_trigger_and_locate_the_command_if_there_is_one, text2time
from my.tools import logit
from my.weather import generate_weather_audio

words_that_sound_like_hey = 'he uh oh hayden either hate hey hay they a heh eight i Freya up great the there edit'
words_that_sound_like_dad = 'doc Dad there that tad thad than Dan dove dog the'
G_trigger_phrases = words_that_sound_like_dad.split(' ') + generate_triggerphrase_permutations(
    words_that_sound_like_hey.split(' '),
    words_that_sound_like_dad.split(' '))
G_stop = False

G_sorry_audio = None
G_fu2 = None
G_watch  = None
G_dowhatnow = None
G_our_cached_weather_report_messages = None
G_goodbye = None
G_yes = None
G_polo = None


def process_text(tts, text):
    global G_our_cached_weather_report_messages, G_stop, G_yes
#    print("voice =", tts.voice)
    if 'marco' in text:
        print("POLO")
    elif 'alarm' in text:
        print("ALARM")
        handle_alarm_command(tts, text)
    elif 'weather' in text:
        print("WEATHER")
        try:
            tts.play(G_our_cached_weather_report_messages.result['shorter audio'])
        except StillAwaitingCachedValue:
            tts.play(G_sorry_audio)
#        do_a_weather_report(tts, ws.forecast, tts.voice, 'Freya', True)c
    elif 'time' in text:
        print("TIME")
        tts.play(G_watch)
    elif 'screw' in text:
        print("SCREW YOU!")
        tts.play(G_fu2)
    elif 'bye' in text:
        print("BYE!")
        tts.play(G_goodbye)
        G_stop = True
    else:
        raise UnknownCommandError("I'm sorry, I don't understand that command >>{text}<<".format(text=text))
#        tts.say(text)
#        tts.play(G_dowhatnow)


def capture_a_snatch_of_audio_from_microphone(s2t):
    while not G_stop:
        time.sleep(.1)
        try:
            audio = s2t.listen()
            return audio
        except MicrophoneTimeoutError:
            print("Timed out, waiting for audio. Waiting again...")
        except MutedMicrophoneError:
            print("The mic was muted, probably by another thread in my app. Waiting again...")
            time.sleep(.2)


def indefinitely_capture_snatches_of_audio_from_microphone(s2t, audio_queue):
    while not G_stop:
        data = capture_a_snatch_of_audio_from_microphone(s2t)
        audio_queue.put(data)


def get_all_from_queue(text_queue):
    outtxt = ''
    while not G_stop:
        try:
            outtxt = text_queue.get_nowait()
            break
        except Empty:
            time.sleep(.1)
    return outtxt


def indefinitely_convert_all_audio(s2t, audio_queue, text_queue):
    while not G_stop:
        try:
            audio_data = audio_queue.get_nowait()
        except Empty:
            time.sleep(.1)
        else:
            text = s2t.recognize(audio_data)
            text_queue.put(text)


def empty_queue(q):
    for _ in range(0, 10):
        try:
            q.get_nowait()
        except Empty:
            pass


def indefinitely_turn_text_into_commands(s2t, text_queue, triggerphrases, goading_call, process_command_func, max_words_in_cache=20, max_secs_for_goading=3):
    global G_stop
    sentence = ''
    demand_triggerphrase = True
    datestamp_of_last_goading = datetime.datetime.now()
    while not G_stop:
        if demand_triggerphrase is False and (datetime.datetime.now() - datestamp_of_last_goading).total_seconds() > max_secs_for_goading:
#            print("Your no-trigger window has closed.")
            demand_triggerphrase = True
        time.sleep(.1)
        if sentence.count(' ') > max_words_in_cache:
#            print("Truncating ...")
            sentence = sentence[sentence.index(' ') + 1:]
        sentence = (sentence + ' ' + get_all_from_queue(text_queue)).strip()
        if len(sentence) == 0:
            pass
        else:
            cutoff_point = trim_away_the_trigger_and_locate_the_command_if_there_is_one(sentence, triggerphrases)
            if cutoff_point >= len(sentence):
#                print(">>{sentence}<< After removing the trigger phrase(s), I find no command.".format(sentence=sentence))
                print("Waiting for follow-up command to be spoken...")
                goading_call()  # So, goad them into saying more! (...but we don't need the trigger phrase, next time they talk)
                datestamp_of_last_goading = datetime.datetime.now()
                demand_triggerphrase = False
                sentence = ''
            elif cutoff_point >= 0 or demand_triggerphrase is False:
                if cutoff_point >= 0:
                    command = sentence[cutoff_point:]
                    print("The given command: >>{command}<<".format(command=command))
#                    print(">>{sentence}<< Command found: >>{command}<<".format(sentence=sentence, command=command))
                else:
                    command = sentence
                    print("Follow-up command: >>{command}<<".format(command=command))
                    print(">>{sentence}<< I couldn't find a trigger phrase. That doesn't matter, though: I was already primed for a command.".format(sentence=sentence))
                s2t.mute = True
                try:
                    process_command_func(command)
                    s2t.adjust_mic_for_ambient_noise()  # FIXME: Try this!
                    demand_triggerphrase = True
                except UnknownCommandError:
                    print("Failed to execute >>{command}<< (unknown command).".format(command=command))
                    if demand_triggerphrase is False:
                        print("Just in case there's a less insane command on the way, I'll wait a little while longer before reinstituting my demand for a triggerphrase.")
                except Exception as e:
                    print("Warning --- exception occurred --- {e}".format(e=str(e)))
                finally:
                    sentence = ''
                    empty_queue(text_queue)
                    s2t.mute = False
            else:
                print("Sentence >>{sentence}<< ...ignored (for now)".format(sentence=sentence))
                time.sleep(.1)


def handle_alarm_command(tts, text):
    timetxt = None
    for phr in ('up at', 'alarm for', 'alarm four', ''):
        i = text.find(phr)
        if i >= 0:
            timetxt = ' ' + text[i + len(phr) + 1:] + ' '
            timetxt = timetxt.replace(' for ', ' four ')  # in case of 'for forty' or 'ten oh for'
            timetxt = timetxt.strip()
            break
    if timetxt is None:
        print("Unable to deduce time text")
    else:
        print("Tryng to calculate hour and mins from time text >>{timetxt}<<".format(timetxt=timetxt))
        hrs, mns = text2time(text.split(' at ')[1])
        print("hrs =", hrs, "mns =", mns)


def main():
    print("Initializing the sheepdip")
    from my.speechrecognition import SpeechRecognitionSingleton as s2t
    global G_stop, G_yes
    from my.text2speech import Text2SpeechSingleton as tts
    global G_sorry_audio, G_fu2, G_watch, G_dowhatnow, G_our_cached_weather_report_messages, G_goodbye
    tts.voice = "Freya"
    owner_name = 'Chuckles'
    G_sorry_audio = tts.audio("Sorry, I'm still waiting for the weather forecast. Please try again later.")
    G_fu2 = tts.audio("Screw you too {owner_name}! I'm over here, working my ass off, and you know what, you're not even worth it.".format(owner_name=owner_name))
    print("Still initializing...")
    G_watch = tts.audio("It's time you got a watch, {owner_name}. Borrow some money from your Dad and buy one.".format(owner_name=owner_name))
    G_dowhatnow = tts.audio("I'm sorry. I don't understand.")
    G_yes = tts.audio("Yes?")  # May I help you {owner_name}?".format(owner_name=owner_name))
    G_goodbye = tts.audio("Toodles! Goodbye {owner_name}".format(owner_name=owner_name))
    G_our_cached_weather_report_messages = SelfCachingCall(180, generate_weather_audio, tts, owner_name)
    G_stop = False
    s2t.always_adjust = True
    s2t.max_recording_time = 5
    s2t.pause_threshold = 0.8
    audio_queue = Queue()  # FIXME: Add a limit. Add exception-catching for when we accidentally overload the queue, too.
    text_queue = Queue()  # FIXME: Make thread-safe, if not already. See https://superfastpython.com/thread-queue/
    audio_thread = Thread(target=indefinitely_capture_snatches_of_audio_from_microphone, args=(s2t, audio_queue,))
    audio_thread.start()
    convertsounds_thread = Thread(target=indefinitely_convert_all_audio, args=(s2t, audio_queue, text_queue,))
    convertsounds_thread.start()
    print("Press CTRL-C to quit.")
    indefinitely_turn_text_into_commands(s2t=s2t, text_queue=text_queue,
                                         triggerphrases=G_trigger_phrases,
                                         goading_call=lambda: tts.play(G_yes),
                                         process_command_func=lambda txt: process_text(tts, txt))
    convertsounds_thread.join()
    audio_thread.join()



if __name__ == '__main__':
    main()


