from ast import AST
from typing import List

from .WalkAST import WalkAST
from .trees import NodeStack

class WalkFind(WalkAST):
  
  def __init__(self) -> None:
    self.class_names: List[str] = []
    self.found: List[AST] = []

  def generic_enter(self, stack: NodeStack, node: AST) -> None:
    if node.__class__.__name__ in self.class_names:
      self.found.append(node)

  def walk(self, tree: AST, class_names: List[str]) -> List[AST]:
    self.class_names = class_names
    self.found = []
    super().walk(tree)
    return self.found
