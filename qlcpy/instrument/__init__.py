from ast import AST, Try, parse
from io import StringIO
from typing import List, Optional
from unittest import mock

from .ProgramData import ProgramData
from .WalkNames import WalkNames
from .WalkNext import WalkNext
from .Instrumentor import Instrumentor
from .TransformForInstrumentor import TransformForInstrumentor
from .WalkFind import WalkFind
from .WalkErrorCauses import WalkErrorCauses, ExceptAndCauses
from .WalkLinePurposes import WalkLinePurposes, LinePurpose
from .VariableRole import VariableRole

INSTRUMENT_NAME = '___i'
TEMPORARY_NAME = '___t'

def collect_elements(tree: AST) -> ProgramData:
  return WalkNames().walk(tree)

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

def find_nodes(tree: AST, class_names: List[str]) -> List[AST]:
  return WalkFind().walk(tree, class_names)

def find_next(tree: AST, search: AST) -> Optional[AST]:
  return WalkNext().walk(tree, search)

def collect_error_causes(node: Try) -> List[ExceptAndCauses]:
  return WalkErrorCauses.get_try_except_causes(node)

def search_line_purposes(tree: AST) -> List[LinePurpose]:
  return WalkLinePurposes().walk(tree)

def analyse_variable_role(var: ProgramData.Element) -> VariableRole:
  return VariableRole(var)