from ast import AST, Call, Constant, Expr, List as AstList, Load, Name, Try
from typing import Any, List, Optional, Tuple

from ..primitives import as_primitive

NodeStack = List[Tuple[AST, str]]

def stack_add(stack: NodeStack, node: AST, field: str) -> NodeStack:
  return [*stack, (node, field)]

def wrap_in_try(*body: AST, fin: Optional[List[AST]] = None) -> AST:
  return Try(list(body), [], [], list(fin or []))

def as_constant(value: Any) -> AST:
  prims = as_primitive(value)
  if type(prims) == list:
    return AstList(list(Constant(p, None) for p in prims), Load())
  return Constant(prims, None)

def simple_call(name: str, args: List[Any]) -> AST:
  return Expr(Call(Name(name, Load()), list(as_constant(a) for a in args), []))

class ASTMethods:
  def _get_class_method(self, prefix: str, node: AST, default: Any) -> Any:
    return getattr(self, prefix + node.__class__.__name__, default)
