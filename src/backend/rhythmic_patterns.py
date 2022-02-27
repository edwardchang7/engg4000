"""
This file will be filled with the functions required to extract and save 
rhythmic patterns from an abc file

1. If polyphonic - seperate
2. Get meter and time signature
3. Translate notes in bars into numbers representing note lengths
4. Analyze numbers looking for patterns
5. Cross reference those sections with original music to get actual musical pattern
"""

from hashlib import new
from math import comb
import re
from typing import List
from abc_tools import get_header,is_polyphonic,get_voicings,get_music


keys = []
pattern_extraction = {}
combination_bar = []


def extract_rhythmic_patterns(file_path:str):
  voicings=get_voicings(file_path)
  meter=get_header(file_path,'M')
  encoded_voicings=encode_voicings(voicings)
  

# Function to isolate the notes in a single bar
def format_bar(bar:str):
  has_notes=re.search('[A-Ga-g]',bar)
  if not has_notes:
    bar=None
  else:
    bar=re.sub('%[0-9][0-9]?[0-9]?',"",bar)
    bar=re.sub('"[^"]*"',"",bar)
    bar=re.sub('![^"]*!',"",bar)
    bar=re.sub('[[A-Z]:[^"]*]',"",bar)
    bar=bar.replace("\n","")
    bar=bar.replace("$","")
    bar=bar.replace("{/f'}", "")
    bar=bar.replace(":", "")
    bar=bar.strip()
  return bar


def encode_voicings(voicings):
  #1. isolate notes
    # split into sections
    # split sections into bars
  for voice in voicings:
    sections=voice.split('||')
    for section in sections:
      bars=section.split("|")
      for bar in bars:
        bar=format_bar(bar)

        if(bar):
            # now each bar has just the note, and the beat count (if any)
            bar = encode_bar(bar) 
            if(bar):  
                combination_bar.extend(bar)






        # if(bar):
        #   bar=encode_bar(bar)


        
  #2. Change notes in bars into a number


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
    bar = bar.replace("/","0")
    bar = bar.split()

    no_mod_bar = []
    all_beats_bar = []
    new_bar = []

    # for each note in the bar remove all modifiers (pitch)
    for note in bar:
        note = ''.join(c if c.isalpha() or c.isdigit() or c == '[' or c == ']' else '' for c in note)
        no_mod_bar.append(note)

    # go through the new bars. for each note of the new bar, check if there is a beat
    # if there is no numbers, put 1
    for note in no_mod_bar:
         # keeps track of whether given note or chord has a beat
        contains_beat = any(char.isdigit() for char in note)

        # create a new bar and put them in
        if not contains_beat:
            all_beats_bar.append(note + "1")
        else:
            all_beats_bar.append(note)

    # replace the notes with the beats
    for note in all_beats_bar:
        beat = note[-1]

        if not beat.isdigit():
            beat = note[0]

        new_bar.append(_keep_beats_only(note, beat))

    # remove all non notes
    for note in new_bar:
        # if a number exist within the note, assume its valid, else, new_bar remove it
        if not any(char.isdigit() for char in note):
            new_bar.remove(note)
        
    if(new_bar):
        return new_bar

'''
Replaces each note with the given beat (keeps square bracket to signify that its a chord)
'''
def _keep_beats_only(note, beat):

    exception_list = {'x'}
    new_note = ''

    for c in note:
        if c.isalpha() and c not in exception_list:
            new_note += beat
        elif c  == '[' or c == ']':
            new_note += c

    return new_note
    
def pattern(seq):
    # get 3 combined bars
    count = 3
    temp = []

    # sets the keys for the dictionary
    for counter in range(3, 6):
        for bar in combination_bar:
            if count == counter:
                count = 0
                keys.append(temp)
                temp = []
            else:
                count += 1
                temp.append(bar)

    
    for set_of_bars in keys:
        if str(set_of_bars) in pattern_extraction.keys():
            pattern_extraction[str(set_of_bars)] += 1
        else:
            pattern_extraction[str(set_of_bars)] = 1


extract_rhythmic_patterns('src/backend/mxl_to_abc/converted_compositions/mary_had_a_little_lamb.abc')
pattern(combination_bar)

for key,value in pattern_extraction.items():
    print(f"{value} : {key}")