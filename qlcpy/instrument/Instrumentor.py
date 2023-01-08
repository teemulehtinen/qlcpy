from typing import Any, Iterable, List, Optional

from ..primitives import Primitive
from .ProgramData import ProgramData

class Instrumentor:

  def __init__(self, data: ProgramData):
    self.data = data
    self.errors: List[str] = []

  def val(self, target: Optional[int], value: Any) -> None:
    if target is None:
      self.errors.append(f'Assignment of {Primitive(value)} to unknown variable')
    else:
      self.data.element_n(target).value(Primitive(value))

  def eval(self, target: Optional[int], branch: int) -> None:
    if target is None:
      self.errors.append(f'Evaluation of an unknown branch')
    else:
      self.data.element_n(target).evaluation(branch)

  def unpack_assignment(self, target: List[Optional[int]], iter: Iterable[Any]) -> Any:
    try:
      for t in target:
        val = next(iter)
        self.val(t, val)
        yield val
    except StopIteration:
      pass

  def assignment(self, target: List[Optional[int]], value: Any) -> Any:
    if len(target) > 1:
      try:
        return self.unpack_assignment(target, iter(value))
      except TypeError:
        pass
    elif len(target) > 0:
      self.val(target[0], value)
    return value

  def iteration(self, target: List[Optional[int]], iter: Iterable[Any]) -> Iterable[Any]:
    for v in iter:
      yield self.assignment(target, v)

  def evaluation(self, target: List[Optional[int]], branch: int) -> None:
    if len(target) > 0:
      self.eval(target[0], branch)
