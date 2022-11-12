from typing import Any

PRIMITIVES = (bool, int, float, complex, str, type(None))

def _primitive(value: Any) -> Any:
  return value if type(value) in PRIMITIVES else f'Ref:{id(value)}'

def as_primitive(value: Any) -> Any:
  if type(value) in (list, tuple):
    return list(_primitive(v) for v in value)
  return _primitive(value)
