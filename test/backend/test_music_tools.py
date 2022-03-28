import unittest
from src.backend.music_tools import whole_step, half_step, M3, m3, P5, change_octave, pad_octave_notation, \
    check_interval


class TextMusicTools(unittest.TestCase):

    def test_halfStep_increasingFreq_one(self):
        self.assertEqual(half_step("A", True), "A#")

    def test_halfStep_increasingFreq_two(self):
        self.assertEqual(half_step("B", True), "c")

    def test_halfStep_increasingFreq_three(self):
        self.assertEqual(half_step("D#,", True), "E,")

    def test_halfStep_decreasingFreq_one(self):
        self.assertEqual(half_step("c'", False), "b")

    def test_halfStep_decreasingFreq_two(self):
        self.assertEqual(half_step("A", False), "G#")

    def test_halfStep_decreasingFreq_three(self):
        self.assertEqual(half_step("F,", False), "E,")

    def test_wholeStep_increasingFreq_one(self):
        self.assertEqual(whole_step("E", True), "F#")

    def test_wholeStep_increasingFreq_two(self):
        self.assertEqual(whole_step("B", True), "c#")

    def test_wholeStep_increasingFreq_three(self):
        self.assertEqual(whole_step("D,", True), "E,")

    def test_wholeStep_decreasingFreq_one(self):
        self.assertEqual(whole_step("c'", False), "a#")

    def test_wholeStep_decreasingFreq_two(self):
        self.assertEqual(whole_step("B", False), "A")

    def test_wholeStep_decreasingFreq_three(self):
        self.assertEqual(whole_step("F#,", False), "E,")

    def test_M3_increasingFreq_one(self):
        self.assertEqual(M3("C", True), "E")

    def test_M3_increasingFreq_two(self):
        self.assertEqual(M3("A#", True), "d")

    def test_M3_increasingFreq_three(self):
        self.assertEqual(M3("b'", True), "d#''")

    def test_M3_decreasingFreq_one(self):
        self.assertEqual(M3("c'", False), "g#")

    def test_M3_decreasingFreq_two(self):
        self.assertEqual(M3("E", False), "C")

    def test_M3_decreasingFreq_three(self):
        self.assertEqual(M3("F#,", False), "D,")

    def test_m3_increasingFreq_one(self):
        self.assertEqual(m3("E", True), "G")

    def test_m3_increasingFreq_two(self):
        self.assertEqual(m3("c'", True), "d#'")

    def test_m3_increasingFreq_three(self):
        self.assertEqual(m3("F,", True), "G#,")

    def test_m3_decreasingFreq_one(self):
        self.assertEqual(m3("C,", False), "A,,")

    def test_m3_decreasingFreq_two(self):
        self.assertEqual(m3("d''", False), "b'")

    def test_m3_decreasingFreq_three(self):
        self.assertEqual(m3("E", False), "C#")

    def test_P5_increasingFreq_one(self):
        self.assertEqual(P5("C", True), "G")

    def test_P5_increasingFreq_two(self):
        self.assertEqual(P5("F#", True), "c#")

    def test_P5_increasingFreq_three(self):
        self.assertEqual(P5("A,", True), "E")

    def test_P5_decreasingFreq_one(self):
        self.assertEqual(P5("A#,", False), "D#,")

    def test_P5_decreasingFreq_two(self):
        self.assertEqual(P5("D", False), "G,")

    def test_P5_decreasingFreq_three(self):
        self.assertEqual(P5("e'", False), "e")

    def test_changeOctave_increasingFreq_one(self):
        self.assertEqual(change_octave("C", True), "c")

    def test_changeOctave_increasingFreq_two(self):
        self.assertEqual(change_octave("g#'", True), "g#''")

    def test_changeOctave_increasingFreq_three(self):
        self.assertEqual(change_octave("A,", True), "A")

    def test_changeOctave_decreasingFreq_one(self):
        self.assertEqual(change_octave("A#,", False), "A#,,")

    def test_changeOctave_decreasingFreq_two(self):
        self.assertEqual(change_octave("D", False), "D,")

    def test_changeOctave_decreasingFreq_three(self):
        self.assertEqual(change_octave("e'", False), "a")

    def test_pad_octave_notation_octave0(self):
        self.assertEqual(pad_octave_notation(0, "A"), "A")

    def test_pad_octave_notation_octave1(self):
        self.assertEqual(pad_octave_notation(1, "A"), "a")

    def test_pad_octave_notation_octaveN1(self):
        self.assertEqual(pad_octave_notation(-1, "A"), "A,")

    def test_pad_octave_notation_octave2(self):
        self.assertEqual(pad_octave_notation(2, "A"), "a'")

    def test_pad_octave_notation_octaveN2(self):
        self.assertEqual(pad_octave_notation(-2, "A"), "A,,")

    def test_check_interval_0(self):
        self.assertEqual(
            check_interval({"note": "D", "degree": "0", "octave": 0}, {"note": "D", "degree": "0", "octave": 0}), ["0"])

    def test_check_interval_0(self):
        self.assertEqual(
            check_interval({"note": "D", "degree": "0", "octave": 0}, {"note": "D", "degree": "0", "octave": 0}), ["0"])

    def test_check_interval_0(self):
        self.assertEqual(
            check_interval({"note": "D", "degree": "0", "octave": 0}, {"note": "D", "degree": "0", "octave": 0}), ["0"])

    def test_check_interval_0(self):
        self.assertEqual(
            check_interval({"note": "D", "degree": "0", "octave": 0}, {"note": "D", "degree": "0", "octave": 0}), ["0"])

    def test_check_interval_0(self):
        self.assertEqual(
            check_interval({"note": "D", "degree": "0", "octave": 0}, {"note": "D", "degree": "0", "octave": 0}), ["0"])