import ast


class Rhythmic_Pattern:
    def __init__(self, pattern, frequency, is_v1):
        # Converts a string in the format of a list to an actual list object
        self.pattern = pattern
        self.frequency = frequency

        if type(self.pattern) is list:
            self.length = len(self.pattern)
            self.beats = _get_length_in_beats(str(pattern))
        else:
            self.pattern = ast.literal_eval(pattern)
            self.length = len(self.pattern)
            self.beats = _get_length_in_beats(pattern)

        self.is_v1 = is_v1

    def __str__(self):
        return f"Pattern: {self.pattern} \nFrequency: {self.frequency} \nLength: {self.length} \nBeats: {self.beats}\nIs V1: {self.is_v1}\n"


def _get_length_in_beats(pattern):
    length = 0
    to_count = True
    is_chord = False
    last_char = ''

    # counts the length of each bar within the combined pattern
    for char in pattern:
        if char == '(':
            to_count = False

        if char == "'":
            last_char = char

        if last_char == "'" and char == '[':
            is_chord = True
            length += 1

        if last_char == "'" and char == ']':
            is_chord = False
            last_char = ""

        # if its a digit, then check if to_count is true (to_count will be false if its a rest's beat)
        if char.isdigit() and to_count and not is_chord:
            length += 1

        elif char.isdigit() and not to_count:
            to_count = True

    return length


