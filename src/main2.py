#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Sheepdip for a clock display.

This module contains classes and a main function to display a JavaScript-based
clock of the user's choosing. It also provides a configurator window, which is
accessed when the user clicks on the clock. Ordinarily, this wouldn't be much
of an achievement. However, in this case, the clock is displayed by a rudimentary
web browser, which in turn has no 'click me' signal nor event. To solve this
problem, I create an invisible (but clickable) window that is drawn in front of
the clock. When the user clicks on this invisible-but-clickable window, the
configurator window pops up... but it's transparent too, all except for its
widgets. The user can adjust settings there. If the user clicks beyond/outside
the configurator's widgets, the click will be detected by the invisible-but-
clickable window, which in turn will hide the configurator window.

In this way, the user is given the impression that (1) the clock is clickable,
(2) clicking on it will let the user reconfigure it 'live', and (3) clicking on
it again will hide the configuration tools. 

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
   
Configuration screen
- click on the center of the clock to get it
- when you've got it
    - you'll see three buttons
    - click 1/2/3 for a different config thing
        - brightness
        - volume
        - clock face
    - click anywhere to hide it again

"""

import os
import sys

from PyQt5 import uic
from PyQt5.QtCore import QUrl, Qt, QObject, pyqtSignal, QPoint, QEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QSizePolicy, QLabel, QStackedLayout, QWidget

from my.gui import set_vdu_brightness, set_audio_volume, make_background_translucent, make_window_transparent
from my.globals import FACES_DCT, TOUCHSCREEN_SIZE_X, TOUCHSCREEN_SIZE_Y, ZOOMS_DCT
import time
from os.path import join, isdir
from os import listdir

from my.gui import BrowserView, BrowserSettings
from my.consts import all_potential_owner_names
from my.text2speech import smart_phrase_audio, speak_a_random_alarm_message, just_apologize, fart_and_apologize
from my.stringutils import generate_random_string
import datetime
BASEDIR = os.path.dirname(__file__) # Base directory of me, the executable script
DEFAULT_CLOCK_NAME = 'braun' # list(FACES_DCT.keys())[0]
# find ui | grep index.html | grep -v /src/ | grep -v original

OWNER_NAME = all_potential_owner_names[0]
VOICE_NAME = [f for f in listdir('audio/cache') if isdir(join('audio/cache', f))][0]
print("VOICE_NAME =", VOICE_NAME)


class BrightnessWindow(QMainWindow):    
    def __init__(self, parent=None):
        super().__init__(parent)

        uic.loadUi(os.path.join(BASEDIR, "ui/brightness.ui"), self)
        make_background_translucent(self)
        self.brightness_slider.valueChanged.connect(set_vdu_brightness)
        

class VolumeWindow(QMainWindow):    
    def __init__(self, parent=None):
        super().__init__(parent)

        uic.loadUi(os.path.join(BASEDIR, "ui/volume.ui"), self)
        make_background_translucent(self)
        self.volume_slider.valueChanged.connect(set_audio_volume)

        
class ClocksWindow(QMainWindow):    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.clockface = parent.clockface
        uic.loadUi(os.path.join(BASEDIR, "ui/clocks.ui"), self)
        make_background_translucent(self)
        [self.faces_qlist.addItem(k) for k in FACES_DCT.keys()]
        self.faces_qlist.currentTextChanged.connect(lambda x: self.clockface.changeFace.emit(x)) 
        [self.faces_qlist.setCurrentItem(x) for x in self.faces_qlist.findItems(DEFAULT_CLOCK_NAME, Qt.MatchExactly)]


class VoicesWindow(QMainWindow):    
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(os.path.join(BASEDIR, "ui/voices.ui"), self)
        make_background_translucent(self)
        self.hello_button.clicked.connect(self.hello_button_clicked)
        self.wakeup_button.clicked.connect(self.wakeup_button_clicked)
        path = 'audio/cache'
        [self.voices_qlist.addItem(f,) for f in listdir(path) if isdir(join(path, f))]
        [self.voices_qlist.setCurrentItem(x) for x in self.voices_qlist.findItems(VOICE_NAME, Qt.MatchExactly)]
        self.voices_qlist.currentTextChanged.connect(self.new_voice_chosen)

    def hello_button_clicked(self):
        fart_and_apologize(voice=VOICE_NAME)
        
    def wakeup_button_clicked(self):
        speak_a_random_alarm_message(owner=OWNER_NAME, voice=VOICE_NAME, 
                                     hour=datetime.datetime.now().hour, minute=datetime.datetime.now().minute, 
                                     snoozed=False)

    def new_voice_chosen(self, voice):
        global VOICE_NAME
        VOICE_NAME = voice
        rndstr = generate_random_string(32)
        flat_filename = '/tmp/tts{rndstr}.flat.mp3'.format(rndstr=rndstr)
        data = smart_phrase_audio(VOICE_NAME, OWNER_NAME) # "I shall call you {nom}. Hello, {nom}.".format(nom=nom)) # x)
        data.export(flat_filename, format="mp3")
        os.system("$(which mpv) %s" % flat_filename)
        os.unlink(flat_filename)

        
class TestingWindow(QMainWindow):    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.clockface = parent.clockface
        uic.loadUi(os.path.join(BASEDIR, "ui/testing.ui"), self)
        make_background_translucent(self)
        self.stopjs_button.clicked.connect(self.stop_jsbutton_clicked)
        self.startjs_button.clicked.connect(self.start_jsbutton_clicked)
    
    def start_jsbutton_clicked(self):
        print("START JS button was clicked")
        s = self.clockface.settings()
        s.setAttribute(BrowserSettings.JavascriptEnabled, True)

    def stop_jsbutton_clicked(self):
        print("STOP JS button was clicked")
        s = self.clockface.settings()
        s.setAttribute(BrowserSettings.JavascriptEnabled, False)


class OwnersWindow(QMainWindow):    
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(os.path.join(BASEDIR, "ui/owners.ui"), self)
        make_background_translucent(self)
        [self.owners_qlist.addItem(s) for s in all_potential_owner_names]
        self.owners_qlist.setCurrentRow(all_potential_owner_names.index(OWNER_NAME))
        self.owners_qlist.currentTextChanged.connect(self.new_owner_chosen)
    
    def new_owner_chosen(self, nom):
        global OWNER_NAME
        OWNER_NAME = nom
        rndstr = generate_random_string(32)
        flat_filename = '/tmp/tts{rndstr}.flat.mp3'.format(rndstr=rndstr)
        data = smart_phrase_audio(VOICE_NAME, nom) # "I shall call you {nom}. Hello, {nom}.".format(nom=nom)) # x)
        data.export(flat_filename, format="mp3")
        os.system("$(which mpv) %s" % flat_filename)
        os.unlink(flat_filename)


class SettingsWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.clockface = parent.clockface
        uic.loadUi(os.path.join(BASEDIR, "ui/settings.ui"), self)
        make_background_translucent(self)
        self.volume_window = VolumeWindow(self)
        self.volume_window.hide()
        self.volume_button.clicked.connect(lambda: self.chosen(self.volume_window))
        self.brightness_window = BrightnessWindow(self)
        self.brightness_window.hide()
        self.brightness_button.clicked.connect(lambda: self.chosen(self.brightness_window))
        self.owners_window = OwnersWindow(self)
        self.owners_window.hide()
        self.owners_button.clicked.connect(lambda: self.chosen(self.owners_window))
        self.clocks_window = ClocksWindow(self)
        self.clocks_window.hide()
        self.clocks_button.clicked.connect(lambda: self.chosen(self.clocks_window))
        self.voices_window = VoicesWindow(self)
        self.voices_window.hide()
        self.voices_button.clicked.connect(lambda: self.chosen(self.voices_window))
        self.testing_window =  TestingWindow(self)
        self.testing_window.hide()
        self.testing_button.clicked.connect(lambda: self.chosen(self.testing_window))
    
    def chosen(self, subwindow=None):
        print("User chose", subwindow)
        for w in (self.volume_window, self.brightness_window, self.owners_window, self.clocks_window, self.testing_window, self.voices_window):
            if w == subwindow:
                w.setVisible(not w.isVisible())
            else:
                w.hide()
    
    def hide(self):
        self.chosen(None)
        super().hide()
        

class ClockFace(BrowserView):
    """The browser widget in which the JavaScript clock is displayed.
    
    This clockface displays whichever clockface it's told to display. The
    files are stored locally and probably in a nearby directory. That's
    why it accepts a local path for load() and turns it into a QUrl(file:///)
    etc. etc.

    """
    changeFace = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.changeFace.connect(self.load)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(TOUCHSCREEN_SIZE_X, TOUCHSCREEN_SIZE_Y)
        self.loadFinished.connect(self.adjust_zoom_etc)

    def load(self, face_name):
        self.face_name = face_name
        super().load(QUrl('file://{cwd}/{relpath}'.format(cwd=os.getcwd(), relpath=FACES_DCT[face_name])))
        
    def adjust_zoom_etc(self, _ok_or_nah):
        self.setZoomFactor(ZOOMS_DCT[self.face_name] if self.face_name in ZOOMS_DCT.keys() else 1)
        self.setStyleSheet('QScrollBar {height:0px;}; QScrollBar {width:0px;}')  # Turn background transparent too


class MainWindow(QMainWindow):
    """The main window for the PALPAC app.
    
    This will stack the clockface, its overlay window, and the configurator window.
    Then it hides the configurator window, leaving the overlay where it can be
    clicked. If the user tries to click on the clockface, they actually click on
    the overlay window, which will trigger the configurator window. Then, if the
    user clicks outside the configurator window, the overlay window will hide it
    again.

    In this way, the overlay window reveals and hides the configurator window.

    Attributes:
        clockface: The clockface to be displayed and used.
        confwindow: The configurator window to be displayed/hidden/used.
        beard: The clickable overlay window. I call it a 'beard' because
            it acts as a beard for the clockface.

    """    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.our_layout = QStackedLayout()
        self.clockface = ClockFace() # The clock itself, on display
        self.clockface.load(DEFAULT_CLOCK_NAME) 
        self.beard = QLabel("") # This label (which is invisible) is *stacked* in front of the clock, making it clickable.
        self.settings = SettingsWindow(self) # The configuration window that appears when the user clicks on the beard/clock.
        make_background_translucent(self.beard)
        for w in (self.clockface, self.beard, self.settings):
            self.our_layout.addWidget(w)
        self.our_layout.setCurrentWidget(self.beard)
        self.our_layout.setStackingMode(QStackedLayout.StackAll) # Ensure that ALL the stack is visible at once.
        strawman = QWidget()
        strawman.setLayout(self.our_layout)
        self.setCentralWidget(strawman)
        self.settings.hide()

    def mousePressEvent(self, event):
        if self.our_layout.currentWidget() == self.beard:
            print("Activating the settings screen")
            self.settings.show()
            self.our_layout.setCurrentWidget(self.settings)
        else:
            print("Hiding the settings screen")
            self.settings.hide()
            self.our_layout.setCurrentWidget(self.beard)
        super().mousePressEvent(event)


if __name__ == '__main__':
#os.system('''mpv audio/startup.mp3 &''')
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec_()




