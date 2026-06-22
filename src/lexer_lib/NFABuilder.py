from parser_lib.Tree.TreeRegexAst import TreeRegexAstNode, TypeAst
from .NFA import NFA
from .LexerSymbol import LexerSymbol, LexerSymbolType

class NFABuilder():
    def __init__(self):
        pass

    def _build_rec(self, tree: TreeRegexAstNode):
        match (tree.type):
            case TypeAst.OR:
                startl, endl = self._build_rec(tree.left)
                startr, endr = self._build_rec(tree.right)
                start, end = self.nfa.union(startl, endl, startr, endr) 
                return start, end
            case TypeAst.KLINI:
                startl, endl = self._build_rec(tree.left)
                start, end = self.nfa.kleene(startl, endl) 
                return start, end
            case TypeAst.CONCAT:
                startl, endl = self._build_rec(tree.left)
                startr, endr = self._build_rec(tree.right)
                start, end = self.nfa.concat(startl, endl, startr, endr) 
                return start, end
            case TypeAst.LEAF:
                return self.nfa.makeSymbol(LexerSymbol(LexerSymbolType.SYMBOL, tree.attr.lexem))

    def build(self, tree: TreeRegexAstNode, id: int):
        self.nfa = NFA(id)
        start, end = self._build_rec(tree)
        self.nfa.start_state = start
        self.nfa.finite_state = end
        return self.nfa