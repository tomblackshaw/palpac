# -*- coding: utf-8 -*-
'''
Created on May 20, 2024

@author: Tom Blackshaw
'''
import random
import unittest

from my.stringutils import generate_random_string, MAX_RANDGENSTR_LEN, convert_24h_and_mins_to_shorttime, find_trigger_phrase_in_sentence,\
    generate_triggerphrase_permutations, trim_away_the_trigger_and_locate_the_command_if_there_is_one, scan_sentence_for_any_one_of_these_trigger_phrases


G_triggers = ['doc', 'Dad', 'there', 'that', 'tad', 'thad', 'than', 'Dan', 'either doc', 'either Dad', 'either there', 'either that', 'either tad', 'either thad', 'either than', 'either Dan', 'hate doc', 'hate Dad', 'hate there', 'hate that', 'hate tad', 'hate thad', 'hate than', 'hate Dan', 'hey doc', 'hey Dad', 'hey there', 'hey that', 'hey tad', 'hey thad', 'hey than', 'hey Dan', 'hay doc', 'hay Dad', 'hay there', 'hay that', 'hay tad', 'hay thad', 'hay than', 'hay Dan', 'they doc', 'they Dad', 'they there', 'they that', 'they tad', 'they thad', 'they than', 'they Dan', 'a doc', 'a Dad', 'a there', 'a that', 'a tad', 'a thad', 'a than', 'a Dan', 'heh doc', 'heh Dad', 'heh there', 'heh that', 'heh tad', 'heh thad', 'heh than', 'heh Dan', 'eight doc', 'eight Dad', 'eight there', 'eight that', 'eight tad', 'eight thad', 'eight than', 'eight Dan', 'i doc', 'i Dad', 'i there', 'i that', 'i tad', 'i thad', 'i than', 'i Dan', 'Freya doc', 'Freya Dad', 'Freya there', 'Freya that', 'Freya tad', 'Freya thad', 'Freya than', 'Freya Dan', 'up doc', 'up Dad', 'up there', 'up that', 'up tad', 'up thad', 'up than', 'up Dan', 'great doc', 'great Dad', 'great there', 'great that', 'great tad', 'great thad', 'great than', 'great Dan', 'the doc', 'the Dad', 'the there', 'the that', 'the tad', 'the thad', 'the than', 'the Dan']

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


class TestFindTriggerWordInSentence(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testGoofy(self):
        self.assertRaises(TypeError, find_trigger_phrase_in_sentence, None, None)
        self.assertRaises(TypeError, find_trigger_phrase_in_sentence, None, 1)
        self.assertRaises(TypeError, find_trigger_phrase_in_sentence, 1.2, None)
        self.assertRaises(ValueError, find_trigger_phrase_in_sentence, " stuff with space either side", 'trigger')
        self.assertRaises(ValueError, find_trigger_phrase_in_sentence, "stuff with space either side ", 'trigger')
        self.assertRaises(ValueError, find_trigger_phrase_in_sentence, "stuff with space either side", ' trigger')
        self.assertRaises(ValueError, find_trigger_phrase_in_sentence, "stuff with space either side", 'trigger ')
        self.assertEqual(find_trigger_phrase_in_sentence('Small', 'Bigger'), -1)
        self.assertEqual(find_trigger_phrase_in_sentence('', 'Small'), -1)
        self.assertRaises(ValueError, find_trigger_phrase_in_sentence, "Sentence", "")

    # def testFirstNWords(self):
    #     self.assertEqual(find_trigger_phrase_in_sentence('Regular Sentence is here', 'is', 2), -1)
    #     self.assertEqual(find_trigger_phrase_in_sentence('Regular Sentence is here', 'is'), -1)
    #     self.assertEqual(find_trigger_phrase_in_sentence('Regular Sentence is here', 'sentence'), 8)
    #     self.assertEqual(find_trigger_phrase_in_sentence('Regular SENTENCE is here', 'sEnTence'), 8)
    #     self.assertEqual(find_trigger_phrase_in_sentence('Regular Sentence is here', 'sEnTence'), 8)
    #     self.assertEqual(find_trigger_phrase_in_sentence('Regular Sentence is here', 'egu'), -1)
    #     self.assertEqual(find_trigger_phrase_in_sentence('Regular Sentence is here', 'ent'), -1)
    #     self.assertEqual(find_trigger_phrase_in_sentence('Sentence is here', 'sentence'), 0)
    #     self.assertEqual(find_trigger_phrase_in_sentence('SENTENCE is here', 'sEnTence'), 0)
    #     self.assertEqual(find_trigger_phrase_in_sentence('Sentence is here', 'ent'), -1)
    #     self.assertEqual(find_trigger_phrase_in_sentence('Sinner is here', 'is'), 7)
    #     self.assertEqual(find_trigger_phrase_in_sentence('Sinner is here', 'here'), -1)
    #     self.assertEqual(find_trigger_phrase_in_sentence('Sinner is here', 'here', 3), -1)
    #     self.assertEqual(find_trigger_phrase_in_sentence('Sinner is here', 'here', 2), -1)
    #     self.assertEqual(find_trigger_phrase_in_sentence('Sinner is here', 'here', 1), -1)
    #     self.assertEqual(find_trigger_phrase_in_sentence('Sinner is', 'here'), -1)
    #     self.assertEqual(find_trigger_phrase_in_sentence('Sinner is', 'sinner'), 0)
    #     self.assertEqual(find_trigger_phrase_in_sentence('Sinner is', 'is'), 7)

    def testPhrases(self):
#         self.assertEqual(find_trigger_phrase_in_sentence('Regular Sentence is here', 'is here', 2), -1)
        self.assertEqual(find_trigger_phrase_in_sentence('Regular Sentence is here', 'is here'), 17)
        self.assertEqual(find_trigger_phrase_in_sentence('Regular Sentence is here', 'sentence is'), 8)
        self.assertEqual(find_trigger_phrase_in_sentence('Regular SENTENCE is here', 'sEnTence iS'), 8)
        self.assertEqual(find_trigger_phrase_in_sentence('Regular Sentence is here', 'sEnTence Is'), 8)
        self.assertEqual(find_trigger_phrase_in_sentence('Regular Sentence is here', 'egu'), -1)
        self.assertEqual(find_trigger_phrase_in_sentence('Regular Sentence is here', 'ent'), -1)
        self.assertEqual(find_trigger_phrase_in_sentence('Sentence is here', 'sentence is'), 0)
        self.assertEqual(find_trigger_phrase_in_sentence('SENTENCE is here', 'sEnTence Is'), 0)
        self.assertEqual(find_trigger_phrase_in_sentence('Sentence is here', 'ent'), -1)
        self.assertEqual(find_trigger_phrase_in_sentence('Sinner is here', 'is here'), 7)
        self.assertEqual(find_trigger_phrase_in_sentence('Sinner is here', 'here'), 10)
        self.assertEqual(find_trigger_phrase_in_sentence('Sinner is', 'here'), -1)
        self.assertEqual(find_trigger_phrase_in_sentence('Sinner is', 'sinner is'), 0)
        self.assertEqual(find_trigger_phrase_in_sentence('Sinner is', 'is'), 7)


class TestGenerateTriggerphrasePermutations(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testGoofy(self):
        self.assertRaises(TypeError, generate_triggerphrase_permutations, None, None)
        self.assertRaises(TypeError, generate_triggerphrase_permutations, None, None, None)
        self.assertRaises(TypeError, generate_triggerphrase_permutations, [1, 2, 3], None)
        self.assertRaises(TypeError, generate_triggerphrase_permutations, None, [1, 2, 3])
        self.assertRaises(TypeError, generate_triggerphrase_permutations, 'hi', None)
        self.assertRaises(TypeError, generate_triggerphrase_permutations, None, 'there')
        self.assertRaises(TypeError, generate_triggerphrase_permutations, None, ('bA', 'bB'))
        self.assertRaises(TypeError, generate_triggerphrase_permutations, None, ['bA', 'bB'])
        self.assertRaises(TypeError, generate_triggerphrase_permutations, ('aA', 'aB'), None)
        self.assertRaises(TypeError, generate_triggerphrase_permutations, ['aA', 'aB'], None)
        self.assertRaises(TypeError, generate_triggerphrase_permutations, ['aA', 'aB'], [1, 2, 3])
        self.assertRaises(TypeError, generate_triggerphrase_permutations, ([1, 2, 3], ['bA', 'bB']))
        self.assertRaises(ValueError, generate_triggerphrase_permutations, [], [])
        self.assertRaises(ValueError, generate_triggerphrase_permutations, (), [])
        self.assertRaises(ValueError, generate_triggerphrase_permutations, [], ())
        self.assertRaises(ValueError, generate_triggerphrase_permutations, (), ())
        self.assertRaises(ValueError, generate_triggerphrase_permutations, (), ['hi', 'there'])
        self.assertRaises(ValueError, generate_triggerphrase_permutations, (), ('hi', 'there'))
        self.assertRaises(ValueError, generate_triggerphrase_permutations, ['hi', 'there'], ())
        self.assertRaises(ValueError, generate_triggerphrase_permutations, ('hi', 'there'), ())
        self.assertRaises(TypeError, generate_triggerphrase_permutations, ('hi', 'there'), (''))  # second param is a string, not a tuple, because of missing comman.
        self.assertRaises(ValueError, generate_triggerphrase_permutations, ('hi', 'there'), ('',))
        self.assertRaises(TypeError, generate_triggerphrase_permutations, [1, 'hi', 'there'], ('hi', 'there'))
        self.assertRaises(TypeError, generate_triggerphrase_permutations, [1, 'hi', 'there'], ('hi', 'there'))
        self.assertRaises(TypeError, generate_triggerphrase_permutations, ('hi', 'there'), [1, 'hi', 'there'])
        self.assertRaises(TypeError, generate_triggerphrase_permutations, ('hi', 'there'), [1, 'hi', 'there'])

    def testSane(self):
        self.assertEqual(generate_triggerphrase_permutations(('aA', 'aB'), ('bA', 'bB')), ['aA bA', 'aA bB', 'aB bA', 'aB bB'])
        self.assertEqual(generate_triggerphrase_permutations(['aA', 'aB'], ('bA', 'bB')), ['aA bA', 'aA bB', 'aB bA', 'aB bB'])
        self.assertEqual(generate_triggerphrase_permutations(['aA', 'aB'], ('bA', 'bB')), ['aA bA', 'aA bB', 'aB bA', 'aB bB'])
        self.assertEqual(generate_triggerphrase_permutations(['aA', 'aB'], ['bA', 'bB']), ['aA bA', 'aA bB', 'aB bA', 'aB bB'])
        self.assertEqual(generate_triggerphrase_permutations(['aaa'], ['bbb']), ['aaa bbb'])
        self.assertEqual(generate_triggerphrase_permutations(('aaa',), ('bbb',)), ['aaa bbb'])
        self.assertEqual(generate_triggerphrase_permutations(('aaa', 'aab', 'aac'), ('dd', 'ee')), ['aaa dd', 'aaa ee', 'aab dd', 'aab ee', 'aac dd', 'aac ee'])


class TestScanSentenceForAnyOneOfTheseTriggerPhrases(unittest.TestCase):


    def setUp(self):
        self.triggerphrases = G_triggers

    def tearDown(self):
        pass

    def testGoofy(self):
        self.assertRaises(TypeError, scan_sentence_for_any_one_of_these_trigger_phrases)
        self.assertRaises(TypeError, scan_sentence_for_any_one_of_these_trigger_phrases, None)
        self.assertRaises(TypeError, scan_sentence_for_any_one_of_these_trigger_phrases, None, None)
        self.assertRaises(TypeError, scan_sentence_for_any_one_of_these_trigger_phrases, None, None, None)
        self.assertRaises(TypeError, scan_sentence_for_any_one_of_these_trigger_phrases, None, 1)
        self.assertRaises(TypeError, scan_sentence_for_any_one_of_these_trigger_phrases, 1.2, None)
        self.assertEqual(scan_sentence_for_any_one_of_these_trigger_phrases('hi dad how are you', self.triggerphrases), 7)
        self.assertEqual(scan_sentence_for_any_one_of_these_trigger_phrases('well hi dad how are you', self.triggerphrases), 12)
        self.assertEqual(scan_sentence_for_any_one_of_these_trigger_phrases('giggity hi tad how are you', self.triggerphrases), 15)
        self.assertEqual(scan_sentence_for_any_one_of_these_trigger_phrases('giggity hi doc how are you', self.triggerphrases), 15)
        self.assertEqual(scan_sentence_for_any_one_of_these_trigger_phrases('giggity hey doc how are you', self.triggerphrases), 16)


class TestTrimAwayTheTriggerAndLocateTheCommandIfThereIsOne(unittest.TestCase):

    def setUp(self):
        self.triggerphrases = G_triggers

    def tearDown(self):
        pass

    def testGoofy(self):
        self.assertRaises(TypeError, trim_away_the_trigger_and_locate_the_command_if_there_is_one)
        self.assertRaises(TypeError, trim_away_the_trigger_and_locate_the_command_if_there_is_one, None)
        self.assertRaises(TypeError, trim_away_the_trigger_and_locate_the_command_if_there_is_one, None, None)
        self.assertRaises(TypeError, trim_away_the_trigger_and_locate_the_command_if_there_is_one, None, None, None)
#        self.assertRaises(TypeError, trim_away_the_trigger_and_locate_the_command_if_there_is_one, '', ['hi',2,'there'])

    def testMiscEdgeCases(self):
        phrases = self.triggerphrases
        original_sentence = 'hey dad that hey dad a dead'
        s1 = original_sentence[scan_sentence_for_any_one_of_these_trigger_phrases(original_sentence, phrases):]
        s2 = s1[scan_sentence_for_any_one_of_these_trigger_phrases(s1, phrases):]
        self.assertEqual(s2, "a dead")
        self.assertEqual(original_sentence[trim_away_the_trigger_and_locate_the_command_if_there_is_one(original_sentence, phrases):], "a dead")

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

