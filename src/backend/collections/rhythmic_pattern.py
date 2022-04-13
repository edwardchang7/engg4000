import ast


class RhythmicPattern:

    def __init__(self, pattern, frequency, is_v1:bool):
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

    def __str__(self) -> str:
        '''
        toString function
        '''
        return f"Pattern: {self.pattern} \nFrequency: {self.frequency} \nLength: {self.length} \nBeats: {self.beats}\nIs V1: {self.is_v1}\n"


def _get_length_in_beats(pattern:str) -> int:
    '''
    counts the number of beats within the bar (chords counted as 1 all together, beam notes are couted sepeareatly)

    Parameters:
        pattern: the rhythmic pattern to count the beats

    Returns:
        the number of beats within this rhythmic pattern
    '''
    length = 0

    pattern_list = ast.literal_eval(pattern)

    end = False

    for beats in pattern_list:
        # get the count of every beat if its its not within a bracket 
        length += sum(len(beat) for beat in beats if "[" not in beats and "(" not in beats)

        # if there is a chord, count the number of chords that exist
        if any("[" in b for b in beats):
            for b in beats:

                length += b.count("[")
                
                if b == "[":
                    end = False

                elif b == "]":
                    end = True

                if end and b.isdigit():
                    length += 1
    return length

