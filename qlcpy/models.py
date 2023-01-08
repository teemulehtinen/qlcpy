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

  def __repr__(self) -> str:
    txt = [f'count={self.count}']
    if self.fill:
      txt.append('filled')
    if self.types:
      txt.append(f'types=[{", ".join(self.types)}]')
    if self.unique_types:
      txt.append('unique')
    return f'<{" ".join(txt)}>'

class QLCOption:
  def __init__(self, type: str, answer: Any, correct: bool = False, info: str = None):
    self.type = type
    self.answer = answer
    self.correct = correct
    self.info = info
  
  def to_dict(self):
    return {
      'type': self.type,
      'answer': self.answer,
      'correct': self.correct,
      'info': self.info,
    }
  
  def __repr__(self) -> str:
    return f'{"*" if self.correct  else " "} {self.answer}: {self.info} [{self.type}]'

class QLC:
  def __init__(self, pos: int, type: str, question: str, options: List[QLCOption]):
    self.pos = pos
    self.type = type
    self.question = question
    self.options = options
  
  def to_dict(self):
    return {
      'type': self.type,
      'question': self.question,
      'options': list(o.to_dict() for o in self.options),
    }

  def __repr__(self) -> str:
    return '\n'.join([f'{self.question} [{self.type}]', *[str(o) for o in self.options]])

class QLCPrepared:
  def __init__(self, pos: int, type: str):
    self.pos = pos
    self.type = type

  def make(self) -> Optional[QLC]:
    return None
