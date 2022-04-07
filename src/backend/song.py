from webbrowser import get
from src.backend.song_builder import build_song_bridge, build_rhythmic_pattern, build_verse, get_song_template
from src.backend.collections.abc_song import ABCSong

def create_new_song(key: str):
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

    song = ABCSong(key_abc, '4/4', song_list)
    song_out = song.get_abc()

    return song_out

