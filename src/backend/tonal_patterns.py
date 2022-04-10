from src.backend.music_tools import whole_step, check_interval, half_step
from src.backend.scales import get_scale
from src.backend.cluster import Cluster
from src.backend.models.tonal_pattern_model import TonalPatternModel
from src.backend.abc_tools import (get_header, get_melodic_and_rythmic, get_music,
                                   get_voicings, is_polyphonic)
from src.backend.collections.tonal_pattern import TonalPattern
from src.backend.models.tonal_pattern_model import TonalPatternModel

import os
import itertools

# CONSTANTS_____________________________________________
# values are in bars
min_pattern_length = 3
max_pattern_length = 16
# ______________________________________________________


# TEST PATTERN__________________________________________
test_pattern = "D6 | A6 |$ D6- | D3 z EF | G6 | F6 | %10 E6- | E4 z A,, | B,6 |$ C6 | D6 | E2 F2 G2 | F6 | E6 | D6- | D4 z2 :|$ C2 F- FAc |"
test_key = "D"


# ______________________________________________________

def frequency_of_pattern(analyze_str, key, pattern):
    '''
                !!!INCOMPLETE
                Determines the frequency of a given pattern in the entire song

        '''
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
            elif prev_chars[:1] == "_":  # fix to work with flats
                prev_chars = "#"
                is_flat = True
            else:
                if prev_chars != "":
                    prev_notes.append(prev_chars)

                prev_chars = ""

            # if it is a flat, set it to the sharp equivalent
            if is_flat is True:
                char = whole_step(char, False)
                is_flat = False

            prev_chars += char

    prev_notes.append(prev_chars)

    total = 0
    pattern_index = 0


    for i in range(1, len(prev_notes)):
        # checks for half notes upwards and downwards
        if True:
            # is_pattern_match(pattern[pattern_index], prev_notes[i-1], prev_notes[i]):
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
def config_input_string(key: str, input_str: str, mask: bool):
    '''
                Takes a .abc formatted string and converts it to a list of note dictionaries

                Param:
                    key: The key of the song
                    input_str: The .abc string
                    mask: indicates if the key has been modified from a flat key

                Return:
                    List of notes as dictionaries
        '''
    # 1. get the notes in the key
    notes_in_key = get_scale(key, "M")

    # Do some note formatting

    # Format sharps correctly
    notes_with_sharps = [note[1].upper() + "#" if note.find("#") == 0 else note.upper() for note in notes_in_key]

    # Boolean list indicates if note index has a sharp
    degree_with_sharp = [True if note[-1] == "#" else False for note in notes_with_sharps]

    # Need notes to be without sharps for comparison to .abc notes which came without sharps, depending on key
    notes_in_key = [note.replace("#", "") for note in notes_with_sharps]
    notes_in_key = [note.upper() for note in notes_in_key]

    # preset flags
    higher = False
    lower = False
    wait = False
    wait2 = False
    wait3 = False
    check = False
    chord = [False, False, False]
    octave = -99
    temp_note = ""

    # step by step for loop (skipping minor details like flag setting)
    # 1. Avoid not needed notation (i.e. $, %, etc.)
    # 2. Check for sharp/flat ("^" or "_"), put it in temp_note
    # 3. If note is a rest or bar, add it into the list as rest or bar
    # 4. It note is a applicable Letter note, 3 cases:
    #       1. temp_note == "^" which means current note needs a padded sharp
    #       2. temp_note == "_" which means flat note needs to be converted to sharp
    #       3. anything else, simply temp_note = note
    # 5. Check for following octave notation "'" or ",", and modify octave value as necessary
    # 6. Checks mask value to see if flat key checks need to be done
    # 7. Add note as a Dict to list
    tonal_val_dict_list = []
    for note in input_str:
        if wait:
            if note == "!" or note == "}" or note == "\"":
                wait = False
        elif wait2:
            if note == "]":
                wait2 = False
            if check:
                if note == "!":
                    wait2 = False
                    check = False
            if note == "!":
                check = True
        elif chord[2]:
            if note == "]":
                chord[0] = False
                chord[1] = False
                chord[2] = False
        else:
            if mask and (temp_note != "" and temp_note != "^" and temp_note != "_"):
                if chord[1]:
                    chord[2] = True
                try:
                    mask_check = half_step(temp_note.upper(), False)
                    mask_check_index = notes_with_sharps.index(mask_check)
                    mask_check_bool = degree_with_sharp[mask_check_index]
                    if mask_check_bool:
                        if higher:
                            if note == "'":
                                octave += 1
                            else:
                                tonal_val_dict_list.append(
                                    {"note": mask_check, "degree": str(mask_check_index + 1), "octave": octave})
                                higher = False
                        elif lower:
                            if note == ",":
                                octave -= 1
                            else:
                                tonal_val_dict_list.append(
                                    {"note": mask_check, "degree": str(mask_check_index + 1), "octave": octave})
                                lower = False
                    else:
                        for_list, higher, lower, octave = add_to_dict_list(higher, lower, note, octave,
                                                                           degree_with_sharp, notes_in_key, temp_note,
                                                                           mask, notes_with_sharps)
                        if for_list != {}:
                            tonal_val_dict_list.append(for_list)
                except ValueError:
                    if len(temp_note) > 1:
                        if temp_note[1] == "#":
                            tonal_val_dict_list.append({"note": temp_note[0], "degree": str(notes_in_key.index(temp_note[0].upper()) + 1.5), "octave": octave})
                    else:
                        for_list, higher, lower, octave = add_to_dict_list(higher, lower, note, octave, degree_with_sharp,
                                                                       notes_in_key, temp_note, mask, notes_with_sharps)
                        if for_list != {}:
                            tonal_val_dict_list.append(for_list)
            elif temp_note != "" and temp_note != "^" and temp_note != "_":
                if chord[1]:
                    chord[2] = True
                if len(temp_note) > 1:
                    if temp_note[1] == "#":
                        tonal_val_dict_list.append(
                            {"note": temp_note[0], "degree": str(notes_in_key.index(temp_note[0].upper()) + 1.5),
                             "octave": octave})
                else:
                    for_list, higher, lower, octave = add_to_dict_list(higher, lower, note, octave, degree_with_sharp,
                                                                   notes_in_key, temp_note, mask, notes_with_sharps)
                    if for_list != {}:
                        tonal_val_dict_list.append(for_list)
            if not chord[1]:
                if note == "!" or note == "{" or note == "\"":
                    wait = True
                elif note == "$":
                    wait2 = True
                elif note == "[":
                    chord[0] = True
                elif note == "x":
                    wait3 = True
                elif note == "^" or note == "_":
                    temp_note = note
                elif note.isalpha() and note != "P" and note != "T":
                    if note == "z":
                        tonal_val_dict_list.append({"note": "z", "degree": "0", "octave": "na"})
                    elif chord[0] and (note == "Q" or note == "K" or note == "M" or note == "I"):
                        chord[2] = True
                    else:
                        if wait3:
                            if not note.isnumeric():
                                wait3 = False

                        if note.islower() and not wait3:
                            higher = True
                            octave = 1
                            if temp_note == "^":
                                temp_note = note + "#"
                            elif temp_note == "_":
                                temp_note = half_step(note, False)
                            else:
                                temp_note = note
                        elif not wait3:
                            lower = True
                            octave = 0
                            if temp_note == "^":
                                temp_note = note + "#"
                            elif temp_note == "_":
                                temp_note = half_step(note, False)
                            else:
                                temp_note = note
                        if chord[0]:
                            chord[1] = True
                elif note == "|":
                    tonal_val_dict_list.append({"note": "|", "degree": "-1", "octave": "na"})
    return tonal_val_dict_list


def add_to_dict_list(higher: bool, lower: bool, note: str, octave: int, degree_with_sharp: list, notes_in_key: list,
                     temp_note: str, mask: bool, notes_with_sharps: list):
    '''
                    Given various input parameters which help determine the note, add a note to the list in the format of a dictionary

                    Param:
                        higher: flag indicates if note is being analyzed and octave > 0
                        lower: flag indicates if note is being analyzed and octave <= 0
                        note: current char from the .abc input string
                        octave: current analyzed octave value of the input note
                        degree_with_sharp: list with flags ti indicate if note need a sharp to be added (due to key)
                        notes_in_key: list with notes (formatted to match .abc) for matching purposes
                        temp_note: with correct flags set (higher/lower), temp_note will contain a note (with sharp if sharp was in .abc format)
                        mask: flag indicates if the key was modified from being a flat key
                        notes_with_sharps: relevant list for matching purposes is mask=True

                    Return:
                        2 Options. Could return and empty dict with un-modified flags changing the octave value, or
                            could return a note in Dict format while also resetting flag
            '''

    if higher:
        if note == "'":
            octave += 1
            return {}, higher, lower, octave
        else:
            if mask:
                return {"note": temp_note, "degree": str(notes_with_sharps.index(temp_note.upper()) + 1),
                    "octave": octave}, False, lower, octave
            else:
                if degree_with_sharp[notes_in_key.index(temp_note.upper())]:
                    return {"note": temp_note + "#", "degree": str(notes_in_key.index(temp_note.upper()) + 1),
                            "octave": octave}, False, lower, octave
                else:
                    return {"note": temp_note, "degree": str(notes_in_key.index(temp_note.upper()) + 1),
                        "octave": octave}, False, lower, octave
    elif lower:
        if note == ",":
            octave -= 1
            return {}, higher, lower, octave
        else:
            if mask:
                return {"note": temp_note, "degree": str(notes_with_sharps.index(temp_note.upper()) + 1),
                        "octave": octave}, higher, False, octave
            else:
                if degree_with_sharp[notes_in_key.index(temp_note.upper())]:
                    return {"note": temp_note + "#", "degree": str(notes_in_key.index(temp_note.upper()) + 1),
                            "octave": octave}, higher, False, octave
                else:
                    return {"note": temp_note, "degree": str(notes_in_key.index(temp_note.upper()) + 1),
                            "octave": octave}, higher, False, octave
    else:
        return {}, higher, lower, octave


# Function will check if pattern length in bars is within the min to max range
def confirm_pattern_length(start_index, end_index, bar_indices):
    '''
            Determines if the given pattern is within the allowed length, preset with constants

            Param:
                start_index: The index of the start of the pattern in the note list
                end_index: The index of the end of the pattern in the note list
                bar_indices: indicates which values to omit because they are note notes

            Return:
                True or False if pattern length is within range
    '''

    pattern_length = 1
    for i in range(start_index, end_index):
        if i in bar_indices:
            pattern_length += 1

    if (pattern_length >= min_pattern_length) and (pattern_length <= max_pattern_length):
        return True
    else:
        return False


# Function to take in a string of notes and extract the tonic-to-tonic patterns
def tonic_to_tonic_filter(key: str, input_str: str, mask: bool):
    '''
            This filter finds patterns given that the pattern begins and ends with a tonic note, within a given range of length

            Param:
                key: The key of the song
                input_str: An .abc string of notes
                mask: indicates if key was modified from being flat key

            Return:
                List of patterns
    '''
    # 1. Configure the input string into a list of dictionaries
    note_list = config_input_string(key, input_str, mask)

    # 2. Iterate through entire list of dictionaries saving the position of all tonic notes and bar lines
    num_notes = len(note_list)
    tonic_note_indices = []
    bar_indices = []
    for i in range(0, num_notes):
        if note_list[i]["degree"] == '1':
            tonic_note_indices.append(i)
        if note_list[i]["degree"] == '-1':
            bar_indices.append(i)

    # 3. Find intervals between tonic notes that are longer than min length and shorter than max length
    # need to take into consideration the bar positions since the min and max lengths are in bars
    for_DB = []
    for start_index in tonic_note_indices:
        for end_index in reversed(tonic_note_indices):

            if not confirm_pattern_length(start_index, end_index, bar_indices):
                break
            else:
                # these are patterns of acceptable length -->ready to store in database
                pattern = note_list[start_index:end_index + 1]

                start_note = {}
                end_note = {}
                pattern_interval = []
                interval = []

                # For the notes in the pattern, find the intervals (independent of the key) for the notes as a separate
                # pattern list
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


def extract_tonal_patterns(file_path: str):
    '''
        Given filepath to a song in ABC format, gets tonal patterns from that song

        Param:
            file_path: file path assumed to be to .ABC song

        Return:
            The list of patterns
    '''

    key = get_header(file_path, 'K')[0]

    key, flat_mask = check_for_flat(key)

    v1, v2 = get_melodic_and_rythmic(file_path)

    pattern_list = []

    for item in v1:

        if item != "V:1\n":
            pattern_list += tonic_to_tonic_filter(key, item, flat_mask)

    for item in v2:

        if item != "V:2\n":
            pattern_list += tonic_to_tonic_filter(key, item, flat_mask)

    return pattern_list

def extract_tonal():

    # the main dir
    str_dir = 'src/backend/mxl_to_abc/converted_compositions'

    # gets each file from the given directory
    directory = os.fsencode(str_dir)

    for file in os.listdir(directory):

        # gets the filename of the given file
        filename = os.fsdecode(file)

        # checks if hte given file ends with the right extension
        if filename.endswith('.abc'):
            # concat the directory with the file name
            file_path = str_dir + "/" + filename

            # extracts the header from the given abc file
            composition_name = get_header(file_path, 'T')

            if isinstance(composition_name, list):
                composition_name = composition_name[0]

            if composition_name[0] == ".":
                composition_name = composition_name[1:]

            if composition_name[-1] == ".":
                composition_name = composition_name[:-1]

            composition_name = composition_name.replace(" ", "_")

            pattern_list = extract_tonal_patterns(file_path)
            tonal_list = []

            for pattern in pattern_list:

                tonal_list.append(TonalPattern(pattern["Pattern"], pattern["num_notes"], pattern["Priority"]))

            cluster_instance = Cluster("thomas", composition_name, False)
            model = TonalPatternModel(composition_name, tonal_list)
            cluster_instance.insert_tonal_pattern_model(cluster_instance, model)


def check_for_flat(key: str):
    '''
        Checks if the key is a flat key and converts it to its sharp equivalent. Also sets associated flag

        Param:
            key: the key to check for flat

        Return:
            The key, modified if necessary, and the flag set to true if modified
    '''

    if len(key) > 1:
        if key[1] == "b":
            return half_step(key[0], False), True
        else:
            return key, False
    else:
        return key, False