import ast
from itertools import accumulate, chain, count


class RhythmicPattern:
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

    '''
    toString function
    '''
    def __str__(self):
        return f"Pattern: {self.pattern} \nFrequency: {self.frequency} \nLength: {self.length} \nBeats: {self.beats}\nIs V1: {self.is_v1}\n"


def _get_length_in_beats(pattern):
    length = 0

    x = ast.literal_eval(pattern)

    for y in x:
        length += sum(len(z) for z in y if "[" not in z and "(" not in z)

        # if there is a chord, count the number of chords that exist
        if any("[" in b for b in y):
            for b in y:
                length += b.count("[")    
        

    return length


