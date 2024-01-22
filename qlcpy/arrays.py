import random
from typing import List
from .primitives import Primitive

def altered_arrays(
  a: List[Primitive],
  other: List[List[Primitive]],
  fix_len: bool = False
) -> List[Primitive]:
  distractors = list(o for o in other if len(o) >= len(a)) or [a]
  altered = [
    list(reversed(a)),
    random.sample(a, len(a)),
    random.sample(a, len(a)),
    random.sample(random.choice(distractors), len(a)),
    random.sample(random.choice(distractors), len(a)),
    [random.randint(0, 10) for _ in a],
    [random.randint(0, 10) for _ in a],
    [random.randint(0, 10) for _ in a],
    [random.randint(0, 10) for _ in a],
  ]
  if fix_len or len(a) < 2:
    return altered
  return altered + [aa[:-1] for aa in altered]
