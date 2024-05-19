'''
Created on May 19, 2024

@author: Tom Blackshaw

weatherstuff

See https://github.com/frenck/python-open-meteo
'''
import os
from random import randint, choice
import random
import sys
import urllib

from bs4 import BeautifulSoup
from elevenlabs import play, stream
from elevenlabs.client import ElevenLabs, VoiceSettings, Voice
from open_meteo import OpenMeteo
import open_meteo
from open_meteo.models import DailyParameters, HourlyParameters
from parse import parse
from python_weather.enums import WindDirection
import requests

from my.consts import WMO_code_warnings_dct
from my.speakmymind import SpeakmymindSingleton
from my.stringstuff import wind_direction_str


def get_lat_and_long(url='http://cqcounter.com/whois/my_ip_address.php'):
    '''wget  -O - | egrep "IP Location|City|Latitude|Longitude"'''
    uf = urllib.request.urlopen(url)
    html = uf.read()
    soup = BeautifulSoup(html, 'html.parser')
    fmt_str = """{}°{}'{}" {}"""
    potlines_lst = [soup.find('td', string=i).find_next_sibling("td").text.strip() for i in ('IP Location', 'City', 'Latitude', 'Longitude', 'Distance')]
    latitude_res = parse(fmt_str, [r for r in potlines_lst if 'N' in r or 'S' in r][-1])
    longitude_res = parse(fmt_str, [r for r in potlines_lst if 'E' in r or 'W' in r][-1])
    myconv = lambda incoming: (float(incoming[0]) + float(incoming[1]) / 60. + float(incoming[2]) / 3600.) * (1 if 'N' in incoming[3] or 'W' in incoming[3] else -1)
    latitude = myconv(latitude_res)
    longitude = myconv(longitude_res)
    return(latitude, longitude)


def get_weather():
    (latitude, longitude) = get_lat_and_long()
    import asyncio

    async def main():
        """Show example on using the Open-Meteo API client."""
        async with OpenMeteo() as open_meteo:
            forecast = await open_meteo.forecast(
                latitude=latitude,
                longitude=longitude,
                current_weather=True,
                daily=[
                    DailyParameters.SUNRISE,
                    DailyParameters.SUNSET,
                    DailyParameters.PRECIPITATION_HOURS,
                    DailyParameters.PRECIPITATION_SUM,
                    DailyParameters.APPARENT_TEMPERATURE_MAX,
                    DailyParameters.APPARENT_TEMPERATURE_MIN
                ],
                hourly=[
                    HourlyParameters.TEMPERATURE_2M,
                    HourlyParameters.RELATIVE_HUMIDITY_2M,
                    HourlyParameters.PRECIPITATION,
                ],
            )
        return(forecast)
    return asyncio.run(main())


def do_a_weather_report(myweather, speaker1, speaker2, testing=False, stability=0.90, similarity_boost=0.01, style=0.5):
    s = SpeakmymindSingleton
    prof_name= [r for r in s.voiceinfo if r.samples is not None][0].name
    if speaker1 == speaker2:
        speaker1 = prof_name
    randgreeting = lambda: random.choice(['Hi', 'Hello', 'Sup', 'Hey', "How you doin'", 'What it do', 'Greetings', "G'day", 'Hi there', "What's up", "How's it going", "Whar's good"])
    randweatherhi = lambda: random.choice(["What's the weather like today?", "How's the weather?", "Weather-wise, where are we at?", "Let's talk weather.", "Tell us about today's weather.", "What will today's weather be like?"])
    randnudge = lambda: random.choice(["Have you anything to add?", "Anything else?", "Is there more?", "You seem tense.",
                                       "There's more, isn't there?", "Okay, what's the bad news?", "You look constipated.", "Go on.", "And?",
                                       "But?", "What is it you're not telling me?", "Spit it out.", "Oh, God. Here it comes.",
                                       "Finish your thought."])
    randgoodbye = lambda: random.choice(["Oh %s, bless your heart.", "Oh %s, that's lovely news.", "%s, you made my day. Really. I'm super cereal.", "Thanks for nothing, %s.", "Oh, that's great, %s.",
                                        "%s, you're a star.", "Hey %s, you're a regular Nostradamus."]) % speaker2
    speechgen = lambda voice, text: s.audio(voice=voice, text=text, advanced=True, model='eleven_multilingual_v2', stability=stability, similarity_boost=similarity_boost, style=style, use_speaker_boost=True)
    # speechgen = lambda voice, text: \
    #         s.audio(voice=voice, text=text, advanced=True, model='eleven_multilingual_v2', stability=0.70, similarity_boost=0.01, style=0.9,use_speaker_boost=True) \
    #         if voice == prof_name \
    #         else \
    #         s.audio(voice=voice, text=text)
    temper_txt = "It's %d degrees Celsius, %d degrees Fahrenheit." % (myweather.current_weather.temperature, myweather.current_weather.temperature * 1.8 + 32)
    wind_txt = 'Wind Speed: zero.' if myweather.current_weather.wind_speed < 1.0 else "Wind Speed %d KPH blowing %s." % (myweather.current_weather.wind_speed, wind_direction_str(myweather.current_weather.wind_direction))
#     forecast_rainfall_quantity = max(myweather.daily.precipitation_sum)
    forecast_rainfall_hours = max(myweather.daily.precipitation_hours)
    chance_of_rain = max(myweather.hourly.precipitation)
    wcode = myweather.current_weather.weather_code
    if testing:
        wcode = random.randint(1, 100)
#         forecast_rainfall_quantity = random.randint(1, 100) / 10.
        forecast_rainfall_hours = random.randint(0, 24)
    if forecast_rainfall_hours < 1 or chance_of_rain < 0.01:
        rain_txt = "It probably won't rain today."
    else:
        rain_txt = "There's a {rainpc} percent chance of rain.".format(rainpc=int(chance_of_rain * 100))
        # rain_txt = "There's a {rainpc} percent chance of rain, with {rainH} out of the next 24 hours producing {rainQ} {rainunit} of rainfall.".format(
        #                             rainpc=int(chance_of_rain * 100),
        #                             rainH=int(forecast_rainfall_hours),
        #                             rainQ=int(forecast_rainfall_quantity),
        #                             rainunit='centimeter' if forecast_rainfall_quantity == 1.0 else 'centimeters')
    (wmo_retort, wmo_warning) = (None, None) if wcode == 0 else WMO_code_warnings_dct[wcode]
    lst = []
    lst.append(speechgen(speaker1, "Hi, I'm {oldn} and here's {name} with the weather report. {greeting} {name}. {question}".format(greeting=randgreeting(), oldn=speaker1, name=speaker2, question=randweatherhi())))
    lst.append(speechgen(speaker2, "{greeting} {name}. {temper_txt}; {wind_txt}; {rain_txt}".format(greeting=randgreeting(), name=speaker1, temper_txt=temper_txt, wind_txt=wind_txt, rain_txt=rain_txt)))
    if wmo_warning:
        lst.append(speechgen(speaker1, randnudge()))
        lst.append(speechgen(speaker2, wmo_warning))
    lst.append(speechgen(speaker1, '%s... ... %s.' % (wmo_retort if wmo_retort else '', randgoodbye())))  # This concludes our weather report.
    for i in lst:
        play(i)

'''
from my.speakmymind import SpeakmymindSingleton
from my.weatherstuff import *
from my.stringstuff import wind_direction_str
import random
s = SpeakmymindSingleton
prof_name= [r for r in s.voiceinfo if r.samples is not None][0].name
w = get_weather()
do_a_weather_report(myweather=w, speaker1 = random.choice(s.voicenames), speaker2 = random.choice(s.voicenames), testing=True, stability=0.90, similarity_boost=0.01, style=0.5)
do_a_weather_report(myweather=w, speaker1 = random.choice(s.voicenames), speaker2 = random.choice(s.voicenames), testing=True, stability=0.50, similarity_boost=0.01, style=0.5)
do_a_weather_report(myweather=w, speaker1 = random.choice(s.voicenames), speaker2 = random.choice(s.voicenames), testing=True, stability=0.10, similarity_boost=0.01, style=0.9)
'''
