from src.backend.collections.abc_song import ABCSong
from src.backend.song_builder import build_verse
from src.backend.song_builder import build_rhythmic_pattern

combined_rhythmic_pattern = build_rhythmic_pattern('GM')
verse = build_verse('GM', combined_rhythmic_pattern)
song = ABCSong('G', '4/4', verse)
output = song.get_abc()
print(output)
