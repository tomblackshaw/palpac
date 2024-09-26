#!/usr/bin/python3
# -*- coding: utf-8 -*-

import random
from os.path import join, isdir
from os import listdir


if __name__ == '__main__':
    from my.text2speech import just_fart
    path = 'sounds/cache'
    voices_lst = [f for f in listdir(path) if isdir(join(path, f))]
    voice = random.choice(voices_lst)
    just_fart()




