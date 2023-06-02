import unittest
import re
from typing import Any, List, Dict

from qlcpy import generate, QLCRequest, QLC

class TestQuestions(unittest.TestCase):
  RE_EM = '<em>([^<]+)</em>'
  RE_LINE = 'line (\d+)'

  @staticmethod
  def _get_part(question: str, regex: str) -> str:
    m = re.search(regex, question, re.IGNORECASE)
    return m.group(1) if m else None

  def _gen_qlcs(self, type: str, count: int = 100) -> List[QLC]:
    return generate(self.src, [QLCRequest(count, types=[type])], self.call)

  def _gen_a_qlc(self, type: str) -> QLC:
    qlcs = self._gen_qlcs(type, 1)
    self.assertEqual(len(qlcs), 1)
    return qlcs[0]
  
  def _test_qlcs(
    self,
    type: str,
    correct: Dict[Any, Any],
    question_regex: str,
    answer_types: bool = False
  ) -> None:
    qlcs = self._gen_qlcs(type)
    self.assertEqual(len(qlcs), len(correct.keys()))
    for qlc in qlcs:
      key = self._get_part(qlc.question, question_regex)
      answer = correct.get(self._get_part(qlc.question, question_regex))
      self.assertIsNotNone(answer, f'{qlc.question} -> {key}')
      for o in qlc.options:
        if o.correct:
          self.assertEqual(o.type if answer_types else o.answer, answer)
        else:
          self.assertNotEqual(o.type if answer_types else o.answer, answer)
    return qlcs

  def setUp(self) -> None:
    with open('test/sample_code.py', 'r') as f:
      self.src = f.read()
    self.call = 'find_first(["lorem", "ipsum", "dolor", "sit", "amet"], "s")'

  def test_variable_names(self):
    qlc = self._gen_a_qlc('VariableNames')
    for t in ['variable', 'reserved_word', 'builtin_function', 'unused_word']:
      self.assertTrue(all(o.correct == (t == 'variable') for o in qlc.options if o.type == t))

  def test_parameter_names(self):
    qlc = self._gen_a_qlc('ParameterNames')
    for t in ['parameter', 'function', 'variable', 'reserved_word']:
      self.assertTrue(all(o.correct == (t == 'parameter') for o in qlc.options if o.type == t))

  def test_loop_end(self):
    qlcs = self._test_qlcs('LoopEnd', { '5': 7, '13': 21, '27': 28 }, self.RE_LINE)

  def test_variable_declaration(self):
    cor = { 'i': 5, 's': 10, 'n': 11, 'word': 12, 'v': 16 }
    self._test_qlcs('VariableDeclaration', cor, self.RE_EM)

  def test_except_source(self):
    self._test_qlcs('ExceptSource', { '20': 16 }, self.RE_LINE)

  def test_line_purpose(self):
    cor = { '13': 'end_condition', '14': 'read_input', '17': 'even_or_odd', '23': 'zero_div_guard' }
    self._test_qlcs('LinePurpose', cor, self.RE_LINE, answer_types=True)

  def test_variable_role(self):
    cor = { 'f': 'dead', 'i': 'stepper', 's': 'gatherer', 'n': 'stepper', 'word': 'holder' }
    self._test_qlcs('VariableRole', cor, self.RE_EM, answer_types=True)

  def test_loop_count(self):
    self._test_qlcs('LoopCount', { '5': 4, '27': 0 }, self.RE_LINE)

  def test_variable_trace(self):
    self._test_qlcs('VariableTrace', { 'f': 'False', 'i': '0, 1, 2, 3' }, self.RE_EM)
