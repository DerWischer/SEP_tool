import os
import sys
from graphviz import Digraph, ExecutableNotFound

ID_COUNTER = 0

def generate_id():
    global ID_COUNTER
    ID_COUNTER += 1
    return "id_" + str(ID_COUNTER)

class Node:    
    def __init__(self, name):
        self.id = str(generate_id())
        self.name = str(name)

class Edge:
    def __init__(self, from_id, to_id, label):
        self.from_id = str(from_id)
        self.to_id = str(to_id)
        self.label = str(label)

class FileCoupling:
    """ Represents a line of code-maat's coupling analysis log file"""
    def __init__(self, entitiy, coupled, degree, avg_revs):
        self.entitiy = entitiy
        self.coupled = coupled
        self.degree = degree
        self.avg_revs = avg_revs
    def dump(self):
        print (self.entitiy + " & " + self.coupled + " --> " + self.degree)

def read_coupling_csv(path):
    """ Reads the csv file at the specified path and parses the lines to
        FileCoupling objects. Returns a list of parsed objects """
    with open(path) as csv:
        next(csv) # skip first line
        file_couplings = []
        for line in csv:
            entity, coupled, degree, avg_revs = line.split(',')
            fc = FileCoupling(entity, coupled, degree, avg_revs)
            file_couplings.append(fc)
    return file_couplings

def get_nodes_and_edges(file_couplings):
    """ Generate a graph from a list of FileCouling objects """
    node_name_dict = {}
    node_id_dict = {}
    edge_list = []
    for entry in file_couplings:
        from_node = get_or_create_node(node_name_dict, entry.entitiy)
        to_node = get_or_create_node(node_name_dict, entry.coupled)

        node_id_dict[from_node.id] = from_node
        node_id_dict[to_node.id] = to_node
        edge_list.append(Edge(from_node.id, to_node.id, entry.degree + "%"))        
    return node_id_dict, edge_list

def get_or_create_node(node_dict, name):
    """ Checks whether a node with the specified name exists in the
        dictionary. If not, a new node is created. Always returns a node. """
    node = node_dict.get(name)
    if not node:
        node = Node(name)
        node_dict[name] = node
    return node

def generate_graph(nodes, edges):
    """ Take a dictionary of nodes (id, node-object) and a list of edge-objects. 
        Returns a Digraph."""
    dot = Digraph(comment="My comment")
    for node_id, node in nodes.items():
        dot.node(node_id, node.name)
    for edge in edges:
        dot.edge(edge.from_id, edge.to_id, edge.label)
    return dot

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print ("Error: Please specify the path to the csv")
        exit(1)

    csv_path = sys.argv[1] 
    
    couplings = read_coupling_csv(csv_path)
    nodes, edges = get_nodes_and_edges(couplings)    
    graph = generate_graph(nodes, edges) # TODO Apply filtering options
    try:
        graph.render('rendered/graph.gv', view=True)
    except ExecutableNotFound as ex:
        print("Error: Executable not found. Install GraphViz and add it to your PATH.")
    except Exception as ex:
        print("Error: Not handled")
        print (ex)
