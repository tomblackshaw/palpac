#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Sheepdip for a clock display.

Created on Aug 19, 2024
Updated on Nov 05, 2024

@author: Tom Blackshaw

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
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QStackedLayout, QWidget, QVBoxLayout

from my.gui import BrowserView, set_vdu_brightness, set_audio_volume, make_background_translucent, \
                screenCaptureWidget, make_scrollbars_zeropixels_in_size, enable_touchscroll, popup_message
from my.globals import PATHNAMES_OF_CLOCKFACES, TOUCHSCREEN_SIZE_X, TOUCHSCREEN_SIZE_Y, ZOOMS_DCT, SOUNDS_CACHE_PATH, SOUNDS_ALARMS_PATH
from os.path import join, isdir, isfile
from os import listdir
from my.text2speech import speak_a_random_alarm_message, fart_and_apologize, get_random_fart_fname, speak_a_random_hello_message
from my.text2speech import Text2SpeechSingleton as tts
import datetime
from my.consts import OWNER_NAME
from my.classes import singleton
from my.tools.sound import stop_sounds, play_audiofile
from my.classes.exceptions import MissingFromCacheError
import random
import pwd
import time
from PyQt5.QtGui import QFont
from my.classes.stolenslider import StolenSlider

BASEDIR = os.path.dirname(__file__)  # Base directory of me, the executable script
VOICE_NAME = [f for f in listdir(SOUNDS_CACHE_PATH) if isdir(join(SOUNDS_CACHE_PATH, f))][0]
ALARMTONE_NAME = [f for f in listdir(SOUNDS_ALARMS_PATH) if isfile(join(SOUNDS_ALARMS_PATH, f))][0]
MY_CLOCKFACE = random.choice(PATHNAMES_OF_CLOCKFACES)
BRIGHTNESS = 100
VOLUME = 8


@singleton
class _MyQtSignals(QObject):
    showClockFace = pyqtSignal(str)
    takePictureOfCurrentClockFace = pyqtSignal()
    showImage = pyqtSignal(str)
    showSettings = pyqtSignal()
    hideSettings = pyqtSignal()
    setJsTest = pyqtSignal(bool)
    setAlarm = pyqtSignal(str)


Yo = _MyQtSignals()


def face_snapshot_fname(face_path):
    homedir = pwd.getpwuid(os.getuid()).pw_dir
    assert('"' not in face_path)
    return('{home}/dotpalpac/thumbs/{faceish}.png'.format(home=homedir, faceish=face_path.replace('/', '_')))


class BrightnessWindow(QMainWindow):
    '''Set brightness'''

    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(os.path.join(BASEDIR, "ui/brightness.ui"), self)
        self.timer = None
        self.slider = StolenSlider(self)
        self.slider.setRange(1, 100)
        self.slider.setSingleStep(20)
        self.slider.setDecimals(0)
        self.slider.setFloat(False)
        self.slider.setSuffix("%")
        self.slider.setValue(BRIGHTNESS)
        font = QFont()
        font.setFamily('Times')
        font.setPointSize(24)
        font.setBold(True)
        self.slider.setFont(font)
        layout = QVBoxLayout()
        layout.addWidget(self.slider)
        self.central_widget.setLayout(layout)
#        self.slider_frame.setCentralWidget(self.slider)
#        self.setCentralWidget(self.slider)
        # self.slider_1.setMinimumWidth(100)
        # self.slider_1.setFixedHeight(18)
        make_background_translucent(self)
        self.brightness_changed(BRIGHTNESS)
        self.slider.valueChanged.connect(self.brightness_changed)

    def brightness_changed(self, x):
        global BRIGHTNESS
        BRIGHTNESS = x
        set_vdu_brightness(x)


class VolumeWindow(QMainWindow):
    '''Set volume'''

    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(os.path.join(BASEDIR, "ui/volume.ui"), self)
        self.timer = None
        self.slider = StolenSlider(self)
        self.slider.setRange(1, 11)
        self.slider.setSingleStep(1)
        self.slider.setDecimals(0)
        self.slider.setFloat(False)
        self.slider.setSuffix("")
        self.slider.setValue(BRIGHTNESS)
        font = QFont()
        font.setFamily('Times')
        font.setPointSize(24)
        font.setBold(True)
        self.slider.setFont(font)
        layout = QVBoxLayout()
        layout.addWidget(self.slider)
        self.central_widget.setLayout(layout)
#        self.slider_frame.setCentralWidget(self.slider)
#        self.setCentralWidget(self.slider)
        # self.slider_1.setMinimumWidth(100)
        # self.slider_1.setFixedHeight(18)
        make_background_translucent(self)
        self.volume_changed(VOLUME)
        self.slider.valueChanged.connect(self.volume_changed)

    def volume_changed(self, x):
        global VOLUME
        VOLUME = x
        set_audio_volume(x)


class PickfaceWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(os.path.join(BASEDIR, "ui/cfgclock.ui"), self)
        make_background_translucent(self)
        self.randomizer_button.clicked.connect(self.pickface_at_random)  # 'Choose Face' button was pushed

    def pickface_at_random(self):
        global MY_CLOCKFACE
        if len(PATHNAMES_OF_CLOCKFACES) <= 1:
            print("Can't pick a clockface at random: there's only one available!")
            return
        old_face_path = MY_CLOCKFACE
        while old_face_path == MY_CLOCKFACE:
            MY_CLOCKFACE = random.choice(PATHNAMES_OF_CLOCKFACES)
        print("Random clockface chosen:", MY_CLOCKFACE.split('/')[2])
        Yo.showClockFace.emit(MY_CLOCKFACE)


class AlarmsWindow(QMainWindow):
    '''Choose which alarm'''

    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(os.path.join(BASEDIR, "ui/alarms.ui"), self)
        make_background_translucent(self)
        path = SOUNDS_ALARMS_PATH
        [self.alarms_qlist.addItem(f) for f in listdir(path) if isfile(join(path, f)) and f.endswith('.ogg')]  # pylint: disable=expression-not-assigned
        [self.alarms_qlist.setCurrentItem(x) for x in self.alarms_qlist.findItems(ALARMTONE_NAME, Qt.MatchExactly)]  # pylint: disable=expression-not-assigned
        for q in (self.alarms_qlist, self.hour_qlist, self.minutesA_qlist, self.minutesB_qlist, self.ampm_qlist):
            enable_touchscroll(q)
        self.alarms_qlist.currentTextChanged.connect(self.new_alarm_chosen)

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
        self.fart_button.clicked.connect(self.fart_button_clicked)
        self.hello_button.clicked.connect(self.hello_button_clicked)
        self.wakeup_button.clicked.connect(self.wakeup_button_clicked)
        make_background_translucent(self)
        _ = SOUNDS_CACHE_PATH
        self.randomizer_button.clicked.connect(self.voice_at_random)

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
            except Exception as e:
                print("This voice failed. Trying another...")

    def fart_button_clicked(self):
        stop_sounds()
        try:
            fart_and_apologize(VOICE_NAME)
        except MissingFromCacheError:
            play_audiofile(get_random_fart_fname(), nowait=True)

    def hello_button_clicked(self):
        stop_sounds()
        try:
            speak_a_random_hello_message(owner=OWNER_NAME, voice=VOICE_NAME)
        except MissingFromCacheError:
            popup_message("Voice Missing", "Please pick a different voice.")

    def wakeup_button_clicked(self):
        stop_sounds()
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
        Yo.setJsTest.connect(self.js_test_button_clicked)
        self.stopjs_button.clicked.connect(lambda: Yo.setJsTest.emit(False))
        self.startjs_button.clicked.connect(lambda: Yo.setJsTest.emit(True))

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
        self.all_subwindows = [
                        self.configure_a_subwindow(AlarmsWindow, self.alarms_button),
                        self.configure_a_subwindow(VoicesWindow, self.voices_button),
                        self.configure_a_subwindow(VolumeWindow, self.volume_button),
                        self.configure_a_subwindow(TestingWindow, self.testing_button),
                        self.configure_a_subwindow(PickfaceWindow, self.faces_button),
                        self.configure_a_subwindow(BrightnessWindow, self.brightness_button)
                        ]

    def configure_a_subwindow(self, a_class, a_button):
        a_window = a_class(self)
        a_window.menubutton = a_button  # The button that activates me
        a_window.hide()
        a_button.clicked.connect(lambda: self.choose_window(a_window))
        return(a_window)

    def choose_window(self, chosen_subwindow=None):
        '''User has clicked on a Settings icon for a specific window (or in an area w/ no icon at all).

        If the user clicks on a Settings icon for a specific window:-
        * Show/hide that window.
        * Hide all icons (except the window's select-me icon) if the window is now visible.
        * Show all icons if the window is now invisible.

        If the user clicks on an area w/ no icon at all:-
        * Hide all windows.
        * Hide all icons.

        '''
        visibility_of_chosen_subwindow = None if chosen_subwindow is None else chosen_subwindow.isVisible()
        # First, hide ALL subwindows *and* their icons (one per subwindow, as presented on the Settings window).
        for w in self.all_subwindows:
            w.menubutton.setVisible(False)  # Hide the Settings menu button that (de)activates the subwindow 'w'
            w.setVisible(False)  # Hide the subwindow 'w'
        # Second, if appropriate, show a specific subwindow and its icon.
        if chosen_subwindow is not None and visibility_of_chosen_subwindow is False:
            chosen_subwindow.setVisible(True)
            chosen_subwindow.menubutton.setVisible(True)
            chosen_subwindow.activateWindow()
        # Third, if there *is* no specific subwindow, display all icons.
        else:
            for w in self.all_subwindows:
                w.menubutton.setVisible(True)

    def hide(self):
        self.choose_window(None)  # No subwindow was chosen. Therefore, this will hide all of them.
        super().hide()


class ClockFace(BrowserView):
    """The browser widget in which the JavaScript clock is displayed.

    This clockface displays whichever clockface it's told to display. The
    files are stored locally and probably in a nearby directory. That's
    why it accepts a local path for load() and turns it into a QUrl(file:///)
    etc. etc.

    Accepted signals:
        setFace
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.previous_shown_file = None
        Yo.showImage.connect(self.show_image)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(TOUCHSCREEN_SIZE_X, TOUCHSCREEN_SIZE_Y)
        Yo.showClockFace.connect(self.show_clockface)

    def show_clockface(self, face_path):
        self.setUpdatesEnabled(False)
        self.load_file('{cwd}/{relpath}'.format(cwd=os.getcwd(), relpath=face_path))
        self.setZoomFactor(ZOOMS_DCT[face_path] if face_path in ZOOMS_DCT.keys() else 1)
        make_scrollbars_zeropixels_in_size(self)
        self.setUpdatesEnabled(True)

    def load_file(self, local_file):
        self.setZoomFactor(1)  # Do this BEFORE loading file.
        the_url = 'file://{local_file}'.format(local_file=local_file)
        if self.previous_shown_file != the_url:
            self.load(QUrl(the_url))
            self.previous_shown_file = the_url
            make_scrollbars_zeropixels_in_size(self)

    def show_image(self, local_file):
        self.setUpdatesEnabled(False)
        print("Loading             ", MY_CLOCKFACE.split('/')[2])
        self.load_file(local_file)
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
        self.beard = QLabel("")  # This label (which is invisible) is *stacked* in front of the clock, making it clickable.
        self.clockface = ClockFace(self)  # The clock itself, on display
        self.settings = SettingsWindow(self)  # The configuration window that appears when the user clicks on the beard/clock.
        make_background_translucent(self.beard)
        [self.our_layout.addWidget(w) for w in (self.clockface, self.beard, self.settings)]  # pylint: disable=expression-not-assigned
        self.our_layout.setCurrentWidget(self.beard)
        self.our_layout.setStackingMode(QStackedLayout.StackAll)  # Ensure that ALL the stack is visible at once.
        i_am_not_sure_what_this_is_for = QWidget()
        i_am_not_sure_what_this_is_for.setLayout(self.our_layout)
        self.setCentralWidget(i_am_not_sure_what_this_is_for)
        print("Initial clockface is....", MY_CLOCKFACE.split('/')[2])
        Yo.hideSettings.connect(self.hide_settings_screen)
        Yo.showSettings.connect(self.show_settings_screen)
        Yo.takePictureOfCurrentClockFace.connect(self.take_picture_of_current_clock_face)
        self.hide_settings_screen()  # ...which also emits the clockface

    def take_picture_of_current_clock_face(self):
#        print("Taking a snapshot of the", MY_CLOCKFACE.split('/')[2])
        os.system('''mkdir -p "%s"''' % os.path.dirname(face_snapshot_fname(MY_CLOCKFACE)))
        screenCaptureWidget(self, self.clockface.pos(), face_snapshot_fname(MY_CLOCKFACE))

    def show_settings_screen(self):
        '''Make the Settings screen the top widget. Behind it, show a snapshot of the clockface.'''
        print("SHOW SETTINGS SCREEN")
        self.take_picture_of_current_clock_face()
        Yo.showImage.emit(face_snapshot_fname(MY_CLOCKFACE))
        self.settings.show()
        self.our_layout.setCurrentWidget(self.settings)

    def hide_settings_screen(self):
        '''Hide the Settings screen. Go back to displaying an animated clockface.'''
        self.our_layout.setCurrentWidget(self.beard)
        print("HIDING SETTINGS SCREEN")
        self.settings.hide()
        Yo.showClockFace.emit(MY_CLOCKFACE)

    def mousePressEvent(self, event):
        '''If the user clicks on the beard that covers the clockface, let's launch the Settings window; otherwise, let's hide it.'''
        if self.our_layout.currentWidget() == self.beard:
            Yo.showSettings.emit()
        else:
            Yo.hideSettings.emit()
        super().mousePressEvent(event)


if __name__ == '__main__':
    if tts is not None:  # This means we're connected to the Internet. In that case, we're probably running on a Mac Mini (not a PALPAC unit)
        os.system("timedatectl set-ntp false")  # stop auto-update of time&date
        os.system("rm %s/*.png" % os.path.dirname(face_snapshot_fname("foo")))
    app = QApplication(sys.argv)
    mainwin = MainWindow()
    mainwin.show()
    app.exec_()

