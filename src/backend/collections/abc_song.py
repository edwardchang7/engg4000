import ast

from coolname import generate_slug

from src.backend.chords import gen_chord_rand


class ABCSong:
    def __init__(self, key: str, time_signature: str, song_input: list, composer: str = "Automated Musicians",
                 song_name: str = generate_slug()):
        # Instance variables used to generate the header
        self.composer: str = composer
        self.title: str = song_name
        self.key: str = key
        self.time_signature: list = list(map(int, time_signature.split("/")))  # Ex: [4, 4]

        # Instance variables used to generate the song
        self.song_input: list = song_input

        # Instance variables used to store results
        self.header: str = ""
        self.song: str = ""
        self.abc_song: str = ""

    def __build_header(self) -> str:
        header = "X: 1\n"
        header += f"C: {self.composer}\n"
        header += f"K: {self.key}\n"
        header += f"T: {self.title}\n"
        header += f"M: {self.time_signature}\n"

        self.header = header
        return header

    def __build_song(self) -> str:
        song: str = ""

        num_of_beats_in_each_measure: float = self.time_signature[0] * self.time_signature[1]
        num_of_measures_in_a_line: int = 4
        is_eighth_note: bool = False
        eighth_note_counter: int = 0
        for note_pattern in self.song_input:
            note: str = note_pattern.note
            length: int = note_pattern.length
            parsed_length: str = None

            # Chord
            if "[" in length and "]" in length:
                parsed_length = ast.literal_eval(length)  # Convert string (note_length) to list (chord)
                parsed_length[0] = str(parsed_length[0])

                if note[-1] == 'm':  # Minor chord
                    chord = gen_chord_rand(note[:-1], 'm', len(parsed_length[0]))
                else:  # Major chord
                    chord = gen_chord_rand(note, 'M', len(parsed_length[0]))

                num_of_beats_in_current_note_or_chord: float = \
                    self.__get_note_type(int(parsed_length[0][0])) * (self.time_signature[0] * self.time_signature[1])
            else:  # Note
                chord = note
                num_of_beats_in_current_note_or_chord: float = \
                    self.__get_note_type(int(length)) * (self.time_signature[0] * self.time_signature[1])
                is_eighth_note = self.__is_eighth_note(int(length))

                if is_eighth_note:
                    eighth_note_counter += 1
                else:
                    eighth_note_counter = 0

            # Check if the current measure has enough room for the current note
            if num_of_beats_in_current_note_or_chord > num_of_beats_in_each_measure:
                num_of_measures_in_a_line -= 1

                if num_of_measures_in_a_line <= 0:
                    song += "| \n"
                    num_of_measures_in_a_line = 4
                else:
                    song += "| "

                num_of_beats_in_each_measure = self.time_signature[0] * self.time_signature[1]

            if "[" in length and "]" in length:
                abc_chord = ""

                for note_item in chord:
                    abc_chord += note_item

                song += f"[{abc_chord}]{parsed_length[0][0]} "  # Add chord to ABC output
            else:
                if is_eighth_note and eighth_note_counter < 5:
                    song += f"{chord}{length}"  # Add beam note to ABC output
                else:
                    song += f" {chord}{length} "  # Add note to ABC output
                    eighth_note_counter = 0

            num_of_beats_in_each_measure -= num_of_beats_in_current_note_or_chord

        song += "||"

        self.song = song
        return song

    def __get_note_type(self, note: int) -> float:
        if note == 0:  # 16th note
            return 1 / 16
        elif note == 1:  # 8th note
            return 1 / 8
        elif note == 2:  # quarter note
            return 1 / 4
        elif note == 3:  # quarter note + .
            return 3 / 8
        elif note == 4:  # half note
            return 1 / 2
        elif note == 6:  # half note + .
            return 3 / 4
        elif note == 8:  # whole note
            return 1

        return None

    def __is_eighth_note(self, note: int) -> bool:
        if note == 1:  # 8th note
            return True
        
        return False

    def get_abc(self) -> str:
        abc_song: str = self.__build_header() + self.__build_song()
        self.abc_song = abc_song
        return abc_song
