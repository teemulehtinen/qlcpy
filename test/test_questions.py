import unittest

from qlcpy import generate, QLCRequest, QLC

class TestQuestions(unittest.TestCase):

  def setUp(self) -> None:
    with open('test/sample_code.py', 'r') as f:
      self.src = f.read()
    self.call = 'find_first_w(["lorem", "ipsum", "dolor", "sit", "amet"], "s")'
  
  def _gen_a_qlc(self, type: str) -> QLC:
    qlcs = generate(self.src, [QLCRequest(1, types=[type])], self.call)
    self.assertEqual(len(qlcs), 1)
    return qlcs[0]

  def test_variable_names(self):
    qlc = self._gen_a_qlc('VariableNames')
    for t in ['variable', 'reserved_word', 'builtin_function', 'unused_word']:
      self.assertTrue(any(o.type == t and o.correct == (t == 'variable') for o in qlc.options))

  def test_loop_end(self):
    qlc = self._gen_a_qlc('LoopEnd')
    for o in qlc.options:
      self.assertEqual(o.correct, o.answer in (6, 13))

  def test_variable_declaration(self):
    qlc = self._gen_a_qlc('VariableDeclaration')
    d = 4 if '<em>i</em>' in qlc.question else 9
    for o in qlc.options:
      self.assertEqual(o.correct, o.answer == d)

  def test_loop_count(self):
    qlc = self._gen_a_qlc('LoopCount')
    n = 0 if 'Line 4' in qlc.question else 4
    for o in qlc.options:
      self.assertEqual(o.correct, o.answer == n)

  def test_variable_trace(self):
    qlc = self._gen_a_qlc('VariableTrace')
    for o in qlc.options:
      self.assertEqual(o.correct, o.answer == '0, 1, 2, 3')
