import ast
import unittest

from qlcpy.instrument import collect_elements, transform, run_with_instrumentor, parse_body

class TestTransform(unittest.TestCase):

  def setUp(self) -> None:
    with open('test/sample_code.py', 'r') as f:
      src = f.read()
    self.tree = ast.parse(src)

  def test_names(self) -> None:
    data = collect_elements(self.tree)
    self.assertEqual(
      list((e.scope, e.id) for e in data.elements_for_types(['function'])),
      [(0, 'find_first'), (0, 'find_first_w')]
    )
    self.assertEqual(
      list((e.scope, e.id) for e in data.elements_for_types(['argument', 'variable'])),
      [
        (1, 'words_list'), (1, 'initial'), (1, 'i'),
        (2, 'words_list'), (2, 'initial'), (2, 'i')
      ]
    )
  
  def test_transform(self) -> None:
    data = collect_elements(self.tree)
    instrumented = transform(self.tree, data, None)
    self.assertNotEqual(self.tree, instrumented)

  def test_run(self) -> None:
    call = "find_first_w(['ah', 'beh', 'ceh'], 'b')"
    instrumentor = run_with_instrumentor(self.tree, parse_body(call))
    self.assertEqual(len(instrumentor.errors), 0)
    vars = list(instrumentor.data.elements_for_types(['variable']))
    self.assertEqual(len(vars), 2)
    self.assertEqual(vars[1].values, [0, 1])
  
  def test_run_for(self) -> None:
    call = "find_first(['ah', 'beh', 'ceh'], 'b')"
    instrumentor = run_with_instrumentor(self.tree, parse_body(call))
    self.assertEqual(len(instrumentor.errors), 0)
    vars = list(instrumentor.data.elements_for_types(['variable']))
    self.assertEqual(len(vars), 2)
    self.assertEqual(vars[0].values, [0, 1, 2])

  def test_input(self) -> None:
    tree = ast.parse(
"""
run = True
while run:
  line = input('Read stdin')
  run = line != 'end'
"""
    )
    instrumentor = run_with_instrumentor(tree, input="line1\nline2\nend\n")
    line = instrumentor.data.element_for_id('line')
    self.assertEqual(line.values, ['line1', 'line2', 'end'])
