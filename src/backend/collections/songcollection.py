"""
A collection to hold a list of patterns within the song
"""


class SongCollection:

    def __init__(self, song_name:str, v1_patterns:list=None, v2_patterns:list=None):
        self.song_name = song_name

        # if a pattern list is passed in then use that pattern list, else create an empty list

        self.v1_patterns = v1_patterns if v1_patterns else []
        self.v2_patterns = v2_patterns if v2_patterns else[]


    
    def add_pattern(self, pattern:list) -> None:
        '''
        Adds the given pattern to either v1 or v2
        '''
        if pattern.frequency > 1:
            if pattern.is_v1:
                self.v1_patterns.append(pattern)
            else:
                self.v2_patterns.append(pattern)

    
    def get_patterns(self) -> list:
        '''
        Returns both v1 and v2
        '''
        return self.v1_patterns, self.v2_patterns

    
