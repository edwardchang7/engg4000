"""
This file will be filled with the functions required to extract and save
rhythmic patterns from an abc file

1. If polyphonic - seperate
2. Get meter and time signature
3. Translate notes in bars into numbers representing note lengths
4. Analyze numbers looking for patterns
5. Cross reference those sections with original music to get actual musical pattern
"""
from ast import pattern
from itertools import combinations_with_replacement
import re
from typing import List
from abc_tools import get_header, is_polyphonic, get_voicings, get_music


pattern_dict = {}
bars_list = []


def extract_rhythmic_patterns(file_path: str):
    voicings = get_voicings(file_path)
    meter = get_header(file_path, 'M')
    encoded_voicings = encode_voicings(voicings)


# Function to isolate the notes in a single bar
def format_bar(bar: str):
    has_notes = re.search('[A-Ga-g]', bar)
    if not has_notes:
        bar = None
    else:
        bar = re.sub('%[0-9]+', "", bar)
        # added
        bar = re.sub(':', "", bar)
        bar = re.sub("{/[a-z]'}", "", bar)
        bar = re.sub("=", "", bar)
        bar = re.sub("Q[0-9]+", "", bar)
        bar = re.sub("[[0-9]+]","",bar)
        # bar = re.sub("[[A-Z][A-Z]]", "", bar)
        # bar = re.sub("[[A-Z][0-9]/[0-9]]","",bar)
        # end
        bar = re.sub('"[^"]*"', "", bar)
        bar = re.sub('![^"]*!', "", bar)
        # bar = re.sub('[[A-Z]:[^"]*]', "", bar)
        bar = bar.replace("\n", "")
        bar = bar.replace("$", "")
        
        #added
        bar = bar.replace("^", "")
        bar = bar.replace("_", "")
        bar = bar.replace("/", "0")
        #end
        bar = bar.strip()
    return bar

# Function to encode a musical bar into numbers representing the note lengths
# def encode_bar(bar:str):


def encode_voicings(voicings):
    # 1. isolate notes
    # split into sections
    # split sections into bars

    # combines 4 bars toghether
    combination_of_bars = ""
    # keeps track of the number of bars combined
    counter = 0
    # flag to check if it has already been added into the combination

    for voice in voicings:
        sections = voice.split('||')
        for section in sections:
            bars = section.split("|")


            '''
            Combine 4 bars together, then send to encode_bars
            '''
            for bar in bars:
                bar = format_bar(bar)

                if(bar):
                    if counter < 2:
                        combination_of_bars += str(bar) + " "
                        counter += 1

                    else:
                        combination_of_bars += str(bar) + " " # the last one to add to the combination, else it would always skip 1
                        bars_list.append(combination_of_bars)
                        counter = 0
                        combination_of_bars = ""

            # for bar in bars:
            #     bar = format_bar(bar)
            #     if(bar):
            #         # each bar_list holds a seperated bar element
            #         bar_list = encode_bar(bar)
            #         print(bar_list)
                    
                # if(bar):
                #   bar=encode_bar(bar)

    # 2. Change notes in bars into a number

'''
Takes in a bar (str) and splits them by white space. The beats of the note are
shown in numbers beside the note.
EX:
8 = 1 (whole) note
6 = 1/2 note with "."
4 = 1/2 note
3 = 1/4 note with "."
2 = 1/4 note
1 = 1/8 note
0 = 16th note
[xxx]n = the chord contains all n type of notes (refer to top for n)
'''
def encode_bars(bar) -> list:
    bar_list = []

    bar = bar.split()

    for note in bar:
        # checks if the given string have numbers in it, if so then we dont need add a number
        # to show the type of note

        contains_num = any(map(str.isdigit, note))

        exception_chars = {'Q','z','x','M'}

        if not contains_num:
            note += '1'

        if note not in exception_chars:
            bar_list.append(note)

    return bar_list


def extract_patterns(bars):
    # checks if the given bar already exist within the dict
    if bars in pattern_dict:
        count = pattern_dict.get(bars)
        count += 1
        # update the count of that given string
        pattern_dict[bars] = count
    else:
        pattern_dict[bars] = 1

    


extract_rhythmic_patterns(
    'src/backend/mxl_to_abc/converted_compositions/mary_had_a_little_lamb.abc')

for line_of_bars in bars_list:
    extract_patterns(line_of_bars)


for key,value in pattern_dict.items():
    print(f"{key} : {value}")