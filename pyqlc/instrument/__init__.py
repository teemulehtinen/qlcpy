from ast import AST
from typing import Any, List, Optional

from .ProgramData import ProgramData
from .WalkNames import WalkNames
from .WalkFind import WalkFind
from .Instrumentor import Instrumentor
from .TransformForInstrumentor import TransformForInstrumentor
from .trees import simple_call

INSTRUMENT_NAME = '___i'
TEMPORARY_NAME = '___t'

def collect_elements(tree: AST) -> ProgramData:
  return WalkNames().walk(tree)

def find_nodes(tree: AST, class_names: List[str]) -> List[AST]:
  return WalkFind().walk(tree, class_names)

def transform(tree: AST, data: ProgramData, call: Optional[AST]) -> AST:
  return TransformForInstrumentor(INSTRUMENT_NAME, TEMPORARY_NAME).transform(tree, data, call)

def run(transformed: AST, data: ProgramData) -> None:
  instrumentor = Instrumentor(data)
  exec(compile(transformed, '<string>', 'exec'), { INSTRUMENT_NAME: instrumentor })
  return instrumentor

def run_with_instrumentor(
  tree: AST,
  func: Optional[str] = None,
  args: Optional[List[Any]] = None
) -> Instrumentor:
  data = collect_elements(tree)
  instrumented = transform(tree, data, simple_call(func, args or []) if func else None)
  return run(instrumented, data)
