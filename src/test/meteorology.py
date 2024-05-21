'''
Created on May 20, 2024

@author: Tom Blackshaw
'''
import unittest

from my.exceptions import WebAPIOutputError, WebAPITimeoutError
from my.globals import MAX_LATLONG_TIMEOUT, DEFAULT_LATLONG_URL
from my.weather.meteorology import get_lat_and_long


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


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
