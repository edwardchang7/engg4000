from re import S

notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

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
        if input_note[1] == '#':
            comp_note += "#"
            octave = input_note[2:]

    if up_frequency:
        for i in range(len(notes)):
            if comp_note == notes[i]:
                if (i + 1) == len(notes):
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

                index = (i + 1) % (len(notes))

    else:
        for i in range(len(notes)):
            if comp_note == notes[i]:
                if (i - 1) == -1:
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

                index = (i - 1) % (len(notes))

    if flag or letter.islower():
        if up_frequency and input_note == "c":
            return notes[index].lower() + octave
        elif not up_frequency and input_note == "c":
            return notes[index] + octave
        else:
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
    return M3(m3(input_note, up_frequency), up_frequency)


def change_octave(input_note, up_frequency):
    '''

      Modifies the frequency of the input note by an entire octave, using 6 whole steps

    '''
    return whole_step(whole_step(
        whole_step(whole_step(whole_step(whole_step(input_note, up_frequency), up_frequency), up_frequency),
                   up_frequency), up_frequency), up_frequency)


def check_interval(starting_note: dict, end_note: dict):
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

    interval = []
    to_append = []
    start_reference = pad_octave_notation(starting_note["octave"], starting_note["note"])
    end_reference = pad_octave_notation(end_note["octave"], end_note["note"])

    # Same note
    if start_reference == end_reference:
        return ["0"]

    up_temp = start_reference
    down_temp = start_reference
    down = False

    while True:

        if up_temp == end_reference:
            # if here, end is the higher frequency note
            break
        elif down_temp == end_reference:
            # if here, start is the higher frequency note
            down = True
            break
        else:
            interval.append("h")
            up_temp = half_step(up_temp, True)
            down_temp = half_step(down_temp, False)

    # Replace 12 half steps with associate interval, octave
    while len(interval) >= 12:
        interval = interval[:-12]
        to_append.append("o")

    # Replace 7 half steps with associate interval, perfect fifth
    if len(interval) >= 7:
        interval = interval[:-7]
        to_append.append("P5")

    # Replace 4 half steps with associate interval, Major third
    if len(interval) >= 4:
        interval = interval[:-4]
        to_append.append("M3")

    # Replace 3 half steps with associate interval, minor third
    if len(interval) >= 3:
        interval = interval[:-3]
        to_append.append("m3")

    # Replace 2 half steps with associate interval, whole step
    if len(interval) >= 2:
        interval = interval[:-2]
        to_append.append("w")

    interval += to_append

    # If start is higher note, is a negative interval so add notation
    if down:
        interval = ["-" + current for current in interval]

    return interval


def pad_octave_notation(octave: int, note: str):
    '''
        Add the necessary "'" and "," to the given note, given the octave

        Param:
          octave: the octave the note is in
          note: the associated note

        Return:
          The note string with octave notation in it
  '''

    if octave > 0:
        while octave != 1:
            note += "'"
            octave -= 1
        return note.lower()
    else:
        while octave != 0:
            note += ","
            octave += 1
        return note