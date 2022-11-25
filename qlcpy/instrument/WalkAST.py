from ast import AST, iter_fields

from .trees import ASTMethods, NodeStack, stack_add

class WalkAST(ASTMethods):

  def generic_enter(self, stack: NodeStack, node: AST) -> None:
    pass

  def generic_leave(self, stack: NodeStack, node: AST) -> None:
    pass

  def _visit(self, stack: NodeStack, node: AST) -> None:
    self._get_class_method('enter_', node, self.generic_enter)(stack, node)
    for field, value in iter_fields(node):
      n_stack = stack_add(stack, node, field)
      for item in value if isinstance(value, list) else [value]:
        if isinstance(item, AST):
          self._visit(n_stack, item)
    self._get_class_method('leave_', node, self.generic_leave)(stack, node)

  def walk(self, tree: AST) -> None:
    self._visit([], tree)
