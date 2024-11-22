#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Sheepdip for a clock display.

Created on Aug 19, 2024

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

from my.classes.exceptions import MissingFromCacheError
from PyQt5 import uic
from PyQt5.QtCore import QUrl, Qt, QObject, pyqtSignal, QSize, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QStackedLayout, QWidget, QVBoxLayout, QDialog
from my.gui import BrowserView, set_vdu_brightness, set_audio_volume, make_background_translucent, screenCaptureWidget, make_scrollbars_zeropixels_in_size, popup_message
from my.globals import PATHNAMES_OF_CLOCKFACES, TOUCHSCREEN_SIZE_X, TOUCHSCREEN_SIZE_Y, ZOOMS_DCT, SOUNDS_CACHE_PATH, SOUNDS_ALARMS_PATH
from os.path import join, isdir, isfile
from os import listdir
from my.text2speech import fart_and_apologize, get_random_fart_fname, speak_this_smart_sentence
from my.text2speech import Text2SpeechSingleton as tts

from my.consts import OWNER_NAME, motivational_comments_lst, wannasnooze_msgs_lst, hello_owner_lst, alarm_messages_lst
from my import BASEDIR
from my.classes import singleton
import random
import pwd
from PyQt5.QtGui import QFont
from my.classes.stolenslider import StolenSlider
from my.gui.tenkey import TenkeyDialog
from my.stringutils import is_time_string_valid, is_date_string_valid
from datetime import datetime
from my.classes import ShuffledPlaylist

ALL_VOICES_PLS = ShuffledPlaylist([f for f in listdir(SOUNDS_CACHE_PATH) if isdir(join(SOUNDS_CACHE_PATH, f))])
VOICE_NAME = ALL_VOICES_PLS.next
ALARMTONES_PLS = ShuffledPlaylist([f for f in listdir(SOUNDS_ALARMS_PATH) if isfile(join(SOUNDS_ALARMS_PATH, f)) and f.endswith('.ogg')])
ALARMTONE_NAME = ALARMTONES_PLS.next
HELLO_OWNER_PLS = ShuffledPlaylist(hello_owner_lst)
MOTIVATIONAL_COMMENTS_PLS = ShuffledPlaylist(motivational_comments_lst)
ALARM_MSGS_PLS = ShuffledPlaylist(alarm_messages_lst)
WANNASNOOZE_MSGS_PLS = ShuffledPlaylist(wannasnooze_msgs_lst)
ALARM_TIME = None
CLOCKFACES_PLS = ShuffledPlaylist(PATHNAMES_OF_CLOCKFACES)
MY_CLOCKFACE = CLOCKFACES_PLS.next
BRIGHTNESS = 100
VOLUME = 8
SNOOZE_TIMER = QTimer()
SNOOZE_TIMER.timeout.connect(lambda x=True: Yo.triggerAlarm.emit(x))
# try:
from my.tools.sound import stop_sounds, play_audiofile, queue_oggfile, clear_ogg_queue
# except PygameStartupError as e:
#     popup_message(str(type(e)), "GET A FRICKIN' LOUDSPEAKER")
#     sys.exit(0)


@singleton
class _MyQtSignals(QObject):
    """Globally available class for triggering specific Qt-level signals for events such as:-
    - showing a specific clock face
    - taking a picture of the current clock face that's currently on display on the widget
    - show a specific image on the widget that usually displays a clock face
    - hide the Settings window
    - show the Settings window
    - trigger the ALARM (plus a 'You were snoozing' message...or not)
    """
    showClockFace = pyqtSignal(str)
    takePictureOfCurrentClockFace = pyqtSignal()
    showImage = pyqtSignal(str)
    showSettings = pyqtSignal()
    hideSettings = pyqtSignal()
    setJsTest = pyqtSignal(bool)
    triggerAlarm = pyqtSignal(bool)


Yo = _MyQtSignals()


def face_snapshot_fname(face_path):
    """Filename of the snapshot of the specific clock face.

    There are a dozen (or so) available clock faces. Each has a name. The name has
    a relative path -- see PATHNAMES_OF_CLOCKFACES -- associated with it. The path
    tends to be the path of the index.html file that displays the clock face.

    This function takes the path of a clock face's index.html file, derives a
    sensible pathname for the snapshot (a sample picture of the clock face), and
    returns it. This is the location where a snapshot will be saved... presumably
    by the code that called me.

    Args:
        face_path (int): The pathname of the clock face's index.html or whatever.

    Returns:
        str: The pathname of the file where a snapshot of this clock face should
            be saved.

    """
    homedir = pwd.getpwuid(os.getuid()).pw_dir
    assert('"' not in face_path)
    return('{home}/dotpalpac/thumbs/{faceish}.png'.format(home=homedir, faceish=face_path.replace('/', '_')))


def set_the_system_clock(year, month, day, hour, minute):
    cmd = '''sudo /usr/bin/date -s "%02d/%02d/%04d %02d:%02d"''' % (month, day, year, hour, minute)
    print("cmd = >>>%s<<<" % cmd)
    if 0 != os.system(cmd):
        print("Failed to run >>>%s<<<" % cmd)
        raise PermissionError("Unable to set time/date")


def trigger_alarm(snoozed):
#    global SNOOZE_TIMER
    SNOOZE_TIMER.stop()
    print("ALARM IS GOING OFF")
    set_vdu_brightness(100)
    wannasnooze, ok = WakeupDialog.getOutput(timestring=ALARM_TIME, snoozed=snoozed)
    if not ok:
        print("Somehow, you canceled the wakeup dialog")
    elif wannasnooze:
        print("QQQ WE ARE SNOOZING.")
        SNOOZE_TIMER.start(5 * 60 * 1000)  # Five minutes = 5 * 60 * 1000
        speak_this_smart_sentence(owner=OWNER_NAME, voice=VOICE_NAME, message_template=WANNASNOOZE_MSGS_PLS.next)
    else:
        print("So, I'm awake, then. Yay.")
    set_vdu_brightness(BRIGHTNESS)


class WakeupDialog(QDialog):
    '''
    classdocs
    '''

    def __init__(self, parent=None, timestring=None, snoozed=False):
        '''
        Constructor
        '''
        super().__init__(parent)
        self.wannasnooze = False
        uic.loadUi(os.path.join(BASEDIR, "ui/wakeup.ui"), self)
#        make_background_translucent(self)
        self.snooze_button.clicked.connect(self.you_pushed_wannasnooze)
        self.awake_button.clicked.connect(self.you_pushed_yesiamawake)
        if timestring is not None:
            self.time_label.setText('GET UP' if timestring is None else timestring)
        speak_this_smart_sentence(OWNER_NAME, VOICE_NAME, ALARM_MSGS_PLS.next)
        for _ in range(0, 64):
            queue_oggfile('%s/%s' % (SOUNDS_ALARMS_PATH, ALARMTONE_NAME))

    def you_pushed_wannasnooze(self):
        self.wannasnooze = True
        self.accept()

    def you_pushed_yesiamawake(self):
        self.wannasnooze = False
        self.accept()

    @staticmethod
    def getOutput(parent=None, timestring=None, snoozed=None):
        dialog = WakeupDialog(parent=parent, timestring=timestring, snoozed=snoozed)
        result = dialog.exec_()
        print("I AM %s" % ('GOING BACK TO SLEEP' if dialog.wannasnooze else 'AWAKE NOW'))
        clear_ogg_queue()
        return (dialog.wannasnooze, result == QDialog.Accepted)


class BrightnessWindow(QMainWindow):
    '''Set brightness'''

    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(os.path.join(BASEDIR, "ui/brightness.ui"), self)
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
        make_background_translucent(self)
        self.brightness_changed(BRIGHTNESS)
        self.slider.valueChanged.connect(self.brightness_changed)

    def brightness_changed(self, x):
        global BRIGHTNESS
        BRIGHTNESS = x
        set_vdu_brightness(x)

    def setVisible(self, onoroff):
        stop_sounds()
        super().setVisible(onoroff)


class VolumeWindow(QMainWindow):
    '''Set volume'''

    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(os.path.join(BASEDIR, "ui/volume.ui"), self)
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
        make_background_translucent(self)
        self.volume_changed(VOLUME)
        self.slider.valueChanged.connect(self.volume_changed)

    def volume_changed(self, x):
        global VOLUME
        VOLUME = x
        set_audio_volume(x)

    def setVisible(self, onoroff):
        stop_sounds()
        super().setVisible(onoroff)


class FaceDateTimeWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(os.path.join(BASEDIR, "ui/cfgclock.ui"), self)
        make_background_translucent(self)
        self.randomizer_button.clicked.connect(self.pickface_at_random)  # 'Choose Face' button was pushed
        self.currentdate_button.clicked.connect(self.set_current_date)
        self.currentyear_button.clicked.connect(self.set_current_year)
        self.currenttime_button.clicked.connect(self.set_current_time)
        self.currentdate_button.setStyleSheet('QPushButton {color: red;}')  # background-color: #A3C1DA;
        self.currentyear_button.setStyleSheet('QPushButton {color: red;}')  # background-color: #A3C1DA;
        self.currenttime_button.setStyleSheet('QPushButton {color: red;}')  # background-color: #A3C1DA;
        self.label.setStyleSheet('QLabel {background-color: #FFFFFF; color: red;}')
        self.year_str = None  # set by setVisible(), which calls self.get_current_date_and_time()
        self.date_str = None  # set by setVisible(), which calls self.get_current_date_and_time()
        self.time_str = None  # set by setVisible(), which calls self.get_current_date_and_time()

    def is_our_date_string_valid(self):
        return is_date_string_valid(self.currentyear_button.text(), self.currentdate_button.text())

    def is_our_time_string_valid(self):
        return is_time_string_valid(self.currenttime_button.text())

    def get_current_date_and_time(self):
        the_date = datetime.now()
        self.year_str = str(the_date.year)
        self.date_str = '%02d/%02d' % (the_date.month, the_date.day)
        self.time_str = '%02d:%02d' % (the_date.hour, the_date.minute)
        self.currentyear_button.setText(self.year_str)
        self.currentdate_button.setText(self.date_str)
        self.currenttime_button.setText(self.time_str)

    def pickface_at_random(self):
        global MY_CLOCKFACE
        if len(PATHNAMES_OF_CLOCKFACES) <= 1:
            print("Can't pick a clockface at random: there's only one available!")
        else:
            old_face_path = MY_CLOCKFACE
            while old_face_path == MY_CLOCKFACE:
                MY_CLOCKFACE = CLOCKFACES_PLS.next
            print("Random clockface chosen:", MY_CLOCKFACE.split('/')[2])
            Yo.showClockFace.emit(MY_CLOCKFACE)

    def set_system_clock(self):
        y = self.year_str
        d = self.date_str
        hh = self.time_str[:2]
        mm = self.time_str[3:]
        print("y =", y)
        print("d =", d)
        print("hh=", hh)
        print("mm=", mm)
        try:
            set_the_system_clock(year=int(y),
                            month=int(d[:2]),
                            day=int(d[3:]),
                            hour=int(hh),
                            minute=int(mm))
        except Exception as e:
            popup_message(str(type(e)), "I was unable to set the time and date.")
            self.get_current_date_and_time()
        except Exception as e:  # pylint: disable=broad-exception-caught
            popup_message(str(type(e)), "I failed to make the time/date stick: %s" % str(type(e)))
            self.get_current_date_and_time()

    def set_current_date(self):
        output, ok = TenkeyDialog.getOutput(formatstring='../..', minlen=4, maxlen=4)
        if not ok:
            print("Canceled the date-setter")
        elif self.is_our_date_string_valid():
            self.date_str = output
            self.currentdate_button.setText(output)
            self.set_system_clock()
        else:
            popup_message("Bad Date", "You specified a dodgy date.")

    def set_current_year(self):
        output, ok = TenkeyDialog.getOutput(formatstring='....', minlen=4, maxlen=4)
        if not ok:
            print("Canceled the year-setter")
        elif self.is_our_date_string_valid():
            self.year_str = output
            self.currentyear_button.setText(output)
            self.set_system_clock()
        else:
            popup_message("Bad Year", "You specified a dodgy year.")

    def set_current_time(self):
        output, ok = TenkeyDialog.getOutput(formatstring='..:..', minlen=4, maxlen=4)
        if not ok:
            print("Canceled the time-setter")
        elif self.is_our_time_string_valid():
            self.time_str = output
            self.currenttime_button.setText(output)
            self.set_system_clock()
        else:
            popup_message("Bad Time", "You specified a dodgy time.")

    def setVisible(self, onoroff):
        stop_sounds()
        self.get_current_date_and_time()
        super().setVisible(onoroff)


class AlarmsWindow(QMainWindow):
    '''Choose which alarm'''

    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(os.path.join(BASEDIR, "ui/alarms.ui"), self)
        make_background_translucent(self)
        self.already_playing = False
        self.randomizer_button.clicked.connect(self.alarm_at_random)
        self.alarmtime_button.clicked.connect(self.set_alarm_time)
        self.update_alarmtime_button_text()
        self.noof_randomizer_clicks = None  # This is reset in self.setVisible()
        self.alarmtime_button.setStyleSheet('QPushButton {background-color: #A3C1DA; color: red;}')

    def update_alarmtime_button_text(self):
        self.alarmtime_button.setText("(none)" if ALARM_TIME is None else ALARM_TIME)

    def stop_playing(self):
        stop_sounds()
        self.already_playing = False
        sz = self.randomizer_button.iconSize()
        self.randomizer_button.setIconSize(QSize(sz.width() // 2, sz.height() // 2))

    def alarm_at_random(self):
        global ALARMTONE_NAME
        self.noof_randomizer_clicks += 1
        if ALARMTONES_PLS.length <= 1:
            print("Can't pick an alarmtone at random: there's only one available!")
        elif self.already_playing:
            self.stop_playing()
        else:
            sz = self.randomizer_button.iconSize()
            self.randomizer_button.setIconSize(QSize(sz.width() * 2, sz.height() * 2))
            if self.noof_randomizer_clicks > 1:
                old_name = ALARMTONE_NAME
                while old_name == ALARMTONE_NAME:
                    ALARMTONE_NAME = ALARMTONES_PLS.next
                print("New alarm chosen", ALARMTONE_NAME)
            try:
                play_audiofile('%s/%s' % (SOUNDS_ALARMS_PATH, ALARMTONE_NAME), nowait=True)
                self.already_playing = True
            except FileNotFoundError:
                print("alarm_at_random() -- alarm sound file was not found. Therefore, I cannot play it.")

    def set_alarm_time(self):
        global ALARM_TIME
        output, ok = TenkeyDialog.getOutput(formatstring='..:..', minlen=4, maxlen=4)
        if not ok:
            print("Canceled the alarm")
            ALARM_TIME = None
        elif not is_time_string_valid(output):
            popup_message("Bad Time", "You specified a dodgy time.")
        else:
            ALARM_TIME = output
        self.update_alarmtime_button_text()

    def setVisible(self, onoroff):
        if self.already_playing:
            self.stop_playing()
        self.noof_randomizer_clicks = 0
        super().setVisible(onoroff)


class VoicesWindow(QMainWindow):
    '''Choose which voice'''

    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi(os.path.join(BASEDIR, "ui/voices.ui"), self)
        make_background_translucent(self)
        self.fart_button.clicked.connect(self.fart_button_clicked)
        self.hello_button.clicked.connect(self.hello_button_clicked)
        self.wakeup_button.clicked.connect(self.wakeup_button_clicked)
        self.randomizer_button.clicked.connect(self.voice_at_random)
        self.shrek_button.clicked.connect(self.shrek_button_clicked)
        _ = SOUNDS_CACHE_PATH

    def voice_at_random(self):
        attempts = 0
        while attempts < 1000:
            attempts += 1
            vox = "???"
            try:
                vox = ALL_VOICES_PLS.next  # random.choice([f for f in listdir(SOUNDS_CACHE_PATH) if isdir(join(SOUNDS_CACHE_PATH, f))])
                if vox != VOICE_NAME:
                    self.new_voice_chosen(vox)
                    break
            except Exception as _:  # pylint: disable=broad-exception-caught
                print("This voice >>>%s<<< failed. Trying another..." % vox)
        print("Random voice >>>%s<<< selected" % vox)

    def shrek_button_clicked(self):
        stop_sounds()
        try:
            speak_this_smart_sentence(OWNER_NAME, VOICE_NAME, MOTIVATIONAL_COMMENTS_PLS.next)
        except MissingFromCacheError:
            self.fart_button_clicked()

    def fart_button_clicked(self):
        stop_sounds()
        try:
            fart_and_apologize(VOICE_NAME)
        except MissingFromCacheError:
            play_audiofile(get_random_fart_fname(), nowait=True)

    def hello_button_clicked(self):
        stop_sounds()
        try:
            speak_this_smart_sentence(OWNER_NAME, VOICE_NAME, HELLO_OWNER_PLS.next)
        except MissingFromCacheError:
            popup_message("Voice Missing", "Please pick a different voice.")

    def wakeup_button_clicked(self):
        stop_sounds()
        try:
            speak_this_smart_sentence(OWNER_NAME, VOICE_NAME, ALARM_MSGS_PLS.next)
        except MissingFromCacheError as _:
            popup_message("Voice Missing", "Please pick a different voice.")

    def new_voice_chosen(self, voice):
        global VOICE_NAME
        VOICE_NAME = voice
        play_audiofile("""{cache}/{voice}/{owner}.mp3""".format(
                                            cache=SOUNDS_CACHE_PATH, voice=VOICE_NAME, owner=OWNER_NAME.lower()),
                       nowait=True)

    def setVisible(self, onoroff):
        stop_sounds()
        super().setVisible(onoroff)


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
#        global ALARM_TIME
        if true_or_false is True:
            print("START button was clicked")
#            the_date = datetime.now()
#            ALARM_TIME = '%02d:%02d' % (the_date.hour, the_date.minute)
            Yo.triggerAlarm.emit(False)
        else:
            print("STOP button was clicked")
            Yo.triggerAlarm.emit(True)
#            self.parent.clockface.load_file(os.path.abspath('ui/icons/The_human_voice-1316067424.jpg'))

    def setVisible(self, onoroff):
        stop_sounds()
        super().setVisible(onoroff)


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
                        self.configure_a_subwindow(FaceDateTimeWindow, self.faces_button),
                        self.configure_a_subwindow(BrightnessWindow, self.brightness_button),
#                        self.configure_a_subwindow(TestingWindow, self.testing_button),
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

    def setVisible(self, onoroff):
        stop_sounds()
        if onoroff is False:
            self.choose_window(None)  # No subwindow was chosen. Therefore, this will hide all of them.
        super().setVisible(onoroff)

#     def hide(self):
# #        stop_sounds()
#         super().hide()


class ClockFace(BrowserView):
    """The browser widget in which the JavaScript clock is displayed.

    This clockface displays whichever clockface it's told to display. The
    files are stored locally and probably in a nearby directory. That's
    why it accepts a local path for load() and turns it into a QUrl(file:///)
    etc. etc.

    Accepted signals:
        showClockFace
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

    def setVisible(self, onoroff):
        stop_sounds()
        super().setVisible(onoroff)


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
        self.alarmchecker_timer = QTimer()
        self.alarmchecker_timer.timeout.connect(self.check_timer)
        self.alarmchecker_timer.start(1000)
        self.beard = QLabel("")  # This label (which is invisible) is *stacked* in front of the clock, making it clickable.
        self.clockface = ClockFace(self)  # The clock itself, on display
        self.settings = SettingsWindow(self)  # The configuration window that appears when the user clicks on the beard/clock.
        [self.our_layout.addWidget(w) for w in (self.clockface, self.beard, self.settings)]  # pylint: disable=expression-not-assigned
        self.our_layout.setCurrentWidget(self.beard)
        self.our_layout.setStackingMode(QStackedLayout.StackAll)  # Ensure that ALL the stack is visible at once.
        i_am_not_sure_what_this_is_for = QWidget()
        i_am_not_sure_what_this_is_for.setLayout(self.our_layout)
        self.setCentralWidget(i_am_not_sure_what_this_is_for)
        make_background_translucent(self.beard)
        self.hide_settings_screen()  # ...which also emits the clockface
        print("Initial clockface is....", MY_CLOCKFACE.split('/')[2])
        Yo.hideSettings.connect(self.hide_settings_screen)
        Yo.showSettings.connect(self.show_settings_screen)
        Yo.triggerAlarm.connect(trigger_alarm)
        Yo.takePictureOfCurrentClockFace.connect(self.take_picture_of_current_clock_face)

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
            self.show_settings_screen()  #            Yo.showSettings.emit()
        else:
            self.hide_settings_screen()  #            Yo.hideSettings.emit()
        super().mousePressEvent(event)

    def check_timer(self):
#        print("CHECKING TIMER")
        self.alarmchecker_timer.start(2000)
        the_date = datetime.now()
        if ALARM_TIME == '%02d:%02d' % (the_date.hour, the_date.minute):
            self.alarmchecker_timer.stop()
            Yo.triggerAlarm.emit(False)
            self.alarmchecker_timer.start(58000)  # A minute *after* the alarm time has passed, we'll resume timer-checking. This does not affect the Snooze function.


if __name__ == '__main__':
    if tts is not None:  # This means we're connected to the Internet. In that case, we're probably running on a Mac Mini (not a PALPAC unit)
        os.system("rm %s/*.png" % os.path.dirname(face_snapshot_fname("foo")))
    os.environ["QV4_JIT_CALL_THRESHOLD"] = "1"
    app = QApplication(sys.argv)
    mainwin = MainWindow()
    mainwin.show()
    app.exec_()

