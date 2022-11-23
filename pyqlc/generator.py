import random
from ast import AST
from typing import List, Optional, Set

from .models import QLCRequest, ProgramInput, QLC
from .questions import TEMPLATES, QLCTemplate
from .instrument import run_with_instrumentor

def select_templates(req: List[QLCRequest]) -> List[QLCTemplate]:
  select: Set[QLCTemplate] = set()
  for r in req:
    if r.types is None:
      return TEMPLATES
    select.update(r.types)
  return list(t for t in TEMPLATES if t in select)

def generate(
  tree: AST,
  requests: Optional[List[QLCRequest]] = None,
  input: Optional[List[ProgramInput]] = None
) -> List[QLC]:
  instrumentor = run_with_instrumentor(
    tree,
    input.func if input else None,
    input.args if input else None
  )
  prepared = list(
    p for t in select_templates(requests) for p in t.maker(t.type, tree, input, instrumentor)
  )
  out: List[QLC] = []
  for r in requests:
    n = r.count - len(out) if r.fill else r.count
    while n > 0 and len(prepared) > 0:
      sample = prepared if r.types is None else list(p for p in prepared if p.type in r.types)
      picked = random.choice(sample) if sample else None
      if picked:
        qlc = picked.make()
        if qlc and r.unique_types:
          prepared = list(p for p in prepared if p.type != picked.type)
        else:
          prepared = list(p for p in prepared if p != picked)
        if qlc is None:
          continue
        out.append(qlc)
      n -= 1
  return out
