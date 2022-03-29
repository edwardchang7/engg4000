import random as rand
from datetime import datetime as dt

# REMOVE THIS BEFORE MERGING INTO MASTER
# ===========================================================
# only uncomment this if you are not using pycharm
import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parent2 = os.path.dirname(parentdir)
sys.path.insert(0, parent2)
# END OF IMPORTS FOR NON-PYCHARM USERS (mostly just for Elliot)
# ===========================================================
# REMOVE THIS BEFORE MERGING INTO MASTER

from src.backend.cluster import Cluster
from src.backend.music_tools import (M3, P5, change_octave, half_step, m3,
                                     whole_step)
from src.backend.scales import get_scale
from src.backend.collections.rhythmic_pattern import Rhythmic_Pattern
from src.backend.collections.tonal_pattern import TonalPattern


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
    if len(pattern_style) > 1:
        selected_index = _get_random_number(len(pattern_style) - 1)
    else:
        selected_index = 0

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
        if (len(list_of_matching_length_songs) > 1):
            selected_index = rand.randint(
                0, len(list_of_matching_length_songs) - 1)
        else:
            selected_index = 0

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
    database = None

    if (collection_name):
        database = Cluster(database_name, collection_name, is_admin)
    else:
        database = Cluster(database_name, "", is_admin)

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
def bridge_pattern(key, start_note, end_note, num_beats):
    # get the initial scale for this given key
    scale = _get_random_scale_type(key)

    # a variable to hold the current note
    current_note = start_note

    # create an empty list to hold the value to return
    bridged_patterns = []

    while (num_beats > 0):

        # get the window within the scale given the current note
        window = _get_window(current_note, scale)

        # randomly generate an index between 0 and 3 (4 = window size)
        selected_index = _get_random_number(3)

        # the selected note will be in this variable
        selected_note = window[selected_index]

        current_note = selected_note

        bridged_patterns.append(current_note)

        num_beats -= 1

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

Return:
    a randomly generated value within the range of [0,limit]
'''
def _get_random_number(limit):
    # set the seed
    rand.seed(dt.now().timestamp())

    # return the generated number
    value = rand.randint(0, limit)

    return value


def build_verse(rhy_pattern:Rhythmic_Pattern, ton_pattern:TonalPattern):
    r_pat = rhy_pattern.pattern
    t_pat = ton_pattern.pattern

    to_return = dict(zip(r_pat, t_pat))

    return to_return

# =============================================================================================
# Functions from another song_builder file
# _____________________________________________________________________________________________
def build_new_pattern(self, first_existing_pattern: list, second_existing_pattern: list,
                      desired_num_of_beats: int) -> list:
    num_of_beats_in_first_pattern = len(first_existing_pattern)
    num_of_beats_in_second_pattern = len(second_existing_pattern)

    num_of_beats_in_new_pattern = desired_num_of_beats - \
        num_of_beats_in_first_pattern - num_of_beats_in_second_pattern

    if num_of_beats_in_new_pattern < 0:
        return None
    elif num_of_beats_in_new_pattern == 0:
        return combine_patterns(first_existing_pattern, second_existing_pattern)
    else:
        pass
        # find common scale
        # return new pattern


def combine_patterns(self, first_pattern: list, second_pattern: list) -> list:
    return first_pattern + second_pattern
# =============================================================================================
# Functions from another song_builder file
# _____________________________________________________________________________________________