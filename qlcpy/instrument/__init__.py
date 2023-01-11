from ast import AST, parse
from io import StringIO
from typing import List, Optional
from unittest import mock

from .ProgramData import ProgramData
from .WalkNames import WalkNames
from .WalkFind import WalkFind
from .Instrumentor import Instrumentor
from .TransformForInstrumentor import TransformForInstrumentor

INSTRUMENT_NAME = '___i'
TEMPORARY_NAME = '___t'

def collect_elements(tree: AST) -> ProgramData:
  return WalkNames().walk(tree)

def find_nodes(tree: AST, class_names: List[str]) -> List[AST]:
  return WalkFind().walk(tree, class_names)

def transform(tree: AST, data: ProgramData, add: Optional[List[AST]]) -> AST:
  return TransformForInstrumentor(INSTRUMENT_NAME, TEMPORARY_NAME).transform(tree, data, add)

def run(
  transformed: AST,
  data: ProgramData,
  input: Optional[str] = None,
  run_main: bool = False,
) -> None:
  instrumentor = Instrumentor(data)
  locals = {
    '__name__': '__main__' if run_main else 'builtins',
    INSTRUMENT_NAME: instrumentor,
  }
  with mock.patch('builtins.input', side_effect=(input or '').split('\n')) as input, \
      mock.patch('sys.stdout', new_callable=StringIO) as output, \
      mock.patch('sys.stderr', new_callable=StringIO) as errors:
    exec(compile(transformed, '<string>', 'exec'), locals)
  return instrumentor

def run_with_instrumentor(
  tree: AST,
  call: Optional[List[AST]] = None,
  input: Optional[str] = None,
  run_main: bool = False,
) -> Instrumentor:
  data = collect_elements(tree)
  instrumented = transform(tree, data, call)
  return run(instrumented, data, input, run_main)

def parse_body(call: Optional[str]):
  if call:
    mod = parse(call)
    return mod.body
  return None
