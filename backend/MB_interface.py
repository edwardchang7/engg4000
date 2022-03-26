import sys

import musicalbeeps

# This redirects the path to look for the files inside "utils" folder
sys.path.append(sys.path[0] + '\\..\\utils')

from chords import gen_chord
from scales import gen_scale
from triads import gen_triad

# Octave 4 is the default octave we usually play in
# This creates a player object that is responsible for outputting the sound
player = musicalbeeps.Player(volume=1, mute_output=False)

# to use this function with the default values do:
# produce_sound(root, type, note_type)
# to use this function and play in a different octave do:
# produce_sound(root, type, note_type, octave_number)
# same logic is applied for the duration
def produce_sound(root, type, note_type, octave=4 ,duration=0.4):
    '''
    Plays the sound based on the type of chord | scale | triad that was given.
    The duration of the sound to play by default is set to 0.4s.
    The sound produces is in the default octave (4).
    The higher the octave number, the higher the pitch

        Parameters:
            root (String)       : the root note of the chord | scale | triad to generate
            type (String)       : the type of combination to generate (chord, scale, triad)
            note_type (String)  : the type of chord | scale | triad to generate (minor, major, etc.)
    '''
    # a dictionary to keep the notes and the duration
    sound_dict = {}

    # the generated chord | scale | triad
    combination = []

    if type == 'triad':
        combination = gen_triad(root, note_type)

    elif type == 'chord':
       combination = gen_chord(root, note_type)

    elif type == 'scale':
        combination = gen_scale(root, note_type)

    # adding all the notes from the combination (scale, chord, triad) into a dictionary 
    # the key   : note
    # the value : duration to play (0.4s by default)
    for note in combination:
        sound_dict[note] = duration

    # for each dictionary item (the note, the duration)
    for note,dur in sound_dict.items():

        '''
        If the note is a '#' note, then input the octave in between the note

            Example:
                to play C# in octave 5, for musical beeps to recognize it 
                you need to input : C5#
                this 'if statement' below does that
                if you want to play C# in octave 4 (default octave)
                you can either do : C# or C4# 
        '''
        if len(note) ==2:
            player.play_note(note[0] + str(octave) + note[1], float(dur)) 

        # if the note is just a single note without any 'modifiers' then just append the octave at the end
        else:
            player.play_note(note + str(octave), float(dur)) 
