from ast import AST
from typing import Callable, List, Optional

from ..instrument import Instrumentor
from ..models import QLCPrepared
from . import names, lines, purpose, dynamic

QLCMaker = Callable[[str, AST, Optional[str], Instrumentor], List[QLCPrepared]]

class QLCTemplate:
  def __init__(self, pos: int, type: str, description: str, maker: QLCMaker):
    self.pos = pos
    self.type = type
    self.description = description
    self.maker = maker

TEMPLATES: List[QLCTemplate] = [
  QLCTemplate(
    0,
    'VariableNames',
    'The variable names',
    names.variable_names,
  ),
  QLCTemplate(
    1,
    'LoopEnd',
    'The last line of a loop',
    lines.loop_end
  ),
  QLCTemplate(
    2,
    'VariableDeclaration',
    'The declaration line for a variable',
    lines.variable_declaration
  ),
  QLCTemplate(
    3,
    'ExceptSource',
    'A potential line to raise an error for an except-block',
    lines.except_source
  ),
  QLCTemplate(
    4,
    'LinePurpose',
    'A purpose of a line',
    purpose.line_purpose,
  ),
  QLCTemplate(
    5,
    'LoopCount',
    'The number of times that a loop was evaluated',
    dynamic.loop_count
  ),
  QLCTemplate(
    6,
    'VariableTrace',
    'The values that were assigned to a variable',
    dynamic.variable_trace
  ),
]
