"""
This file will be filled with the functions required to extract and save 
rhythmic patterns from an abc file
"""

from abc_tools import get_header,is_polyphonic,get_voicings,get_music


# Testing for the abc_tools
voicings=get_voicings('mxl_to_abc\converted_compositions\Cant_help_falling_in_love__Elvis_Presley.abc')

for voice in voicings:
  print(voice)
  print("\n\n")

print(len(voicings))

