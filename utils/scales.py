from music_tools import *

# notes = ['C', 'C#', 'D', 'D#', 'E', 'F',  'F#', 'G', 'G#', 'A', 'A#', 'B']

# # Major Ionion Scale
# I_major = 'WWHWWWH'

# # Natural minor Aeolian Scale
# A_minor = 'WHWWHWW'

# # Major Pentatonic Scale
# P_major = 'WWPW'

# # Minor Pentatonic Scale
# P_minor = 'PWWP'


def get_scale(root, type):
    '''
    Returns a chord from the root node.

        Parameters:
            root (String) : the root note of the chord
            type (String) : the type of chord to build
        Return:
            a chord with the root as the chord type
    '''
    # adds the root node into the list first
    scale = [root]

    if type == 'M':
        # WW
        for _ in range(2):
            root = whole_step(root)
            scale.append(root)

        # H
        root = half_step(root)
        scale.append(root)

        # WWW
        for _ in range(3):
            root = whole_step(root)
            scale.append(root)

        # H
        scale.append(half_step(root))

        return scale

    elif type == 'm':
        # W
        root = whole_step(root)
        scale.append(root)

        # H
        root = half_step(root)
        scale.append(root)

        # WW
        for _ in range(2):
            root = whole_step(root)
            scale.append(root)

        # H
        root = half_step(root)
        scale.append(root)

        # WW
        for _ in range(2):
            root = whole_step(root)
            scale.append(root)

        return scale

    elif type == 'pM':
        # WW
        for _ in range(2):
            root = whole_step(root)
            scale.append(root)

        # HW
        root = whole_step(half_step(root))
        scale.append(root)

        # W
        scale.append(whole_step(root))

        return scale

    elif type == 'pm':
        # WH
        root = whole_step(half_step(root))
        scale.append(root)

        # WW
        for _ in range(2):
            root = whole_step(root)
            scale.append(root)

        # WH
        root = whole_step(half_step(root))
        scale.append(root)

        return scale

# def getScale(root, scaleType):
#     '''
#     Returns either a major or minor chord with the root as the root note.

#         Parameters:
#             root (String)        : the root note of the chord
#             scaleType (String)   : the type of chord to build

#         Returns:
#             the chord generated from the root note
#     '''

#     # a list to hold the generated chord
#     scale = [root]

#     # The initial index of the note to start at
#     key = notes.index(root)

#     if scaleType == 'M':
#         stepList = I_major
#     elif scaleType == 'm':
#         stepList = A_minor
#     elif scaleType == 'pM':
#         stepList = P_major
#     elif scaleType == 'pm':
#         stepList = P_minor

#     # if the scaleType selected is a major chord (M)
#     for char in stepList:
#         # Whole step += 2; half step += 1
#         if char == 'P':
#             key += 3
#         elif char == 'W':
#             key += 2
#         elif char == 'H':
#             key += 1

#         # to ensure that key does not go over the length of the notes array
#         key = key % len(notes)

#         # add it to the list to return
#         scale.append(notes[key])

#     return scale

