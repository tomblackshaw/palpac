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

from PyQt5.QtCore import QUrl, Qt, QObject, pyqtSignal, QSize
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QStackedLayout, QWidget, QMessageBox

from my.gui import BrowserView, set_vdu_brightness, set_audio_volume, make_background_translucent, \
                screenCaptureWidget, make_scrollbars_zeropixels_in_size, enable_touchscroll, popup_message
from my.globals import FACES_DCT, FACES_LST, TOUCHSCREEN_SIZE_X, TOUCHSCREEN_SIZE_Y, ZOOMS_DCT, SOUNDS_CACHE_PATH, SOUNDS_ALARMS_PATH
from os.path import join, isdir, isfile
from os import listdir
from my.text2speech import speak_a_random_alarm_message, fart_and_apologize, get_random_fart_fname, speak_a_random_hello_message
import datetime
from my.consts import OWNER_NAME
from my.classes import singleton
from my.tools.sound import stop_sounds, play_audiofile
from my.classes.exceptions import MissingFromCacheError
import random
from PyQt5.QtGui import QIcon

BASEDIR = os.path.dirname(__file__) # Base directory of me, the executable script
DEFAULT_CLOCK_NAME = list(FACES_DCT.keys())[-1]
VOICE_NAME = [f for f in listdir(SOUNDS_CACHE_PATH) if isdir(join(SOUNDS_CACHE_PATH, f))][0]
ALARMTONE_NAME = [f for f in listdir(SOUNDS_ALARMS_PATH) if isfile(join(SOUNDS_ALARMS_PATH, f))][0]
CLOCKFACE_NUMBER = random.randint(0, len(FACES_LST))

@singleton
class _MyQtSignals(QObject):
    setFace = pyqtSignal(str)
    freezeFace = pyqtSignal(str)
    showSettings = pyqtSignal()
    hideSettings = pyqtSignal()
    setJsTest = pyqtSignal(bool)
    setAlarm = pyqtSignal(str)

MyQtSignals = _MyQtSignals() 


def fork_me_right(myfunc):
    # Fork a child process
    processid = os.fork()
    if processid > 0 : # processid > 0 represents the parent process
        return
    else:
        myfunc()
        sys.exit(0)
  
  
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



class PickfaceWindow(QMainWindow):    
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(os.path.join(BASEDIR, "ui/clocks.ui"), self)
        make_background_translucent(self)
        self.randomizer_button.clicked.connect(self.pickface_at_random) # 'Choose Face' button was pushed

    def pickface_at_random(self):
        new_face = FACES_LST[CLOCKFACE_NUMBER]
        assert(len(FACES_LST) > 1)
        while new_face == FACES_LST[CLOCKFACE_NUMBER]: 
            new_face = random.choice(FACES_LST)
        if not os.path.exists(freezeframe_fname(new_face)): 
            print("Sorry. I don't have a freezeframe pic of %s; I'll load the clock face instead." % new_face)
            MyQtSignals.setFace.emit(new_face)
            MyQtSignals.hideSettings.emit()
        else:
            MyQtSignals.freezeFace.emit(new_face)
            
   
class AlarmsWindow(QMainWindow):    
    '''Choose which alarm'''
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(os.path.join(BASEDIR, "ui/alarms.ui"), self)
        make_background_translucent(self)
        path = SOUNDS_ALARMS_PATH
        [self.alarms_qlist.addItem(f,) for f in listdir(path) if isfile(join(path, f)) and f.endswith('.ogg')]
        [self.alarms_qlist.setCurrentItem(x) for x in self.alarms_qlist.findItems(ALARMTONE_NAME, Qt.MatchExactly)]
        self.alarms_qlist.currentTextChanged.connect(self.new_alarm_chosen)
        for q in (self.alarms_qlist, self.hour_qlist, self.minutesA_qlist, self.minutesB_qlist, self.ampm_qlist):
            enable_touchscroll(q)
        print("QQQ please add the 'scroller rounder-up' so that the selecting of a given hour/minute/second causes all dials to line up neatly.")
        
    def new_alarm_chosen(self, alarmtone):
        global ALARMTONE_NAME
        ALARMTONE_NAME = alarmtone
        stop_sounds()
        try:
            play_audiofile('%s/%s' % (SOUNDS_ALARMS_PATH, alarmtone), nowait=True)
        except FileNotFoundError:
            print("new_alarm_chosen() -- alarm sound file was not found. Therefore, I cannot play it.")()
        
    def setVisible(self, onoroff):
        stop_sounds()
        super().setVisible(onoroff)


class VoicesWindow(QMainWindow):    
    '''Choose which voice'''
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(os.path.join(BASEDIR, "ui/voices.ui"), self)
        make_background_translucent(self)
        self.randomizer_button.clicked.connect(self.voice_at_random)
        self.fart_button.clicked.connect(self.fart_button_clicked)
        self.hello_button.clicked.connect(self.hello_button_clicked)
        self.wakeup_button.clicked.connect(self.wakeup_button_clicked)
        _ = SOUNDS_CACHE_PATH
        # [self.voices_qlist.addItem(f,) for f in listdir(path) if isdir(join(path, f))]
        # [self.voices_qlist.setCurrentItem(x) for x in self.voices_qlist.findItems(VOICE_NAME, Qt.MatchExactly)]
        # self.voices_qlist.currentTextChanged.connect(self.new_voice_chosen)
        # enable_touchscroll(self.voices_qlist)

    def voice_at_random(self):
        print("RANDOM VOICE SELECTED")
        attempts = 0
        while attempts < 100:
            attempts += 1
            try:
                vox = random.choice([f for f in listdir(SOUNDS_CACHE_PATH) if isdir(join(SOUNDS_CACHE_PATH, f))])
                if vox != VOICE_NAME:
                    self.new_voice_chosen(vox)
                    break
            except:
                print("This voice failed. Trying another...")
        
    # def voicename_button_clicked(self):
    #     play_audiofile("""{cache}/{voice}/{owner}.mp3""".format(
    #                                         cache=SOUNDS_CACHE_PATH, voice=VOICE_NAME, owner=OWNER_NAME.lower()), 
    #                    nowait=True)    
    
    def fart_button_clicked(self):
        try:
            fart_and_apologize(VOICE_NAME)
        except MissingFromCacheError:
            play_audiofile(get_random_fart_fname(), nowait=True)
            
    def hello_button_clicked(self):
        try:
            speak_a_random_hello_message(owner=OWNER_NAME, voice=VOICE_NAME)
        except MissingFromCacheError:
            popup_message("Voice Missing", "Please pick a different voice.")

    def wakeup_button_clicked(self):
        try:
            speak_a_random_alarm_message(owner=OWNER_NAME, voice=VOICE_NAME, 
                                     hour=datetime.datetime.now().hour, minute=datetime.datetime.now().minute, 
                                     snoozed=False, fail_quietly=True)
        except MissingFromCacheError as e:
            popup_message("Voice Missing", "Please pick a different voice.")




    def new_voice_chosen(self, voice):
        global VOICE_NAME
        VOICE_NAME = voice
        play_audiofile("""{cache}/{voice}/{owner}.mp3""".format(
                                            cache=SOUNDS_CACHE_PATH, voice=VOICE_NAME, owner=OWNER_NAME.lower()), 
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
        self.configure_a_subwindow(PickfaceWindow, self.clocks_button)
        self.configure_a_subwindow(VoicesWindow, self.voices_button)
        self.configure_a_subwindow(TestingWindow,self.testing_button)
        self.configure_a_subwindow(BrightnessWindow, self.brightness_button)
        
    def configure_a_subwindow(self, a_class, a_button):
        a_window = a_class(self)
        a_window.parent_menubutton = a_button # The button that activates me
        a_window.hide()
        a_button.clicked.connect(lambda: self.choose_window(a_window))
        self.all_subwindows.append(a_window)
    
    def choose_window(self, chosen_subwindow=None):
        # Hide/show the chosen window (or, if no window was chosen, hide *all* windows)
        for w in self.all_subwindows:
            if w == chosen_subwindow:
                w.setVisible(not w.isVisible())
            else:
                w.hide()
        for w in self.all_subwindows:
            w.parent_menubutton.setVisible(False if chosen_subwindow is not None \
                                                and w != chosen_subwindow \
                                                and chosen_subwindow.isVisible() \
                                                else True)

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
        global CLOCKFACE_NUMBER
        self.setUpdatesEnabled(False)
        CLOCKFACE_NUMBER = FACES_LST.index(face_name)
        self.load_file('{cwd}/{relpath}'.format(cwd=os.getcwd(), relpath=FACES_DCT[face_name]))
        self.setZoomFactor(ZOOMS_DCT[face_name] if face_name in ZOOMS_DCT.keys() else 1)
        make_scrollbars_zeropixels_in_size(self)
        self.setUpdatesEnabled(True)

    def load_file(self, local_file):
        self.setZoomFactor(1) # Do this BEFORE loading file.
        the_url = 'file://{local_file}'.format(local_file=local_file)
        self.load(QUrl(the_url))
        make_scrollbars_zeropixels_in_size(self)

    def freeze_face(self, face_name):
        self.setUpdatesEnabled(False)
        global CLOCKFACE_NUMBER
        CLOCKFACE_NUMBER = FACES_LST.index(face_name)
        self.load_file(freezeframe_fname(face_name)) # Show the freezeframe
        self.setUpdatesEnabled(True)



class MainWindow(QMainWindow):
    """The main window for the PALPAC app.
    
    This will stack the clockface, its overlay window, and the configurator window.
    Then it hides the configurator window, leaving the overlay where it can be
    clicked. If the user tries to click on the clockface, they actually click on
    the overlay window, which will trigger the configurator window. Then, if the
    user clicks outside the configurator window, the overlay window will hide it
    again. That is how the clockface is clickable: it isn't, but the overlay
    window *is* clickable.

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
        MyQtSignals.setFace.emit(FACES_LST[CLOCKFACE_NUMBER])

    def show_settings_screen(self):
        '''Make the Settings screen the top widget. Behind it, show a freezeframe of the clockface.'''
        face_name = FACES_LST[CLOCKFACE_NUMBER]
        screenCaptureWidget(self, self.clockface.pos(), freezeframe_fname(face_name))
        MyQtSignals.freezeFace.emit(face_name)
        self.settings.show()
        self.our_layout.setCurrentWidget(self.settings)
        
    def hide_settings_screen(self):
        '''Hide the Settings screen. Go back to displaying an animated clockface.'''
        self.settings.hide()
        self.our_layout.setCurrentWidget(self.beard)
        MyQtSignals.setFace.emit(FACES_LST[CLOCKFACE_NUMBER])

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






