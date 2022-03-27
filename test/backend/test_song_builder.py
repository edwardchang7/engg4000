from telnetlib import SUPPRESS_LOCAL_ECHO
import unittest

# REMOVE THIS BEFORE MERGING INTO MASTER
# ===========================================================
# only uncomment this if you are not using pycharm
# import os, sys, inspect

# currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# parentdir = os.path.dirname(currentdir)
# parent2 = os.path.dirname(parentdir)
# sys.path.insert(0, parent2)
# END OF IMPORTS FOR NON-PYCHARM USERS (mostly just for Elliot)
# ===========================================================
# REMOVE THIS BEFORE MERGING INTO MASTER

# -- NOTE TO SELF: AFTER MERGING TONAL_PATTERNS IN HERE THEN UNCOMMENT THIS
# from src.backend.Collections.Tonal_Pattern import Tonal_Pattern
from src.backend import song_builder
from src.backend import scales

class TestSongBuilder(unittest.TestCase):

    def test_db_connection(self):
        database_name = "elliot"
        is_admin = False
        # makes a database connection
        database = song_builder._make_db_connection(database_name, is_admin)

        self.assertIsNotNone(database)

        return database


    def test_get_song_names_from_DB(self):
        results = song_builder._get_db_song_names()
        expected = ['The_Entertainer', 'Dancing_in_the_Moonlight', 'Symphony_No_5_in_C_MinorFirst_Movement_Ludwig_van_BeethovenAdp_from_arrangement_by_Ernst_Pauer_(1826-1905)', 'Symphony_No._5_in_C_MinorFirst_Movement_Ludwig_van_BeethovenAdp._from_arrangement_by_Ernst_Pauer_(1826-1905)', 'Sonate_No._14,_Moonlight1_st_Movement_Opus_27_No._2Ludwig_van_Beethoven_(1770–1827)', 'Mary_had_a_herd_of_Lambs', 'Waltz_in_A_Minor_Frederic_ChopinB_150', 'Sonate_No_14,_Moonlight1_st_Movement_Opus_27_No_2Ludwig_van_Beethoven_(1770–1827)', 'Take_Me_To_Church', 'Title', 'Closing_Time', "I_Can't_Help_Falling_in_Love", 'Canon_in_D', 'rhythmic_patterns']
    
        self.assertListEqual(results, expected)

        return results

    def test_get_random_pattern_style(self):
        pattern_style = [(4,4), (3,5), (5,3)]

        random_selected_pattern = song_builder._get_random_pattern_style()

        self.assertIn(random_selected_pattern, pattern_style)

        return random_selected_pattern

    def test_rhythmic_patterns(self):
        all_song_names = self.test_get_song_names_from_DB()
        pattern_lengths = self.test_get_random_pattern_style()

        pattern_length_1 = pattern_lengths[0]
        pattern_length_2 = pattern_lengths[1]

        first_song_name = all_song_names[0]

        random_selected_rhythmic_pattern_1 = song_builder._get_rhythmic_patterns(first_song_name, pattern_length_1)
        random_selected_rhythmic_pattern_2 = song_builder._get_rhythmic_patterns(first_song_name, pattern_length_2)

        pattern_1 = random_selected_rhythmic_pattern_1.pattern
        pattern_2 = random_selected_rhythmic_pattern_2.pattern

        self.assertEqual(pattern_length_1, len(pattern_1))
        self.assertEqual(pattern_length_2, len(pattern_2))

        combined_length = len(pattern_1) + len(pattern_2)

        self.assertEqual(combined_length, 8)

        return pattern_1, pattern_2

    def test_build_rhythmic_pattern(self):
        key = ""
        pattern_1, pattern_2 = song_builder.build_rhythmic_pattern(key)

        self.assertIsNotNone(pattern_1)
        self.assertIsNotNone(pattern_2)

        pattern_1_length = len(pattern_1.pattern)
        pattern_2_length = len(pattern_2.pattern)

        combined_length = pattern_1_length + pattern_2_length

        self.assertEqual(combined_length, 8)

    # NOTE TO SELF: UNCOMMENT THIS AFTER MERGING TONAL_PATTERNS IN THIS BRANCH
    # def test_convert_tonal_patterns(self):
    #     pattern =[['h'], ['-h'], ['w'], ['-w'], ['m3'], ['-m3'], ['M3'], ['-M3'], ['P5'], ['-P5'], ['o'], ['-o'], ['0']]
    #     num_notes  = 14
    #     priority = 0

    #     answer = ["C#", "C", "D", "C", "D#", "C", "E", "C", "G", "C", "c", "C", "C"]

    #     tonal_pattern_obj = Tonal_Pattern(pattern, num_notes, priority)

    #     results = song_builder.convert_tonal_pattern('C', tonal_pattern_obj)

    #     self.assertIsNotNone(tonal_pattern_obj)
    #     self.assertEqual(results, answer)

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
        start_note = 'C'
        end_note = 'C'
        beat_length = 5

        scale = self.test_get_random_scale_type()
        generated_bridged_pattern = song_builder.bridge_pattern(key, start_note, end_note, beat_length)

        self.assertIsNotNone(scale)
        self.assertIsNotNone(generated_bridged_pattern)
        self.assertEqual(len(generated_bridged_pattern), beat_length)

# DEBUG
# REMOVE THIS BEFORE MERGING INTO MASTER
# THIS IS JUST TO RUN ALL THE TEST WITHIN THIS FILE ONLY
if __name__ == '__main__':
    unittest.main()