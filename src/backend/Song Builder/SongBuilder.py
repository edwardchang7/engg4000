

import random as rand
from ast import pattern
from datetime import datetime as dt

from src.backend.cluster import Cluster

'''
Takes in a genre and returns a song template for the given genre

Parameters:
    genre: the genre to return the song template

Return:
    the song template based on the given genre
'''
def get_song_template(genre):
    return ['A','A','B','A']


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
    pattern_1 = _get_rhythimc_patterns(song_name, length_1)
    pattern_2 = _get_rhythimc_patterns(song_name, length_2)

    # only used for comparison to ensure the 2 patterns don't match
    # why hash? cuz its faster
    hashed_pattern_1 = hash(pattern_1)
    hashed_pattern_2 = hash(pattern_2)

    # randomly generate another pattern as long as hashed_pattern_1 matches hashed_pattern_2
    while(hashed_pattern_1 == hashed_pattern_2):
        pattern_2 = _get_rhythimc_patterns(song_name, length_2)

    # return the combination of both patterns
    return pattern_1.extend(pattern_2)

'''
Selects a random song name from the list of songs within the database

Return:
    A list of song names 
'''   
def _get_random_song_name():
    song_names = _get_db_song_names()

    # sets a random seed
    rand.seed(dt.now())

    selected_index = rand.randint(0, len(song_names))

    return song_names[selected_index]


'''
Randomly selects a pattern style

Return:
    a random selected pattern style that has a length of 8 
'''
def _get_random_pattern_style():

    # set a random seed
    rand.seed(dt.now())

    # Each of this are the possible combinations of bars
    pattern_style = [(4,4), (3,5), (5,3)]

    # randomly selects a pattern style and return it
    selected_index = rand.randint(0, len(pattern_style) - 1)

    return pattern_style[selected_index]

'''
Gets a list of Rhythmic Pattern objects from the db within the given collection that matches the pattern length

Parameters:
    song_name : the song name to search for the patterns (the name of the collection)
    pattern_length : the length for the patterns to match with

Return:
    a list of Rhythmic Pattern objects that matches the given pattern length within the given collection name
'''
def _get_rhythimc_patterns(song_name, pattern_length):

    # making initial db connection again
    cluster = Cluster("elliot", song_name, False)

    return cluster.query_rhythmic_patterns(cluster, song_name, pattern_length)

'''
Gets a random pattern from the list of patterns

Parameters:
    patterns: a list of patterns within a given song name that matches a specified length

Return:
    a random pattern from within the list of patterns
'''
def _get_random_pattern(patterns):

    # set a random seed
    rand.seed(dt.now())

    selected_index = rand.randint(0, len(patterns) - 1)

    # returns a random pattern within the given list of patterns
    return patterns[selected_index]


'''
Gets a list of song names that exist within the database

Return:
    a list of all the song names within the database 
'''
def _get_db_song_names():
    database = None # make db connection

    song_names = None # Retreive all song names from within the database

    # return a list of all collection names
    return None
