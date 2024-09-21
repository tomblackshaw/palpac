#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Sheepdip for a clock display.

This module contains classes and a main function to display a Javascript-based
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
from PyQt5.QtCore import QUrl, Qt, QObject, pyqtSignal, QPoint, QEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QSizePolicy, QLabel, QStackedLayout, QWidget

from my.gui import set_vdu_brightness, set_audio_volume, make_background_translucent
from my.globals import FACES_DCT, TOUCHSCREEN_SIZE_X, TOUCHSCREEN_SIZE_Y, ZOOMS_DCT
import time

from my.gui import Browser
BASEDIR = os.path.dirname(__file__) # Base directory of me, the executable script
DEFAULT_CLOCK_NAME = 'braun' # list(FACES_DCT.keys())[0]
# find ui | grep index.html | grep -v /src/ | grep -v original





class ConfiguratorWindow(QMainWindow):
    """The configurator window, with which the clock is reconfigured/adjusted.

    This subclass is instanced (instantiated?) once. Its instance is displayed
    whenever the user clicks on the clock (or rather, on the invisible window
    in front of the clock). It lets the user adjust the time, date, volume,
    screen brightness, etc.
    
    When the user adjusts the volume or brightness, those changes are made
    instantly by calling the appropriate subroutine.
    
    When a different *clock face* is chosen, that's different. A signal is sent
    to the clock face itself.

    """    
    def __init__(self, clockface):
        super().__init__()
        self.clockface = clockface
        uic.loadUi(os.path.join(BASEDIR, "ui/configuratorwindow.ui"), self)
        self.setAttribute(Qt.WA_TranslucentBackground)  # Turn background of window transparent
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.sliBrightness.valueChanged.connect(set_vdu_brightness)
        self.sliVolume.valueChanged.connect(set_audio_volume)
        [self.lswFaces.addItem(k) for k in FACES_DCT.keys()]
        self.lswFaces.currentTextChanged.connect(lambda x: self.clockface.changeFace.emit(x)) 
        [self.lswFaces.setCurrentItem(x) for x in self.lswFaces.findItems(DEFAULT_CLOCK_NAME, Qt.MatchExactly)]
        self.show()
        
    def clicked(self):
        print("Configuration window -- hiding!")
        self.hide()


class ClockFace(Browser):
    changeFace = pyqtSignal(str)
    def __init__(self):
        super().__init__()
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
    # FIXME: WRITE THESE DOX
    def __init__(self, parent=None):
        super().__init__(parent)
        self.our_layout = QStackedLayout()
        self.clockface = ClockFace()
        self.clockface.load(DEFAULT_CLOCK_NAME)
        self.config_win = ConfiguratorWindow(self.clockface)
        self.clockbeard = QLabel("") # This label (which is invisible) is *stacked* in front of the clock, making it clickable.
        make_background_translucent(self.clockbeard)
        for w in (self.config_win, self.clockface, self.clockbeard):
            self.our_layout.addWidget(w)
        self.our_layout.setCurrentWidget(self.clockbeard)
        self.our_layout.setStackingMode(QStackedLayout.StackAll) # Ensure that ALL the stack is visible at once.
        strawman = QWidget()
        strawman.setLayout(self.our_layout)
        self.setCentralWidget(strawman) # Apparently, it's necessary to create a straw-man widget and give it this burden.

    def mousePressEvent(self, event):
        if self.our_layout.currentWidget() == self.clockbeard:
            self.our_layout.setCurrentWidget(self.config_win)
            self.config_win.show()
        else:
            self.config_win.hide()
            self.our_layout.setCurrentWidget(self.clockbeard)
        super().mousePressEvent(event)


if __name__ == '__main__':
#os.system('''mpv audio/startup.mp3 &''')
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec_()




