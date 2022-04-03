class ABCSong:
    def __init__(self, composer: str = "Automated Musicians", song_name: str = None, key: str, time_signature: str, song_input: list):
        # Instance variables used to generate the header
        self.composer = composer
        self.title = song_name if song_name is not None else "" #TODO: implement coolname dependency
        self.key = key
        self.time_signature = time_signature

        # Instance variables used to generate the abc song
        self.song_input = song_input

        # Instance variables used to keep track of results
        self.header = ""
        self.song = ""
        self.abc_song = ""

    def __build_header(self) -> str:
        header = "X:1\n"
        header += f"C:{self.composer}"
        header += f"K:{self.key}"
        header += f"T:{self.title}"
        header += f"M:{self.time_signature}\n"

        self.header = header
        return header
    
    def __build_song(self) -> str:
        song = ""
        # Used to iterate song_input, which is: [note_pattern_key, note_pattern_beat, note_pattern_key, note_pattern_beat, ...]
        # True = note_pattern_key
        # False = note_pattern_beat
        iterator = True

        for list_item in song_input:
            if iterator:
                #TODO: code for writing note/chord to abc format
            else:
                #TODO: code for writing beat number to abc format
            iterator = not iterator

        self.song = song
        return song

    def get_abc(self) -> str:
        abc_song = __build_header() + __build_song()
        self.abc = abc_song
        return abc_song




# Write a secion of PatternNote's to abc format
# PatternNote.note
# PatternNote.noteLength

'''
noteLengths:
8 = whole note
6 = half note + .
4 = half note
3 = quater note + .
2 = quater note
1 = 8th note
0 = 16th note
'''

# Chord generation example:
# given entry --> C:['111'] (C major chord with 3 notes)
#
# use function def gen_chord_rand(root: str, type: str, num_notes: int) from chords.py
# gen_chord_rand(C,M,3)= ['C', 'E', 'G']
# can then write it into abc like [CEG]
