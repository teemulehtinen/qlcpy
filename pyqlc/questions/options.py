import random
from typing import Any, Callable, Iterable, List, Optional

from ..models import QLCOption

class QLCOptionRequest:
  def __init__(
    self,
    opt: Iterable[QLCOption],
    n: Optional[int] = None,
    fill: Optional[bool] = None
  ):
    self.opt = opt
    self.n = n
    self.fill = fill

def pick_options(*requests: QLCOptionRequest) -> List[QLCOption]:
  out: List[QLCOption] = []
  for r in requests:
    if not r.n is None and r.fill and len(out) >= r.n:
      continue
    opts = [o for o in r.opt if not o.answer in [u.answer for u in out]]
    if r.n is None:
      out.extend(opts)
    else:
      out.extend(random.sample(opts, min(max(0, r.n - len(out)) if r.fill else r.n, len(opts))))
  out_int = list(o for o in out if type(o.answer) == int)
  out_str = list(o for o in out if type(o.answer) != int)
  return [
    *[out_int[i] for i, _ in sorted(enumerate(out_int), key=lambda e: e[1].answer)],
    *[out_str[i] for i, _ in sorted(enumerate(out_str), key=lambda e: str(e[1].answer))]
  ]

def opt(
  answers: Iterable[Any],
  type: str,
  info: Optional[str] = '',
  correct: Optional[bool] = False
) -> Iterable[QLCOption]:
  return [QLCOption(type, a, correct, info) for a in answers]

def options(
  answers: Iterable[Any],
  type: str,
  info: Optional[str] = '',
  correct: Optional[bool] = False
) -> QLCOptionRequest:
  return QLCOptionRequest(opt(answers, type, info, correct))

def random_options(
  count: int,
  answers: Iterable[Any],
  type: str,
  info: Optional[str] = '',
  correct: Optional[bool] = False
) -> QLCOptionRequest:
  return QLCOptionRequest(opt(answers, type, info, correct), count)

def fill_random_options(
  count: int,
  answers: Iterable[Any],
  type: str,
  info: Optional[str] = '',
  correct: Optional[bool] = False
) -> QLCOptionRequest:
  return QLCOptionRequest(opt(answers, type, info, correct), count, True)
