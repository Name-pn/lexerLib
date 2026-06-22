from lexer_lib import RegexNFA

regex_controller = RegexNFA('examples/test_lang_grammar.txt')
print('analize')
regex_controller.automation.pretty_print_grouped()
regex_controller.setAnalize("123aaaabb()")
token = regex_controller.next()
while token:
    print("start: ", token.start_index, " end: ", token.end_index, " id: ", token.pattern_id)
    token = regex_controller.next()

print("Good")