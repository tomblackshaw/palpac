'''
Created on May 22, 2024

@author: Tom Blackshaw

text2speech test
'''
import unittest
from my.text2speech import generate_alarm_message


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testGoofy(self):
        self.assertRaises(TypeError, generate_alarm_message, None, None, None, None, None, None)
        self.assertRaises(TypeError, generate_alarm_message, None, None, None, None, None)
        self.assertRaises(ValueError, generate_alarm_message, None, None, None, None)
        self.assertRaises(TypeError, generate_alarm_message, None, None, None)
        self.assertRaises(TypeError, generate_alarm_message, None, None)
        self.assertRaises(TypeError, generate_alarm_message, None)
        self.assertRaises(TypeError, generate_alarm_message)
        self.assertRaises(TypeError, generate_alarm_message, '')
        self.assertRaises(ValueError, generate_alarm_message, 'Biggles', -1, 0, 'Simple template')
        self.assertRaises(ValueError, generate_alarm_message, 'Biggles', 'minus one', 'zero', 'Simple template')
        self.assertRaises(ValueError, generate_alarm_message, 'Biggles', 0, 99, 'Simple template')
        self.assertRaises(ValueError, generate_alarm_message, 'Biggles', 24, 0, 'Simple template')
        self.assertRaises(ValueError, generate_alarm_message, 'Biggles', 0, 60, 'Simple template')
        self.assertRaises(ValueError, generate_alarm_message, 'Biggles', 24, 60, 'Simple template')

    def testThis(self):
        for owner_name in ('Bill', 'Ted', 'Excellent', 'Adventure'):
            for time_24h in range(0, 24):
                for time_minutes in range(0, 60):
                    _ = generate_alarm_message(owner_name, time_24h, time_minutes, 'Simple template ${shorttime} ${owner} yep yep')
                    self.assertRaises(KeyError, generate_alarm_message, owner_name, time_24h, time_minutes, 'Simple ${wtf_is_this} template')


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
