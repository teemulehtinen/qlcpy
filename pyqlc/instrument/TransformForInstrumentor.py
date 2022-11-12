from ast import (
  AnnAssign, AST, Assign, Attribute, BinOp, Call, Constant, Del, Delete,
  For, FunctionDef, Load, List as ASTList, Module, Name, Store
)
from typing import List, Optional

from .TransformAST import TransformAST, NodeStack
from .ProgramData import ProgramData
from .trees import wrap_in_try

class TransformForInstrumentor(TransformAST):

  def __init__(
    self,
    ins_name: str,
    tmp_name: str,
  ) -> None:
    self.ins_name = ins_name
    self.tmp_name = tmp_name
    self.data: Optional[ProgramData] = None
    self.call: Optional[AST] = None

  def ins(self, method: str, *args: AST) -> AST:
    return Call(
      Attribute(Name(self.ins_name, Load()), method, Load()),
      list(args),
      []
    )

  def target(self, node: AST) -> AST:
    # TODO handle Subscript/Attribute in target?
    return ASTList(
      list(
        Constant(i, None) for i, _ in [
          self.data.element_for_node(el, ['function', 'variable', 'argument']) for el in (
            node.elts if node.__class__.__name__ in ('Tuple', 'List') else [node]
          )
        ]
      ),
      Load()
    )

  def explode_assignment_list(self, targets: List[AST], value: AST) -> AST:
    return wrap_in_try(
      Assign([Name(self.tmp_name, Store())], value, None),
      *[
        Assign(
          [t],
          self.ins('assignment', self.target(t), Name(self.tmp_name, Load())),
          None
        ) for t in targets
      ],
      fin=[Delete([Name(self.tmp_name, Del())])]
    )

  def leave_Assign(self, stack: NodeStack, node: AST) -> AST:
    if len(node.targets) > 1:
      return self.explode_assignment_list(node.targets, node.value)
    return Assign(
      node.targets,
      self.ins('assignment', self.target(node.targets[0]), node.value),
      node.type_comment
    )

  def leave_AugAssign(self, stack: NodeStack, node: AST) -> AST:
    value = BinOp(Name(node.target.id, Load()), node.op, node.value)
    return Assign(
      [node.target],
      self.ins('assignment', self.target(node.target), value),
      None
    )

  def leave_AnnAssign(self, stack: NodeStack, node: AST) -> AST:
    if node.value:
      return AnnAssign(
        node.target,
        node.annotation,
        self.ins('assignment', self.target(node.target), node.value),
        node.simple
      )
    return node

  def leave_For(self, stack: NodeStack, node: AST) -> AST:
    return For(
      node.target,
      self.ins('iteration', self.target(node.target), node.iter),
      [
        # TODO count passes
        *node.body
      ],
      node.orelse,
      node.type_comment
    )
  
  def leave_FunctionDef(self, stack: NodeStack, node: AST) -> AST:
    return FunctionDef(
      node.name,
      node.args,
      [
        # TODO count calls
        *node.body
      ],
      node.decorator_list,
      node.returns,
      node.type_comment
    )

  def leave_Module(self, stack: NodeStack, node: AST) -> AST:
    return Module(
      [*node.body, *([self.call] if self.call else [])],
      node.type_ignores
    )

  def transform(self, tree: AST, data: ProgramData, call: Optional[AST] = None) -> AST:
    self.data = data
    self.call = call
    return super().transform(tree)
