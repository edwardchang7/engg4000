"""
This file will be filled with the functions required to extract and save 
rhythmic patterns from an abc file

1. If polyphonic - seperate
2. Get meter and time signature
3. Translate notes in bars into numbers representing note lengths
4. Analyze numbers looking for patterns
5. Cross reference those sections with original music to get actual musical pattern
"""

import re
import warnings
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
from src.backend.collections.rhythmic_pattern import RhythmicPattern
from src.backend.collections.songcollection import SongCollection
from src.backend.models.rhythmic_pattern_model import RhythmicPatternModel

from abc_tools import get_header, get_melodic_and_rythmic, get_voicings

# surpress the warnings from format_bar function
warnings.simplefilter(action="ignore", category=FutureWarning)

v1_keys = []
v2_keys = []

v1_pattern = {}
v2_pattern = {}

v1_combination = []
v2_combination = []

song_list = []

meter = -1


def extract_rhythmic_patterns(file_path: str):
    global meter

    voicings = get_voicings(file_path)
    meter = get_header(file_path, 'M')

    # Gets the seperated list of v1 and v2
    v1, v2 = get_melodic_and_rythmic(file_path)

    '''
    1. Seperates each bar
    2. Remove unnecessary notation
    3. Replace all notes with the beat counts
    4. Combine all bars
    5. extract patterns
    '''
    encode_voicings(v1, v2)

# Function to isolate the notes in a single bar


def format_bar(bar: str):
    has_notes = re.search('[A-Ga-g]', bar) or 'z' in bar
    if not has_notes:
        bar = None
    else:
        bar = re.sub('%[0-9][0-9]?[0-9]?', "", bar)
        bar = re.sub('"[^"]*"', "", bar)
        bar = re.sub('![^"]*!', "", bar)
        bar = re.sub('[[A-Z]:[^"]*]', "", bar)
        bar = bar.replace("\n", "")
        bar = bar.replace("$", "")
        bar = bar.replace("{/f'}", "")
        bar = bar.replace(":", "")
        bar = bar.strip()

    return bar


def encode_voicings(v1, v2):
    # 1. isolate notes
    # split into sections
    # split sections into bars
    for v in v1:
        bars = v.split('|')
        for bar in bars:
            # Strips all unnecessary notation
            bar = format_bar(bar)

            if(bar):
                # At this point, each bar only has the notes and the pitch
                bar = encode_bar(bar)
                # Here the bar only has the beat count itself
                if(bar):
                    v1_combination.append(bar)

    for v in v2:
        bars = v.split('|')
        for bar in bars:
            # Strips all unnecessary notation
            bar = format_bar(bar)

            if(bar):
                # At this point, each bar only has the notes and the pitch
                bar = encode_bar(bar)
                # Here the bar only has the beat count itself
                if(bar):
                    v2_combination.append(bar)


'''
8 = whole note
6 = half note + .
4 = half note
3 = quater note + .
2 = quater note
1 = 8th note
0 = 16th note
'''


def encode_bar(bar):

    # replace '/' with 0 to show its a 16th note
    bar = bar.replace("/", "0")
    bar = bar.split()

    no_mod_bar = []
    all_beats_bar = []
    new_bar = []

    # for each note in the bar remove all modifiers (pitch)
    for note in bar:
        note = ''.join(c if c.isalpha() or c.isdigit() or c ==
                       '[' or c == ']' else '' for c in note)
        no_mod_bar.append(note)

    # go through the new bars. for each note of the new bar, check if there is a beat
    # if there is no numbers, put 1
    for note in no_mod_bar:
        # keeps track of whether given note or chord has a beat
        contains_beat = any(char.isdigit() for char in note)

        # create a new bar and put them in
        temp_note = note + "1" if not contains_beat else note
        all_beats_bar.append(temp_note)
            

    # replace the notes with the beats
    for note in all_beats_bar:
        beat = note[-1]

        # if the beat is placed at the start instead
        if not beat.isdigit(): beat = note[0]

        new_bar.append(_keep_beats_only(note, beat))

    # remove all non notes
    for note in new_bar:
        # if a number exist within the note, assume its valid, else, new_bar remove it
        if not any(char.isdigit() for char in note):
            new_bar.remove(note)

    if(new_bar):
        if(_check_valid_beats(new_bar)):
            return new_bar

    return None


'''
Replaces each note with the given beat (keeps square bracket to signify that its a chord)
'''


def _keep_beats_only(note, beat):

    exception_list = {'x'}
    new_note = ''

    # If this is a chord, keep the sqr brackets
    for c in note:
        if c == 'z':
            # moreve c
            new_note += '(' + beat + ')'
        elif c.isalpha() and c not in exception_list:
            # remove c
            new_note += beat
        elif c == '[' or c == ']':
            new_note += c

    return new_note


'''
checks if the given bar matches the meter
'''


def _check_valid_beats(bar):

    beat_count = 0

    for note_beat in bar:

        # If its a combination of chords
        if note_beat.count("[") >= 1:
            notes = note_beat.split("[")

            for note in notes:
                if note:
                    beat = note[0]
                    if beat == '0':
                        beat_count += 1/4
                    elif beat == '1':
                        beat_count += 1/2
                    elif beat == '2':
                        beat_count += 1
                    elif beat == '3':
                        beat_count += 1.5
                    elif beat == '4':
                        beat_count += 2
                    elif beat == '6':
                        beat_count += 3
                    elif beat == '8':
                        beat_count += 4

        else:
            for beat in note_beat:
                if beat.isdigit():
                    if beat == '0':
                        beat_count += 1/4
                    elif beat == '1':
                        beat_count += 1/2
                    elif beat == '2':
                        beat_count += 1
                    elif beat == '3':
                        beat_count += 1.5
                    elif beat == '4':
                        beat_count += 2
                    elif beat == '6':
                        beat_count += 3
                    elif beat == '8':
                        beat_count += 4

    return beat_count == int(meter[0])


def extract_pattern():
    v1_temp = []
    v2_temp = []

    # This loop extracts a bar with the min length of 3 and max length of 5 from v1
    for counter in range(3, 6):
        i = 0
        count = 0
        index = 0

        # This ensures that it only extract information from v1
        while(True):
            # if the combination length (count) is counter, it means the max length is reached
            if count == counter:
                # resets the combination length counter (count)
                count = 0
                # saves a 'set' of combined bars to v1_keys
                v1_keys.append(v1_temp)
                v1_temp = []
                # increases the index to know which bar to start from again
                index += 1
                i = index
            # if the combination length (count) != counter
            else:
                count += 1
                # if the index is the length of the combined bars, then decrease it by 1 else you would get IndexOutOfBounds
                if i >= len(v1_combination):
                    i -= 1

                if(i < 0):
                    break

                v1_temp.append(v1_combination[i])
                i += 1

            # If the index  == length, it means you reached the end of v1, so break from the while loop, and increase
            # the max line for the combination
            if index == len(v1_combination):
                break

    # This loop extracts a bar with the min length of 3 and max length of 5 from v1
    for counter in range(3, 6):
        i = 0
        count = 0
        index = 0
        while(True):
            # if the combination length (count) is counter, it means the max length is reached
            if count == counter:
                # resets the combination length counter (count)
                count = 0
                # saves a 'set' of combined bars to v2_keys
                v2_keys.append(v2_temp)
                v2_temp = []
                # increases the index to know which bar to start from again
                index += 1
                i = index
            # if the combination length (count) != counter
            else:
                if(v2_combination):
                    count += 1
                    # if the index is the length of the combined bars, then decrease it by 1 else you would get IndexOutOfBounds
                    if i >= len(v2_combination):
                        i -= 1
                    v2_temp.append(v2_combination[i])
                    i += 1

            # If the index  == length, it means you reached the end of v1, so break from the while loop, and increase
            # the max line for the combination
            if index == len(v2_combination):
                break

    for set_of_bars in v1_keys:
        if str(set_of_bars) in v1_pattern.keys():
            v1_pattern[str(set_of_bars)] += 1
        else:
            v1_pattern[str(set_of_bars)] = 1

    for set_of_bars in v2_keys:
        if str(set_of_bars) in v2_pattern.keys():
            v2_pattern[str(set_of_bars)] += 1
        else:
            v2_pattern[str(set_of_bars)] = 1

# CALL THIS FUNCTION TO EXTRACT EVERY FILW WITHIN THE DIR BELOW
def extract_all_files():

    global v1_pattern, v2_pattern, v1_keys, v2_keys, v1_combination, v2_combination

    # the main dir 
    str_dir = 'src/backend/mxl_to_abc/converted_compositions'

    count = 0

    # gets each file from the given directory
    directory = os.fsencode(str_dir)

    # for each file within the given directory, extract patterns from this
    for file in os.listdir(directory):

        # gets the filename of the given file
        filename = os.fsdecode(file)

        # checks if hte given file ends with the right extension
        if filename.endswith('.abc'):

            # concat the directory with the file name
            file_path = str_dir + "/" + filename

            # extracts the header from the given abc file
            composition_name = get_header(file_path, 'T')
            
            # converts the header into a string if it returns a list
            actual_header = ""

            # replacing the name 
            composition_name=get_header(file_path, 'T')

            # converting list to a string header
            if type(composition_name) == list:
                for header in composition_name:
                    header = header.replace(" ", "_")
                    actual_header += str(header)
            else:
                actual_header = composition_name.replace(" ", "_")

            # creates the song object
            song = SongCollection(actual_header)

            # appends the song object to the song_list
            song_list.append(song)


            # The actual extraction process
            extract_rhythmic_patterns(file_path)
            extract_pattern()

            # for each pattern and frequency, create a RhythmicPattern object and add it to the given song
            for k,v in v1_pattern.items():
                pattern = RhythmicPattern(k, v, True)
                song.add_pattern(pattern)

            for k,v in v2_pattern.items():
                pattern = RhythmicPattern(k, v, False)
                song.add_pattern(pattern)

            # Reset the global variables for the next song
            v1_pattern = {}
            v2_pattern = {}

            v1_keys = []
            v2_keys = []

            v1_combination = []
            v2_combination = []


def upload_rhythmic_patterns_to_DB():
    for song in song_list:
        database = Cluster("elliot", song.song_name, False)
        v1,v2 = song.get_patterns()

        model = RhythmicPatternModel(song.song_name, v1)
        passed = database.insert_rhythmic_pattern_model(database, model)

        # -----------------------------------------------------------------------
             # DEBUGGING PURPOSES, REMOVE BEFORE MERGING WITH MASTER
             # -----------------------------------------------------------------------
        print(f"V1 of song {song.song_name} has been {str(passed).upper()} added")

        if v2:
            model = RhythmicPatternModel(song.song_name, v2)
            passed = database.insert_rhythmic_pattern_model(database, model)
            
             # -----------------------------------------------------------------------
             # DEBUGGING PURPOSES, REMOVE BEFORE MERGING WITH MASTER
             # -----------------------------------------------------------------------
            print(f"V2 of song {song.song_name} has been {str(passed).upper()} added")
