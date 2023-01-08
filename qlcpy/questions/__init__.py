from ast import AST
from typing import Callable, List, Optional

from ..instrument import Instrumentor
from ..models import QLCPrepared
from . import lines, dynamic

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
    'LoopEnd',
    'The last line of a loop',
    lines.loop_end
  ),
  QLCTemplate(
    1,
    'VariableDeclaration',
    'The declaration line for a variable',
    lines.variable_declaration
  ),
  QLCTemplate(
    2,
    'LoopCount',
    'The number of times that a loop was evaluated',
    dynamic.loop_count
  ),
  QLCTemplate(
    3,
    'VariableTrace',
    'The values that were assigned to a variable',
    dynamic.variable_trace
  ),
]
