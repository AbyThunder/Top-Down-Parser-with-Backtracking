from grammar import input_handler
from parser import parser

def main():
    GRAMMAR, GRAMMAR_original, input_string, input_string_original, non_terminal_symbols, terminal_symbols = input_handler()
    parser(GRAMMAR, GRAMMAR_original, input_string, input_string_original, non_terminal_symbols, terminal_symbols)

main()