from ast import AST
from typing import Callable, List

from ..instrument import Instrumentor
from ..models import QLC

class QLCPreparer:

  def prepare(self, tree: AST, instrumentor: Instrumentor) -> List[Callable[..., QLC]]:
    return []
