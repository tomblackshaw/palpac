'''
Created on May 19, 2024

@author: Tom Blackshaw

weatherstuff

See https://github.com/frenck/python-open-meteo
'''
import random
import urllib

from bs4 import BeautifulSoup
from elevenlabs import play
from open_meteo import OpenMeteo
from open_meteo.models import DailyParameters, HourlyParameters
from parse import parse

from my.consts import WMO_code_warnings_dct
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


def play_dialogue_lst(dialogue_lst, stability, similarity_boost, style):
    from my.speakmymind import SpeakmymindSingleton as s
    speechgen = lambda voice, text: s.audio(voice=voice, text=text, advanced=True, model='eleven_multilingual_v2', stability=stability, similarity_boost=similarity_boost, style=style, use_speaker_boost=True)
    data_to_play = []
    for (name, text) in dialogue_lst:
        print("{name}: {text}".format(name=name, text=text))
        data_to_play.append(speechgen(name, text))
    for d in data_to_play:
        play(d)


def generate_weather_report_dialogue(myweather, speaker1, speaker2, testing=False):
    randgreeting = lambda: random.choice(["Look who it is", "Howdy", 'Hi', 'Hello', 'Sup', 'Hey', "How you doin'", 'What it do', 'Greetings', "G'day", 'Hi there', "What's up", "How's it going", "What's good"])
    randweatherhi = lambda: random.choice(["What's the weather like today?", "How's the weather?", "Weather-wise, where are we at?", "Let's talk weather.", "Tell us about today's weather.", "What will today's weather be like?"])
    randnudge = lambda: random.choice(["Have you anything to add?", "Anything else?", "Is there more?", "You seem tense.",
                                       "There's more, isn't there?", "Okay, what's the bad news?", "You look constipated.", "You look anxious.", "What's with the long face?", "Go on.", "And?",
                                       "But?", "What is it you're not telling me?", "Spit it out.", "Oh, God. Here it comes.",
                                       "Finish your thought.", "Continue.", "Uh oh. I know that look."])
    randgoodbye = lambda: random.choice(["Oh %s, bless your heart.", "Oh %s, that's lovely news.", "%s, you made my day. Really. I'm super cereal.", "Thanks for nothing, %s.", "That's great, %s.",
                                        "%s, you're a star.", "Hey %s, you're a regular Nostradamus."]) % speaker2
    forecast_rainfall_quantity = myweather.daily.precipitation_sum[0]  # day 1 of the seven-day forecast
    forecast_rainfall_hours = myweather.daily.precipitation_hours[0]  # day 1 of the seven-day forecast
    chance_of_rain = max(myweather.hourly.precipitation)
    temperature = myweather.current_weather.temperature
    mintemp = myweather.daily.apparent_temperature_min[0]  # day 1 of the seven-day forecast
    maxtemp = myweather.daily.apparent_temperature_max[0]  # day 1 of the seven-day forecast
    wcode = myweather.current_weather.weather_code
    windspeed = myweather.current_weather.wind_speed
    winddirection = myweather.current_weather.wind_direction
    if testing:
        wcode = random.randint(1, 100)
        forecast_rainfall_quantity = random.randint(1, 100) / 10.
        forecast_rainfall_hours = random.randint(0, 24)
        mintemp = random.randint(-50, 10)
        maxtemp = mintemp + random.randint(1, 100)
        temperature = int((mintemp+maxtemp)/2)
        windspeed = random.randint(0, 100)
        winddirection = random.randint(0, 360)
    if forecast_rainfall_hours < 1 or chance_of_rain < 0.01:
        rain_txt = "It probably won't rain today."
    else:
        rain_txt = "There's a {rainpc} percent chance of rain.".format(rainpc=int(chance_of_rain * 100))
        rain_txt = "There's a {rainpc} percent chance of rain, with {rainH} out of the next 24 hours producing a total of {rainQ} {rainunit} of rainfall.".format(
                                    rainpc=int(chance_of_rain * 100),
                                    rainH=int(forecast_rainfall_hours),
                                    rainQ=int(forecast_rainfall_quantity),
                                    rainunit='centimeter' if forecast_rainfall_quantity == 1 else 'centimeters')
    (wmo_retort, wmo_warning) = (None, None) if wcode == 0 else WMO_code_warnings_dct[wcode]
    temper_txt = "The temperature is {tempC} degrees Celsius, {tempF} Fahrenheit, with a maximum of {maxC} (that's {maxF}) and a minimum of {minC} (that's {minF}).".format(
        tempC=temperature ,
        tempF=int(temperature * 1.8 + 32),
        maxC=maxtemp,
        maxF=int(maxtemp * 1.8 + 32),
        minC=mintemp,
        minF=int(mintemp * 1.8 + 32)
        ).replace('-', 'minus ').replace(' 1 degrees', ' 1 degree')
    wind_txt = 'Wind Speed: zero.' if windspeed < 1.0 else "Wind Speed %d KPH blowing %s." % (windspeed, wind_direction_str(winddirection))
    dialogue_lst = []
    dialogue_lst.append([speaker1, "Hi, I'm {oldn} and here's {name} with the weather report. {greeting} {name}. {question}".format(
        greeting=randgreeting(),
        oldn=speaker1,
        name=speaker2,
        question=randweatherhi())])
    dialogue_lst.append([speaker2, "{greeting}, {name}. {temper_txt} {wind_txt} {rain_txt}".format(
        greeting=randgreeting(),
        name=speaker1,
        temper_txt=temper_txt,
        wind_txt=wind_txt,
        rain_txt=rain_txt)])
    if wmo_warning:
        dialogue_lst.append([speaker1, randnudge()])
        dialogue_lst.append([speaker2, wmo_warning])
    dialogue_lst.append([speaker1, '%s %s' % (wmo_retort if wmo_retort else '', randgoodbye())])  # This concludes our weather report.
    return dialogue_lst


def do_a_weather_report(myweather, speaker1, speaker2, testing=False, stability=0.90, similarity_boost=0.01, style=0.5):
    from my.speakmymind import SpeakmymindSingleton as s
    prof_name = [r for r in s.voiceinfo if r.samples is not None][0].name
    if speaker1 == speaker2:
        speaker1 = prof_name
    # speechgen = lambda voice, text: \
    #         s.audio(voice=voice, text=text, advanced=True, model='eleven_multilingual_v2', stability=0.70, similarity_boost=0.01, style=0.9,use_speaker_boost=True) \
    #         if voice == prof_name \
    #         else \
    #         s.audio(voice=voice, text=text)
    dialogue_lst = generate_weather_report_dialogue(myweather=myweather, speaker1=speaker1, speaker2=speaker2, testing=testing)
    play_dialogue_lst(dialogue_lst=dialogue_lst, stability=stability, similarity_boost=similarity_boost, style=style)

'''
from my.speakmymind import SpeakmymindSingleton
from my.weatherstuff import *
from my.stringstuff import wind_direction_str
import random
s = SpeakmymindSingleton
prof_name= [r for r in s.voiceinfo if r.samples is not None][0].name
w = get_weather()
dialogue_lst = generate_weather_report_dialogue(testing=True, myweather=w, speaker1 = random.choice(s.voicenames), speaker2 = random.choice(s.voicenames))
play_dialogue_lst(dialogue_lst, 0.90, 0.01, 0.5)
do_a_weather_report(testing=True, myweather=w, speaker1 = random.choice(s.voicenames), speaker2 = random.choice(s.voicenames), , stability=0.90, similarity_boost=0.01, style=0.5)
do_a_weather_report(testing=True, myweather=w, speaker1 = random.choice(s.voicenames), speaker2 = random.choice(s.voicenames), stability=0.50, similarity_boost=0.01, style=0.5)
do_a_weather_report(testing=True, myweather=w, speaker1 = random.choice(s.voicenames), speaker2 = random.choice(s.voicenames), stability=0.10, similarity_boost=0.01, style=0.9)
'''
