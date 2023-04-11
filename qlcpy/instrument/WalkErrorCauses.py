from ast import AST, BinOp, Call, Div, ExceptHandler, Load, Name, Num, Raise, Set, Subscript, Try
from typing import List, Union

from .WalkAST import WalkAST
from .trees import NodeStack

class ErrorCause():
  def __init__(self, error: str, line: int, end_line: int):
    self.error = error
    self.line = line
    self.end_line = end_line

class ExceptAndCauses():
  def __init__(self, error: str, line: int, causes: List[ErrorCause]):
    self.error = error
    self.line = line
    self.causes = causes

class WalkErrorCauses(WalkAST):

  ERROR_MAPPINGS = {
    'ArithmeticError': ['OverflowError', 'ZeroDivisionError', 'FloatingPointError'],
    'LookupError': ['IndexError', 'KeyError'],
  }

  @classmethod
  def map_to_errors(cls, handler: ExceptHandler) -> List[str]:
    if not handler.type is None and type(handler.type) == Name:
      if handler.type.id in cls.ERROR_MAPPINGS:
        return cls.ERROR_MAPPINGS[handler.type.id]
      return [handler.type.id]
    return ['BaseException', 'Exception']

  def __init__(self) -> None:
    self.causes: List[ErrorCause] = []
    self.masked: List[List[str]] = []
    self.in_raise = False

  def append_cause(self, cause: ErrorCause) -> None:
    for m in self.masked:
      if 'Exception' in m or cause.error in m:
        return
    self.causes.append(cause)

  def enter_BinOp(self, stack: NodeStack, node: BinOp) -> None:
    if not self.masked and type(node.op) == Div and (
      type(node.right) != Num or node.right.n == 0
    ):
      self.causes.append(ErrorCause('ZeroDivisionError', node.lineno, node.end_lineno))

  def enter_Name(self, stack: NodeStack, node: Name) -> None:
    if type(node.ctx) == Load:
      self.causes.append(ErrorCause('NameError', node.lineno, node.end_lineno))

  def enter_Subscript(self, stack: NodeStack, node: Subscript) -> None:
    self.causes.append(ErrorCause('IndexError', node.lineno, node.end_lineno))
    self.causes.append(ErrorCause('KeyError', node.lineno, node.end_lineno))
    self.causes.append(ErrorCause('TypeError', node.lineno, node.end_lineno))

  def enter_Call(self, stack: NodeStack, node: Call) -> None:
    if type(node.func) == Name and type(node.func.ctx) == Load:
      if self.in_raise:
        self.append_cause(ErrorCause(node.func.id, node.lineno, node.end_lineno))
      elif node.func.id in ('float', 'int'):
        self.append_cause(ErrorCause('ValueError', node.lineno, node.end_lineno))
        self.append_cause(ErrorCause('TypeError', node.lineno, node.end_lineno))
      elif node.func.id in (
        'abs', 'all', 'any', 'bin', 'bool', 'chr', 'dict', 'id', 'len', 'list',
        'max', 'min', 'oct', 'ord', 'pow', 'range', 'repr', 'reversed', 'round',
        'set', 'slice', 'sorted', 'str', 'sum', 'tuple', 'zip'
      ):
        self.append_cause(ErrorCause('TypeError', node.lineno, node.end_lineno))
      elif not node.func.id in ('print'):
        self.append_cause(ErrorCause('Exception', node.lineno, node.end_lineno))

  def enter_Raise(self, stack: NodeStack, node: Raise) -> None:
    self.in_raise = True

  def leave_Raise(self, stack: NodeStack, node: Raise) -> None:
    self.in_raise = False

  def enter_Try(self, stack: NodeStack, node: Try) -> None:
    errors: Set[str] = set()
    for h in node.handlers:
      errors.update(self.map_to_errors(h))
    self.masked.append(list(errors))
  
  def leave_Try(self, stack: NodeStack, node: Try) -> None:
    self.masked.pop()

  def walk(self, tree: Union[AST, List[AST]]):
    for n in tree if isinstance(tree, list) else [tree]:
      self._visit([], n)
    return self.causes

  @classmethod
  def get_try_except_causes(cls, node: Try) -> List[ExceptAndCauses]:
    causes = cls().walk(node.body)
    def handled_causes(h: ExceptHandler):
      if h.type is None:
        return [
          *causes,
          cls.ErrorCause('BaseException', node.body[0].lineno, node.body[-1].end_lineno)
        ]
      if h.type.id == 'Exception':
        return causes
      handled = cls.ERROR_MAPPINGS.get(h.type.id, [h.type.id])
      return list(c for c in causes if c.error in handled)
    return list(
      ExceptAndCauses(h.type.id if h.type else '', h.lineno, handled_causes(h))
      for h in node.handlers
    )
