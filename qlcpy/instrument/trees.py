from ast import AST, Call, Constant, Expr, List as AstList, Load, Name, Try, iter_child_nodes
from collections import deque
from typing import Any, Iterator, List, Optional, Tuple

NodeStack = List[Tuple[AST, str]]

def stack_add(stack: NodeStack, node: AST, field: str) -> NodeStack:
  return [*stack, (node, field)]

def stack_top(stack: NodeStack) -> AST:
  return stack[-1][0]

def stack_search(stack: NodeStack, types: List[str]) -> Iterator[AST]:
  for n, _ in reversed(stack):
    if n.__class__.__name__ in types:
      yield n

def wrap_in_try(*body: AST, fin: Optional[List[AST]] = None) -> AST:
  return Try(list(body), [], [], list(fin or []))

class ASTMethods:
  def _get_class_method(self, prefix: str, node: AST, default: Any) -> Any:
    return getattr(self, prefix + node.__class__.__name__, default)

def iter_tree(node: AST) -> Iterator[AST]:
  buf = deque([node])
  while buf:
    n = buf.popleft()
    for c in iter_child_nodes(n):
      buf.appendleft(c)
    yield n

def first_field(node: AST, fields: List[str]) -> List[AST]:
  for f in fields:
    v = getattr(node, f)
    if not v is None:
      return v if isinstance(v, list) else [v]
  return []