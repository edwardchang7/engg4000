class NotePattern:

    # save memory space by defining the attributed beforehand
    __slots__ = ('note', 'length')
    
    def __init__(self, note:str, length:str):
        self.note = note
        self.length = length

    def __str__(self):
        '''
        toString function
        '''
        return f"{self.note} : {self.length}"
