"""
A collection to hold a list of patterns within the song
"""


class Song_Collection:
    def __init__(self, song_name, v1_patterns=None, v2_patterns=None):
        self.song_name = song_name

        # if a pattern list is passed in then use that pattern list, else create an empty list
        if v1_patterns:
            self.v1_patterns = v1_patterns
        else:
            self.v1_patterns = []

        if v2_patterns:
            self.v2_patterns = v2_patterns
        else:
            self.v2_patterns = []

    '''
    Adds the given pattern to either v1 or v2
    '''
    def add_pattern(self, pattern) -> None:
        if pattern.frequency > 1:
            if pattern.is_v1:
                self.v1_patterns.append(pattern)
            else:
                self.v2_patterns.append(pattern)

    '''
    Returns both v1 and v2
    '''
    def get_patterns(self):
        return self.v1_patterns, self.v2_patterns

    def __str__(self):
        to_return = self.song_name + "\n"

        for bar in self.v1_patterns:
            to_return += str(bar)

        for bar in self.v2_patterns:
            to_return += str(bar)

        return to_return
