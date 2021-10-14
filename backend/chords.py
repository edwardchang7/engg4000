'''
Author : Elliot
Last Edit : Thomas (13.10.2021 10:54AM)
'''

import triads

# A major / minor notes (not for pentatonic scale)
notes = ['C', 'C#', 'D', 'D#', 'E', 'F',  'F#', 'G', 'G#', 'A', 'A#', 'B']

# the number of semitones the seventh note is away from the previous triad

# Seventh Chord
major_seventh_chord = triads.M_triad + "4"
major_minor_seventh_chord = triads.M_triad + "3"
minor_seventh_chord = triads.m_triad + "3"
half_dim_chord = triads.D_triad + "4"
full_dim_chord = triads.D_triad + "3"

def genChord(root, chordType):
    '''
    Returns a list of notes to build the specified root chord

        Parameters:
            root (String)       : the note of the root chord
            chordType (String)  : the type of chord to build

        Returns:
            a list of notes within the chord
    '''

    base_chord = None

    # sets the initial key to the root index
    key = notes.index(root)

    # a empty variable to hold the selected chord type
    selectedChord = None

    # select the base triad of the chord to produce
    if chordType == 'M' or chordType == 'M7' or chordType == 'Mm7':
        base_chord = triads.genTriad(root, 'M')
    elif chordType == 'm' or chordType == 'm7':
        base_chord = triads.genTriad(root, 'm')
    elif chordType == 'D' or chordType == 'HD' or chordType == 'FD':
        base_chord = triads.genTriad(root, 'D')
    elif chordType == 'sus2':
        base_chord = triads.genTriad(root, 'sus2')
    elif chordType == 'sus4':
        base_chord = triads.genTriad(root, 'sus4')

    if chordType == 'M' or chordType == 'm' or chordType == 'D' or chordType == 'sus2' or chordType == 'sus4':
        return base_chord
    else:
        if chordType == 'M7':
            selectedChord = major_seventh_chord
        elif chordType == 'Mm7' :
            selectedChord = major_minor_seventh_chord
        elif chordType == 'm7':
            selectedChord = minor_seventh_chord
        if chordType == 'HD':
            selectedChord = half_dim_chord
        if chordType == 'FD':
            selectedChord = full_dim_chord

    # Goes through the numbers in each selectedChord
    # Each digit will be the next position of the note to add to the chord list
        for step in selectedChord:
            key += int(step)

            # to ensure that key does not go over the length of the notes array
            key = key % len(notes)

        base_chord.append(notes[key])
    
        return base_chord



        