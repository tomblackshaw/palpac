'''
Created on May 25, 2024

@author: Tom Blackshaw
'''
import os
import sys

from my.classes import singleton
from my.classes.exceptions import MissingVoskModelError, CannotImportVoskError, CannotSetVoskLogLevelError, CannotImportLooseVersionError


def initialize_vosk():
    """Initialize the Vosk speech recognition tools.

    Check that the 'model' folder exists. This is where the relevant
    speech recognition data files reside. They are up to 1GB in size,
    which is why they are not distributed with the PALPAC packages.

    Note:
        Someone or something should download the relevant model from
        https://alphacephei.com/vosk/models *before* using this
        software.

    Args:
        n/a

    Returns:
        n/a

    Raises:
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
sr.aifc                        sr.google                      sr.Recognizer()                sr.TranscriptionNotReady(
sr.annotations                 sr.hashlib                     sr.recognizers                 sr.UnknownValueError(
sr.audio                       sr.hmac                        sr.Request(                    sr.urlencode(
sr.AudioData(                  sr.HTTPError(                  sr.RequestError(               sr.URLError(
sr.AudioFile(                  sr.io                          sr.requests                    sr.urlopen(
sr.audioop                     sr.json                        sr.subprocess                  sr.uuid
sr.AudioSource()               sr.math                        sr.sys                         sr.WaitTimeoutError(
sr.base64                      sr.Microphone(                 sr.tempfile                    sr.wave
sr.collections                 sr.os                          sr.threading                   sr.WavFile(
sr.exceptions                  sr.PortableNamedTemporaryFile( sr.time                        sr.whisper
sr.get_flac_converter()        sr.recognize_api(              sr.TranscriptionFailed(
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.__api = None
#        self.__api_lock = ReadWriteLock()
        initialize_vosk()
        import speech_recognition as speech_recog_api
        self.__api = speech_recog_api

        super().__init__()

    @property
    def api(self):
#        self.__api_lock.acquire_read()
        retval = self.__api
#        self.__api_lock.release_read()
        return retval

    @property
    def recognizer(self):
        return self.api.Recognizer()

