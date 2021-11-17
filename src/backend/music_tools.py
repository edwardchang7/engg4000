notes = ['C', 'C#', 'D', 'D#', 'E', 'F',  'F#', 'G', 'G#', 'A', 'A#', 'B']

'''

  Within utility functions:
    input_note    : note to change frequency of
    up_frequency  : bool value which deleniates whether frequency of note is increasing or decreasing

'''

def half_step(input_note, up_frequency):

  comp_note = input_note[0].upper()
  octave = input_note[1:]

  if len(input_note) > 1:
    if input_note[1] == '#':
      comp_note = comp_note + '#'
      octave = input_note[2:]

  if up_frequency:
    for i in range(len(notes)):
      if comp_note == notes[i]:
        if (i+1) == len(notes):
          if octave == "''" or octave == "'" or octave == '':
            octave = octave + "'"
          elif octave == ",":
            octave = ''
          elif octave == ",,":
            octave = ","
          elif octave == ",,,":
            octave = ",,"

        index=(i+1)%(len(notes))

  else:
    for i in range(len(notes)):
      if comp_note == notes[i]:
        if (i-1) == -1:
          if octave == ",," or octave == "," or octave == '':
            octave = octave + ","
          elif octave == "'":
            octave = ''
          elif octave == "''":
            octave = "'"
          elif octave == "'''":
            octave = "''"

        index=(i-1)%(len(notes))

  if octave.count("'") > 0:
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
