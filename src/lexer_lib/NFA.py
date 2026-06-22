from .LexerSymbol import LexerSymbol, EPSILON, EOF, LexerSymbolType
from .Match import Match
from .Automation import Automation

def nextChar(string: str, index: int):
    if index >= len(string):
        return EOF
    else:
        return LexerSymbol(LexerSymbolType.SYMBOL, string[index])

class NFA(Automation):
    def __init__(self, id):
        super().__init__()
        self.id = id

    def makeSymbol(self, symbol: LexerSymbol):
         new_start = self.max_state + 1
         new_end = self.max_state + 2
         self.max_state = new_end
         self.goto_table[new_start, symbol].append(new_end)
         return new_start, new_end
    
    def concat(self, leftStart: int, leftEnd: int, rightStart: int, rightEnd: int):
        self.goto_table[leftEnd, EPSILON].append(rightStart)
        return leftStart, rightEnd

    def union(self, leftStart: int, leftEnd: int, rightStart: int, rightEnd: int):
        new_start = self.max_state + 1
        new_end = self.max_state + 2

        self.goto_table[new_start, EPSILON].append(leftStart)
        self.goto_table[new_start, EPSILON].append(rightStart)
        self.goto_table[leftEnd, EPSILON].append(new_end)
        self.goto_table[rightEnd, EPSILON].append(new_end)

        self.max_state = new_end
        return new_start, new_end

    def kleene(self, start: int, end: int):
        new_start = self.max_state + 1
        new_end = self.max_state + 2

        self.goto_table[new_start, EPSILON].append(start)
        self.goto_table[new_start, EPSILON].append(new_end)
        self.goto_table[end, EPSILON].append(start)
        self.goto_table[end, EPSILON].append(new_end)

        self.max_state = new_end
        return new_start, new_end

    def run(self, string: str):
        self.alreadyOn = [False for i in range(self.max_state + 1)]
        self.new_states = []
        self.old_states = []
        self._addState(self.start_state)
        index_str = 0
        char = nextChar(string, index_str)
        index_str += 1

        while char != EOF:
            self.swap_stacks()

            for state in self.old_states:
                for t in self.goto_table[state, char]:
                    if not self.alreadyOn[t]:
                        self._addState(t)

            char = nextChar(string, index_str)
            index_str += 1

        return Match(self.id, 0, index_str) if self.alreadyOn[self.finite_state] else None
    
    def runFromIndex(self, index_str: int, string: str):
        self.alreadyOn = [False for i in range(self.max_state + 1)]
        self.new_states = []
        self.old_states = []
        self._addState(self.start_state)
        char = nextChar(string, index_str)
        start = index_str
        end = None
        
        index_str += 1

        while len(self.new_states > 0):
            self.swap_stacks()

            for state in self.old_states:
                for t in self.goto_table[state, char]:
                    if not self.alreadyOn[t]:
                        self._addState(t)

            char = nextChar(string, index_str)
            index_str += 1
            if self.alreadyOn[self.finite_state]:
                end = index_str
        return Match(self.id, start, end) if end else None