from .NFABuilder import NFABuilder
from .RegexLexer import RegexLexer
from .MultiNFA import MultiNFA
from parser_lib import LALRAnalyzerCST, LALRAnalyzerAST
from parser_lib import Grammar
from .Automation import Automation
from .Match import Match

def delete_comments(string):
    return '\n'.join([line.strip() for line in string.split("\n") if len(line) > 0 and line[0] != '#'])


class Regex():
    def add_reg_pattern(self, line):
        self.ids.append(int(line.split(":", 1)[0])) 
        self.regex_patterns.append(line.split(":", 1)[1])

    def add_reg_def(self, line):
        regex_var_name, regex_var_def = line.split("=", 1)
        self.regex_vars.append(regex_var_name)
        self.regex_defs.append(regex_var_def)

    def __init__(self, file_name):
        with open(file_name, "r") as f:
            txt = f.read()
        self.txt = txt
        self.txt = delete_comments(self.txt)

        self.ids = []
        self.regex_patterns = []
        self.regex_vars = []
        self.regex_defs = []

        for line in self.txt.split('\n'):
            n = len(line)
            eq_pos = line.find('=')
            if eq_pos == -1:
                eq_pos = n
            colon_pos = line.find(':')
            if colon_pos == -1:
                colon_pos = n
            if colon_pos == n and eq_pos == n:
                raise SyntaxError("There aren`t colon and equal symbol")
            if eq_pos < colon_pos:
                self.add_reg_def(line)
            else:
                self.add_reg_pattern(line)

        self.vars_to_def = {}
        for var, r_def in zip(self.regex_vars, self.regex_defs):
            if var not in self.vars_to_def:
                self.vars_to_def[var] = "(" + r_def + ")"
            else:
                raise ValueError(f"Redefine regex definition {var}")

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
            tokens_after_replace = []
            for token in tokens:
                if token.ttype == "NAME":
                    tokens_after_replace.extend(self.lexer.tokenize(self.vars_to_def[token.lexem]))
                else:
                    tokens_after_replace.append(token)    
            tree = self.parser.parse(tokens_after_replace)
            local_nfa = nfa_builder.build(tree, id)
            nfa_list.append(local_nfa)
        self.automation = MultiNFA(nfa_list)

class RegexDFA():
    def __init__(self, file_name):
        pass