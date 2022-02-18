import src.backend.scales

notes = ['C', '#C', 'D', '#D', 'E', 'F',  '#F', 'G', '#G', 'A', '#A', 'B']

'''

  Within utility functions:
    input_note    : note to change frequency of
    up_frequency  : bool value which denotes whether frequency of note is increasing or decreasing

'''

def half_step(input_note, up_frequency):

    letter = input_note[0]
    comp_note = input_note[0].upper()
    octave = input_note[1:]
    index = 0
    flag = False

    if len(input_note) > 1:
        if input_note[0] == '#':
            letter = input_note[1]
            comp_note = '#' + input_note[1].upper()
            octave = input_note[2:]

    if up_frequency:
        for i in range(len(notes)):
            if comp_note == notes[i]:
                if (i+1) == len(notes):
                    if octave == "''" or octave == "'":
                        octave = octave + "'"
                    elif octave == "":
                        flag = True
                        if letter.islower():
                            octave = octave + "'"
                    elif octave == ",":
                        octave = ''
                    elif octave == ",,":
                        octave = ","
                    elif octave == ",,,":
                        octave = ",,"

                index = (i+1) % (len(notes))

    else:
        for i in range(len(notes)):
            if comp_note == notes[i]:
                if (i-1) == -1:
                    if octave == ",," or octave == ",":
                        octave = octave + ","
                    elif octave == "":
                        if not letter.islower():
                            octave = octave + ","
                    elif octave == "'":
                        octave = ''
                    elif octave == "''":
                        octave = "'"
                    elif octave == "'''":
                        octave = "''"

                index = (i-1) % (len(notes))

    if flag or letter.islower():
        return notes[index].lower() + octave
    else:
        return notes[index] + octave

def whole_step(input_note, up_frequency):
    return half_step(half_step(input_note, up_frequency), up_frequency)


def M3(input_note, up_frequency):
    '''

      Modifies the frequency of the input note by a Major Third, using whole steps

    '''
    return whole_step(whole_step(input_note, up_frequency), up_frequency)


def m3(input_note, up_frequency):
    '''

        Modifies the frequency of the input note by a Minor Third, using whole/half steps

      '''
    return whole_step(half_step(input_note, up_frequency), up_frequency)


def P5(input_note, up_frequency):
    '''

        Modifies the frequency of the input note by a Perfect 5th, using major/minor thirds

      '''
    return M3(m3(input_note, up_frequency),  up_frequency)


def change_octave(input_note, up_frequency):
    '''

        Modifies the frequency of the input note by an entire octave, using 6 whole steps

      '''
    return whole_step(whole_step(whole_step(whole_step(whole_step(whole_step(input_note, up_frequency), up_frequency), up_frequency), up_frequency), up_frequency), up_frequency)


def is_pattern_match(pattern_type, root, prev):
    '''
      Returns a boolean value of given notes are the pattern_type away from each other

      Param:
        pattern_type : the type of step (half step, whole step, etc)
        root : the original note to step from
        prev : the note to step to

      Return:
        a boolean value if the `prev` note matches the pattern_type given
    '''

    if 'h' in pattern_type or 'H' in pattern_type:
        if '-' in pattern_type:
            return half_step(root, False) == prev
        else:
            return half_step(root, True) == prev

    elif 'w' in pattern_type or 'W' in pattern_type:
        if '-' in pattern_type:
            return whole_step(root, False) == prev
        else:
            return whole_step(root, True) == prev

'''
COPY THIS FORMAT BELOW TO ADD MORE PATTERN TYPES


elif 'keyword.lower()' or 'keyword.upper()' in pattern_type:
  if '-' in pattern_type:
    return 'function_name_to_check' == prev
  else:
    return 'function_name_to_check' == prev
'''

def check_interval(key:str, starting_note:str, end_note:str):
    '''
          Checks and returns what kind of interval (i.e. H, W, P5, wtc.) is between end_note and starting_note

          Param:
            key: key relating the input scale
            scale: reference scale
            starting_note: note to start the interval on
            end_note: note to end the interval on

          Return:
            The type of interval as a str
        '''

    try:
        scale = src.backend.scales.get_scale(key[0], key[1])
    except IndexError:
        scale = src.backend.scales.get_scale(key, "M")

    ##must account for sharps/flats in Key for proper intervals

    #if starting_note's index in scale < end_note
        #easy case, check if starting_note + half_step, or + whole_step etc. == end_note
    #if starting_notes's index in scale > end_note
        #octave change within interval, keep track
