#!/usr/bin/python
'''

Display a clock in the background.
In the foreground, let the user adjust a slider that's visible only when the user taps the screen.
'''

import os
import sys

from PyQt5 import uic
from PyQt5.QtCore import QUrl, Qt, QEvent, QObject, QEvent, QSize
from PyQt5.QtGui import QCursor, QImage, QPalette, QBrush
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QPushButton, QGridLayout, QSizePolicy, QDesktopWidget

from my.gui import set_vdu_brightness

try:
    from PyQt5.QtWebKitWidgets import QWebView as Browser
except ImportError:
    from PyQt5.QtWebEngineWidgets import QWebEngineView as Browser

BASEDIR = os.path.dirname(__file__)


def center_the_widget(q):
    qr = q.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    q.move(qr.topLeft())


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(os.path.join(BASEDIR, "ui/invisiwindow.ui"), self)
        self.btnClose.clicked.connect(self.close)
        self.setWindowModality(Qt.ApplicationModal)
        self.setAttribute(Qt.WA_TranslucentBackground)  # Turn background of window transparent
        self.setWindowFlags(Qt.FramelessWindowHint)


class InvisibleButClickableOverlayWindow(QMainWindow):

    def __init__(self, widget_to_open):
        super().__init__()
        self.the_widget_to_open = widget_to_open
        self.setFixedSize(480, 480)
        self.show()
#        self.activateWindow()  # FIXME: Superfluous?
        self.raise_()  # FIXME: Superfluous?
        self.setWindowOpacity(0.)  # Turn entire window transparent
        self.setStyleSheet('QWidget{background: #000000}')  # Turn background transparent too

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.the_widget_to_open.show()
        self.the_widget_to_open.activateWindow()


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
confwindow = MainWindow()
clickme = InvisibleButClickableOverlayWindow(confwindow)

# center_the_widget(clickme)
# center_the_widget(confwindow)
# center_the_widget(browser)

app.exec_()
