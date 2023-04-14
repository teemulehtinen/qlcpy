from ast import (
	AST, If, For, While, Pass, Try, ExceptHandler, Raise, FunctionDef, Delete,
	Return, Break, Continue, Store, Load
)
from typing import Dict, List, Optional

from .WalkAST import WalkAST, NodeStack
from .ProgramData import ProgramData

ScopeNames = Dict[str, ProgramData.Element]

class WalkNames(WalkAST):

	CLASS_TO_RESERVED_WORD: Dict[type, str] = {
		If: 'if', For: 'for', While: 'while', Pass: 'pass', Try: 'try',
		ExceptHandler: 'except', Raise: 'raise', FunctionDef: 'def',
		Delete: 'del', Return: 'return', Break: 'break', Continue: 'continue',
	}
	COMMON_BUILTIN_IDS: List[str] = [
		'abs','all','any','bool','dict','float','input','int','len','list',
  	'max','min','object','open','print','range','reversed','round','set',
  	'sorted','sum','tuple','zip'
	]

	class Scope(dict):
		def __init__(self, id: int, names: Optional[ScopeNames] = None) -> None:
			super().__init__(**names or {})
			self.id = id
			self.data = None

	def __init__(self) -> None:
		self.scope_count = 0
		self.scopes: List[self.Scope] = [self.Scope(self.scope_count)]

	def push_scope(self) -> None:
		self.scope_count += 1
		self.scopes.append(self.Scope(self.scope_count, self.scopes[-1]))

	def pop_scope(self) -> None:
		self.scopes.pop()

	def current_scope(self) -> int:
		return self.scopes[-1].id

	def record_name(
		self,
		type: str,
		id: str,
		declaration: Optional[AST] = None,
		stack: Optional[NodeStack] = None
	) -> ProgramData.Element:
		s = self.current_scope() if declaration else 0
		el = self.data.declare(type, s, id, declaration, stack)
		if not declaration:
			for s in self.scopes:
				if not id in s:
					s[id] = el
		else:
			self.scopes[-1][id] = el
		return el

	def enter_Name(self, stack: NodeStack, node: AST) -> None:
		self.generic_enter(stack, node)
		if type(node.ctx) == Store:
			el = self.scopes[-1].get(node.id, None)
			if el is None:
				self.record_name('variable', node.id, node, stack)
			else:
				el.reference(node, stack)
		elif type(node.ctx) == Load:
			el = self.scopes[-1].get(node.id, None)
			if el is None:
				el = self.record_name(
					'builtin' if node.id in self.COMMON_BUILTIN_IDS else 'unknown',
					node.id
				)
			el.reference(node, stack)

	def enter_FunctionDef(self, stack: NodeStack, node: AST) -> None:
		self.generic_enter(stack, node)
		el = self.record_name('function', node.name, node, stack)
		self.push_scope()
		el.set_container_scope(self.current_scope())

	def leave_FunctionDef(self, stack: NodeStack, node: AST) -> None:
		self.pop_scope()

	def enter_Lambda(self, stack: NodeStack, node: AST) -> None:
		self.generic_enter(stack, node)
		self.push_scope()

	def leave_Lambda(self, stack: NodeStack, node: AST) -> None:
		self.pop_scope()

	def enter_arg(self, stack: NodeStack, node: AST) -> None:
		self.generic_enter(stack, node)
		self.record_name('argument', node.arg, node, stack)

	def enter_If(self, stack: NodeStack, node: AST) -> None:
		self.generic_enter(stack, node)
		self.data.declare('conditional', self.current_scope(), 'if', node, stack)
	
	def enter_For(self, stack: NodeStack, node: AST) -> None:
		self.generic_enter(stack, node)
		self.data.declare('loop', self.current_scope(), 'for', node, stack)

	def enter_While(self, stack: NodeStack, node: AST) -> None:
		self.generic_enter(stack, node)
		self.data.declare('loop', self.current_scope(), 'while', node, stack)

	def enter_Try(self, stack: NodeStack, node: AST) -> None:
		self.generic_enter(stack, node)
		self.data.declare('try', self.current_scope(), 'try', node, stack)

	def generic_enter(self, stack: NodeStack, node: AST) -> None:
		word = self.CLASS_TO_RESERVED_WORD.get(type(node))
		if not word is None:
			el = self.scopes[-1].get(word, None)
			if el is None:
				el = self.record_name('keyword', word)
			el.reference(node, stack)

	def walk(self, tree: AST) -> ProgramData:
		self.data = ProgramData()
		super().walk(tree)
		return self.data
