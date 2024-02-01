from typing import List, Optional, Tuple
from ast import AST, Add, Assign, AugAssign, AnnAssign, BinOp, Call, Constant, For, Index, Name, Sub

from .trees import first_field, iter_tree, NodeStack, stack_search, stack_top
from .ProgramData import ProgramData

def none_is(bools: List[bool]) -> bool:
  return all(not b for b in bools)

def is_for(node: AST) -> bool:
  return type(node) == For

def is_for_range(node: For) -> bool:
  return type(node.iter) == Call and type(node.iter.func) == Name and node.iter.func.id == 'range'

def is_index(node: AST) -> bool:
  return type(node) == Index

def is_reference(node: AST, id: str) -> bool:
  return type(node) == Name and node.id == id

def expr_includes_variable(node: AST, id: str) -> bool:
  return any(is_reference(n, id) for n in iter_tree(node))

def is_guarded_by_condition(stack: NodeStack, id: str) -> bool:
  for n in stack_search(stack[:-1], ['If', 'While']):
    test = getattr(n, 'test')
    if test and expr_includes_variable(test, id):
      return True
  return False

def is_in_condition_before_loop(stack: NodeStack) -> bool:
  for n, _ in reversed(stack[:-1]):
    t = n.__class__.__name__
    if t in ('If'):
      return True
    if t in ('While', 'For'):
      return False
  return False

class AssignmentInfo:

  @staticmethod
  def is_a_target(node: AST, id: str):
    return any(is_reference(t, id) for t in first_field(node, ['targets', 'target']))

  @staticmethod
  def extract_binop(node: AST, id: str) -> Tuple[Optional[AST], Optional[AST]]:
    if type(node) == BinOp:
      if is_reference(node.left, id):
        return node.op, node.right
      if is_reference(node.right, id):
        return node.op, node.left
    return None, None

  def __init__(self, node: AST, id: str):
    self.node = node
    self.is_assignment: bool = False
    self.expr: Optional[AST] = None
    self.includes_variable: bool = False
    self.augments_variable: bool = False
    self.op: Optional[AST] = None
    self.value: Optional[AST] = None
    if type(node) == AugAssign and is_reference(node.target, id):
      self.is_assignment = True
      self.expr = node.value
      self.includes_variable = True
      self.augments_variable = True
      self.op = node.op
      self.value = node.value
    elif type(node) in (Assign, AnnAssign) and self.is_a_target(node, id):
      self.is_assignment = True
      self.expr = node.value
      self.value = node.value
      op, value = self.extract_binop(node.value, id)
      if not op is None:
        self.includes_variable = True
        self.augments_variable = True
        self.op = op
        self.value = value
      elif any(is_reference(n, id) for n in iter_tree(node.value)):
        self.includes_variable = True

class VariableRole():
  DEAD = 'dead'
  FIXED = 'fixed'
  STEPPER = 'stepper'
  GATHERER = 'gatherer'
  HOLDER = 'holder'
  NONE = 'unknown'
  SUPPORTED_ROLES = [DEAD, FIXED, STEPPER, GATHERER, HOLDER]

  def __init__(self, var: ProgramData.Element):
    self.var = var
    self.role = self.classify_variable(var)

  def other_roles(self):
    return list(k for k in self.SUPPORTED_ROLES if k != self.role)

  @classmethod
  def classify_variable(cls, var: ProgramData.Element) -> str:

    # Only declaration
    stores = list(r for r in var.references if r.is_store)
    if len(stores) == 0:
      parent = stack_top(var.declaration.stack)
      if is_for(parent):
        if is_for_range(parent) and len(var.references) > 0:
          return cls.STEPPER
        return cls.NONE
      a = AssignmentInfo(parent, var.id)
      if a.is_assignment:
        if len(var.references) == 0:
          return cls.DEAD
        if type(a.expr) == Constant:
          return cls.FIXED
      return cls.NONE

    # Includes iterators
    parents = list(stack_top(r.stack) for r in stores)
    fors = list(is_for(p) for p in parents)
    if all(fors) and all(is_for_range(p) for p in parents):
      return cls.STEPPER
    if any(fors):
      return cls.NONE
    
    # Something else than for or assignment?
    assignments = list(AssignmentInfo(p, var.id) for p in parents)
    if any(not a.is_assignment for a in assignments):
      return cls.NONE

    # None depend on the variable
    if none_is(a.includes_variable for a in assignments):
      if (
        none_is(type(a.expr) == Constant for a in assignments)
        and all(is_guarded_by_condition(r.stack, var.id) for r in stores)
      ):
        return cls.HOLDER
      return cls.NONE

    # Share same variable augmentation
    if all(a.augments_variable for a in assignments):
      ops = set(a.op for a in assignments)
      if len(ops) == 1:
        op = ops.pop()
        if type(op) in [Add, Sub]:
          vals = set(a.value.n if type(a.value) == Constant else None for a in assignments)
          if (
            not None in vals and len(vals) == 1 and type(vals.pop()) == int
            and not any(is_in_condition_before_loop(r.stack) for r in stores)
            and any(is_index(stack_top(r.stack)) for r in var.references if not r.is_store)
          ):
            return cls.STEPPER
        if type(op) == Add:
          parent = stack_top(var.declaration.stack)
          a = AssignmentInfo(parent, var.id)
          if a.is_assignment and type(a.expr) == Constant and type(a.expr.n) in [int, str]:
            return cls.GATHERER

    return cls.NONE
