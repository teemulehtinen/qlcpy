from typing import Any, List, Optional

class QLCRequest:
  def __init__(
    self,
    count: int,
    fill: Optional[bool] = None,
    types: Optional[List[str]] = None,
    unique_types: Optional[bool] = None
  ):
    self.count = count
    self.fill = fill
    self.types = types
    self.unique_types = unique_types

class Input:
  def __init__(self, func: str, args: List[Any]):
    self.func = func
    self.args = args

def generate(
  source: str,
  requests: Optional[List[QLCRequest]] = None,
  input: Optional[List[Input]] = None
) -> str:
  pass
