'''
A class to hold a tonal pattern
'''

class TonalPattern:
    def __init__(self, pattern: list, num_of_notes: int, priority: int):
        self.pattern = pattern
        self.priority = priority
        self.num_of_notes = num_of_notes

    def __str__(self):
        return f"pattern: {self.pattern}\nnum_notes: {self.num_of_notes}\npriority: {self.priority}\n"
