from ast import AST
from typing import Any, List, Optional

class ProgramData:

	class Element:

		def __init__(self, type: str, scope: int, id: str, declaration: Optional[AST]) -> None:
			self.type = type
			self.scope = scope
			self.id = id
			self.declaration = declaration
			self.references: List[AST] = []
			self.values: List[Any] = []
		
		def reference(self, node: AST) -> None:
			self.references.append(node)
		
		def value(self, value: Any) -> None:
			self.values.append(value)
		
		def has_node(self, node: AST) -> bool:
			return node == self.declaration or node in self.references

		def __repr__(self) -> str:
			info = [f'{self.type}: (S{self.scope}) {self.id}']
			if not self.declaration is None:
				info.append(f'  declared on {self.declaration.lineno}')
			if len(self.references) > 0:
				info.append(f'  referenced on {", ".join(str(r.lineno) for r in self.references)}')
			if len(self.values) > 0:
				info.append(f'  assigned values {", ".join(str(v) for v in self.values)}')
			return '\n'.join(info)
	
	def __init__(self):
		self.elements: List[self.Element] = []

	def declare(self, type: str, scope: int, id: str, declaration: Optional[AST] = None) -> Element:
		el = self.Element(type, scope, id, declaration)
		self.elements.append(el)
		return el

	def element_n(self, n: int) -> Element:
		return self.elements[n]

	def element_for_node(self, node: AST, types: List[str]) -> Element:
		for i, el in enumerate(self.elements):
			if el.type in types and el.has_node(node):
				return i, el
		return None, None
	
	def elements_for_types(self, types: List[str]) -> List[Element]:
		for el in self.elements:
			if el.type in types:
				yield el
	
	def __repr__(self) -> str:
		return '\n'.join(str(el) for el in self.elements)
