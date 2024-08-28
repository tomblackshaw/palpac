#!/usr/bin/python

import os
import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication
from ui import set_vdu_brightness

try:
    from PyQt5.QtWebKitWidgets import QWebView as Browser
except ImportError:
    from PyQt5.QtWebEngineWidgets import QWebEngineView as Browser

# os.system('''amixer set "Master" 80%''')
# os.system('''mpv audio/startup.mp3 &''')
set_vdu_brightness(80)
app = QApplication(sys.argv)
view = Browser()
view.load(QUrl('file://{cwd}/{relpath}'.format(cwd=os.getcwd(), relpath=sys.argv[1])))
view.setFixedSize(480, 480)
view.show()
app.exec_()
