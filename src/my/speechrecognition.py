'''
Created on May 25, 2024

@author: Tom Blackshaw
'''

# https://stackoverflow.com/questions/59810209/speech-recognition-is-too-slow
# https://www.simplilearn.com/tutorials/python-tutorial/speech-recognition-in-python#:~:text=Open%20a%20Python%20interpreter%20or%20your%20preferred%20Python,following%20commands%3A%20import%20speech_recognition%20as%20sr%20print%20%28sr.__version__%29
#
# from _queue import Empty
# from array import array
# from queue import Queue
# from struct import pack
# from sys import byteorder
# from threading import Thread
# import ast
# import datetime
# import os
# import sys
# import time
# import wave
#
# from speech_recognition.exceptions import UnknownValueError
# import pyaudio
#
# from my.classes.exceptions import StillAwaitingCachedValue
# from my.classes.selfcachingcall import SelfCachingCall
# from my.stringutils import find_trigger_word_in_sentence
# from my.tools import logit
# from my.weather import WeatherSingleton as ws, generate_short_and_long_weather_forecast_messages
from my.classes.speechrecognitionclass import _SpeechRecognitionClass

SpeechRecognitionSingleton = _SpeechRecognitionClass()
