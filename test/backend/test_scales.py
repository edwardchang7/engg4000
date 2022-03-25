import unittest
from src.backend.scales import get_scale

class TestScales(unittest.TestCase):

  def test_M_one(self):
    self.assertEqual(get_scale('C','M'), ['C', 'D', 'E', 'F', 'G', 'A', 'B', "c"])
  
  def test_M_two(self):
    self.assertEqual(get_scale('#D','M'), ['#D', 'F', 'G', '#G', '#A', "c", "d", "#d"])

  def test_M_three(self):
    self.assertEqual(get_scale('F','M'), ['F', 'G', 'A', '#A', "c", "d", "e", "f"])

  def test_m_one(self):
    self.assertEqual(get_scale('#G','m'), ['#G', '#A', 'B', "#c", "#d", "e", "#f", "#g"])

  def test_m_two(self):
    self.assertEqual(get_scale('B','m'), ['B', "#c", "d", "e", "#f", "g", "a", "b"])

  def test_m_three(self):
    self.assertEqual(get_scale('#A','m'), ['#A', "c", "#c", "#d", "f", "#f", "#g", "#a"])

  def test_pM_one(self):
    self.assertEqual(get_scale('G','pM'), ['G', 'A', 'B', "d", "e"])

  def test_pM_two(self):
    self.assertEqual(get_scale('#C','pM'), ['#C', '#D', 'F', '#G', '#A'])

  def test_pM_three(self):
    self.assertEqual(get_scale('E','pM'), ['E', '#F', '#G', 'B', "#c"])

  def test_pm_one(self):
    self.assertEqual(get_scale('#G','pm'), ['#G', 'B', "#c", "#d", "#f"])

  def test_pm_two(self):
    self.assertEqual(get_scale('B','pm'), ['B', "d", "e", "#f", "a"])

  def test_pm_three(self):
    self.assertEqual(get_scale('#A','pm'), ['#A', "#c", "#d", "f", "#g"])