'''
Author : Elliot
Last Edit : Elliot (7.10.2021 12:04AM) 
'''

# A major / minor notes (not for pentatonic scale)
notes = ['C', 'C#', 'D', 'D#', 'E', 'F',  'F#', 'G', 'G#', 'A', 'A#', 'B']

# A major / minor notes (for the pentatonic scales)

# Major Ionion Scale
I_major = 'WWHWWWH'

# Natural minor Aeolian Scale
A_minor = 'WHWWHWW'

# Major Pentatonic Scale
P_major = 'WWPW'

# Minor Pentatonic Scale
P_minor = 'PWWP'


def getScale(root, scaleType):
    '''
    Returns either a major or minor chord with the root as the root note.

        Parameters:
            root (String)        : the root note of the chord
            scaleType (String)   : the type of chord to build

        Returns:
            the chord generated from the root note
    '''

    # a list to hold the generated chord
    scale = [root]

    # The initial index of the note to start at
    key = notes.index(root)

    if scaleType == 'M':
        stepList = I_major
    elif scaleType == 'm':
        stepList = A_minor
    elif scaleType == 'pM':
        stepList = P_major
    elif scaleType == 'pm':
        stepList = P_minor

    # if the scaleType selected is a major chord (M)
    for char in stepList:
        # Whole step += 2; half step += 1
        if char == 'P':
            key += 3
        elif char == 'W':
            key += 2
        elif char == 'H':
            key += 1

        # to ensure that key does not go over the length of the notes array
        key = key % len(notes)

        # add it to the list to return
        scale.append(notes[key])

    return scale
