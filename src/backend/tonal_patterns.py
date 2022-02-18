from src.backend.music_tools import whole_step, check_interval
from src.backend.scales import get_scale
import itertools

# Falling in love with you test pattern~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
test_pattern = "D6 | A6 |$ D6- | D3 z EF | G6 | F6 | %10 E6- | E4 z A, | B,6 |$ C6 | D6 | E2 F2 G2 | F6 | E6 | D6- | D4 z2 :|$ C2 F- FAc |"
test_key = "D"
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Function to remove all rhythmic and tonal related symbols from pattern leaving just the note names
def format_pattern(key:str, input_string:str, pattern):

    # symbols that we want to keep in the pattern
    exceptions = ["'", ",", "_", "^", "|"]

    formatted_pattern = ""
    is_note = True

    # removes any strings within ""
    for char in input_string:
        if char == '"':
            is_note = not is_note

        if is_note:
            # removes rhythmic related things
            if char.isalpha() or char in exceptions:
                formatted_pattern += char

    # hardcoded for now to test pattern freq
    return formatted_pattern


# Function to ???
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

            #if it is a flat, set it to the sharp equivalent
            if is_flat is True:
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



# Function to translate from input string to list of patterns (pattern = dictionary of relevant info about note)
def config_input_string(key:str, input_str:str):
    # 1. get the notes in the key
    notes_in_key=get_scale("D","M")

    # Do some note formatting
    #TODO consider the key signature here and how it will affect removing/adding flats and sharps
    # -->for now just removing sharps
    notes_in_key=[note.replace("#","") for note in notes_in_key]
    notes_in_key=[note.upper() for note in notes_in_key]

    #preset flags
    higher = False
    lower = False
    octave = -99
    temp_note = ""

    # 2. (note_index + 1) =  their tonal value
    # 3. Transpose all the notes in the extracted pattern
    # 4. Octave referenced to middle C (0 relates to original Scale's octave)
    tonal_val_dict_list=[]
    for note in input_str:
        if higher:
            if note=="'":
                octave += 1
            else:
                tonal_val_dict_list.append(
                    {"note": temp_note, "degree": str(notes_in_key.index(temp_note.upper()) + 1), "octave": octave})
                higher = False
        elif lower:
            if note==",":
                octave -= 1
            else:
                tonal_val_dict_list.append(
                    {"note": temp_note, "degree": str(notes_in_key.index(temp_note) + 1), "octave": octave})
                lower = False
        if note.isalpha():
            if note == "z":
                tonal_val_dict_list.append({"note": "z", "degree": "0", "octave": "na"})
            else:
                if note.islower():
                    higher = True
                    octave = 1
                    temp_note = note
                else:
                    lower = True
                    octave = 0
                    temp_note = note
        elif note == "|":
            tonal_val_dict_list.append({"note": "|", "degree": "-1", "octave": "na"})
    for item in tonal_val_dict_list:
        print(item)
    tonic_to_tonic_filter(key, tonal_val_dict_list)

#Function which extracts a tonic-tonic pattern in the given list of notes
#Currently reset to look at a pattern of a certain length of bars (or find one close to there)
def tonic_to_tonic_filter(key:str, tonal_val_list:list):
    #1. Set range to analyze
    bars = 16

    pattern = []
    start_note = {}
    end_note = {}
    for note in tonal_val_list:
        if bars < 1:
            #check pattern
            print(pattern)
            break
        elif note["degree"] == -1:
            bars -= 1
        else:
            try:
                if start_note["degree"] != 0 and note["degree"] != 0:
                    end_note = note
                    # check_interval in music_tools (seemed like a better spot for that type of function)
                    pattern.append(check_interval(key, start_note, end_note))
                    start_note = end_note
            except KeyError:
                start_note = note
            except:
                print("Unknown Error")

# TESTING STUFF~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("FORMATTED PATTERN:")
print(format_pattern(test_key, test_pattern, pattern=None))

config_input_string(test_key, test_pattern)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~









