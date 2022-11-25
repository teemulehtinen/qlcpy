from ast import AST
from typing import Callable, List, Optional

from ..instrument import Instrumentor
from ..models import QLCPrepared
from . import lines, dynamic

QLCMaker = Callable[[str, AST, Optional[str], Instrumentor], List[QLCPrepared]]

class QLCTemplate:
  def __init__(self, type: str, description: str, maker: QLCMaker):
    self.type = type
    self.description = description
    self.maker = maker

TEMPLATES: List[QLCTemplate] = [
  QLCTemplate(
    'LoopEnd',
    'The last line of a loop',
    lines.loop_end
  ),
  QLCTemplate(
    'VariableDeclaration',
    'The declaration line for a variable',
    lines.variable_declaration
  ),
  QLCTemplate(
    'LoopCount',
    'The number of times that a loop was evaluated',
    dynamic.loop_count
  ),
  QLCTemplate(
    'VariableTrace',
    'The values that were assigned to a variable',
    dynamic.variable_trace
  ),
]
