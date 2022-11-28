from ast import AST, parse
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

def run(transformed: AST, data: ProgramData, input: Optional[str]) -> None:
  instrumentor = Instrumentor(data)
  with mock.patch('builtins.input', side_effect=(input or '').split('\n')):
    exec(compile(transformed, '<string>', 'exec'), { INSTRUMENT_NAME: instrumentor })
  return instrumentor

def run_with_instrumentor(
  tree: AST,
  call: Optional[List[AST]] = None,
  input: Optional[str] = None
) -> Instrumentor:
  data = collect_elements(tree)
  instrumented = transform(tree, data, call)
  return run(instrumented, data, input)

def parse_body(call: Optional[str]):
  if call:
    mod = parse(call)
    return mod.body
  return None
