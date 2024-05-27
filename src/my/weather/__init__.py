# -*- coding: utf-8 -*-
"""my.weather

Created on May 19, 2024

@author: Tom Blackshaw

This module facilitates my access to the Open Meteo online weather service.
See See https://github.com/frenck/python-open-meteo for more information.

Example:
    $ python3
    >>> lat,lng = get_latitude_and_longitude()
    >>> w = get_weather(lat,lng)

Example:
    $ python3
    >>> from my.weather import WeatherSingleton as ws
    >>> i = ws.forecast
    >>> print(i)

Example:
    from my.text2speech import Text2SpeechSingleton as tts
    from my.weather import WeatherSingleton as w, do_a_weather_report
    import random
    prof_name= get_first_prof_name(tts) # [r for r in tts.voiceinfo if r.samples is not None][0].name
    do_a_weather_report(tts=tts, testing=True, myforecast=w.forecast,
                speaker1 = prof_name,
                speaker2 = "Freya",
                stability=0.10, similarity_boost=0.01, style=0.9)

Section breaks are created by resuming unindented text. Section breaks
are also implicitly created anytime a new section starts.

Attributes:
    WeatherSingleton <== you know the deal

.. _Style Guide:
   https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

"""
import json
import random
import urllib

from bs4 import BeautifulSoup
from open_meteo import OpenMeteo
from open_meteo.models import DailyParameters, HourlyParameters, Forecast
from parse import parse
import requests

from my.classes import singleton, ReadWriteLock
from my.classes.exceptions import StillAwaitingCachedValue, WebAPITimeoutError, WebAPIOutputError
from my.classes.selfcachingcall import SelfCachingCall
from my.consts import WMO_code_warnings_dct
from my.globals import  MAX_LATLONG_TIMEOUT
from my.stringutils import wind_direction_str, url_validator
from my.text2speech import get_first_prof_name
from my.tools import object_from_dictionary


def get_latitude_and_longitude(url='https://ipinfo.io', timeout=10):
    """Gets my latitude and longitude.

    By calling ipinfo.io's relevant URL, I deduce my current latitude
    and longitude. I return it as a two-item tuple.

    Args:
        url (str, optional): An alternate URL for the PHP or other URL.
        timeout (int, optional): How long to wait before timing out. Range
            permitted: 0-MAX_LATLONG_TIMEOUT seconds.

    Returns:
        A two-item tuple of my latitude and longitude. For example:

        (-69.43, -8.574132)

        Returned value is always a tuple. Returned numbers are always
        floats.

    Raises:
        ValueError: The URL or the timeout was invalid.
        WebAPIOutputError: The URL's output gave an incomprehensible set
            of lat/long values. This might be a result of a bad URL.

    """
    if url_validator(url) is False:
        raise ValueError("Please specify a valid URL for url parameter. {url} is not a valid URL.".format(url=url))
    try:
        loc = get_ipinfo(url, timeout)['loc']
    except Exception as e:
        raise WebAPIOutputError("The URL '%s' did not produce a JSON-compatible output. Please check the URL and try again." % url) from e
    try:
        lati_str, longi_str = loc.split(',')
        latitude = float(lati_str)
        longitude = float(longi_str)
    except:
        raise WebAPIOutputError("The URL '%s' gave loc='%s', not meaningful lat/long values. Please check the URL and try again." % (url, str(loc))) from e
    return(latitude, longitude)



def get_ipinfo(url='https://ipinfo.io', timeout=10):
    """Gets my IP address, latitude, longitude, city, state, timezone, etc.

    By calling ipinfo.io's relevant URL, I deduce the aforementioned
    information.

    Args:
        url (str, optional): An alternate URL for the PHP or other URL.
        timeout (int, optional): How long to wait before timing out. Range
            permitted: 0-MAX_LATLONG_TIMEOUT seconds.

    Returns:
        A dictionary. For example:
            {'ip': '191.96.106.211',
            'city': 'Los Angeles',
            'region': 'California',
            'country': 'US',
            'loc': '34.0522,-118.2437',
            'org': 'AS174 Cogent Communications',
            'postal': '90009',
            'timezone': 'America/Los_Angeles',
            'readme': 'https://ipinfo.io/missingauth'}

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
        geo_req = requests.get(url, timeout=timeout)
    except Exception as e:
        raise WebAPITimeoutError("{url} timed out while I was trying to get ip info from it".format(url=url)) from e
    try:
        geo_json = json.loads(geo_req.text)
    except Exception as e:
        raise WebAPIOutputError("The URL '%s' did not produce a JSON-compatible output. Please check the URL and try again." % url) from e
    return geo_json


def get_weather(latitude, longitude):
    """Retrieve weather info from OpenMeteo.

    I call the OpenMeteo API to retrieve detailed information on my local
    weather. I do not process the result. I merely return it.

    Args:
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.

    Note:
        If latitude and longitude are not supplied, I shall deduce them
        on your behalf.

    Returns:
        open_meteo.models.Forecast: structure containing weather info. For
        example:

        $ d = get_weather()
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
    if [latitude, longitude].count(None) not in (0, 2):
        raise ValueError("Please specify latitude *and* longitude... or neither of them. Don't specify just one of them, please.")
    # if latitude is None and longitude is None:
    #     (latitude, longitude) = get_latitude_and_longitude()
    if type(latitude) not in (int, float) or type(longitude) not in (int, float):
        raise TypeError("Latitude and/or longitude are the wrong type. Please check your code and try again.")
    if latitude < -180 or longitude < -180 or latitude > 180 or longitude > 180:
        raise ValueError("Latitude and/or longitude are too large/small. Please check your code and try again.")
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


def generate_weather_report_dialogue(forecast, speaker1, speaker2, testing=False):
    """Generate a dialogue from the weather.

    From the supplied OpenMeteo result, generate a slightly sarcastic dialogue
    between two Eleven Labs voices. The dialogue contains meterological info
    for the region covered by the report.

    Args:
        forecast (open_meteo.models.Forecast): a structure containing weather
            info for the latitude and longitude passed to get_weather() or
            from WeatherSingleton.forecast
        speaker1 (str): The name of the Eleven Labs voice to be used for speaker#1.
        speaker2 (str): The name of the Eleven Labs voice to be used for speaker#2.
        testing: If True, randomize the weather values, for testing.
            If False, don't.

    Example:
        $ python3
        >>> from my.weather import WeatherSingleton as ws
        >>> generate_weather_report_dialogue(ws.forecast, 'Freya', 'Jessie', True)

    Returns:
        list of tuples: The names and the dialogue. For example:

        [('Rachel', 'Hi there. How are you?'),
        ('Callum', 'Fine. How is the weather?'),
        ('Rachel', 'It sucks.'),
        ('Callum', 'OK, then.')]

        Returned strings are always UTF-8.

    Raises:
        TypeError: Supplied parameters are of the wrong type.
        ValueError: Supplied parameters are defective.

    """
    if type(forecast) is not Forecast:
        raise TypeError("Please specify a parameter for forecast. Usually, you supply the result of a call to get_weather().")
    if type(speaker1) is not str or type(speaker2) is not str:
        raise TypeError("speaker1 and speaker2 must be strings.")
    randgreeting = lambda: random.choice(["Look who it is", "Howdy", 'Hi', 'Hello', 'Sup', 'Hey', "How you doin'", 'What it do', 'Greetings', "G'day", 'Hi there', "What's up", "How's it going", "What's good"])
    randweatherhi = lambda: random.choice(["What's the weather like today?", "How's the weather?", "Weather-wise, where are we at?", "Let's talk weather.", "Tell us about today's weather.", "What will today's weather be like?"])
    randnudge = lambda: random.choice(["Have you anything to add?", "Anything else?", "Is there more?", "You seem tense.",
                                       "There's more, isn't there?", "Okay, what's the bad news?", "You look constipated.", "You look anxious.", "What's with the long face?", "Go on.", "And?",
                                       "But?", "What is it you're not telling me?", "Spit it out.", "Oh, God. Here it comes.",
                                       "Finish your thought.", "Continue.", "Uh oh. I know that look."])
    randgoodbye = lambda: random.choice(["Oh %s, bless your heart.", "Oh %s, that's lovely news.", "%s, you made my day. Really. I'm super cereal.", "Thanks for nothing, %s.", "That's great, %s.",
                                        "%s, you're a star.", "Hey %s, you're a regular Nostradamus.", "As nerds go, %s, you're okay."]) % speaker2
    forecast_rainfall_quantity = forecast.daily.precipitation_sum[0]  # day 1 of the seven-day forecast
    forecast_rainfall_hours = forecast.daily.precipitation_hours[0]  # day 1 of the seven-day forecast
    chance_of_rain = max(forecast.hourly.precipitation)
    temperature = forecast.current_weather.temperature
    mintemp = forecast.daily.apparent_temperature_min[0]  # day 1 of the seven-day forecast
    maxtemp = forecast.daily.apparent_temperature_max[0]  # day 1 of the seven-day forecast
    wcode = forecast.current_weather.weather_code
    windspeed = forecast.current_weather.wind_speed
    winddirection = forecast.current_weather.wind_direction
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


def do_a_weather_report(tts, forecast, speaker1, speaker2, testing=False):  # , stability=0.30, similarity_boost=0.01, style=0.5):
    """Read a real weather report out loud, using AI voices.

    The weather info itself comes from openmeteo. The AI voices are from Eleven
    Labs. The dialogue is assembled here and recited here.

    Args:
        tts (Text2SpeechSingleton): The class instance that wraps around the
            libraries from Eleven Labs and facilitates actual speech.
        forecast (open_meteo.models.Forecast): The record containing the
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

    Raises:
        FIXME: Unknown.

    """
    prof_name = get_first_prof_name(tts)  # [r for r in tts.voice if r.samples is not None][0].name
    if speaker1 == speaker2:
        speaker1 = prof_name
    # speechgen = lambda voice, text: \
    #         s.audio(voice=voice, text=text, advanced=True, model='eleven_multilingual_v2', stability=0.70, similarity_boost=0.01, style=0.9,use_speaker_boost=True) \
    #         if voice == prof_name \
    #         else \
    #         s.audio(voice=voice, text=text)
    from my.text2speech import play_dialogue_lst
    dialogue_lst = generate_weather_report_dialogue(forecast=forecast, speaker1=speaker1, speaker2=speaker2, testing=testing)
    play_dialogue_lst(tts=tts, dialogue_lst=dialogue_lst)



def generate_short_and_long_weather_forecast_messages(forecast, owner_name, testing=False):
    """Generate shortform and longform weather forecast messages.

    From the supplied OpenMeteo result, generate two strings - one, shorter; the
    other, longer - containing meaningful information about the weather.

    Args:
        forecast (open_meteo.models.Forecast): a structure containing weather info
            and forecast. This structure was generated by get_weather(lat, long).
        owner_name (str): Who owns the alarm clock?
        speaker1 (str): The name of the Eleven Labs voice to be used for speaker#1.
        speaker2 (str): The name of the Eleven Labs voice to be used for speaker#2.
        testing: If True, randomize the weather values, for testing.
            If False, don't.

    Example:
        $ python3
        >>> from my.weather import WeatherSingleton as ws
        >>> generate_short_and_long_weather_forecast_messages(ws.forecast, 'Freya', 'Jessie', True)

    Returns:
        A tuple of strings. For example:

        ('blah blah', 'blah blah blah')

        Returned strings are always UTF-8.

    Raises:
        FIXME: I do not know which exceptions may occur. Please add entries.

    """
    if forecast is None:
        raise ValueError("Please specify a valid parameter for forecast. Usually, you supply the result of a call to get_weather().")
    randgreeting = lambda: random.choice(["Look who it is", "Howdy", 'Hi', 'Hello', 'Sup', 'Hey', "How you doin'", 'What it do', 'Greetings', "G'day", 'Hi there', "What's up", "How's it going", "What's good"])
    forecast_rainfall_quantity = forecast.daily.precipitation_sum[0]  # day 1 of the seven-day forecast
    forecast_rainfall_hours = forecast.daily.precipitation_hours[0]  # day 1 of the seven-day forecast
    chance_of_rain = max(forecast.hourly.precipitation)
    temperature = forecast.current_weather.temperature
    mintemp = forecast.daily.apparent_temperature_min[0]  # day 1 of the seven-day forecast
    maxtemp = forecast.daily.apparent_temperature_max[0]  # day 1 of the seven-day forecast
    wcode = forecast.current_weather.weather_code
    windspeed = forecast.current_weather.wind_speed
    winddirection = forecast.current_weather.wind_direction
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
    (wmo_retort, wmo_warning) = ('', '') if wcode == 0 else WMO_code_warnings_dct[wcode]
    wind_txt = 'no wind' if windspeed < 1.0 else "{windspeed} KPH winds blowing {winddir}".format(windspeed=windspeed, winddir=wind_direction_str(winddirection))
    longer_temper_txt = "The temperature is {tempC} degrees Celsius, {tempF} Fahrenheit, with a maximum of {maxC} (that's {maxF}), a minimum of {minC} (that's {minF}), and {wind_txt}.".format(
        tempC=temperature ,
        tempF=int(temperature * 1.8 + 32),
        maxC=maxtemp,
        maxF=int(maxtemp * 1.8 + 32),
        minC=mintemp,
        minF=int(mintemp * 1.8 + 32),
        wind_txt=wind_txt
        ).replace('-', 'minus ').replace(' 1 degrees', ' 1 degree')
    shorter_temper_txt = "It's {tempC} Celsius, {tempF} Fahrenheit, and {wind_txt}.".format(
        tempC=temperature ,
        tempF=int(temperature * 1.8 + 32),
        wind_txt=wind_txt
        ).replace('-', 'minus ').replace(' 1 degrees', ' 1 degree')
    longer_message = "{greeting}, {owner_name}. {temper_txt} {rain_txt} {wmo_warning} {wmo_retort}".format(
        greeting=randgreeting(),
        owner_name=owner_name,
        temper_txt=longer_temper_txt,
        rain_txt=rain_txt,
        wmo_warning=wmo_warning,
        wmo_retort=wmo_retort)
    shorter_message = "{owner_name}, {temper_txt} {rain_txt} {wmo_warning}".format(
        owner_name=owner_name,
        temper_txt=shorter_temper_txt,
        rain_txt=rain_txt,
        wmo_warning=wmo_warning)
    return(shorter_message, longer_message)


@singleton
class _WeatherClass:
    """Returns the cached result of a call to get_weather().

    The programmer calls me. I return a recently cached result of a call
    to get_weather(), courtesy of a self-caching class. I return
    the same as get_weather() returns, albeit cached.

    Args:
        n/a

    Returns:
        See get_weather().

    Raises:
        StillAwaitingCachedValue: The self-caching instance of
            get_weather() hasn't returned a value yet. I am still
            waiting for a response to its first call to openmeteo.
        WebAPIOutputError: The openmeteo website gave an illegible
            response to our request for weather data.
        WebAPITimeoutError: The openmeteo website timed out.

    """

    def __init__(self):
        self.__latitude, self.__longitude = get_latitude_and_longitude()
        self.__longitude_lock = ReadWriteLock()
        self.__latitude_lock = ReadWriteLock()
        self._our_weather_caching_call = SelfCachingCall(300, self.force_update)
        super().__init__()

    def force_update(self):
        return get_weather(self.latitude, self.longitude)

    @property
    def longitude(self):
        self.__longitude_lock.acquire_read()
        retval = self.__longitude
        self.__longitude_lock.release_read()
        return retval

    @longitude.setter
    def longitude(self, value):
        self.__longitude_lock.acquire_write()
        self.__longitude = value
        self.__longitude_lock.release_write()

    @property
    def latitude(self):
        self.__latitude_lock.acquire_read()
        retval = self.__latitude
        self.__latitude_lock.release_read()
        return retval

    @latitude.setter
    def latitude(self, value):
        self.__latitude_lock.acquire_write()
        self.__latitude = value
        self.__latitude_lock.release_write()

    @property
    def forecast(self):
        try:
            return self._our_weather_caching_call.result
        except StillAwaitingCachedValue:
            self._our_weather_caching_call.update_me()
            return self.forecast
        except TimeoutError as e:
            raise WebAPITimeoutError("The openmeteo website timed out") from e
        except WebAPIOutputError:
            raise WebAPIOutputError("The openmeteo website returned an incomprehensible output") from e


WeatherSingleton = _WeatherClass()


def speak_a_weather_report(tts, owner_name, latitude=None, longitude=None, testing=False):
    if latitude is None or longitude is None:
        latitude, longitude = get_latitude_and_longitude()
    forecast = get_weather(latitude, longitude)
    shorter_msg, longer_msg = generate_short_and_long_weather_forecast_messages(forecast, owner_name, testing)
    data = tts.audio(text=shorter_msg)
    del longer_msg
    tts.play(data)


def generate_weather_audio(tts, owner_name, latitude=None, longitude=None, testing=False):
    if latitude is None or longitude is None:
        latitude, longitude = get_latitude_and_longitude()
    forecast = get_weather(latitude, longitude)
    shorter_msg, longer_msg = generate_short_and_long_weather_forecast_messages(forecast, owner_name, testing)
    shorter_audio = tts.audio(text=shorter_msg)
    longer_audio = tts.audio(text=longer_msg)
    return {'shorter msg': shorter_msg, 'shorter audio':shorter_audio, 'longer msg': longer_msg, 'longer audio':longer_audio}


