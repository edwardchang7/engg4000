import ast

from coolname import generate_slug


class ABCSong:
    def __init__(self, composer: str = "Automated Musicians", song_name: str = generate_slug(), key: str, time_signature: str, song_input: list):
        # Instance variables used to generate the header
        self.composer: str = composer
        self.title: str = song_name
        self.key: str = key
        self.time_signature: str = time_signature

        # Instance variables used to generate the song
        self.song_input: list = song_input

        # Instance variables used to store results
        self.header: str = ""
        self.song: str = ""
        self.abc_song: str = ""

    def __build_header(self) -> str:
        header = "X:1\n"
        header += f"C:{self.composer}"
        header += f"K:{self.key}"
        header += f"T:{self.title}"
        header += f"M:{self.time_signature}\n"

        self.header = header
        return header
    
    def __build_song(self) -> str:
        song: str = ""

        for note_pattern in song_input:
            note: str = note_pattern.get_note()
            length: int = note_pattern.get_length()

            # Check if note in note_pattern is a chord
            if "[" in note and "]" in note:
                note = ast.literal_eval(note) # Convert string to list

            


        self.song = song
        return song

    def get_abc(self) -> str:
        abc_song: str = self.__build_header() + self.__build_song()
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
