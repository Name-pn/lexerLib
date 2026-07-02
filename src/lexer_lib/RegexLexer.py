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
        if len(c) > 1:
            return LTerminal(c, self.types['NAME'].name)
        match (c):
            case '*':
                return Terminal(self.types['ASTERISK'].name)
            case '|':
                return Terminal(self.types['OR'].name)
            case '(':
                return Terminal(self.types['LEFT_BRACKET'].name)
            case ')':
                return Terminal(self.types['RIGHT_BRACKET'].name)
            case '{':
                return Terminal(self.types['LEFT_CURLY_BRACKET'].name)
            case '}':
                return Terminal(self.types['RIGHT_CURLY_BRACKET'].name)
            case c if 0 <= ord(c) <= 255:
                return LTerminal(c, self.types['SYMBOL'].name)
            case _:
                raise ValueError(f"Unknown character: {c}")
            
    def get_escape(self, c):
        return LTerminal(c, self.types['SYMBOL'].name)

    def get_name_string(self, string: str, index: int):
        res = ""
        if len(string) > index and (string[index] >= 'a' and string[index] <= 'z' or\
            string[index] >= 'A' and string[index] <= 'Z' or string[index] == '_'):
            res = res + (string[index])
            index += 1
        while len(string) > index and (string[index] >= 'a' and string[index] <= 'z' or\
            string[index] >= 'A' and string[index] <= 'Z' or\
            string[index] >= '0' and string[index] <= '9' or string[index] == '_'):
            res = res + (string[index])
            index += 1
        if not res:
            raise SyntaxError("Empty regex name calling")
        if len(string) <= index or string[index] != '}':
            raise SyntaxError("There isnt closing curly bracket")
        return res, index

    def tokenize(self, string):
        res = []
        index = 0
        while index < len(string):
            if string[index] == "\\":
                index += 1
                if index >= len(string):
                    raise SyntaxError("After \\ must be symbol")
                char = self.ESCAPE_MAP.get(string[index], string[index])
                res.append(self.get_escape(char))
            elif string[index] == "{":
                index += 1
                name, index = self.get_name_string(string, index)
                #res.append(self.get_token('{'))
                res.append(self.get_token(name))
                #res.append(self.get_token('}'))
            else:
                char = string[index]
                res.append(self.get_token(char))
            index += 1
        return res