import unittest
from src.backend.chords import gen_chord


class TestChords(unittest.TestCase):

    def test_major7Chord_one(self):
        self.assertEqual(gen_chord('C', 'M7', []), ['C', 'E', 'G', 'B'])

    def test_major7Chord_two(self):
        self.assertEqual(gen_chord("a'", 'M7', []), ["a'", "c#''", "e''", "g#''"])

    def test_major7Chord_three(self):
        self.assertEqual(gen_chord('D#,,', 'M7', []), ['D#,,', 'G,,', 'A#,,', 'D,'])

    def test_majorminor7Chord_one(self):
        self.assertEqual(gen_chord('C', 'Mm7', []), ['C', 'D#', 'G', 'B'])

    def test_majorminor7Chord_two(self):
        self.assertEqual(gen_chord("a'", 'Mm7', []), ["a'", "c''", "e''", "g#''"])

    def test_majorminor7Chord_three(self):
        self.assertEqual(gen_chord('D#,,', 'Mm7', []), ['D#,,', 'F#,,', 'A#,,', 'D,'])

    def test_minor7Chord_one(self):
        self.assertEqual(gen_chord('C', 'm7', []), ['C', 'D#', 'G', 'A#'])

    def test_minor7Chord_two(self):
        self.assertEqual(gen_chord("a'", 'm7', []), ["a'", "c''", "e''", "g''"])

    def test_minor7Chord_three(self):
        self.assertEqual(gen_chord('D#,,', 'm7', []), ['D#,,', 'F#,,', 'A#,,', 'C#,'])

    def test_halfDiminishedChord_one(self):
        self.assertEqual(gen_chord('C', 'HD', []), ['C', 'D#', 'F#', 'A#'])

    def test_halfDiminishedChord_two(self):
        self.assertEqual(gen_chord("a'", 'HD', []), ["a'", "c''", "d#''", "g''"])

    def test_halfDiminishedChord_three(self):
        self.assertEqual(gen_chord('D#,,', 'HD', []), ['D#,,', 'F#,,', 'A,,', 'C#,'])

    def test_fullDiminishedChord_one(self):
        self.assertEqual(gen_chord('C', 'FD', []), ['C', 'D#', 'F#', 'A'])

    def test_fullDiminishedChord_two(self):
        self.assertEqual(gen_chord("a'", 'FD', []), ["a'", "c''", "d#''", "f#''"])

    def test_fullDiminishedChord_three(self):
        self.assertEqual(gen_chord('D#,,', 'FD', []), ['D#,,', 'F#,,', 'A,,', 'C,'])

    def test_major7_extraNotes(self):
        self.assertEqual(gen_chord('C', 'M7', ["0'", "2,,"]), ['C', 'E', 'G', 'B', "c'", 'G,,'])

    def test_sus2_extraNotes(self):
        self.assertEqual(gen_chord('F#', 'sus2', ["0,", "1''"]), ['F#', 'G#', "c#'", 'F#,', "g#''"])

    def test_halfDiminished_extraNotes(self):
        self.assertEqual(gen_chord('E', 'HD', ["0'", "2,,", "1''", "3,"]),
                         ['E', 'G', 'A#', "d'", "e'", 'A#,,', "g''", 'D'])


