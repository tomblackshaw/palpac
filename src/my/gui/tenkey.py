'''
Created on Nov 8, 2024

@author: mchobbit
'''
from my import BASEDIR
from my.gui import make_background_translucent
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QDialog
import sys
from PyQt5.QtCore import QPoint

from my.globals import TOUCHSCREEN_SIZE_X, TOUCHSCREEN_SIZE_Y


def format_the_number_string(formattingstring, inputnumberstring):
    outstr = ''
    for c in formattingstring:
        if c == '.':
            if len(inputnumberstring) > 0:
                outstr += inputnumberstring[0]
                inputnumberstring = inputnumberstring[1:]
            else:
                break
        else:
            outstr += c
    return(outstr)


class TenkeyDialog(QDialog):
    '''
    classdocs
    '''

    def __init__(self, parent=None, formatstring=None, minlen=None, maxlen=None):
        '''
        Constructor
        '''
        # Initialize tenkey widget
        # Make it a modal widget
        # Specify the format: 99:99 or 99/99 or 9999
        # Initialize the enteredtext_lineedit accordingly
        # Set connections & signals for zero_button thru nine_button
        # Set connections & signals for backspace_button, accept_button
        # Hide the accept_button (UNTIL there are 4 digits entered in enteredtext_lineedit)
        # Show the cancel_button (UNLESS there are 4 digits entered in enteredtext_lineedit)
        # Hide the backspace_button (UNLESS there are 1 or more digits entered in enteredtext_lineedit)
        # Hide all 10 digit buttons (UNLESS there are <4 digits entered in enteredtext_lineedit)
        # Let user push the buttons
        # When the user clicks 'OK', I'll close the window & return the result.
        # If the user clicks 'backspace' when the string is already empty, I'll close & *not* return the result.
        if None in (formatstring, minlen, maxlen):
            raise ValueError("Please specify formatstring, minlen, and maxlen: e.g. '..:..', 4, 4")
        super().__init__(parent)
        uic.loadUi(os.path.join(BASEDIR, "ui/tenkey.ui"), self)
        make_background_translucent(self)
        self.enteredtext_lineedit.setText('')
        self.formatstring = formatstring
        self.maxlen = maxlen
        self.minlen = minlen
        self.__youtyped = ''
        self.zero_button.clicked.connect(lambda: self.digit_pushed(0))  # TODO: Use functools.partial instead
        self.one_button.clicked.connect(lambda: self.digit_pushed(1))
        self.two_button.clicked.connect(lambda: self.digit_pushed(2))
        self.three_button.clicked.connect(lambda: self.digit_pushed(3))
        self.four_button.clicked.connect(lambda: self.digit_pushed(4))
        self.five_button.clicked.connect(lambda: self.digit_pushed(5))
        self.six_button.clicked.connect(lambda: self.digit_pushed(6))
        self.seven_button.clicked.connect(lambda: self.digit_pushed(7))
        self.eight_button.clicked.connect(lambda: self.digit_pushed(8))
        self.nine_button.clicked.connect(lambda: self.digit_pushed(9))
        self.backspace_button.clicked.connect(self.backspace_pushed)
        self.cancel_button.clicked.connect(self.cancel_pushed)
        self.accept_button.clicked.connect(self.accept_pushed)
        self.hide_and_show_aux_buttons_appropriately()

    def digit_pushed(self, i):
        print("%d pushed" % i)
        if len(self.youtyped) < self.maxlen:
            self.youtyped += str(i)
        else:
            print("Sorry. Ignoring it. Max len already.")
        self.hide_and_show_aux_buttons_appropriately()

    @property
    def youtyped(self):
        return self.__youtyped

    @youtyped.setter
    def youtyped(self, value):
        self.__youtyped = value
        self.enteredtext_lineedit.setText(format_the_number_string(self.formatstring, value))

    def backspace_pushed(self):
        print("backspace pushed")
        if len(self.youtyped) > 0:
            self.youtyped = self.youtyped[:-1]
        else:
            print("Sorry. Ignoring it. Zero length already.")
        self.hide_and_show_aux_buttons_appropriately()

    def cancel_pushed(self):
        print("cancel pushed")
        self.reject()

    def accept_pushed(self):
        if self.minlen <= len(self.youtyped) <= self.maxlen:
            print("accept pushed")
            self.accept()
        else:
            print("ignored: wrong length")

    def hide_and_show_aux_buttons_appropriately(self):
        if len(self.youtyped) == 0:
            self.backspace_button.hide()
            self.cancel_button.show()
            self.accept_button.hide()
        elif len(self.youtyped) < self.minlen or len(self.youtyped) > self.maxlen:
            self.backspace_button.show()
            self.cancel_button.show()
            self.accept_button.hide()
        else:
            self.backspace_button.show()
            self.cancel_button.hide()
            self.accept_button.show()

    @staticmethod
    def getOutput(parent=None, formatstring=None, minlen=None, maxlen=None):
        dialog = TenkeyDialog(parent=parent, formatstring=formatstring, minlen=minlen, maxlen=maxlen)
        dialog.move(QPoint(TOUCHSCREEN_SIZE_X // 2 - dialog.size().width(), TOUCHSCREEN_SIZE_Y // 2 - dialog.size().height()))
        dialog.move(QApplication.desktop().screen().rect().center())  # - dialog.rect().center())
        result = dialog.exec_()
        s = dialog.enteredtext_lineedit.text()
        return (s, result == QDialog.Accepted)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    output, ok = TenkeyDialog.getOutput(formatstring='..:..', minlen=2, maxlen=4)
    print("output=%s; ok=%s" % (str(output), str(ok)))
#    app.exec_()
