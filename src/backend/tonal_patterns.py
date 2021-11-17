from music_tools import *
from scales import *

def analyze_patterns(key = 'GM', input_string = 'E/ | G A/ (B3/4 c/4) B/ | A F/ (D3/4 E/4) F/ | G E/ (E3/4 ^D/4) E/ | F3/ B, E/ | G A/ (B3/4 c/4) B/ | A F/ (D3/4 E/4) F/ | (G3/4 F/4) E/ (^D3/4 ^C/4) D/ | E3/ E3/ |"^Chorus" d3/ (d3/4 c/4) B/ | A F/ (D3/4 E/4) F/ | G E/ (E3/4 ^D/4) E/ | F ^D/ B,3/ | d3/ (d3/4 c/4) B/ | A F/ (D3/4 E/4) F/ | (G3/4 F/4) E/ (^D3/4 ^C/4) D/ | E3/ E|]'):

    analyze_str = ""
    flag = True

    for char in input_string:
        if char == '"': #removes "chorus" from string
            flag = not flag
        if flag:
            if char.isalpha() or char == "'" or char == "," or char == "_" or char == "^" or char == "|": #removes rythmyic related things
                analyze_str += char

    print(get_scale(key[0], key[1]))
    print(analyze_str)

    #hardcoded for now to test pattern freq
    pattern = ['h', '-h']

    print(frequency_of_pattern(analyze_str, key, pattern))
    print(frequency_of_pattern(analyze_str, key, pattern[::-1]))

def frequency_of_pattern(analyze_str, key, pattern):

    prev_chars = ""
    prev_notes = []
    total = 0

    for char in analyze_str:
        print(char)
        print(prev_chars)
        print(prev_notes)
        if char == "'" or char == ",":
            prev_chars += char
        elif char != "|" and char != " ":
            if prev_chars[:1] == "^":
                prev_chars += "#"
            elif prev_chars[:1] == "_": #fix to work with flats
                prev_chars += "_"
            else:
                if prev_chars != "":
                    prev_notes.append(prev_chars)
                prev_chars = ""
                prev_chars += char

        if len(prev_notes) == len(pattern) + 1:
            i = 0
            up = True
            test_note = ""
            for note in prev_notes:

                if test_note != "":
                    if test_note != note:
                        break
                if i < len(pattern):
                    if pattern[i][0] == '-':
                        up = False
                        pattern[i][0] = pattern[i][1]

                    if pattern[i][0] == 'h':
                        print(note)
                        test_note = half_step(note, up)

                i + 1

            if i == len(prev_notes):

                total += 1

            prev_chars = ""
            prev_notes = []

    return total
