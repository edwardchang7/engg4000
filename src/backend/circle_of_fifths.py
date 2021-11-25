class CircleOfFifths:
    # COF represented as lists
    major_notes: list = ['C', 'G', 'D', 'A', 'E', 'B', '_G', '_D', '_A', '_E', '_B', 'F']
    alternative_major_notes: list = ['C', 'G', 'D', 'A', 'E', '_C', '^F', '^C', '_A', '_E', '_B', 'F']
    minor_notes: list = ['a', 'e', 'b', '^f', '^c', '^g', '^d', '_b', 'f', 'c', 'g', 'd']
    alternative_minor_notes: list = ['a', 'e', 'b', '^f', '^c', '_a', '_e', '^a', 'f', 'c', 'g', 'd']

    # The number of sharps and flats BETWEEN two certain notes
    TWO_SHARPS = 2
    THREE_SHARPS = 3
    THREE_FLATS = 3
    FOUR_FLATS = 4

    # Index of a certain note within the COF lists above
    B_MAJOR_NOTE_INDEX = 5
    B_FLAT_MAJOR_NOTE_INDEX = 10
    C_FLAT_ALTERNATIVE_MAJOR_NOTE_INDEX = 5
    B_FLAT_ALTERNATIVE_MAJOR_NOTE_INDEX = 10
    B_MINOR_NOTE_INDEX = 2
    B_FLAT_MINOR_NOTE_INDEX = 7
    B_ALTERNATIVE_MINOR_NOTE_INDEX = 2
    A_SHARP_ALTERNATIVE_MINOR_NOTE_INDEX = 7

    # Code -1 to signify that the provided note is not within a COF list
    BASE_NOTE_NOT_FOUND = -1

    def get_cof(self, base_note: str) -> list:
        """
        Gets a COF list that is specifically based on the note passed as base_note. Each note in this COF list is the
        fifth note of its previous note.

        :param base_note: The first note within the COF list to get.
        :return: A COF list based on the provided base_note. Returns an empty list if an incorrect base_note was
            provided.
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

    def get_num_of_sharps_between_two_notes(self, base_note: str) -> int:
        """
        Gets the number of sharps BETWEEN the provided base_note and the next note present in the COF.

        :param base_note: A note present in the COF.
        :return: The number of sharps BETWEEN the provided base_note to the next note present in the COF. If base_note
            cannot be found from the list of notes in the COF, this function will return -1 instead.
        """
        if base_note in self.major_notes:
            base_note_index: int = self.major_notes.index(base_note)

            if self.B_MAJOR_NOTE_INDEX <= base_note_index <= self.B_FLAT_MAJOR_NOTE_INDEX:
                return self.TWO_SHARPS

            return self.THREE_SHARPS
        elif base_note in self.alternative_major_notes:
            base_note_index: int = self.alternative_major_notes.index(base_note)

            if self.C_FLAT_ALTERNATIVE_MAJOR_NOTE_INDEX <= base_note_index <= self.B_FLAT_ALTERNATIVE_MAJOR_NOTE_INDEX:
                return self.TWO_SHARPS

            return self.THREE_SHARPS
        elif base_note in self.minor_notes:
            base_note_index: int = self.minor_notes.index(base_note)

            if self.B_MINOR_NOTE_INDEX <= base_note_index <= self.B_FLAT_MINOR_NOTE_INDEX:
                return self.TWO_SHARPS

            return self.THREE_SHARPS
        elif base_note in self.alternative_minor_notes:
            base_note_index: int = self.alternative_minor_notes.index(base_note)

            if self.B_ALTERNATIVE_MINOR_NOTE_INDEX <= base_note_index <= self.A_SHARP_ALTERNATIVE_MINOR_NOTE_INDEX:
                return self.TWO_SHARPS

            return self.THREE_SHARPS

        return self.BASE_NOTE_NOT_FOUND
        
    def get_num_of_flats_between_two_notes(self, base_note: str) -> int:
        """
        Gets the number of flats BETWEEN the provided base_note and the next note present in the COF.

        :param base_note: A note present in the COF.
        :return: The number of flats BETWEEN the provided base_note to the next note present in the COF. If base_note
            cannot be found from the list of notes in the COF, this function will return -1 instead.
        """
        if base_note in self.major_notes:
            base_note_index: int = self.major_notes.index(base_note)

            if self.B_MAJOR_NOTE_INDEX <= base_note_index <= self.B_FLAT_MAJOR_NOTE_INDEX:
                return self.FOUR_FLATS

            return self.THREE_FLATS
        elif base_note in self.alternative_major_notes:
            base_note_index: int = self.alternative_major_notes.index(base_note)

            if self.C_FLAT_ALTERNATIVE_MAJOR_NOTE_INDEX <= base_note_index <= self.B_FLAT_ALTERNATIVE_MAJOR_NOTE_INDEX:
                return self.FOUR_FLATS

            return self.THREE_FLATS
        elif base_note in self.minor_notes:
            base_note_index: int = self.minor_notes.index(base_note)

            if self.B_MINOR_NOTE_INDEX <= base_note_index <= self.B_FLAT_MINOR_NOTE_INDEX:
                return self.FOUR_FLATS

            return self.THREE_FLATS
        elif base_note in self.alternative_minor_notes:
            base_note_index: int = self.alternative_minor_notes.index(base_note)

            if self.B_ALTERNATIVE_MINOR_NOTE_INDEX <= base_note_index <= self.A_SHARP_ALTERNATIVE_MINOR_NOTE_INDEX:
                return self.FOUR_FLATS

            return self.THREE_FLATS

        return self.BASE_NOTE_NOT_FOUND

    def get_perfect_cadence(self, base_key):
        if base_key in self.major_notes:
            base_key_index = self.major_notes.index(base_key)

            if base_key_index == len(self.major_notes) - 1:
                return base_key, self.major_notes[0]

            return base_key, self.major_notes[base_key_index + 1]
        elif base_key in self.minor_notes:
            base_key_index = self.minor_notes.index(base_key)

            if base_key_index == len(self.minor_notes) - 1:
                return base_key, self.minor_notes[0]

            return base_key, self.minor_notes[base_key_index + 1]
