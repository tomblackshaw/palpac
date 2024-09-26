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

from my.gui import set_vdu_brightness, set_audio_volume, make_background_translucent, make_window_transparent, screenCaptureWidget
from my.globals import FACES_DCT, TOUCHSCREEN_SIZE_X, TOUCHSCREEN_SIZE_Y, ZOOMS_DCT, MPV_BIN
import time
from os.path import join, isdir
from os import listdir

from my.gui import BrowserView, BrowserSettings
#from my.consts import all_potential_owner_names
from my.text2speech import smart_phrase_audio, speak_a_random_alarm_message, just_apologize, fart_and_apologize
from my.stringutils import generate_random_string
import datetime
from PyQt5.QtGui import QPixmap
BASEDIR = os.path.dirname(__file__) # Base directory of me, the executable script
DEFAULT_CLOCK_NAME = 'braun' # list(FACES_DCT.keys())[0]
# find ui | grep index.html | grep -v /src/ | grep -v original

#OWNER_NAME = all_potential_owner_names[0]
VOICE_NAME = [f for f in listdir('sounds/cache') if isdir(join('sounds/cache', f))][0]

def freezeframe_fname(face_name):
    return('{cwd}/ui/clocks/{face_name}'.format(cwd=os.getcwd(), face_name=face_name))


class BrightnessWindow(QMainWindow):    
    '''Set brightness'''
    def __init__(self, parent=None):
        super().__init__(parent)

        uic.loadUi(os.path.join(BASEDIR, "ui/brightness.ui"), self)
        make_background_translucent(self)
        self.brightness_slider.valueChanged.connect(set_vdu_brightness)
        

class VolumeWindow(QMainWindow):    
    '''Set volume'''
    def __init__(self, parent=None):
        super().__init__(parent)

        uic.loadUi(os.path.join(BASEDIR, "ui/volume.ui"), self)
        make_background_translucent(self)
        self.volume_slider.valueChanged.connect(set_audio_volume)

        
class ClocksWindow(QMainWindow):    
    '''Choose which clockface'''
    def __init__(self, parent=None):
        super().__init__(parent)
        initial_clock_name = DEFAULT_CLOCK_NAME
        self.clockface = parent.clockface
        uic.loadUi(os.path.join(BASEDIR, "ui/clocks.ui"), self)
        make_background_translucent(self)
        [self.faces_qlist.addItem(k) for k in FACES_DCT.keys()]
        [self.faces_qlist.setCurrentItem(x) for x in self.faces_qlist.findItems(initial_clock_name, Qt.MatchExactly)]
        self.clockface.chooseFace.emit(initial_clock_name)
        self.faces_qlist.currentTextChanged.connect(self.face_changed)

    def face_changed(self, x):
        self.clockface.freezeFace.emit(x) # true == screenshot&freeze after loading

class VoicesWindow(QMainWindow):    
    '''Choose which voice'''
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(os.path.join(BASEDIR, "ui/voices.ui"), self)
        make_background_translucent(self)
        self.hello_button.clicked.connect(self.hello_button_clicked)
        self.wakeup_button.clicked.connect(self.wakeup_button_clicked)
        path = 'sounds/cache'
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
        os.system("{mpv} {fnam}".format(mpv=MPV_BIN, fnam=flat_filename))
        os.unlink(flat_filename)


class TestingWindow(QMainWindow):
    '''Test stuff'''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.clockface = parent.clockface
        uic.loadUi(os.path.join(BASEDIR, "ui/testing.ui"), self)
        make_background_translucent(self)
        self.stopjs_button.clicked.connect(self.stop_jsbutton_clicked)
        self.startjs_button.clicked.connect(self.start_jsbutton_clicked)
    
    def start_jsbutton_clicked(self):
        print("START button was clicked")

    def stop_jsbutton_clicked(self):
        print("STOP CLOCK button was clicked")
    

class OwnersWindow(QMainWindow):    
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(os.path.join(BASEDIR, "ui/owners.ui"), self)
        make_background_translucent(self)
#        [self.owners_qlist.addItem(s) for s in all_potential_owner_names]
#        self.owners_qlist.setCurrentRow(all_potential_owner_names.index(OWNER_NAME))
        self.owners_qlist.currentTextChanged.connect(self.new_owner_chosen)
    
    def new_owner_chosen(self, nom):
        global OWNER_NAME
        OWNER_NAME = nom
        rndstr = generate_random_string(32)
        flat_filename = '/tmp/tts{rndstr}.flat.mp3'.format(rndstr=rndstr)
        data = smart_phrase_audio(VOICE_NAME, nom) # "I shall call you {nom}. Hello, {nom}.".format(nom=nom)) # x)
        data.export(flat_filename, format="mp3")
        os.system("{mpv} {fnam}".format(mpv=MPV_BIN, fnam=flat_filename))
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
    chooseFace = pyqtSignal(str)
    freezeFace = pyqtSignal(str)
    

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.chooseFace.connect(self.choose_face)
        self.freezeFace.connect(self.freeze_face)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(TOUCHSCREEN_SIZE_X, TOUCHSCREEN_SIZE_Y)
        self._freeze_after_load = False # Changed to True by change_and_freeze()

    def choose_face(self, face_name):
        self.face_name = face_name
        self.load_file('{cwd}/{relpath}'.format(cwd=os.getcwd(), relpath=FACES_DCT[face_name]))
        self.adjust_zoom_etc()
    
    def load_file(self, local_file):
        self.setZoomFactor(1)
        self.load(QUrl('file://{local_file}'.format(local_file=local_file)))
        
    def adjust_zoom_etc(self, _ok_or_nah=False):
        del _ok_or_nah # Unused
        self.setZoomFactor(ZOOMS_DCT[self.face_name] if self.face_name in ZOOMS_DCT.keys() else 1)
        self.setStyleSheet('QScrollBar {height:0px;}; QScrollBar {width:0px;}')  # Turn background transparent too

    def freeze_face(self, face_name):
        if not os.path.exists(freezeframe_fname(face_name)):
            print("Sorry. I don't have a freezeframe pic of %s; I'll load the clock face instead." % face_name)
            self.choose_face(face_name)
        else:
            self.face_name = face_name
            self.load_file(freezeframe_fname(face_name))
        


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
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.our_layout = QStackedLayout()
        self.clockface = ClockFace(self) # The clock itself, on display
        self.beard = QLabel("") # This label (which is invisible) is *stacked* in front of the clock, making it clickable.
        self.clockface.beard = self.beard
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
#            if not os.path.exists(freezeframe_fname(self.clockface.face_name)):
            print("Taking freezeframe of", self.clockface.face_name)
            screenCaptureWidget(self, self.clockface.pos(), freezeframe_fname(self.clockface.face_name), 'png')
            self.clockface.freezeFace.emit(self.clockface.face_name)
            self.settings.show()
            self.our_layout.setCurrentWidget(self.settings)
        else:
            print("Hiding the settings screen")
            self.settings.hide()
            self.our_layout.setCurrentWidget(self.beard)
            self.clockface.chooseFace.emit(self.clockface.face_name)
        super().mousePressEvent(event)


if __name__ == '__main__':
    os.system('''%s sounds/startup.mp3 &''' % MPV_BIN)
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec_()




