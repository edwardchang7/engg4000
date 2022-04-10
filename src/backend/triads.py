from src.backend.music_tools import M3, half_step, whole_step


def gen_triad(root:str, type:str) -> list:
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


