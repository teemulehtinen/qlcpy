from ast import AST
from typing import Optional

from .WalkAST import WalkAST
from .trees import NodeStack

class WalkNext(WalkAST):
  
  def __init__(self) -> None:
    self.search: Optional[AST] = None
    self.take_flag: bool = False
    self.found: Optional[AST] = None

  def generic_leave(self, stack: NodeStack, node: AST) -> None:
    if node == self.search:
      self.take_flag = True

  def generic_enter(self, stack: NodeStack, node: AST) -> None:
    if self.take_flag and stack[-1][1] == 'body':
      self.take_flag = False
      self.found = node

  def walk(self, tree: AST, search: AST) -> Optional[AST]:
    self.search = search
    self.found = None
    super().walk(tree)
    return self.found
