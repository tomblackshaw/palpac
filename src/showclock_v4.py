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

Todo:
    * For module TODOs
    * You have to also use ``sphinx.ext.todo`` extension

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import os
import sys

from PyQt5 import uic
from PyQt5.QtCore import QUrl, Qt, QObject, pyqtSignal, QPoint, QEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QSizePolicy

from my.gui import set_vdu_brightness, set_audio_volume, make_entire_window_transparent, set_background_translucent
from my.globals import FACES_DCT, TOUCHSCREEN_SIZE_X, TOUCHSCREEN_SIZE_Y, FACETWEAKS_DCT
import time
from showclock_v2 import DEFAULT_CLOCK_NAME

# Each PyQt5 installation has EITHER a QWebView OR a QWebEngineView, depending on the OS. For example,
# MacOS Sonoma appears to have a QWebEngineView whereas Debian Buster has a QWebView. It's possible to
# use either (in my case) because I use only the most rudimentary features of each/both instance. 
try:
    from PyQt5.QtWebKitWidgets import QWebView as Browser
except ImportError:
    from PyQt5.QtWebEngineWidgets import QWebEngineView as Browser

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
        set_background_translucent(self)
        self.sliBrightness.valueChanged.connect(set_vdu_brightness)
        self.sliVolume.valueChanged.connect(set_audio_volume)
        [self.lswFaces.addItem(k) for k in FACES_DCT.keys()]
        self.lswFaces.currentTextChanged.connect(lambda x: self.clockface.changeFace.emit(x)) 
        [self.lswFaces.setCurrentItem(x) for x in self.lswFaces.findItems(DEFAULT_CLOCK_NAME, Qt.MatchExactly)]
        self.setFixedSize(TOUCHSCREEN_SIZE_X, TOUCHSCREEN_SIZE_Y)
        self.move(0, 0)
        self.clickme = OverlayWindow(func_when_clicked=self.clicked)
        
    def clicked(self):
        self.setVisible(not self.isVisible())


class OverlayWindow(QMainWindow):
    def __init__(self, func_when_clicked):
        super().__init__()
        self.func_when_clicked = func_when_clicked
        make_entire_window_transparent(self)
        self.setFixedSize(TOUCHSCREEN_SIZE_X, TOUCHSCREEN_SIZE_Y)
        self.move(0, 0)
        self.show()
        self.raise_() # Ensure that I appear *in front of* the ClockFace
        
    def mousePressEvent(self, event):
        self.func_when_clicked()
        super().mousePressEvent(event)




class ClockFace(Browser):
    changeFace = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.changeFace.connect(self.load)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(TOUCHSCREEN_SIZE_X, TOUCHSCREEN_SIZE_Y)
        self.move(0, 0)
        self.show()
        self.old_x = 0
        self.old_y = 0
        self.loadFinished.connect(self.adjust_zoom_etc)


    def load(self, face_name):
        self.face_name = face_name
        self.setWindowOpacity(0.1)
        self.setZoomFactor(1)
        self.scroll(-self.old_x, -self.old_y)
        super().load(QUrl('file://{cwd}/{relpath}'.format(cwd=os.getcwd(), relpath=FACES_DCT[face_name])))
        self.setStyleSheet('QScrollBar {height:0px;}; QScrollBar {width:0px;}')  # Turn background transparent too
        
    def adjust_zoom_etc(self, _ok_or_nah):
        x, y, zoom = FACETWEAKS_DCT[self.face_name] if self.face_name in FACETWEAKS_DCT.keys() else (0, 0, 1)
        self.scroll(x, y)
        self.old_x = x 
        self.old_y = y 
        self.setZoomFactor(zoom)
        self.setWindowOpacity(1.0)
        self.setStyleSheet('QScrollBar {height:0px;}; QScrollBar {width:0px;}')  # Turn background transparent too



class ClickableClockFace(Browser):
    """
    A subclass of the QMainWindow with the eventFilter method.
    """

    def __init__(self):
        super().__init__() # super(ClockFace, self)
    
    def eventFilter(self, obj, event):
        if event.type() == QEvent.TouchBegin:  # Catch the TouchBegin event.
            print('We have a touch begin')
            return True
        elif event.type() == QEvent.TouchEnd:  # Catch the TouchEnd event.
            print('We have a touch end')
            return True        
        return super().eventFilter(obj, event)
    
    
# class ClockFace(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.b = ClkBrowser()
#         self.layout = QVBoxLayout()
#         self.layout.addWidget(self.b)
#         self.setCentralWidget(self.b)
#         self.setWindowFlags(Qt.FramelessWindowHint)
#         self.setStyleSheet('QWidget{background: #000000}')  # Turn background transparent too
#         self.setFixedSize(TOUCHSCREEN_SIZE_X, TOUCHSCREEN_SIZE_Y)
#         self.move(0, 0)
#         self.show()

if __name__ == '__main__':
#os.system('''mpv audio/startup.mp3 &''')
    app = QApplication(sys.argv)
    clockface = ClickableClockFace()
    #clockface.load(DEFAULT_CLOCK_NAME)
    clockface.load(FACES_DCT[DEFAULT_CLOCK_NAME])
    clockface.show()
    #win = ConfiguratorWindow(clockface=ClickableClockFace())
    #win.hide()
    app.exec_()





