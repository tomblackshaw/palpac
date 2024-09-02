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

.. _Style Guide:
   https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html



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

import datetime
import os
import sys

from PyQt5.QtWidgets import QWidget

from my.classes.exceptions import StillAwaitingCachedValue, WebAPITimeoutError, WebAPIOutputError, MainAppStartupError
from my.gui import compile_all_uic_files, set_audio_volume
from my.randomquotes import RandomQuoteSingleton as q
from my.text2speech import speak_a_random_alarm_message


# from PyQt5.QtCore import QUrl
# from PyQt5.QtWidgets import QWidget, QApplication  # pylint: disable=no-name-in-module
# from PyQt5.QtWebKit import QWebSettings
# from PyQt5.QtWebKitWidgets import QWebView , QWebPage
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
    for binname in ('mpv', 'pyuic5'):
        if 0 != os.system('which {binname} > /dev/null'.format(binname=binname)):
            raise MainAppStartupError("{binname} is missing. Please install it.".format(binname=binname))
#    os.system("mpv audio/startup.mp3 &")
#    add_to_os_path_if_existent('/opt/homebrew/bin', strict=False)
    compile_all_uic_files('ui')
#    app = QApplication(sys.argv)
#    qwin = FunWidget(tts=Text2SpeechSingleton)
#    qwin.showMaximized()
#    sys.exit(app.exec())
    voices_lst = ['Sarah', 'Laura', 'Charlie', 'George', 'Callum', 'Liam', 'Charlotte', 'Alice', 'Matilda', 'Will', 'Jessica', 'Eric', 'Chris', 'Brian', 'Daniel', 'Lily', 'Bill', 'Hugo']
    if len(sys.argv) == 1 or sys.argv[1] not in voices_lst:
        print("Options:", voices_lst)
        sys.exit(1)
    this_voice = sys.argv[1]
    set_audio_volume(int(sys.argv[2])) # between 0 and 10
    speak_a_random_alarm_message(owner='Charlie', voice=this_voice, hour=datetime.datetime.now().hour, minute=datetime.datetime.now().minute, snoozed=False)

#     make_the_monks_chant(['Callum', 'Jessica', 'Sarah'], 'Hello world, you are loved.'.split(' '),
#                          (Cmaj, Fmaj, Gmaj, Fmin, Cmaj), outfile='/tmp/out.mp3', squelch=3)

# class MyBrowser(QWebPage):
#     ''' Settings for the browser.'''
#
#     def userAgentForUrl(self, url):
#         ''' Returns a User Agent that will be seen by the website. '''
#         return "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
#
#
# class Browser(QWebView):
#
#     def __init__(self):
#         # QWebView
#         self.view = QWebView.__init__(self)
#         # self.view.setPage(MyBrowser())
#         self.setWindowTitle('Loading...')
#         self.titleChanged.connect(self.adjustTitle)
#
#         # super(Browser).connect(self.ui.webView,QtCore.SIGNAL("titleChanged (const QString&amp;)"), self.adjustTitle)
#     def load(self, url):
#         self.setUrl(QUrl(url))
#         QWebSettings.globalSettings().setAttribute(QWebSettings.JavascriptEnabled, True)
#
#     def adjustTitle(self):
#         self.setWindowTitle(self.title())
#
#
# app = QApplication(sys.argv)
# view = Browser()
# view.showMaximized()
# view.load("file:///home/m/palpac/src/ui/clocks/clock-master/index.html")
# app.exec_()

