from ast import AST
from typing import List

from ..i18n import t
from ..instrument import find_nodes, Instrumentor, ProgramData
from ..models import ProgramInput, QLC, QLCPrepared
from .options import pick_options, options, fill_random_options

class LoopCount(QLCPrepared):
  def __init__(self, type: str, input: ProgramInput, element: ProgramData.Element):
    super().__init__(type)
    self.input = input
    self.loop = element

  def make(self):
    count = sum(1 for b in self.loop.evaluations if b == 0)
    if count > 10:
      return None
    return QLC(
      self.type,
      (
        t('q_loop_count_call', self.loop.declaration.lineno, str(self.input))
        if self.input else
        t('q_loop_count', self.loop.declaration.lineno)
      ),
      pick_options(
        options([count], 'correct_count', t('o_loop_count_correct'), True),
        fill_random_options(4, range(10), 'random_count', t('o_loop_count_random')),
      )
    )

def loop_count(
  type: str,
  tree: AST,
  input: ProgramInput,
  instrumentor: Instrumentor
) -> List[QLCPrepared]:
  return list(LoopCount(type, input, e) for e in instrumentor.data.elements_for_types('loop'))

def variable_trace(
  type: str,
  tree: AST,
  input: ProgramInput,
  instrumentor: Instrumentor
) -> List[QLCPrepared]:
  return []
