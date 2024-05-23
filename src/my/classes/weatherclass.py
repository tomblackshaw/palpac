# -*- coding: utf-8 -*-
"""my.classes.weatherclass

Created on May 21, 2024

@author: Tom Blackshaw

This module demonstrates documentation. Docstrings may extend over multiple lines. Sections are created
with a section header and a colon followed by a block of indented text.

Example:
    Examples can be given using either the ``Example`` or ``Examples``
    sections. Sections support any reStructuredText formatting, including
    literal blocks::

        $ python example_google.py

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

.. _Style Guide:
    https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

"""

from my.classes import singleton
from my.classes.selfcachingcall import SelfCachingCall
from my.exceptions import StillAwaitingCachedValue, WebAPITimeoutError, WebAPIOutputError


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
