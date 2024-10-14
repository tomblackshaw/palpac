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

"""



import os
import sys

from PyQt5 import uic

from PyQt5.QtCore import QUrl, Qt, QObject, pyqtSignal
from PyQt5.QtWidgets import QScroller, QApplication, QMainWindow, QLabel, QStackedLayout, QWidget

from random import choice
from my.gui import BrowserView, set_vdu_brightness, set_audio_volume, make_background_translucent, \
                screenCaptureWidget, disable_scrollbars, enable_touchscroll
from my.globals import FACES_DCT, TOUCHSCREEN_SIZE_X, TOUCHSCREEN_SIZE_Y, ZOOMS_DCT
from os.path import join, isdir, isfile
from os import listdir
from my.text2speech import smart_phrase_audio, speak_a_random_alarm_message, fart_and_apologize, get_random_fart_fname,\
    smart_phrase_filenames
from my.stringutils import generate_random_string
import datetime
from my.consts import OWNER_NAME, farting_msgs_lst
from my.classes import singleton
from my.tools.sound import stop_sounds, play_audiofile

BASEDIR = os.path.dirname(__file__) # Base directory of me, the executable script
DEFAULT_CLOCK_NAME = list(FACES_DCT.keys())[-1]
VOICE_NAME = [f for f in listdir('sounds/cache') if isdir(join('sounds/cache', f))][0]
ALARMTONE_NAME = [f for f in listdir('sounds/alarms') if isfile(join('sounds/alarms', f))][0]

@singleton
class _MyQtSignals(QObject):
    setFace = pyqtSignal(str)
    freezeFace = pyqtSignal(str)
    showSettings = pyqtSignal()
    hideSettings = pyqtSignal()
    setJsTest = pyqtSignal(bool)
    setAlarm = pyqtSignal(str)

MyQtSignals = _MyQtSignals() 


def freezeframe_fname(face_name):
    return('{cwd}/ui/clocks/thumbs/{face_name}.png'.format(cwd=os.getcwd(), face_name=face_name))


class BrightnessWindow(QMainWindow):    
    '''Set brightness'''
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(os.path.join(BASEDIR, "ui/brightness.ui"), self)
        make_background_translucent(self)
        self.brightness_slider.valueChanged.connect(self.brightness_changed)
        
    def brightness_changed(self, x):
        set_vdu_brightness(x)
        

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
        uic.loadUi(os.path.join(BASEDIR, "ui/clocks.ui"), self)
        make_background_translucent(self)
        [self.faces_qlist.addItem(k) for k in FACES_DCT.keys()]
        [self.faces_qlist.setCurrentItem(x) for x in self.faces_qlist.findItems(initial_clock_name, Qt.MatchExactly)]
        MyQtSignals.setFace.emit(initial_clock_name)
        self.faces_qlist.currentTextChanged.connect(self.face_changed)
        enable_touchscroll(self.faces_qlist)
        
    def face_changed(self, x):
        if not os.path.exists(freezeframe_fname(x)): # TODO: ...or the cache is >3 days old?
            print("Sorry. I don't have a freezeframe pic of %s; I'll load the clock face instead." % x)
            MyQtSignals.setFace.emit(x)
            MyQtSignals.hideSettings.emit()
        else:
            MyQtSignals.freezeFace.emit(x)



class AlarmsWindow(QMainWindow):    
    '''Choose which alarm'''
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(os.path.join(BASEDIR, "ui/alarms.ui"), self)
        make_background_translucent(self)
        path = 'sounds/alarms'
        [self.alarms_qlist.addItem(f,) for f in listdir(path) if isfile(join(path, f)) and f.endswith('.ogg')]
        [self.alarms_qlist.setCurrentItem(x) for x in self.alarms_qlist.findItems(ALARMTONE_NAME, Qt.MatchExactly)]
        self.alarms_qlist.currentTextChanged.connect(self.new_alarm_chosen)
        for q in (self.alarms_qlist, self.hour_qlist, self.minutesA_qlist, self.minutesB_qlist, self.ampm_qlist):
            enable_touchscroll(q)
        
    def new_alarm_chosen(self, alarmtone):
        global ALARMTONE_NAME
        ALARMTONE_NAME = alarmtone
        stop_sounds()
        play_audiofile('sounds/alarms/%s' % alarmtone, nowait=True)
        
    def setVisible(self, onoroff):
        stop_sounds()
        super().setVisible(onoroff)


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
        enable_touchscroll(self.voices_qlist)


    def hello_button_clicked(self):
        fart_and_apologize(VOICE_NAME)

    def wakeup_button_clicked(self):
        speak_a_random_alarm_message(owner=OWNER_NAME, voice=VOICE_NAME, 
                                     hour=datetime.datetime.now().hour, minute=datetime.datetime.now().minute, 
                                     snoozed=False)

    def new_voice_chosen(self, voice):
        global VOICE_NAME
        VOICE_NAME = voice
        play_audiofile("""sounds/cache/{voice}/{owner}.mp3""".format(
                                            voice=VOICE_NAME, owner=OWNER_NAME.lower()), 
                       nowait=True)


class TestingWindow(QMainWindow):
    '''Test stuff'''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        uic.loadUi(os.path.join(BASEDIR, "ui/testing.ui"), self)
        make_background_translucent(self)
        MyQtSignals.setJsTest.connect(self.js_test_button_clicked)
        self.stopjs_button.clicked.connect(lambda: MyQtSignals.setJsTest.emit(False))
        self.startjs_button.clicked.connect(lambda: MyQtSignals.setJsTest.emit(True))

    def js_test_button_clicked(self, true_or_false):
        if true_or_false is True:
            print("START button was clicked")
        else:
            print("STOP button was clicked")
            self.parent.clockface.load_file(os.path.abspath('ui/icons/The_human_voice-1316067424.jpg'))
    

class SettingsWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.clockface = parent.clockface
        uic.loadUi(os.path.join(BASEDIR, "ui/settings.ui"), self)
        make_background_translucent(self)
        self.all_subwindows = []
        self.configure_a_subwindow(AlarmsWindow, self.alarms_button)
        self.configure_a_subwindow(VolumeWindow, self.volume_button)
        self.configure_a_subwindow(ClocksWindow, self.clocks_button)
        self.configure_a_subwindow(VoicesWindow, self.voices_button)
        self.configure_a_subwindow(TestingWindow,self.testing_button)
        self.configure_a_subwindow(BrightnessWindow, self.brightness_button)
        
    def configure_a_subwindow(self, a_class, a_button):
        a_window = a_class(self)
        a_window.hide()
        a_button.clicked.connect(lambda: self.choose_window(a_window))
        self.all_subwindows.append(a_window)
    
    def choose_window(self, chosen_subwindow=None):
        for w in self.all_subwindows:
            if w == chosen_subwindow:
                w.setVisible(not w.isVisible())
            else:
                w.hide()

    def hide(self):
        self.choose_window(None) # No subwindow was chosen. Therefore, this will hide all of them.
        super().hide()


class ClockFace(BrowserView):
    """The browser widget in which the JavaScript clock is displayed.
    
    This clockface displays whichever clockface it's told to display. The
    files are stored locally and probably in a nearby directory. That's
    why it accepts a local path for load() and turns it into a QUrl(file:///)
    etc. etc.
    
    Accepted signals:
        setFace
        freezeFace

    """    

    def __init__(self, parent=None):
        super().__init__(parent)
        MyQtSignals.setFace.connect(self.choose_face)
        MyQtSignals.freezeFace.connect(self.freeze_face)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(TOUCHSCREEN_SIZE_X, TOUCHSCREEN_SIZE_Y)

    def choose_face(self, face_name):
        self.setUpdatesEnabled(False)
        self.face_name = face_name
        self.load_file('{cwd}/{relpath}'.format(cwd=os.getcwd(), relpath=FACES_DCT[face_name]))
        self.setZoomFactor(ZOOMS_DCT[self.face_name] if self.face_name in ZOOMS_DCT.keys() else 1)
        disable_scrollbars(self)
        self.setUpdatesEnabled(True)

    def load_file(self, local_file):
        self.setZoomFactor(1)
        the_url = 'file://{local_file}'.format(local_file=local_file)
        self.load(QUrl(the_url))
        disable_scrollbars(self)

    def freeze_face(self, face_name):
        self.setUpdatesEnabled(False)
        self.face_name = face_name
        self.load_file(freezeframe_fname(face_name)) # Show the freezeframe
        self.setUpdatesEnabled(True)



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
        settings: The configurator window to be displayed/hidden/used.
        beard: The clickable overlay window. I call it a 'beard' because
            it acts as a beard for the clockface.
            
    Accepted signals:
        showSettings
        hideSettings

    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.our_layout = QStackedLayout()
        self.beard = QLabel("") # This label (which is invisible) is *stacked* in front of the clock, making it clickable.
        self.clockface = ClockFace(self) # The clock itself, on display
        self.settings = SettingsWindow(self) # The configuration window that appears when the user clicks on the beard/clock.
        make_background_translucent(self.beard)
        [self.our_layout.addWidget(w) for w in (self.clockface, self.beard, self.settings)]
        self.our_layout.setCurrentWidget(self.beard)
        self.our_layout.setStackingMode(QStackedLayout.StackAll) # Ensure that ALL the stack is visible at once.
        strawman = QWidget()
        strawman.setLayout(self.our_layout)
        self.setCentralWidget(strawman)
        self.settings.hide()
        MyQtSignals.hideSettings.connect(self.hide_settings_screen)
        MyQtSignals.showSettings.connect(self.show_settings_screen)

    def show_settings_screen(self):
        '''Make the Settings screen the top widget. Behind it, show a freezeframe of the clockface.'''
        screenCaptureWidget(self, self.clockface.pos(), freezeframe_fname(self.clockface.face_name))
        MyQtSignals.freezeFace.emit(self.clockface.face_name)
        self.settings.show()
        self.our_layout.setCurrentWidget(self.settings)
        
    def hide_settings_screen(self):
        '''Hide the Settings screen. Go back to displaying an animated clockface.'''
        self.settings.hide()
        self.our_layout.setCurrentWidget(self.beard)
        MyQtSignals.setFace.emit(self.clockface.face_name)

    def mousePressEvent(self, event):
        '''If the user clicks on the beard that covers the clockface, let's launch the Settings window; otherwise, let's hide it.'''
        if self.our_layout.currentWidget() == self.beard:
            MyQtSignals.showSettings.emit()
        else:
            MyQtSignals.hideSettings.emit()
        super().mousePressEvent(event)


if __name__ == '__main__':
    play_audiofile('sounds/startup.mp3', nowait=True)
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec_()






