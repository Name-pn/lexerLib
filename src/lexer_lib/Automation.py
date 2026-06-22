from collections import defaultdict
from .LexerSymbol import EPSILON

class Automation():
    def __init__(self):
        self.start_state = 0
        self.finite_state = 0
        self.max_state = 0
        self.goto_table = defaultdict(list)

    def _addState(self, state):
        self.new_states.append(state)
        self.alreadyOn[state] = True
        for t in self.goto_table[state, EPSILON]:
            if not self.alreadyOn[t]:
                self._addState(t)

    def swap_stacks(self):
        self.old_states = self.new_states
        self.alreadyOn = [False for i in range(self.max_state + 1)]
        self.new_states = []

    def pretty_print_grouped(self):
        from collections import defaultdict
        grouped = defaultdict(list)
        for (state, symbol), targets in self.goto_table.items():
            sym_type, lexem = symbol.type, symbol.lexem
            type_name = sym_type.name if hasattr(sym_type, 'name') else str(sym_type)
            lex_str = lexem if lexem is not EPSILON else 'ε'
            grouped[state].append((type_name, lex_str, targets))
        for state, transitions in sorted(grouped.items()):
            print(f"State {state}:")
            for typ, lex, dest in transitions:
                print(f"  {typ} ({lex}) -> {dest}")
            print()

    def runFromIndex(self, index_str: int, string: str):
        raise NotImplementedError("runFromIndex")
    
    def run(self, string: str):
        raise NotImplementedError("runFromIndex")