'''
Author : Elliot, Thomas
Last Edit : Thomas (13.10.2021 10:54AM)
'''

from src.backend.triads import *
from src.backend.music_tools import *
# A major / minor notes (not for pentatonic scale)
# notes = ['C', 'C#', 'D', 'D#', 'E', 'F',  'F#', 'G', 'G#', 'A', 'A#', 'B']

# the number of semitones the seventh note is away from the previous triad

def gen_chord(root, type, extra_note_list):
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
        chord = gen_triad(root, 'M')

    elif type == 'm' or type == 'm7':
        chord = gen_triad(root, 'm')

    elif type == 'D' or type == 'HD' or type == 'FD':
        chord = gen_triad(root, 'D')

    elif type == 'sus2':
        chord = gen_triad(root, 's2')

    elif type == 'sus4':
        chord = gen_triad(root, 's4')

    if not extra_note_list and (type == 'M' or type == 'm' or type == 'D' or type == 'sus2' or type == 'sus4'):
        return chord

    else:
        root = chord[len(chord) - 1]
        if type == 'M7':
            chord.append(M3(root, True))
        elif type == 'Mm7':
            chord.append(m3(root, True))
        elif type == 'm7':
            chord.append(m3(root, True))
        elif type == 'HD':
            chord.append(M3(root, True))
        elif type == 'FD':
            chord.append(m3(root, True))
    if not extra_note_list:
        return chord

    else: #if extra_note_list is not empty, then need to add more notes
        for note_in_chord in extra_note_list:
            if note_in_chord[0] == '0':
                note = chord[0]
            elif note_in_chord[0] == '1':
                note = chord[1]
            elif note_in_chord[0] == '2':
                note = chord[2]
            elif note_in_chord[0] == '3':
                note = chord[3]

            for symbol in note_in_chord[1:]:
                if symbol == "'":
                    note = change_octave(note, True)
                elif symbol == ',':
                    note = change_octave(note, False)

            chord.append(note)

        # Ex: if extra_note_list = [] and we call gen_chord('C', 'm7', extra_note_list) => output = ['C', 'D#', 'G', A#']
        # if extra_note_list = ["1'", '3,', "2''"] and we call gen_chord('C', 'm7', extra_note_list) => output = ['C', 'D#', 'G', A#', "d#'", 'A#,', "g''"]

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
