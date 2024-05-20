# -*- coding: utf-8 -*-
"""main.py

Created on May 18, 2024

@author: Tom Blackshaw

PALPAC - the passive-aggressive Linux-based personal alarm clock

Example:
    To run a unit test::

        $ python3 -m unittest discover
    ...or...
        $ python3 -m unittest test.blah.blah.blah

Todo:
    * QQQ Finish me QQQ
    * You have to also use ``sphinx.ext.todo`` extension

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

# import os
import sys

from PyQt6.QtWidgets import QWidget, QApplication  # QPushButton, QLineEdit, QInputDialog, QApplication)
from elevenlabs import play

# from my.exceptions import PyQtUICompilerError
from my.stringutils import add_to_os_path_if_existent, get_random_quote
from my.tools import compile_all_uic_files
from ui.newform import Ui_Form


def compile_all_uic_files(a_path):
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f for f in listdir(a_path) if isfile(join(a_path, f))]
    for f in onlyfiles:
        if f.endswith('.ui'):
            cmd = '''pyuic6 -o "{a_path}/{pyfile}" "{a_path}/{uifile}"'''.format(
                a_path=a_path,
                uifile=f,
                pyfile=f[:-2] + 'py')
            if 0 != os.system(cmd):
                raise PyQtUICompilerError("{cmd} failed".format(cmd=cmd))


class FunWidget(QWidget):

    def __init__(self, isay):
        super().__init__()
        self.isay = isay

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
        self.ui.plainTextEdit.setPlainText(get_random_quote())

    def playme(self):
        play(self.speechclient.audio(text=self.ui.plainTextEdit.toPlainText(), voice=self.tts.random_name))

#########################################################################################################


if __name__ == '__main__':
    add_to_os_path_if_existent('/opt/homebrew/bin', strict=False)
    compile_all_uic_files('ui')
    # Prepare to speak. Contact ElevenLabs and get a clientclass.
    # Make a request to the ZenQuotes API
    app = QApplication(sys.argv)
    from my.text2speech import Text2SpeechSingleton as tts
    qwin = FunWidget(tts=tts)
#    ex = Example(speechclient=speechclient)
    sys.exit(app.exec())

