from ast import AST
from typing import Any, List, Optional

from ..arrays import random_steps
from ..i18n import t
from ..instrument import find_nodes, Instrumentor, ProgramData
from ..models import QLC, QLCPrepared
from ..primitives import primitive_to_str
from .options import pick_options, options, fill_random_options

class LoopCount(QLCPrepared):
  def __init__(self, type: str, call: Optional[str], element: ProgramData.Element):
    super().__init__(type)
    self.call = call
    self.loop = element

  def make(self):
    count = sum(1 for b in self.loop.evaluations if b == 0)
    if count > 10:
      return None
    return QLC(
      self.type,
      (
        t('q_loop_count_call', self.loop.declaration.lineno, self.call)
        if self.call else
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
  call: Optional[str],
  ins: Instrumentor
) -> List[QLCPrepared]:
  return list(LoopCount(type, call, e) for e in ins.data.elements_for_types('loop'))

class VariableTrace(QLCPrepared):
  def __init__(self, type: str, call: Optional[str], element: ProgramData.Element, seeds: List[Any]):
    super().__init__(type)
    self.call = call
    self.variable = element
    self.seeds = seeds
  
  def make(self):
    decl = self.variable.declaration
    vals = self.variable.values
    if decl is None or len(vals) > 5:
      return None
    return QLC(
      self.type,
      (
        t('q_variable_trace_call', decl.id, decl.lineno, self.call)
        if self.call else
        t('q_variable_trace', decl.id, decl.lineno)
      ),
      pick_options(
        options([primitive_to_str(vals)], 'correct_trace', t('o_variable_trace_correct'), True),
        options(
          [primitive_to_str(vals[:-1])] if len(vals) > 1 else [],
          'miss_value',
          t('o_variable_trace_miss')
        ),
        fill_random_options(
          4,
          [primitive_to_str(a) for a in random_steps(vals, self.seeds)],
          'random_values',
          t('o_variable_trace_random')
        ),
      )
    )

def variable_trace(
  type: str,
  tree: AST,
  call: Optional[str],
  ins: Instrumentor
) -> List[VariableTrace]:
  seeds = list(n.value for n in find_nodes(tree, ['Constant']))
  return list(VariableTrace(type, call, e, seeds) for e in ins.data.elements_for_types('variable'))
