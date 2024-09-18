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

try:
    from PyQt5.QtWebKitWidgets import QWebView as Browser
except ImportError:
    from PyQt5.QtWebEngineWidgets import QWebEngineView as Browser

BASEDIR = os.path.dirname(__file__)


class ConfiguratorWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(os.path.join(BASEDIR, "ui/invisiwindow.ui"), self)
        self.setAttribute(Qt.WA_TranslucentBackground)  # Turn background of window transparent
        self.setWindowFlags(Qt.FramelessWindowHint)


class InvisibleButClickableOverlayWindow(QMainWindow):

    def __init__(self, widget_to_open):
        super().__init__()
        self.the_widget_to_open = widget_to_open
        self.setFixedSize(480, 480)
        self.show()
        self.raise_()  # FIXME: Superfluous?
        self.setWindowOpacity(0.)  # Turn entire window transparent
        self.setStyleSheet('QWidget{background: #000000}')  # Turn background transparent too

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if self.the_widget_to_open.isVisible():
            self.the_widget_to_open.hide()
        else:
            self.the_widget_to_open.show()


class MyBrowser(Browser):

    def __init__(self, relpath):
        super().__init__()
        self.load(QUrl('file://{cwd}/{relpath}'.format(cwd=os.getcwd(), relpath=relpath)))
        self.setFixedSize(480, 480)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.show()


app = QApplication(sys.argv)
os.system('''amixer set "Master" 80%''')
os.system('''mpv audio/startup.mp3 &''')
set_vdu_brightness(80)
browser = MyBrowser('ui/clocks/braun-clock/dist/index.html' if len(sys.argv) < 2 else sys.argv[1])  # 3d-clock
confwindow = ConfiguratorWindow()
clickme = InvisibleButClickableOverlayWindow(confwindow)

app.exec_()
