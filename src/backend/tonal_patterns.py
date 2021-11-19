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
    pattern = ['w', 'w']

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


    total = 0
    pattern_index = 0

    # -------- DEBUG --------- 
    # TO BE DELETED BEFORE MERGING WITH MASTER
    print(prev_notes)

    for i in range(1, len(prev_notes)):
        # checks for half notes upwards and downwards
        if pattern[pattern_index] == "h" and is_half_step(prev_notes[i-1], prev_notes[i], True):
            pattern_index += 1
        elif pattern[pattern_index] == "-h" and is_half_step(prev_notes[i-1], prev_notes[i], False):
            pattern_index += 1
        elif pattern[pattern_index] == "w" and is_whole_step(prev_notes[i-1], prev_notes[i], True):
            pattern_index += 1
        elif pattern[pattern_index] == "-w" and is_whole_step(prev_notes[i-1], prev_notes[i], False):
            pattern_index += 1

        else:
            # if the pattern is broken, reset the counter for the pattern
            pattern_index = 0
            # Since the pattern is broken, check if it is the start of the given pattern
            # only reduce i by 1 if its not at the start so that it checks if its the start of the pattern
            if i > 1:
                i -= 1

        # finished parsing through the pattern
        if pattern_index == len(pattern):
            # reset the counter and increase the total count of the pattern found by 1
            pattern_index = 0
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
    # This exception list is for examples like if you do a whole step for A# it returns c' rather than C
    # This ensures that it stays at c' rather than 'c
    exceptions = ["'", ","]

    if len(note) >= 2 and note[1] not in exceptions:
        to_return = note[1] + note[0]

        # Append any remaining modifiers at the end
        # EX: if you input "#A," it will return A#, <-- The "," is kept in place
        # EX: if you do "c'" it will return "c'" <-- no changes are to be made if its valid
        # EX: if you do "c" it will return c <-- no changes are to be made if its valid
        for i in range (2, len(note)):
            to_return += note[i]

        return to_return
        
    return note
