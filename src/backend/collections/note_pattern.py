'''
A class to hold a note and the length
'''

class Note_Pattern:

    # save memory space by defining the attributed beforehand
    __slots__ = ('note', 'length')
    
    def __init__(self, note:str, length:int):
        self.note = note
        self.length = length

    def __str__(self):
        return f"{self.note} : {self.length}"
