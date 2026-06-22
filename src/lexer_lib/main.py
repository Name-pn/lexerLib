from parser_lib import LALRAnalyzerCST, LALRAnalyzerAST
from parser_lib import Grammar
from .LexerSymbol import LexerSymbol, LexerSymbolType, EPSILON
from .NFABuilder import NFABuilder
from .RegexLexer import RegexLexer
from .Regex import RegexNFA

gr = Grammar.load("src/lexer_lib/regex_grammar.txt")
lexer = RegexLexer(gr.enum)
parser2 = LALRAnalyzerAST(gr)

string = '(1|2|3)*'
tokens = lexer.tokenize(string)
print(tokens)
tree2 = parser2.parse(tokens)
print('second\n', tree2)
print("copy", tree2)

builder = NFABuilder()
nfa = builder.build(tree2, 0)
print("start: ", nfa.start_state, "end: ", nfa.finite_state, "goto: ", nfa.goto_table)
for index, item in enumerate(nfa.goto_table.items()):
    print(index, item)
test_string = '123'
res = nfa.run(test_string)
print(res.start_index, res.end_index, res.pattern_id, "end ", nfa.finite_state)
regex_controller = RegexNFA('examples/test_lang_grammar.txt')
regex_controller.setAnalize("545abbbba")
print('analize')
print(regex_controller.automation.goto_table)
print("frag", regex_controller.automation.goto_table[0, EPSILON])
regex_controller.setAnalize("123aaaabb")
print("test1 answer true: ", True if regex_controller.automation.run("123") is not None else False)
print("test2 answer true: ", True if regex_controller.automation.run("aaa") is not None else False)
print("test3 answer true: ", True if regex_controller.automation.run("b")  is not None else False)
print("test4 answer false: ", True if regex_controller.automation.run("b123a")  is not None else False)
token = regex_controller.next()
while token:
    print("start: ", token.start_index, " end: ", token.end_index, " id: ", token.pattern_id)
    token = regex_controller.next()

print("Good")