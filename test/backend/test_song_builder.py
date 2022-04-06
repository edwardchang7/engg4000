from turtle import up
import unittest

# ===========================================================
# only uncomment this if you are not using pycharm
import os
import sys
import inspect
from backend.music_tools import whole_step
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parent2 = os.path.dirname(parentdir)
sys.path.insert(0, parent2)
# ===========================================================
# REMOVE THIS BEFORE MERGING INTO MASTER
from src.backend.collections.tonal_pattern import TonalPattern
from src.backend.collections.rhythmic_pattern import RhythmicPattern
from src.backend.collections.note_pattern import NotePattern
from src.backend import scales, song_builder

class Test_Song_Builder(unittest.TestCase):

    def test_db_connection(self):
        database_name = "elliot"
        is_admin = False
        # makes a database connection
        database = song_builder._make_db_connection(database_name, is_admin)

        self.assertIsNotNone(database)

        return database

    def test_get_song_names_from_DB(self):
        results = song_builder._get_db_song_names(False)
        expected = ['The_Entertainer', 'Dancing_in_the_Moonlight', 'Symphony_No._5_in_C_MinorFirst_Movement_Ludwig_van_BeethovenAdp._from_arrangement_by_Ernst_Pauer_(1826-1905)', 'Sonate_No._14,_Moonlight1_st_Movement_Opus_27_No._2Ludwig_van_Beethoven_(1770–1827)', 'Mary_had_a_herd_of_Lambs', 'Waltz_in_A_Minor_Frederic_ChopinB_150', 'Take_Me_To_Church', 'Title', 'Closing_Time', "I_Can't_Help_Falling_in_Love", 'Canon_in_D', 'rhythmic_patterns']

        self.assertListEqual(results, expected)

        return results

    def test_get_random_pattern_style(self):
        pattern_style = [(4, 4), (3, 5), (5, 3)]

        random_selected_pattern = song_builder._get_random_pattern_style()

        self.assertIn(random_selected_pattern, pattern_style)

        return random_selected_pattern

    def test_rhythmic_patterns(self):
        all_song_names = self.test_get_song_names_from_DB()
        pattern_lengths = self.test_get_random_pattern_style()

        pattern_length_1 = pattern_lengths[0]
        pattern_length_2 = pattern_lengths[1]

        first_song_name = all_song_names[0]

        random_selected_rhythmic_pattern_1 = song_builder._get_rhythmic_pattern(
            first_song_name, pattern_length_1)
        random_selected_rhythmic_pattern_2 = song_builder._get_rhythmic_pattern(
            first_song_name, pattern_length_2)

        pattern_1 = random_selected_rhythmic_pattern_1.pattern
        pattern_2 = random_selected_rhythmic_pattern_2.pattern

        self.assertEqual(pattern_length_1, len(pattern_1))
        self.assertEqual(pattern_length_2, len(pattern_2))

        combined_length = len(pattern_1) + len(pattern_2)

        self.assertEqual(combined_length, 8)

        return pattern_1, pattern_2

    def test_build_rhythmic_pattern(self):
        length_to_check = 8
        key = ""
        rhythmic_pattern_obj = song_builder.build_rhythmic_pattern(key)

        self.assertIsNotNone(rhythmic_pattern_obj)

        pattern_length = len(rhythmic_pattern_obj.pattern)

        self.assertEqual(pattern_length, length_to_check)

        return rhythmic_pattern_obj

    def test_convert_tonal_patterns(self):
        pattern = [['h'], ['-h'], ['w'], ['-w'], ['m3'], ['-m3'],
                   ['M3'], ['-M3'], ['P5'], ['-P5'], ['o'], ['-o'], ['0']]
        num_notes = 14
        priority = 0

        answer = ["C", "C#", "C", "D", "C", "D#", "C",
                  "E", "C", "G", "C", "c", "C", "C"]

        tonal_pattern_obj = TonalPattern(pattern, num_notes, priority)

        results = song_builder.convert_tonal_pattern('C', tonal_pattern_obj)

        self.assertIsNotNone(tonal_pattern_obj)
        self.assertEqual(results, answer)

        return results

    def test_get_random_scale_type(self):
        key = 'CM'
        root = key[0]

        generated_scale = song_builder._get_random_scale_type(key, True)

        major_scale = scales.get_scale(root, 'M')

        self.assertIsNotNone(generated_scale)
        self.assertListEqual(generated_scale, major_scale)

        return generated_scale

    def test_get_window(self):
        key = 'CM'
        note = 'E'
        actual_window = ['D', 'C', 'F', 'G']

        scale = scales.get_scale(key[0], 'M')
        generated_window = song_builder._get_window(note, scale)

        self.assertIsNotNone(generated_window)
        self.assertListEqual(generated_window, actual_window)

        return generated_window

    def test_bridge_pattern(self):
        key = 'CM'
        tonal_pattern_1 = self.test_convert_tonal_patterns()
        tonal_pattern_2 = self.test_convert_tonal_patterns()
        beat_length = 3
        generated_length = len(tonal_pattern_1) + beat_length

        generated_bridged_pattern = song_builder.bridge_pattern(key, tonal_pattern_1, tonal_pattern_2, beat_length)

        self.assertIsNotNone(generated_bridged_pattern)
        self.assertEqual(len(generated_bridged_pattern), generated_length)

        return generated_bridged_pattern

    def test_build_verse(self):
        rhythmic_pattern_obj  = self.test_build_rhythmic_pattern()
        key = "CM"
        verse = song_builder.build_verse(key, rhythmic_pattern_obj)
        self.assertIsNotNone(verse)

    def test_modulate_verse(self):
        note1 = NotePattern("C", 1)
        note2 = NotePattern("E", 1)
        note3 = NotePattern("G", 1)


        note_list = []
        note_list.append(note1)
        note_list.append(note2)
        note_list.append(note3)

        interval = "w"
        key = "CM"
        up_frequency = True

        modulated = song_builder.modulate_verse(note_list, interval, up_frequency, key)
        
        self.assertEqual(modulated[0].note, "D")
        self.assertEqual(modulated[1].note, "F#")
        self.assertEqual(modulated[2].note, "A")

    def test_modulate_real_verse(self):
        rhythmic_pattern_obj  = self.test_build_rhythmic_pattern()
        key = "CM"
        verse = song_builder.build_verse(key, rhythmic_pattern_obj)

        interval = "w"
        key = "CM"
        up_frequency = True

        modulated = song_builder.modulate_verse(verse, interval, up_frequency, key)
        
        self.assertIsNotNone(modulated)
        check = whole_step(song_builder._strip_note_modifiers(verse[0].note), up_frequency)
        self.assertEqual(song_builder._strip_note_modifiers(modulated[0].note), check)
        check = whole_step(song_builder._strip_note_modifiers(verse[1].note), up_frequency)
        self.assertEqual(song_builder._strip_note_modifiers(modulated[1].note), check)

    def test_random_cadence(self):
        note1 = NotePattern("C", 1)
        note2 = NotePattern("E", 1)
        note3 = NotePattern("G", 1)

        key = "CM"

        note_list = []
        note_list.append(note1)
        note_list.append(note2)
        note_list.append(note3)

        bridge = song_builder.add_random_cadence(note_list, key)

        self.assertIsNotNone(bridge)
        self.assertEqual(len(bridge), len(note_list))
        self.assertEqual(bridge[0].length, note_list[0].length)

    def test_random_cadence_real_verse(self):
        rhythmic_pattern_obj  = self.test_build_rhythmic_pattern()
        key = "CM"
        verse = song_builder.build_verse(key, rhythmic_pattern_obj)

        bridge = song_builder.add_random_cadence(verse, key)

        self.assertIsNotNone(bridge)
        self.assertEqual(len(verse), len(bridge))
        self.assertEqual(verse[0].length, bridge[0].length)

    def test_build_bridge(self):
        rhythmic_pattern_obj  = self.test_build_rhythmic_pattern()
        key = "CM"
        verse = song_builder.build_verse(key, rhythmic_pattern_obj)

        bridge = song_builder.build_song_bridge(verse, key)

        self.assertIsNotNone(bridge)
        self.assertEqual(len(bridge), len(verse))


# DEBUG
# REMOVE THIS BEFORE MERGING INTO MASTER
# THIS IS JUST TO RUN ALL THE TEST WITHIN THIS FILE ONLY
if __name__ == '__main__':
    unittest.main()
