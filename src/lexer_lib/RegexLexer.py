from parser_lib.Symbol.LTerminal import LTerminal
from parser_lib.Symbol.Terminal import Terminal

class RegexLexer():
    ESCAPE_MAP = {
        'n': '\n',
        't': '\t',
        'r': '\r',
        #'\\': '\\',
    }

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
            
    def get_escape(self, c):
        return LTerminal(c, self.types['SYMBOL'].name)

    def tokenize(self, string):
        res = []
        index = 0
        while index < len(string):
            is_escape = False
            if string[index] != "\\":
                char = string[index]
            else:
                is_escape = True
                index += 1
                if index >= len(string):
                    raise SyntaxError("After \\ must be symbol")
                char = self.ESCAPE_MAP.get(string[index], string[index]) 
            if is_escape:
                res.append(self.get_escape(char))
            else:
                res.append(self.get_token(char))
            index += 1
        return res