# -*- coding: utf-8 -*-
"""my.classes.elevenwrapper

Created on May 19, 2024

@author: Tom Blackshaw

Module for interacting with the ElevenLabs text-to-speech API. There is a
lot of cool stuff in here.

.. _Style Guide:
   https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

"""

from random import choice
import os

from elevenlabs.client import ElevenLabs, Voice

from my.classes import singleton, ReadWriteLock
from my.classes.exceptions import MissingVoskAPIKeyError
from my.globals import ELEVENLABS_KEY_BASENAME
from my.stringutils import flatten


# import random
def get_elevenlabs_clientclass(key_filename):
    """Retrieve the API class instance for interacting with the API.

    Using the key from the named filename, contact the Eleven Labs
    API and ask for the client class instance. This is how we
    communicate with the API.

    Args:
        key_filename (str): The pathname of the API key filename.

    Returns:
        client (elevenlabs.client.ElevenLabs): The client with which
            we communicate with the Eleven Labs API.

    Raises:
        MissingVoskAPIKeyError: The specified file, which should contain
            the API key, does not exist.

    """
    try:
        api_key = open(key_filename, 'r', encoding="utf-8").read().strip(' \n')
    except FileNotFoundError as e:
        raise MissingVoskAPIKeyError ("Please save the Eleven Labs API key to {key_filename} and try again.".format(key_filename=key_filename)) from e
    client = ElevenLabs(
        api_key=api_key)
    return client


@singleton
class _Text2SpeechClass:
    """Class that wraps around the Eleven Labs client class.

    Eleven Labs is a company that provides excellent text-to-speech
    services via a subscription-based API. The _Text2SpeechClass wraps
    around the Python-based API that it supplies.

    Properties created with the ``@property`` decorator should be documented
    in the property's getter method.

    Attributes:
        api_models (list[str]): Human-readable list of available speech
            synthesis models. Some are better suited to English or American
            accents; some, to Indian- or Chinese-language voices, for
            instance.
        api_voices (list[str]): Human-readable list of available voices.
            Each voice has its own accent, cadence, etc.
        voice (str): The currently chosen voice for any speech produced.
        model (str): The currently chosen model for any speech produced.
        stability (float): How accurately should the produced speech resemble
            the original speaker's source material? 0.0=none; 1.0=identical;
            anything less than 0.3 is unwise.
        similarity (float): How much randomness or variation should there be,
            between each result from Eleven Labs' API? 0.0=none; 1.0=gonzo.
        style (float): How much flair and/or scenery-chewing should there be?
            0.0=none; 1.0=gonzo; more than 0.5 is unwise.
        boost (bool): Should Eleven Labs try super-duper hard to make the
            speaker sound authentic? True if yes; False if no.

    Note:
        The default voice is chosen at random from all available voices.
        However, if one or more *professional* voices are available, a
        *professional* voice is chosen at random from only that group.

    """
    def __init__(self):
        self.key_filename = '%s%s%s' % (os.path.expanduser('~'), os.sep, ELEVENLABS_KEY_BASENAME)
        self.client = get_elevenlabs_clientclass(self.key_filename)
        self.__api_models_lock = ReadWriteLock()
        self.__api_voices_lock = ReadWriteLock()
        self.__voice_lock = ReadWriteLock()
        self.__advanced_lock = ReadWriteLock()
        self.__model_lock = ReadWriteLock()
        self.__stability_lock = ReadWriteLock()
        self.__similarity_lock = ReadWriteLock()
        self.__style_lock = ReadWriteLock()
        self.__boost_lock = ReadWriteLock()
        self.__api_voices = self.client.voices.get_all().voices
        self.__api_models = self.client.models.get_all()
        self.__voice = None
        self.__advanced = False
        self.__model = 'eleven_multilingual_v2'
        self.__stability = 0.30
        self.__similarity = 0.01
        self.__style = 0.50
        self.__boost = True
        professionals = [r for r in self.api_voices if r.samples is not None]
        if professionals != []:
            self.voice = professionals[0].name
            self.advanced = True
        else:
            self.voice = self.random_voice
        super().__init__()

    @property
    def api_models(self):
        self.__api_models_lock.acquire_read()
        retval = self.__api_models
        self.__api_models_lock.release_read()
        return retval

    @api_models.setter
    def api_models(self, value):
        self.__api_models_lock.acquire_write()
        self.__api_models = value
        self.__api_models_lock.release_write()

    @property
    def api_voices(self):
        self.__api_voices_lock.acquire_read()
        retval = self.__api_voices
        self.__api_voices_lock.release_read()
        return retval

    @api_voices.setter
    def api_voices(self, value):
        self.__api_voices_lock.acquire_write()
        self.__api_voices = value
        self.__api_voices_lock.release_write()

    @property
    def advanced(self):
        self.__advanced_lock.acquire_read()
        retval = self.__advanced
        self.__advanced_lock.release_read()
        return retval

    @advanced.setter
    def advanced(self, value):
        if type(value) is not bool:
            raise TypeError("When setting advanced=X, ensure X is a boolean.")
        self.__advanced_lock.acquire_write()
        self.__advanced = value
        self.__advanced_lock.release_write()

    @advanced.deleter
    def advanced(self):
        del self.__advanced

    @property
    def model(self):
        self.__model_lock.acquire_read()
        retval = self.__model
        self.__model_lock.release_read()
        return retval

    @model.setter
    def model(self, value):
        if type(value) is not str:
            raise TypeError("When setting advanced=X, ensure X is a string.")
        if value not in [r for r in self.all_models]:
            raise ValueError("model {model} is not a recognized model, according to the API".format(model=value))
        self.__model_lock.acquire_write()
        self.__model = value
        self.__model_lock.release_write()

    @model.deleter
    def model(self):
        del self.__model

    @property
    def stability(self):
        self.__stability_lock.acquire_read()
        retval = self.__stability
        self.__stability_lock.release_read()
        return retval

    @stability.setter
    def stability(self, value):
        if type(value) is not float:
            raise TypeError("When setting stability=X, ensure X is a float.")
        self.__stability_lock.acquire_write()
        self.__stability = value
        self.__stability_lock.release_write()

    @stability.deleter
    def stability(self):
        del self.__stability

    @property
    def similarity(self):
        self.__similarity_lock.acquire_read()
        retval = self.__similarity
        self.__similarity_lock.release_read()
        return retval

    @similarity.setter
    def similarity(self, value):
        if type(value) is not float:
            raise TypeError("When setting similarity=X, ensure value is a float.")
        self.__similarity_lock.acquire_write()
        self.__similarity = value
        self.__similarity_lock.release_write()

    @similarity.deleter
    def similarity(self):
        del self.__similarity

    @property
    def style(self):
        self.__style_lock.acquire_read()
        retval = self.__style
        self.__style_lock.release_read()
        return retval

    @style.setter
    def style(self, value):
        if type(value) is not float:
            raise TypeError("When setting style=X, ensure X is a float.")
        self.__style_lock.acquire_write()
        self.__style = value
        self.__style_lock.release_write()

    @style.deleter
    def style(self):
        del self.__style

    @property
    def boost(self):
        self.__boost_lock.acquire_read()
        retval = self.__boost
        self.__boost_lock.release_read()
        return retval

    @boost.setter
    def boost(self, value):
        if type(value) is not bool:
            raise TypeError("When setting boost=X, ensure X is a boolean.")
        self.__boost_lock.acquire_write()
        self.__boost = value
        self.__boost_lock.release_write()

    @boost.deleter
    def boost(self):
        del self.__boost

    @property
    def all_voices(self):
        return [r.name for r in self.api_voices]

    @property
    def all_models(self):
        return [r.model_id for r in self.api_models]

    @property
    def api_voicelabels(self):
        return list(set(flatten([[k for k in r.labels.keys()] for r in self.api_voices])))

    @property
    def api_voicecategories(self):
        return list(set([r.category for r in self.api_voices]))

    @property
    def random_voice(self):
        return choice([r for r in self.all_voices])

    @property
    def voice(self):
        self.__voice_lock.acquire_read()
        retval = self.__voice
        self.__voice_lock.release_read()
        return retval

    @voice.setter
    def voice(self, value):
        if type(value) is not str:
            raise TypeError("When setting name=X, ensure X is a string.")
        try:
            if value in [r.name for r in self.api_voices if r.samples is not None]:
                self.advanced = True
        except IndexError:
            self.advanced = False  # print("Okay. This is not a professional voice. We do not need to use advanced settings.")
        if value not in self.all_voices:
            raise ValueError("{name} is not a recognized voice name.".format(name=value))
        self.__voice_lock.acquire_write()
        self.__voice = value
        self.__voice_lock.release_write()

    @voice.deleter
    def voice(self):
        del self.__voice

    def id_of_a_name(self, a_name):
        return [r for r in self.api_voices if r.name == a_name][0].voice_id

    def name_of_an_id(self, an_id):
        return [r for r in self.api_voices if r.voice_id == an_id][0].name

    def audio(self, text, getgenerator=False):
        if self.advanced is False:
            audio = self.client.generate(text=text, voice=self.voice)
        else:
            audio = self.client.generate(text=text, model=self.model, voice=Voice(
                voice_id=self.id_of_a_name(self.voice),
                similarity_boost=self.similarity,
                stability=self.stability,
                style=self.style,
                use_speaker_boost=self.boost))
        return audio if getgenerator else b''.join(audio)

    def play(self, data):
        from elevenlabs import play
        if type(data) is str:
            raise ValueError("Please supply audio data, not a string, when calling me.")
        play(data)

    def say(self, txt):
        if type(txt) is not str:
            raise ValueError("Please supply a string, when calling me.")
        self.play(self.audio(text=txt))



