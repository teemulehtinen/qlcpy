from typing import Any

PRIMITIVES = (bool, int, float, str, type(None))

def _primitive(value: Any) -> Any:
  return value if type(value) in PRIMITIVES else f'Ref:{id(value)}'

def as_primitive(value: Any) -> Any:
  if type(value) in (list, tuple):
    return list(_primitive(v) for v in value)
  return _primitive(value)

def _print(value: Any) -> Any:
  if type(value) in (int, float):
    return f'{value}'
  if type(value) == bool:
    return 'True' if value else 'False'
  return f'"{str(value)}"'

def primitive_to_str(value: Any) -> str:
  if type(value) in (list, tuple):
    return ", ".join(_print(v) for v in value)
  return _print(value)