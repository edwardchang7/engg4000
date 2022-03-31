import inspect
from lib2to3.pygram import pattern_symbols
# REMOVE THIS BEFORE MERGING INTO MASTER
# ===========================================================
# only uncomment this if you are not using pycharm
import os
import random as rand
import sys
import time
from datetime import datetime as dt

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
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
from src.backend.music_tools import M3, P5, change_octave, half_step, m3, whole_step
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

    return pattern_1, pattern_2


'''
Selects a random song name from the list of songs within the database

Return:
    A list of song names 
'''
def _get_random_song_name():
    song_names = _get_db_song_names()

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
    selected_index = _get_random_number(len(pattern_style) - 1) if len(pattern_style) > 1 else 0

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

    # making connection to the DB
    db = _make_db_connection(db_name, is_admin, song_name)

    list_of_matching_length_songs = db.query_rhythmic_patterns(
        db, song_name, pattern_length)

    # if there is a matching pattern length within the given song name, then return it
    if (list_of_matching_length_songs):

        matching_songs_length = len(list_of_matching_length_songs)

        selected_index = rand.randint(0, matching_songs_length - 1) if matching_songs_length > 1 else 0

        return list_of_matching_length_songs[selected_index]

    # els return nothing
    else:
        return None


'''
Gets a list of song names that exist within the database

Return:
    a list of all the song names within the database 
'''
def _get_db_song_names():
    db_name = "elliot"
    is_admin = False

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

    database = Cluster(database_name, collection_name, is_admin) if collection_name else Cluster(database_name, "", is_admin)

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
    pattern = tonal_pattern.pattern
    to_return = []

    # sets the current note
    current_note = key

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

    if not tonal_pattern_1 or not tonal_pattern_2 or not num_beats: return None

    # a variable to hold the notes
    current_note = tonal_pattern_1.pattern[-1]
    last_note = tonal_pattern_2.pattern[0]

    # create an empty list to hold the value to return
    # gets a copy of the patterns array since a reference is passed in Python, not the value
    bridged_patterns = tonal_pattern_1.pattern.copy()

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
    bridged_patterns.extend(tonal_pattern_2.pattern)

    return bridged_patterns


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

    # empty placeholder to be returned
    window = []

    # gets the index of the note within the scale
    index_of_note = scale.index(note)

    length_of_scale = len(scale)

    lower_bound_2 = index_of_note - 2
    lower_bound_1 = index_of_note - 1
    upper_bound_2 = index_of_note + 2
    upper_bound_1 = index_of_note + 1

    # make it so that it loops back to the top/bottom of the list
    if lower_bound_2 < 0: lower_bound_2 = length_of_scale - abs(lower_bound_2)
    if upper_bound_2 >= length_of_scale: upper_bound_2 %= length_of_scale
    if lower_bound_1 < 0: lower_bound_1 = length_of_scale - abs(lower_bound_1)
    if upper_bound_1 >= length_of_scale: upper_bound_1 %= length_of_scale

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
    major_scale_types = ['M', 'pm']

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

    # return the generated number
    value = rand.randint(start, limit)

    return value

'''

'''
def build_verse(rhy_pattern):
    # the list to return
    verse_to_return = [] 
    # temporary placeholder for holding all the combined patterns with the bridge patterns
    verse_in_list = []

    # number of available patterns left to get
    num_available_patterns = 4

    # bridge pattern buffer size
    bridge_pattern_buffer_size = 12

    # the key list for the dictionary to return
    key_list = rhy_pattern.pattern

    # the number of beats left after subtracting the bridge pattern buffer
    num_beats_left = rhy_pattern.beats - bridge_pattern_buffer_size

    # selected tonal patterns
    list_of_selected_tonal_patterns = []

    while num_beats_left > 2 and num_available_patterns > 0:
        # a randomly selected song name
        song_name = _get_random_song_name()

        # get all TP of the given song name
        tonal_pattens_of_given_song = None # CHANGE THIS

        # gets a random number to select a random tonal pattern
        selected_index = _get_random_number(len(tonal_pattens_of_given_song) -1)

        # the randomly selected tonal pattern
        selected_tonal_pattern = tonal_pattens_of_given_song[selected_index]

        # add it to a list of selected tonal patterns
        list_of_selected_tonal_patterns.append(selected_tonal_pattern)

        # decrease the count of available patterns and the remaining number of beats required
        num_beats_left -= 1
        num_available_patterns -= 1

    # get the new buffer size
    bridge_pattern_buffer_size += num_beats_left

    # a randomly generated list of bridge lengths
    bridge_lengths = _get_random_bridge_length(bridge_pattern_buffer_size, len(list_of_selected_tonal_patterns) -1)

    # loops through all the existing tonal patterns
    for index in range(len(list_of_selected_tonal_patterns) - 1):
        # takes the first pattern
        first_pattern = list_of_selected_tonal_patterns[index]
        # and the next pattern
        second_pattern = list_of_selected_tonal_patterns[index + 1]
        # to be bridged
        bridged_pattern = bridge_pattern(first_pattern, second_pattern, bridge_lengths[index])
        # add the bridged pattern in to the exising verse
        verse_in_list.extend(bridged_pattern)

    verse_to_return = match_rhythmic_with_tonals(rhy_pattern, verse_in_list)

'''
pairs the rhythimc pattern with the tonal patterns

Parameters:
    rhythmic_pattern: The rhythimc pattern object to get the rhythimc patterns from
    verse_note_list: a list of notes that have been converted to match the length of the rhythmic pattern

Return:
    a list of Note_Patterns that has the length of each note / chord along with the note itself
'''
def match_rhythmic_with_tonals(rhythmic_pattern, verse_note_list):
    # the patterns to match
    pattern = rhythmic_pattern.pattern
    # an empty placeholder 
    to_return = []

    # loop through the given rthythmic pattern, create a note pattern object, and append ot to the list to be returned
    for index in range(len(pattern)):
        to_return.append(Note_Pattern(pattern[index], verse_note_list[index]))

    return to_return


'''
Gets a random bridge length to return

Parameters:
    total_length: the total length of all the bridge buffers

Return:
    a list of each size of the bridge length
'''
def _get_random_bridge_length(total_length, number_of_bridges):
    length_to_return = []

    # initially, fill each length to return with 3
    for _ in range(number_of_bridges):
        length_to_return.append(3)

    remaining_length = total_length - (3 * number_of_bridges)

    while(remaining_length > 0):
        random_selected_index = _get_random_number(number_of_bridges-1)
        length_to_return[random_selected_index] += 1
        remaining_length -= 1
    
    return length_to_return