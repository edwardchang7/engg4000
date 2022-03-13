'''
A class to hold a rhythmic pattern
'''

import ast

class Rhythmic_Pattern:

    def __init__(self, pattern, frequency, is_v1):
        self.pattern = ast.literal_eval(pattern)
        self.frequency = frequency
        self.length = len(self.pattern)
        self.beats = _get_beats_length(pattern)
        self.is_v1 = is_v1

    '''
    toString method
    '''
    def __str__(self):
        return (f"Pattern: {self.pattern} \nFrequency: {self.frequency} \nLength: {self.length} \nBeats: {self.beats}\nIs V1: {self.is_v1}\n")
        

def _get_beats_length(pattern):
    length = 0
    to_count = True

    # counts t he length of each bar within the combined pattern
    for char in pattern:
        if char == '(':
            to_count = False

        if char.isdigit() and to_count:
            length += 1

        elif char.isdigit() and not to_count:
            to_count = True


    return length


