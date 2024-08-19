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



0 0
1 51
2 60
3 68
4 75
5 81
6 86
7 90
8 93
9 95
10 96
11 100
'''

# from my.classes.text2speechclass import convert_audio_recordings_list_into_an_mp3_file
# from my.stringutils import convert_24h_and_mins_to_shorttime

# def speak_from_cache(voice, phrases):
#     from my.text2speech import Text2SpeechSingleton as tts
#     data = []
#     tts.voice = voice
#     for txt in phrases:
#         data.append(get_cached_audio_for_phrase(tts.voice, txt))
#     convert_audio_recordings_list_into_an_mp3_file(data, 'out.mp3', trim_level=1)
#     os.system("mpv out.mp3")



"""

import os
import sys

from PyQt5.QtWidgets import QWidget, QApplication  # pylint: disable=no-name-in-module

from my.classes.exceptions import StillAwaitingCachedValue, WebAPITimeoutError, WebAPIOutputError, MainAppStartupError
from my.randomquotes import RandomQuoteSingleton as q
from my.stringutils import add_to_os_path_if_existent, generate_random_alarm_message
from my.text2speech import smart_phrase_audio
from my.tools import compile_all_uic_files


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
#        self.ui = Ui_Form()
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
        except StillAwaitingCachedValue:  # as e:
            txt = 'Unable to obtain quote: cache is not populated yet.'
        except WebAPITimeoutError:  # as e:
            txt = 'I am sorry, but the ZenQuotes website did not get back to me in time.'
        except WebAPIOutputError:  # as e:
            txt = 'I am sorry, but the ZenQuotes website generated a weird output.'
        except Exception as e:  # pylint: disable=broad-exception-caught
            txt = 'Unknown exception raised: {e}'.format(e=str(e))
        self.ui.plainTextEdit.setPlainText(txt)

    def playme(self):
        """Play the text from the plainTextEdit instance.

        Note:
            This uses self.tts, which is the singleton for talking to ElevenLabs.

        Args:
            n/a

        Returns:
            n/a

        """
        self.tts.voice = self.tts.random_voice
        self.tts.say(self.ui.plainTextEdit.toPlainText())
#        self.tts.play(self.tts.audio(text=self.ui.plainTextEdit.toPlainText()))

#########################################################################################################



if __name__ == '__main__':
    for binname in ('mpv', 'pyuic6'):
        if 0 != os.system('which {binname} > /dev/null'.format(binname=binname)):
            raise MainAppStartupError("{binname} is missing. Please install it.".format(binname=binname))
    os.system('''amixer set "Master" 80%''')
    os.system("mpv audio/startup.mp3 &")
#    add_to_os_path_if_existent('/opt/homebrew/bin', strict=False)
#    compile_all_uic_files('ui')
#    app = QApplication(sys.argv)
#    qwin = FunWidget(tts=Text2SpeechSingleton)
#    qwin.showMaximized()
#    sys.exit(app.exec())
    this_voice = 'Sarah'
    txt = generate_random_alarm_message('Charlie', 1, 30, for_voice=this_voice)
    with open('/tmp/out.mp3', 'wb') as f:
        f.write(smart_phrase_audio(this_voice, txt))
    os.system("$(which mpv) /tmp/out.mp3")

