'''
Created on May 24, 2024

@author: Tom Blackshaw
'''

from _queue import Empty
from array import array
from queue import Queue
from struct import pack
from sys import byteorder
from threading import Thread
import datetime
import os
import time
import wave

from speech_recognition.exceptions import UnknownValueError
import pyaudio

from my.classes.exceptions import StillAwaitingCachedValue
from my.classes.selfcachingcall import SelfCachingCall
from my.weather import WeatherSingleton as ws, generate_short_and_long_weather_forecast_messages

SLOWTALKER_TIMEOUT_IN_MICROSECONDS = 500999  # Assume that a normal human won't pause for more than 0.5s between words
THRESHOLD = 1000  # The higher the number, the MORE SENSITIVE the microphone will be.
NOOF_SILENCE = 32
CHUNK_SIZE = 2048
FORMAT = pyaudio.paInt16
RATE = 44100

G_stop = False
#
#
# def producer(queue, fname, r):
#     import speech_recognition as sr
#     while True:
#         print("please speak a word into the microphone")
#         try:
#             sample_width, data = record()
#             data = pack('<' + ('h' * len(data)), *data)
#             queue.put((datetime.datetime.now(), sample_width, data))
#             record_to_file(fname)
#         except OSError as e:  # https://stackoverflow.com/questions/10733903/pyaudio-input-overflowed/
#             if 'overflow' in str(e).lower():
#                 pass
# #                print("Warning. Input overflowed. Losing a frame or two.")
#             else:
#                 raise e
#         else:
#             # os.system('mpv {fname}'.format(fname=fname))
#             print("FORK ME! (FIXME) Trying to decode...")
#             try:
#                 with sr.AudioFile(fname) as source:
#                     # listen for the data (load audio to memory)
#                     audio_data = r.record(source)
#                     # recognize (convert from speech to text)
#                     text = r.recognize_google(audio_data)
#             except UnknownValueError:  # as e:
#                 time.sleep(.1)
#                 pass  # print("Failed to decode")
#             else:
#                 queue.put((datetime.datetime.now(), text))  # print('result =', text)
#         try:
#             os.unlink(fname)
#         except FileNotFoundError:
#             pass  # print("Warning - {fname} not found. Cannot delete temp file.".format(fname=fname))
#
#
# def consumer(queue, tts):
#     print('Consumer: Running')
#     new_timestamp = datetime.datetime.now()
#     while True:
#         sentence = ''
#         # get a unit of work
#         old_timestamp = new_timestamp
#         new_timestamp, text = queue.get()
#         if (new_timestamp - old_timestamp).microseconds >= 800999:
#             sentence = sentence.strip()
#             print("Sentence ==>", sentence)
#             sentence = ''
#         sentence += text + ' '
#         print("BTW, text was", text, "and now sentence is", sentence)
# #             tts.say(text)
#         # check for stop
#         if text is None:
#             time.sleep(1)
#         # report
#
#
# def record_and_pack_from_next_audioin_burst():
#     start_datestamp = datetime.datetime.now()
#     sample_width, data = record()
#     data = pack('<' + ('h' * len(data)), *data)
#     finish_datestamp = datetime.datetime.now()
#     return (start_datestamp, finish_datestamp, sample_width, data)
#
#
# def indefinitely_record_and_pack_incoming_audio(audio_queue):
#     global G_stop
#     while not G_stop:
#         try:
#             data = record_and_pack_from_next_audioin_burst()
#             audio_queue.put(data)
#         except OSError as e:
#             print("(indefinitely_record_and_pack_incoming_audio) Warning -- %s" % str(e))
#             time.sleep(.1)
#
#
# def convert_all_audio_in_queue(audio_queue, text_queue):
#     import speech_recognition as sr
#     r = sr.Recognizer()
#     last_finish_ds = datetime.datetime.now()
#     while True:
#         try:
#             start_datestamp, finish_datestamp, sample_width, data = audio_queue.get_nowait()
#             interpause_in_microseconds = (last_finish_ds - start_datestamp).microseconds
#             last_finish_ds = finish_datestamp
#         except Empty:
#             return
#         else:
#             audio_data = sr.AudioData(data, RATE, sample_width)
#             text = r.recognize_sphinx(audio_data)
#             text_queue.put((start_datestamp, finish_datestamp, interpause_in_microseconds, text))
#
#
# def get_sentences(text_queue, sentences_queue):
#     global G_stop
#     sentence = ''
#     while True:
#         try:
#             start_ds, end_ds, pause_IN_MICROseconds, text = text_queue.get_nowait()
#         except Empty:
#             if G_stop:
#                 break
#             else:
# #                print('waiting...')
#                 time.sleep(.1)
#         else:
#             print("text =", text)
#             sentence += text + ' '
#             if pause_IN_MICROseconds < SLOWTALKER_TIMEOUT_IN_MICROSECONDS:
# #                print("Waiting for more text")
#                 time.sleep(.1)
#             else:
# #                print("text =", text)
#                 sentence = sentence.strip()
#                 sentences_queue.put(sentence)
# #                print("==>", sentence, "<==")
#                 sentence = ''
#
#
# def indefinitely_convert_all_audio(audio_queue, text_queue):
#     global G_stop
#     while not G_stop:
#         convert_all_audio_in_queue(audio_queue, text_queue)

#
# def main():
#     import speech_recognition as sr
#     global G_stop
#     from my.classes.text2speechclass import Text2SpeechSingleton as tts
#     global G_sorry_audio, G_fu2, G_watch, G_dowhatnow, G_our_cached_weather_report_messages
# #     process_text(tts, "What's the weather like?")
#     r = sr.Recognizer()
#     tts.voice = "Freya"
#     owner_name = 'Chuckles'
#     # G_sorry_audio = tts.audio("Sorry, I'm still waiting for the weather forecast. Please try again later.")
#     # G_fu2 = tts.audio("Fuck you too, {owner_name}! I'm over here, working my ass off, and you know what, you're not even worth it.".format(owner_name=owner_name))
#     # G_watch = tts.audio("It's time you got a watch, {owner_name}. Borrow some money from your Dad and buy one.".format(owner_name=owner_name))
#     # G_dowhatnow = tts.audio("I'm sorry. I don't understand.")
#     # G_our_cached_weather_report_messages = SelfCachingCall(180, generate_weather_audio, owner_name, "Freya")
#     G_stop = False
#     from my.classes.text2speechclass import Text2SpeechSingleton as tts
#     import speech_recognition as sr
#     audio_queue = Queue()
#     text_queue = Queue()
#     sentences_queue = Queue(maxsize=50)
#     # rec1 = record_and_pack_from_next_audioin_burst()
#     # rec2 = record_and_pack_from_next_audioin_burst()
#     # rec3 = record_and_pack_from_next_audioin_burst()
#     # G_stop = False
#     audio_thread = Thread(target=indefinitely_record_and_pack_incoming_audio, args=(audio_queue,))
#     audio_thread.start()
#     convertsounds_thread = Thread(target=indefinitely_convert_all_audio, args=(audio_queue, text_queue,))
#     convertsounds_thread.start()
#     sentences_thread = Thread(target=get_sentences, args=(text_queue, sentences_queue,))
#     sentences_thread.start()
#     print("Press Ctrl-C to quit.")
#     while True:
#         sentence = sentences_queue.get()
#         print("SENTENCE =>", sentence)
#     G_stop = True
#     audio_thread.join()
#     convertsounds_thread.join()
#     sentences_thread.join()

if __name__ == '__main__':
    pass
