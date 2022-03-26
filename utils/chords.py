'''
Author : Elliot, Thomas
Last Edit : Thomas (13.10.2021 10:54AM)
'''

import triads
from music_tools import *

# A major / minor notes (not for pentatonic scale)
# notes = ['C', 'C#', 'D', 'D#', 'E', 'F',  'F#', 'G', 'G#', 'A', 'A#', 'B']

# the number of semitones the seventh note is away from the previous triad

def gen_chord(root, type):
    '''
    Returns a list of notes to build the specified root chord

        Parameters:
            root (String)       : the note of the root chord
            chordType (String)  : the type of chord to build

        Returns:
            a list of notes within the chord
    '''
    chord = None

    # major M, major_7th : M7, major_minor_7th : Mm7
    if type == 'M' or type == 'M7' or type == 'Mm7':
        chord = triads.gen_triad(root, 'M')

    elif type == 'm' or type == 'm7':
        chord = triads.gen_triad(root, 'm')

    elif type == 'D' or type == 'HD' or type == 'FD':
        chord = triads.gen_triad(root, 'D')

    elif type == 'sus2':
        chord = triads.gen_triad(root, 'sus2')

    elif type == 'sus4':
        chord = triads.gen_triad(root, 'sus4')

    if type == 'M' or type == 'm' or type == 'D' or type == 'sus2' or type == 'sus4':
        return chord

    else:
        root = chord[len(chord) - 1]
        if type == 'M7':
            chord.append(whole_step(whole_step(root)))
        elif type == 'Mm7':
            chord.append(whole_step(half_step(root)))
        elif type == 'm7':
            chord.append(whole_step(half_step(root)))
        elif type == 'HD':
            chord.append(whole_step(whole_step(root)))
        elif type == 'FD':
            chord.append(whole_step(half_step(root)))
    
    return chord

# # Seventh Chord
# major_seventh_chord = triads.M_triad + "4"
# major_minor_seventh_chord = triads.M_triad + "3"
# minor_seventh_chord = triads.m_triad + "3"
# half_dim_chord = triads.D_triad + "4"
# full_dim_chord = triads.D_triad + "3"


# def genChord(root, chordType):
#     '''
#     Returns a list of notes to build the specified root chord

#         Parameters:
#             root (String)       : the note of the root chord
#             chordType (String)  : the type of chord to build

#         Returns:
#             a list of notes within the chord
#     '''

#     base_chord = None

#     # sets the initial key to the root index
#     key = notes.index(root)

#     # a empty variable to hold the selected chord type
#     selectedChord = None

#     # select the base triad of the chord to produce
#     if chordType == 'M' or chordType == 'M7' or chordType == 'Mm7':
#         base_chord = triads.genTriad(root, 'M')

#     elif chordType == 'm' or chordType == 'm7':
#         base_chord = triads.genTriad(root, 'm')

#     elif chordType == 'D' or chordType == 'HD' or chordType == 'FD':
#         base_chord = triads.genTriad(root, 'D')

#     elif chordType == 'sus2':
#         base_chord = triads.genTriad(root, 'sus2')

#     elif chordType == 'sus4':
#         base_chord = triads.genTriad(root, 'sus4')

#     if chordType == 'M' or chordType == 'm' or chordType == 'D' or chordType == 'sus2' or chordType == 'sus4':
#         return base_chord
#     else:
#         if chordType == 'M7':
#             selectedChord = major_seventh_chord
#         elif chordType == 'Mm7':
#             selectedChord = major_minor_seventh_chord
#         elif chordType == 'm7':
#             selectedChord = minor_seventh_chord
#         if chordType == 'HD':
#             selectedChord = half_dim_chord
#         if chordType == 'FD':
#             selectedChord = full_dim_chord

#     # Goes through the numbers in each selectedChord
#     # Each digit will be the next position of the note to add to the chord list
#         for step in selectedChord:
#             key += int(step)

#             # to ensure that key does not go over the length of the notes array
#             key = key % len(notes)

#         base_chord.append(notes[key])

#         return base_chord
