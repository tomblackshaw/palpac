# -*- coding: utf-8 -*-

import datetime
import os
import sys

from PyQt5.QtWidgets import QWidget

from my.classes.exceptions import StillAwaitingCachedValue, WebAPITimeoutError, WebAPIOutputError, MainAppStartupError
from my.gui import set_audio_volume
from my.randomquotes import RandomQuoteSingleton as q
from my.text2speech import speak_a_random_alarm_message

#########################################################################################################




if __name__ == '__main__':
    for binname in ('mpv',): 
        if 0 != os.system('which {binname} > /dev/null'.format(binname=binname)):
            raise MainAppStartupError("{binname} is missing. Please install it.".format(binname=binname))
    voices_lst = ['Daniel', 'Chris', 'Jake- Smart, Formal, Confident', 'Sarah',
                  'New York Nick - Modern NYC Wiseguy', 'Eric', 'Alice', 'Callum',
                  'Olivier Calm', 'Liam', 'Laura', 'Jake - Smart, Formal, Confident',
                   'Will', 'Natasha - Valley girl', 'Sonia', 'Charlotte', 'Jessica',
                   'Frederick - Old Gnarly Narrator', 'George', 'Matilda',
                    'Charlie', 'Bill', 'Brian', 'Maya', 'Lily', 'Hugo']
    if len(sys.argv) == 1 or sys.argv[1] not in voices_lst:
        print("Options:", voices_lst)
        sys.exit(1)
    this_voice = sys.argv[1]
    set_audio_volume(int(sys.argv[2])) # between 0 and 10
    speak_a_random_alarm_message(owner='Charlie', voice=this_voice, hour=datetime.datetime.now().hour, minute=datetime.datetime.now().minute, snoozed=False)

