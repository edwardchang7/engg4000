notes = ['C', '#C', 'D', '#D', 'E', 'F',  '#F', 'G', '#G', 'A', '#A', 'B']

'''

  Within utility functions:
    input_note    : note to change frequency of
    up_frequency  : bool value which deleniates whether frequency of note is increasing or decreasing

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


def h_step(input_note, up_frequency):

    # default the index to -1, will be changed to the index of the root note in notes if the root note is found within the notes
    index = -1

    # flag for if the given root is in the list
    in_list = input_note in notes

    # gets the index of the given root note if it is in the list, else index remains as -1
    if in_list:
        index = notes.index(input_note)

    if index >= 0:  # meaning that the given note is found within notes

        # check for if the root note is not the end of the notes list
        if index != len(notes)-1 and up_frequency:
            return notes[index + 1]

        elif index != 0 and not up_frequency:  # check for if the root note is not the first note
            return notes[index - 1]

        # if its the last note found in notes and going upwards
        elif index == len(notes)-1 and up_frequency:
            index = (index + 1) % len(notes)
            return notes[index].lower()

        # if its the first note found in notes and going backwards
        elif index == 0 and not up_frequency:  
            index = (index - 1) % len(notes)
            return notes[index] + ","

    elif not input_note.islower():  # if the root note is not found within the notes

        # remove all the modifiers that come along with the note
        original_note, modifiers = _strip(input_note)

        # get the index of the orinal note in the notes list
        index = notes.index(original_note)

        # check if its not the last note going upwards
        if index != len(notes)-1 and up_frequency:
            return notes[index + 1] + modifiers

        # check if its not the first not going downwards
        elif index != 0 and not up_frequency:
            return notes[index - 1] + modifiers

        # if its the first note going downwards
        if index == 0 and not up_frequency:
            index = (index - 1) % len(notes)
            return notes[index] + modifiers[:-1]

        # if its the last note going upwards
        elif index == len(notes) - 1 and up_frequency:
            index = (index + 1) % len(notes)
            return notes[index] + modifiers + modifiers[-1]

    elif input_note.islower():  # if its a lower cased char

        # convert the root to upper case
        original_note, modifiers = _strip(input_note.upper())

        # gets the index of the original note in the notes list
        index = notes.index(original_note)

        # check if its not the last note going upwards
        if index != len(notes) - 1 and up_frequency:
            return notes[index + 1].lower() + modifiers

        # check if its not the first note going downwards
        elif index != 0 and not up_frequency:
            return notes[index - 1].lower() + modifiers

        # if its the first note going downwards
        if index == 0 and not up_frequency:
            index = (index - 1) % len(notes)
            # if there are no modifiers, return uppercase version
            if len(modifiers) == 0:
                return notes[index]
            else:
                return notes[index].lower() + modifiers[:-1]

        # if its the last note going upwards
        if index == len(notes) - 1 and up_frequency:
            index = (index + 1) % len(notes)
            # if there are no modifers, add the ' at the end
            if len(modifiers) == 0:
                return notes[index].lower() + "'"
            else:
                return notes[index].lower() + modifiers + modifiers[-1]


def _strip(root):
    modifiers_list = ["'", ","]

    modifier, note = "", ""

    for c in root:
        if c in modifiers_list:
            modifier += c
        else:
            note += c

    return note, modifier


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

#------------ DEBUG ----------------
# REMOVE BEOFRE MERGING WITH MASTER
low = [note + "," for note in notes]
lower = [note + "," for note in low]
lowest = [note + "," for note in lower]

high = [note.lower() for note in notes]
higher = [note + "'" for note in high]
highest = [note + "'" for note in higher]

x = lower, upwards = True
print(x)
print([h_step(note, upwards) for note in x])
#------------ DEBUG ----------------