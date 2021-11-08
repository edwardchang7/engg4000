import unittest
from src.backend.scales import get_scale

class TestScales(unittest.TestCase):

  def test_M_one(self):
    self.assertEqual(get_scale('C','M'), ['C', 'D', 'E', 'F', 'G', 'A', 'B', 'C'])
  
  def test_M_two(self):
    self.assertEqual(get_scale('D#','M'), ['D#', 'F', 'G', 'G#', 'A#', 'C', 'D', 'D#'])

  def test_M_three(self):
    self.assertEqual(get_scale('F','M'), ['F', 'G', 'A', 'A#', 'C', 'D', 'E', 'F'])

  def test_m_one(self):
    self.assertEqual(get_scale('G#','m'), ['G#', 'A#', 'B', 'C#', 'D#', 'E', 'F#', 'G#'])

  def test_m_two(self):
    self.assertEqual(get_scale('B','m'), ['B', 'C#', 'D', 'E', 'F#', 'G', 'A', 'B'])

  def test_m_three(self):
    self.assertEqual(get_scale('A#','m'), ['A#', 'C', 'C#', 'D#', 'F', 'F#', 'G#', 'A#'])

  def test_pM_one(self):
    self.assertEqual(get_scale('G','pM'), ['G', 'A', 'B', 'D', 'E'])

  def test_pM_two(self):
    self.assertEqual(get_scale('C#','pM'), ['C#', 'D#', 'F', 'G#', 'A#'])

  def test_pM_three(self):
    self.assertEqual(get_scale('E','pM'), ['E', 'F#', 'G#', 'B', 'C#'])

  def test_pm_one(self):
    self.assertEqual(get_scale('G#','pm'), ['G#', 'B', 'C#', 'D#', 'F#'])

  def test_pm_two(self):
    self.assertEqual(get_scale('B','pm'), ['B', 'D', 'E', 'F#', 'A'])

  def test_pm_three(self):
    self.assertEqual(get_scale('A#','pm'), ['A#', 'C#', 'D#', 'F', 'G#'])