#!/usr/bin/python3

'''
Created on May 18, 2024

@author: Tom Blackshaw


'''

import os
import sys

from PyQt6.QtWidgets import (QWidget, QPushButton, QLineEdit, QInputDialog, QApplication)
from elevenlabs import play

from my.speakmymind import SpeakmymindSingleton
from my.stringstuff import get_random_zenquote, add_to_os_path
from ui.newform import Ui_Form


class Login(QWidget):

    def __init__(self, speechclient):
        super().__init__()
        self.speechclient = speechclient

        # use the Ui_login_form
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # show the login window
        self.show()
        self.ui.btnQuit.clicked.connect(lambda: sys.exit())
        self.ui.btnPlay.clicked.connect(lambda: self.playme())
        self.ui.btnRandQuote.clicked.connect(lambda: self.repopulateWithRandomQuote())
        self.show()
    
    def repopulateWithRandomQuote(self):
        self.ui.plainTextEdit.setPlainText(get_random_zenquote())
        
    def playme(self):
        play(self.speechclient.audio(text=self.ui.plainTextEdit.toPlainText(), voice=self.speechclient.random_name))

#########################################################################################################
 
if __name__ == '__main__':
    add_to_os_path('/opt/homebrew/bin')
    os.system('''echo $PWD''')
    os.system('''pyuic6 ui/newform.ui -o ui/newform.py''')
    # Prepare to speak. Contact ElevenLabs and get a clientclass.
    # Make a request to the ZenQuotes API
    app = QApplication(sys.argv)
    qwin = Login(speechclient=SpeakmymindSingleton)
#    ex = Example(speechclient=speechclient)
    sys.exit(app.exec())

