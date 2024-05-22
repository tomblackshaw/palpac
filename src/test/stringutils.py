'''
Created on May 20, 2024

@author: Tom Blackshaw
'''
import random
import unittest

from my.stringutils import generate_random_string, MAX_RANDGENSTR_LEN, convert_24h_and_mins_to_shorttime


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
        self.assertRaises(TypeError, generate_random_string, MAX_RANDGENSTR_LEN + 1)
        self.assertRaises(TypeError, generate_random_string, -1)
        _ = generate_random_string(MAX_RANDGENSTR_LEN)
        self.assertEqual(generate_random_string(0), '')
        for i in range(0, 100):
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
        self.assertEqual(convert_24h_and_mins_to_shorttime(0, 0, -1), "11:59AM")
        self.assertEqual(convert_24h_and_mins_to_shorttime(0, 0), "12 midnight")
        self.assertEqual(convert_24h_and_mins_to_shorttime(12, 0), "12 noon")
        self.assertEqual(convert_24h_and_mins_to_shorttime(23, 59, 1), "12 midnight")
        self.assertEqual(convert_24h_and_mins_to_shorttime(0, 1, -1), "12 midnight")
        self.assertEqual(convert_24h_and_mins_to_shorttime(12, 1, -1), "12 noon")
        self.assertEqual(convert_24h_and_mins_to_shorttime(11, 59, 1), "12 noon")
        for diff in range(0,5):
            for h in range(0, 23):
                for m in range(0, 60):
                    s1 = convert_24h_and_mins_to_shorttime(h, m)
                    s2 = convert_24h_and_mins_to_shorttime(h, m, diff)

        for i in range(0, 1000):
            s = convert_24h_and_mins_to_shorttime(0, 59)
            diff = random.randint(0, 120) - 60
            s = convert_24h_and_mins_to_shorttime(0, 59, diff)
        for hr in range(0,24):
            for mn in range(0, 60):
                s = convert_24h_and_mins_to_shorttime(hr, mn)
        del i, s


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

