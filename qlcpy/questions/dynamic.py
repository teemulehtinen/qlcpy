from ast import AST
from typing import List, Optional

from ..arrays import altered_arrays
from ..i18n import t
from ..instrument import Instrumentor, ProgramData
from ..models import QLC, QLCPrepared
from ..primitives import includes_references, primitives_to_str
from .options import pick_options, options, fill_options

class LoopCount(QLCPrepared):
  def __init__(
    self,
    pos: int,
    type: str,
    call: Optional[str],
    element: ProgramData.Element,
    scope: ProgramData.Element,
  ):
    super().__init__(pos, type)
    self.call = call
    self.loop = element
    self.scope = scope

  def make(self):
    if not self.scope is None and len(self.scope.evaluations) != 1:
      return None
    count = sum(1 for b in self.loop.evaluations if b == 0)
    return QLC(
      self.pos,
      self.type,
      (
        t('q_loop_count_call', self.loop.declaration.node.lineno, self.call)
        if self.call else
        t('q_loop_count', self.loop.declaration.node.lineno)
      ),
      pick_options(
        options([count], 'correct_count', t('o_loop_count_correct'), True),
        options([count + 1], 'one_off_count', t('o_loop_count_one_off')),
        fill_options(4, range(10), 'random_count', t('o_loop_count_random')),
      )
    )

def loop_count(
  pos: int,
  type: str,
  tree: AST,
  call: Optional[str],
  ins: Instrumentor
) -> List[QLCPrepared]:
  return list(
    LoopCount(
      pos,
      type,
      call,
      e,
      ins.data.element_for_scope(e.scope),
    ) for e in ins.data.elements_for_types(['loop'])
  )

class VariableTrace(QLCPrepared):
  def __init__(
    self,
    pos: int,
    type: str,
    call: Optional[str],
    element: ProgramData.Element,
    scope: ProgramData.Element,
    all: List[ProgramData.Element]
  ):
    super().__init__(pos, type)
    self.call = call
    self.variable = element
    self.scope = scope
    self.all = all
  
  def make(self):
    decl = self.variable.declaration
    vals = self.variable.values
    if (
      decl is None
      or len(vals) < 1
      or includes_references(vals)
      or (not self.scope is None and len(self.scope.evaluations) != 1)
    ):
      return None
    other = [
      o.values for o in self.all
      if o != self.variable and not includes_references(o.values)
    ]
    if len(vals) > 8:
      return QLC(
        self.pos,
        self.type,
        (
          t('q_variable_trace_start_call', decl.node.id, decl.node.lineno, self.call)
          if self.call else
          t('q_variable_trace_start', decl.node.id, decl.node.lineno)
        ),
        pick_options(
          options(
            [f'{primitives_to_str(vals[:4])}, ...'],
            'correct_trace',
            t('o_variable_trace_start_correct'),
            True
          ),
          fill_options(
            4,
            [
              f'{primitives_to_str(a)}, ...'
              for a in altered_arrays(vals[:4], other, True)
            ],
            'random_values',
            t('o_variable_trace_start_random')
          ),
        )
      )
    return QLC(
      self.pos,
      self.type,
      (
        t('q_variable_trace_call', decl.node.id, decl.node.lineno, self.call)
        if self.call else
        t('q_variable_trace', decl.node.id, decl.node.lineno)
      ),
      pick_options(
        options([primitives_to_str(vals)], 'correct_trace', t('o_variable_trace_correct'), True),
        options([primitives_to_str(vals[:-1])] if len(vals) > 1 else [], 'miss_value', t('o_variable_trace_miss')),
        fill_options(
          4,
          [
            primitives_to_str(a)
            for a in altered_arrays(vals, other)
          ],
          'random_values',
          t('o_variable_trace_random')
        ),
      )
    )

def variable_trace(
  pos: int,
  type: str,
  tree: AST,
  call: Optional[str],
  ins: Instrumentor
) -> List[VariableTrace]:
  vars = list(ins.data.elements_for_types(['variable']))
  return list(
    VariableTrace(
      pos,
      type,
      call,
      v,
      ins.data.element_for_scope(v.scope),
      vars
    ) for v in vars
  )
