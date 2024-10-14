'''
'''


import pygame  # @UnresolvedImport


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

    