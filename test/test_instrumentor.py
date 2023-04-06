import unittest

from qlcpy.instrument import Instrumentor, ProgramData

class TestInstrumentor(unittest.TestCase):

  def setUp(self) -> None:
    self.data = ProgramData()
    for v in ('a', 'b', 'i'):
      self.data.declare('variable', 0, v)
    self.ins = Instrumentor(self.data)

  def test_simple_assignment(self) -> None:
    a = self.ins.assignment([0], 7)
    self.assertEqual(a, 7)
    self.assertEqual(self.data.element_n(0).values, [7])

  def test_two_assignments(self) -> None:
    a = self.ins.assignment([0], 1)
    self.assertEqual(a, 1)
    a = self.ins.assignment([0], 10)
    self.assertEqual(a, 10)
    self.assertEqual(self.data.element_n(0).values, [1, 10])

  def test_unpack_assignment(self) -> None:
    a, b = self.ins.assignment([0, 1], (3, 4))
    self.assertEqual(a, 3)
    self.assertEqual(b, 4)
    self.assertEqual(self.data.element_n(0).values, [3])
    self.assertEqual(self.data.element_n(1).values, [4])

  def test_iteration(self) -> None:
    a, b, c = self.ins.iteration([2], range(3))
    self.assertEqual(a, 0)
    self.assertEqual(b, 1)
    self.assertEqual(c, 2)
    self.assertEqual(self.data.element_n(2).values, [0, 1, 2])

  def test_for_iteration(self) -> None:
    a = 0
    for i in self.ins.iteration([2], range(5)):
      a += i
    self.assertEqual(a, 10)
    self.assertEqual(self.data.element_n(2).values, [0, 1, 2, 3, 4])
