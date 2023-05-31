import random
from ast import AST, Set, Try
from typing import List, Optional

from ..i18n import t
from ..instrument import (
  find_nodes, find_next, collect_error_causes, ExceptAndCauses, Instrumentor, ProgramData
)
from ..models import QLC, QLCPrepared
from .options import pick_options, options, take_options, fill_options

class LoopEnd(QLCPrepared):
  def __init__(self, pos: int, type: str, node: AST, next: Optional[AST]):
    super().__init__(pos, type)
    self.node = node
    self.next = next

  def make(self):
    beg = self.node.lineno
    end = self.node.end_lineno
    nex = self.next.lineno if self.next else self.node.end_lineno + 2
    return QLC(
      self.pos,
      self.type,
      t('q_loop_end', beg),
      pick_options(
        options([end], 'last_line_inside_block', t('o_loop_end_correct'), True),
        options([max(1, beg - 1)], 'line_before_block', t('o_loop_end_before')),
        options([nex], 'line_after_block', t('o_loop_end_after')),
        fill_options(4, range(beg + 1, end), 'line_inside_block', t('o_loop_end_inside')),
        fill_options(4, [nex + 1], 'line_after_block', t('o_loop_end_after'))
      )
    )

def loop_end(
  pos: int,
  type: str,
  tree: AST,
  call: Optional[str],
  ins: Instrumentor
) -> List[LoopEnd]:

  return list(
    LoopEnd(pos, type, node, find_next(tree, node))
    for node in find_nodes(tree, ['For', 'While'])
  )

class VariableDeclaration(QLCPrepared):
  def __init__(self, pos: int, type: str, element: ProgramData.Element):
    super().__init__(pos, type)
    self.variable = element
  
  def make(self):
    decl = self.variable.declaration
    refs = self.variable.references
    # NOTE: if-else structures can easily assign 1st time on 2nd store name, what to do?
    if decl is None or len(refs) == 0:
      return None
    ref = random.choice(refs)
    text_id = {
      'Store': 'q_variable_write_declaration',
      'Load': 'q_variable_read_declaration',
      'Del': 'q_variable_del_declaration',
    }
    return QLC(
      self.pos,
      self.type,
      t(text_id[ref.node.ctx.__class__.__name__], ref.node.id, ref.node.lineno),
      pick_options(
        options([decl.node.lineno], 'declaration_line', t('o_variable_declaration_correct'), True),
        take_options(
          2,
          [r.node.lineno for r in refs],
          'reference_line',
          t('o_variable_declaration_reference')
        ),
        fill_options(
          4,
          range(max(1, decl.node.lineno - 2), max(r.node.lineno for r in refs) + 3),
          'random_line',
          t('o_variable_declaration_random')
        )
      )
    )

def variable_declaration(
  pos: int,
  type: str,
  tree: AST,
  call: Optional[str],
  ins: Instrumentor
) -> List[VariableDeclaration]:
  return list(
    VariableDeclaration(pos, type, e) for e in ins.data.elements_for_types(['variable'])
  )

class ExceptSource(QLCPrepared):
  TARGETED = ['ZeroDivisionError', 'ValueError', 'IndexError']

  class CandidateExcept():
    def __init__(self, except_line: int, source_lines: List[int], distractor_lines: List[int]):
      self.except_line = except_line
      self.source_lines = source_lines
      self.distractor_lines = distractor_lines

  def __init__(self, pos: int, type: str, node: AST):
    super().__init__(pos, type)
    self.node: Try = node

  def prepate_candidates(self, e: ExceptAndCauses) -> CandidateExcept:
    target = list(c.line for c in e.causes if c.error in self.TARGETED)
    if len(target) == 0:
      return self.CandidateExcept(e.line, [], [])
    reserved: Set[int] = set()
    for c in e.causes:
      reserved.update(range(c.line, c.end_line + 1))
    body_lines = range(self.node.body[0].lineno, self.node.body[-1].end_lineno + 1)
    return self.CandidateExcept(
      e.line,
      target,
      set(body_lines) - reserved,
    )

  def make(self):
    candidates = list(self.prepate_candidates(e) for e in collect_error_causes(self.node))
    candidates = list(c for c in candidates if len(c.source_lines) > 0)
    if len(candidates) == 0:
      return None
    case = sorted(candidates, key=lambda c: len(c.distractor_lines), reverse=True)[0]
    beg = self.node.lineno
    end = self.node.end_lineno
    few_before = range(max(1, beg - 3), beg)
    return QLC(
      self.pos,
      self.type,
      t('q_except_source', case.except_line),
      pick_options(
        take_options(1, case.source_lines, 'source_line', t('o_except_source'), True),
        options([beg], 'try_line', t('o_except_try_line')),
        take_options(1, few_before, 'before_try_block', t('o_except_outside_try')),
        fill_options(4, case.distractor_lines, 'not_source_line', t('o_except_not_source')),
        fill_options(4, [end + 2], 'after_try_block', t('o_except_outside_try')),
      )
    )

def except_source(
    pos: int,
    type: str,
    tree: AST,
    call: Optional[str],
    ins: Instrumentor
) -> List[ExceptSource]:
  return list(
    ExceptSource(pos, type, node) for node in find_nodes(tree, ['Try'])
  )