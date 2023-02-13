class Node:
    def __init__(self, symbol):
        self.symbol = symbol
        self.children = []

    def add_children(self, node):
        self.children.append(node)

    def remove_children(self):
        self.children = []

    def print_node(self, n, t):
        print("symbol: ", list(n.keys())[list(n.values()).index(self.symbol)])
        rev_dict = dict((v,k) for k,v in t.items())
        print("children: ", [rev_dict[elem] for elem in self.children])
    