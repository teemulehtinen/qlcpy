from typing import List

from .QLCPreparer import QLCPreparer
from . import lines, dynamic

class QLCTemplate:
  def __init__(self, type: str, description: str, preparer: QLCPreparer):
    self.type = type
    self.description = description
    self.preparer = preparer

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
