import inspect,os,sys, random
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parent2 = os.path.dirname(parentdir)
sys.path.insert(0, parent2)


from src.backend.song_builder import build_song_bridge, build_rhythmic_pattern, build_v2, build_verse, get_song_template
from src.backend.collections.abc_song import ABCSong

notes_to_pick = ['A', 'A#', 'B', 'C', 'C#',  'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
modifiers = ['M', 'm']

selected_note_index = random.randint(0,len(notes_to_pick) - 1)
selected_modifer_index = random.randint(0,len(modifiers) - 1)

key = notes_to_pick[selected_note_index] + modifiers[selected_modifer_index]

rhythm = build_rhythmic_pattern(key)
verse = build_verse(key, rhythm)

modulate = True #Set flag to add larger variation in bridge
bridge = build_song_bridge(verse, key, modulate)

template = get_song_template()

song_list = []

for section in template:
    if section == "A":
        song_list += verse
    elif section == "C":
        song_list += bridge

key_abc = key.replace("M", "")
key_abc = key.replace("m", "")

v2 = build_v2(key, verse)
song = ABCSong(key_abc, '4/4', [song_list, v2])
song_out = song.get_abc()

with open(song.title + ".abc", 'x') as f:
    f.write(song_out)

import os
os.startfile(song.title+ ".abc")