from ast import (
  AST, Assign, BinOp, Call, Compare, Constant, Div, Eq, Gt, GtE, If, Load,
  Lt, LtE, Mod, Name, NotEq, While
)
from typing import List

from .WalkAST import WalkAST
from .trees import NodeStack

class LinePurpose():
  READ_INPUT = 'read_input'
  ZERO_DIV_GUARD = 'zero_div_guard'
  END_CONDITION = 'end_condition'
  EVEN_OR_ODD = 'even_or_odd'
  SUPPORTED_PURPOSES = [READ_INPUT, ZERO_DIV_GUARD, END_CONDITION, EVEN_OR_ODD]

  def __init__(self, line: int, purpose: str):
    self.line = line
    self.purpose = purpose
  
  def other_purposes(self):
    return list(k for k in self.SUPPORTED_PURPOSES if k != self.purpose)

class ProcedureScope():
  def __init__(self):
    self.loop_depth: int = 0
    self.breaked: bool = False
    self.top_cond: List[LinePurpose] = []
    self.top_loops_count: int = 0

class WalkLinePurposes(WalkAST):

  def __init__(self) -> None:
    self.purposes: List[LinePurpose] = []
    self.procedures: List[ProcedureScope] = [ProcedureScope()]

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
    if (
      type(node.op) == Mod and type(node.left) == Name
      and type(node.right) == Constant and node.right.value == 2
      and len(stack) >= 2 and type(stack[-1][0]) == Compare
      and type(stack[-2][0]) == If and stack[-2][1] == 'test'
    ):
      self.purposes.append(LinePurpose(node.lineno, LinePurpose.EVEN_OR_ODD))

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
  
  def enter_FunctionDef(self, stack: NodeStack, node: AST):
    self.procedures.append(ProcedureScope())

  def leave_FunctionDef(self, stack: NodeStack, node: While):
    self.unpack_proc(self.procedures.pop())

  def enter_For(self, stack: NodeStack, node: AST):
    self.procedures[-1].loop_depth += 1

  def leave_For(self, stack: NodeStack, node: AST):
    proc = self.procedures[-1]
    proc.loop_depth -= 1
    if proc.loop_depth == 0:
      proc.top_loops_count += 1
  
  def enter_While(self, stack: NodeStack, node: While):
    self.procedures[-1].loop_depth += 1

  def leave_While(self, stack: NodeStack, node: While):
    proc = self.procedures[-1]
    proc.loop_depth -= 1
    if proc.loop_depth == 0:
      proc.top_loops_count += 1
      if not proc.breaked and type(node.test) != Constant:
        proc.top_cond.append(LinePurpose(node.lineno, LinePurpose.END_CONDITION))

  def enter_Break(self, stack: NodeStack, node: AST):
    self.procedures[-1].breaked = True
  
  def enter_Return(self, stack: NodeStack, node: AST):
    self.procedures[-1].breaked = True
  
  def unpack_proc(self, proc: ProcedureScope):
    if len(proc.top_cond) == 1 and proc.top_loops_count == 1:
      self.purposes.append(proc.top_cond[0])

  def walk(self, tree: AST) -> List[LinePurpose]:
    self.purposes = []
    super().walk(tree)
    self.unpack_proc(self.procedures.pop())
    return self.purposes
