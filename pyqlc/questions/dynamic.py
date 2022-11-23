from ast import AST
from typing import List

from ..i18n import t
from ..instrument import find_nodes, Instrumentor, ProgramData
from ..models import ProgramInput, QLC, QLCPrepared
from .options import pick_options, options, fill_random_options

def loop_count(
  type: str,
  tree: AST,
  input: ProgramInput,
  instrumentor: Instrumentor
) -> List[QLCPrepared]:
  return []

def variable_trace(
  type: str,
  tree: AST,
  input: ProgramInput,
  instrumentor: Instrumentor
) -> List[QLCPrepared]:
  return []
