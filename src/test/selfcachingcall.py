'''
Created on May 21, 2024

@author: Tom Blackshaw
'''
import time, os
import unittest

from my.classes.selfcachingcall import SelfCachingCall
from my.exceptions import StillAwaitingCachedValue

GVAR = 0


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testBBC(self):
        timeout = 3
        d = SelfCachingCall(5, os.system, "ping -W{timeout} -c1 bbc.com > /dev/null 2> /dev/null".format(timeout=timeout))
        time.sleep(timeout)
        self.assertEqual(d.result, 0)
        d.join()

    def testLocalhost(self):
        timeout = 2
        d = SelfCachingCall(timeout, os.system, "ping -W{timeout} -c1 localhost > /dev/null 2> /dev/null".format(timeout=timeout))
        time.sleep(timeout)
        self.assertEqual(d.result, 0)
        d.join()

    def testBadURL(self):
        timeout = 2
        d = SelfCachingCall(timeout, os.system, "ping -W{timeout} -c1 www.ahfuioashdfilknsf.com > /dev/null 2> /dev/null".format(timeout=timeout))
        time.sleep(timeout)
        self.assertNotEqual(d.result, 0)
        d.join()

    def testGoofyParams(self):
        def x():
            d = SelfCachingCall(0, os.system("ls / 2> /dev/null > /dev/null"))
            d.join()

        self.assertRaises(ValueError, x)

    def testPrematureResultAccess(self):
        pauselen = .2

        def myfunc():
            global GVAR
            time.sleep(pauselen)
            GVAR += 1
            return GVAR * 100

        def getres(c):
            return c.result

        global GVAR
        GVAR = 0
        self.assertEqual(GVAR, 0)
        c = SelfCachingCall(pauselen, myfunc)
        self.assertRaises(StillAwaitingCachedValue, getres, c)
        c.join()

    def testGlobalVarIncrementing(self):
        pauselen = .1
        growthnum = 100

        def myfunc(addme):
            global GVAR
            GVAR += addme
            return GVAR

        global GVAR
        GVAR = 0
        self.assertEqual(GVAR, 0)
        c = SelfCachingCall(pauselen, myfunc, growthnum)
        time.sleep(pauselen / 2)
        for i in range(1, 20):
            time.sleep(pauselen)
            self.assertGreaterEqual(c.result, growthnum * i)
        c.join()

    def testFailureOfCachedFunction(self):
        pauselen = .2

        def myfunc():
            global GVAR
            GVAR += 1
            return GVAR

        def getres(c):
            return c.result

        global GVAR
        GVAR = 999
        self.assertEqual(GVAR, 999)
        c = SelfCachingCall(pauselen, myfunc)
        time.sleep(pauselen)
        self.assertGreaterEqual(c.result, 1000)
        GVAR = 'Hello there. I shall cause myfunc() to fail. Let us see how SelfCachingCall handles this.'
        time.sleep(pauselen * 1.5)
        self.assertRaises(TypeError, getres, c)
        GVAR = 55
        time.sleep(pauselen)
        self.assertLessEqual(c.result, 56)
        c.join()



if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
