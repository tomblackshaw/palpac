# -*- coding: utf-8 -*-
"""my.classes.weatherclass

Created on May 21, 2024

@author: Tom Blackshaw

This module wraps around the OpenMeteo weather API by providing a
cached result of periodic call to that API.

Example:
    Like this::

        $ python3
        >>> from my.classes.weatherclass import WeatherSingleton as ws
        >>> i = ws.weather
        >>> print(i)

Attributes:
    WeatherSingleton (_WeatherClass): Singleton to be imported for
        retrieving some weather info. It is a singleton.

.. _Style Guide:
   https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

"""

from my.classes import singleton
from my.classes.selfcachingcall import SelfCachingCall
from my.classes.exceptions import StillAwaitingCachedValue, WebAPITimeoutError, WebAPIOutputError


@singleton
class _WeatherClass:
    """Returns the cached result of a call to get_weather().

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

    def __init__(self):
        from my.weather.meteorology import get_weather
        self._our_weather_caching_call = SelfCachingCall(300, get_weather)
        super().__init__()

    @property
    def weather(self):
        """:obj:`list` of :obj:`str`: Properties with both a getter and setter
        should only be documented in their getter method.

        If the setter method contains notable behavior, it should be
        mentioned here.
        """
        try:
            return self._our_weather_caching_call.result
        except StillAwaitingCachedValue:
            self._our_weather_caching_call.update_me()
            return self.weather
        except TimeoutError as e:
            raise WebAPITimeoutError("The openmeteo website timed out") from e
        except WebAPIOutputError:
            raise WebAPIOutputError("The openmeteo website returned an incomprehensible output") from e


WeatherSingleton = _WeatherClass()
