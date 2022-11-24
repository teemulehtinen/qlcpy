from ast import (
  AnnAssign, AST, Assign, Attribute, BinOp, Call, Constant, Del, Delete, Expr,
  For, FunctionDef, If, Load, List as ASTList, Module, Name, Store, While
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
    self.add: List[AST] = []

  def ins(self, method: str, *args: AST) -> AST:
    return Call(
      Attribute(Name(self.ins_name, Load()), method, Load()),
      list(args),
      []
    )

  def target(self, node: AST, types: Optional[List[str]] = None) -> AST:
    # TODO handle Subscript/Attribute in target?
    return ASTList(
      list(
        Constant(i, None) for i, _ in [
          self.data.element_for_node(el, types or ['function', 'variable', 'argument']) for el in (
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
      node.body,
      node.orelse,
      node.type_comment
    )

  def enter_If(self, stack: NodeStack, node: AST) -> AST:
    target = self.target(node, ['conditional'])
    orelse = self.transform_attr(stack, node, 'orelse')
    return If(
      self.transform_attr(stack, node, 'test'),
      [
        Expr(self.ins('evaluation', target, Constant(0, None))),
        *self.transform_attr(stack, node, 'body')
      ],
      [
        Expr(self.ins('evaluation', target, Constant(1, None))),
        *orelse
      ] if orelse else orelse
    )

  def enter_While(self, stack: NodeStack, node: AST) -> AST:
    target = self.target(node, ['loop'])
    orelse = self.transform_attr(stack, node, 'orelse')
    return While(
      self.transform_attr(stack, node, 'test'),
      [
        Expr(self.ins('evaluation', target, Constant(0, None))),
        *self.transform_attr(stack, node, 'body')
      ],
      [
        Expr(self.ins('evaluation', target, Constant(1, None))),
        *orelse
      ] if orelse else orelse
    )

  def enter_For(self, stack: NodeStack, node: AST) -> AST:
    target = self.target(node, ['loop'])
    orelse = self.transform_attr(stack, node, 'orelse')
    return For(
      self.transform_attr(stack, node, 'target'),
      self.transform_attr(stack, node, 'iter'),
      [
        Expr(self.ins('evaluation', target, Constant(0, None))),
        *self.transform_attr(stack, node, 'body')
      ],
      [
        Expr(self.ins('evaluation', target, Constant(1, None))),
        *orelse,
      ] if orelse else orelse,
      self.transform_attr(stack, node, 'type_comment')
    )

  def enter_FunctionDef(self, stack: NodeStack, node: AST) -> AST:
    target = self.target(node, ['function'])
    return FunctionDef(
      self.transform_attr(stack, node, 'name'),
      self.transform_attr(stack, node, 'args'),
      [
        Expr(self.ins('evaluation', target, Constant(0, None))),
        *self.transform_attr(stack, node, 'body')
      ],
      self.transform_attr(stack, node, 'decorator_list'),
      self.transform_attr(stack, node, 'returns'),
      self.transform_attr(stack, node, 'type_comment')
    )

  def leave_Module(self, stack: NodeStack, node: AST) -> AST:
    return Module([*node.body, *self.add], node.type_ignores)

  def transform(self, tree: AST, data: ProgramData, add: Optional[List[AST]] = None) -> AST:
    self.data = data
    self.add = add or []
    return super().transform(tree)
