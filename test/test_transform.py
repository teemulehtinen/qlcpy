import ast
import unittest

from qlcpy.instrument import collect_elements, transform, run_with_instrumentor, parse_body
from qlcpy.primitives import Primitive

def read_ast(file):
  with open(file, 'r') as f:
    return ast.parse(f.read())

class TestTransform(unittest.TestCase):

  def setUp(self) -> None:
    self.tree = read_ast('test/sample_code.py')
    self.issues_tree = read_ast('test/issues_code.py')

  def test_names(self) -> None:
    data = collect_elements(self.tree)
    self.assertEqual(
      list((e.scope, e.id) for e in data.elements_for_types(['function'])),
      [(0, 'find_first'), (0, 'count_average_of_even')]
    )
    self.assertEqual(
      list((e.scope, e.id) for e in data.elements_for_types(['argument', 'variable'])),
      [
        (1, 'words_list'), (1, 'initial'), (1, 'f'), (1, 'i'),
        (2, 's'), (2, 'n'), (2, 'word'), (2, 'v')
      ]
    )
  
  def test_transform(self) -> None:
    data = collect_elements(self.tree)
    instrumented = transform(self.tree, data, None)
    self.assertNotEqual(self.tree, instrumented)

  def test_issues(self) -> None:
    data = collect_elements(self.issues_tree)
    instrumented = transform(self.issues_tree, data, None)
    self.assertNotEqual(self.issues_tree, instrumented)

  def test_run(self) -> None:
    call = "find_first(['ah', 'beh', 'ceh'], 'b')"
    instrumentor = run_with_instrumentor(self.tree, parse_body(call))
    self.assertEqual(len(instrumentor.errors), 0)
    vars = list(instrumentor.data.elements_for_types(['variable']))
    self.assertEqual(vars[1].values, [0, 1])
  
  def test_input(self) -> None:
    call = "count_average_of_even()"
    instrumentor = run_with_instrumentor(self.tree, parse_body(call), '4\n8\n\n')
    self.assertEqual(len(instrumentor.errors), 0)
    vars = list(instrumentor.data.elements_for_types(['variable']))
    self.assertEqual(vars[2].values, [0, 4, 12])
    self.assertEqual(vars[4].values, [None, '4', '8', ''])

