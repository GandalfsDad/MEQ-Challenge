class Nodes:

    def __init__(self, initial_nodes=None):
        self.__nodes = {}

        if initial_nodes:
            for node in initial_nodes:
                self.add(node)

    def add(self, node):
        self.__nodes[node.name] = node

    def generate_nodes(self, names):
        for name in names:
            self.add(Node(name))

    def __getitem__(self, index):
        return self.__nodes[index]
    
    def __str__(self):
        return str(self.__nodes)
    
    def __repr__(self):
        return f"Nodes({[node for node in self.__nodes.values()]})"


class Node:
    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        return self.__name

    def __str__(self):
        return self.__name
    
    def __repr__(self):
        return  f"Node('{self.__name}')"