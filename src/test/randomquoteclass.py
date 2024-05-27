# -*- coding: utf-8 -*-
""""test.randomquotesclass

Created on May 21, 2024

@author: Tom Blackshaw
"""
import time
import unittest
from my.randomquotes import RandomQuoteSingleton as q


class TestOne(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSimple(self):
        self.assertGreater(len(q.quote), 4)

    def testAnUpdate(self):
        first_quote = q.quote
        time.sleep(3)
        q.force_update()
        second_quote = q.quote
        self.assertNotEqual(first_quote, second_quote, """I retrieved two quotes -
{first_quote}
and
{second_quote}
- from ZenQuotes. They match! Why?""".format(first_quote=first_quote, second_quote=second_quote))
        time.sleep(3)

# class TestOverloadZenquotesServer(unittest.TestCase):
#
#     def setUp(self):
#         pass
#
#     def tearDown(self):
#         pass
#
#     def testOverloadServer(self):
#
#         def myfunc(noofattempts=32):
#             for i in range(0, noofattempts):
#                 q.force_update()
#                 s = q.quote
#                 self.assertLess(s.lower().find('zenquotes.io'), 0)
#             raise WebAPIOverloadError("After {noofattempts} attempts to overload the server, we haven't received a single 'Server Overloaded' error. That's weird, but OK...".format(noofattempts=noofattempts))
#
#         self.assertRaises(WebAPIOverloadError, myfunc)
#         time.sleep(60)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
