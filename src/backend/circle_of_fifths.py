class CircleOfFifths:
    # COF notes organized into lists
    major_notes: list = ['C', 'G', 'D', 'A', 'E', 'B', '_G', '_D', '_A', '_E', '_B', 'F']
    alternative_major_notes: list = ['C', 'G', 'D', 'A', 'E', '_C', '^F', '^C', '_A', '_E', '_B', 'F']
    minor_notes: list = ['a', 'e', 'b', '^f', '^c', '^g', '^d', '_b', 'f', 'c', 'g', 'd']
    alternative_minor_notes: list = ['a', 'e', 'b', '^f', '^c', '_a', '_e', '^a', 'f', 'c', 'g', 'd']

    # The number of piano keys (specifically black or white) between other two certain piano keys
    TWO_BLACK_KEYS = 2
    THREE_BLACK_KEYS = 3
    THREE_WHITE_KEYS = 3
    FOUR_WHITE_KEYS = 4

    # Index of a certain note within the COF note lists above
    B_MAJOR_NOTE_INDEX = 5
    B_FLAT_MAJOR_NOTE_INDEX = 10
    C_FLAT_ALTERNATIVE_MAJOR_NOTE_INDEX = 5
    B_FLAT_ALTERNATIVE_MAJOR_NOTE_INDEX = 10
    B_MINOR_NOTE_INDEX = 2
    B_FLAT_MINOR_NOTE_INDEX = 7
    B_ALTERNATIVE_MINOR_NOTE_INDEX = 2
    A_SHARP_ALTERNATIVE_MINOR_NOTE_INDEX = 7

    # Code -1 to signify that the provided note is not within a COF note list
    BASE_NOTE_NOT_FOUND = -1

    def get_cof(self, base_note: str) -> list:
        """
        Gets a scale that is specifically based on the note passed as base_note. This scale is different from the normal
        scale because it is in the context of 'circle of fifths' where a note is the fifth note after the previous note.

        :param base_note: The first note within the scale to get.
        :return: A scale based on the provided base_note. Returns an empty list if an incorrect base_note was provided.
        """
        notes: list = []

        if base_note in self.major_notes:
            notes = self.major_notes
        elif base_note in self.alternative_major_notes:
            notes = self.alternative_major_notes
        elif base_note in self.minor_notes:
            notes = self.minor_notes
        elif base_note in self.alternative_minor_notes:
            notes = self.alternative_minor_notes
        else:
            return notes

        base_note_index: int = notes.index(base_note)

        return notes[base_note_index:] + notes[:base_note_index]

    def get_num_of_black_keys(self, base_note: str) -> int:
        """
        Gets the number of black keys (on a piano) that are in between the provided base_note and the next note present
        in COF.

        :param base_note: A note present in the COF.
        :return: The number of black keys (on a piano) that are in between the provided base_note to the next note
            present in COF. If base_note cannot be found from the list of notes in the COF, this function will return
            -1 instead.
        """
        if base_note in self.major_notes:
            base_note_index: int = self.major_notes.index(base_note)

            if self.B_MAJOR_NOTE_INDEX <= base_note_index <= self.B_FLAT_MAJOR_NOTE_INDEX:
                return self.TWO_BLACK_KEYS

            return self.THREE_BLACK_KEYS
        elif base_note in self.alternative_major_notes:
            base_note_index: int = self.alternative_major_notes.index(base_note)

            if self.C_FLAT_ALTERNATIVE_MAJOR_NOTE_INDEX <= base_note_index <= self.B_FLAT_ALTERNATIVE_MAJOR_NOTE_INDEX:
                return self.TWO_BLACK_KEYS

            return self.THREE_BLACK_KEYS
        elif base_note in self.minor_notes:
            base_note_index: int = self.minor_notes.index(base_note)

            if self.B_MINOR_NOTE_INDEX <= base_note_index <= self.B_FLAT_MINOR_NOTE_INDEX:
                return self.TWO_BLACK_KEYS

            return self.THREE_BLACK_KEYS
        elif base_note in self.alternative_minor_notes:
            base_note_index: int = self.alternative_minor_notes.index(base_note)

            if self.B_ALTERNATIVE_MINOR_NOTE_INDEX <= base_note_index <= self.A_SHARP_ALTERNATIVE_MINOR_NOTE_INDEX:
                return self.TWO_BLACK_KEYS

            return self.THREE_BLACK_KEYS

        return self.BASE_NOTE_NOT_FOUND
        
    def get_num_of_white_keys(self, base_note: str) -> int:
        """
        Gets the number of white keys (on a piano) that are in between the provided base_note and the next note present
        in COF.

        :param base_note: A note present in the COF.
        :return: The number of white keys (on a piano) that are in between the provided base_note to the next note
            present in COF. If base_note cannot be found from the list of notes in the COF, this function will return
            -1 instead.
        """
        if base_note in self.major_notes:
            base_note_index: int = self.major_notes.index(base_note)

            if self.B_MAJOR_NOTE_INDEX <= base_note_index <= self.B_FLAT_MAJOR_NOTE_INDEX:
                return self.FOUR_WHITE_KEYS

            return self.THREE_WHITE_KEYS
        elif base_note in self.alternative_major_notes:
            base_note_index: int = self.alternative_major_notes.index(base_note)

            if self.C_FLAT_ALTERNATIVE_MAJOR_NOTE_INDEX <= base_note_index <= self.B_FLAT_ALTERNATIVE_MAJOR_NOTE_INDEX:
                return self.FOUR_WHITE_KEYS

            return self.THREE_WHITE_KEYS
        elif base_note in self.minor_notes:
            base_note_index: int = self.minor_notes.index(base_note)

            if self.B_MINOR_NOTE_INDEX <= base_note_index <= self.B_FLAT_MINOR_NOTE_INDEX:
                return self.FOUR_WHITE_KEYS

            return self.THREE_WHITE_KEYS
        elif base_note in self.alternative_minor_notes:
            base_note_index: int = self.alternative_minor_notes.index(base_note)

            if self.B_ALTERNATIVE_MINOR_NOTE_INDEX <= base_note_index <= self.A_SHARP_ALTERNATIVE_MINOR_NOTE_INDEX:
                return self.FOUR_WHITE_KEYS

            return self.THREE_WHITE_KEYS

        return self.BASE_NOTE_NOT_FOUND
