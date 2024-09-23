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

from my.gui import Browser
BASEDIR = os.path.dirname(__file__) # Base directory of me, the executable script
DEFAULT_CLOCK_NAME = 'braun' # list(FACES_DCT.keys())[0]
# find ui | grep index.html | grep -v /src/ | grep -v original







class SetBrightnessWindow(QMainWindow):    
    def __init__(self):
        super().__init__()

        uic.loadUi(os.path.join(BASEDIR, "ui/setbrightness.ui"), self)
        make_background_translucent(self)
        


class SetVolumeWindow(QMainWindow):    
    def __init__(self):
        super().__init__()

        uic.loadUi(os.path.join(BASEDIR, "ui/setvolume.ui"), self)
        make_background_translucent(self)

        


class ChooseClockfaceWindow(QMainWindow):    
    def __init__(self):
        super().__init__()

        uic.loadUi(os.path.join(BASEDIR, "ui/chooseclockface.ui"), self)
        make_background_translucent(self)





class ConfiguratorWindow(QMainWindow):    
    def __init__(self):
        super().__init__()

        uic.loadUi(os.path.join(BASEDIR, "ui/configuratorwindow.ui"), self)
        make_background_translucent(self)






class ClockFace(Browser):
    """The browser widget in which the JavaScript clock is displayed.
    
    This clockface displays whichever clockface it's told to display. The
    files are stored locally and probably in a nearby directory. That's
    why it accepts a local path for load() and turns it into a QUrl(file:///)
    etc. etc.

    """
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
        self.settings = ConfiguratorWindow() # The configuration window that appears when the user clicks on the beard/clock.
        make_background_translucent(self.beard)
        for w in (self.clockface, self.beard, self.settings):
            self.our_layout.addWidget(w)
        self.our_layout.setCurrentWidget(self.beard)
        self.our_layout.setStackingMode(QStackedLayout.StackAll) # Ensure that ALL the stack is visible at once.
        strawman = QWidget()
        strawman.setLayout(self.our_layout)
        self.setCentralWidget(strawman)
        self.settings.hide()
        self.settings.volume_button.clicked.connect(self.volume_button_clicked)
        self.settings.brightness_button.clicked.connect(self.brightness_button_clicked)
        self.settings.clocks_button.clicked.connect(self.clocks_button_clicked)
        self.volume_widget = SetVolumeWindow()
        self.brightness_widget = SetBrightnessWindow()
        self.clocks_widget = ChooseClockfaceWindow()
        
    def volume_button_clicked(self):
        print("VOLUME")
        self.volume_widget.setVisible(not self.volume_widget.isVisible())
        self.brightness_widget.hide()
        self.clocks_widget.hide()
        
        
    def brightness_button_clicked(self):
        print("BRIGHTNESS")
        self.volume_widget.hide()
        self.brightness_widget.setVisible(not self.brightness_widget.isVisible())
        self.clocks_widget.hide()
        
    def clocks_button_clicked(self):
        print("CLOCKS ")
        self.volume_widget.hide()
        self.brightness_widget.hide()
        self.clocks_widget.setVisible(not self.clocks_widget.isVisible())

    def mousePressEvent(self, event):
        if self.our_layout.currentWidget() == self.beard:
            print("Activating the settings screen")
            self.settings.show()
            self.our_layout.setCurrentWidget(self.settings)
        else:
            print("Hiding the settings screen")
            self.volume_widget.hide()
            self.brightness_widget.hide()
            self.clocks_widget.hide()
            self.settings.hide()
            self.our_layout.setCurrentWidget(self.beard)
        super().mousePressEvent(event)


if __name__ == '__main__':
#os.system('''mpv audio/startup.mp3 &''')
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec_()




