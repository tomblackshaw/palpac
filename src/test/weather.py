# -*- coding: utf-8 -*-
""""test.weather

Created on May 20, 2024

@author: Tom Blackshaw
"""
import unittest

from open_meteo.models import Forecast, DailyForecast, CurrentWeather

from my.classes.exceptions import WebAPIOutputError, WebAPITimeoutError
from my.weather import get_latitude_and_longitude


class Test_get_latitude_and_longitude(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_latitude_and_longitude(self):
        a, b = get_latitude_and_longitude()
        self.assertLess(a, 181, "Latitude should be 180 or less")
        self.assertLess(b, 181, "Longitude should be 180 or less")
        self.assertGreater(a, -179, "Latitude should be -180 or more")
        self.assertGreater(b, -179, "Longitude should be -180 or more")
#        self.assertRaises(ValueError, get_latitude_and_longitude, DEFAULT_LATLONG_URL, MAX_LATLONG_TIMEOUT + 1)

    def testWithGoofyURL(self):
        self.assertRaises(ValueError, get_latitude_and_longitude, 'definitely not a URL', 5)
        self.assertRaises(WebAPIOutputError, get_latitude_and_longitude, 'http://cnn.com/nope.nope.nope', 5)
#        self.assertRaises(WebAPIOutputError, get_latitude_and_longitude, DEFAULT_LATLONG_URL + 'qqq', 5)

#    def testWithGoofyTimeout(self):
#        self.assertRaises(WebAPITimeoutError, get_latitude_and_longitude, DEFAULT_LATLONG_URL, .0001)


class TestWeather(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testDailies(self):
        from my.weather import WeatherSingleton as w
        forecast = w.forecast
#        self.assertEqual(type(w), _WeatherClass)
        self.assertEqual(type(forecast), Forecast)
        self.assertEqual(type(forecast.daily), DailyForecast)
        self.assertEqual(type(forecast.current_weather), CurrentWeather)

    def testGoofyGetWeatherValues(self):
        from my.weather import get_weather
#        _ = get_weather()
        self.assertRaises(TypeError, get_weather)
        self.assertRaises(ValueError, get_weather, None, 69)
        self.assertRaises(ValueError, get_weather, 69, None)
        self.assertRaises(ValueError, get_weather, 181, -181)
        self.assertRaises(ValueError, get_weather, -181, 181)
        self.assertRaises(TypeError, get_weather, "hi", "there")


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
