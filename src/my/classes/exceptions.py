# -*- coding: utf-8 -*-
"""my.exceptions

Created on May 20, 2024

@author: Tom Blackshaw

This module demonstrates documentation. Docstrings may extend over multiple lines. Sections are created
with a section header and a colon followed by a block of indented text.


Error
    StartupError
        VoskStartupError
            MissingVoskModelError
        PyQtStartupError
            PyQtUICompilerError
        Text2SpeechStartupError
            VoiceNotChosenYetError
    WebAPIError
        WebAPIOutputError
        WebAPITimeoutError
    CachingError
        StillAwaitingCachedValue
    Text2SpeechError
        VoiceNotFoundError
            NoProfessionalVoicesError
    Speech2TextError
        RecognitionError
            MicrophoneError
                MicrophoneTimeoutError
                MutedMicrophoneError
            UnknownCommandError

Example:
    n/a

Attributes:
    n/a

.. _Style Guide:
   https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

"""


class Error(Exception):
    """Base class for other exceptions"""

    def __init__(self, message):  # pylint: disable=useless-parent-delegation
        super().__init__(message)


class StartupError(Error):
    """Class for all startup errors"""

    def __init__(self, message):  # pylint: disable=useless-parent-delegation
        super().__init__(message)

# class Text2SpeechStartupError(StartupError):
#     """Class for all Text2Speech Startup Errors"""
#
#     def __init__(self, message):  # pylint: disable=useless-parent-delegation
#         super().__init__(message)
#
#
# class VoiceNotChosenYetError(Text2SpeechStartupError):
#     """The programmer hasn't chosen a voice yet; use tts.voice=... to do that."""
#
#     def __init__(self, message):  # pylint: disable=useless-parent-delegation
#
#         super().__init__(message)


class VoskStartupError(StartupError):
    """Class for all Vosk startup errors"""

    def __init__(self, message):  # pylint: disable=useless-parent-delegation
        super().__init__(message)


class CannotImportVoskError(VoskStartupError):
    """The 'import vosk' call failed"""

    def __init__(self, message):  # pylint: disable=useless-parent-delegation
        super().__init__(message)


class CannotImportLooseVersionError(VoskStartupError):  # TODO: elaborate on this
    """The 'from distutils.version import LooseVersion' call failed"""

    def __init__(self, message):  # pylint: disable=useless-parent-delegation
        super().__init__(message)


class CannotSetVoskLogLevelError(VoskStartupError):
    """I cannot set Vosk's log level"""

    def __init__(self, message):  # pylint: disable=useless-parent-delegation
        super().__init__(message)


class MissingVoskModelError(VoskStartupError):
    """Model folder is missing; it should be saved to 'model' folder in src dir"""

    def __init__(self, message):  # pylint: disable=useless-parent-delegation
        super().__init__(message)


class PyQtStartupError(StartupError):
    """Class for all PyQt startup errors"""

    def __init__(self, message):  # pylint: disable=useless-parent-delegation
        super().__init__(message)


class PyQtUICompilerError(PyQtStartupError):
    """Class for all PyQt startup errors"""

    def __init__(self, message):  # pylint: disable=useless-parent-delegation

        super().__init__(message)


class WebAPIError(Error):
    """Class for web API errors"""

    def __init__(self, message):  # pylint: disable=useless-parent-delegation

        super().__init__(message)


class WebAPIOutputError(WebAPIError):
    """Class for web API output errors"""

    def __init__(self, message):  # pylint: disable=useless-parent-delegation

        super().__init__(message)


class WebAPIOverloadError(WebAPIError):
    """Class for web API output errors"""

    def __init__(self, message):  # pylint: disable=useless-parent-delegation

        super().__init__(message)


class WebAPITimeoutError(WebAPIError):
    """Class for web API timeout errors"""

    def __init__(self, message):  # pylint: disable=useless-parent-delegation

        super().__init__(message)


class CachingError(Error):
    """Class for all caching errors"""

    def __init__(self, message):  # pylint: disable=useless-parent-delegation

        super().__init__(message)


class StillAwaitingCachedValue(CachingError):
    """If we're trying to access a cached value that hasn't been cached yet.

    The class SelfCachingCall() calls the supplied function every N seconds
    and stores the result. If the result is an exception, it stores that.
    Either way, it replies with the result (or the exception) when the
    programmer asks for it. In this way, the programmer can receive
    instantaneously the result of a function call without having to wait
    for it to run.

    Of course, this means that there won't be a result at first. Otherwise,
    the programmer would have to wait until the first result had been cached:
    the opposite of the intended purpose of this class. Granted, the programmer
    would have to wait only once. Still, I don't like that. I would rather
    raise an exception and say, "We haven't cached the first value yet."

    Example:
        >>> from my.classes import SelfCachingCall
        >>> c = SelfCachingCall(2, myfunc, 100)
        >>> c.result
        my.globals.exceptions.StillAwaitingCachedValue: We have not cached the first result yet
        >>> sleep(1); c.result
        605

    Args:
        msg (str): Human readable string describing the exception.
        code (:obj:`int`, optional): Error code.

    Attributes:
        msg (str): Human readable string describing the exception.
        code (int): Exception error code.

    """

    def __init__(self, message):  # pylint: disable=useless-parent-delegation

        super().__init__(message)


class Text2SpeechError(Error):
    """Class for all text2speech errors"""

    def __init__(self, message):  # pylint: disable=useless-parent-delegation

        super().__init__(message)


class VoiceNotFoundError(Text2SpeechError):
    """Class for all 'voice not found' errors"""

    def __init__(self, message):  # pylint: disable=useless-parent-delegation

        super().__init__(message)


class NoProfessionalVoicesError(VoiceNotFoundError):
    """Class for all 'there are no professional voices available' errors"""

    def __init__(self, message):  # pylint: disable=useless-parent-delegation

        super().__init__(message)


class Speech2TextError(Error):
    """Class for all speechrecognitionclass errors"""

    def __init__(self, message):  # pylint: disable=useless-parent-delegation

        super().__init__(message)


class RecognitionError(Speech2TextError):
    """Class for all my custom speech recognition errors"""

    def __init__(self, message):  # pylint: disable=useless-parent-delegation

        super().__init__(message)


class MicrophoneError(RecognitionError):
    """Class for all my custom microphone errors"""

    def __init__(self, message):  # pylint: disable=useless-parent-delegation

        super().__init__(message)


class MicrophoneTimeoutError(MicrophoneError):
    """Class for all my timed-out microphone errors"""

    def __init__(self, message):  # pylint: disable=useless-parent-delegation

        super().__init__(message)


class MutedMicrophoneError(MicrophoneError):
    """Class for all my muted microphone errors"""

    def __init__(self, message):  # pylint: disable=useless-parent-delegation

        super().__init__(message)


class UnknownCommandError(RecognitionError):
    """Class for all my 'unknown command' errors"""

    def __init__(self, message):  # pylint: disable=useless-parent-delegation

        super().__init__(message)

