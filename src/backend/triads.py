'''
Author : Elliot, Thomas
Last Edit : Thomas (17.11.2021 11:19PM)
'''

from src.backend.music_tools import *

# # Major and minor triad
# M_triad = root->major_third(M3)->minor_third(m3)
# m_triad = root->minor_third(m3)->major_third(M3)

# # Diminished triad
# D_triad = root->minor_third(m3)->minor_third(m3)

# # Suspended triad (sus2 and sus4)
# sus2_triad = root->whole_step->major_third(M3) + half_step
# sus4_triad = root->major_third(M3) + half_step->whole_step


def gen_triad(root, type):
    '''
    Returns a list of notes to build the specified root triad
        Parameters:
            root (String)       : the note of the root triad
            triadType (String)  : the type of triad to build
        Returns:
            a list of notes within the triad
    '''

    triad = [root]

    if type == 'M':
        root = whole_step(whole_step(root, True), True)
        triad.append(root)

        triad.append(whole_step(half_step(root, True), True))

    elif type == 'm':
        root = whole_step(half_step(root, True), True)
        triad.append(root)

        triad.append(whole_step(whole_step(root, True), True))

    elif type == 'D':
        root = whole_step(half_step(root, True), True)
        triad.append(root)

        triad.append(whole_step(half_step(root, True), True))

    elif type == 's2':
        root = whole_step(root, True)
        triad.append(root)

        triad.append(M3(half_step(root, True), True))

    elif type == 's4':
        root = M3(half_step(root, True), True)
        triad.append(root)

        triad.append(whole_step(root, True))

    return triad
