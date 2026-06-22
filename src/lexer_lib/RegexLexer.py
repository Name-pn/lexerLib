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
            case c if 0 <= ord(c) <= 255:
                return LTerminal(c, self.types['SYMBOL'].name)
            case _:
                raise ValueError(f"Unknown character: {c}")

    def tokenize(self, string):
        res = []
        index = 0
        while index < len(string):
            if string[index] != "\\":
                res.append(self.get_token(string[index]))
            else:
                index += 1
                if index >= len(string):
                    raise Exception("After \\ must be special symbol")
                res.append(LTerminal(string[index], self.types['SYMBOL'].name))
            index += 1
        return res