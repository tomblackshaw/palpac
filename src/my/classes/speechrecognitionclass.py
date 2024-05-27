# -*- coding: utf-8 -*-
"""Module that wraps around Python's SpeechRecognition class(es).

Created on May 25, 2024

@author: Tom Blackshaw

This module contains (1) a class that wraps around Python's SpeechRecognition
class(es), and (2) subroutines that support that class.

Example:
    Assuming a microphone is present, the library can be asked to record
    output of the mic, turn it into text (without punctuation and
    probably lowercase), and return it::

        $ python3
        >>> from my.speechrecognition import SpeechRecognitionSingleton as s2t
        >>> audio_data = s2t.listen()
        >>> text = s2t.recognize(audio_data)

There are other properties and methods. This is the most important, but
others exist.

"""

import ast
import os
import sys

from my.classes import singleton, ReadWriteLock
from my.classes.exceptions import MissingVoskModelError, CannotImportVoskError, CannotSetVoskLogLevelError, CannotImportLooseVersionError, MutedMicrophoneError


def initialize_vosk():
    """Initialize the Vosk speech recognition tools.

    Check that the 'model' folder exists. This is where the relevant
    speech recognition data files reside. They are up to 1GB in size,
    which is why they are not distributed with the PALPAC packages.

    Note:
        Someone or something should download the relevant model from
        https://alphacephei.com/vosk/models *before* using this
        software.

        NoProfessionalVoicesError: There is no professional-grade voice
            available via the configured Eleven Labs account.

    TODO: Write me

    """
    if not os.path.exists("model"):
        raise MissingVoskModelError("Vosk model folder is missing. Please go to https://alphacephei.com/vosk/models and download the appropriate model (probably vosk-model-small-en-us-0.15); unzip it; rename the unzipped folder as 'model'; move it here.")
    try:
        import vosk
    except ImportError as e:
        raise CannotImportVoskError("Unable to perform initial importing of vosk Python library. Are you sure vosk is installed?") from e
    try:
        vosk.SetLogLevel(-1)
    except Exception as e:
        raise CannotSetVoskLogLevelError("Cannot set vosk's log level. Is vosk properly installed?") from e
    try:
        from distutils.version import LooseVersion  # pylint: disable=deprecated-module @UnusedImport, unknown-option-value
    except ModuleNotFoundError:
        sys.path.append("{cwd}/my/fake".format(cwd=os.getcwd()))
        try:
            from distutils.version import LooseVersion  # pylint: disable=deprecated-module @UnusedImport, unknown-option-value @Reimport
        except ModuleNotFoundError as e:
            raise CannotImportLooseVersionError("This OS is missing its distutils Python library. I tried a kludge, using a homemade LooseVersion class, but that failed.") from e
        else:
            print("FYI, distutils was missing. Perhaps this is a MacOS system. Anyway, I've provided a rudimentary LooseVersion class as a temporary workaround ")


@singleton
class _SpeechRecognitionClass:
    '''
    classdocs
    # TODO: Write me
    __api has these properties:
sr.aifc                        sr.google                      sr.Recognizer()                sr.TranscriptionNotReady(
sr.annotations                 sr.hashlib                     sr.recognizers                 sr.UnknownValueError(
sr.audio                       sr.hmac                        sr.Request(                    sr.urlencode(
sr.AudioData(                  sr.HTTPError(                  sr.RequestError(               sr.URLError(
sr.AudioFile(                  sr.io                          sr.requests                    sr.urlopen(
sr.audioop                     sr.json                        sr.subprocess                  sr.uuid
sr.AudioSource()               sr.math                        sr.sys                         sr.WaitTimeoutError(
sr.base64                                                       sr.tempfile                    sr.wave
sr.collections                 sr.os                          sr.threading                   sr.WavFile(
sr.exceptions                  sr.PortableNamedTemporaryFile( sr.time                        sr.whisper
sr.get_flac_converter()        sr.recognize_api(              sr.TranscriptionFailed(
    '''

    def __init__(self):
        self.__api = None
#        self.__api_lock = ReadWriteLock()
        initialize_vosk()
        import speech_recognition as speechrecognitionAPI
        self.__api = speechrecognitionAPI
        self.__pause_threshold_lock = ReadWriteLock()
        self.__recognizer = self.api.Recognizer()
        self.__timeout = 30.0
        self.__timeout_lock = ReadWriteLock()
        self.__max_recording_time = 10.0
        self.__max_recording_time_lock = ReadWriteLock()
        self.__always_adjust = True
        self.__always_adjust_lock = ReadWriteLock()
        self.__mute = False
        self.__mute_lock = ReadWriteLock()
        super().__init__()

    def adjust_for_ambient_noise(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)

    def listen(self):
        if self.__mute:
            raise MutedMicrophoneError("Microphone was muted. Please un-mute it with mute=False and try again.")
        else:
            with self.microphone as source:
                if self.__always_adjust:
                    self.recognizer.adjust_for_ambient_noise(source)  # Audio source must be entered before adjusting, see documentation for ``AudioSource`
                try:
                    audio = self.recognizer.listen(source, timeout=self.__timeout, phrase_time_limit=self.__max_recording_time)
                    return audio
                except WaitTimeoutError as e:
                    raise MicrophoneTimeoutError("Mic timed out, waiting for sounds.") from e
                else:
                    raise e

    @property
    def api(self):
#        self.__api_lock.acquire_read()
        retval = self.__api
#        self.__api_lock.release_read()
        return retval

    @property
    def mute(self):
        self.__mute_lock.acquire_read()
        retval = self.__mute
        self.__mute_lock.release_write()
        return retval

    @mute.setter
    def mute(self, value):
        self.__mute_lock.acquire_write()
        self.__mute = value
        self.__mute_lock.release_write()

    @property
    def recognize(self, audio_data):
        raw_txt_to_be_evald = self.recognizer.recognize_vosk(audio_data)
        text = ast.literal_eval(raw_txt_to_be_evald)['text'].strip()
        return text

    @property
    def recognizer(self):
        return self.__recognizer

    @property
    def microphone(self):
        return self.api.Microphone()

    @property
    def timeout(self):
        self.__timeout_lock.acquire_read()
        retval = self.__timeout
        self.__timeout_lock.release_write()
        return retval

    @timeout.setter
    def timeout(self, value):
        self.__timeout_lock.acquire_write()
        self.__timeout = value
        self.__timeout_lock.release_write()

    @property
    def always_adjust(self):
        self.__always_adjust_lock.acquire_read()
        retval = self.__always_adjust
        self.__always_adjust_lock.release_write()
        return retval

    @always_adjust.setter
    def always_adjust(self, value):
        self.__always_adjust_lock.acquire_write()
        self.__always_adjust = value
        self.__always_adjust_lock.release_write()

    @property
    def pause_threshold(self):
        self.__pause_threshold_lock.acquire_read()
        retval = self.recognizer.pause_threshold
        self.__pause_threshold_lock.release_read()
        return retval

    @pause_threshold.setter
    def pause_threshold(self, value):
        self.__pause_threshold_lock.acquire_write()
        self.recognizer.pause_threshold = value
        self.__pause_threshold_lock.release_write()

    @property
    def max_recording_time(self):
        self.__max_recording_time_lock.acquire_read()
        retval = self.__max_recording_time
        self.__max_recording_time_lock.release_write()
        return retval

    @max_recording_time.setter
    def max_recording_time(self, value):
        self.__max_recording_time_lock.acquire_write()
        self.__max_recording_time = value
        self.__max_recording_time_lock.release_write()
