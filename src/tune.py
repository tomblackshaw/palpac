#!/usr/bin/python3
'''
create MP3s
mix them @ sofware level
Sing one MP3 file at a time
'''

from functools import partial
from pathlib import Path
import argparse
import datetime
import os
import random
import sys

from pydub.audio_segment import AudioSegment
import librosa
import librosa.display
import psola

from my.stringutils import generate_random_alarm_message
from my.text2speech import smart_phrase_audio
from my.tools.sound.sing import autotune_this_mp3, make_the_monks_chant
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sig
import soundfile as sf




