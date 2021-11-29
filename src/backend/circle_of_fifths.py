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

    G_MAJOR_OR_E_MINOR_NOTE_INDEX = 1
    C_SHARP_MAJOR_OR_A_SHARP_NOTE_INDEX = 7
    F_MAJOR_OR_D_MINOR_NOTE_INDEX = 1
    B_MAJOR_OR_C_FLAT_MINOR_NOTE_INDEX = 7

    ZERO_SHARPS = 0

    INITIAL_NOTE_INDEX_VALUE = -1

    # Code -1 to signify that the provided note is not within a COF list
    BASE_NOTE_NOT_FOUND = -1
    BASE_KEY_NOT_FOUND = ()

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

    def get_perfect_cadence(self, base_key: str) -> tuple:
        """
        Gets the perfect cadence as a tuple, which the first index is the fifth of the provided base_key and the second
        index is the provided base_key. Returns an empty tuple if the provided base_key cannot be found from any of the
        COF lists.

        :param base_key: A key to get the perfect cadence with.
        :return: A tuple which the first index is the fifth of the provided base_key and the second index is the
            provided base_key. Returns an empty tuple instead if the provided base_key cannot be found from any of the
            COF lists.
        """
        if base_key in self.major_notes:
            base_key_index: int = self.major_notes.index(base_key)

            if base_key_index == len(self.major_notes) - 1:
                return self.major_notes[0], base_key

            return self.major_notes[base_key_index + 1], base_key
        elif base_key in self.minor_notes:
            base_key_index: int = self.minor_notes.index(base_key)

            if base_key_index == len(self.minor_notes) - 1:
                return self.minor_notes[0], base_key

            return self.minor_notes[base_key_index + 1], base_key

        return self.BASE_KEY_NOT_FOUND

    def get_num_of_sharps_in_note(self, note):
        """
        Gets the number of sharps in a COF note.

        :param note: The COF note to get the number of sharps from.
        :return: The number of sharps in the given COF note. If an incorrect COF note was provided, this method returns
            -1 instead.
        """
        note_index = self.INITIAL_NOTE_INDEX_VALUE

        if note in self.major_notes:
            note_index = self.major_notes.index(note)
        elif note in self.minor_notes:
            note_index = self.minor_notes.index(note)

        return self.__get_num_of_sharps(note_index)

    def get_num_of_flats_in_note(self, note):
        """
        Gets the number of flats in a COF note.

        :param note: The COF note to get the number of flats from.
        :return: The number of flats in the given COF note. If an incorrect COF note was provided, this method returns
            -1 instead.
        """
        note_index = self.INITIAL_NOTE_INDEX_VALUE
        cof_major_notes = self.__get_reversed_cof_list(self.major_notes)
        cof_minor_notes = self.__get_reversed_cof_list(self.minor_notes)

        if note in cof_major_notes:
            note_index = cof_major_notes.index(note)
        elif note in cof_minor_notes:
            note_index = cof_minor_notes.index(note)

        return self.__get_num_of_flats(note_index)

    def __get_num_of_sharps(self, note_index):
        if note_index == self.INITIAL_NOTE_INDEX_VALUE:
            return self.BASE_NOTE_NOT_FOUND
        elif self.G_MAJOR_OR_E_MINOR_NOTE_INDEX <= note_index <= self.C_SHARP_MAJOR_OR_A_SHARP_NOTE_INDEX:
            return note_index

        return self.ZERO_SHARPS

    def __get_num_of_flats(self, note_index):
        if note_index == self.INITIAL_NOTE_INDEX_VALUE:
            return self.BASE_NOTE_NOT_FOUND
        elif self.F_MAJOR_OR_D_MINOR_NOTE_INDEX <= note_index <= self.B_MAJOR_OR_C_FLAT_MINOR_NOTE_INDEX:
            return note_index

        return self.ZERO_SHARPS

    def __get_reversed_cof_list(self, cof_list):
        cof_list_copy = cof_list.copy()
        note = cof_list_copy.pop(0)
        cof_list_copy.append(note)
        cof_list_copy.reverse()
        return cof_list_copy
