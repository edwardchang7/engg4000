'''
A class to hold a note and the length
'''

class Note_Pattern:
    
    def __init__(self, note:str, length:int):
        self.note = note
        self.length = length

    def __str__(self):
        return f"{self.note} : {self.length}"
