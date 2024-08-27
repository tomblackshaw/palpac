# -*- coding: utf-8 -*-
""" sheepdip

Created on May 21, 2024

@author: Tom Blackshaw



EXAMPLE

from my.text2speech import Text2SpeechSingleton as tts
from my.stringutils import generate_random_alarm_message
import datetime
import random
tts.voice = random.choice(tts.all_voices)
tts.say(generate_random_alarm_message('Charles Rabson', datetime.datetime.now().hour, datetime.datetime.now().minute)) # , for_voice=tts.voice))

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
tts.say("1, 2, 3, 4, 5.")

tts.say("In the beginning was the word, and the word was with God, and the word was God.")

import os
os.system('''for i in $(wpctl status | grep HDMI | tr ' ' '\n' | tr '.' '\n' | grep -x "[0-9]*"); do  wpctl set-volume $i 100% 2> /dev/null; done''')
from my.text2speech import Text2SpeechSingleton as tts
from elevenlabs import stream, play
tts.voice = 'Freya'
#data = tts.audio("Hello world.", stream=True)

audio_stream = tts.client.generate(
  text="Your text here",
  voice="Freya",
  optimize_streaming_latency=1,  # Adjust as needed
  output_format="mp3_44100_128",  # Adjust as needed
  voice_settings={
    "similarity_boost": 1.0,  # Adjust as needed
    "stability": 1.0,  # Adjust as needed
    "style": 1,  # Adjust as needed
    "use_speaker_boost": True  # Adjust as needed
  }
)



stream(audio_stream)
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
from my.tools import logit
# from my.weather import generate_weather_audio

G_stop = False

G_sorry_audio = None
G_fu2 = None
G_watch  = None
G_dowhatnow = None
G_our_cached_weather_report_messages = None
G_goodbye = None
G_yes = None
G_polo = None



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

def main():
    os.system('''for i in $(wpctl status | grep HDMI | tr ' ' '\n' | tr '.' '\n' | grep -x "[0-9]*"); do  wpctl set-volume $i 100% 2> /dev/null; done''')
    print("Initializing the sheepdip")
    # from my.speechrecognition import SpeechRecognitionSingleton as s2t
    global G_stop, G_yes
    from my.text2speech import Text2SpeechSingleton as tts
    global G_sorry_audio, G_fu2, G_watch, G_dowhatnow, G_our_cached_weather_report_messages, G_goodbye
    tts.voice = "Sarah"
    owner_name = 'Chuckles'
    G_sorry_audio = tts.audio("Sorry, I'm still waiting for the weather forecast. Please try again later.")
    G_fu2 = tts.audio("Screw you too {owner_name}! I'm over here, working my ass off, and you know what, you're not even worth it.".format(owner_name=owner_name))
    print("Still initializing...")
    G_watch = tts.audio("It's time you got a watch, {owner_name}. Borrow some money from your Dad and buy one.".format(owner_name=owner_name))
    G_dowhatnow = tts.audio("I'm sorry. I don't understand.")
    G_yes = tts.audio("Yes?")  # May I help you {owner_name}?".format(owner_name=owner_name))
    G_goodbye = tts.audio("Toodles! Goodbye {owner_name}".format(owner_name=owner_name))
#    G_our_cached_weather_report_messages = SelfCachingCall(180, generate_weather_audio, tts, owner_name)
    G_stop = False
    # s2t.always_adjust = True
    # s2t.max_recording_time = 5
    # s2t.pause_threshold = 0.8
    # audio_queue = Queue()  # FIXME: Add a limit. Add exception-catching for when we accidentally overload the queue, too.
    # text_queue = Queue()  # FIXME: Make thread-safe, if not already. See https://superfastpython.com/thread-queue/
    # audio_thread = Thread(target=indefinitely_capture_snatches_of_audio_from_microphone, args=(s2t, audio_queue,))
    # audio_thread.start()
    # convertsounds_thread = Thread(target=indefinitely_convert_all_audio, args=(s2t, audio_queue, text_queue,))
    # convertsounds_thread.start()
    # print("Press CTRL-C to quit.")
    # indefinitely_turn_text_into_commands(s2t=s2t, text_queue=text_queue,
    #                                      triggerphrases=G_trigger_phrases,
    #                                      goading_call=lambda: tts.play(G_yes),
    #                                      process_command_func=lambda txt: process_text(tts, txt))
    # convertsounds_thread.join()
    # audio_thread.join()


if __name__ == '__main__':
    main()


