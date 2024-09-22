# -*- coding: utf-8 -*-

import datetime
import os
import sys

from my.classes.exceptions import MainAppStartupError
from my.gui import set_audio_volume
from my.text2speech import speak_a_random_alarm_message
from os.path import join, isdir
from os import listdir

#########################################################################################################




if __name__ == '__main__':
    for binname in ('mpv',): 
        if 0 != os.system('which {binname} > /dev/null'.format(binname=binname)):
            raise MainAppStartupError("{binname} is missing. Please install it.".format(binname=binname))
    path = 'audio/cache'
    voices_lst = [f for f in listdir(path) if isdir(join(path, f))]
    if len(sys.argv) == 1 or sys.argv[1] not in voices_lst:
        print("Options:", voices_lst)
        sys.exit(1)
    this_voice = sys.argv[1]
    set_audio_volume(int(sys.argv[2])) # between 0 and 10
    speak_a_random_alarm_message(owner='Charlie', voice=this_voice, hour=datetime.datetime.now().hour, minute=datetime.datetime.now().minute, snoozed=False)

