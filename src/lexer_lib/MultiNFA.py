from .LexerSymbol import LexerSymbol, EPSILON, EOF, LexerSymbolType
from .Match import Match
from collections import defaultdict
from .NFA import nextChar, NFA
from .Automation import Automation

class MultiNFA(Automation):
    def __init__(self, nfa_list: list[NFA]):
        super().__init__()
        self.start_state = 0
        self.finite_states = []
        self.max_state = 0
        self.finite_state_to_id = {}
        
        for nfa in nfa_list:
            offset = self.max_state + 1
            self._moveGoto(nfa, offset)
            self.max_state = nfa.max_state + offset
            self.finite_states.append(self.max_state)
            self.finite_state_to_id[self.max_state] = nfa.id
        self.alreadyOn = [False for i in range(self.max_state + 1)]
        self.new_states = []
        self.old_states = []

    def _moveGoto(self, nfa: NFA, offset: int)->None:
        for item in nfa.goto_table.items():
            key, lst = item
            state_from, move_symbol = key
            self.goto_table[(state_from + offset, move_symbol)].extend([el + offset for el in lst])
        self.goto_table[self.start_state, EPSILON].append(offset + nfa.start_state)

    def _finiteMatch(self):
        for end in self.finite_states:
            if self.alreadyOn[end]:
                return self.finite_state_to_id[end]
        return None

    def run(self, string: str):
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
        
        id = self._finiteMatch()
        if id:
            return Match(id, 0, index_str)
        return id

    
    def runFromIndex(self, index_str: int, string: str):
        self._addState(self.start_state)
        char = nextChar(string, index_str)
        start = index_str
        end = None
        last_id = None
        index_str += 1
        while len(self.new_states) > 0:
            self.swap_stacks()

            for state in self.old_states:
                for t in self.goto_table[state, char]:
                    if not self.alreadyOn[t]:
                        self._addState(t)

            char = nextChar(string, index_str)
            index_str += 1
            id = self._finiteMatch()
            if id is not None:
                end = index_str
                last_id = id
        return Match(last_id, start, end-1) if end else None