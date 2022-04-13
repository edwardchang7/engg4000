import re

"""
 This file contains tools for writing, reading and tweaking abc notation.
"""


def get_header(abc_file_path:str, header:str) -> str:
  """
  This function will retrieve the header value(s) of the given header key\n
  HEADERS EVERY SONG HAS\n
  X = Tune number\n
  T = Title of the tune\n
  T = A secondary title\n
  K = Tune key\n

  OPTIONAL HEADERS\n
  C = Composer of the music\n
  M = the meter of the music (4/4, 6/8 etc)\n
  L = note length as a proportion of a bar (ex 1/8, 1/4)\n
  R = Rhythm (jig, reel, waltz, polka etc)\n
  Q = Speed of playback in bpm\n
  V = Voicing \n
  P = Parts - specifying which parts should be played\n
  """
  
  with open(abc_file_path) as f:
    lines = f.readlines()
  
  header_list=[]
  for line in lines:
    if line.__contains__(header+":"):
      header_list.append(line[2:len(line)-1])
  f.close()
  
  # if there is only 1 element in the list, just return that element
  if len(header_list)==1 or header=='M':
    return header_list[0]

  # otherwise return the list
  return header_list


def is_polyphonic(abc_file_path:str) -> bool:
  '''
  This function will return 
  True --> Polyphonic
  False --> Monophonic
  '''
  num_voices=get_header(abc_file_path,"V")
  for voice in num_voices:
    if len(voice)>4:{
      num_voices.remove(voice)
    }
  # if there is more than 1 voicing, return True
  return (len(num_voices)>1)


def get_music(abc_file_path:str) -> list:
  '''
  This function will get the bulk music portion of the passed in abc file
  Chopping headers, footers etc
  '''
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



def get_voicings(abc_file_path:str) -> list:
  '''
  This function will return a list of strings
  Each element in the list will be an independent lines/voicing/melody of the passed in abc file
  '''
  
  # if there is only one voicing return that voicing
  if not is_polyphonic(abc_file_path):
    return get_music(abc_file_path)

  #otherwise split them and return a list of voicings
  else:
    music = get_music(abc_file_path)
    lines=re.split('V:[0-9]+',music)
    lines=lines[1:]
    return lines


def get_melodic_and_rythmic(abc_file_path:str) -> list:
  '''
  Gets the melodic and rhythmic voicings from the given file

  Parameters:
    abc_file_path: the abc file path

  Returns:
    voicing 1 and voicing 2
  '''
  lines = []
  found1, found2 = False, False
  v1 = []
  v2 = []

  with open(abc_file_path) as f:
    lines = f.readlines()

  for line in lines:

    if len(line) == 4 and line == 'V:3\n':
      break

    if len(line) == 4 and line == 'V:1\n':
      found1 = True
    elif len(line) == 4 and line == 'V:2\n':
      found1 = False
      found2 = True
    
    if(found1 and not found2):
      v1.append(line)

    if(found2 and not found1):
      v2.append(line)

  return v1,v2


