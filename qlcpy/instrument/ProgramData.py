from ast import AST, Store
from typing import Iterator, List, Optional

from .WalkAST import NodeStack
from ..primitives import Primitive

class Reference:
	def __init__(self, node: AST, stack: NodeStack):
		self.node = node
		self.stack = stack.copy()
		self.is_store: bool = hasattr(node, 'ctx') and type(node.ctx) == Store
	
	def __eq__(self, other):
		if isinstance(other, AST):
			return self.node == other
		return super().__eq__(other)

class ProgramData:

	class Element:

		def __init__(
			self,
			type: str,
			scope: int,
			id: str,
			declaration: Optional[AST],
			stack: Optional[NodeStack],
		) -> None:
			self.type = type
			self.scope = scope
			self.id = id
			self.declaration: Optional[Reference] = None
			self.container_scope: Optional[int] = None
			self.references: List[Reference] = []
			self.values: List[Primitive] = []
			self.evaluations: List[int] = []
			if declaration:
				self.declaration = Reference(declaration, stack or [])

		def set_container_scope(self, scope: int) -> None:
			self.container_scope = scope

		def reference(self, node: AST, stack: NodeStack) -> None:
			self.references.append(Reference(node, stack))

		def value(self, value: Primitive) -> None:
			self.values.append(value)

		def evaluation(self, branch: int) -> None:
			self.evaluations.append(branch)

		def has_reference(self, node: AST) -> bool:
			return node == self.declaration or node in self.references

		def __repr__(self) -> str:
			cscope = f' -> S{self.container_scope}' if self.container_scope else ''
			info = [f'{self.type}: (S{self.scope}{cscope}) {self.id}']
			if not self.declaration is None:
				info.append(f'  declared on {self.declaration.node.lineno}')
			if len(self.references) > 0:
				info.append(f'  referenced on {", ".join(str(r.node.lineno) for r in self.references)}')
			if len(self.values) > 0:
				info.append(f'  assigned values {", ".join(str(v) for v in self.values)}')
			if len(self.evaluations) > 0:
				info.append(f'  evaluated {len(self.evaluations)} times')
			return '\n'.join(info)

	def __init__(self):
		self.elements: List[self.Element] = []

	def declare(
		self,
		type: str,
		scope: int,
		id: str,
		declaration: Optional[AST] = None,
		stack: Optional[NodeStack] = None
	) -> Element:
		el = self.Element(type, scope, id, declaration, stack)
		self.elements.append(el)
		return el

	def element_n(self, n: int) -> Element:
		return self.elements[n]

	def element_for_node(self, node: AST, types: List[str]) -> Element:
		for i, el in enumerate(self.elements):
			if el.type in types and el.has_reference(node):
				return i, el
		return None, None
	
	def elements_for_types(self, types: List[str]) -> Iterator[Element]:
		for el in self.elements:
			if el.type in types:
				yield el

	def element_for_id(self, id: str) -> Element:
		for el in self.elements:
			if el.id == id:
				return el
		return None
	
	def element_for_scope(self, scope: int) -> Element:
		for el in self.elements:
			if el.container_scope == scope:
				return el
		return None
	
	def elements_in_scope(self, scope: int, types: List[str] = None) -> Iterator[Element]:
		for el in self.elements:
			if el.scope == scope and (types is None or el.type in types):
				yield el

	def __repr__(self) -> str:
		return '\n'.join(str(el) for el in self.elements)
