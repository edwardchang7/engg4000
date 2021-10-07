import musicalbeeps

player = musicalbeeps.Player(volume=1, mute_output=False)
file_name = "tetris.txt"
music_sheet = open(f"music_sheets/{file_name}", "r")

lines = music_sheet.readlines()
note_count = 0
for line in lines:
    note_count += 1
    line = line.split(":")
    note = line[0].strip()
    duration = line[1].strip()
    player.play_note(note, float(duration))

print(f"There are a total of {note_count} notes in {file_name} music sheet.")
