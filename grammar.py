import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import string

GRAMMAR_NON_TERMINAL_SEPARATOR = "::="
SEPARATOR = "|"
INPUT_STRING_END_SYMBOL = "$"


def input_handler():
    file_name = get_grammar_file()
    GRAMMAR, non_terminal_symbols, terminal_symbols, GRAMMAR_original = parse_file_to_grammar(file_name)
    input_string, input_string_original = get_input_string(terminal_symbols)
    return GRAMMAR, GRAMMAR_original, input_string, input_string_original, non_terminal_symbols, terminal_symbols

def get_grammar_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    is_txt = Path(file_path).suffix == '.txt'
    print("Provided file: {}".format(file_path))
    
    if not is_txt:
        raise NameError("Grammar file must be in .txt format.")
    
    return file_path

def parse_file_to_grammar(file_path):
    with open(file_path) as f:
        lines = f.readlines()

    GRAMMAR = {}
    GRAMMAR_original = {}
    non_terminal_symbols_original = []
    terminal_symbols_original = []
    n = dict
    for line in lines:
        line = line.strip()
        if line[:2] == "#S":
            line = line.split(GRAMMAR_NON_TERMINAL_SEPARATOR)
            line.pop(0)
            for el in line:
                if '|' in el:
                    raise SyntaxError("Error in starting symbol")
                else:
                    el = el.strip()
                    non_terminal_symbols_original += el
        elif line[:2] == "#N":
            line = line.split(GRAMMAR_NON_TERMINAL_SEPARATOR)
            line.pop(0)
            for el in line:
                if '|' in el:
                    el = el.split(SEPARATOR)
                    el = (x.strip() for x in el)
                    non_terminal_symbols_original += el

        elif line[:2] == "#T":
            line = line.split(GRAMMAR_NON_TERMINAL_SEPARATOR)
            line.pop(0)
            for el in line:
                if '|' in el:
                    el = el.split(SEPARATOR)
                    el = (x.strip() for x in el)
                    terminal_symbols_original += el

        else:
            n = dict(zip(non_terminal_symbols_original, string.ascii_uppercase))
            t = dict(zip(terminal_symbols_original, string.ascii_lowercase))
            line = line.split(GRAMMAR_NON_TERMINAL_SEPARATOR)
            non_terminal = line[0].strip()
            validate_non_terminal(non_terminal, GRAMMAR_original, non_terminal_symbols_original)
            line.pop(0)
            production_rules = []
            production_rules_original = []
            for el in line:
                if non_terminal in el:
                    raise SyntaxError(
                        "Error in non-terminal symbol {}. Left recursion is not supported!".format(non_terminal))

                if '|' in el:
                    el = el.split(SEPARATOR)
                    el = (x.strip() for x in el)
                    validate_production_rule(el, non_terminal)
                    production_rules += el
                    production_rules_original += el
                else:
                    el = el.strip()
                    validate_production_rule(el, non_terminal)
                    production_rules.append(el)
                    production_rules_original.append(el)

            production_rules_original = production_rules.copy()
            GRAMMAR_original[non_terminal] = production_rules_original
            for i in range(len(production_rules)):
                for key in reversed(list(n.keys())):
                    production_rules[i] = production_rules[i].replace(key, n[key])

                for key in reversed(list(t.keys())):
                    production_rules[i] = production_rules[i].replace(key, t[key])
            validate_terminal(production_rules, t, n)
            GRAMMAR[n.get(non_terminal)] = production_rules
    
    print(GRAMMAR_original)
    validate_grammar(GRAMMAR)
    return GRAMMAR, n, t, GRAMMAR_original

def validate_terminal(terminal, t, n):
    rev_dict = dict((v, k) for k, v in t.items())
    rev_dict2 = dict((v, k) for k, v in n.items())
    rev_dict["$"] = "$"
    rev_dict.update(rev_dict2)
    for i in range(len(terminal)):
        for j in range(len(terminal[i])):
            temp = terminal[i]
            if not temp[j] in rev_dict.keys():
                raise SyntaxError("Invalid terminal symbols")

def validate_production_rule(rule, non_terminal):
    if rule == "":
        raise SyntaxError(
            "Error in non-terminal symbol {}. Production rule can not be empty!".format(non_terminal))

def validate_non_terminal(non_terminal, GRAMMAR, non_terminal_symbols):
    if not non_terminal in non_terminal_symbols:
        raise SyntaxError(
            "Error in non-terminal symbol {}. Production rules must start with non-terminal symbols.".format(
                non_terminal))

    if non_terminal in GRAMMAR:
        raise SyntaxError(
            "Non-terminal symbol {} already exists in GRAMMAR!".format(non_terminal))

def validate_grammar(GRAMMAR):
    for key in GRAMMAR:
        production_rules = GRAMMAR[key]
        for production in production_rules:
            for el in production:
                if el.isupper() and not (el in GRAMMAR):
                    raise SyntaxError("Error in {}. Invalid GRAMMAR".format(el))

def get_input_string(t):
    input_string_original = input("Enter input string: ")
    input_string = convert_input_string(input_string_original, t)
    validate_input_string(input_string, t)
    return input_string, input_string_original

def convert_input_string(input_string, t):
    for i in range(len(input_string)):
        for key in t.keys():
            input_string = input_string.replace(key, t[key])
    return input_string

def validate_input_string(input_string, t):
    if input_string == "" or input_string[-1] != INPUT_STRING_END_SYMBOL:
        raise SyntaxError("Invalid input string")
    rev_dict = dict((v, k) for k, v in t.items())
    rev_dict["$"] = "$"
    for i in range(len(input_string)):
        if not input_string[i] in rev_dict.keys():
            raise SyntaxError("Input string contains character: {} outside the terminal symbols".format(input_string[i]))
