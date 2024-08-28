'''
Created on Aug 4, 2024

@author: Tom Blackshaw
'''
import os
import sys

from PyQt5 import QtCore
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog

from my.classes import ReadWriteLock
from my.gui import set_vdu_brightness, compile_all_uic_files
from ui.ConfigDialog import Ui_ConfigDiualog
from ui.MainWindow import Ui_MainWindow

# from PyQt5.QtWebKitWidgets import QWebView , QWebPage
# from PyQt5.QtWebKit import QWebSettings
# from PyQt5.Qt import *
# from PyQt5.Qt import QPushButton
# from PyQt5.QtWebEngineWidgets import *
# from PyQt5.QtWidgets import QApplication
# from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow
HYPERPIXEL21ROUND_DIMENSIONS_IN_PIXELS = (480, 480)


class ConfigDialog(QDialog, Ui_ConfigDiualog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.chosen_clock = None
        self.clickable_labels = (self.lblAnal1, self.lblAnal2, self.lblAndydig, self.lblBraun,
                  self.lblClean, self.lblCloxy, self.lblCube, self.lblKittycat,
                  self.lblNeon, self.lblOphelia, self.lblPeter, self.lblPie,
                  self.lblPurism, self.lblRounded, self.lblSlide, self.lblWally)
        for lbl in self.clickable_labels:
            lbl.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj in self.clickable_labels and event.type() == event.MouseButtonPress:
            print("chosen a clock")
            print(obj.objectName())
            self.chosen_clock = obj.objectName()
            self.close()
        return super(ConfigDialog, self).eventFilter(obj, event)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.clocks_dct = {
                      'lblAnal1':(1.2, 'AnalogClock-master/index.html'),
                      'lblCloxy':(1.25, 'clock-master/index.html'),
#                      'pure':'pure-css-watch-animation/dist/index.html',
#                      'canvy':(1.5, 'Customizable-Analog-Alarm-Clock-with-jQuery-Canvas-thooClock/index.html'),
                      'lblClean':(1, 'minimal-clean-analog/index.html'),
                      'lblRounded':(2.45, 'rounded-clock-main/index.html'),
                      'lblAnal2':(1.46, 'analog-clock/dist/index.html'),
                      'lblPurism':(2.2, 'minimalist-clock-pure-css-with-current-time/dist/index.html'),
                      'lblWally':(1, 'wall-clock/dist/index.html'),
                      'lblAndydig':(1, 'analog-digital-clock/dist/index.html'),
#                      'nils':(1, 'nilsclock/dist/index.html'),
                      'lblPeter':(1.2, 'peter/dist/index.html'),
                      'lblSlide':(1, 'slide-clock/dist/index.html'),
                      'lblOphelia':(1.6, 'ophelia/dist/index.html'),
                      'lblCube':(1.4, 'cube-clock/dist/index.html'),
                      'lblPie':(1.15, 'pie-time/dist/index.html'),
                      'lblKittycat':(1, 'kitkat-clock/dist/index.html'),
                      'lblBraun':(1.3, 'braun-clock/dist/index.html'),
                      'lblNeon':(1.18, 'this-neon/dist/index.html')}
#                      'neon3':(1, 'other-neon/dist/index.html'),
#                      'neon2':(0.9, 'neon-clock-css-jquery/dist/index.html')}
        print("hi")
        self.__clockname_lock = ReadWriteLock()
        self.__clockname = None

    def choose_clock(self):
    #     self.webengineview.focusProxy().installEventFilter(self)
    #
    # def eventFilter(self, obj, event):
    #     if obj is self.webengineview.focusProxy() and event.type() == event.MouseButtonPress:
        print("Widget click")
        dlg = ConfigDialog()
        dlg.setModal(True)
        dlg.show()
        print("Shown")
        dlg.exec_()
        print("Back.")
        dlg.hide()
        if dlg.chosen_clock is None:
            print("OK. You didn't choose a clock.")
        else:
            print("You chose", dlg.chosen_clock)
            self.clockname = dlg.chosen_clock
            if os.path.exists("/tmp/procno"):
                with open("/tmp/procno", 'r') as f:
                    procno = int(f.read().strip())
                os.system("kill %d" % procno)
            os.system("/Applications/Firefox.app/Contents/MacOS/firefox ui/clocks/%s & echo $! > /tmp/procno" % self.clocks_dct[self.clockname][1])
            os.system("sleep 6")

    #     return super(MainWindow, self).eventFilter(obj, event)

    @property
    def clockname(self):
        self.__clockname_lock.acquire_read()
        retval = self.__clockname
        self.__clockname_lock.release_read()
        return retval
    @property
    def all_clocknames(self):
        return list(self.clocks_dct.keys())
    @clockname.setter
    def clockname(self, value):
        self.__clockname_lock.acquire_write()
        try:
            self.__clockname = value
            the_zoom, the_fnam = self.clocks_dct[value]
            url = 'file://{cwd}/ui/clocks/{url}'.format(cwd=os.getcwd(), url=the_fnam)
            self.webengineview.load(QUrl(url))
            self.webengineview.setZoomFactor(the_zoom)
        finally:
            self.__clockname_lock.release_write()

# https://pythonspot.com/pyqt5-webkit-browser/


if __name__ == '__main__':
#    sys.path.insert(0, '/opt/homebrew/bin')
    compile_all_uic_files('ui')
#    os.system("$(which pyuic5) ui/mainwindow.ui -o ui/MainWindow.py")
#    os.system("$(which pyuic5) ui/configdialog.ui -o ui/ConfigDialog.py")
    os.system("$(which pyrcc5) ui/palpac.qrc -o ui/palpac_rc.py")
    set_vdu_brightness(70)

    vers = sys.version_info
    major_ver, minor_ver = vers[:2]
#    if major_ver < 3 or minor_ver < 12:
#        raise PythonVersionError("Python version {major_ver}.{minor_ver} is too old. I need 3.12 or higher.".format(major_ver=major_ver, minor_ver=minor_ver))
    app = QApplication(sys.argv)
    w = MainWindow()
    try:
        w.clockname = sys.argv[1]
    except IndexError:
        w.clockname = w.all_clocknames[-1]
    w.setWindowOpacity(0.1)
    w.setWindowFlags(QtCore.Qt.FramelessWindowHint)
#    w.setWindowFlags(QtCore.Qt.WA_TranslucentBackground)
    print(w.all_clocknames)
    # analog analdig analmast vanilla caac digiclock flatso analclean pureclock neon purewatch rotate rounded wally


    w.show()
    w.toolButton.clicked.connect(w.choose_clock)
    res = app.exec_()
    sys.exit(res)
    # web = QWebEngineView()
    # web.load(QUrl(sys.argv[1]))
    # web.show()
    # sys.exit(app.exec_())

