from tree import Node

def parser(GRAMMAR, GRAMMAR_original, input, input_original, non_terminal_symbols, terminal_symbols,):
    print("\nProvided contex-free grammar:")
    print(GRAMMAR_original)
    print("\nProvided input string:", input_original)

    if GRAMMAR != {}:
        out, parse_tree, match, input_iter = rec_parse(
            GRAMMAR, "A", input, 0, "", Node("A"), [], 0, non_terminal_symbols, terminal_symbols, GRAMMAR_original, input_original)
        print("\n\nEnd of input parsing")
        
        if match == True and (out == input or out == input[:-1]) and parse_tree != []:
            print("Input string accepted by the GRAMMAR\n")
            combine = {}
            combine.update(terminal_symbols)
            combine.update(non_terminal_symbols)
            combine["$"] = "$"
            print_parse_tree(parse_tree, non_terminal_symbols, combine)
            
        else:
            print("Input string not accepted by the GRAMMAR.\n")

def rec_parse(GRAMMAR, nonterminal, input, input_iter, out, node, parse_tree, matched, non_terminal_symbols, terminal_symbols, GRAMMAR_original, input_original):
    rules = GRAMMAR[nonterminal]
    match = False
    key = [k for k, v in non_terminal_symbols.items() if v == nonterminal][0]
    print("-----------------------------------")
    print("GRAMMAR: " + key)
    r = GRAMMAR_original[key]
    parse_tree.append(node)
    
    for rule in rules:
        match = False
        matched = 0
        
        for i in range(len(rule)):
            node.add_children(rule[i])
            combine = {}
            combine.update(terminal_symbols)
            combine.update(non_terminal_symbols)
            combine["$"] = "$"
            print_parse_tree(parse_tree, non_terminal_symbols, combine)
            st = convert_input_string(input_original, terminal_symbols)
            st = st.split("|")
            print("Current production rule {} : {}".format(key, r[rules.index(rule)]))
            print("Current input character: " + st[input_iter])
            
            if rule[i].isupper() == True:                
                out, parse_tree, match, input_iter = rec_parse(
                    GRAMMAR, rule[i], input, input_iter, out, Node(rule[i]), parse_tree, matched, non_terminal_symbols, terminal_symbols, GRAMMAR_original, input_original)
                
                if out == input[:-1] and match == True:
                    match = True
                    return out, parse_tree, match, input_iter
                
            else:
                if rule[i] == input[input_iter]:
                    out = out + rule[i]
                    input_iter += 1
                    matched += 1
                    match = True
                    
                elif rule[i] == '$':
                    match = True
                    continue
                
                else:
                    print("\t\tBacktracking...")
                    for el in range(matched):
                        out = out.replace(out[el], "")
                        input_iter = input_iter - 1
                    node.remove_children()
                    match = False
                    matched = 0
                    break

        if (out == input[:-1] or out == input or input == '$') and match == True:  
            return out, parse_tree, match, input_iter

    return out, parse_tree, match, input_iter

def print_parse_tree(parse_tree, n, t):
    for el in parse_tree:
        if el.children == []:
            parse_tree.remove(el)

    if len(parse_tree) == 0:
        return

    print("\n-------------------------    PARSE TREE      -------------------------")
    for el in parse_tree:
        el.print_node(n, t)
    print("----------------------------------------------------------------------\n")

def convert_input_string(input_string, t):    
    for key in t.keys():
        input_string = input_string.replace(key, key + "|")
    return input_string
