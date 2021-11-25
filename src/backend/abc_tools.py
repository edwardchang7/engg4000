import math
import re

"""
 This file contains tools for writing, reading and tweaking abc notation.
"""

"""
This function will retreive the header value(s) of the given header key 
HEADERS EVERY SONG HAS
X = Tune number
T = Title of the tune
T = A secondary title
K = Tune key

OPTIONAL HEADERS
C = Composer of the music
M = the meter of the music (4/4, 6/8 etc)
L = note length as a proportion of a bar (ex 1/8, 1/4)
R = Rhythm (jig, reel, waltz, polka etc)
Q = Speed of playback in bpm
V = Voicing 
P = Parts - specifying which parts chould be played

"""
def get_header(abc_file_path:str, header:str) -> str:
  
  with open(abc_file_path) as f:
    lines = f.readlines()
  
  header_list=[]
  for line in lines:
    if line.__contains__(header+":"):
      header_list.append(line[2:len(line)-1])
  f.close()
  
  # if there is only 1 element in the list, just return that element
  if len(header_list)==1:
    return header_list[0]

  # otherwise return the list
  return header_list

'''
This function will return 
True --> Polyphonic
False --> Monophonic
'''
def is_polyphonic(abc_file_path:str):

  num_voices=get_header(abc_file_path,"V")
  # if there is more than 1 voicing, return True
  return (len(num_voices)>1)

'''
This function will get the bulk music portion of the passed in abc file
Chopping headers, footers etc
'''
def get_music(abc_file_path:str):
  with open(abc_file_path) as f:
    lines = f.readlines()

  line_count=0
  reading=False
  music=""

  for line in lines:

    # V:1 signifies the first voicing
    if line=="V:1\n":
      reading=True

    if reading:
      music+=line
    
    line_count+=1

  f.close()

  return music


'''
This function will return a list of strings
Each element in the list will be an independant lines/voicing/melody of the passed in abc file
'''
def get_voicings(abc_file_path:str):
  
  # if there is only one voicing return that voicing
  if not is_polyphonic(abc_file_path):
    return get_music(abc_file_path)

  #otherwise split them and return a list of voicings
  else:
    music = get_music(abc_file_path);
    lines=re.split('V:[0-9]+',music)
    lines=lines[1:]
    return lines

