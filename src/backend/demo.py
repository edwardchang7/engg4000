from src.backend.collections.abc_song import ABCSong
from src.backend.song_builder import build_verse
from src.backend.song_builder import build_rhythmic_pattern

combined_rhythmic_pattern = build_rhythmic_pattern('CM')
verse = build_verse('CM', combined_rhythmic_pattern)
song = ABCSong('C', '4/4', verse)
output = song.get_abc()
print(output)
