from ast import (
  AST, Assign, BinOp, Call, Compare, Constant, Div, Eq, Gt, GtE, If, Load,
  Lt, LtE, Name, NotEq, While
)
from typing import List

from .WalkAST import WalkAST
from .trees import NodeStack

class LinePurpose():
  READ_INPUT = 'read_input'
  ZERO_DIV_GUARD = 'zero_div_guard'
  END_CONDITION = 'end_condition'
  SUPPORTED_PURPOSES = [READ_INPUT, ZERO_DIV_GUARD, END_CONDITION]

  def __init__(self, line: int, purpose: str):
    self.line = line
    self.purpose = purpose
  
  def other_purposes(self):
    return list(k for k in self.SUPPORTED_PURPOSES if k != self.purpose)

class LoopContents():
  def __init__(self):
    self.break_lines: List[int] = []

class WalkLinePurposes(WalkAST):

  def __init__(self) -> None:
    self.purposes: List[LinePurpose] = []
    self.loop_stack: List[LoopContents] = []

  def enter_Call(self, stack: NodeStack, node: Call) -> None:
    if (
      type(node.func) == Name and type(node.func.ctx) == Load and node.func.id == 'input'
      and any(type(parent) == Assign and field == 'value' for parent, field in stack)
    ):
      self.purposes.append(LinePurpose(node.lineno, LinePurpose.READ_INPUT))

  def enter_BinOp(self, stack: NodeStack, node: BinOp):
    if type(node.op) == Div and type(node.right) == Name and type(node.right.ctx) == Load:
      for parent, field in stack:
        if type(parent) == If and self.check_zero_guard(parent, field, node.right.id):
          self.purposes.append(LinePurpose(parent.lineno, LinePurpose.ZERO_DIV_GUARD))

  def check_zero_guard(self, node: If, field: str, variable: str) -> bool:
    if type(node.test) == Compare and len(node.test.comparators) == 1:
      left = node.test.left
      op = type(node.test.ops[0])
      right = node.test.comparators[0]
      if type(left) == Name and left.id == variable and type(right) == Constant:
        if field == 'orelse':
          return op == Eq and right.n == 0
        return any([
          op == NotEq and right.n == 0,
          op == Gt and right.n == 0,
          op == GtE and right.n == 1
        ])
      if type(left) == Constant and type(right) == Name and right.id == variable:
        if field == 'orelse':
          return op == Eq and left.n == 0
        return any([
          op == NotEq and left.n == 0,
          op == Lt and left.n == 0,
          op == LtE and left.n == 1
        ])
    return False
  
  def enter_While(self, stack: NodeStack, node: While):
    self.loop_stack.append(LoopContents())

  def enter_Break(self, stack: NodeStack, node: AST):
    for lc in self.loop_stack:
      lc.break_lines.append(node.lineno)
  
  def enter_Return(self, stack: NodeStack, node: AST):
    for lc in self.loop_stack:
      lc.break_lines.append(node.lineno)

  def leave_While(self, stack: NodeStack, node: While):
    contents = self.loop_stack.pop()
    if type(node.test) != Constant and len(contents.break_lines) == 0 and len(self.loop_stack) == 0:
      self.purposes.append(LinePurpose(node.lineno, LinePurpose.END_CONDITION))

  def walk(self, tree: AST) -> List[LinePurpose]:
    self.purposes = []
    super().walk(tree)
    return self.purposes
