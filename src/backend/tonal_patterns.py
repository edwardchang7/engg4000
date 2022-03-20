from src.backend.music_tools import whole_step, check_interval, half_step
from src.backend.scales import get_scale
#from src.backend.cluster import Cluster
from src.backend.models.tonal_pattern_model import TonalPatternModel
from src.backend.abc_tools import (get_header, get_melodic_and_rythmic, get_music,
                       get_voicings, is_polyphonic)
import itertools

# CONSTANTS_____________________________________________
# values are in bars
min_pattern_length=3
max_pattern_length=16
# ______________________________________________________


# TEST PATTERN__________________________________________
test_pattern = "D6 | A6 |$ D6- | D3 z EF | G6 | F6 | %10 E6- | E4 z A,, | B,6 |$ C6 | D6 | E2 F2 G2 | F6 | E6 | D6- | D4 z2 :|$ C2 F- FAc |"
test_key = "D"
# ______________________________________________________

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
# Take into account length
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
        if True:
            #is_pattern_match(pattern[pattern_index], prev_notes[i-1], prev_notes[i]):
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



# Function to translate from input string to list of note dictionaries
def config_input_string(key:str, input_str:str, mask:bool):
    # 1. get the notes in the key
    notes_in_key=get_scale(key,"M")
    # Format sharps correctly
    notes_with_sharps=[note[1].upper() + "#" if note.find("#") == 0 else note.upper() for note in notes_in_key]
    # Do some note formatting
    #TODO consider the key signature here and how it will affect removing/adding flats and sharps
    # -->for now just removing sharps

    # Boolean indicates if notee
    degree_with_sharp = [True if note[-1] == "#" else False for note in notes_with_sharps]
    notes_in_key=[note.replace("#","") for note in notes_with_sharps]
    notes_in_key=[note.upper() for note in notes_in_key]

    #preset flags
    higher = False
    lower = False
    wait = False
    wait2 = False
    chord = [False, False, False]
    octave = -99
    temp_note = ""

    # 2. (note_index + 1) =  their tonal value
    # 3. Transpose all the notes in the extracted pattern
    # 4. Octave referenced to middle C (0 relates to original Scale's octave)
    # 5. Add Sharps to notes which require it from the Key
    tonal_val_dict_list=[]
    for note in input_str:
        if wait:
            if note == "!" or note == "}":
                wait = False
        elif wait2:
            if note == "]":
                wait2 = False
        elif chord[2]:
            if note == "]":
                chord[0] = False
                chord[1] = False
                chord[2] = False
        else:
            if mask and temp_note != "":
                if chord[1]:
                    chord[2] = True
                try:
                    mask_check = half_step(temp_note.upper(), False)
                    mask_check_index = notes_with_sharps.index(mask_check)
                    mask_check_bool = degree_with_sharp[mask_check_index]
                    if mask_check_bool:
                        if higher:
                            if note=="'":
                                octave += 1
                            else:
                                tonal_val_dict_list.append({"note": mask_check, "degree": str(mask_check_index + 1), "octave": octave})
                                higher = False
                        elif lower:
                            if note==",":
                                octave -= 1
                            else:
                                tonal_val_dict_list.append({"note": mask_check, "degree": str(mask_check_index + 1), "octave": octave})
                                lower = False
                    else:
                        for_list, higher, lower = add_to_dict_list(higher, lower, note, octave, degree_with_sharp, notes_in_key, temp_note, mask, notes_with_sharps)
                        if for_list != {}:
                            tonal_val_dict_list.append(for_list)
                except ValueError:
                    for_list, higher, lower = add_to_dict_list(higher, lower, note, octave, degree_with_sharp, notes_in_key, temp_note, mask, notes_with_sharps)
                    if for_list != {}:
                        tonal_val_dict_list.append(for_list)
            else:
                if chord[1]:
                    chord[2] = True
                for_list, higher, lower = add_to_dict_list(higher, lower, note, octave, degree_with_sharp, notes_in_key, temp_note, mask, notes_with_sharps)
                if for_list != {}:
                    tonal_val_dict_list.append(for_list)

            if not chord[1]:
                if note == "!" or note == "{":
                    wait = True
                elif note == "$":
                    wait2 = True
                elif note == "[":
                    chord[0] = True
                elif note.isalpha():
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
                        if chord[0]:
                            chord[1] = True
                elif note == "|":
                    tonal_val_dict_list.append({"note": "|", "degree": "-1", "octave": "na"})
    return tonal_val_dict_list

def add_to_dict_list(higher:bool, lower:bool, note:str, octave:int, degree_with_sharp:list, notes_in_key:list, temp_note:str, mask:bool, notes_with_sharps:list):

    if higher:
        if note=="'":
            octave += 1
            return {}, higher, lower
        else:
            if mask:
                return {"note": temp_note, "degree": str(notes_with_sharps.index(temp_note.upper()) + 1), "octave": octave}, False, lower
            else:
                if degree_with_sharp[notes_in_key.index(temp_note.upper())]:
                    return {"note": temp_note + "#", "degree": str(notes_in_key.index(temp_note.upper()) + 1), "octave": octave}, False, lower
                else:
                    return {"note": temp_note, "degree": str(notes_in_key.index(temp_note.upper()) + 1), "octave": octave}, False, lower
    elif lower:
        if note==",":
            octave -= 1
            return {}, higher, lower
        else:
            if mask:
                return {"note": temp_note, "degree": str(notes_with_sharps.index(temp_note.upper()) + 1), "octave": octave}, higher, False
            else:
                if degree_with_sharp[notes_in_key.index(temp_note.upper())]:
                    return {"note": temp_note + "#", "degree": str(notes_in_key.index(temp_note.upper()) + 1), "octave": octave}, higher, False
                else:
                    return {"note": temp_note, "degree": str(notes_in_key.index(temp_note.upper()) + 1), "octave": octave}, higher, False
    else:
        return {}, higher, lower

# Function will check if pattern length in bars is within the min to max range
def confirm_pattern_length(start_index, end_index, bar_indices):
    pattern_length = 1
    for i in range(start_index, end_index):
        if i in bar_indices:
            pattern_length += 1

    if (pattern_length >= min_pattern_length) and (pattern_length <= max_pattern_length):
        return True
    else:
        return False

# Function to take in a string of notes and extract the tonic-to-tonic patterns
def tonic_to_tonic_filter(key:str, input_str:str, mask:bool):
    """
    Pro strat: Much more time efficient - lets use this one
    1. Configure the input string into a list of dictionaries
    2. Iterate through entire list of dictionaries saving the position of all tonic notes
    3. Find intervals between tonic notes that are longer than min length and shorter than max length
    4. Extract those intervals
    """
    # 1. Configure the input string into a list of dictionaries
    note_list=config_input_string(key,input_str, mask)

    # 2. Iterate through entire list of dictionaries saving the position of all tonic notes and bar lines
    num_notes=len(note_list)
    tonic_note_indices = []
    bar_indices=[]
    for i in range(0,num_notes):
        if note_list[i]["degree"]=='1':
            tonic_note_indices.append(i)
        if note_list[i]["degree"]=='-1':
            bar_indices.append(i)

    # 3. Find intervals between tonic notes that are longer than min length and shorter than max length
    # need to take into consideration the bar positions since the min and max lengths are in bars
    for_DB = []
    for start_index in tonic_note_indices:
        for end_index in reversed(tonic_note_indices):

            if not confirm_pattern_length(start_index,end_index, bar_indices):
                break
            else:
                # these are patterns of acceptable length -->ready to store in database
                pattern = note_list[start_index:end_index+1]

                #TEST PRINT so you can see the patterns
                #print(str(start_index) + "->" + str(end_index))

                start_note = {}
                end_note = {}
                pattern_interval = []
                interval = []

                for note in pattern:
                    if note["note"] != "|" and note["note"] != "z":
                        if start_note == {}:
                            start_note = note
                        else:
                            end_note = note
                            interval = check_interval(start_note, end_note)
                            start_note = end_note
                            pattern_interval.append(interval)

                for_DB.append({"Pattern": pattern_interval, "num_notes": len(pattern_interval), "Priority": 0})


    return for_DB

def extract_tonal_patterns(file_path:str):

    key = get_header(file_path, 'K')[0]
    
    key, flat_mask = check_for_flat(key)

    v1,v2 = get_melodic_and_rythmic(file_path)

    pattern_list = []

    for item in v1:

        if item != "V:1\n":
            pattern_list += tonic_to_tonic_filter(key, item, flat_mask)

    for item in v2:

        if item != "V:2\n":
            pattern_list += tonic_to_tonic_filter(key, item, flat_mask)

    return pattern_list

def check_for_flat(key:str):

    if len(key) > 1:
        if key[1] == "b":
            return half_step(key[0], False), True
        else:
            return key, False
    else:
        return key, False