notes = ['C', 'C#', 'D', 'D#', 'E', 'F',  'F#', 'G', 'G#', 'A', 'A#', 'B']

def halfStep(inputNote):
  for i in range(len(notes)):
    if inputNote==notes[i]:
      index=(i+1)%(len(notes))
      return notes[index]

def wholeStep(inputNote):
  for i in range(len(notes)):
    if inputNote==notes[i]:
      index=(i+2)%(len(notes))
      return notes[index]
