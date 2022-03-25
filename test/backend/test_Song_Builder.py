import os
import sys
import unittest

from src.backend.cluster import Cluster
from src.backend.Song_Builder import SongBuilder


class TestSongBuilder(unittest.TestCase):

    def test_db_connection(self):
        database_name = "elliot"
        is_admin = False

        database = SongBuilder._make_db_connection(database_name, is_admin)

        self.assertIsNotNone(database)

        return database


    def test_get_song_names_from_DB(self):
        results = SongBuilder._get_db_song_names()
        expected = ['The_Entertainer', 'Dancing_in_the_Moonlight', 'Symphony_No_5_in_C_MinorFirst_Movement_Ludwig_van_BeethovenAdp_from_arrangement_by_Ernst_Pauer_(1826-1905)', 'Symphony_No._5_in_C_MinorFirst_Movement_Ludwig_van_BeethovenAdp._from_arrangement_by_Ernst_Pauer_(1826-1905)', 'Sonate_No._14,_Moonlight1_st_Movement_Opus_27_No._2Ludwig_van_Beethoven_(1770–1827)', 'Mary_had_a_herd_of_Lambs', 'Waltz_in_A_Minor_Frederic_ChopinB_150', 'Sonate_No_14,_Moonlight1_st_Movement_Opus_27_No_2Ludwig_van_Beethoven_(1770–1827)', 'Take_Me_To_Church', 'Title', 'Closing_Time', "I_Can't_Help_Falling_in_Love", 'Canon_in_D', 'rhythmic_patterns']

        self.assertEqual(results, expected)

        return results

    def test_get_random_pattern_style(self):
        pattern_style = [(4,4), (3,5), (5,3)]

        random_selected_pattern = SongBuilder._get_random_pattern_style()

        self.assertIn(random_selected_pattern, pattern_style)

        return random_selected_pattern

    def test_rhythmic_patterns(self):
        all_song_names = self.test_get_song_names_from_DB()
        pattern_lengths = self.test_get_random_pattern_style()

        pattern_length_1 = pattern_lengths[0]
        pattern_length_2 = pattern_lengths[1]

        first_song_name = all_song_names[0]

        random_selected_rhythmic_pattern_1 = SongBuilder._get_rhythmic_patterns(first_song_name, pattern_length_1)
        random_selected_rhythmic_pattern_2 = SongBuilder._get_rhythmic_patterns(first_song_name, pattern_length_2)

        pattern_1 = random_selected_rhythmic_pattern_1.pattern
        pattern_2 = random_selected_rhythmic_pattern_2.pattern

        self.assertEquals(pattern_length_1, len(pattern_1))
        self.assertEquals(pattern_length_2, len(pattern_2))

        combined_length = len(pattern_1) + len(pattern_2)

        self.assertEquals(combined_length, 8)

        return pattern_1, pattern_2

    def test_build_rhythmic_pattern(self):
        key = ""
        pattern_1, pattern_2 = SongBuilder.build_rhythmic_pattern(key)

        self.assertIsNotNone(pattern_1)
        self.assertIsNotNone(pattern_2)

        pattern_1_length = len(pattern_1.pattern)
        pattern_2_length = len(pattern_2.pattern)

        combined_length = pattern_1_length + pattern_2_length

        self.assertEquals(combined_length, 8)



if __name__ == '__main__':
    unittest.main()