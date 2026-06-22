from enum import Enum, auto
from typing import Optional

class LexerSymbolType(Enum):
    EPSILON = auto()
    SYMBOL = auto()
    EOF = auto()

class LexerSymbol():
    def __init__(self, type: LexerSymbolType, lexem: Optional[str]):
        self.type = type
        self.lexem = lexem

    def __eq__(self, value: 'LexerSymbol'):
        return self.type == value.type and self.lexem == value.lexem
    
    def __str__(self):
        return f"type: {self.type}, lexem: {self.lexem}"
    
    def __repr__(self):
        return f"type: {self.type}, lexem: {self.lexem}"
    
    def isEps(self):
        return self.type == LexerSymbolType.EPSILON
    
    def __hash__(self):
        return hash((self.type, self.lexem))


EPSILON = LexerSymbol(LexerSymbolType.EPSILON, None)
EOF = LexerSymbol(LexerSymbolType.EOF, None)