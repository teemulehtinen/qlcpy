import ast
import random
from typing import List, Optional, Set

from .models import QLCRequest, QLC
from .questions import TEMPLATES, QLCTemplate
from .instrument import run_with_instrumentor, parse_body

def select_templates(req: List[QLCRequest]) -> List[QLCTemplate]:
  available: List[str] = list(t.type for t in TEMPLATES)
  for r in req:
    for typ in (r.types or []):
      if not typ in available:
        raise ValueError(f'Uknown QLC type: {typ}')
  select: Set[str] = set()
  for r in req:
    if r.types is None:
      return TEMPLATES
    select.update(r.types)
  return list(t for t in TEMPLATES if t.type in select)

def generate(
  src: str,
  requests: Optional[List[QLCRequest]] = None,
  call: Optional[str] = None,
  input: Optional[str] = None,
  run_main: bool = False,
  silent_call: bool = False,
) -> List[QLC]:
  tree = ast.parse(src)
  call = call.replace('\\n', '\n') if call else None
  instrumentor = run_with_instrumentor(tree, parse_body(call), input, run_main)
  prepared = list(
    p
    for t in select_templates(requests)
    for p in t.maker(t.pos, t.type, tree, None if silent_call else call, instrumentor)
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
  return sorted(out, key=lambda qlc: qlc.pos)
