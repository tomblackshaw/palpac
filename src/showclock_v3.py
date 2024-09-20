#!/usr/bin/python
'''

Display a clock in the background.
In the foreground, let the user adjust a slider that's visible only when the user taps the screen.
'''

import os
import sys

from PyQt5 import uic
from PyQt5.QtCore import QUrl, Qt, QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow

from my.gui import set_vdu_brightness, set_audio_volume, make_entire_window_transparent, set_background_translucent
from my.globals import FACES_DCT, TOUCHSCREEN_SIZE_X, TOUCHSCREEN_SIZE_Y

try:
    from PyQt5.QtWebKitWidgets import QWebView as Browser
except ImportError:
    from PyQt5.QtWebEngineWidgets import QWebEngineView as Browser

BASEDIR = os.path.dirname(__file__)
DEFAULT_CLOCK_NAME = list(FACES_DCT.keys())[0]
# find ui | grep index.html | grep -v /src/ | grep -v original



class ConfiguratorWindow(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(os.path.join(BASEDIR, "ui/configuratorwindow.ui"), self)
        set_background_translucent(self)
        self.sliBrightness.valueChanged.connect(set_vdu_brightness)
        self.sliVolume.valueChanged.connect(set_audio_volume)
        [self.lswFaces.addItem(k) for k in FACES_DCT.keys()]

class OverlayWindow(QMainWindow):
    '''invisible but clickable'''
    def __init__(self, func_when_clicked):
        super().__init__()
        self.func_when_clicked = func_when_clicked
        make_entire_window_transparent(self)
        self.setFixedSize(TOUCHSCREEN_SIZE_X, TOUCHSCREEN_SIZE_Y)
        self.show()
        self.raise_() # Ensure that I appear *in front of* the ClockFace
        
    def mousePressEvent(self, event):
        self.func_when_clicked()
        super().mousePressEvent(event)


class ClockFace(Browser):
    changeFace = pyqtSignal(str)
    def __init__(self, relpath=None):
        super().__init__()
        self.changeFace.connect(self.load)
        self.setFixedSize(TOUCHSCREEN_SIZE_X, TOUCHSCREEN_SIZE_Y)
        self.setWindowFlags(Qt.FramelessWindowHint)
        if relpath is not None:
            self.load(relpath)
        self.show()

    def load(self, relpath):
        super().load(QUrl('file://{cwd}/{relpath}'.format(cwd=os.getcwd(), relpath=relpath)))


class MainWindow(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clockface = ClockFace()
        self.confwindow = ConfiguratorWindow()
        self.clickme = OverlayWindow(func_when_clicked=lambda : self.confwindow.setVisible(not self.confwindow.isVisible()))
        self.confwindow.lswFaces.currentTextChanged.connect(lambda x: self.clockface.changeFace.emit(FACES_DCT[x]))
        [self.confwindow.lswFaces.setCurrentItem(x) for x in self.confwindow.lswFaces.findItems(DEFAULT_CLOCK_NAME, Qt.MatchExactly)]

#os.system('''mpv audio/startup.mp3 &''')
app = QApplication(sys.argv)
win = MainWindow()
app.exec_()




