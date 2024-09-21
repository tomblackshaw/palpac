#!/usr/bin/python
'''

Display a clock in the background.
In the foreground, let the user adjust a slider that's visible only when the user taps the screen.
'''

import os
import sys

from PyQt5 import uic
from PyQt5.QtCore import QUrl, Qt, QObject, QEvent, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget

from my.gui import set_vdu_brightness, set_audio_volume
from my.classes import ReadWriteLock

try:
    from PyQt5.QtWebKitWidgets import QWebView as Browser
except ImportError:
    from PyQt5.QtWebEngineWidgets import QWebEngineView as Browser

BASEDIR = os.path.dirname(__file__)
TOUCHSCREEN_SIZE_X, TOUCHSCREEN_SIZE_Y = 480, 480 
DEFAULT_CLOCK_NAME = 'neon 2'
# find ui | grep index.html | grep -v /src/ | grep -v original
FACES_DCT = {'neon 1':'ui/clocks/neon-clock-css-jquery/dist/index.html',
             'neon 2':'ui/clocks/this-neon/dist/index.html',
             'braun':'ui/clocks/braun-clock/dist/index.html',
             'anal 1':'ui/clocks/analog-clock-1/dist/index.html',
             'anal 2':'ui/clocks/analog-digital-clock/dist/index.html',
             'digital 1':'ui/clocks/digital-clock-1/dist/index.html',
             'digital 2': 'ui/clocks/digital-clock-2/dist/index.html',
             'clean': 'ui/clocks/minimal-clean-analog/index.html',
             'simple': 'ui/clocks/simple_javascript_clock/dist/index.html',
             'css':'ui/clocks/a-css-clock/dist/index.html',
             'jss':'ui/clocks/js-css-clock-with-sound/dist/index.html',
             'wall':'ui/clocks/wall-clock/dist/index.html',
             'rounded':'ui/clocks/rounded-clock-main/index.html',
             'series 2':'ui/clocks/time-series-2-typographic-clock/dist/index.html',
             '3D':'ui/clocks/3d-clock/dist/index.html',
             'slide':'ui/clocks/slide-clock/dist/index.html',
             'challenge':'ui/clocks/dev-challenge-week-3/dist/index.html',
             'another':'ui/clocks/another-canvas-clock/dist/index.html',
    }


class Communicate(QObject):
    changeFace = pyqtSignal(str)
    
    
def change_brightness(x):
    print("brightness is now", x)
    set_vdu_brightness(x)


def change_volume(x):
    print("volume is now", x)
    set_audio_volume(x)
    
    
def make_entire_window_transparent(q):
    q.setWindowOpacity(0.)  # Turn entire window transparent
    q.setStyleSheet('QWidget{background: #000000}')  # Turn background transparent too

    
def set_background_translucent(q):
    q.setAttribute(Qt.WA_TranslucentBackground)  # Turn background of window transparent
    q.setWindowFlags(Qt.FramelessWindowHint)


class ConfiguratorWindow(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(os.path.join(BASEDIR, "ui/configuratorwindow.ui"), self)
        set_background_translucent(self)
        self.sliBrightness.valueChanged.connect(lambda x: change_brightness(x))
        self.sliVolume.valueChanged.connect(lambda x: change_volume(x))
        for k in FACES_DCT.keys():
            self.lswFaces.addItem(k)


class OverlayWindow(QMainWindow):
    '''invisible but clickable'''
    def __init__(self, widget_to_open):
        super().__init__()
        self.the_widget_to_open = widget_to_open
        make_entire_window_transparent(self)
        self.setFixedSize(TOUCHSCREEN_SIZE_X, TOUCHSCREEN_SIZE_Y)
        self.show()
        self.raise_()
        
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.the_widget_to_open.setVisible(not self.the_widget_to_open.isVisible())


class ClockFace(Browser):
    def __init__(self, relpath=None):
        super().__init__()
        self.c = Communicate()
        self.c.changeFace.connect(self.load)
        self.setFixedSize(TOUCHSCREEN_SIZE_X, TOUCHSCREEN_SIZE_Y)
        self.setWindowFlags(Qt.FramelessWindowHint)
        if relpath is not None:
            self.load(relpath)
        self.show()

    def load(self, relpath):
        print("Loading", relpath)
        super().load(QUrl('file://{cwd}/{relpath}'.format(cwd=os.getcwd(), relpath=relpath)))


class ClockWithOverlay(OverlayWindow):
    def __init__(self, widget_to_open):
        super().__init__(widget_to_open)
        self.clockface = ClockFace()

class MainWindow(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clockface = ClockFace()
        self.confwindow = ConfiguratorWindow()
        self.clickme = OverlayWindow(widget_to_open=self.confwindow)
        self.confwindow.lswFaces.currentTextChanged.connect(lambda x: self.clockface.c.changeFace.emit(FACES_DCT[x]))
        [self.confwindow.lswFaces.setCurrentItem(x) for x in self.confwindow.lswFaces.findItems(DEFAULT_CLOCK_NAME, Qt.MatchExactly)]


if __name__ == '__main__':
    #os.system('''mpv audio/startup.mp3 &''')
    app = QApplication(sys.argv)
    win = MainWindow()
    app.exec_()




