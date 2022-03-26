class RhythmicPatternModel:
    collection_name: str = None
    rhythmic_pattern_objects: list = None

    def __init__(self, collection_name: str, rhythmic_pattern_objects: list):
        self.collection_name = collection_name
        self.rhythmic_pattern_objects = rhythmic_pattern_objects
