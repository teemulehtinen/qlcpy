from typing import Any, Callable, List, Optional, Union

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

class ProgramInput:
  def __init__(self, func: str, args: List[Any]):
    self.func = func
    self.args = args

class QLCOption:
  def __init__(self, type: str, answer: Union[str, int], correct: bool = False, info: str = None):
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

class QLC:
  def __init__(self, type: str, question: str, options: List[QLCOption]):
    self.type = type
    self.question = question
    self.options = options
  
  def to_dict(self):
    return {
      'type': self.type,
      'question': self.question,
      'options': self.options,
    }

class QLCPrepared:
  def __init__(self, type: str, make: Callable[..., QLC]):
    self.type = type
    self.make = make