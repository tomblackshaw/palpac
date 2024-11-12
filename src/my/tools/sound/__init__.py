# -*- coding: utf-8 -*-
"""Wraparound for audio playback, courtesy of pydub and pygame.

Created on Aug 21, 2024
Updated on Nov 05, 2024

@author: Tom Blackshaw

This module contains functions for converting audio (from mp3 to ogg) and
queuing their background playbcck (using a thread).

Example:
    TODO writeme

Attributes:
    consumer_thread
    ogg_queue

Todo:
    * Write TODOs

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import pygame  # @UnresolvedImport
import time
from pydub.audio_segment import AudioSegment
from my.tools.sound.trim import trim_my_audio
from my.globals import SOUNDS_CACHE_PATH
from pydub.exceptions import CouldntDecodeError
import os
from os import listdir
from os.path import isfile, join
from my.classes.exceptions import MissingFromCacheError
from threading import Thread
from queue import Empty, Queue


def stop_sounds():
    pygame.mixer.music.stop()
    pygame.mixer.stop()


def play_audiofile(fname, vol=1.0, nowait=False):
    if not os.path.exists(fname):
        raise FileNotFoundError("play_audiofile() cannot play %s: it doesn't exist" % fname)
    elif fname.endswith('.mp3'):
        play_mp3file(fname=fname, vol=vol, nowait=nowait)
    elif fname.endswith('.ogg'):
        play_oggfile(fname=fname, vol=vol, nowait=nowait)
    else:
        raise ValueError("play_audiofile() cannot handle files of type .%s" % fname.split('.')[-1])


def play_mp3file(fname, vol=1.0, nowait=False):
    try:
        pygame.mixer.music.load(fname)
    except FileNotFoundError as e:
        raise FileNotFoundError("play_mp3file() cannot play %s: it doesn't exist" % fname) from e
    else:
        pygame.mixer.music.set_volume(vol)
        pygame.mixer.music.play()
        if not nowait:
            while pygame.mixer.music.get_busy() == True:
                continue


def play_oggfile(fname, vol=1.0, nowait=False):
    try:
        sound1 = pygame.mixer.Sound(fname)
    except FileNotFoundError as e:
        raise FileNotFoundError("FYI, play_oggfile() cannot play %s: it doesn't exist" % fname) from e
    else:
        chan = pygame.mixer.find_channel(True)
        chan.set_volume(vol, vol)
        chan.play(sound1)
        if not nowait:
            while chan.get_busy() == True:
                continue


def mp3_to_ogg_conversions(path):
    errors = 0
    mp3files = [f for f in listdir(path) if isfile(join(path, f)) and f.endswith('.mp3')]
    for f in mp3files:
        mp3fname = '%s/%s' % (path, f)
        oggfname = mp3fname.replace('.mp3', '.ogg')
        if not os.path.exists(oggfname):
            try:
                convert_one_mp3_to_ogg_file(mp3fname, oggfname)
            except CouldntDecodeError:
                print("WARNING - could not decode %s; so, I'll delete it." % mp3fname)
                os.unlink(mp3fname)
                errors = errors + 1
    return errors


def mp3_to_ogg_voice_conversions(voice:str):
    path = '%s/%s' % (SOUNDS_CACHE_PATH, voice)
    mp3_to_ogg_conversions(path)


def convert_one_mp3_to_ogg_file(mp3fname, oggfname):
    assert(os.path.exists(mp3fname))
    try:
        os.unlink(oggfname)
    except FileNotFoundError as _:
        pass
    untrimmed_audio = AudioSegment.from_mp3(mp3fname)
    trimmed_aud = trim_my_audio(untrimmed_audio, trim_level=1)
    trimmed_aud.export(oggfname, format="ogg")
    assert(os.path.exists(oggfname))
#    print("Written output file to", oggfname)


def ogg_file_queue_thread_func(qu):
    while True:
        try:
            item = qu.get()
        except Empty:
            continue
        else:
            print(f'Processing item {item}')
            try:
                play_oggfile(item)
            except FileNotFoundError:
                print("ogg_file_queue_thread_func() -- cannot play %s: it doesn't exist" % item)
            qu.task_done()


def clear_ogg_queue():
    while True:
        try:
            _ = ogg_queue.get_nowait()
        except Empty:
            break
    stop_sounds()


_CLEAR_THE_QUEUE = False


def queue_oggfile(fname):  # TODO: rename queue_audiofile
    global ogg_queue
    if not os.path.exists(fname):
        raise MissingFromCacheError("queue_oggfile() cannot queue %s: it doesn't exist" % fname)
    ogg_queue.put(fname)

######################## MAIN-ish ###########################


ogg_queue = Queue()
pygame.mixer.init()
consumer_thread = Thread(
        target=ogg_file_queue_thread_func,
        args=(ogg_queue,),
        daemon=True
    )
consumer_thread.start()
