from ast import AST
from typing import List, Optional

from ..i18n import t
from ..instrument import Instrumentor, ProgramData
from ..models import QLC, QLCPrepared
from .options import pick_options, take_options, fill_options, random_order

WORD_LIST = ['total', 'other', 'foo', 'bar', 'n', 'tmp', 'magic', 'temp', 'important']

class VariableNames(QLCPrepared):
  def __init__(self, pos: int, type: str, data: ProgramData):
    super().__init__(pos, type)
    self.data = data

  def make(self):
    vars = list(self.data.elements_for_types(['variable']))
    kws = list(self.data.elements_for_types(['keyword']))
    bis = list(self.data.elements_for_types(['builtin']))
    uws = [w for w in WORD_LIST if self.data.element_for_id(w) is None]
    return QLC(
      self.pos,
      self.type,
      t('q_variable_names'),
      pick_options(
        take_options(2, random_order(e.id for e in vars), 'variable', t('o_variable_name'), True),
        fill_options(3, random_order(e.id for e in kws), 'reserved_word', t('o_reserved_word')),
        take_options(1, random_order(e.id for e in bis), 'builtin_function', t('o_built_in_function')),
        fill_options(5, random_order(uws), 'unused_word', t('o_unused_word')),
      )
    )

def variable_names(pos: int,
  type: str,
  tree: AST,
  call: Optional[str],
  ins: Instrumentor
) -> List[VariableNames]:
  if len(list(ins.data.elements_for_types(['variable']))) > 0:
    return [VariableNames(pos, type, ins.data)]
  return []
