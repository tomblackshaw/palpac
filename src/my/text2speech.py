# -*- coding: utf-8 -*-
"""my.text2speech

Created on May 19, 2024

@author: Tom Blackshaw

Wrapper for ElevenLabs API. This module demonstrates documentation. Docstrings may extend over multiple lines. Sections are created
with a section header and a colon followed by a block of indented text.

Example:
    Examples can be given using either the ``Example`` or ``Examples``
    sections. Sections support any reStructuredText formatting, including
    literal blocks::

        $ python3
        >>> from my.text2speech import Text2SpeechSingleton as tts
        >>> s = "Hello there. There's a car in the bar, by the farm."
        >>> tts.say(s)
        >>> for i in range(0,10): tts.name = tts.random_name; audiodata = tts.audio(s); tts.play(audiodata)

Section breaks are created by resuming unindented text. Section breaks
are also implicitly created anytime a new section starts.

Attributes:
    module_level_variable1 (int): Module level variables may be documented in
        either the ``Attributes`` section of the module docstring, or in an
        inline docstring immediately following the variable.

        Either form is acceptable, but the two should not be mixed. Choose
        one convention to document module level variables and be consistent
        with it.

Todo:
    * For module TODOs
    * You have to also use ``sphinx.ext.todo`` extension

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

from random import choice
import os
import random
import string

from elevenlabs.client import ElevenLabs, Voice

from my.classes import singleton
from my.consts import alarm_messages_lst, default_speaker_alarm_message_dct, hello_owner_lst
from my.globals import ELEVENLABS_KEY_BASENAME
from my.stringutils import flatten, convert_24h_and_mins_to_shorttime


def get_elevenlabs_clientclass(key_filename):
    """Example function with PEP 484 type annotations.

    Args:
        param1: The first parameter.
        param2: The second parameter.

    Returns:
        The return value. True for success, False otherwise.

    """
    # TODO: Write docs
    try:
        api_key = open(key_filename, 'r', encoding="utf-8").read().strip(' \n')
    except FileNotFoundError as e:
        raise FileNotFoundError ("Please save the Eleven Labs API key to %s and re-run this script." % key_filename) from e
    client = ElevenLabs(
        api_key=api_key)
    return client



@singleton
class _SpeakmymindClass(object):

    If the class has public attributes, they may be documented here
    in an ``Attributes`` section and follow the same formatting as a
    function's ``Args`` section. Alternatively, attributes may be documented
    inline with the attribute's declaration (see __init__ method below).

    Properties created with the ``@property`` decorator should be documented
    in the property's getter method.

    Attributes:
        attr1 (str): Description of `attr1`.
        attr2 (:obj:`int`, optional): Description of `attr2`.

    """
    def __init__(self):
        """Example of docstring on the __init__ method.

        The __init__ method may be documented in either the class level
        docstring, or as a docstring on the __init__ method itself.

        Either form is acceptable, but the two should not be mixed. Choose one
        convention to document the __init__ method and be consistent with it.

        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Args:
            param1 (str): Description of `param1`.
            param2 (:obj:`int`, optional): Description of `param2`. Multiple
                lines are supported.
            param3 (:obj:`list` of :obj:`str`): Description of `param3`.

        """
        # TODO: Write docs
        self.key_filename = '%s%s%s' % (os.path.expanduser('~'), os.sep, ELEVENLABS_KEY_BASENAME)
        self.client = get_elevenlabs_clientclass(self.key_filename)
        self.__all_voices = self.client.voices.get_all().voices
        self.__all_models = self.client.models.get_all()
        self.__name = None
        self.__advanced = False
        self.__model = 'eleven_multilingual_v2'
        self.__stability = 0.30
        self.__similarity = 0.01
        self.__style = 0.50
        self.__boost = True
        super().__init__()
        try:
            self.name = [r for r in self.all_voices if r.samples is not None][0].name
            self.advanced = True
        except IndexError:
            self.name = random.choice(self.all_names).name

    @property
    def advanced(self):
        # TODO: Add read/write locks
        return self.__advanced

    @advanced.setter
    def advanced(self, x):
        # TODO: Add read/write locks
        if type(x) is not bool:
            raise TypeError("When setting advanced=X, ensure X is a boolean.")
        self.__advanced = x

    @advanced.deleter
    def advanced(self):
        del self.__advanced

    @property
    def model(self):
        # TODO: Add read/write locks
        return self.__model

    @model.setter
    def model(self, x):
        # TODO: Add read/write locks
        if type(x) is not str:
            raise TypeError("When setting advanced=X, ensure X is a string.")
        if x not in [r.model_id for r in self.all_models]:
            raise ValueError("model {model} is not a recognized model, according to the API".format(model=x))
        self.__model = x

    @model.deleter
    def model(self):
        del self.__model

    @property
    def stability(self):
        # TODO: Add read/write locks
        return self.__stability

    @stability.setter
    def stability(self, x):
        # TODO: Add read/write locks
        if type(x) is not float:
            raise TypeError("When setting stability=X, ensure X is a float.")
        self.__stability = x

    @stability.deleter
    def stability(self):
        del self.__stability

    @property
    def similarity(self):
        # TODO: Add read/write locks
        return self.__similarity

    @similarity.setter
    def similarity(self, x):
        # TODO: Add read/write locks
        if type(x) is not float:
            raise TypeError("When setting similarity=X, ensure X is a float.")
        self.__similarity = x

    @similarity.deleter
    def similarity(self):
        del self.__similarity

    @property
    def style(self):
        # TODO: Add read/write locks
        return self.__style

    @style.setter
    def style(self, x):
        # TODO: Add read/write locks
        if type(x) is not float:
            raise TypeError("When setting style=X, ensure X is a float.")
        self.__style = x

    @style.deleter
    def style(self):
        del self.__style

    @property
    def boost(self):
        # TODO: Add read/write locks
        return self.__boost

    @boost.setter
    def boost(self, x):
        # TODO: Add read/write locks
        if type(x) is not bool:
            raise TypeError("When setting boost=X, ensure X is a boolean.")
        self.__boost = x

    @boost.deleter
    def boost(self):
        del self.__boost

    @property
    def all_voices(self):
        return self.__all_voices

    @property
    def all_models(self):
        return self.__all_models

    @property
    def voice_labels(self):
        return list(set(flatten([[k for k in r.labels.keys()] for r in self.__all_voices])))

    @property
    def voice_categories(self):
        return list(set([r.category for r in self.__all_voices]))

    @property
    def all_names(self):
        return [r.name for r in self.__all_voices]

    @property
    def random_name(self):
        return choice([r.name for r in self.__all_voices])

    @property
    def name(self):
        # TODO: Add read/write locks
        return self.__name

    @name.setter
    def name(self, x):
        # TODO: Add read/write locks
        if type(x) is not str:
            raise TypeError("When setting name=X, ensure X is a boolean.")
        try:
            if x in [r.name for r in self.all_voices if r.samples is not None]:
                self.advanced = True
        except IndexError:
            self.advanced = False  # print("Okay. This is not a professional voice. We do not need to use advanced settings.")
        if x not in self.all_names:
            raise ValueError("{name} is not a recognized voice name.".format(name=x))
        self.__name = x

    @name.deleter
    def name(self):
        del self.__name

    def id_of_a_name(self, a_name):
        return [r for r in self.all_voices if r.name == a_name][0].voice_id

    def name_of_an_id(self, an_id):
        return [r for r in self.all_voices if r.voice_id == an_id][0].name

    def audio(self, text, getgenerator=False):
        if self.advanced is False:
            audio = self.client.generate(text=text, voice=self.name)
        else:
            audio = self.client.generate(text=text, model=self.model, voice=Voice(
                voice_id=self.id_of_a_name(self.name),
                similarity_boost=self.similarity,
                stability=self.stability,
                style=self.style,
                use_speaker_boost=self.boost))
        return audio if getgenerator else b''.join(audio)

    def play(self, data):
        from elevenlabs import play
        play(data)

    def say(self, txt):
        self.play(self.audio(text=txt))


def play_dialogue_lst(tts, dialogue_lst, stability=0.5, similarity_boost=0.01, style=0.5):
    """Recites dialogue.

    Using the Eleven Labs website's API, their Python module, and mpv/ffmpeg, I play
    the supplied dialogue list. 'Do' the named voices, too. FYI, the API's key is
    stored at ~/$ELEVENLABS_KEY_BASENAME.

    Args:
        tts: Text-to-speech singleton Text2SpeechSingleton.
        dialogue_lst: List of dialogue tuples. The first item is the name of the voice
            to be used. The second item is the text to be recited.
        stability: The stability level (between 0.3 and 1.0 recommended).
        similarity_boost: The similarity level (between 0.01 and 1.0 recommended).
        style: The similarity level (between 0.0 and 0.5 recommended).

    Returns:
        n/a

    Raises:
        IOError: An error occurred accessing the smalltable.
    """
    from elevenlabs import play
    speechgen = lambda voice, text: tts.audio(voice=voice, text=text, advanced=True, model='eleven_multilingual_v2', stability=stability, similarity_boost=similarity_boost, style=style, use_speaker_boost=True)
    data_to_play = []
    from my.tools import logit
    for (name, text) in dialogue_lst:
        logit("{name}: {text}".format(name=name, text=text))
        data_to_play.append(speechgen(name, text))
    for d in data_to_play:
        play(d)


# bytesresult = speakclient.audio('Rachel', 'hello there')
# play(bytesresult)


Text2SpeechSingleton = _SpeakmymindClass()


def generate_alarm_message(owner, time_24h, time_minutes, message_template):  # TODO: This should use string.template.

    '''
from my.text2speech import *
import random
time_24h = random.randint(0,24)
time_minutes = random.randint(0,60)
owner = 'Chuckles'
message_template = alarm_messages_lst[0]
    '''
    if owner == '' or owner is None:
        raise ValueError("Owner -- the name of the human who owns this alarm clock -- needs to be a non-empty string. You supplied a duff value.")
    if type(time_24h) is not int or type(time_minutes) is not int or time_24h < 0 or time_24h >= 24 or time_minutes < 0 or time_minutes >= 60:
        raise ValueError("You supplied a duff hour and/or minute.")
    shorttime = convert_24h_and_mins_to_shorttime(time_24h, time_minutes)
    one_minute_ago = convert_24h_and_mins_to_shorttime(time_24h, time_minutes, diff=-1)
    one_minute_later = convert_24h_and_mins_to_shorttime(time_24h, time_minutes, diff=1)
    hello_owner = random.choice(hello_owner_lst)
    morning_or_afternoon_or_evening = 'morning' if time_24h < 12 else 'afternoon' if time_24h < 18 else 'evening'
    newval = message_template
    for _ in range(0, 5):
        oldval = newval
        ov_template= string.Template(oldval)
        newval = ov_template.substitute(hello_owner=hello_owner, owner=owner, shorttime=shorttime, one_minute_ago=one_minute_ago, one_minute_later=one_minute_later, morning_or_afternoon_or_evening=morning_or_afternoon_or_evening)
#        print("""{oldval} ==> {newval}""".format(oldval=oldval, newval=newval))
# s = message_template.replace('${', '').replace('}', '').replace('hello_owner', hello_owner).replace('owner', owner
#                         ).replace('shorttime', shorttime).replace('one_minute_ago', one_minute_ago
#                         ).replace("one_minute_later", one_minute_later).replace("morning_or_afternoon_or_evenin", morning_or_afternoon_or_evening)
    if '${' in newval:
        raise KeyError("Unresolved variable in {newval}. Look for the string in braces and check your source code.".format(newval=newval))
    return newval


def generate_random_alarm_message(owner_of_clock, time_24h, time_minutes, voice=None):
    """Example function with types documented in the docstring.

    `PEP 484`_ type annotations are supported. If attribute, parameter, and
    return types are annotated according to `PEP 484`_, they do not need to be
    included in the docstring:

    Args:
        param1 (int): The first parameter.
        param2 (str): The second parameter.

    Returns:
        bool: The return value. True for success, False otherwise.

    .. _PEP 484:
        https://www.python.org/dev/peps/pep-0484/

    """
    if voice in default_speaker_alarm_message_dct.keys():
        message_template = random.choice([default_speaker_alarm_message_dct[voice]] + alarm_messages_lst)
    else:
        message_template = random.choice(alarm_messages_lst)
    message = generate_alarm_message(owner_of_clock, time_24h, time_minutes, message_template)
    return message


def speak_random_alarm(owner_of_clock, time_24h, time_minutes, voice=None, tts=Text2SpeechSingleton):
    """Example function with types documented in the docstring.

    `PEP 484`_ type annotations are supported. If attribute, parameter, and
    return types are annotated according to `PEP 484`_, they do not need to be
    included in the docstring:

    Args:
        param1 (int): The first parameter.
        param2 (str): The second parameter.

    Returns:
        bool: The return value. True for success, False otherwise.

    .. _PEP 484:
        https://www.python.org/dev/peps/pep-0484/

    """
    if voice is None:
        voice = tts.random_name
    message = generate_random_alarm_message(owner_of_clock, time_24h, time_minutes, voice)
    prof_name = [r for r in tts.names if r.samples is not None][0].name
    if voice == prof_name:
        d = tts.audio(voice=voice, text=message, advanced=True, model='eleven_multilingual_v2', stability=0.30, similarity_boost=0.01, style=0.90, use_speaker_boost=True)
    else:
        d = tts.audio(voice=voice, text=message)
    tts.play(d)

def speak_totally_randomized_alarm_and_time(owner_of_clock):
    """Example function with types documented in the docstring.

    `PEP 484`_ type annotations are supported. If attribute, parameter, and
    return types are annotated according to `PEP 484`_, they do not need to be
    included in the docstring:

    Args:
        param1 (int): The first parameter.
        param2 (str): The second parameter.

    Returns:
        bool: The return value. True for success, False otherwise.

    .. _PEP 484:
        https://www.python.org/dev/peps/pep-0484/

    """
    time_24h = random.randint(0, 24)
    time_minutes = random.randint(0, 60)
    speak_random_alarm(owner_of_clock, time_24h, time_minutes)
