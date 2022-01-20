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
from typing import List
from abc_tools import get_header,is_polyphonic,get_voicings,get_music

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
    bar=bar.strip()
  return bar

# Function to encode a musical bar into numbers representing the note lengths
# def encode_bar(bar:str):

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
        print("--> "+bar)
        # if(bar):
        #   bar=encode_bar(bar)
        
  #2. Change notes in bars into a number

extract_rhythmic_patterns('mxl_to_abc/converted_compositions/Dancing_in_the_Moonlight.abc')