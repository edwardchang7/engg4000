import unittest

from src.backend.circle_of_fifths import CircleOfFifths


class TestCircleOfFifths(unittest.TestCase):
    cof = CircleOfFifths()

    def test_get_scale_with_major_note(self):
        expected_result = ['D', 'A', 'E', 'B', '_G', '_D', '_A', '_E', '_B', 'F', 'C', 'G']
        actual_result = self.cof.get_cof('D')

        self.assertEqual(actual_result, expected_result)

    def test_get_scale_with_alternative_major_note(self):
        expected_result = ['^F', '^C', '_A', '_E', '_B', 'F', 'C', 'G', 'D', 'A', 'E', '_C']
        actual_result = self.cof.get_cof('^F')

        self.assertEqual(actual_result, expected_result)

    def test_get_scale_with_minor_note(self):
        expected_result = ['b', '^f', '^c', '^g', '^d', '_b', 'f', 'c', 'g', 'd', 'a', 'e']
        actual_result = self.cof.get_cof('b')

        self.assertEqual(actual_result, expected_result)

    def test_get_scale_with_alternative_minor_note(self):
        expected_result = ['_e', '^a', 'f', 'c', 'g', 'd', 'a', 'e', 'b', '^f', '^c', '_a']
        actual_result = self.cof.get_cof('_e')

        self.assertEqual(actual_result, expected_result)

    def test_get_scale_with_non_existent_note(self):
        expected_result = []
        actual_result = self.cof.get_cof('T')

        self.assertEqual(actual_result, expected_result)

    def test_get_num_flats_with_major_notes(self):
        major_notes = self.cof.major_notes
        expected_num_flats = [3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 3]

        for i in range(len(major_notes)):
            self.assertEqual(self.cof.get_num_of_flats_between_two_notes(major_notes[i]), expected_num_flats[i])

    def test_get_num_flats_with_alternative_major_notes(self):
        alternative_major_notes = self.cof.alternative_major_notes
        expected_num_flats = [3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 3]

        for i in range(len(alternative_major_notes)):
            self.assertEqual(
                self.cof.get_num_of_flats_between_two_notes(alternative_major_notes[i]),
                expected_num_flats[i]
            )

    def test_get_num_flats_with_minor_notes(self):
        minor_notes = self.cof.minor_notes
        expected_num_flats = [3, 3, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3]

        for i in range(len(minor_notes)):
            self.assertEqual(self.cof.get_num_of_flats_between_two_notes(minor_notes[i]), expected_num_flats[i])

    def test_get_num_flats_with_alternative_minor_notes(self):
        alternative_minor_notes = self.cof.alternative_minor_notes
        expected_num_flats = [3, 3, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3]

        for i in range(len(alternative_minor_notes)):
            self.assertEqual(
                self.cof.get_num_of_flats_between_two_notes(alternative_minor_notes[i]),
                expected_num_flats[i]
            )

    def test_get_num_sharps_with_major_notes(self):
        major_notes = self.cof.major_notes
        expected_num_sharps = [3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 3]

        for i in range(len(major_notes)):
            self.assertEqual(self.cof.get_num_of_sharps_between_two_notes(major_notes[i]), expected_num_sharps[i])

    def test_get_num_sharps_with_alternative_major_notes(self):
        alternative_major_notes = self.cof.alternative_major_notes
        expected_num_sharps = [3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 3]

        for i in range(len(alternative_major_notes)):
            self.assertEqual(
                self.cof.get_num_of_sharps_between_two_notes(alternative_major_notes[i]),
                expected_num_sharps[i]
            )

    def test_get_num_sharps_with_minor_notes(self):
        minor_notes = self.cof.minor_notes
        expected_num_sharps = [3, 3, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3]

        for i in range(len(minor_notes)):
            self.assertEqual(self.cof.get_num_of_sharps_between_two_notes(minor_notes[i]), expected_num_sharps[i])

    def test_get_num_sharps_with_alternative_minor_notes(self):
        alternative_minor_notes = self.cof.alternative_minor_notes
        expected_num_sharps = [3, 3, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3]

        for i in range(len(alternative_minor_notes)):
            self.assertEqual(
                self.cof.get_num_of_sharps_between_two_notes(alternative_minor_notes[i]),
                expected_num_sharps[i]
            )

    def test_get_perfect_cadence_with_major_key(self):
        expected_perfect_cadence = ('G', 'C')
        actual_perfect_cadence = self.cof.get_perfect_cadence('C')
        self.assertEqual(expected_perfect_cadence, actual_perfect_cadence)

        expected_perfect_cadence = ('_G', 'B')
        actual_perfect_cadence = self.cof.get_perfect_cadence('B')
        self.assertEqual(expected_perfect_cadence, actual_perfect_cadence)

        expected_perfect_cadence = ('C', 'F')
        actual_perfect_cadence = self.cof.get_perfect_cadence('F')
        self.assertEqual(expected_perfect_cadence, actual_perfect_cadence)

    def test_get_perfect_cadence_with_minor_key(self):
        expected_perfect_cadence = ('e', 'a')
        actual_perfect_cadence = self.cof.get_perfect_cadence('a')
        self.assertEqual(expected_perfect_cadence, actual_perfect_cadence)

        expected_perfect_cadence = ('^d', '^g')
        actual_perfect_cadence = self.cof.get_perfect_cadence('^g')
        self.assertEqual(expected_perfect_cadence, actual_perfect_cadence)

        expected_perfect_cadence = ('a', 'd')
        actual_perfect_cadence = self.cof.get_perfect_cadence('d')
        self.assertEqual(expected_perfect_cadence, actual_perfect_cadence)

    def test_get_num_of_sharps_in_each_major_note(self):
        expected_result = 0
        actual_result = self.cof.get_num_of_sharps_in_note('C')
        self.assertEqual(expected_result, actual_result)

        expected_result = 1
        actual_result = self.cof.get_num_of_sharps_in_note('G')
        self.assertEqual(expected_result, actual_result)

        expected_result = 2
        actual_result = self.cof.get_num_of_sharps_in_note('D')
        self.assertEqual(expected_result, actual_result)

        expected_result = 3
        actual_result = self.cof.get_num_of_sharps_in_note('A')
        self.assertEqual(expected_result, actual_result)

        expected_result = 4
        actual_result = self.cof.get_num_of_sharps_in_note('E')
        self.assertEqual(expected_result, actual_result)

        expected_result = 5
        actual_result = self.cof.get_num_of_sharps_in_note('B')
        self.assertEqual(expected_result, actual_result)

        expected_result = 6
        actual_result = self.cof.get_num_of_sharps_in_note('_G')
        self.assertEqual(expected_result, actual_result)

        expected_result = 7
        actual_result = self.cof.get_num_of_sharps_in_note('_D')
        self.assertEqual(expected_result, actual_result)

        expected_result = 0
        actual_result = self.cof.get_num_of_sharps_in_note('_A')
        self.assertEqual(expected_result, actual_result)

        expected_result = 0
        actual_result = self.cof.get_num_of_sharps_in_note('_E')
        self.assertEqual(expected_result, actual_result)

        expected_result = 0
        actual_result = self.cof.get_num_of_sharps_in_note('_B')
        self.assertEqual(expected_result, actual_result)

        expected_result = 0
        actual_result = self.cof.get_num_of_sharps_in_note('F')
        self.assertEqual(expected_result, actual_result)

    def test_get_num_of_sharps_in_each_minor_note(self):
        expected_result = 0
        actual_result = self.cof.get_num_of_sharps_in_note('a')
        self.assertEqual(expected_result, actual_result)

        expected_result = 1
        actual_result = self.cof.get_num_of_sharps_in_note('e')
        self.assertEqual(expected_result, actual_result)

        expected_result = 2
        actual_result = self.cof.get_num_of_sharps_in_note('b')
        self.assertEqual(expected_result, actual_result)

        expected_result = 3
        actual_result = self.cof.get_num_of_sharps_in_note('^f')
        self.assertEqual(expected_result, actual_result)

        expected_result = 4
        actual_result = self.cof.get_num_of_sharps_in_note('^c')
        self.assertEqual(expected_result, actual_result)

        expected_result = 5
        actual_result = self.cof.get_num_of_sharps_in_note('^g')
        self.assertEqual(expected_result, actual_result)

        expected_result = 6
        actual_result = self.cof.get_num_of_sharps_in_note('^d')
        self.assertEqual(expected_result, actual_result)

        expected_result = 7
        actual_result = self.cof.get_num_of_sharps_in_note('_b')
        self.assertEqual(expected_result, actual_result)

        expected_result = 0
        actual_result = self.cof.get_num_of_sharps_in_note('f')
        self.assertEqual(expected_result, actual_result)

        expected_result = 0
        actual_result = self.cof.get_num_of_sharps_in_note('c')
        self.assertEqual(expected_result, actual_result)

        expected_result = 0
        actual_result = self.cof.get_num_of_sharps_in_note('g')
        self.assertEqual(expected_result, actual_result)

        expected_result = 0
        actual_result = self.cof.get_num_of_sharps_in_note('d')
        self.assertEqual(expected_result, actual_result)

    def test_get_num_of_flats_in_each_major_note(self):
        expected_result = 0
        actual_result = self.cof.get_num_of_flats_in_note('C')
        self.assertEqual(expected_result, actual_result)

        expected_result = 0
        actual_result = self.cof.get_num_of_flats_in_note('G')
        self.assertEqual(expected_result, actual_result)

        expected_result = 0
        actual_result = self.cof.get_num_of_flats_in_note('D')
        self.assertEqual(expected_result, actual_result)

        expected_result = 0
        actual_result = self.cof.get_num_of_flats_in_note('A')
        self.assertEqual(expected_result, actual_result)

        expected_result = 0
        actual_result = self.cof.get_num_of_flats_in_note('E')
        self.assertEqual(expected_result, actual_result)

        expected_result = 7
        actual_result = self.cof.get_num_of_flats_in_note('B')
        self.assertEqual(expected_result, actual_result)

        expected_result = 6
        actual_result = self.cof.get_num_of_flats_in_note('_G')
        self.assertEqual(expected_result, actual_result)

        expected_result = 5
        actual_result = self.cof.get_num_of_flats_in_note('_D')
        self.assertEqual(expected_result, actual_result)

        expected_result = 4
        actual_result = self.cof.get_num_of_flats_in_note('_A')
        self.assertEqual(expected_result, actual_result)

        expected_result = 3
        actual_result = self.cof.get_num_of_flats_in_note('_E')
        self.assertEqual(expected_result, actual_result)

        expected_result = 2
        actual_result = self.cof.get_num_of_flats_in_note('_B')
        self.assertEqual(expected_result, actual_result)

        expected_result = 1
        actual_result = self.cof.get_num_of_flats_in_note('F')
        self.assertEqual(expected_result, actual_result)

    def test_get_num_of_flats_in_each_minor_note(self):
        expected_result = 0
        actual_result = self.cof.get_num_of_flats_in_note('a')
        self.assertEqual(expected_result, actual_result)

        expected_result = 0
        actual_result = self.cof.get_num_of_flats_in_note('e')
        self.assertEqual(expected_result, actual_result)

        expected_result = 0
        actual_result = self.cof.get_num_of_flats_in_note('b')
        self.assertEqual(expected_result, actual_result)

        expected_result = 0
        actual_result = self.cof.get_num_of_flats_in_note('^f')
        self.assertEqual(expected_result, actual_result)

        expected_result = 0
        actual_result = self.cof.get_num_of_flats_in_note('^c')
        self.assertEqual(expected_result, actual_result)

        expected_result = 7
        actual_result = self.cof.get_num_of_flats_in_note('^g')
        self.assertEqual(expected_result, actual_result)

        expected_result = 6
        actual_result = self.cof.get_num_of_flats_in_note('^d')
        self.assertEqual(expected_result, actual_result)

        expected_result = 5
        actual_result = self.cof.get_num_of_flats_in_note('_b')
        self.assertEqual(expected_result, actual_result)

        expected_result = 4
        actual_result = self.cof.get_num_of_flats_in_note('f')
        self.assertEqual(expected_result, actual_result)

        expected_result = 3
        actual_result = self.cof.get_num_of_flats_in_note('c')
        self.assertEqual(expected_result, actual_result)

        expected_result = 2
        actual_result = self.cof.get_num_of_flats_in_note('g')
        self.assertEqual(expected_result, actual_result)

        expected_result = 1
        actual_result = self.cof.get_num_of_flats_in_note('d')
        self.assertEqual(expected_result, actual_result)
