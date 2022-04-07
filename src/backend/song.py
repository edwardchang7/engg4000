import inspect,os,sys
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parent2 = os.path.dirname(parentdir)
sys.path.insert(0, parent2)


from webbrowser import get
from src.backend.song_builder import build_song_bridge, build_rhythmic_pattern, build_v2, build_verse, get_song_template
from src.backend.collections.abc_song import ABCSong

rhythm = build_rhythmic_pattern('CM')
verse = build_verse('CM', rhythm)

modulate = True #Set flag to add larger variation in bridge
bridge = build_song_bridge(verse, 'CM', modulate)

template = get_song_template()

song_list = []

for section in template:
    if section == "A":
        song_list += verse
    elif section == "C":
        song_list += bridge

key_abc = 'CM'.replace("M", "")
key_abc = 'CM'.replace("m", "")

v2 = build_v2('CM', verse)
song = ABCSong(key_abc, '4/4', [song_list, v2])
song_out = song.get_abc()
print(song_out)
