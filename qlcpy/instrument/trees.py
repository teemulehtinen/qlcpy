from ast import AST, Call, Constant, Expr, List as AstList, Load, Name, Try
from typing import Any, List, Optional, Tuple

NodeStack = List[Tuple[AST, str]]

def stack_add(stack: NodeStack, node: AST, field: str) -> NodeStack:
  return [*stack, (node, field)]

def wrap_in_try(*body: AST, fin: Optional[List[AST]] = None) -> AST:
  return Try(list(body), [], [], list(fin or []))

class ASTMethods:
  def _get_class_method(self, prefix: str, node: AST, default: Any) -> Any:
    return getattr(self, prefix + node.__class__.__name__, default)
