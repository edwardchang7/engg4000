class NotePattern:

    # save memory space by defining the attributed beforehand
    __slots__ = ('note', 'length')
    
    def __init__(self, note, length):
        self.note = note
        self.length = length

    def __str__(self):
        return f"{self.note} : {self.length}"
