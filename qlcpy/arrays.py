import random
from typing import Any, List

def _changed_element(a1: Any, a2: Any) -> Any:
  if type(a2) != list:
    return a2
  if len(a2) > len(a1):
    return a2[-1]
  if len(a2) < len(a1):
    return None
  for i in range(len(a2)):
    if a2[i] != a1[i]:
      return a2[i]
  return None

def _to_numeric(v: Any) -> int:
  if v is None:
    return 0
  if type(v) == bool:
    return 1 if v else 0
  if type(v) == str:
    return ord(v[0])
  return v

def _detect_type(a: List[Any]) -> type:
  for v in a:
    if type(v) in (bool, int, float, str):
      return type(v)
  return int

def _craft_to_type(v: float, t: type) -> Any:
  if t == bool:
    return int(v) % 2 == 1
  if t == int:
    return int(v)
  if t == str:
    return chr(int(v))
  return v

def random_steps(a: List[Any], seeds: List[Any]) -> List[List[Any]]:
  if len(a) > 1:
    if all(type(e) == list for e in a):
      return [
        reversed(a),
        reversed(a)[:-1],
        list(_changed_element(a[i], a[i + 1]) for i in range(len(a) - 1)),
      ]
    typ = _detect_type(a)
    step = min(_to_numeric(a[1]) - _to_numeric(a[0]), 10)
    beg0 = _to_numeric(a[0])
    beg1 = _to_numeric(random.choice(seeds))
    return [
      list(_craft_to_type(beg0 + i * 2 * step, typ) for i in range(len(a))),
      list(_craft_to_type(beg1 - i * step, typ) for i in range(len(a) - 1)),
      list(_craft_to_type(beg1 + i * step, typ) for i in range(len(a) - 1)),
    ]
  vals = list(set(r for r in seeds if type(r) != str or len(r) < 10))
  vals.extend(random.randint(0, 10) for i in range(5 - len(vals)))
  return vals
