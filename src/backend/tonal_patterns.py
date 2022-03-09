from src.backend.music_tools import whole_step, check_interval
from src.backend.scales import get_scale
from src.backend.cluster import Cluster
from src.backend.models.tonal_pattern_model import TonalPatternModel
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
def config_input_string(key:str, input_str:str):
    # 1. get the notes in the key
    notes_in_key=get_scale(key,"M")
    # Format sharps correctly
    notes_in_key=[note[1] + "#" if note.find("#") == 0 else note for note in notes_in_key]
    # Do some note formatting
    #TODO consider the key signature here and how it will affect removing/adding flats and sharps
    # -->for now just removing sharps

    # Boolean indicates if notee
    degree_with_sharp = [True if note[-1] == "#" else False for note in notes_in_key]
    print("Tahng")
    print(degree_with_sharp)
    print(notes_in_key)
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
    # 5. Add Sharps to notes which require it from the Key
    tonal_val_dict_list=[]
    for note in input_str:
        if higher:
            if note=="'":
                octave += 1
            else:
                if degree_with_sharp[notes_in_key.index(temp_note.upper())]:
                    tonal_val_dict_list.append(
                        {"note": temp_note + "#", "degree": str(notes_in_key.index(temp_note.upper()) + 1), "octave": octave})
                else:
                    tonal_val_dict_list.append(
                        {"note": temp_note, "degree": str(notes_in_key.index(temp_note.upper()) + 1), "octave": octave})
                higher = False
        elif lower:
            if note==",":
                octave -= 1
            else:
                if degree_with_sharp[notes_in_key.index(temp_note.upper())]:
                    tonal_val_dict_list.append(
                        {"note": temp_note + "#", "degree": str(notes_in_key.index(temp_note) + 1), "octave": octave})
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
    return tonal_val_dict_list

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
def tonic_to_tonic_filter(key:str, input_str:str):
    """
    Pro strat: Much more time efficient - lets use this one
    1. Configure the input string into a list of dictionaries
    2. Iterate through entire list of dictionaries saving the position of all tonic notes
    3. Find intervals between tonic notes that are longer than min length and shorter than max length
    4. Extract those intervals
    """
    # 1. Configure the input string into a list of dictionaries
    note_list=config_input_string(key,input_str)

    # 2. Iterate through entire list of dictionaries saving the position of all tonic notes and bar lines
    num_notes=len(note_list)
    tonic_note_indices = []
    bar_indices=[]
    for i in range(0,num_notes):
        if note_list[i]["degree"]=='1':
            tonic_note_indices.append(i)
        if note_list[i]["degree"]=='-1':
            bar_indices.append(i)
    print(tonic_note_indices)
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
                print(str(start_index) + "->" + str(end_index))

                start_note = {}
                end_note = {}
                pattern_interval = []
                interval = []
                value = False

                for note in pattern:
                    if note["note"] != "|" and note["note"] != "z":
                        if start_note == {}:
                            start_note = note
                        else:
                            end_note = note
                            interval, octave = check_interval(start_note, end_note)
                            start_note = end_note
                            pattern_interval.append(interval)
                            if octave:
                                value = True

                for_DB.append({"Key": key, "Pattern": pattern_interval, "Octave_Change": value})

    return for_DB

def tonal_patterns():

    for_db = tonic_to_tonic_filter(test_key, test_pattern)

    database = Cluster("thomas", "tonal_patterns", False)

    for pattern in for_db:
        t_model = TonalPatternModel(pattern["Key"], pattern["Pattern"], pattern["Octave_Change"])
        result = database.insert_model(database, t_model)
        if result:
            print("success")
        else:
            print("Failure")

# TESTING STUFF~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print("FInput PATTERN:")

tonal_patterns()
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~