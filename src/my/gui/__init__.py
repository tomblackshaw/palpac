# -*- coding: utf-8 -*-
"""my.tools

Created on May 19, 2024
Updated on Nov 05, 2024

@author: Tom Blackshaw

This module contains GUI-related tools.

.. _Style Guide:
   https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

"""

import os
from PyQt5.QtCore import Qt, QObject
from PyQt5.QtWidgets import QApplication, QScroller, QMessageBox


try: 
    from PyQt5.QtWebEngineWidgets import QWebEngineView as BrowserView
    from PyQt5.QtWebEngineWidgets import QWebEngineSettings as BrowserSettings
#    print("We are using QtWebEngineWidgets, which is good. It has JavascriptEnable(true/false) as an option.")
except ImportError: # QtWebKitWidgets was removed in Qt 5.6; you're using an ancient library.
    from PyQt5.QtWebKitWidgets import QWebView as BrowserView
    print("We ae using QtWebKitWidgets, which was deprecated in Qt 5.5 and removed in Qt 5.6; that's not great.")
    class BrowserSettings(QObject):
        def __init__(self):
            raise ImportError("MISSING BrowserSettings CLASS - you're using an ancient web browser widget.")



def set_vdu_brightness(brightness:int):
    # Technically, brightness>100 will be ignored by the hardware.
    if type(brightness) is not int:
        raise TypeError("Brightness parameter must be an integer")
    elif brightness < 0 or brightness > 100:
        raise ValueError("Brightness parameter must be between 0 and 100 (inclusive)")
    # echo {onoroff} > /sys/class/backlight/rpi_backlight/brightness; \
    res = os.system('''gpio -g mode 19 pwm; gpio -g pwm 19 {brightness}'''.format(brightness=brightness * 10))
    return res


def set_audio_volume(volume:int, mixer:str="Master"):
    """Set the volume of the principal ALSA device.

    Args:
        v (int): Volume level, from 0 to 11. (Don't use 11.)

    Raises:
        ValueError: if v<0 or >11
        TypeError: if v is not int.
    """
    real_vol_list = [0, 51, 60, 68, 75, 81, 86, 90, 93, 95, 96, 100]
    if type(volume) is not int:
        raise TypeError("set_audio_volume() takes an integer parameter, please.")
    if volume < 0 or volume > 11:
        raise ValueError("set_audio_volume() takes an int between 0 and 10, inclusive, please.")
    os.system('''amixer set "{mixer}" {volume}%'''.format(mixer=mixer, volume=real_vol_list[volume]))


def make_window_transparent(q:QObject, opacity=0.):
    q.setWindowOpacity(opacity)  # Turn entire window transparent
    q.setStyleSheet('QWidget{background: #000000}')  # Turn background transparent too

    
def make_background_translucent(q:QObject):
    q.setAttribute(Qt.WA_TranslucentBackground)  # Turn background of window transparent
    q.setWindowFlags(Qt.FramelessWindowHint)


def enable_touchscroll(q:QObject):
    QScroller.grabGesture(q, QScroller.LeftMouseButtonGesture) # Enable scroll-with-mouse-button


def make_scrollbars_zeropixels_in_size(w):
    w.setStyleSheet('QScrollBar {height:0px;}; QScrollBar {width:0px;}')  # Turn background transparent too
#    w.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
#    w.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)


def getRelativeFrameGeometry(widget):
    g = widget.geometry()
    fg = widget.frameGeometry()
    return fg.translated(-g.left(),-g.top())


def screenCaptureWidget(widget, parent_pos, filename, fileformat='png'):
#    rfg = getRelativeFrameGeometry(QApplication.primaryScreen())
    rfg = widget.frameGeometry()
    screen = QApplication.primaryScreen()
    screenshot = screen.grabWindow( widget.winId(), rfg.left()+parent_pos.x(), rfg.top() + parent_pos.y(),
                                       rfg.width(), rfg.height())
    screenshot.save(filename, fileformat)  

def popup_message(title, text):
    msg = QMessageBox()
    msg.setStyleSheet("QMessageBox {font-size:32px}; QPushButton {color:red; font-family: Arial; font-size:32px;}")
    msg.setWindowTitle(title)
    msg.setText(text)
    _ = msg.exec_()

