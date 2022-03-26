from ..utils.music_tools import wholeStep,halfStep

def test_halfStep_one():
  assert halfStep("A")=="A#"
  
def test_halfStep_two():
  assert halfStep("G#")=="A"

def test_halfStep_three():
  assert halfStep("B")=="C"

def test_wholeStep_one():
  assert wholeStep("E")=="F#"

def test_wholeStep_two():
  assert wholeStep("G")=="A"

def test_wholeStep_three():
  assert wholeStep("B")=="C#"

