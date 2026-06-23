from .NFABuilder import NFABuilder
from .RegexLexer import RegexLexer
from .MultiNFA import MultiNFA
from parser_lib import LALRAnalyzerCST, LALRAnalyzerAST
from parser_lib import Grammar
from .Automation import Automation
from .Match import Match

class Regex():
    def __init__(self, file_name):
        with open(file_name, "r") as f:
            txt = f.read()
        self.txt = txt
        self.ids = [int(line.split(":")[0]) for line in txt.split("\n")]
        self.regex_patterns = [(line.split(":")[-1]) for line in txt.split("\n")]
        self.grammar = Grammar.load("src/lexer_lib/regex_grammar.txt")
        self.lexer = RegexLexer(self.grammar.enum)
        self.parser = LALRAnalyzerAST(self.grammar)
        self.automation = Automation()
        self.index = None
        self.to_process = None

    def setAnalize(self, string: str):
        self.to_process = string
        self.index = 0

    def next(self)->None|Match:
        m = self.automation.runFromIndex(self.index, self.to_process)
        if m:
            self.index = m.end_index
        return m


class RegexNFA(Regex):
    def __init__(self, file_name):
        super().__init__(file_name)
        self._compile()

    def _compile(self):
        nfa_builder = NFABuilder()
        nfa_list = []
        for id, regex in zip(self.ids, self.regex_patterns):
            tokens = self.lexer.tokenize(regex)
            print(tokens)
            tree = self.parser.parse(tokens)
            local_nfa = nfa_builder.build(tree, id)
            nfa_list.append(local_nfa)
        self.automation = MultiNFA(nfa_list)

class RegexDFA():
    def __init__(self, file_name):
        pass