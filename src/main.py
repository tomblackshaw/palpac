'''
Created on May 18, 2024

@author: Tom Blackshaw

from main import *
c = get_elevenlabs_clientclass()
audio = c.generate(text=text, voice='Hugo', model='eleven_multilingual_v2', settings=VoiceSettings(stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True))


s = speakclient
s.stream_audio('Hi there. This is a test.', 'Hugo', advanced=True, model='eleven_multilingual_v2', stability=0.50, similarity_boost=0.01, style=0.10,use_speaker_boost=True)
s.stream_audio('Hi there. This is a test.', 'Hugo')
'''

import os
from random import randint
import sys

from PyQt6.QtWidgets import (QWidget, QPushButton, QLineEdit, QInputDialog, QApplication)
from elevenlabs import stream  # play, stream
from elevenlabs.client import ElevenLabs, VoiceSettings, Voice
import requests

from ui.newform import Ui_Form

ELEVENLABS_KEY_BASENAME = '.eleven_api_key'   # e.g. /home/foo/.eleven_api_key

 
'''
response = c.voices.get_all()
voices_dct = {}
for i in response.voices:
    voices_dct[i.name

'''
def add_to_os_path(a_path):
    if os.path.exists(a_path):
        os.environ['PATH'] += os.pathsep + a_path


def get_random_zenquote():
    response = requests.get('https://zenquotes.io/api/random')
    data = response.json()[0]
    quote = data['q'] + ' - ' + data['a']
    return quote


def get_elevenlabs_clientclass(key_filename):
    try:
        api_key = open(key_filename, 'r', encoding="utf-8").read().strip(' \n')
    except FileNotFoundError as e:
        del e
        raise FileNotFoundError ("Please save the Eleven Labs API key to %s and re-run this script." % key_filename)
    client = ElevenLabs(
        api_key=api_key)
    return client


def flatten(xss):
    return [x for xs in xss for x in xs]


class SpeakmymindClass(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            key_filename = '%s%s%s' % (os.path.expanduser('~'), os.sep, ELEVENLABS_KEY_BASENAME)
            cls.instance = super(SpeakmymindClass, cls).__new__(cls)
            cls.client = get_elevenlabs_clientclass(key_filename)
            cls._all_voices_info = cls.client.voices.get_all()
            cls._audio_dct = {}
        return cls.instance

    @property
    def voiceinfo(self):
        return self._all_voices_info.voices

    def voice_id(self, a_name):
        return [r for r in self.voiceinfo if r.name == a_name][0].voice_id

    def voice_name(self, an_id):
        return [r for r in self.voiceinfo if r.voice_id == an_id][0].voice_name

    @property
    def voice_labels(self):
        return list(set(flatten([[k for k in r.labels.keys()] for r in self.voiceinfo])))

    @property
    def voice_categories(self):
        return list(set([r.category for r in self.voiceinfo]))

    @property
    def voicenames(self):
        return [r.name for r in self._voices_get_all.voices]

    @property
    def random_voice_id(self, category=None):
        full_list = [r.voice_id for r in self.voiceinfo if category is None or r.category == category]
        i = randint(0, len(full_list))
        return full_list[i]

    @property
    def random_voice_name(self, category=None):
        full_list = [r.name for r in self.voiceinfo if category is None or r.category == category]
        i = randint(0, len(full_list))
        return full_list[i]
    
    def stream_audio(self, text, voice, advanced=False, model=None, similarity_boost=None, stability=None, style=None, use_speaker_boost=None):
        if advanced is False:
            audio = self.client.generate(text=text, voice=voice)
        else:
            audio = self.client.generate(text=text, model=model, voice=Voice(
                voice_id=self.voice_id(voice),
                similarity_boost=similarity_boost,
                stability=stability,
                style=style,
                use_speaker_boost=use_speaker_boost))
        stream(audio)


speakclient = SpeakmymindClass()


class Example(QWidget):

    def __init__(self, speechclient):
        super().__init__()
        self.initUI()
        self.speechclient = speechclient

    def initUI(self):

        self.btn = QPushButton('Dialog', self)
        self.btn.move(20, 20)
        self.btn.clicked.connect(self.showDialog)

        self.le = QLineEdit(self)
        self.le.move(130, 22)
        self.setGeometry(300, 300, 450, 350)
        self.setWindowTitle('Input dialog')
        self.show()

    def showDialog(self):

        text, ok = QInputDialog.getText(self, 'Input Dialog',
                                        'Enter your name:')

        if ok:
            if text == '':
                text = get_random_zenquote
            self.le.setText(str(text))
        audio = self.speechclient.generate(
            text=text, voice='Hugo', model='eleven_multilingual_v2')
        stream(audio)


def play_my_speech(speechclient, text):
    audio = speechclient.generate(text=text, voice='Hugo', model='eleven_multilingual_v2')
    stream(audio)



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
        self.ui.btnPlay.clicked.connect(lambda: self.play())
        self.ui.btnRandQuote.clicked.connect(lambda: self.repopulateWithRandomQuote())
        self.show()
    
    def repopulateWithRandomQuote(self):
        self.ui.plainTextEdit.setPlainText(get_random_zenquote())
        
    def play(self):
        play_my_speech(self.speechclient, self.ui.plainTextEdit.toPlainText())

#########################################################################################################
 
if __name__ == '__main__':
    add_to_os_path('/opt/homebrew/bin')
    os.system('''echo $PWD''')
    os.system('''pyuic6 ui/newform.ui -o ui/newform.py''')
    # Prepare to speak. Contact ElevenLabs and get a clientclass.
    speechclient = get_elevenlabs_clientclass()
    # Make a request to the ZenQuotes API
    app = QApplication(sys.argv)
    qwin = Login(speechclient=speechclient)
#    ex = Example(speechclient=speechclient)
    sys.exit(app.exec())

