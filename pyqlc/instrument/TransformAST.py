from ast import AST, fix_missing_locations, iter_fields
from copy import copy
from typing import Any

from .trees import ASTMethods, NodeStack, stack_add

class TransformAST(ASTMethods):

  def transform_item(self, stack: NodeStack, item: Any) -> Any:
    return self._transform(stack, item) if isinstance(item, AST) else item

  def transform_field(self, stack: NodeStack, value: Any) -> Any:
    if isinstance(value, list):
      return list(self.transform_item(stack, item) for item in value)
    return self.transform_item(stack, value)

  def transform_attr(self, stack: NodeStack, node: AST, field: str) -> Any:
    return self.transform_field(stack_add(stack, node, field), getattr(node, field))

  def generic_enter(self, stack: NodeStack, node: AST) -> AST:
    n = None
    for field, value in iter_fields(node):
      n_value = self.transform_field(stack_add(stack, node, field), value)
      if n_value != value:
        if n is None:
          n = copy(node)
        setattr(n, field, n_value)
    return n or node

  def generic_leave(self, stack: NodeStack, node: AST) -> AST:
    return node

  def _transform(self, stack: NodeStack, node: AST) -> AST:
    n = self._get_class_method('enter_', node, self.generic_enter)(stack, node)
    return self._get_class_method('leave_', n, self.generic_leave)(stack, n)

  def transform(self, tree: AST) -> AST:
    root = self._transform([], tree)
    fix_missing_locations(root)
    return root
