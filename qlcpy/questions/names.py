from ast import AST, FunctionDef
from typing import List, Optional

from ..i18n import t
from ..instrument import Instrumentor, ProgramData
from ..models import QLC, QLCPrepared
from .options import pick_options, options, take_options, fill_options

WORD_LIST = ['total', 'other', 'foo', 'bar', 'n', 'tmp', 'magic', 'temp', 'important']

class VariableNames(QLCPrepared):
  def __init__(self, pos: int, type: str, data: ProgramData):
    super().__init__(pos, type)
    self.data = data

  def make(self):
    vars = list(self.data.elements_for_types(['variable']))
    if len(vars) == 0:
      return None
    kws = list(self.data.elements_for_types(['keyword']))
    bis = list(self.data.elements_for_types(['builtin']))
    uws = [w for w in WORD_LIST if self.data.element_for_id(w) is None]
    return QLC(
      self.pos,
      self.type,
      t('q_variable_names'),
      pick_options(
        take_options(2, [e.id for e in vars], 'variable', t('o_variable_name'), True),
        fill_options(3, [e.id for e in kws], 'reserved_word', t('o_reserved_word')),
        take_options(1, [e.id for e in bis], 'builtin_function', t('o_built_in_function')),
        fill_options(5, uws, 'unused_word', t('o_unused_word')),
      )
    )

def variable_names(
  pos: int,
  type: str,
  tree: AST,
  call: Optional[str],
  ins: Instrumentor
) -> List[VariableNames]:
  return [VariableNames(pos, type, ins.data)]

class ParameterNames(QLCPrepared):
  def __init__(self, pos: int, type: str, data: ProgramData, function: ProgramData.Element):
    super().__init__(pos, type)
    self.data = data
    self.function = function

  def make(self):
    args = list(self.data.elements_in_scope(self.function.container_scope, ['argument']))
    if len(args) == 0:
      return None
    vars = list(self.data.elements_in_scope(self.function.container_scope, ['variable']))
    kws = list(self.data.elements_for_types(['keyword']))
    return QLC(
      self.pos,
      self.type,
      t('q_parameter_names', self.function.declaration.node.lineno),
      pick_options(
        take_options(2, [e.id for e in args], 'parameter', t('o_parameter_name'), True),
        options([self.function.id], 'function', t('o_function_name')),
        take_options(2, [e.id for e in vars], 'variable', t('o_variable_name')),
        fill_options(5, [e.id for e in kws], 'reserved_word', t('o_reserved_word')),
      )
    )

def parameter_names(
  pos: int,
  type: str,
  tree: AST,
  call: Optional[str],
  ins: Instrumentor
) -> List[ParameterNames]:
  return [ParameterNames(pos, type, ins.data, e) for e in ins.data.elements_for_types(['function'])]
