from src.backend.music_tools import *
from src.backend.scales import *
import itertools

def analyze_patterns(key = 'GM', input_string = "E'/ | G A/ (B3/4 c/4) B/"):

    # list of symbols to keep track of
    exceptions = ["'", ",", "_", "^", "|"]

    analyze_str = ""
    flag = True

    for char in input_string:
        if char == '"': #removes any strings within ""
            flag = not flag
        
        if flag:
            if char.isalpha() or char in exceptions: #removes rythmyic related things
                analyze_str += char

    #hardcoded for now to test pattern freq
    pattern = ['h', '-h']

    print(frequency_of_pattern(analyze_str, key, pattern))

def frequency_of_pattern(analyze_str,key, pattern):

    prev_chars = ""
    prev_notes = []
    total = 0
    is_flat = False

    for char in analyze_str:
        if char == "'" or char == ",":
            prev_chars += char
        elif char != "|" and char != " ":
            if prev_chars[:1] == "^":
                prev_chars = "#"
            elif prev_chars[:1] == "_": #fix to work with flats
                prev_chars = "#"
                is_flat = True
            else:
                if prev_chars != "":
                    prev_notes.append(flip(prev_chars))

                prev_chars = ""

            if is_flat is True: #if it is a flat, set it to the sharp equivalent
                char = whole_step(char, False)
                is_flat = False

            prev_chars += char

    prev_notes.append(flip(prev_chars))

# prev_notes = ["A", "#A", "A"]
# pattern = [h, hh]

    total = 0

    print(prev_notes)

    for i in range (1, len(prev_notes)): #inclusive start, exclusive end
        if is_half_step(prev_notes[i], prev_notes[i-1]):
            total += 1

    


    # if len(prev_notes) == len(pattern) + 1:
    #     i = 0
    #     up = True
    #     test_note = ""
    #     for note in prev_notes:
    #         if test_note != "":
    #             if test_note != note:
    #                 break
    #         if i < len(pattern):
    #             if pattern[i][0] == '-':
    #                 up = False
    #                 pattern[i] = 'h'

    #             if pattern[i][0] == 'h':
    #                 test_note = half_step(note, up)
                
    #         if test_note == "A#":
    #             test_note = "#A"

    #         i += 1

    #     if i == len(prev_notes):
    #         total += 1

    #     prev_chars = ""
    #     prev_notes = []

    return total


def flip(note):
    '''
    A function to 'fix' the notation. If the note given is '#A', it will return 'A#'

    Param:
        the note to flip
    '''
    if len(note) == 2:
        return note[1] + note[0]
    return note