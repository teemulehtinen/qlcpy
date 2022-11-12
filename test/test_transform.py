import ast
import unittest

from pyqlc.instrument import collect_names, transform, run_with_instrumentor

class TestTransform(unittest.TestCase):

  def setUp(self) -> None:
    with open('test/sample_code.py', 'r') as f:
      src = f.read()
    self.tree = ast.parse(src)

  def test_names(self) -> None:
    data = collect_names(self.tree)
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
    data = collect_names(self.tree)
    instrumented = transform(self.tree, data, None)
    self.assertNotEqual(self.tree, instrumented)
    # TODO find some instrumentor nodes
    #import astpretty
    #astpretty.pprint(changed, show_offsets=False)
    #import astor
    #print(astor.to_source(instrumented))

  def test_run(self) -> None:
    instrumentor = run_with_instrumentor(self.tree, 'find_first_w', [['ah', 'beh', 'ceh'], 'b'])
    self.assertEqual(len(instrumentor.errors), 0)
    vars = list(instrumentor.data.elements_for_types(['variable']))
    self.assertEqual(len(vars), 2)
    self.assertEqual(vars[1].values, [0, 1])
  
  def test_run_for(self) -> None:
    instrumentor = run_with_instrumentor(self.tree, 'find_first', [['ah', 'beh', 'ceh'], 'b'])
    self.assertEqual(len(instrumentor.errors), 0)
    vars = list(instrumentor.data.elements_for_types(['variable']))
    self.assertEqual(len(vars), 2)
    self.assertEqual(vars[0].values, [0, 1, 2])
