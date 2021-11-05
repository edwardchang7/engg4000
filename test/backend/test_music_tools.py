from src.backend.music_tools import whole_step,half_step,M3,m3,P5,change_octave

def test_halfStep_increasingFreq_one():
  assert half_step("A", True)=="A#"
  
def test_halfStep_increasingFreq_two():
  assert half_step("B", True)=="c'"

def test_halfStep_increasingFreq_three():
  assert half_step("D#,", True)=="E,"


def test_halfStep_decreasingFreq_one():
  assert half_step("c'", False) == "B"

def test_halfStep_decreasingFreq_two():
  assert half_step("A", False) == "G#"

def test_halfStep_decreasingFreq_three():
  assert half_step("F,", False) == "E,"


def test_wholeStep_increasingFreq_one():
  assert whole_step("E", True)=="F#"

def test_wholeStep_increasingFreq_two():
  assert whole_step("B", True)=="c#'"

def test_wholeStep_increasingFreq_three():
  assert whole_step("D,", True)=="E,"


def test_wholeStep_decreasingFreq_one():
  assert whole_step("c'", False)=="A#"

def test_wholeStep_decreasingFreq_two():
  assert whole_step("B", False)=="A"

def test_wholeStep_decreasingFreq_three():
  assert whole_step("F#,", False)=="E,"


def test_M3_increasingFreq_one():
  assert M3("C", True)=="E"

def test_M3_increasingFreq_two():
  assert M3("A#", True)=="d'"

def test_M3_increasingFreq_three():
  assert M3("b'", True)=="d#''"


def test_M3_decreasingFreq_one():
  assert M3("c'", False)=="G#"

def test_M3_decreasingFreq_two():
  assert M3("E", False)=="C"

def test_M3_decreasingFreq_three():
  assert M3("F#,", False)=="D,"


def test_m3_increasingFreq_one():
  assert m3("E", True)=="G"

def test_m3_increasingFreq_two():
  assert m3("c'", True)=="d#'"

def test_m3_increasingFreq_three():
  assert m3("F,", True)=="G#,"


def test_m3_decreasingFreq_one():
  assert m3("C,", False)=="A,,"

def test_m3_decreasingFreq_two():
  assert m3("d''", False)=="b'"

def test_m3_decreasingFreq_three():
  assert m3("E", False)=="C#"


def test_P5_increasingFreq_one():
  assert P5("C", True)=="G"

def test_P5_increasingFreq_two():
  assert P5("F#", True)=="c#'"

def test_P5_increasingFreq_three():
  assert P5("A,", True)=="E"


def test_P5_decreasingFreq_one():
  assert P5("A#,", False)=="D#,"

def test_P5_decreasingFreq_two():
  assert P5("D", False)=="G,"

def test_P5_decreasingFreq_three():
  assert P5("e'", False)=="A"


def test_changeOctave_increasingFreq_one():
  assert change_octave("C", True)=="c'"

def test_changeOctave_increasingFreq_two():
  assert change_octave("g#'", True)=="g#''"

def test_changeOctave_increasingFreq_three():
  assert change_octave("A,", True)=="A"


def test_changeOctave_decreasingFreq_one():
  assert change_octave("A#,", False)=="A#,,"

def test_changeOctave_decreasingFreq_two():
  assert change_octave("D", False)=="D,"

def test_changeOctave_decreasingFreq_three():
  assert change_octave("e'", False)=="E"
