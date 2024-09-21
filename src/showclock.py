#!/usr/bin/python
'''

Display a clock in the background.
In the foreground, let the user adjust a slider that's visible only when the user taps the screen.
'''

import os
import sys

from PyQt5 import uic
from PyQt5.QtCore import QUrl, Qt, QObject, QEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget

from my.gui import set_vdu_brightness
from my.classes import ReadWriteLock

try:
    from PyQt5.QtWebKitWidgets import QWebView as Browser
except ImportError:
    from PyQt5.QtWebEngineWidgets import QWebEngineView as Browser

BASEDIR = os.path.dirname(__file__)


class ConfiguratorWindow(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(os.path.join(BASEDIR, "ui/configuratorwindow.ui"), self)
        self.setAttribute(Qt.WA_TranslucentBackground)  # Turn background of window transparent
        self.setWindowFlags(Qt.FramelessWindowHint)


class InvisibleButClickableOverlayWindow(QMainWindow):

    def __init__(self, widget_to_open):
        super().__init__()
        self.the_widget_to_open = widget_to_open
        self.setFixedSize(480, 480)
        self.show()
        self.raise_()
        self.setWindowOpacity(0.)  # Turn entire window transparent
        self.setStyleSheet('QWidget{background: #000000}')  # Turn background transparent too

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if self.the_widget_to_open.isVisible():
            self.the_widget_to_open.hide()
        else:
            self.the_widget_to_open.show()


class ClockFace(Browser):

    def __init__(self, relpath=None):
        super().__init__()
        self.setFixedSize(480, 480)
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
        self.clickme = InvisibleButClickableOverlayWindow(self.confwindow)
        self.__face = None
        self.__face_lock = ReadWriteLock()

    @property
    def face(self):
        self.__face_lock.acquire_read()
        try:
            retval = self.__face
            return retval
        finally:
            self.__face_lock.release_read()

    @face.setter
    def face(self, value):
        self.__face_lock.acquire_write()
        try:
            if value is None or type(value) is not str:
                raise ValueError("When setting face, specify a string & not a {t}".format(t=str(type(value))))
            self.__face = value
        finally:
            self.__face_lock.release_write()    

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    #os.system('''amixer set "Master" 80%''')
    #os.system('''mpv audio/startup.mp3 &''')
    #set_vdu_brightness(80)
    # clockface = ClockFace('ui/clocks/braun-clock/dist/index.html' if len(sys.argv) < 2 else sys.argv[1])  # 3d-clock
    # confwindow = ConfiguratorWindow()
    # clickme = InvisibleButClickableOverlayWindow(confwindow)
    win = MainWindow()
    win.clockface.load('ui/clocks/braun-clock/dist/index.html' if len(sys.argv) < 2 else sys.argv[1])  # 3d-clock
    app.exec_()




