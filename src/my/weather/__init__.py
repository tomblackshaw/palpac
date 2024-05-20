'''
Created on May 19, 2024

@author: Tom Blackshaw

weatherstuff

See https://github.com/frenck/python-open-meteo

from my.speakmymind import SpeakmymindSingleton as s
from my.weatherstuff import *
import random
do_a_weather_report(get_weather(), random.choice(s.voicenames), random.choice(s.voicenames), True)

w = get_weather()
#dialogue_lst = generate_weather_report_dialogue(testing=True, myweather=w, speaker1 = random.choice(s.voicenames), speaker2 = random.choice(s.voicenames))
do_a_weather_report(testing=True, myweather=w, speaker1 = random.choice(s.voicenames), speaker2 = random.choice(s.voicenames), stability=0.10, similarity_boost=0.01, style=0.9)


prof_name= [r for r in s.voiceinfo if r.samples is not None][0].name
dialogue_lst = generate_weather_report_dialogue(testing=True, myweather=w, speaker1 = random.choice(s.voicenames), speaker2 = random.choice(s.voicenames))
play_dialogue_lst(dialogue_lst, 0.90, 0.01, 0.5)
do_a_weather_report(testing=True, myweather=w, speaker1 = prof_name, speaker2 = random.choice(s.voicenames), stability=0.90, similarity_boost=0.01, style=0.5)
do_a_weather_report(testing=True, myweather=w, speaker1 = random.choice(s.voicenames), speaker2 = random.choice(s.voicenames), stability=0.50, similarity_boost=0.01, style=0.5)
do_a_weather_report(testing=True, myweather=w, speaker1 = random.choice(s.voicenames), speaker2 = random.choice(s.voicenames), stability=0.10, similarity_boost=0.01, style=0.9)
'''
