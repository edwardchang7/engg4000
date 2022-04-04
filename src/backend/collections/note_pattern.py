'''
A class to hold a note and the length
'''

class Note_Pattern:
    
    def __init__(self, note:str, length:int):
        self.note = note
        self.length = length

    def get_note(self):
        return self.note

    def get_length(self):
        return self.length

    def __str__(self):
        return f"{self.note} : {self.length}"
