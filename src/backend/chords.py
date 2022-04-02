from src.backend.triads import *
from src.backend.music_tools import *


def gen_chord(root, type, extra_note_list):
    """
    Returns a list of notes to build the specified root chord

        Parameters:
            root (String)       : the note of the root chord
            chordType (String)  : the type of chord to build
            extra_note_list     : list which indicates which extra notes to add to chord
                                    each index is of the form "<note_number><abc_octave_punctuation>" i.e. "1''"
                                    root's note_number = 0

        Returns:
            a list of notes within the chord
    """
    chord = None

    # major M, major_7th : M7, major_minor_7th : Mm7
    if type == 'M' or type == 'M7':
        chord = gen_triad(root, 'M')

    elif type == 'm' or type == 'm7' or type == 'Mm7':
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
            chord.append(M3(root, True))
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


