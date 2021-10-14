'''
Author : Elliot
Last Edit : Thomas (13.10.2021 10:24AM)
'''

# A major / minor notes (not for pentatonic scale)
notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# the number of semitones away from the previous note

# Major and minor triad
M_triad = "43"
m_triad = "34"

# Diminished triad
D_triad = "33"

# Suspended triad (sus2 and sus4)
sus2_triad = "25"
sus4_triad = "52"

def genTriad(root, triadType):
    '''
    Returns a list of notes to build the specified root triad
        Parameters:
            root (String)       : the note of the root triad
            triadType (String)  : the type of triad to build
        Returns:
            a list of notes within the triad
    '''

    # adds the root note to the list first
    triad = [root]

    # sets the initial key to the root index
    key = notes.index(root)

    # a empty variable to hold the selected triad type
    selectedtriad = None

    # select the type of triad to produce
    if triadType == 'M':
        selectedtriad = M_triad
    elif triadType == 'm':
        selectedtriad = m_triad
    elif triadType == 'D':
        selectedtriad = D_triad
    elif triadType == 'sus2':
        selectedtriad = sus2_triad
    elif triadType == 'sus4':
        selectedtriad = sus4_triad

    # Goes through the numbers in each selectedtriad
    # Each digit will be the next position of the note to add to the triad list
    for num in selectedtriad:
        key += int(num)

        # to ensure that key does not go over the length of the notes array
        key = key % len(notes)

        triad.append(notes[key])

    return triad
