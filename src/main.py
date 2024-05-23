# -*- coding: utf-8 -*-
"""Main source file and subroutine.

This is the script that is run by the OS (or the user) when they want to
launch PALPAC. A bash script, I imagine, will 'cd' into this folder
and run main.py (me) accordingly.

Example:
    This is how a sample script would look::

        $ cd /path/to/palpac/files
        $ cd src
        $ python3 main.py

Section breaks are created by resuming unindented text. Section breaks
are also implicitly created anytime a new section starts.

Todo:
    * For module TODOs
    * You have to also use ``sphinx.ext.todo`` extension

.. _Style Guide:
   https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

"""

import sys

from PyQt6.QtWidgets import QWidget, QApplication  # pylint: disable=no-name-in-module

from my.classes.randomquoteclass import RandomQuoteSingleton as q
from my.exceptions import StillAwaitingCachedValue
from my.stringutils import add_to_os_path_if_existent
from my.tools import compile_all_uic_files
from ui.newform import Ui_Form


class FunWidget(QWidget):
    """The FunWidget (a subclass of QWidget) for testing PALPAC.

    This is a sample subclass for running a simple PyQt app and testing
    some of the PALPAC subroutines.

    Attributes:
        attr1 (str): Description of `attr1`.
        attr2 (:obj:`int`, optional): Description of `attr2`.

    """

    def __init__(self, tts):
        super().__init__()
        self.tts = tts

        # use the Ui_login_form
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # show the login window
        self.show()
        self.ui.btnQuit.clicked.connect(sys.exit)  # lambda: sys.exit())
        self.ui.btnPlay.clicked.connect(self.playme)  # lambda: self.playme())
        self.ui.btnRandQuote.clicked.connect(self.repopulateWithRandomQuote)  # lambda: self.repopulateWithRandomQuote())
        self.show()

    def repopulateWithRandomQuote(self):
        """Save a random inspirational quote to the plainTextEdit field.

        Note:
            This uses get_random_quote().

        Args:
            n/a

        Returns:
            n/a

        """
        try:
            txt = q.quote
        except StillAwaitingCachedValue:
            txt = 'Unable to obtain quote: cache is not populated yet.'
        except Exception as e:
            txt = 'Unable to obtain quote: {e}'.format(e=str(e))
        self.ui.plainTextEdit.setPlainText(txt)

    def playme(self):
        """Play the supplied text.

        Note:
            This uses self.tts, which is the singleton for talking to ElevenLabs.

        Args:
            n/a

        Returns:
            n/a

        """
        self.tts.play(self.tts.audio(text=self.ui.plainTextEdit.toPlainText(), voice=self.tts.random_name))


#########################################################################################################



if __name__ == '__main__':
    from my.text2speech import Text2SpeechSingleton
    add_to_os_path_if_existent('/opt/homebrew/bin', strict=False)
    compile_all_uic_files('ui')
    app = QApplication(sys.argv)
    qwin = FunWidget(tts=Text2SpeechSingleton)
    sys.exit(app.exec())
