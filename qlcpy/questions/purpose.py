from ast import AST
from typing import List, Optional

from ..i18n import t
from ..instrument import search_line_purposes, Instrumentor
from ..models import QLC, QLCPrepared
from .options import pick_options, options, take_options, fill_options

class LinePurpose(QLCPrepared):
  def __init__(self, pos: int, type: str, line: int, purpose: str):
    super().__init__(pos, type)
    self.line = line
    self.purpose = purpose

  def make(self):
    return QLC(
      self.pos,
      self.type,
      t('q_line_purpose', self.line),
      pick_options(*[
        options(
          [t(f'o_line_purpose_{key}')],
          key,
          t('o_line_purpose_correct') if key == self.purpose else t('o_line_purpose_incorrect'),
          key == self.purpose
        ) for key in ['read_input', 'zero_div_guard', 'end_condition', 'ignores_input']
      ])
    )

def line_purpose(
  pos: int,
  type: str,
  tree: AST,
  call: Optional[str],
  ins: Instrumentor
) -> List[LinePurpose]:
  return list(
    LinePurpose(pos, type, p.line, p.purpose) for p in search_line_purposes(tree)
  )

# TODO variable_role
