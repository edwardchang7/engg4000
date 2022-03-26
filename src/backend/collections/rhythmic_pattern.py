import ast


class RhythmicPattern:
    def __init__(self, pattern, frequency, is_v1):
        # Converts a string in the format of a list to an actual list object
        self.pattern = pattern
        self.frequency = frequency

        if type(self.pattern) is list:
            self.length = len(self.pattern)
            self.beats = _get_beats_length(str(pattern))
        else:
            self.pattern = len(ast.literal_eval(self.pattern))
            self.beats = _get_beats_length(pattern)

        self.is_v1 = is_v1

    def __str__(self):
        return f"Pattern: {self.pattern} \nFrequency: {self.frequency} \nLength: {self.length} \nBeats: {self.beats}\nIs V1: {self.is_v1}\n"


def _get_beats_length(pattern):
    length = 0
    to_count = True

    # counts the length of each bar within the combined pattern
    for char in pattern:
        if char == '(':
            to_count = False

        # if its a digit, then check if to_count is true (to_count will be false if its a rest's beat)
        if char.isdigit() and to_count:
            length += 1

        elif char.isdigit() and not to_count:
            to_count = True

    return length
