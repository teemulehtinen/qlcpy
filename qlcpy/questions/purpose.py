import random
from ast import AST
from typing import List, Optional

from ..i18n import t
from ..instrument import (
  analyse_variable_role, Instrumentor, LinePurpose, ProgramData, search_line_purposes
)
from ..models import QLC, QLCPrepared
from .options import pick_options, options

class LinePurpose(QLCPrepared):
  def __init__(self, pos: int, type: str, lp: LinePurpose):
    super().__init__(pos, type)
    self.lp = lp

  def make(self):
    return QLC(
      self.pos,
      self.type,
      t('q_line_purpose', self.lp.line),
      pick_options(
        options([t(f'o_line_purpose_{self.lp.purpose}')], self.lp.purpose, t('o_correct'), True),
        *[
          options([t(f'o_line_purpose_{key}')], key, t('o_incorrect'))
          for key in random.sample(self.lp.other_purposes() + ['ignores_input'], 3)
        ]
      )
    )

def line_purpose(
  pos: int,
  type: str,
  tree: AST,
  call: Optional[str],
  ins: Instrumentor
) -> List[LinePurpose]:
  return list(LinePurpose(pos, type, lp) for lp in search_line_purposes(tree))

class VariableRole(QLCPrepared):
  def __init__(self, pos: int, type: str, variable: ProgramData.Element):
    super().__init__(pos, type)
    self.variable = variable

  def make(self):
    analysis = analyse_variable_role(self.variable)
    if (analysis.role == analysis.NONE):
      return None

    # Remove arguable options
    dis = analysis.other_roles()
    if analysis.role == analysis.STEPPER:
      dis.remove(analysis.GATHERER)
    elif analysis.role == analysis.GATHERER:
      dis.remove(analysis.STEPPER)

    return QLC(
      self.pos,
      self.type,
      t('q_variable_role', self.variable.id, self.variable.declaration.node.lineno),
      pick_options(
        options([t(f'o_variable_{analysis.role}')], analysis.role, t('o_correct'), True),
        *[
          options([t(f'o_variable_{key}')], key, t('o_incorrect'))
          for key in random.sample(dis, 3)
        ]
      )
    )

def variable_role(
    pos: int,
    type: str,
    tree: AST,
    call: Optional[str],
    ins: Instrumentor,
) -> List[VariableRole]:
  return list(VariableRole(pos, type, v) for v in ins.data.elements_for_types(['variable']))