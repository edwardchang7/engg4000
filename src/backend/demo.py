import inspect,os,sys
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parent2 = os.path.dirname(parentdir)
sys.path.insert(0, parent2)


from src.backend.collections.abc_song import ABCSong
from src.backend.song_builder import build_verse
from src.backend.song_builder import build_rhythmic_pattern
from src.backend.song_builder import build_v2

combined_rhythmic_pattern = build_rhythmic_pattern('CM')
verse = build_verse('CM', combined_rhythmic_pattern)
v2 = build_v2('CM', verse)
song = ABCSong('C', '4/4', [verse, v2])
output = song.get_abc()
print(output)