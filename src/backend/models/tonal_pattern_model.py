class TonalPatternModel:
    Key = None
    Pattern = None
    Octave_Change = None

    def __init__(self, key_value, pattern_value, octave_change_value):
        self.Key = key_value
        self.Pattern = pattern_value
        self.Octave_Change = octave_change_value
