import unittest

from src.backend.circle_of_fifths import CircleOfFifths


class TestCircleOfFifths(unittest.TestCase):
    def test_get_scale_with_major_note(self):
        cof = CircleOfFifths()

        expected_result = ['D', 'A', 'E', 'B', '_G', '_D', '_A', '_E', '_B', 'F', 'C', 'G']
        actual_result = cof.get_cof('D')

        self.assertEqual(actual_result, expected_result)

    def test_get_scale_with_alternative_major_note(self):
        cof = CircleOfFifths()

        expected_result = ['^F', '^C', '_A', '_E', '_B', 'F', 'C', 'G', 'D', 'A', 'E', '_C']
        actual_result = cof.get_cof('^F')

        self.assertEqual(actual_result, expected_result)

    def test_get_scale_with_minor_note(self):
        cof = CircleOfFifths()

        expected_result = ['b', '^f', '^c', '^g', '^d', '_b', 'f', 'c', 'g', 'd', 'a', 'e']
        actual_result = cof.get_cof('b')

        self.assertEqual(actual_result, expected_result)

    def test_get_scale_with_alternative_minor_note(self):
        cof = CircleOfFifths()

        expected_result = ['_e', '^a', 'f', 'c', 'g', 'd', 'a', 'e', 'b', '^f', '^c', '_a']
        actual_result = cof.get_cof('_e')

        self.assertEqual(actual_result, expected_result)

    def test_get_scale_with_non_existent_note(self):
        cof = CircleOfFifths()

        expected_result = []
        actual_result = cof.get_cof('T')

        self.assertEqual(actual_result, expected_result)

    def test_get_num_flats_with_major_notes(self):
        cof = CircleOfFifths()
        major_notes = cof.major_notes
        expected_num_flats = [3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 3]

        for i in range(len(major_notes)):
            self.assertEqual(cof.get_num_of_flats_between_two_notes(major_notes[i]), expected_num_flats[i])

    def test_get_num_flats_with_alternative_major_notes(self):
        cof = CircleOfFifths()
        alternative_major_notes = cof.alternative_major_notes
        expected_num_flats = [3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 3]

        for i in range(len(alternative_major_notes)):
            self.assertEqual(cof.get_num_of_flats_between_two_notes(alternative_major_notes[i]), expected_num_flats[i])

    def test_get_num_flats_with_minor_notes(self):
        cof = CircleOfFifths()
        minor_notes = cof.minor_notes
        expected_num_flats = [3, 3, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3]

        for i in range(len(minor_notes)):
            self.assertEqual(cof.get_num_of_flats_between_two_notes(minor_notes[i]), expected_num_flats[i])

    def test_get_num_flats_with_alternative_minor_notes(self):
        cof = CircleOfFifths()
        alternative_minor_notes = cof.alternative_minor_notes
        expected_num_flats = [3, 3, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3]

        for i in range(len(alternative_minor_notes)):
            self.assertEqual(cof.get_num_of_flats_between_two_notes(alternative_minor_notes[i]), expected_num_flats[i])

    def test_get_num_sharps_with_major_notes(self):
        cof = CircleOfFifths()
        major_notes = cof.major_notes
        expected_num_sharps = [3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 3]

        for i in range(len(major_notes)):
            self.assertEqual(cof.get_num_of_sharps_between_two_notes(major_notes[i]), expected_num_sharps[i])

    def test_get_num_sharps_with_alternative_major_notes(self):
        cof = CircleOfFifths()
        alternative_major_notes = cof.alternative_major_notes
        expected_num_sharps = [3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 3]

        for i in range(len(alternative_major_notes)):
            self.assertEqual(cof.get_num_of_sharps_between_two_notes(alternative_major_notes[i]), expected_num_sharps[i])

    def test_get_num_sharps_with_minor_notes(self):
        cof = CircleOfFifths()
        minor_notes = cof.minor_notes
        expected_num_sharps = [3, 3, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3]

        for i in range(len(minor_notes)):
            self.assertEqual(cof.get_num_of_sharps_between_two_notes(minor_notes[i]), expected_num_sharps[i])

    def test_get_num_sharps_with_alternative_minor_notes(self):
        cof = CircleOfFifths()
        alternative_minor_notes = cof.alternative_minor_notes
        expected_num_sharps = [3, 3, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3]

        for i in range(len(alternative_minor_notes)):
            self.assertEqual(cof.get_num_of_sharps_between_two_notes(alternative_minor_notes[i]), expected_num_sharps[i])
