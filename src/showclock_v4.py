#!/usr/bin/python
'''

Display a clock in the background.
In the foreground, let the user adjust a slider that's visible only when the user taps the screen.
'''

import os
import sys

from PyQt5 import uic
from PyQt5.QtCore import QUrl, Qt, QObject, pyqtSignal, QPoint
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout

from my.gui import set_vdu_brightness, set_audio_volume, make_entire_window_transparent, set_background_translucent
from my.globals import FACES_DCT, TOUCHSCREEN_SIZE_X, TOUCHSCREEN_SIZE_Y, FACETWEAKS_DCT
import time

try:
    from PyQt5.QtWebKitWidgets import QWebView as Browser
except ImportError:
    from PyQt5.QtWebEngineWidgets import QWebEngineView as Browser

BASEDIR = os.path.dirname(__file__)
DEFAULT_CLOCK_NAME = 'braun' # list(FACES_DCT.keys())[0]
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
    def __init__(self):
        super().__init__()
        self.changeFace.connect(self.load)
        self.setFixedSize(TOUCHSCREEN_SIZE_X, TOUCHSCREEN_SIZE_Y)
        self.setWindowFlags(Qt.FramelessWindowHint)
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
        
    def adjust_zoom_etc(self, ok_or_nah):
        x, y, zoom = FACETWEAKS_DCT[self.face_name] if self.face_name in FACETWEAKS_DCT.keys() else (0, 0, 1)
        self.scroll(x, y)
        self.old_x = x 
        self.old_y = y 
        self.setZoomFactor(zoom)
#        self.setStyleSheet('QScrollBar {height:0px;}; QScrollBar {width:0px;}')  # Turn background transparent too
        self.setWindowOpacity(1.0)
#        self.setStyleSheet('QWidget{background: #000000}')
#        set_background_translucent(self)


class ClockfaceWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.b = ClockFace()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.b)
#        self.b.setLayout(self.layout)
        self.setCentralWidget(self.b)
        self.setFixedSize(TOUCHSCREEN_SIZE_X, TOUCHSCREEN_SIZE_Y)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet('QWidget{background: #000000}')  # Turn background transparent too
        self.show()

class MainWindow(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.confwindow = ConfiguratorWindow()
        self.clockface = ClockfaceWindow() # ClockFace()
        self.clickme = OverlayWindow(func_when_clicked=lambda : self.confwindow.setVisible(not self.confwindow.isVisible()))
        self.confwindow.lswFaces.currentTextChanged.connect(lambda x: self.clockface.b.changeFace.emit(x)) # TODO: remove lambda
        [self.confwindow.lswFaces.setCurrentItem(x) for x in self.confwindow.lswFaces.findItems(DEFAULT_CLOCK_NAME, Qt.MatchExactly)]

#os.system('''mpv audio/startup.mp3 &''')
app = QApplication(sys.argv)
win = MainWindow()
app.exec_()




