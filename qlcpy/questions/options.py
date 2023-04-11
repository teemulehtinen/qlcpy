import random
from typing import Any, Iterable, List, Optional

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
  answers: List[Any] = []
  for r in requests:
    target = 100 if r.n is None else (r.n if r.fill else len(out) + r.n)
    for o in r.opt:
      if len(out) >= target:
        break
      if not o.answer in answers:
        answers.append(o.answer)
        out.append(o)
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

def random_order(answers: Iterable[Any]) -> Iterable[Any]:
  mix_answers = list(answers)
  return random.sample(mix_answers, len(mix_answers))

def take_options(
  count: int,
  answers: Iterable[Any],
  type: str,
  info: Optional[str] = '',
  correct: Optional[bool] = False
) -> QLCOptionRequest:
  return QLCOptionRequest(opt(random_order(answers), type, info, correct), count)

def fill_options(
  count: int,
  answers: Iterable[Any],
  type: str,
  info: Optional[str] = '',
  correct: Optional[bool] = False
) -> QLCOptionRequest:
  return QLCOptionRequest(opt(random_order(answers), type, info, correct), count, True)
