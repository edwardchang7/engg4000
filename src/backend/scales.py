from src.backend.music_tools import *

def get_scale(root:str, type:str) -> list:
    '''
    Returns a scale beginning from the root node.

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
            root = whole_step(root, True)
            scale.append(root)

        # H
        root = half_step(root, True)
        scale.append(root)

        # WWW
        for _ in range(3):
            root = whole_step(root, True)
            scale.append(root)

        # H
        scale.append(half_step(root, True))

        return scale

    elif type == 'm':
        # W
        root = whole_step(root, True)
        scale.append(root)

        # H
        root = half_step(root, True)
        scale.append(root)

        # WW
        for _ in range(2):
            root = whole_step(root, True)
            scale.append(root)

        # H
        root = half_step(root, True)
        scale.append(root)

        # WW
        for _ in range(2):
            root = whole_step(root, True)
            scale.append(root)

        return scale

    elif type == 'pM':
        # WW
        for _ in range(2):
            root = whole_step(root, True)
            scale.append(root)

        # HW
        root = whole_step(half_step(root, True), True)
        scale.append(root)

        # W
        scale.append(whole_step(root, True))

        return scale

    elif type == 'pm':
        # WH
        root = whole_step(half_step(root, True), True)
        scale.append(root)

        # WW
        for _ in range(2):
            root = whole_step(root, True)
            scale.append(root)

        # WH
        root = whole_step(half_step(root, True), True)
        scale.append(root)

        return scale


