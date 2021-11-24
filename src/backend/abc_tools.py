"""
 This file contains tools for writing, reading and tweaking abc notation.
"""

"""
This function will retreive the header value of the given header key 

REQUIRED HEADERS
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
    contents = f.read()
    print(contents)
  
  f.close()

