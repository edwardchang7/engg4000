import unittest

from src.backend.abc_tools import get_header, is_polyphonic, get_music, get_voicings

mono_test_composition_path = "test/backend/test_composition/Monophonic_Cant_help_falling_in_love__Elvis_Presley.abc"
poly_test_composition_path = "test/backend/test_composition/Cant_help_falling_in_love__Elvis_Presley.abc"
test_music_string = """V:1
 z"^pizz." Ad fdA | z Ac ecA | z FA dAF | fdA afd |:"_arco" D6 | A6 |$ D6- | D3 z EF | G6 | F6 | %10
 E6- | E4 z A, | B,6 |$ C6 | D6 | E2 F2 G2 | F6 | E6 | D6- | D4 z2 :|$ C2 F- FAc | B6 | C2 F- FAc | %23
 B6 | C2 F- FAc | B6 | A2 A- A3- |$ A2 F- FAF | G6 | A6 || d6 | a6 | d6- | d3 z ef |$ g6 | f6 | %36
 e6- | e4 z A | B6 | c6 | d6 |$ e2 f2 g2 | f6 | e6 | d6- | d4 z A | B6 | c6 |$ d4 z2 | e2 f2 g2 | %50
"^rit."[Q:3/8=55] f6[Q:3/8=50] |[Q:3/8=45] e6 |[Q:3/8=40] d6- | d6[Q:3/8=30] |] %54"""


class TestTools(unittest.TestCase):
    def test_get_header(self):
        self.assertTrue(get_header(poly_test_composition_path, "T") == "I Can't Help Falling in Love")
        self.assertTrue(get_header(poly_test_composition_path, "C") == "Elvis")
        self.assertTrue(get_header(poly_test_composition_path, "Z") == "arr. Cathy Donnelly")
        self.assertTrue(get_header(poly_test_composition_path, "L") == "1/8")
        self.assertTrue(get_header(poly_test_composition_path, "M") == "6/8")
        self.assertTrue(get_header(poly_test_composition_path, "K") == "D")
        self.assertTrue(get_header(poly_test_composition_path, "V") == ['1 treble nm="Violin" snm="Vln."',
                                                                        '2 bass nm="Violoncello" snm="Vc."', '1', '2'])

    def test_is_polyphonic(self):
        self.assertTrue(is_polyphonic(poly_test_composition_path))
        self.assertFalse(is_polyphonic(mono_test_composition_path))

    def test_get_music(self):
        self.assertTrue(get_music(mono_test_composition_path) == test_music_string)

    def test_get_voicings(self):
        poly_voicings = [
            '\n z"^pizz." Ad fdA | z Ac ecA | z FA dAF | fdA afd |:"_arco" D6 | A6 |$ D6- | D3 z EF | G6 | F6 | %10\n '
            'E6- | E4 z A, | B,6 |$ C6 | D6 | E2 F2 G2 | F6 | E6 | D6- | D4 z2 :|$ C2 F- FAc | B6 | C2 F- FAc | %23\n '
            'B6 | C2 F- FAc | B6 | A2 A- A3- |$ A2 F- FAF | G6 | A6 || d6 | a6 | d6- | d3 z ef |$ g6 | f6 | %36\n e6- '
            '| e4 z A | B6 | c6 | d6 |$ e2 f2 g2 | f6 | e6 | d6- | d4 z A | B6 | c6 |$ d4 z2 | e2 f2 g2 | '
            '%50\n"^rit."[Q:3/8=55] f6[Q:3/8=50] |[Q:3/8=45] e6 |[Q:3/8=40] d6- | d6[Q:3/8=30] |] %54\n',
            '\n"^pizz." D,,3 F, z F, | A,,3 F, z F, | D,,3 F, z F, | A,,3 A,,B,,C, |: D,,D,F, A,F,D, | %5\n F,,C,F, '
            'A,F,C, |$ B,,D,F, B,F,D, | A,,D,F, A,F,D, | G,,B,,D, G,D,B,, | D,,D,F, DF,D, | %10\n A,,C,E, A,E,C, | A,'
            ',C,E, A,E,A,, | G,,B,,D, G,D,B,, |$ A,,C,E, G,E,C, | B,,D,F, B,F,D, | %15\n E,,G,,B,, E,B,,G,, | A,,D,F, '
            'A,F,D, | A,,C,E, A,E,C, | D,F,A, DA,D, | FDA, AFD :|$ %20\n"^arco" F,,3 F,3 | C,3 C,,=F,,^G,, | F,,3 F,'
            '3 | C,3 C,,=F,,^G,, | F,,3 F,3 | C,3 C,=F,^G, | %26\n ^F,3 ^F,,3 |$ B,,3 B,,^D,F, | E,3- E,C,B,, | A,,'
            '3 A,3 ||"^pizz." D,,D,F, A,F,D, | F,,C,F, A,F,C, | %32\n B,,D,F, B,F,D, | A,,D,F, A,F,D, |$ G,,B,,D, G,'
            'D,B,, | D,,A,,F, DF,D, | A,,C,E, A,E,C, | %37\n A,,C,E, A,E,A,, | G,,B,,D, G,D,B,, | A,,C,E, G,E,C, | B,'
            ',D,F, B,F,D, |$ E,,G,,B,, E,B,,G,, | %42\n A,,D,F, A,F,D, | A,,C,E, A,E,C, | D,F,A, DA,F, | FA,F, A,F,D, '
            '| G,,D,G, B,G,D, | A,,E,G, CG,E, |$ %48\n B,,F,B, DB,F, | E,G,B, EB,G, | A,,D,F, A,F,D, | A,,C,E, A,E,C, '
            '| D,,A,,D, A,F,D, | DA,F, FA,A |] %54\n']
        self.assertTrue(get_voicings(poly_test_composition_path) == poly_voicings)
