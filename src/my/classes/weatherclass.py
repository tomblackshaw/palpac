'''
Created on May 21, 2024

@author: Tom Blackshaw
'''

from my.classes import singleton
from my.classes.selfcachingcall import SelfCachingCall
from my.exceptions import StillAwaitingCachedValue, WebAPITimeoutError, WebAPIOutputError


@singleton
class _WeatherClass(object):
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
