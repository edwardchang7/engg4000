
import random as rand
from datetime import datetime as dt

from src.backend.cluster import Cluster
from src.backend.music_tools import half_step ,whole_step ,M3 ,m3 ,P5 ,change_octave
from src.backend.scales import get_scale

'''
Takes in a genre and returns a song template for the given genre

Parameters:
    genre: the genre to return the song template

Return:
    the song template based on the given genre
'''
def get_song_template(genre):
    return ['A' ,'A' ,'B' ,'A']


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
    whil e(not pattern_1 or not pattern_2):
        song_name = _get_random_song_name()
        pattern_1 = _get_rhythmic_patterns(song_name, length_1)
        pattern_2 = _get_rhythmic_patterns(song_name, length_2)

    # randomly generate another pattern as long as pattern_1 == pattern_2
    whil e(pattern_1 is pattern_2):
        pattern_2 = _get_rhythmic_patterns(song_name, length_2)

    return pattern_1, pattern_2

'''
Selects a random song name from the list of songs within the database

Return:
    A list of song names 
'''
def _get_random_song_name():
    song_names = _get_db_song_names()

    # sets a random seed
    rand.seed(dt.now().timestamp())

    selected_index = rand.randint(0, len(song_names) -1)

    return song_names[selected_index]


'''
Randomly selects a pattern style

Return:
    a random selected pattern style that has a length of 8 
'''


def _get_random_pattern_style():
    # set a random seed
    rand.seed(dt.now().timestamp())

    # Each of this are the possible combinations of bars
    pattern_style = [(4, 4), (3, 5), (5, 3)]

    # randomly selects a pattern style and return it
    if len(pattern_style) > 1:
        selected_index = rand.randint(0, len(pattern_style) - 1)
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

    list_of_matching_length_songs = db.query_rhythmic_patterns(db, song_name, pattern_length)

    rand.seed(dt.now().timestamp())

    # if there is a matching pattern length within the given song name, then return it
    if (list_of_matching_length_songs):
        if (len(list_of_matching_length_songs) > 1):
            selected_index = rand.randint(0, len(list_of_matching_length_songs) - 1)
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
                new_note = half_step(current_note, False) if '-' in step else half_step(current_note, True)

            elif 'w' in step:
                new_note = whole_step(current_note, False) if '-' in step else whole_step(current_note, True)

            elif 'm3' in step:
                new_note = m3(current_note, False) if '-' in step else m3(current_note, True)

            elif 'M3' in step:
                new_note = M3(current_note, False) if '-' in step else M3(current_note, True)

            elif 'P5' in step:
                new_note = P5(current_note, False) if '-' in step else P5(current_note, True)

            elif 'o' in step:
                new_note = change_octave(current_note, False) if '-' in step else change_octave(current_note, True)

            elif '0' in step:
                new_note = current_note

        # update the current note
        current_note = new_note

        # add the current note to the list
        to_return.append(current_note)

    return to_return


def bridge_pattern(key, start_note, end_note, num_beats):
    # get the initial scale for this given key
    scale = _get_random_pattern_style(key)

    # a variable to hold the current note
    current_note = start_note

    # create an empty list to hold the value to return
    bridged_patterns = []

    while (num_beats > 0):
        num_beats -= 1

    return bridged_patterns


def _get_window(note, scale):
    index_of_note = scale.index(note)


'''
Gets a scale given the key with a random type

Parameters
    key: The key to generate the scale in

Return
    The generated scale in the given key
'''


def _get_random_scale_type(key):
    # split the root and the scale type
    root = key[0]
    scale_type = key[1]

    # set the seet for random class
    rand.seed(dt.now().timestamp())

    # the differnt types of scale types
    minor_scale_types = ['m', 'pm']
    major_scale_types = ['M', 'pm']

    # randomly generate a number, if its even then use minor / major scales,
    # else if its odd then use either pentatonic minor / major
    selected_index = 0 if (rand.randint(0, 100) % 2 == 0) else 1

    # This will hold the scale type
    selected_scale_type = minor_scale_types[selected_index] if 'm' in scale_type else major_scale_types[selected_index]

    # this will hold the generated scale
    generated_scale = get_scale(root, selected_scale_type)

    return generated_scale


def build_new_pattern(self, first_existing_pattern: list, second_existing_pattern: list,
                      desired_num_of_beats: int) -> list:
    num_of_beats_in_first_pattern = len(first_existing_pattern)
    num_of_beats_in_second_pattern = len(second_existing_pattern)

    num_of_beats_in_new_pattern = desired_num_of_beats - num_of_beats_in_first_pattern - num_of_beats_in_second_pattern

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