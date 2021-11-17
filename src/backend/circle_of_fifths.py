class CircleOfFifths:
    major_notes: list = ['C', 'G', 'D', 'A', 'E', 'B', '_G', '_D', '_A', '_E', '_B', 'F']
    alternative_major_notes: list = ['C', 'G', 'D', 'A', 'E', '_C', '^F', '^C', '_A', '_E', '_B', 'F']
    minor_notes: list = ['a', 'e', 'b', '^f', '^c', '^g', '^d', '_b', 'f', 'c', 'g', 'd']
    alternative_minor_notes: list = ['a', 'e', 'b', '^f', '^c', '_a', '_e', '^a', 'f', 'c', 'g', 'd']

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

    def get_num_sharps(self, base_note: str) -> int:
        """
        Gets the number of sharps (or the number of black keys on a piano) from the provided base_note key to the
        next key present in 'circle of fifths'.

        :param base_note: A note present in the 'circle of fifths'.
        :return: The number of sharps (or the number of black keys on a piano) from the provided base_note to the next
            key present in 'circle of fifths'. If base_note cannot be found from the list of notes in the 'circle of
            fifths', this function will return -1 instead.
        """
        if base_note in self.major_notes:
            base_note_index: int = self.major_notes.index(base_note)
            if 5 <= base_note_index <= 10:
                return 2
            return 3
        elif base_note in self.alternative_major_notes:
            base_note_index: int = self.alternative_major_notes.index(base_note)
            if 5 <= base_note_index <= 10:
                return 2
            return 3
        elif base_note in self.minor_notes:
            base_note_index: int = self.minor_notes.index(base_note)
            if 2 <= base_note_index <= 7:
                return 2
            return 3
        elif base_note in self.alternative_minor_notes:
            base_note_index: int = self.alternative_minor_notes.index(base_note)
            if 2 <= base_note_index <= 7:
                return 2
            return 3
        return -1
        
    def get_num_flats(self, base_note: str) -> int:
        """
        Gets the number of flats (or the number of white keys on a piano) from the provided base_note key to the
        next key present in 'circle of fifths'.

        :param base_note: A note present in the 'circle of fifths'.
        :return: The number of flats (or the number of white keys on a piano) from the provided base_note to the next
            key present in 'circle of fifths'. If base_note cannot be found from the list of notes in the 'circle of
            fifths', this function will return -1 instead.
        """
        if base_note in self.major_notes:
            base_note_index: int = self.major_notes.index(base_note)
            if 5 <= base_note_index <= 10:
                return 4
            return 3
        elif base_note in self.alternative_major_notes:
            base_note_index: int = self.alternative_major_notes.index(base_note)
            if 5 <= base_note_index <= 10:
                return 4
            return 3
        elif base_note in self.minor_notes:
            base_note_index: int = self.minor_notes.index(base_note)
            if 2 <= base_note_index <= 7:
                return 4
            return 3
        elif base_note in self.alternative_minor_notes:
            base_note_index: int = self.alternative_minor_notes.index(base_note)
            if 2 <= base_note_index <= 7:
                return 4
            return 3

        return -1
