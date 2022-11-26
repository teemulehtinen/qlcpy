import ast
import unittest

from qlcpy.instrument import collect_elements, transform, parse_body

class TestTmp(unittest.TestCase):

  def setUp(self) -> None:
    with open('test/sample_code.py', 'r') as f:
      src = f.read()
    self.tree = ast.parse(src)

  def test_names(self) -> None:
    call = "find_first(['ah','beh','ceg'], 'b')"
    data = collect_elements(self.tree)
    instrumented = transform(self.tree, data, parse_body(call))
    #import astpretty
    #astpretty.pprint(instrumented, show_offsets=False)
    import astor
    print(astor.to_source(instrumented))
