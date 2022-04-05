

# REMOVE THIS BEFORE MERGING INTO MASTER
# ===========================================================
# only uncomment this if you are not using pycharm
import inspect
import os
import random as rand
import sys
import re
import time
from datetime import datetime as dt
from msilib.schema import Error

currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parent2 = os.path.dirname(parentdir)
sys.path.insert(0, parent2)
# END OF IMPORTS FOR NON-PYCHARM USERS (mostly just for Elliot)
# ===========================================================
# REMOVE THIS BEFORE MERGING INTO MASTER
from src.backend.cluster import Cluster
from src.backend.collections.note_pattern import Note_Pattern
from src.backend.collections.rhythmic_pattern import Rhythmic_Pattern
from src.backend.collections.tonal_pattern import TonalPattern
from src.backend.music_tools import (M3, P5, change_octave, half_step, m3,
                                     whole_step)
from src.backend.scales import get_scale

'''
Takes in a genre and returns a song template for the given genre

Parameters:
    genre: the genre to return the song template

Return:
    the song template based on the given genre
'''
def get_song_template(genre):
    return ['A', 'A', 'B', 'A']


fail_window = 0
fail_length = 0

'''
Gets a key and returns a combination of rhythmic patterns

Parameters:
    key : the key to return the patterns in

Returns:
    a combination of patterns that matches the selected style
'''
def build_rhythmic_pattern(key):

    # gets a random song name from the list of songs that exist within the database
    song_name = _get_random_song_name()

    # selected_style will be one of the pattern_styles above
    selected_style = _get_random_pattern_style()

    # fetch the patterns from the db based on the selected style
    length_1 = selected_style[0]
    length_2 = selected_style[1]

    # get the list of rhythmic pattern objects for the given song that matches the given length
    pattern_1 = _get_rhythmic_patterns(song_name, length_1)
    pattern_2 = _get_rhythmic_patterns(song_name, length_2)

    # if pattern_1 is empty (meaning the given song name does not have matching pattern lengths)
    while(not pattern_1 or not pattern_2):
        song_name = _get_random_song_name()
        pattern_1 = _get_rhythmic_patterns(song_name, length_1)
        pattern_2 = _get_rhythmic_patterns(song_name, length_2)

    # randomly generate another pattern as long as pattern_1 == pattern_2
    while(pattern_1 is pattern_2):
        pattern_2 = _get_rhythmic_patterns(song_name, length_2)

    combined_pattern = pattern_1.pattern.copy()
    combined_pattern.extend(pattern_2.pattern)

    combined_rhythmic_pattern_object = Rhythmic_Pattern(combined_pattern, 0, False)

    return combined_rhythmic_pattern_object


'''
Selects a random song name from the list of songs within the database

Parameters:
    get_from_tonal_patterns: if this is true, get the song names from "thomas" db instead

Return:
    A list of song names 
'''
def _get_random_song_name(get_from_tonal_patterns=False):
    song_names = _get_db_song_names(get_from_tonal_patterns)

    selected_index = _get_random_number(len(song_names) - 1)

    return song_names[selected_index]


'''
Randomly selects a pattern style

Return:
    a random selected pattern style that has a length of 8 
'''
def _get_random_pattern_style():
    # Each of this are the possible combinations of bars
    pattern_style = [(4, 4), (3, 5), (5, 3)]

    # randomly selects a pattern style and return it
    selected_index = _get_random_number(
        len(pattern_style) - 1) if len(pattern_style) > 1 else 0

    return pattern_style[selected_index]


'''
Gets a list of Rhythmic Pattern objects from the db within the given collection that matches the pattern length

Parameters:
    song_name : the song name to search for the patterns (the name of the collection)
    pattern_length : the length for the patterns to match with

Return:
    a list of Rhythmic Pattern objects that matches the given pattern length within the given collection name
'''
def _get_rhythmic_patterns(song_name, pattern_length):
    db_name = "elliot"
    is_admin = False

    # DEBUG
    counter = 0

    # making connection to the DB
    db = _make_db_connection(db_name, is_admin, song_name)

    list_of_matching_length_songs = db.query_rhythmic_patterns(
        db, song_name, pattern_length)

    # if there is a matching pattern length within the given song name, then return it
    if (list_of_matching_length_songs):
        # the length of all the matching song lengths
        matching_songs_length = len(list_of_matching_length_songs)
        # randomly generate an index
        selected_index = _get_random_number(matching_songs_length - 1) if matching_songs_length > 1 else 0
        # take a randomly selected pattern
        pattern_to_return = list_of_matching_length_songs[selected_index]
        # while the selected pattern is V1, and there are other options, regenerate get a new pattern from the same song
        while not pattern_to_return.is_v1 and matching_songs_length > 1:
            selected_index = _get_random_number(matching_songs_length - 1)
            pattern_to_return = list_of_matching_length_songs[selected_index]

            counter += 1
            # if it has been looping for more than 10 times, break
            if counter > 10:
                break

        return list_of_matching_length_songs[selected_index]

    # els return nothing
    else:
        return None


'''
Gets a list of song names that exist within the database

Parameters: 
    get_from_tonal_patterns: if this is set to true, then get all song names from "thomas" db instead

Return:
    a list of all the song names within the database 
'''
def _get_db_song_names(get_from_tonal_patterns:False):
    is_admin = False
    
    db_name = "elliot" if not get_from_tonal_patterns else "thomas"

    # making connection to the DB
    db = _make_db_connection(db_name, is_admin)

    # get the list of song names
    song_names = db.get_collection_names(db)

    # return a list of all collection names
    return song_names


'''
Make initial DB connection 

Parameters:
    database_name : the database name to connect to
    is_admin : a boolean value to specify the admin status
    colleciton_name : the collection name to return (None will return all collection names)

Return:
    a cluster instance
'''
def _make_db_connection(database_name, is_admin, collection_name=None):

    database = Cluster(database_name, collection_name,
                       is_admin) if collection_name else Cluster(database_name, "", is_admin)

    return database


'''
Converts each pattern given to notes

Parameters:
    key: the starting note to step up or step down from
    tonal_pattern: the tonal pattern object that has the attribute of steps required

Return:
    a list of notes that matches the pattern
'''
def convert_tonal_pattern(key, tonal_pattern):
    #DEBUG
    print(f"Converting tonal patterns...")
    #DEBUG END
    pattern = tonal_pattern.pattern
    to_return = []

    # sets the current note
    current_note = key[0]

    to_return.append(current_note)

    for lst in pattern:
        for step in lst:
            if 'h' in step:
                new_note = half_step(
                    current_note, False) if '-' in step else half_step(current_note, True)
            elif 'w' in step:
                new_note = whole_step(
                    current_note, False) if '-' in step else whole_step(current_note, True)
            elif 'm3' in step:
                new_note = m3(
                    current_note, False) if '-' in step else m3(current_note, True)
            elif 'M3' in step:
                new_note = M3(
                    current_note, False) if '-' in step else M3(current_note, True)
            elif 'P5' in step:
                new_note = P5(
                    current_note, False) if '-' in step else P5(current_note, True)
            elif 'o' in step:
                new_note = change_octave(
                    current_note, False) if '-' in step else change_octave(current_note, True)
            elif '0' in step:
                new_note = current_note

            # update the current note
            current_note = new_note

            # add the current note to the list
            to_return.append(current_note)

    return to_return


def _strip_modifiers_from_scale(scale):
    scale_to_return = []

    note_to_add = None

    for note in scale:
        note_to_add = note if note.isalpha() or "#" in note else None  
        scale_to_return.append(note_to_add)

    return scale_to_return

'''
Given a starting note and an ending note, fill in the number of notes
based on the num_beats, with each note at most +2 from current note or -2
from the current note.

Parameters:
    key: The key to generate the scale in
    start_note: the starting note of the pattern
    end_note: the ending note of the pattern
    num_beats: the number of elements to fill

Return:
    A list of randomly generated notes that sounds nice together
    within the given key of the scale
'''
def bridge_pattern(key, tonal_pattern_1, tonal_pattern_2, num_beats):
    # get the initial scale for this given key
    scale = _get_random_scale_type(key)
    scale = _strip_modifiers_from_scale(scale)

    bridged_patterns = []

    if not tonal_pattern_1 or not tonal_pattern_2 or not num_beats:
        return None

    # a variable to hold the notes
    current_note = tonal_pattern_1[-1]

    # QUESTION
    # LAST NOTE IS STILL NOT USED
    last_note = tonal_pattern_2[0]

    while (num_beats > 0):

        # get the window within the scale given the current note
        window = _get_window(current_note, scale)

        # randomly generate an index between 0 and 3 (4 = window size)
        selected_index = _get_random_number(3)

        # the selected note will be in this variable
        selected_note = window[selected_index]

        # update the current note
        current_note = selected_note

        bridged_patterns.append(current_note)

        num_beats -= 1

    # out of the loop, append the 2nd part of the tonal_pattern
    bridged_patterns.extend(tonal_pattern_2)

    return bridged_patterns


def _strip_note_modifiers(note):

    if not note:
        return None

    to_return = ""

    for c in note:
        to_return += c if c.isalpha() or c == "#" else ""

    return to_return


'''
Given the note and the scale, generates a window of notes
of length 4, (+2 and -2 index from the given note within the scale)

Parameters:
    note: The note to go up by 2 and down by 2 in the scale
    scale: the scale that the given note exist within

Return:
    a list of 4 notes (+2 from note and -2 from note)
'''
def _get_window(note, scale):
    global fail_length, fail_window
    #DEBUG
    print(f"Getting window...")
    # DEBUG END

    # empty placeholder to be returned
    window = []

    note = _strip_note_modifiers(note)

    # only used if the given note has reached the highest octave
    previous_note = None
    keep_going_up = True

    # DEBUG
    counter = 0

    temp = note
    lower = ""
    upper = ""

    # while the upper note is still not in the scale
    while temp not in scale:


        temp = half_step(temp, True) if keep_going_up else half_step(temp, False)
        
        temp = _strip_note_modifiers(temp)

        if not temp or temp == previous_note or temp == note:
            keep_going_up = False
            temp = note.upper() if note.islower() else note.lower()

        previous_note = temp if temp else note

        if counter >= 50:
            # DEBUG
            print("Failed to get window :(")
            fail_window += 1
            raise Error("Just raise an error so I can see what broke")
        counter += 1

    # gets the index of the note within the scale
    index_of_note = scale.index(temp)

    length_of_scale = len(scale)

    lower_bound_2 = index_of_note - 2
    lower_bound_1 = index_of_note - 1
    upper_bound_2 = index_of_note + 2
    upper_bound_1 = index_of_note + 1

    # make it so that it loops back to the top/bottom of the list
    if lower_bound_2 < 0:
        lower_bound_2 = length_of_scale - abs(lower_bound_2)
    if upper_bound_2 >= length_of_scale:
        upper_bound_2 %= length_of_scale
    if lower_bound_1 < 0:
        lower_bound_1 = length_of_scale - abs(lower_bound_1)
    if upper_bound_1 >= length_of_scale:
        upper_bound_1 %= length_of_scale

    # append all the 4 neighbouring notes to the window
    window.append(scale[lower_bound_1])
    window.append(scale[lower_bound_2])
    window.append(scale[upper_bound_1])
    window.append(scale[upper_bound_2])

    return window


'''
Gets a scale given the key with a random type

Parameters
    key: The key to generate the scale in
    test: only set to True for testing

Return
    The generated scale in the given key
'''
def _get_random_scale_type(key, test=False):
    # split the root and the scale type
    root = key[0]
    scale_type = key[1]

    # only used for testing
    if test:
        generated_scale = get_scale(root, 'M')
        return generated_scale

    # the differnt types of scale types
    minor_scale_types = ['m', 'pm']
    major_scale_types = ['M', 'pM']

    # randomly generate a number, if its even then use minor / major scales,
    # else if its odd then use either pentatonic minor / major (50 / 50 chances)
    selected_index = 0 if (_get_random_number(100) % 2 == 0) else 1

    # This will hold the scale type
    selected_scale_type = minor_scale_types[selected_index] if 'm' in scale_type else major_scale_types[selected_index]

    # this will hold the generated scale
    generated_scale = get_scale(root, selected_scale_type)

    return generated_scale


'''
Returns a random number between the range of [0,limit]

Parameters:
    limit: the maximum value that can be randomly generated 
    start: the starting value

Return:
    a randomly generated value within the range of [0,limit]
'''
def _get_random_number(limit, start=0):
    # set the seed
    rand.seed(dt.now().timestamp())

    # a quick nap of about 3ms so that it doesnt always use the same seed if this function is called multiple times consecutively
    time.sleep(0.003)

    # return the generated number only if the given limit is greater than the start
    value = rand.randint(start, limit) if limit != 0 and limit > start else 0

    return value


'''

'''
def build_verse(key, rhythmic_pattern:Rhythmic_Pattern):
    # the list to return
    verse_to_return = []
    # temporary placeholder for holding all the combined patterns with the bridge patterns
    verse_in_list = []

    # number of available patterns left to get
    num_available_patterns = 4

    # bridge pattern buffer size
    bridge_pattern_buffer_size = 0

    num_beats_left = rhythmic_pattern.beats

    # select a tonal pattern and add it to the list_of_selected_tonal_patterns
    list_of_selected_tonal_patterns = []

    #DEBUG
    print(f"Getting tonal patterns...")
    # DEBUG END
    selected_tonal_pattern = get_tonal_pattern(num_beats_left)
    list_of_selected_tonal_patterns.append(selected_tonal_pattern)

    # update the num_beats_left
    num_beats_left -= selected_tonal_pattern.num_of_notes

    # handle the case where there is only one pattern + 1->3 extra notes
    if num_beats_left < 3:
        bridge_pattern_buffer_size += num_beats_left
    else:
        while num_beats_left > 4 and num_available_patterns > 0:
        
            # get a tonal pattern and add it to the list_of_selected_tonal_patterns
            #DEBUG
            print(f"Getting tonal patterns...")
            # DEBUG END
            selected_tonal_pattern = get_tonal_pattern(num_beats_left)
            list_of_selected_tonal_patterns.append(selected_tonal_pattern)

            # decrease the count of available patterns and the remaining number of beats required
            num_beats_left -= selected_tonal_pattern.num_of_notes
            num_available_patterns -= 1

            # each tonal pattern added to the list should have 3 beats (if possible) allocated to bridge it to the others
            if num_beats_left <= 6 and len(list_of_selected_tonal_patterns) > 1:
                break
            else:
                bridge_pattern_buffer_size+=3

        bridge_pattern_buffer_size += num_beats_left

    if len(list_of_selected_tonal_patterns) == 1:
        print(f"Making single bridge...")
        converted_tonal_pattern = convert_tonal_pattern(key, list_of_selected_tonal_patterns[0])
        single_bridge = bridge_pattern(key, converted_tonal_pattern, [key[0]], bridge_pattern_buffer_size)
        converted_tonal_pattern.extend(single_bridge)
        verse_to_return = converted_tonal_pattern
        return verse_to_return 

    # randomly allocate bridge lengths
    #DEBUG
    print(f"Getting random bridge lengths...")
        # DEBUG END
    bridge_lengths = _get_random_bridge_length(
        bridge_pattern_buffer_size, len(list_of_selected_tonal_patterns) - 1)

    # loops through all the existing tonal patterns
    for index in range(len(list_of_selected_tonal_patterns)-1):

        first_tonal_pattern_obj = list_of_selected_tonal_patterns[index]
        second_tonal__pattern_obj = list_of_selected_tonal_patterns[index + 1]

        # convert the pattern to notes
        first_converted_pattern = convert_tonal_pattern(key, first_tonal_pattern_obj)
        second_converted_pattern = convert_tonal_pattern(key, second_tonal__pattern_obj)

        verse_in_list.extend(first_converted_pattern)
        # and brige them together
        #DEBUG
        print(f"Bridging patterns...")
        # DEBUG END
        bridged_pattern = bridge_pattern(key,first_converted_pattern, second_converted_pattern, bridge_lengths[index])
        # add the bridged pattern in to the exising verse
        verse_in_list.extend(bridged_pattern)

    # pair each rhythmic pattern with the generated notes
    #DEBUG
    print(f"Pairing tonal patterns with rhytmic patterns...")
    # DEBUG END
    verse_to_return = match_rhythmic_with_tonals(rhythmic_pattern, verse_in_list)

    return verse_to_return


def get_tonal_pattern(num_beats_left):

    db_name = "thomas"
    is_admin = False
    # get a random song name from "thomas" db
    song_name = _get_random_song_name(get_from_tonal_patterns=True)
    # database connection
    database = _make_db_connection(db_name, is_admin, song_name)
    # if the database connection failed, return None
    if not database:
        return None

    # DEBUG
    counter = 0

    # get all the tonal patterns of the given song name
    tonal_patterns_of_given_song = database.query_tonal_patterns(database, song_name, num_beats_left-3)

    while not tonal_patterns_of_given_song and num_beats_left > 4 and counter < 30:
        counter += 1
        song_name = _get_random_song_name(get_from_tonal_patterns=True)
        # database connection
        database = _make_db_connection(db_name, is_admin, song_name)
        # if the database connection failed, return None
        if not database:
            return None
        tonal_patterns_of_given_song = database.query_tonal_patterns(database, song_name, num_beats_left-3)

    # gets a random number to select a random tonal pattern
    selected_index = _get_random_number(len(tonal_patterns_of_given_song) - 1)

    # the randomly selected tonal pattern
    return tonal_patterns_of_given_song[selected_index]

'''
pairs the rhythimc pattern with the tonal patterns

Parameters:
    rhythmic_pattern: The rhythimc pattern object to get the rhythimc patterns from
    verse_note_list: a list of notes that have been converted to match the length of the rhythmic pattern

Return:
    a list of Note_Patterns that has the length of each note / chord along with the note itself
'''


def match_rhythmic_with_tonals(rhythmic_pattern:Rhythmic_Pattern, verse_note_list):
    # the patterns to match
    pattern = rhythmic_pattern.pattern 
    # an empty placeholder
    to_return = []

    # DEBUG
    if len(verse_note_list) < len(pattern):
        global fail_length
        print(f"The length of verse_note_list {len(verse_note_list)} is shorter than the pattern length of {rhythmic_pattern.beats}")
        fail_length += 1
        raise IndexError("out of bounds")
    # DEBUG END

    index = 0

    is_chord = False
    break_outer_loop = False

    # loop through the given rthythmic pattern, create a note pattern object, and append ot to the list to be returned
    for bar in pattern:
        for notes in bar:
            if len(notes) == 3 and '(' in notes and ')' in notes:
                to_return.append(Note_Pattern("z", notes[1]))
            else:
                beam_beats = list(filter(None, re.split("(\W)", notes)))

                for beats in beam_beats:
                    if beats == "[":
                        is_chord = True
                        
                    elif is_chord:
                        to_return.append(Note_Pattern(verse_note_list[index], "[" + str(beats) + "]"))
                        index += 1
                        is_chord = False
                    
                    elif beats.isdigit():
                        for individual_beat in beats:
                            to_return.append(Note_Pattern(verse_note_list[index], individual_beat))
                            index += 1

                            
                    


    return to_return


'''
Gets a random bridge length to return

Parameters:
    total_length: the total length of all the bridge buffers

Return:
    a list of each size of the bridge length
'''
def _get_random_bridge_length(total_length, number_of_bridges):
    global fail_length, fail_window

    length_to_return = []
    min_length=3
    if total_length < 3:
        min_length=total_length

    # initially, fill each length to return with 3
    for _ in range(number_of_bridges):
        length_to_return.append(min_length)

    remaining_length = total_length - (min_length * number_of_bridges)

    while(remaining_length > 0 and number_of_bridges > 0):
        random_selected_index = _get_random_number(number_of_bridges-1)
        length_to_return[random_selected_index] += 1 
        remaining_length -= 1

    return length_to_return

# DEBUG
counter = 0
limit = 200
failed = 0
success = 0
notes_to_pick = ['A','B','C','D','E','F','G']
modifiers = ['M', 'm']


while(True):
    counter += 1
    try:

        note_to_use =notes_to_pick[_get_random_number(len(notes_to_pick) - 1)]
        modifier_to_use = modifiers[_get_random_number(len(modifiers) - 1)]
        key_to_use = note_to_use + modifier_to_use

        
        print(f"===== Starting Run number {counter} using {key_to_use}...")
        combined_rhythmic_pattern = build_rhythmic_pattern(key_to_use)
        verse = build_verse(key_to_use, combined_rhythmic_pattern)
        success += 1
        
        print(f"This is the original pattern{combined_rhythmic_pattern.pattern}")

        # for note in verse:
        #     if note is None:
        #         print("what")
        #     print(note)

        print(f"===== Run number {counter} has been successful!")
        print()

    except:
        print(f" ----- error occured on try number {counter}")
        print()
        failed += 1
        break

    

print(f"{success} / {counter}  || Window Fail Count : {fail_window} and Length Fail Count: {fail_length}:: The success rate is {(success / counter) * 100}%")
# DEBUG - END
