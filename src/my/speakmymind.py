'''
Created on May 19, 2024

@author: Tom Blackshaw
speakmymind
'''

'''
from my.speakmymind import SpeakmymindSingleton
from my.tools import SelfCachingCall
from elevenlabs import play
s = SpeakmymindSingleton
prof_name= [r for r in s.voiceinfo if r.samples is not None][0].name
play(s.audio('Rachel', 'hello there'))
play(s.audio(s.random_name, 'Hi there. This is a test.'))
prof_audio = lambda text: s.audio(prof_name, text, advanced=True, model='eleven_multilingual_v2', stability=0.50, similarity_boost=0.01, style=0.10,use_speaker_boost=True)
freya_audio = lambda text: s.audio('Freya', text, advanced=True, model='eleven_multilingual_v2', stability=0.30, similarity_boost=0.01, style=0.50,use_speaker_boost=True)
play(s.audio(voice="Freya", text="Word up, homie G skillet dawg. What's crack-a-lackin'?"))
annoying_audio = lambda voice: s.audio(voice=voice, text="Like, OMG, you are totes late, Chuckles. JK, it's 7AM and POV your drip is straight fire. Or gay fire. Whatevs. Anyway, time to rise and shine, my short king sigma!",
                advanced=True, model='eleven_multilingual_v2', stability=0.30, similarity_boost=0.01, style=0.90,use_speaker_boost=True)

data_lst = [annoying_audio(au) for au in ('Freya', prof_name)]
for d in data_lst:
    play(d)

dramatic_audio = lambda voice, text : s.audio(voice=voice, text=text, advanced=True, model='eleven_multilingual_v2', stability=0.70, similarity_boost=0.01, style=0.9,use_speaker_boost=True)
def say_it_with_multiple_voices(voice_lst, text):
    dramatic_audio = lambda voice, text : s.audio(voice=voice, text=text, advanced=True, model='eleven_multilingual_v2', stability=0.70, similarity_boost=0.01, style=0.9,use_speaker_boost=True)#  if voice == prof_name else False)
    data_lst = [dramatic_audio(voice=r, text=text) for r in voice_lst]
    for d in data_lst:
        play(d)

damn_it_janet = lambda text: say_it_with_multiple_voices(['Freya', prof_name], text)
data_lst = [annoying_audio(au) for au in ('Freya', prof_name)]
for d in data_lst:
    play(d)

for d in ['Freya', 'Rachel', prof_name, 'Jessie']:


freya_say_it = lambda text : play(dramatic_audio('Freya', text)
prof_say_it = lambda text : play(dramatic_audio(prof_audio, text)

data_lst = [dramatic_audio(name, "Wake up, Chuckles!") for name in list(set([s.random_name,s.random_name,s.random_name,s.random_name,s.random_name,s.random_name]))]
cachingcalls = [SelfCachingCall(5, play, d) for d in data_lst]
for cc in cachingcalls: cc.join()

freya_scc = SelfCachingCall(5, play, freya_data)
rachel_scc = SelfCachingCall(5, play, rachel_data)
prof_scc = SelfCachingCall(5, play, prof_data)

prompts = (("Rachel", "Hey, %s, how's the weather today?" % prof_name), (prof_name, "The temperature is 80 degrees, there is a 10% chance of rain, wind is 5 miles her hour, excellent visibility. Freya? How's the traffic?"), ("Freya", "Traffic these nuts! I'm going to Target."))
data_lst = [dramatic_audio(voice=voice, text=text) for voice, text in prompts]
for d in data_lst:
    play(d)

simplesay = lambda voice, text: play(s.audio(voice=voice, text=text, advanced=True, model='eleven_multilingual_v2', stability=0.70, similarity_boost=0.01, style=0.9,use_speaker_boost=True))


'''
import os
from random import choice

from elevenlabs.client import ElevenLabs, Voice

from my.globals import ELEVENLABS_KEY_BASENAME
from my.stringstuff import flatten
from my.tools import singleton


def get_elevenlabs_clientclass(key_filename):
    try:
        api_key = open(key_filename, 'r', encoding="utf-8").read().strip(' \n')
    except FileNotFoundError as e:
        del e
        raise FileNotFoundError ("Please save the Eleven Labs API key to %s and re-run this script." % key_filename)
    client = ElevenLabs(
        api_key=api_key)
    return client


@singleton
class _SpeakmymindClass(object):

    def __init__(self):
        self.key_filename = '%s%s%s' % (os.path.expanduser('~'), os.sep, ELEVENLABS_KEY_BASENAME)
        self.client = get_elevenlabs_clientclass(self.key_filename)
        self._all_voices_info = self.client.voices.get_all()
        self._audio_dct = {}
        super().__init__()

    @property
    def voiceinfo(self):
        return self._all_voices_info.voices

    @property
    def voice_labels(self):
        return list(set(flatten([[k for k in r.labels.keys()] for r in self.voiceinfo])))

    @property
    def voice_categories(self):
        return list(set([r.category for r in self.voiceinfo]))

    @property
    def voicenames(self):
        return [r.name for r in self.voiceinfo]

    @property
    def random_name(self):
        return choice([r.name for r in self.voiceinfo])

    def get_id_of_name(self, a_name):
        return [r for r in self.voiceinfo if r.name == a_name][0].voice_id

    def get_name_of_id(self, an_id):
        return [r for r in self.voiceinfo if r.voice_id == an_id][0].name

    def audio(self, voice, text, getgenerator=False, advanced=False, model=None, similarity_boost=None, stability=None, style=None, use_speaker_boost=None):
        if advanced is False:
            audio = self.client.generate(text=text, voice=voice)
        else:
            audio = self.client.generate(text=text, model=model, voice=Voice(
                voice_id=self.get_id_of_name(voice),
                similarity_boost=similarity_boost,
                stability=stability,
                style=style,
                use_speaker_boost=use_speaker_boost))
        return audio if getgenerator else b''.join(audio)


# bytesresult = speakclient.audio('Rachel', 'hello there')
# play(bytesresult)
SpeakmymindSingleton = _SpeakmymindClass()
