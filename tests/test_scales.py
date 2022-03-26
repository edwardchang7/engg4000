from ..utils.scales import getScale

def test_M_one():
  assert getScale('C','M') == ['C', 'D', 'E', 'F', 'G', 'A', 'B', 'C']
  
def test_M_two():
  assert getScale('D#','M') == ['D#', 'F', 'G', 'G#', 'A#', 'C', 'D', 'D#']

def test_M_three():
  assert getScale('F','M') == ['F', 'G', 'A', 'A#', 'C', 'D', 'E', 'F']

def test_m_one():
  assert getScale('G#','m') == ['G#', 'A#', 'B', 'C#', 'D#', 'E', 'F#', 'G#']

def test_m_two():
  assert getScale('B','m') == ['B', 'C#', 'D', 'E', 'F#', 'G', 'A', 'B']

def test_m_three():
  assert getScale('A#','m') == ['A#', 'C', 'C#', 'D#', 'F', 'F#', 'G#', 'A#']

def test_pM_one():
  assert getScale('G','pM') == ['G', 'A', 'B', 'D', 'E']

def test_pM_two():
  assert getScale('C#','pM') == ['C#', 'D#', 'F', 'G#', 'A#']

def test_pM_three():
  assert getScale('E','pM') == ['E', 'F#', 'G#', 'B', 'C#']

def test_pm_one():
  assert getScale('G#','pm') == ['G#', 'B', 'C#', 'D#', 'F#']

def test_pm_two():
  assert getScale('B','pm') == ['B', 'D', 'E', 'F#', 'A']

def test_pm_three():
  assert getScale('A#','pm') == ['A#', 'C#', 'D#', 'F', 'G#']