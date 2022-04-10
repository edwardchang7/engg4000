import random as rand
import re
import time
import traceback
from datetime import datetime as dt
from functools import reduce
from itertools import chain
from typing import Tuple
from src.backend.cluster import Cluster
from src.backend.collections.note_pattern import NotePattern
from src.backend.collections.rhythmic_pattern import RhythmicPattern
from src.backend.collections.tonal_pattern import TonalPattern
from src.backend.LoopError import LoopError
from src.backend.music_tools import (M3, P5, change_octave, half_step, m3,
                                     whole_step)
from src.backend.scales import get_scale





def get_song_template():
    '''
    Takes in a genre and returns a song template for the given genre

    Parameters:
        genre: the genre to return the song template

    Return:
        the song template based on the given genre
    '''
    return ['A', 'A', 'B', 'A']




def build_rhythmic_pattern(key:str) -> RhythmicPattern:
    '''
    Gets a key and returns a combination of rhythmic patterns

    Parameters:
        key : the key to return the patterns in

    Returns:
        a combination of patterns that matches the selected style
    '''

    # gets a random song name from the list of songs that exist within the database
    song_name = _get_random_song_name()

    # selected_style will be one of the pattern_styles above
    selected_style = _get_random_pattern_style()

    # fetch the patterns from the db based on the selected style
    length_1 = selected_style[0]
    length_2 = selected_style[1]

    # get the list of rhythmic pattern objects for the given song that matches the given length
    pattern_1 = _get_rhythmic_pattern(song_name, length_1)
    pattern_2 = _get_rhythmic_pattern(song_name, length_2)

    # to not get stuck in an infinite loop
    counter = 0

    # if pattern_1 is empty (meaning the given song name does not have matching pattern lengths)
    while(not pattern_1 or not pattern_2):
        song_name = _get_random_song_name()
        pattern_1 = _get_rhythmic_pattern(song_name, length_1)
        pattern_2 = _get_rhythmic_pattern(song_name, length_2)

        counter += 1

        if counter > 20:
            raise LoopError("Stuck in getting rhythmic patterns")

    # randomly generate another pattern as long as pattern_1 == pattern_2
    while(pattern_1 is pattern_2):
        pattern_2 = _get_rhythmic_pattern(song_name, length_2)

    # combined both patterns into 1
    combined_pattern = list(chain(pattern_1.pattern, pattern_2.pattern))

    # to create a rhythmic_pattern_object
    combined_rhythmic_pattern_object = RhythmicPattern(
        combined_pattern, 0, False)
        
    # and return the rhythmic_pattern_object
    return combined_rhythmic_pattern_object



def _get_random_song_name(get_from_tonal_patterns:bool=False) -> str:
    '''
    Selects a random song name from the list of songs within the database

    Parameters:
        get_from_tonal_patterns: if this is true, get the song names from "thomas" db instead

    Return:
        A list of song names 
    '''
    # gets all the songs from the database
    song_names = _get_db_song_names(get_from_tonal_patterns)

    if not get_from_tonal_patterns:
        song_names.remove("Take_Me_To_Church")
        song_names.remove("The_Entertainer")

    # generate a random index
    selected_index = _get_random_number(len(song_names) - 1)
    # return the song name at the random index
    return song_names[selected_index]



def _get_random_pattern_style() -> Tuple:
    '''
    Randomly selects a pattern style

    Return:
        a random selected pattern style that has a length of 8 
    '''
    # Each of this are the possible combinations of bars
    pattern_style = [(4, 4), (3, 5), (5, 3)]

    # randomly selects a pattern style and return it
    selected_index = _get_random_number(len(pattern_style) - 1) 

    return pattern_style[selected_index]



def _get_rhythmic_pattern(song_name:str, pattern_length:int) -> RhythmicPattern:
    '''
    Gets a list of Rhythmic Pattern objects from the db within the given collection that matches the pattern length

    Parameters:
        song_name : the song name to search for the patterns (the name of the collection)
        pattern_length : the length for the patterns to match with

    Return:
        a Rhythmic Pattern objects that matches the given pattern length within the given collection name
    '''
    # DB Settings
    db_name = "elliot"
    is_admin = False

    # used to ensure that its not stuck in the loop
    counter = 0
    reset_song = False

    # making connection to the DB
    db = _make_db_connection(db_name, is_admin, song_name)

    # gets a list of rhythmic_patterns within the given song_name that matches the pattern_length
    list_of_matching_length_songs = db.query_rhythmic_patterns(db, song_name, pattern_length)

    # if there is a matching pattern length within the given song name, then return it
    if  len(list_of_matching_length_songs) > 1 :
        # the length of all the matching song lengths
        matching_songs_length = len(list_of_matching_length_songs)
        # randomly generate an index
        selected_index = _get_random_number(matching_songs_length - 1) if matching_songs_length > 1 else 0
        # take a randomly selected pattern
        pattern_to_return = list_of_matching_length_songs[selected_index]
        # while the selected pattern is not V1, and there are other options, regenerate get a new pattern from the same song
        while not pattern_to_return.is_v1 and matching_songs_length > 1:
            selected_index = _get_random_number(matching_songs_length - 1)
            pattern_to_return = list_of_matching_length_songs[selected_index]
            counter += 1
            # if it has been looping for more than 10 times, break
            if counter >= 20 and not reset_song:
                counter = 0
                new_song_name = _get_random_song_name()
                list_of_matching_length_songs = db.query_rhythmic_patterns(db, new_song_name, pattern_length)
                if not list_of_matching_length_songs:
                    list_of_matching_length_songs = db.query_rhythmic_patterns(db, new_song_name, pattern_length)
                reset_song = True

            # if we picked another song and it still has no v1
            elif reset_song and counter >= 10:
                raise LoopError("Error in loop for getting a rhythmic pattern")

        return list_of_matching_length_songs[selected_index]

    # else return nothing
    else:
        return None



def _get_db_song_names(get_from_tonal_patterns:bool = False) -> list:
    '''
    Gets a list of song names that exist within the database

    Parameters: 
        get_from_tonal_patterns: if this is set to true, then get all song names from "thomas" db instead

    Return:
        a list of all the song names within the database 
    '''
    is_admin = False
    # use elliot as the db name if we're only getting rhythmic patterns, else get from Thomas
    db_name = "elliot" if not get_from_tonal_patterns else "thomas"

    # making connection to the DB
    db = _make_db_connection(db_name, is_admin)

    # get the list of song names
    song_names = db.get_collection_names(db)

    # return a list of all collection names
    return song_names



def _make_db_connection(database_name:str, is_admin:bool, collection_name:bool = None) -> Cluster:
    '''
    Make initial DB connection 

    Parameters:
        database_name : the database name to connect to
        is_admin : a boolean value to specify the admin status
        colleciton_name : the collection name to return (None will return all collection names)

    Return:
        a cluster instance
    '''
    # the cluster instance to be returned
    database = Cluster(database_name, collection_name,is_admin) if collection_name else Cluster(database_name, "", is_admin)

    return database



def convert_tonal_pattern(key:str, tonal_pattern:TonalPattern) -> list:
    '''
    Converts each pattern given to notes

    Parameters:
        key[note, modifer]: the starting note to step up or step down from
        tonal_pattern: the tonal pattern object that has the attribute of steps required

    Return:
        a list of notes that matches the pattern
    '''
    # gets the pattern from the given tonal pattern
    pattern = tonal_pattern.pattern

    # the convereted tonal pattern to notes
    to_return = []

    # sets the current note
    current_note = key[0] if len(key) == 2 else key[0] + key[1]

    # append the current note to be returned
    to_return.append(current_note)

    pattern = chain.from_iterable(pattern)

    # for each "group" of tonal patterns, converted them into notes, using the key as the first note
    for step in pattern:
        new_note = _get_note(step, current_note)
        # update the current note
        current_note = new_note

        # add the current note to the list
        to_return.append(current_note)

    return to_return


def _get_note(step:str, note:str) -> str:
    '''
    Gets the next note based on the step and the given note

    Parameters:
        step : the step to take from teh given note
        note : the note to modify

    Return:
        the next note based on the given step
    '''
    if 'h' in step:
            new_note = half_step(
                note, False) if '-' in step else half_step(note, True)
    elif 'w' in step:
        new_note = whole_step(
            note, False) if '-' in step else whole_step(note, True)
    elif 'm3' in step:
        new_note = m3(
            note, False) if '-' in step else m3(note, True)
    elif 'M3' in step:
        new_note = M3(
            note, False) if '-' in step else M3(note, True)
    elif 'P5' in step:
        new_note = P5(
            note, False) if '-' in step else P5(note, True)
    elif 'o' in step:
        new_note = change_octave(
            note, False) if '-' in step else change_octave(note, True)
    elif '0' in step:
        new_note = note

    return new_note



def _strip_modifiers_from_scale(scale:list) -> list:
    '''
    Removes all note modifiers (the pitch) from each note in the scale

    Parameters:
        scale: the scale to strip all modifiers from

    Return:
        the same scale but with just the base notes (no modifiers)
    '''

    # strip all modifers from each note
    scale_to_return = list(map(_strip_note_modifiers, scale))

    return scale_to_return



def bridge_pattern(key:str, tonal_pattern_1:list, tonal_pattern_2:list, num_beats:int) -> list:
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
    # get the initial scale for this given key
    scale = _get_random_scale_type(key)
    # now strip all the modifiers from the notes in the scale
    scale = _strip_modifiers_from_scale(scale)
    # a placeholder to keep the bridged_patterns
    bridged_patterns = []
    # if either tonal patterns are None or number of beats are None (should not happen) then return None
    if not tonal_pattern_1 or not tonal_pattern_2 or not num_beats:
        return None

    # a variable to hold the notes
    current_note = tonal_pattern_1[-1]

    for _ in range(num_beats):
        # get the window within the scale given the current note
        window = _get_window(current_note, scale)

        # randomly generate an index between 0 and 3 (4 = window size)
        selected_index = _get_random_number(3)

        # the selected note will be in this variable
        selected_note = window[selected_index]

        # update the current note
        current_note = selected_note

        # add the note to the bridge
        bridged_patterns.append(current_note)

    # out of the loop, append the 2nd part of the tonal_pattern
    bridged_patterns.extend(tonal_pattern_2)

    # this bridged_patterns only hold the notes of the bridge, and the 2nd tonal pattern. 
    # the first part of the tonal pattern still has to be added in
    return bridged_patterns


def _strip_note_modifiers(note:str) -> str:
    '''
    Removes all modifiers from the notes

    Parameters:
        note: the note to remove the modifiers from

    Return:
        the note but without modifiers
    '''
    # if the note is None, reutrn none
    if not note:
        return None

    # only add to character to be returned if its a valid character or if its "#"
    to_return = [c for c in note if c.isalpha() or c == "#"]

    # now stick everything back together since the line above turns each char into an element in a list
    to_return = str(reduce(lambda a,b: a + b, to_return))

    return to_return



def _get_window(note:str, scale:list) -> list:
    '''
    Given the note and the scale, generates a window of notes
    of length 4, (+2 and -2 index from the given note within the scale)

    Parameters:
        note: The note to go up by 2 and down by 2 in the scale
        scale: the scale that the given note exist within

    Return:
        a list of 4 notes (+2 from note and -2 from note)
    '''
    # empty placeholder to be returned
    window = []

    note = _strip_note_modifiers(note)

    # only used if the given note has reached the highest octave
    previous_note = None
    keep_going_up = True

    # To prevent it from being stuck in an infinite loop
    counter = 0

    # a temporary placeholder for the current note to get the window of
    temp = note

    # while the upper note is still not in the scale
    while temp not in scale:
        
        # temp = halfstep upwards if keep_going_up is true
        temp = half_step(
            temp, True) if keep_going_up else half_step(temp, False)

        # remove the modifiers from the new note
        temp = _strip_note_modifiers(temp)

        # if the new note is None, or that it made a full loop (with each note not being in the scale),
        # then try again but this time with the upperCased version of the note
        if not temp or temp == previous_note or temp == note:
            keep_going_up = False
            temp = note.upper() if note.islower() else note.lower()

        # update the previous note (so that we know if it reached the highest octave or lowest octave)
        previous_note = temp if temp else note

        # if this loop has been looping for over 50 times assume theres an error and just break from this loop
        if counter >= 50:
            raise LoopError("Error in getting window loop")

        counter += 1

    # the reversed scale
    reversed_scale = list(reversed(scale))

    scale_index_of_note = scale.index(temp) + 1
    reversed_index_of_note = reversed_scale.index(temp) + 1

    for _ in range(2):
        scale_index = scale_index_of_note % len(scale)
        reversed_index = reversed_index_of_note % len(reversed_scale)
        window.append(scale[scale_index])
        window.append(reversed_scale[reversed_index])
        scale_index_of_note += 1
        reversed_index_of_note+= 1

    return window



def _get_random_scale_type(key:str, test:bool =False) -> str:
    '''
    Gets a scale given the key with a random type

    Parameters
        key: The key to generate the scale in
        test: only set to True for testing

    Return
        The generated scale in the given key
    '''
    # split the root and the scale type
    root = key[0] if len(key) == 2 else key[0] + key[1]
    scale_type = key[1] if len(key) == 2 else key[2]

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



def _get_random_number(limit:int, start:int =0) -> int:
    '''
    Returns a random number between the range of [0,limit]

    Parameters:
        limit: the maximum value that can be randomly generated 
        start: the starting value

    Return:
        a randomly generated value within the range of [0,limit]
    '''
    # set the seed
    dt.now().timestamp() 

    # a quick nap of about 3ms so that it doesnt always use the same seed if this function is called multiple times consecutively
    time.sleep(0.003)

    # return the generated number only if the given limit is greater than the start
    value = rand.randint(start, limit) if limit != 0 and limit > start else 0

    return value



def build_verse(key:str, rhythmic_pattern: RhythmicPattern) -> list:
    '''
    builds the verse based on the given key and rhytmic_pattern

    Parameters:
        key: the key to generate the verse in
        rhythmic_pattern: the rhythmic_pattern to match the notes with

    Return
        a list of NotePattern objects that holds the note and the beats
'''
    # the list to return
    verse_to_return = []
    # temporary placeholder for holding all the combined patterns with the bridge patterns
    verse_in_list = []

    # number of available patterns left to get
    num_available_patterns = 4

    # bridge pattern buffer size
    bridge_pattern_buffer_size = 0

    # the remaining number of beats to generate 
    num_beats_left = rhythmic_pattern.beats

    # select a tonal pattern and add it to the list_of_selected_tonal_patterns
    list_of_selected_tonal_patterns = []

    # randomly select a tonal pattern that has num_notes <= the num_beats_left
    selected_tonal_pattern = get_tonal_pattern(num_beats_left)
    # add it to the list of selected tonal patterns
    list_of_selected_tonal_patterns.append(selected_tonal_pattern)

    # update the num_beats_left
    num_beats_left -= selected_tonal_pattern.num_of_notes

    # handle the case where there is only one pattern + 1->3 extra notes
    if num_beats_left < 3:
        bridge_pattern_buffer_size += num_beats_left
    else:
        # while the number of beats left is > 4 (cuz aparently there arent any patterns <= 4)
        while num_beats_left > 4 and num_available_patterns > 0:

            # get a tonal pattern and add it to the list_of_selected_tonal_patterns
            selected_tonal_pattern = get_tonal_pattern(num_beats_left)

            # append the selected pattern to the list of existing tonal patterns
            list_of_selected_tonal_patterns.append(selected_tonal_pattern)

            # decrease the count of available patterns and the remaining number of beats required
            num_beats_left -= selected_tonal_pattern.num_of_notes
            num_available_patterns -= 1

            # each tonal pattern added to the list should have 3 beats (if possible) allocated to bridge it to the others
            if num_beats_left <= 6 and len(list_of_selected_tonal_patterns) > 1:
                break
            else:
                # add 3 to the min size of total bridge length
                bridge_pattern_buffer_size += 3

        # add the remaining beats to the total length of bridge to generate
        bridge_pattern_buffer_size += num_beats_left

    # if the length of the selected tonal patterns is 1 (if there is only 1 tonal pattern and not enough num notes left)
    if len(list_of_selected_tonal_patterns) == 1:
        # convert the given tonal pattern into actual notes
        converted_tonal_pattern = convert_tonal_pattern(key, list_of_selected_tonal_patterns[0])
        # create a single bridge, where its [tonal_pattern] + "bridge" + [tonic_note]
        # the "bridge" length is the bridge_buffer_size

        root = key[0] if len(key) == 2 else key[0] + key[1]

        single_bridge = bridge_pattern(key, converted_tonal_pattern, [root], bridge_pattern_buffer_size)
        # append the single bridge to the set of converted tonal patterns
        converted_tonal_pattern.extend(single_bridge)
        # return the converted tonal_pattern

        verse_to_return = match_rhythmic_with_tonals(rhythmic_pattern, converted_tonal_pattern)
        return verse_to_return

    # randomly allocate bridge lengths
    bridge_lengths = _get_random_bridge_length(bridge_pattern_buffer_size, len(list_of_selected_tonal_patterns) - 1)

    # loops through all the existing tonal patterns
    for index in range(len(list_of_selected_tonal_patterns)-1):
        # get the first tonal pattern object
        first_tonal_pattern_obj = list_of_selected_tonal_patterns[index]
        # and the second tonal pattern object
        second_tonal__pattern_obj = list_of_selected_tonal_patterns[index + 1]

        # convert the pattern to notes
        first_converted_pattern = convert_tonal_pattern(key, first_tonal_pattern_obj)
        second_converted_pattern = convert_tonal_pattern(key, second_tonal__pattern_obj)

        # add only the pattern from the first converted tonal pattern
        verse_in_list.extend(first_converted_pattern)
        # and brige them together
        bridged_pattern = bridge_pattern(key, first_converted_pattern, second_converted_pattern, bridge_lengths[index])
        # add the bridged pattern in to the exising verse
        # bridged_pattern here is the "bridge_notes" + second_converted_pattern
        verse_in_list.extend(bridged_pattern)

    # pair each rhythmic pattern with the generated notes
    verse_to_return = match_rhythmic_with_tonals(rhythmic_pattern, verse_in_list)

    return verse_to_return


def build_song_bridge(reference_verse: list, key: str, modulate: bool):
    '''
    Creates the bridge for the song given the verse and certain presets

    Parameters:
        reference_verse: the verse to use as reference for bridge building
        key: key of the song

    Return:
        The modulated verse, and the modulated key
    '''

    bridge = []

    if modulate:
        bridge, key = modulate_verse(reference_verse, ["m3"], True, key)
    else:
        bridge = reference_verse

    bridge = add_random_cadence(bridge, key)

    return bridge


def add_random_cadence(reference: list, key: str):
    '''
    Randomly modifies certain sections of verse/bridge to add cadences

    Parameters:
        reference: the verse/bridge to modify
        key: key of the song

    Return:
        The verse/bridge with changes to certain notes
    '''

    modified = []
    deceptive = False
    perf_plag = False
    octave = ""

    reference_scale = get_scale(key[:-1], key[-1])
    reference_scale = [note.upper() for note in reference_scale]

    for note_pattern in reference:

        new_note = note_pattern.note
        new_length = note_pattern.length
        try:
            degree = reference_scale.index(_strip_note_modifiers(new_note).upper())
        except ValueError:
            degree = -1

        rand = _get_random_number(1)

        if deceptive:
            stripped = _strip_note_modifiers(new_note)
            octave = new_note[len(stripped):]
            new_note = reference_scale[5]

            if len(octave) != 0:
                if octave.find("'") != -1:
                    new_note = new_note.lower() + octave
                elif octave.find(",") != -1:
                    new_note = new_note + octave

            deceptive = False

        if rand == 1:

            if degree == 4:

                deceptive = True

            if degree == 0:

                perf_plag = True


        if perf_plag:
            good_for_cadence = False
            index = -1
            rand = _get_random_number(1)

            new_note_degree = 4

            if rand == 1:

                new_note_degree = 3

            for i in range(len(modified), 0, -1):
                old_note_pattern = modified[i - 1]
                if old_note_pattern.note != "z":
                    good_for_cadence = True
                    index = i - 1
                    break

            if good_for_cadence:
                old_note_pattern = modified.pop(index)
                stripped = _strip_note_modifiers(old_note_pattern.note)
                octave = old_note_pattern.note[len(stripped):]

                replacement_note = reference_scale[new_note_degree]

                if len(octave) != 0:
                    if octave.find("'") != -1:
                        replacement_note = replacement_note.lower() + octave
                    elif octave.find(",") != -1:
                        replacement_note = replacement_note + octave

                replacement = NotePattern(replacement_note, old_note_pattern.length)
                modified.insert(index, replacement)

            perf_plag = False


        new_pattern = NotePattern(new_note, new_length)
        modified.append(new_pattern)

    return modified


def modulate_verse(reference_verse: list, interval: list, up_frequency: bool, key: str):
    '''
    Modulates a given verse depending on the input interval

    Parameters:
        reference_verse: the verse to modulate
        interval: list of steps indicating the total interval
        up_frequency: indicates whether interval is up or down
        key: key of the song

    Return:
        The modulated verse, and the modulated key
    '''

    interval_length = 0
    key_done = False
    key_type = key[-1]
    modulated = []

    for step in interval:
        if step == "o":
            interval_length += 12
        elif step == "P5":
            interval_length += 7
        elif step == "M3":
            interval_length += 4
        elif step == "m3":
            interval_length += 3
        elif step == "w":
            interval_length += 2
        elif step == "h":
            interval_length += 1

    for note_pattern in reference_verse:
        if not key_done:
            key = half_step(key[:-1], up_frequency)
        new_note = half_step(note_pattern.note, up_frequency)
        for i in range(interval_length - 1):
            if not key_done:
                key = half_step(key, up_frequency)
            new_note = half_step(new_note, up_frequency)

        if not key_done:
            key_done = True
        new_note_pattern = NotePattern(new_note, note_pattern.length)
        modulated.append(new_note_pattern)

    return modulated, key + key_type


def get_tonal_pattern(num_beats_left:int) -> TonalPattern:
    '''
    Gets a random tonal pattern

    Parameters:
        num_beats_left: the number of beats to get 

    Return:
        a tonal pattern object
    '''
    # db settings
    db_name = "thomas"
    is_admin = False
    # get a random song name from "thomas" db
    song_name = _get_random_song_name(get_from_tonal_patterns=True)
    # database connection
    database = _make_db_connection(db_name, is_admin, song_name)
    # if the database connection failed, return None
    if not database:
        return None

    # to ensure its not stuck in an infinite while loop
    counter = 0

    # get all the tonal patterns of the given song name
    tonal_patterns_of_given_song = database.query_tonal_patterns(database, song_name, num_beats_left-3)

    # for some reason the tonal_patterns_of_given_song is sometimes empty. Why? Not sure lmao. so I just added a check
    # and to make sure this does not run more than 30 times
    while not tonal_patterns_of_given_song and num_beats_left > 4 and counter < 30:
        counter += 1
        # gets a random song name from Thomas's db instead 
        song_name = _get_random_song_name(get_from_tonal_patterns=True)
        # database connection
        database = _make_db_connection(db_name, is_admin, song_name)
        # if the database connection failed, return None
        if not database:
            return None
        # gets the tonal pattern of the given song name if it was empty previously
        tonal_patterns_of_given_song = database.query_tonal_patterns(database, song_name, num_beats_left-3)

        if counter >= 30 and not tonal_patterns_of_given_song:
            raise LoopError("Error in loop of getting tonal pattern")

    # gets a random number to select a random tonal pattern
    selected_index = _get_random_number(len(tonal_patterns_of_given_song) - 1) if len(tonal_patterns_of_given_song) > 1 else 0

    # the randomly selected tonal pattern
    return tonal_patterns_of_given_song[selected_index]


def _make_note_pattern(note:str, beat:str) -> NotePattern:
    '''
Creates a NotePattern Object with the given note and beat

Parameters:
    note: the note of the NotePattern
    beat: the beat of the note

Returns:
    a Note pattern object
'''
    return NotePattern(note, beat)



def match_rhythmic_with_tonals(rhythmic_pattern: RhythmicPattern, verse_note_list:list) -> list:
    '''
    pairs the rhythimc pattern with the tonal patterns

    Parameters:
        rhythmic_pattern: The rhythimc pattern object to get the rhythimc patterns from
        verse_note_list: a list of notes that have been converted to match the length of the rhythmic pattern

    Return:
        a list of Note_Patterns that has the length of each note / chord along with the note itself
    '''
    # the patterns to match
    pattern = rhythmic_pattern.pattern
    # an empty placeholder
    to_return = []

    # this index keeps track of the notes in the verse_note_list
    index = 0

    # will be true of the given note is a chord
    is_chord = False

    # loop through the given rthythmic pattern, create a note pattern object, and append ot to the list to be returned
    for bar in pattern:
        for notes in bar:
            # if the notes is a rest note, create a note pattern with "z" as the note and the beats
            if len(notes) == 3 and '(' in notes and ')' in notes:
                to_return.append(_make_note_pattern("z", notes[1]))
            # else if its not a rest note, then do this
            else:
                # break up the notes into groups of beats (might be 1, might be more)
                beam_beats = list(filter(None, re.split("(\W)", notes)))
                # for each beat in the "group" of beats
                for beats in beam_beats:
                    # if the given character at that time is "[" we know its the start of a chord
                    if beats == "[":
                        is_chord = True
                    
                    # if the flag is_chord is up, it means at this point, it has the "content" of the chord
                    # EX: content of the chord => chord = '[111]' content of chord = 111
                    elif is_chord:
                        # if its a chord, create a Note_pattern and add it to the list, and put the "[" and "]" back
                        # to signify that its a chord
                        to_return.append(_make_note_pattern(verse_note_list[index], "[" + str(beats) + "]"))
                        # increase the index to get the next note in the verse_note_list
                        index += 1
                        # since we already used the content of the chord, reset the flag
                        is_chord = False
                    # if its not a chord, and jsut a set of beats like `1111` or `1` then
                    elif beats.isdigit():
                        # go through each of these beats, and append a note to it through the verse_note_list
                        for individual_beat in beats:
                            to_return.append(_make_note_pattern(verse_note_list[index], individual_beat))
                            index += 1
    return to_return


def _get_random_bridge_length(total_length:int, number_of_bridges:int) -> list:
    '''
    Gets a random bridge length to return

    Parameters:
        total_length: the total length of all the bridge buffers

    Return:
        a list of each size of the bridge length
    '''
    # the lengths of each bridge to return
    length_to_return = []
    # the minimum length is 3
    min_length = 3
    # if the total length is less than the minimum length, update the minimum length
    if total_length < 3:
        min_length = total_length

    # fill each bridge to be the min length by default
    for _ in range(number_of_bridges):
        length_to_return.append(min_length)

    # if there are still beats left to be filled
    remaining_length = total_length - (min_length * number_of_bridges)

    # randomly add them to each "bridge" length
    while(remaining_length > 0 and number_of_bridges > 0):
        random_selected_index = _get_random_number(number_of_bridges-1)
        length_to_return[random_selected_index] += 1
        remaining_length -= 1

    return length_to_return


def build_v2(tonic:str, input_verse:list) -> list:
    '''
Builds a complimenting V2 pattern that can be combined with V1

Parameters:
    verse: a list of Note_Patterns

Return:
    v2_verse: a list of PatternNotes
'''
    v2_notes = []
    beat_counter = 0

    # keep a running counter of beats, every 4 beats append the next note to a new list
    for note in input_verse:
        # if checking first note of a bar then append it to the v2 note list
        if beat_counter == 0: v2_notes.append(note.note)

        beat_counter += int(note.length) if "[" not in note.length else int(note.length[1])
        # WILL THIS ACCOUNT FOR 16th notes signified by 0
        if beat_counter == 8: beat_counter = 0
    
    v2_note_patterns=[]

    tonic = tonic[0] if len(tonic) == 2 else tonic[0] + tonic[1]

    for note in v2_notes:
        note_to_append = note if note != "z" else tonic
        v2_note_patterns.append(_make_note_pattern(note_to_append, 8))

    return v2_note_patterns
