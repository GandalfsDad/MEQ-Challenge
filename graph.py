from nodes import Nodes, Node
import random

class Edge:

    def __init__(self, from_node, to_node, label):
        self.from_node = from_node
        self.to_node = to_node
        self.label = label

    def __repr__(self):
        return f"Edge({self.from_node}, {self.to_node}, {self.label})"

class Graph:

    def __init__(self, nodes):
        self.edges = []
        self.__nodes = nodes

    def add_edge(self, from_node, to_node, label):

        if not self.edge_exists(from_node, to_node, label):
            #Don't add the edge if it already exists
            self.edges.append(Edge(from_node, to_node, label))


    def get_descendants(self, node):
        return [edge for edge in self.edges if edge.from_node == node]
    
    def remaining_edges(self, node):
        existing = set([edge.label for edge in self.get_descendants(node)])

        remaining = set([1,2,3]) - existing

        if len(remaining) == 0:
            node.mark_complete()

        return remaining

    def check_completeness(self, node):
        
        descendants = self.get_descendants(node)
        remaining_edges = self.remaining_edges(node)

        #If node is Z then will get reset to A
        if node == self.nodes['Z']:
            return None

        #If there are no descendants we are at a new node and can pick any edge
        if len(descendants) == 0:
            return remaining_edges.pop()

        #If there are 3 descendants we have visited all edges and can check if descendants are complete
        if len(descendants) == 3:

            #If all descendants are complete then mark node as complete and arbitrarily move forward
            if all([descendant.to_node.complete for descendant in descendants]):
                node.mark_complete()
                return random.randint(1,3)
            
            #Else visit the first non-complete descendant
            else:
                for descendant in descendants:
                    if descendant.to_node.complete:
                        continue
                    else:
                        return descendant.label
        
        #Else visit a remaining edge
        else:
            return remaining_edges.pop()

        #If we get here then something has gone wrong   
        raise Exception("No path found")

    def edge_exists(self, from_node, to_node, label):
        return len([edge for edge in self.edges if (edge.from_node == from_node) & (edge.to_node == to_node)& (edge.label == label)])>=1

    def render(self, path):
        with open(path, 'w') as f:
            f.write("digraph {\n")
            for edge in self.edges:
                f.write(f"{edge.from_node.name} -> {edge.to_node.name} [label={edge.label}]\n")

            f.write("}")


    @property
    def is_complete(self):
        return len(self.edges) == 3*25+1
    
    @property
    def nodes(self):
        return self.__nodes
