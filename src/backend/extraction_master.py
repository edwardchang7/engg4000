import os

from src.backend.abc_tools import get_header
from src.backend.Collections.Song_Collection import Song_Collection
from src.backend.Collections.Tonal_Pattern import Tonal_Pattern
from src.backend.tonal_patterns import extract_tonal_patterns
from src.backend.cluster import Cluster
from src.backend.models.tonal_pattern_model import TonalPatternModel

def extract_patterns():

    song_list = []

    # the main dir 
    str_dir = 'mxl_to_abc/converted_compositions'

    count = 0

    # gets each file from the given directory
    directory = os.fsencode(str_dir)

    # for each file within the given directory, extract patterns from this
    for file in os.listdir(directory):

        patterns = []

        # gets the filename of the given file
        filename = os.fsdecode(file)

        # checks if hte given file ends with the right extension
        if filename.endswith('.abc'):

            # concat the directory with the file name
            file_path = str_dir + "/" + filename

            # extracts the header from the given abc file
            composition_name = get_header(file_path, 'T')
        
            # converts the header into a string if it returns a list
            actual_header = ""

            # replacing the name 
            composition_name=get_header(file_path, 'T')

            # converting list to a string header
            if type(composition_name) == list:
                for header in composition_name:
                    header = header.replace(" ", "_")
                    actual_header += str(header)
            else:
                actual_header = composition_name.replace(" ", "_")

            # creates the song object
            song = Song_Collection(actual_header)

            # appends the song object to the song_list
            song_list.append(song)

            patterns = extract_tonal_patterns(file_path)

            for item in patterns:

                pattern = Tonal_Pattern(item["Pattern"], item["num_notes"], item["Priority"])
                song.add_pattern(pattern)

    for song in song_list:

        database = Cluster("Thomas", song.song_name, False)
        v1,v2 = song.get_patterns()

        model = TonalPatternModel(song.song_name, v1)
        passed = database.insert_rhythmic_pattern_model(database, model)

        print(f"V1 of song {song.song_name} has been {str(passed).upper()} added")