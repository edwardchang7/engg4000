from src.backend.music_tools import *
from src.backend.scales import *
import itertools

def analyze_patterns(key = 'GM', input_string = "E'/ | G A/ (B3/4 c/4) ^B/", pattern=None):

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
                    prev_notes.append(prev_chars)

                prev_chars = ""

            if is_flat is True: #if it is a flat, set it to the sharp equivalent
                char = whole_step(char, False)
                is_flat = False

            prev_chars += char

    prev_notes.append(prev_chars)


    total = 0
    pattern_index = 0

    # -------- DEBUG --------- 
    # TO BE DELETED BEFORE MERGING WITH MASTER
    # -------- DEBUG --------- 
    print(prev_notes)


    for i in range(1, len(prev_notes)):
        # checks for half notes upwards and downwards
        if is_pattern_match(pattern[pattern_index], prev_notes[i-1], prev_notes[i]):
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

    return total
