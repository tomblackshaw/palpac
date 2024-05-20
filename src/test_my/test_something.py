'''
Created on May 20, 2024

@author: Tom Blackshaw
'''
import unittest
from my.stringstuff import generate_random_string, MAX_RANDGENSTR_LEN


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testGenerateRandomString(self):

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


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

