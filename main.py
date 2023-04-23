import socket
from nodes import Nodes, Node
from graph import Graph, Edge
from util import generate_uppercase

HOST = "20.28.230.252"  
PORT = 65432  



def main():
    nodes = Nodes()
    nodes.generate_nodes(generate_uppercase())
    nodes['Z'].mark_complete()

    g = Graph(nodes)

    #g = Graph()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        
        #Receive Starting State
        from_node_name = s.recv(1024)
        from_node_name = from_node_name.decode('utf-8').strip()
        
        while not(g.is_complete):
            #If we are at Z then we need to reset to A
            if from_node_name == 'Z':
                to_node_name = s.recv(1024)
                to_node_name = to_node_name.decode('utf-8').strip()
                g.add_edge(nodes[from_node_name], nodes[to_node_name], 'Reset')
                from_node_name = to_node_name

            #Check for direction
            direction = g.get_next_direction(nodes[from_node_name])
            
            #Send direction
            s.sendall(f'{direction}\n'.encode('utf-8'))
            to_node_name = s.recv(1024)
            to_node_name = to_node_name.decode('utf-8').strip()

            #Add edge to graph
            g.add_edge(nodes[from_node_name], nodes[to_node_name], direction)
            from_node_name = to_node_name

    #render
    g.render('output.dot')




if __name__ == '__main__':
    main()