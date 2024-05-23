# -*- coding: utf-8 -*-
"""my.weather

Created on May 19, 2024

@author: Tom Blackshaw

This module contains goodies related to the weather. This file is the
__init__.py file and doesn't do very much at the moment.

Example:
    from my.text2speech import Text2SpeechSingleton as tts
    from my.classes.weatherclass import WeatherSingleton as w
    from my.weather.meteorology import do_a_weather_report
    import random
    prof_name= [r for r in tts.voiceinfo if r.samples is not None][0].name
    do_a_weather_report(tts=tts, testing=True, myweather=w.weather,
                speaker1 = prof_name,
                speaker2 = "Freya",
                stability=0.10, similarity_boost=0.01, style=0.9)

Section breaks are created by resuming unindented text. Section breaks
are also implicitly created anytime a new section starts.

Attributes:
    n/a

Todo:
    * For module TODOs
    * You have to also use ``sphinx.ext.todo`` extension

.. _Style Guide:
    https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

"""


