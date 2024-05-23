# -*- coding: utf-8 -*-
'''
Created on May 22, 2024

@author: Tom Blackshaw

text2speech test
'''
import random
import unittest


from my.text2speech import generate_alarm_message, Text2SpeechSingleton as tts


class TestOne(unittest.TestCase):

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

    def testFieldAdvanced(self):
        for i in (True, False, True, True, False, False, True, False):
            tts.advanced = i
            self.assertEqual(tts.advanced, i)

        def myfunc():
            tts.advanced = 'Foo'

        self.assertRaises(TypeError, myfunc)

    def testFieldStability(self):
        for _ in range(0, 100):
            x = random.randint(0, 100) / 100
            tts.stability = x
            self.assertEqual(tts.stability, x)

        def myfunc():
            tts.stability = 'Foo'

        self.assertRaises(TypeError, myfunc)

    def testFieldSimilarity(self):
        for _ in range(0, 100):
            x = random.randint(0, 100) / 100
            tts.similarity = x
            self.assertEqual(tts.similarity, x)

        def myfunc():
            tts.similarity = 'Foo'

        self.assertRaises(TypeError, myfunc)

    def testFieldStyle(self):
        for _ in range(0, 100):
            x = random.randint(0, 100) / 100
            tts.style = x
            self.assertEqual(tts.style, x)

        def myfunc():
            tts.style = 'Foo'

        self.assertRaises(TypeError, myfunc)

    def testFieldBoost(self):
        for i in (True, False, True, True, False, False, True, False):
            tts.boost = i
            self.assertEqual(tts.boost, i)

        def myfunc():
            tts.boost = 'Foo'

        self.assertRaises(TypeError, myfunc)

    def testGetModelsAndVoices(self):
        from elevenlabs.types.model import Model
        from elevenlabs.types.voice import Voice
        self.assertEqual(type(tts.api_models[0]), Model)
        self.assertEqual(type(tts.api_voices[0]), Voice)

    def testFieldModel(self):
        all_possibilities = [r.model_id for r in tts.api_models]
        for i in all_possibilities:
            tts.model = i
            self.assertEqual(tts.model, i)

        def myfuncI():
            tts.model = 'Foo'

        def myfuncV():
            tts.model = 12345

        self.assertRaises(ValueError, myfuncI)
        self.assertRaises(TypeError, myfuncV)

    def testFieldName(self):  # test field 'name', not 'fieldname'
        all_possibilities = tts.all_names
        for i in all_possibilities:
            tts.name = i
            self.assertEqual(tts.name, i)

        def myfuncI():
            tts.name = 'Foo'

        def myfuncV():
            tts.name = 12345

        self.assertRaises(ValueError, myfuncI)
        self.assertRaises(TypeError, myfuncV)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
