# -*- coding: utf-8 -*-
"""my.weather

Created on May 19, 2024

@author: Tom Blackshaw

This module facilitates my access to the Open Meteo online weather service.
See See https://github.com/frenck/python-open-meteo for more information.

Example:
    lat,lng = get_lat_and_long()
    w = get_weather()

Section breaks are created by resuming unindented text. Section breaks
are also implicitly created anytime a new section starts.

Attributes:
    n/a

Todo:
    * For module TODOs
    * You have to also use ``sphinx.ext.todo`` extension

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import random
import urllib

from bs4 import BeautifulSoup
from open_meteo import OpenMeteo
from open_meteo.exceptions import OpenMeteoConnectionError
from open_meteo.models import DailyParameters, HourlyParameters
from parse import parse

from my.classes.selfcachingcall import SelfCachingCall
from my.consts import WMO_code_warnings_dct
from my.exceptions import WebAPITimeoutError, WebAPIOutputError, StillAwaitingCachedValue
from my.globals import DEFAULT_LATLONG_URL, MAX_LATLONG_TIMEOUT
from my.stringutils import wind_direction_str, url_validator
from my.text2speech import play_dialogue_lst

def get_lat_and_long(url=DEFAULT_LATLONG_URL, timeout=10):
    """Gets my latitude and longitude.

    By calling cqcounter.com's relevant URL, I deduce my current latitude
    and longitude. I return it as a two-item tuple.

    Args:
        url (str, optional): An alternate URL for the PHP or other URL.
        timeout (int, optional): How long to wait before timing out. Range
            permitted: 0-MAX_LATLONG_TIMEOUT seconds.

    Returns:
        A two-item tuple of my latitude and longitude. For example:

        (-69.43, -8.574132)

        Returned values is always a tuple. Returned numbers are always
        floats.

    Raises:
        ValueError: The URL or the timeout was invalid.
        WebAPIOutputError: The URL's output gave an incomprehensible set
            of lat/long values. This might be a result of a bad URL.

    """
    if timeout <= 0 or timeout > MAX_LATLONG_TIMEOUT:
        raise ValueError("{timeout} is a silly timeout value; please change it & try again".format(timeout=timeout))
    if not url_validator(url):
        raise ValueError("{url} is not a valid URL; please ensure that it begins with http at least".format(url=url))
    try:
        uf = urllib.request.urlopen(url, timeout=timeout)
    except urllib.error.URLError as e:
        if 'timed out' in str(e):
            raise WebAPITimeoutError("{url} timed out; please try again later".format(url=url))
        else:
            raise ValueError("{url} is not a valid URL, according to urllib; please fix it".format(url=url))
    except urllib.error.HTTPError:
        raise WebAPIOutputError("{url} timed out while I was trying to get my latitude and longitude from it".format(url=url))
    except Exception as e:
        raise WebAPIOutputError("{url} gave an unspecified error: {e}; please check the source code and try again".format(url=url, e=str(e)))
    html = uf.read()
    soup = BeautifulSoup(html, 'html.parser')
    fmt_str = """{}°{}'{}" {}"""
    try:
        potlines_lst = [soup.find('td', string=i).find_next_sibling("td").text.strip() for i in ('IP Location', 'City', 'Latitude', 'Longitude', 'Distance')]
        latitude_res = parse(fmt_str, [r for r in potlines_lst if 'N' in r or 'S' in r][-1])
        longitude_res = parse(fmt_str, [r for r in potlines_lst if 'E' in r or 'W' in r][-1])
        myconv = lambda incoming: (float(incoming[0]) + float(incoming[1]) / 60. + float(incoming[2]) / 3600.) * (1 if 'N' in incoming[3] or 'W' in incoming[3] else -1)
        latitude = myconv(latitude_res)
        longitude = myconv(longitude_res)
    except (ValueError, AttributeError, IndexError):
        raise WebAPIOutputError("The URL '%s' did not produce meaningful lat/long values. Please check the URL and try again." % url)
    else:
        return(latitude, longitude)


def get_weather_SUB():
    """Retrieve weather info from OpenMeteo.

    I call the OpenMeteo API to retrieve detailed information on my local
    weather. I do not process the result. I merely return it.

    Args:
        n/a

    Returns:
        open_meteo.models.Forecast: structure containing weather info. For
        example:

        $ d = get_weather_SUB()
        $ d.current_weather
        CurrentWeather(time=datetime.datetime(...), temperature=15.5, wind_speed=10.5, ...)
        $ d.elevation
        109.5
        $ d.latitude
        101.10
        $ d.longitude
        50.50
        $ d.hourly.precipitation
        [0.0, 0.0, 0.0, 0.0, ...]

        Returned item is always an open_meteo.models.Forecast type.

    Raises:
        TimeoutError: The API thinks I'm trying too hard. It rejected my
            attempt to interrogate it.

    """
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


our_weather_caching_call = None


def get_weather():
    """Returns the cached result of a call to get_weather_SUB().

    The programmer calls me. I return a recently cached result of a call
    to get_weather_SUB(), courtesy of a self-caching class. I return
    the same as get_weather_SUB() returns, albeit cached.

    Args:
        n/a

    Returns:
        See get_weather_SUB().

    Raises:
        StillAwaitingCachedValue: The self-caching instance of
            get_weather_SUB() hasn't returned a value yet. I am still
            waiting for a response to its first call to openmeteo.
        WebAPIOutputError: The openmeteo website gave an illegible
            response to our request for weather data.
        WebAPITimeoutError: The openmeteo website timed out.

    """
    global our_weather_caching_call
    if our_weather_caching_call is None:
        our_weather_caching_call = SelfCachingCall(300, get_weather_SUB)
        force_update = True
    try:
        if force_update:
            our_weather_caching_call._update_me()
        return our_weather_caching_call.result
    except TimeoutError:
        raise WebAPITimeoutError("The openmeteo website timed out")
    except WebAPIOutputError:
        raise WebAPIOutputError("The openmeteo website returned an incomprehensible output")


def generate_weather_report_dialogue(myweather, speaker1, speaker2, testing=False):
    """Generate a dialogue from the weather.

    From the supplied OpenMeteo result, generate a slightly sarcastic dialogue
    between two Eleven Labs voices. The dialogue contains meterological info
    for the region covered by the report.

    Args:
        myweather (open_meteo.models.Forecast): a structure containing weather
            info for the latitude and longitude passed to get_weather().
        speaker1 (str): The name of the Eleven Labs voice to be used for speaker#1.
        speaker2 (str): The name of the Eleven Labs voice to be used for speaker#2.
        testing: If True, randomize the weather values, for testing.
            If False, don't.

    Returns:
        list of tuples: The names and the dialogue. For example:

        [('Rachel', 'Hi there. How are you?'),
        ('Callum', 'Fine. How is the weather?'),
        ('Rachel', 'It sucks.'),
        ('Callum', 'OK, then.')]

        Returned strings are always UTF-8.

    Raises:
        FIXME: I do not know which exceptions may occur. Please add entries.

    """
    if myweather is None:
        raise ValueError("Please specify a valid parameter for myweather. Usually, you supply the result of a call to get_weather().")
    randgreeting = lambda: random.choice(["Look who it is", "Howdy", 'Hi', 'Hello', 'Sup', 'Hey', "How you doin'", 'What it do', 'Greetings', "G'day", 'Hi there', "What's up", "How's it going", "What's good"])
    randweatherhi = lambda: random.choice(["What's the weather like today?", "How's the weather?", "Weather-wise, where are we at?", "Let's talk weather.", "Tell us about today's weather.", "What will today's weather be like?"])
    randnudge = lambda: random.choice(["Have you anything to add?", "Anything else?", "Is there more?", "You seem tense.",
                                       "There's more, isn't there?", "Okay, what's the bad news?", "You look constipated.", "You look anxious.", "What's with the long face?", "Go on.", "And?",
                                       "But?", "What is it you're not telling me?", "Spit it out.", "Oh, God. Here it comes.",
                                       "Finish your thought.", "Continue.", "Uh oh. I know that look."])
    randgoodbye = lambda: random.choice(["Oh %s, bless your heart.", "Oh %s, that's lovely news.", "%s, you made my day. Really. I'm super cereal.", "Thanks for nothing, %s.", "That's great, %s.",
                                        "%s, you're a star.", "Hey %s, you're a regular Nostradamus.", "As nerds go, %s, you're okay."]) % speaker2
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
        wcode = random.randint(0, 100)
        forecast_rainfall_quantity = random.randint(1, 100) / 10.
        forecast_rainfall_hours = random.randint(0, 24)
        mintemp = random.randint(-50, 10)
        maxtemp = mintemp + random.randint(1, 100)
        temperature = int((mintemp + maxtemp) / 2)
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

    if wcode not in WMO_code_warnings_dct.keys():
        from my.tools import logit
        logit("Warning - %s is not a recognized weather code. I am choosing 100 instead." % str(wcode))
        wcode = 100
    (wmo_retort, wmo_warning) = (None, None) if wcode == 0 else WMO_code_warnings_dct[wcode]
    wind_txt = 'no wind' if windspeed < 1.0 else "{windspeed} KPH winds blowing {winddir}.".format(windspeed=windspeed, winddir=wind_direction_str(winddirection))
    temper_txt = "The temperature is {tempC} degrees Celsius, {tempF} Fahrenheit, with a maximum of {maxC} (that's {maxF}), a minimum of {minC} (that's {minF}), and {wind_txt}".format(
        tempC=temperature ,
        tempF=int(temperature * 1.8 + 32),
        maxC=maxtemp,
        maxF=int(maxtemp * 1.8 + 32),
        minC=mintemp,
        minF=int(mintemp * 1.8 + 32),
        wind_txt=wind_txt
        ).replace('-', 'minus ').replace(' 1 degrees', ' 1 degree')
    dialogue_lst = []
    dialogue_lst.append([speaker1, "Hi, I'm {oldn} and here's {name} with the weather report. {greeting}, {name}. {question}".format(
        greeting=randgreeting(),
        oldn=speaker1,
        name=speaker2,
        question=randweatherhi())])
    dialogue_lst.append([speaker2, "{greeting}, {name}. {temper_txt} {rain_txt}".format(
        greeting=randgreeting(),
        name=speaker1,
        temper_txt=temper_txt,
        rain_txt=rain_txt)])
    if wmo_warning:
        dialogue_lst.append([speaker1, randnudge()])
        dialogue_lst.append([speaker2, wmo_warning])
    dialogue_lst.append([speaker1, '%s %s' % (wmo_retort if wmo_retort else '', randgoodbye() + " That was %s, our meteorologist." % speaker2)])  # This concludes our weather report.
    return dialogue_lst


def do_a_weather_report(tts, myweather, speaker1, speaker2, testing=False, stability=0.30, similarity_boost=0.01, style=0.5):
    """Read a real weather report out loud, using AI voices.

    The weather info itself comes from openmeteo. The AI voices are from Eleven
    Labs. The dialogue is assembled here and recited here.

    Args:
        tts (Text2SpeechSingleton): The class instance that wraps around the
            libraries from Eleven Labs and facilitates actual speech.
        myweather (open_meteo.models.Forecast): The record containing the
            current information about the weather and the forecast.
        speaker1 (str): The name of speaker 1. A list of voices may be
            obtained from the variable tts.voicenames
        speaker2 (str): The name of speaker 2.
        testing (bool): If True, randomize weather info.
        stability (float): How closely should the output be modeled on the
            original voice? Keep it above 0.30 for best results.
        similarity_boost (float): How much inflection etc. should be allowed
            in the voice?
        style (float): How much unnecessary drama should be in the voice?
            Keep the value below 0.5 for best results.

    Returns:
        n/a

    .. _PEP 484:
        https://www.python.org/dev/peps/pep-0484/

    """
    prof_name = [r for r in tts.voiceinfo if r.samples is not None][0].name
    if speaker1 == speaker2:
        speaker1 = prof_name
    # speechgen = lambda voice, text: \
    #         s.audio(voice=voice, text=text, advanced=True, model='eleven_multilingual_v2', stability=0.70, similarity_boost=0.01, style=0.9,use_speaker_boost=True) \
    #         if voice == prof_name \
    #         else \
    #         s.audio(voice=voice, text=text)
    dialogue_lst = generate_weather_report_dialogue(myweather=myweather, speaker1=speaker1, speaker2=speaker2, testing=testing)
    play_dialogue_lst(tts=tts, dialogue_lst=dialogue_lst, stability=stability, similarity_boost=similarity_boost, style=style)
