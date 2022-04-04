import ast

from coolname import generate_slug
from src.backend.chords import gen_chord_rand


class ABCSong:
    def __init__(self, composer: str = "Automated Musicians", song_name: str = generate_slug(), key: str, time_signature: str, song_input: list):
        # Instance variables used to generate the header
        self.composer: str = composer
        self.title: str = song_name
        self.key: str = key
        self.time_signature: list = time_signature.split("/") # Ex: ['4','4']

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
    
    def __build_song(self, num_of_measures: int) -> str:
        song: str = ""

        num_of_beats_in_each_measure: float = time_signature[0] * time_signature[1]
        for note_pattern in song_input:
            note: str = note_pattern.get_note()
            length: int = note_pattern.get_length()
            parsed_note: str = None
            parsed_length: str = None

            # Chord
            if "[" in length and "]" in length:
                parsed_length = ast.literal_eval(note_length) # Convert string (note_length) to list (chord)
                
                if note[-1] == 'm': # Minor chord
                    chord = gen_chord_rand(note[:-1], 'm', len(parsed_length[0]))
                else # Major chord
                    chord = gen_chord_rand(note, 'M', len(parsed_length[0]))

                num_of_beats_in_current_note_or_chord: float = __get_note_type(parsed_length[0][0]) * (time_signature[0] * time_signature[1]) 
            else # Note
                chord = gen_chord_rand(note, 'M', 1)
                num_of_beats_in_current_note_or_chord: float = __get_note_type(length) * (time_signature[0] * time_signature[1]) 
            
            # Check if the current measure has enough room for the current note
            if num_of_beats_in_current_note_or_chord > num_of_beats_in_each_measure:
                song += "| \n"
                num_of_beats_in_each_measure = time_signature[0] * time_signature[1]
                num_of_beats_in_each_measure -= num_of_beats_in_current_note

            song += f"[{"".join(chord)}] " # Add chord to ABC output

        self.song = song
        return song

    def get_abc(self) -> str:
        abc_song: str = self.__build_header() + self.__build_song()
        self.abc = abc_song
        return abc_song

    def __get_note_type(self, note) -> float:
        match note:
            case 0: # 16th note
                return 1/16
            case 1: # 8th note
                return 1/8
            case 2: # quarter note
                return 1/4
            case 3: # quarter note + .
                return 3/8
            case 4: # half note
                return 1/2
            case 6: # half note + .
                return 3/4
            case 8: # whole note
                return 1
            case _:
                return None



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
