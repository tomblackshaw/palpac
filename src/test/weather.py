# -*- coding: utf-8 -*-
'''
Created on May 20, 2024

@author: Tom Blackshaw
'''
import unittest

from open_meteo.models import Forecast, DailyForecast, CurrentWeather

from my.classes.exceptions import WebAPIOutputError, WebAPITimeoutError
from my.globals import MAX_LATLONG_TIMEOUT, DEFAULT_LATLONG_URL
from my.weather import get_lat_and_long, _WeatherClass
import my.weather


class Test_get_lat_and_long(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_lat_and_long(self):
        a, b = get_lat_and_long()
        self.assertLess(a, 181, "Latitude should be 180 or less")
        self.assertLess(b, 181, "Longitude should be 180 or less")
        self.assertGreater(a, -179, "Latitude should be -180 or more")
        self.assertGreater(b, -179, "Longitude should be -180 or more")
        self.assertRaises(ValueError, get_lat_and_long, DEFAULT_LATLONG_URL, MAX_LATLONG_TIMEOUT + 1)

    def testWithGoofyURL(self):
        self.assertRaises(ValueError, get_lat_and_long, 'definitely not a URL', 5)
        self.assertRaises(WebAPIOutputError, get_lat_and_long, 'http://cnn.com/nope.nope.nope', 5)
        self.assertRaises(WebAPIOutputError, get_lat_and_long, DEFAULT_LATLONG_URL + 'qqq', 5)

    def testWithGoofyTimeout(self):
        self.assertRaises(WebAPITimeoutError, get_lat_and_long, DEFAULT_LATLONG_URL, .0001)


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


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
