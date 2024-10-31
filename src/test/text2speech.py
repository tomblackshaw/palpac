# -*- coding: utf-8 -*-
"""test.text2speech

Created on May 22, 2024

@author: Tom Blackshaw

text2speech test
"""

import random
import unittest
from my.text2speech import *
from my.stringutils import *
from my.consts import *

from my.stringutils import generate_detokenized_message, pathname_of_phrase_audio, list_files_in_dir
from my.text2speech import Text2SpeechSingleton as tts, deliberately_cache_a_smart_phrase,\
    get_list_of_files_for_speaking_a_random_alarm_message, smart_phrase_filenames
import os
from my.consts import hello_owner_lst, OWNER_NAME
from my.classes.exceptions import MissingFromCacheError
from regen_cache_for_voice import cache_this_smart_phrase
from my.cachedspeech import smart_phrase_audio


# class TestOne(unittest.TestCase):
#
#     def setUp(self):
#         pass
#
#     def tearDown(self):
#         pass
#
#     def testGoofy(self):
#         self.assertRaises(TypeError, generate_detokenized_message, None, None, None, None, None, None)
#         self.assertRaises(TypeError, generate_detokenized_message, None, None, None, None, None)
#         self.assertRaises(ValueError, generate_detokenized_message, None, None, None, None)
#         self.assertRaises(TypeError, generate_detokenized_message, None, None, None)
#         self.assertRaises(TypeError, generate_detokenized_message, None, None)
#         self.assertRaises(TypeError, generate_detokenized_message, None)
#         self.assertRaises(TypeError, generate_detokenized_message)
#         self.assertRaises(TypeError, generate_detokenized_message, '')
#         self.assertRaises(ValueError, generate_detokenized_message, 'Biggles', -1, 0, 'Simple template')
#         self.assertRaises(ValueError, generate_detokenized_message, 'Biggles', 'minus one', 'zero', 'Simple template')
#         self.assertRaises(ValueError, generate_detokenized_message, 'Biggles', 0, 99, 'Simple template')
#         self.assertRaises(ValueError, generate_detokenized_message, 'Biggles', 24, 0, 'Simple template')
#         self.assertRaises(ValueError, generate_detokenized_message, 'Biggles', 0, 60, 'Simple template')
#         self.assertRaises(ValueError, generate_detokenized_message, 'Biggles', 24, 60, 'Simple template')
#
#     def testThis(self):
#         for owner_name in ('Bill', 'Ted', 'Excellent', 'Adventure'):
#             for time_24h in range(0, 24):
#                 for time_minutes in range(0, 60):
#                     _ = generate_detokenized_message(owner_name, time_24h, time_minutes, 'Simple template ${shorttime} ${owner} yep yep')
#                     self.assertRaises(KeyError, generate_detokenized_message, owner_name, time_24h, time_minutes, 'Simple ${wtf_is_this} template')
#
#     def testFieldAdvanced(self):
#         for i in (True, False, True, True, False, False, True, False):
#             tts.advanced = i
#             self.assertEqual(tts.advanced, i)
#
#         def myfunc():
#             tts.advanced = 'Foo'
#
#         self.assertRaises(ValueError, myfunc)
#
#     def testFieldStability(self):
#         for _ in range(0, 100):
#             x = random.randint(0, 100) / 100
#             tts.stability = x
#             self.assertEqual(tts.stability, x)
#
#         def myfunc():
#             tts.stability = 'Foo'
#
#         self.assertRaises(TypeError, myfunc)
#
#     def testFieldSimilarity(self):
#         for _ in range(0, 100):
#             x = random.randint(0, 100) / 100
#             tts.similarity = x
#             self.assertEqual(tts.similarity, x)
#
#         def myfunc():
#             tts.similarity = 'Foo'
#
#         self.assertRaises(TypeError, myfunc)
#
#     def testFieldStyle(self):
#         for _ in range(0, 100):
#             x = random.randint(0, 100) / 100
#             tts.style = x
#             self.assertEqual(tts.style, x)
#
#         def myfunc():
#             tts.style = 'Foo'
#
#         self.assertRaises(TypeError, myfunc)
#
#     def testFieldBoost(self):
#         for i in (True, False, True, True, False, False, True, False):
#             tts.boost = i
#             self.assertEqual(tts.boost, i)
#
#         def myfunc():
#             tts.boost = 'Foo'
#
#         self.assertRaises(TypeError, myfunc)
#
#     def testGetModelsAndVoices(self):
#         from elevenlabs.types.model import Model
#         from elevenlabs.types.voice import Voice
#         self.assertEqual(type(tts.api_models[0]), Model)
#         self.assertEqual(type(tts.api_voices[0]), Voice)
#
#     def testFieldModel(self):
#         all_possibilities = [r.model_id for r in tts.api_models]
#         for i in all_possibilities:
#             tts.model = i
#             self.assertEqual(tts.model, i)
#
#         # def myfuncI():
#         #     tts.model = 'Foo'
#         #
#         # def myfuncV():
#         #     tts.model = 12345
#         #
#         # self.assertRaises(ValueError, myfuncI)
#         # self.assertRaises(TypeError, myfuncV)
#
#     # def testTheFieldKnownAs_Voice(self): 
#     #     all_possibilities = tts.all_voices
#     #     for i in all_possibilities:
#     #         tts.voice = i
#     #         self.assertEqual(tts.voice, i)
#     #
#     #     def myfuncI():
#     #         tts.voice = 'Foo'
#     #
#     #     def myfuncV():
#     #         tts.voice = 12345
#     #
#     #     self.assertRaises(ValueError, myfuncI)
#     #     self.assertRaises(TypeError, myfuncV)
#
# class Test_deliberately_cache_a_smart_phrase(unittest.TestCase):
#
#     def setUp(self):
#         pass
#
#     def tearDown(self):
#         pass
#
#     def testDuffParams(self):
#         self.assertRaises(TypeError, lambda : deliberately_cache_a_smart_phrase(voice=None, smart_phrase="One"))
#         self.assertRaises(ValueError, lambda : deliberately_cache_a_smart_phrase(voice='AAAAA', smart_phrase="One"))
#         self.assertFalse(os.path.exists('audio/cache/AAAAA'))
#         self.assertRaises(TypeError, lambda : deliberately_cache_a_smart_phrase(voice='Aria', smart_phrase=None))
#
#     def testSpeakOne(self):
#         for voice in ('Laura','Sarah'):
#             all_oggs = []
#             all_mp3s = []
#             os.system('rm %s/{*,.*ogg,.*mp3}' % pathname_of_phrase_audio(voice))
#             os.system('rmdir %s' % pathname_of_phrase_audio(voice))
#             for phrase in ('one', 'One', 'onE'):
#                 path_ogg = pathname_of_phrase_audio(voice, phrase, suffix='ogg')
#                 path_mp3 = pathname_of_phrase_audio(voice, phrase, suffix='mp3')
#                 path_dft = pathname_of_phrase_audio(voice, phrase)
#                 all_oggs.append(path_ogg)
#                 all_mp3s.append(path_mp3)
#                 self.assertEqual(path_ogg, path_dft)
#                 self.assertEqual(path_ogg[-4:], '.ogg')
#                 self.assertEqual(path_mp3[-4:], '.mp3')
#                 if os.path.exists(path_ogg):
#                     os.unlink(path_ogg)
#                 if os.path.exists(path_mp3):
#                     os.unlink(path_mp3)
#                 self.assertFalse(os.path.exists(path_ogg))
#                 self.assertFalse(os.path.exists(path_mp3))
#                 deliberately_cache_a_smart_phrase(voice=voice, smart_phrase=phrase)
#                 self.assertTrue(os.path.exists(path_ogg))
#                 self.assertTrue(os.path.exists(path_mp3))
#             self.assertEqual(list(set(all_mp3s))[0], all_mp3s[0])
#             self.assertEqual(list(set(all_oggs))[0], all_oggs[0])
#
#     def testSpeakTwo(self):
#         voice = 'River'
#         os.system('rm %s/{*,.*ogg,.*mp3}' % pathname_of_phrase_audio(voice))
#         os.system('rmdir %s' % pathname_of_phrase_audio(voice))
#         self.assertRaises(TypeError, lambda : deliberately_cache_a_smart_phrase(voice=voice, smart_phrase=None))
#         self.assertRaises(ValueError, lambda: deliberately_cache_a_smart_phrase(voice=voice, smart_phrase=""))
#         self.assertRaises(ValueError, lambda: deliberately_cache_a_smart_phrase(voice=voice, smart_phrase=" "))
#         self.assertFalse(os.path.exists(pathname_of_phrase_audio(voice, 'two', 'mp3')))
#         self.assertFalse(os.path.exists(pathname_of_phrase_audio(voice, 'two', 'ogg')))
#         self.assertFalse(os.path.exists(pathname_of_phrase_audio(voice, 'two')))
#         deliberately_cache_a_smart_phrase(voice=voice, smart_phrase=" Two ")
#         self.assertTrue(os.path.exists(pathname_of_phrase_audio(voice, 'two', 'mp3')))
#         self.assertTrue(os.path.exists(pathname_of_phrase_audio(voice, 'twO', 'ogg')))
#         self.assertTrue(os.path.exists(pathname_of_phrase_audio(voice, 'tWo')))
#         self.assertTrue(os.path.exists(pathname_of_phrase_audio(voice, 'two ', 'mp3')))
#         self.assertTrue(os.path.exists(pathname_of_phrase_audio(voice, ' twO', 'ogg')))
#         self.assertTrue(os.path.exists(pathname_of_phrase_audio(voice, 'tWo ')))
#         self.assertTrue(os.path.exists(pathname_of_phrase_audio(voice, ' tWo')))
#         self.assertTrue(os.path.exists(pathname_of_phrase_audio(voice, ' tWo ')))
#         self.assertFalse(os.path.exists(pathname_of_phrase_audio(voice)))
#         self.assertFalse(os.path.exists(pathname_of_phrase_audio(voice, ' ')))
#         oggfiles = list_files_in_dir(pathname_of_phrase_audio(voice), endswith_str='ogg')
#         mp3files = list_files_in_dir(pathname_of_phrase_audio(voice), endswith_str='mp3')
#         allfiles = list_files_in_dir(pathname_of_phrase_audio(voice))
#         self.assertEqual(oggfiles, ['two.ogg'])
#         self.assertEqual(mp3files, ['two.mp3'])
#         self.assertEqual(allfiles, ['two.ogg','two.mp3'])
#
#
#     def testJustUsePunctuation(self):
#         voice = 'Laura'
#         os.system('mkdir "%s"' % pathname_of_phrase_audio(voice))
#         os.system('rm %s/{*,.*ogg,.*mp3}' % pathname_of_phrase_audio(voice))
#         self.assertEqual([], list_files_in_dir(pathname_of_phrase_audio(voice)))
#         self.assertRaises(ValueError, lambda: deliberately_cache_a_smart_phrase(voice, ' ?'))
#         self.assertRaises(ValueError, lambda: deliberately_cache_a_smart_phrase(voice, '!'))
#         self.assertRaises(ValueError, lambda: deliberately_cache_a_smart_phrase(voice, '.'))
#         self.assertRaises(ValueError, lambda: deliberately_cache_a_smart_phrase(voice, '...'))
#         self.assertRaises(ValueError, lambda: deliberately_cache_a_smart_phrase(voice, ' ... '))
#         self.assertEqual([], list_files_in_dir(pathname_of_phrase_audio(voice)))
#
#     def testPunctuatedWords(self):
#         voice = 'Laura'
#         os.system('mkdir "%s"' % pathname_of_phrase_audio(voice))
#         os.system('rm %s/{*,.*ogg,.*mp3}' % pathname_of_phrase_audio(voice))
#         self.assertEqual([], list_files_in_dir(pathname_of_phrase_audio(voice)))
#         self.assertRaises(ValueError, lambda: deliberately_cache_a_smart_phrase(voice, ' ?'))
#         self.assertRaises(ValueError, lambda: deliberately_cache_a_smart_phrase(voice, '!'))
#         self.assertRaises(ValueError, lambda: deliberately_cache_a_smart_phrase(voice, '.'))
#         self.assertRaises(ValueError, lambda: deliberately_cache_a_smart_phrase(voice, '"'))
#         self.assertRaises(ValueError, lambda: deliberately_cache_a_smart_phrase(voice, '...'))
#         self.assertRaises(ValueError, lambda: deliberately_cache_a_smart_phrase(voice, ' ... '))
#         self.assertRaises(ValueError, lambda: deliberately_cache_a_smart_phrase(voice, '" "'))
#         self.assertRaises(ValueError, lambda: deliberately_cache_a_smart_phrase(voice, '" " '))
#         self.assertRaises(ValueError, lambda: deliberately_cache_a_smart_phrase(voice, ' " '))        
#         self.assertEqual([], list_files_in_dir(pathname_of_phrase_audio(voice)))
#
#
#     def testSpeakThreeWithTime(self):
#         voice = 'Laura'
#         os.system('rm %s/{*,.*ogg,.*mp3}' % pathname_of_phrase_audio(voice))
# #        os.system('rmdir %s' % pathname_of_phrase_audio(voice))
# #        self.assertRaises(FileNotFoundError, lambda :list_files_in_dir(pathname_of_phrase_audio(voice)))
#         os.mkdir(pathname_of_phrase_audio(voice))
#         allfiles = list_files_in_dir(pathname_of_phrase_audio(voice))
#         self.assertEqual(allfiles, [])
#         smart_phrase = "${hello_owner}. As Martin Luther King once said, Wake-up delayed is wake-up denied. It is now ${shorttime}."
#         deliberately_cache_a_smart_phrase(voice, smart_phrase)
#         allfiles = list_files_in_dir(pathname_of_phrase_audio(voice))
#         self.assertEqual(allfiles, ["sounds/cache/{voice}/as_martin_luther_king_once_said,_wake-up_delayed_is_wake-up_denied^_it_is_now.mp3".format(voice=voice),
#                                     "sounds/cache/{voice}/as_martin_luther_king_once_said,_wake-up_delayed_is_wake-up_denied^_it_is_now.ogg".format(voice=voice)])



# class Test_generate_detokenized_message(unittest.TestCase):
#
#     def setUp(self):
#         pass
#
#     def tearDown(self):
#         pass
#
#     def testMidnightMessage(self):
#         voice = 'Laura'
#         owner = OWNER_NAME
#         os.system('rm %s/{*,.*ogg,.*mp3}' % pathname_of_phrase_audio(voice))
# #        os.system('rmdir %s' % pathname_of_phrase_audio(voice))
#         message_template = """Hello, %s. It's ${shorttime} and time's a-wasting.""" % owner
#         my_txt = generate_detokenized_message(owner=owner, time_24h=0, time_minutes=0, message_template=message_template)
#         self.assertEqual(my_txt, "Hello, %s. It's 12 midnight and time's a-wasting." % owner)
# #        filenames = smart_phrase_filenames(voice=voice, smart_phrase=my_txt, fail_quietly=True)
# #        self.assertEqual(filenames, [])
# #        self.assertRaises(MissingFromCacheError, lambda: smart_phrase_filenames(voice=voice, smart_phrase=my_txt, fail_quietly=False))
#         deliberately_cache_a_smart_phrase(voice, my_txt)
#         filenames = smart_phrase_filenames(voice=voice, smart_phrase=my_txt, fail_quietly=True)
#         second_attempt = smart_phrase_filenames(voice=voice, smart_phrase=my_txt, fail_quietly=True)
#         self.assertEqual(filenames, second_attempt)
#         self.assertEqual(["hello,_%s^_it's_12_midnight_and_time's_a-wasting^.mp3" % owner.lower(),
#                           "hello,_%s^_it's_12_midnight_and_time's_a-wasting^.ogg" % owner.lower()],
#                           list_files_in_dir(pathname_of_phrase_audio(voice)))
#         os.system('rm %s/{*,.*ogg,.*mp3}' % pathname_of_phrase_audio(voice))        
#         for phrase in ("Hello, %s." % owner, "It's", "12 midnight", "and time's a-wasting."):
#             deliberately_cache_a_smart_phrase(voice, phrase)
#         filenames = smart_phrase_filenames(voice=voice, smart_phrase=my_txt, fail_quietly=True)
#         second_attempt = smart_phrase_filenames(voice=voice, smart_phrase=my_txt, fail_quietly=True)
#         self.assertEqual(filenames, second_attempt)
#         self.assertEqual(filenames, ['sounds/cache/Laura/hello,_%s^.ogg' % owner.lower(), "sounds/cache/Laura/it's.ogg", 'sounds/cache/Laura/12_midnight.ogg', "sounds/cache/Laura/and_time's_a-wasting^.ogg"])
#         filenames = smart_phrase_filenames(voice=voice, smart_phrase=my_txt, fail_quietly=False)
#
#     def testSpecificMessageTen(self):
#         voice = 'Laura'
#         owner = OWNER_NAME
#         os.system('rm %s/{*,.*ogg,.*mp3}' % pathname_of_phrase_audio(voice))
# #        os.system('rmdir %s' % pathname_of_phrase_audio(voice))
#         message_template = """Groover! Hey %s, Frubby's ${shorttime}, chonker.""" % owner
#         my_txt = generate_detokenized_message(owner=owner, time_24h=12, time_minutes=1, message_template=message_template)
#         self.assertEqual(my_txt, "Groover! Hey %s, Frubby's 12:01 P.M., chonker." % owner)
#         filenames = smart_phrase_filenames(voice=voice, smart_phrase=my_txt, fail_quietly=True)
# #        self.assertEqual(filenames, [])
# #        self.assertRaises(MissingFromCacheError, lambda: smart_phrase_filenames(voice=voice, smart_phrase=my_txt, fail_quietly=False))
#         deliberately_cache_a_smart_phrase(voice, my_txt)
#         filenames = list_files_in_dir(pathname_of_phrase_audio(voice))
# #        self.assertEqual(filenames, ["groover&_hey_%s,_frubby's_12:01_p^m^,_chonker^.mp3" % owner.lower(), "groover&_hey_%s,_frubby's_12:01_p^m^,_chonker^.ogg" % owner.lower()])
#         # Now, let's cache some hours, minutes, etc. and see what a difference it make.
#         os.system('rm %s/{*,.*ogg,.*mp3}' % pathname_of_phrase_audio(voice))
#         for t in ["P.M.", "twelve?", "oh-one", "groover! Hey %s, Frubby's" % owner.lower(), "Chonker."]:
#             deliberately_cache_a_smart_phrase(voice, t)
#         shouldbe_basenames = [os.path.basename(r) for r in smart_phrase_filenames(voice, my_txt, fail_quietly=True)]
#         self.assertEqual(shouldbe_basenames, ["groover&_hey_%s,_frubby's.ogg" % owner.lower(), "twelve?.ogg", 'oh-one.ogg', 'p^m^.ogg', 'chonker^.ogg'])
#         isactually_basenames = [os.path.basename(r) for r in list_files_in_dir(pathname_of_phrase_audio(voice), '.ogg')]
#         shouldbe_basenames.sort()
#         isactually_basenames.sort()
#         self.assertEqual(shouldbe_basenames, isactually_basenames)
#
#     def testSpecificMessageEleven(self):
#         voice = 'Aria'
#         owner = OWNER_NAME
#         phrase1 = "Hey, %s! Check it." % owner
#         phrase2 = "Hey, %s! Check it," % owner
#         phrase3 = "Hey, %s! Check it" % owner
#         deliberately_cache_a_smart_phrase(voice, phrase1)
#         deliberately_cache_a_smart_phrase(voice, phrase2)
#         deliberately_cache_a_smart_phrase(voice, phrase3)
#         deliberately_cache_a_smart_phrase(voice, phrase1)
#         deliberately_cache_a_smart_phrase(voice, phrase2)
#         deliberately_cache_a_smart_phrase(voice, phrase3)


# class Test_this_one_thing(unittest.TestCase):
#
#     def test_list_phrases_to_handle(self):
#         list_phrases_to_handle("Hello, world. What is the plan here?")
    
    # def testSpecificMessageTwelve(self):
    #     voice = 'Aria'
    #     owner = OWNER_NAME
    #     self.assertRaises(ValueError, lambda: deliberately_cache_a_smart_phrase(voice, " Hey, %s! Check it." % (owner)))
    #     self.assertRaises(ValueError, lambda: deliberately_cache_a_smart_phrase(voice, "!Hey, %s! Check it." % (owner)))                          
    #     for c in "!?;',. ":
    #         self.assertRaises(ValueError, lambda: deliberately_cache_a_smart_phrase(voice, "%sHey, %s! Check it." % (c, owner)))

    
# class Test_lots_of_random_alarm_messages(unittest.TestCase):
#
#     def setUp(self):
#         pass
#
#     def tearDown(self):
#         pass
#
#     def testOneHundredTimesRandomMessages(self):
#         voice = 'Laura'
#         owner = OWNER_NAME
#         for _ in range(100):
#             for snoozed in (False, True):
#                 files_lst = get_list_of_files_for_speaking_a_random_alarm_message(owner=owner,
#                                                                                hour=random.randint(0,24),
#                                                                                minute=random.randint(0,60),
#                                                                                voice=voice,
#                                                                                snoozed=snoozed, fail_quietly=True)
#                 try:
#                     f2 = get_list_of_files_for_speaking_a_random_alarm_message(owner=owner,
#                                                                                hour=random.randint(0,24),
#                                                                                minute=random.randint(0,60),
#                                                                                voice=voice,
#                                                                                snoozed=snoozed, fail_quietly=False)
#                 except Exception as e:
#                     raise e
            
#     def testKnockKnockMessage(self):
#         voice = 'Laura'
#         owner = OWNER_NAME
#         os.system('rm %s/knock*knock*who*there*warrant*by*way*.*' % pathname_of_phrase_audio(voice))
#         basetemplate = "Knock, knock! Who's there? Get a warrant. Oh, and by the way, it's ${shorttime}" 
#         os.system('rm "%s"*.ogg' % pathname_of_phrase_audio(voice, basetemplate.split('$')[0]))
#         os.system('rm "%s"*.mp3' % pathname_of_phrase_audio(voice, basetemplate.split('$')[0]))
#         for punc in '?!.,:;':
#             message_template = basetemplate + punc
#             my_txt = generate_detokenized_message(owner=owner, time_24h=0, time_minutes=0, message_template=message_template)
#             deliberately_cache_a_smart_phrase(voice, my_txt)
#             filenames = smart_phrase_filenames(voice=voice, smart_phrase=my_txt, fail_quietly=True)
# #             self.assertEqual(filenames, [])
#             filenames = smart_phrase_filenames(voice=voice, smart_phrase=my_txt, fail_quietly=False)
#             _ = smart_phrase_audio(voice, my_txt, 'mp3')
#             _ = smart_phrase_audio(voice, my_txt, 'ogg')

# class Test_generate_detokenized_message(unittest.TestCase):
#
# cache_this_list_of_smart_phrases_for_voice(voice, hours_lst)
        
#
#         for phrase in ("o'clock", "A.M.", "P.M.", "twelve newn"):
#             deliberately_cache_a_smart_phrase(voice, phrase)
#
#         #         recognized_tokens = 
# # """${hello_owner} Current location of {owner}, bed. Appropriate location of {owner}, somewhere else. It is ${shorttime}. Do you know where your future is?""".replace('{owner}', OWNER_NAME),
# # def decoded_token(token:str, hello_owner:str, owner:str, shorttime:str, one_minute_ago:str, one_minute_later:str, morning_or_afternoon_or_evening:str) -> str:

        
# Force the caching of phrase 'y' as spoken by voice 'voice'



if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

