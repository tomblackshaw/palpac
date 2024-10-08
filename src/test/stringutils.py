# -*- coding: utf-8 -*-
"""test.stringutils

Created on May 20, 2024

@author: Tom Blackshaw
"""
import random
import unittest
from my.stringutils import convert_24h_and_mins_to_shorttime, url_validator, generate_random_string, MAX_RANDGENSTR_LEN



class TestGenerateRandomString(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testThis(self):

        self.assertRaises(TypeError, generate_random_string)
        self.assertRaises(TypeError, generate_random_string, 'x')
        self.assertRaises(TypeError, generate_random_string, '')
        self.assertRaises(TypeError, generate_random_string, True)
        self.assertRaises(TypeError, generate_random_string, None)
        self.assertRaises(ValueError, generate_random_string, MAX_RANDGENSTR_LEN + 1)
        self.assertRaises(ValueError, generate_random_string, -1)
        self.assertRaises(ValueError, generate_random_string, 0)
        # _ = generate_random_string(MAX_RANDGENSTR_LEN)
        # self.assertEqual(generate_random_string(0), '')
        for i in range(1, 100):
            self.assertEqual(i, len(generate_random_string(i)))


class TestConvert24hAndMinsToShorttime(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testGoofy(self):
        self.assertRaises(TypeError, convert_24h_and_mins_to_shorttime)
        self.assertRaises(TypeError, convert_24h_and_mins_to_shorttime, None, None)
        self.assertRaises(TypeError, convert_24h_and_mins_to_shorttime, 'Hi', 'there')
        self.assertRaises(ValueError, convert_24h_and_mins_to_shorttime, -1, -1)
        self.assertRaises(ValueError, convert_24h_and_mins_to_shorttime, 99, 99)
        self.assertRaises(ValueError, convert_24h_and_mins_to_shorttime, 0, 99)
        self.assertRaises(ValueError, convert_24h_and_mins_to_shorttime, 99, 0)
        self.assertRaises(ValueError, convert_24h_and_mins_to_shorttime, 24, 0)
        self.assertRaises(ValueError, convert_24h_and_mins_to_shorttime, 0, 60)

    def testDiff(self):
        self.assertEqual(convert_24h_and_mins_to_shorttime(0, 0, -1), "11:59PM")
        self.assertEqual(convert_24h_and_mins_to_shorttime(0, 0), "12 midnight")
        self.assertEqual(convert_24h_and_mins_to_shorttime(12, 0), "12 newn")
        self.assertEqual(convert_24h_and_mins_to_shorttime(23, 59, 1), "12 midnight")
        self.assertEqual(convert_24h_and_mins_to_shorttime(0, 1, -1), "12 midnight")
        self.assertEqual(convert_24h_and_mins_to_shorttime(12, 1, -1), "12 newn")
        self.assertEqual(convert_24h_and_mins_to_shorttime(11, 59, 1), "12 newn")
        self.assertEqual(convert_24h_and_mins_to_shorttime(7, 0), "7AM")
        self.assertEqual(convert_24h_and_mins_to_shorttime(19, 0), "7PM")
        for diff in range(0,5):
            for h in range(0, 23):
                for m in range(0, 60):
                    s1 = convert_24h_and_mins_to_shorttime(h, m)
                    s2 = convert_24h_and_mins_to_shorttime(h, m, diff)
        del s1, s2

    def testMore(self):
        for i in range(0, 1000):
            s = convert_24h_and_mins_to_shorttime(0, 59)
            diff = random.randint(0, 120) - 60
            s = convert_24h_and_mins_to_shorttime(0, 59, diff)
        for hr in range(0,24):
            for mn in range(0, 60):
                s = convert_24h_and_mins_to_shorttime(hr, mn)
        del i, s

    def testWeirdOnes(self):
        self.assertEqual(convert_24h_and_mins_to_shorttime(11, 5), "11:05AM")
        self.assertEqual(convert_24h_and_mins_to_shorttime(23, 5), "11:05PM")


class TestURLValidator(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testGoofy(self):
        self.assertRaises(TypeError, url_validator)
        self.assertRaises(TypeError, url_validator, None)
        self.assertRaises(TypeError, url_validator, 1)
        self.assertRaises(TypeError, url_validator, [1, 2, 3])
        self.assertEqual(False, url_validator('qqqq://123'))
        self.assertEqual(False, url_validator(''))
        self.assertEqual(True, url_validator('https://microsoft.com'))

# class TestText2Time(unittest.TestCase):
#
#     def setUp(self):
#         pass
#
#     def tearDown(self):
#         pass
#
#     def testGoofy(self):
#         self.assertRaises(TypeError, text2time, None)
#         self.assertRaises(TypeError, text2time, 12)
#         self.assertRaises(TypeError, text2time, 12.44)
# #        self.assertRaises(ValueError, text2time, "twenty five")
#         self.assertRaises(ValueError, text2time, "minus one")
#         self.assertRaises(ValueError, text2time, "twelve sixty nine")
#
#     def testMidnightMidday(self):
#         self.assertEqual(text2time("twelve newn"), (12, 0))
#         self.assertEqual(text2time("newn"), (12, 0))
#         self.assertEqual(text2time("twelve midnight"), (0, 0))
#         self.assertEqual(text2time("midnight"), (0, 0))
#
#     def testHourAlone(self):
#         self.assertEqual(text2time("twelve am"), (0,0))
#         self.assertEqual(text2time("one am"), (1,0))
#         self.assertEqual(text2time("two am"), (2,0))
#         self.assertEqual(text2time("three am"), (3,0))
#         self.assertEqual(text2time("four am"), (4,0))
#         self.assertEqual(text2time("five am"), (5,0))
#         self.assertEqual(text2time("six am"), (6,0))
#         self.assertEqual(text2time("seven am"), (7,0))
#         self.assertEqual(text2time("eight am"), (8,0))
#         self.assertEqual(text2time("nine am"), (9,0))
#         self.assertEqual(text2time("ten am"), (10,0))
#         self.assertEqual(text2time("eleven am"), (11,0))
#         self.assertEqual(text2time("twelve pm"), (12,0))
#
#     def testHundred(self):
#         self.assertEqual(text2time("twenty four hundred"), (0,0))
#         self.assertEqual(text2time("zero hundred"), (0,0))
#         self.assertEqual(text2time("one hundred"), (1,0))
#         self.assertEqual(text2time("two hundred"), (2,0))
#         self.assertEqual(text2time("three hundred"), (3,0))
#         self.assertEqual(text2time("four hundred"), (4,0))
#         self.assertEqual(text2time("five hundred"), (5,0))
#         self.assertEqual(text2time("six hundred"), (6,0))
#         self.assertEqual(text2time("seven hundred"), (7,0))
#         self.assertEqual(text2time("eight hundred"), (8,0))
#         self.assertEqual(text2time("nine hundred"), (9,0))
#         self.assertEqual(text2time("ten hundred"), (10,0))
#         self.assertEqual(text2time("eleven hundred"), (11,0))
#         self.assertEqual(text2time("twelve hundred"), (12,0))
#         self.assertEqual(text2time("thirteen hundred"), (13,0))
#         self.assertEqual(text2time("fourteen hundred"), (14,0))
#         self.assertEqual(text2time("fifteen hundred"), (15,0))
#         self.assertEqual(text2time("sixteen hundred"), (16,0))
#         self.assertEqual(text2time("seventeen hundred"), (17,0))
#         self.assertEqual(text2time("eighteen hundred"), (18,0))
#         self.assertEqual(text2time("nineteen hundred"), (19,0))
#         self.assertEqual(text2time("twenty hundred"), (20,0))
#         self.assertEqual(text2time("twenty one hundred"), (21,0))
#         self.assertEqual(text2time("twenty two hundred"), (22,0))
#         self.assertEqual(text2time("twenty three hundred"), (23,0))
#
#     def testHundrHours(self):
#         self.assertEqual(text2time("twenty four hundred hours"), (0,0))
#         self.assertEqual(text2time("zero hundred hours"), (0,0))
#         self.assertEqual(text2time("one hundred hours"), (1,0))
#         self.assertEqual(text2time("two hundred hours"), (2,0))
#         self.assertEqual(text2time("three hundred hours"), (3,0))
#         self.assertEqual(text2time("four hundred hours"), (4,0))
#         self.assertEqual(text2time("five hundred hours"), (5,0))
#         self.assertEqual(text2time("six hundred hours"), (6,0))
#         self.assertEqual(text2time("seven hundred hours"), (7,0))
#         self.assertEqual(text2time("eight hundred hours"), (8,0))
#         self.assertEqual(text2time("nine hundred hours"), (9,0))
#         self.assertEqual(text2time("ten hundred hours"), (10,0))
#         self.assertEqual(text2time("eleven hundred hours"), (11,0))
#         self.assertEqual(text2time("twelve hundred hours"), (12,0))
#         self.assertEqual(text2time("thirteen hundred hours"), (13,0))
#         self.assertEqual(text2time("fourteen hundred hours"), (14,0))
#         self.assertEqual(text2time("fifteen hundred hours"), (15,0))
#         self.assertEqual(text2time("sixteen hundred hours"), (16,0))
#         self.assertEqual(text2time("seventeen hundred hours"), (17,0))
#         self.assertEqual(text2time("eighteen hundred hours"), (18,0))
#         self.assertEqual(text2time("nineteen hundred hours"), (19,0))
#         self.assertEqual(text2time("twenty hundred hours"), (20,0))
#         self.assertEqual(text2time("twenty one hundred hours"), (21,0))
#         self.assertEqual(text2time("twenty two hundred hours"), (22,0))
#         self.assertEqual(text2time("twenty three hundred hours"), (23,0))
#
#     def testEdges(self):
#         self.assertEqual(text2time("twelve oh one am"), (0, 1))
#         self.assertEqual(text2time("one oh one am"), (1, 1))
#         self.assertEqual(text2time("twelve oh one pm"), (12, 1))
#         self.assertEqual(text2time("one oh one pm"), (13, 1))
#
#     def testManyCombos(self):
#         all_times_str = ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve',
#                      'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty',
#                      'twenty one', 'twenty two', 'twenty three', 'twenty four', 'twenty five', 'twenty six', 'twenty seven', 'twenty eight', 'twenty nine', 'thirty',
#                      'thirty one', 'thirty two', 'thirty three', 'thirty four', 'thirty five', 'thirty six', 'thirty seven', 'thirty eight', 'thirty nine', 'forty',
#                      'forty one', 'forty two', 'forty three', 'forty four', 'forty five', 'forty six', 'forty seven', 'forty eight', 'forty nine', 'fifty',
#                      'fifty one', 'fifty two', 'fifty three', 'fifty four', 'fifty five', 'fifty six', 'fifty seven', 'fifty eight', 'fifty nine', 'sixty']
#         for hour_num in range(1, 12):
#             for minute_num in range(0, 60):
#                 hour_str = all_times_str[hour_num]
#                 minute_str = all_times_str[minute_num]
#                 if 0 < minute_num < 10:
#                     minute_str = 'oh ' + minute_str
#                 s = '{h} {m} am'.format(h=hour_str, m=minute_str).replace('  ', ' ').strip()
#                 returned_hr, returned_min = text2time(s)
#                 self.assertEqual((hour_num, minute_num), (returned_hr, returned_min), "{hr}:{min} => {s} => {returned_hr}:{returned_min}".format(
#                     hr=hour_num, min=minute_num, s=s, returned_hr=returned_hr, returned_min=returned_min))
#
#         for hour_num in range(1, 12):
#             for minute_num in range(0, 60):
#                 hour_str = all_times_str[hour_num]
#                 minute_str = all_times_str[minute_num]
#                 if 0 < minute_num < 10:
#                     minute_str = 'oh ' + minute_str
#                 s = '{h} {m} pm'.format(h=hour_str, m=minute_str).replace('  ', ' ').strip()
#                 returned_hr, returned_min = text2time(s)
#                 self.assertEqual((hour_num + 12, minute_num), (returned_hr, returned_min), "{hr}:{min} => {s} => {returned_hr}:{returned_min}".format(
#                     hr=hour_num, min=minute_num, s=s, returned_hr=returned_hr, returned_min=returned_min))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

