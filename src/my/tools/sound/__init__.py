'''
'''


import pygame  # @UnresolvedImport
import time
from pydub.audio_segment import AudioSegment
from my.tools.sound.trim import trim_my_audio
from my.globals import SOUNDS_CACHE_PATH
from pydub.exceptions import CouldntDecodeError
import os
from os import listdir
from os.path import isfile, join


pygame.mixer.init()

def stop_sounds():
    pygame.mixer.music.stop()
    pygame.mixer.stop()


def play_audiofile(fname, vol=1.0, nowait=False):
    if fname.endswith('.mp3'):
        play_mp3file(fname=fname, vol=vol, nowait=nowait)
    elif fname.endswith('.ogg'):
        play_oggfile(fname=fname, vol=vol, nowait=nowait)
    else:
        raise ValueError("play_audiofile() cannot handle files of type .%s" % fname.split('.')[-1])

def play_mp3file(fname, vol=1.0, nowait=False):
    pygame.mixer.music.load(fname)
    pygame.mixer.music.set_volume(vol)
    pygame.mixer.music.play()
    if not nowait:
        while pygame.mixer.music.get_busy() == True:
            continue

def play_oggfile(fname, vol=1.0, nowait=False):
    sound1 = pygame.mixer.Sound(fname)
    chan = pygame.mixer.find_channel(True)
    chan.set_volume(vol,vol)
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
    except:
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
            play_oggfile(item)
            qu.task_done()

from threading import Thread

from queue import Empty, Queue
ogg_queue = Queue()

consumer_thread = Thread(
        target=ogg_file_queue_thread_func,
        args=(ogg_queue,),
        daemon=True
    )
consumer_thread.start()




def queue_oggfile(fname):
    global ogg_queue
    ogg_queue.put(fname)
