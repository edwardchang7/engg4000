'''
A class to hold a tonal pattern
'''

class Tonal_Pattern:

    def __init__(self, pattern, num_notes, priority):
        # converts a string in the format of a list to an actual list object
        self.pattern = pattern
        self.priority = priority
        self.num_notes = num_notes

    '''
    toString method
    '''
    def __str__(self):
        return (f"Pattern: {self.pattern} \nnum_notes: {self.num_notes} \nPriority: {self.priority} \n")