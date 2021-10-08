'''
Author : Elliot
Last Edit : Elliot (8.10.2021 08:54AM) 
'''

# A major / minor notes (not for pentatonic scale)
notes = ['C', 'C#', 'D', 'D#', 'E', 'F',  'F#', 'G', 'G#', 'A', 'A#', 'B']

# the number of semitones away from the previous note

# Major and minor Chord
M_chord = "43"
m_chord = "34"

#Diminished Chord
D_chord = "33"

# Suspended Chord (sus2 and sus4)
sus2_chord = "25"
sus4_chord = "52"


def genChord(root, chordType):
    '''
    Returns a list of notes to build the specified root chord

        Parameters:
            root 
    '''

    # adds the root note to the list first
    chord = [root]

    # sets the initial key to the root index
    key = notes.index(root)

    # a empty variable to hold the selected chord type
    selectedChord = None

    # select the type of chord to produce
    if chordType == 'M':
        selectedChord = M_chord
    elif chordType == 'm':
        selectedChord = m_chord
    elif chordType == 'D':
        selectedChord = D_chord
    elif chordType == 'sus2':
        selectedChord = sus2_chord
    elif chordType == 'sus4':
        selectedChord = sus4_chord

    # Goes through the numbers in each selectedChord
    # Each digit will be the next position of the note to add to the chord list
    for num in selectedChord:
        key += int(num)

        # to ensure that key does not go over the length of the notes array
        key = key % len(notes)

        chord.append(notes[key])
    
    return chord


genChord('C', 'M')

        