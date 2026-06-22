from parser_lib.Symbol.LTerminal import LTerminal
from parser_lib.Symbol.Terminal import Terminal

class RegexLexer():
    def __init__(self, types):
        self.types = types

    def get_token(self, c):
        match (c):
            case '*':
                return Terminal(self.types['ASTERISK'].name)
            case '|':
                return Terminal(self.types['OR'].name)
            case '(':
                return Terminal(self.types['LEFT_BRACKET'].name)
            case ')':
                return Terminal(self.types['RIGHT_BRACKET'].name)
            case c if 'a' <= c <= 'z' or 'A' <= c <= 'Z' or '0' <= c <= '9':
                return LTerminal(c, self.types['SYMBOL'].name)
            case _:
                raise ValueError(f"Unknown character: {c}")

    def tokenize(self, string):
        res = []
        for c in string:
            res.append(self.get_token(c))
        return res