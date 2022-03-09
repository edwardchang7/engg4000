class SongBuilder:
    def build_new_pattern(self, first_existing_pattern: list, second_existing_pattern: list, desired_num_of_beats: int) -> list:
        int num_of_beats_in_first_pattern = len(first_existing_pattern)
        int num_of_beats_in_second_pattern = len(second_existing_pattern)

        int num_of_beats_in_new_pattern = desired_num_of_beats - num_of_beats_in_first_pattern - num_of_beats_in_second_pattern
        if num_of_beats_in_new_pattern < 0:
            return None
        else if num_of_beats_in_new_pattern == 0:
            return combine_patterns(first_existing_pattern, second_existing_pattern)
        else
            # find common scale
            # return new pattern
        
    def combine_patterns(self, first_pattern: list, second_pattern: list) -> list:
        return first_pattern + second_pattern

    def get_intro():
    def get_verse():
    def get_prechorus():
    def get_chorus():
    def get_bridge():
    def get_outro():