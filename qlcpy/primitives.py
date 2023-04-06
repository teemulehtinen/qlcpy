from typing import Any, List, Set

class Primitive:
  PRIMITIVE_TYPES = (bool, int, float, str, type(None))

  def __init__(self, value: Any):
    if type(value) in self.PRIMITIVE_TYPES:
      self.type = type(value)
      self.value = value
    else:
      self.type = 'Reference'
      self.value = id(value)
  
  def __repr__(self) -> str:
    if self.type in (int, float):
      return f'{self.value}'
    if self.type == str:
      return f'"{self.value}"'
    if self.type == bool:
      return 'True' if self.value else 'False'
    if self.type == type(None):
      return 'None'
    return f'Reference[{self.value}]'
  
  def __eq__(self, other) -> bool:
    if self.type == 'Reference':
      return self.value == id(other)
    return self.value == other

def primitives_to_str(values: List[Primitive]) -> str:
  return ", ".join(str(v) for v in values)

def includes_references(values: List[Primitive]) -> bool:
  return any(v.type == 'Reference' for v in values)