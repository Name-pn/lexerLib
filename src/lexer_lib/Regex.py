from .NFABuilder import NFABuilder
from .RegexLexer import RegexLexer
from .MultiNFA import MultiNFA
from parser_lib import LALRAnalyzerCST, LALRAnalyzerAST
from parser_lib import Grammar
from .Automation import Automation
from .Match import Match

def delete_comments(string):
    return '\n'.join([line for line in string.split("\n") if len(line) > 0 and line[0] != '#'])


class Regex():
    def __init__(self, file_name):
        with open(file_name, "r") as f:
            txt = f.read()
        self.txt = txt
        self.txt = delete_comments(self.txt)
        self.ids = [int(line.split(":")[0]) for line in self.txt.split("\n") if ':' in line]
        self.regex_patterns = [(line.split(":")[-1]) for line in self.txt.split("\n") if ':' in line]
        self.regex_vars = [line.split("=")[0] for line in self.txt.split("\n") if '=' in line]
        self.regex_defs = [line.split("=")[-1] for line in self.txt.split("\n") if '=' in line]
        self.vars_to_def = {}
        for var, r_def in zip(self.regex_vars, self.regex_defs):
            self.vars_to_def[var] = "(" + r_def + ")"
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
            for index, token in enumerate(tokens):
                if token.ttype == "NAME":
                    tokens = tokens[:index] + self.lexer.tokenize(self.vars_to_def[token.lexem]) + tokens[index + 1:]

            print(tokens)
            tree = self.parser.parse(tokens)
            local_nfa = nfa_builder.build(tree, id)
            nfa_list.append(local_nfa)
        self.automation = MultiNFA(nfa_list)

class RegexDFA():
    def __init__(self, file_name):
        pass