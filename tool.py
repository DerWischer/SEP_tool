import os
import sys
from graphviz import Graph, ExecutableNotFound
import subprocess
import shutil
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
        FileCoupling objects. Returns a list of parsed objects. """
    with open(path) as csv:
        next(csv) # skip first line
        file_couplings = []
        for line in csv:
            entity, coupled, degree, avg_revs = line.split(',')
            fc = FileCoupling(entity, coupled, degree, avg_revs)
            file_couplings.append(fc)
    return file_couplings

def get_nodes_and_edges(file_couplings, minDegree):
    """ Takes a list of FileCoupling objects and return a dictionary of nodes (id, node-object)
        and a list of edge-objects.
        > Excludes any nodes below minDegree"""
    node_name_dict = {}
    node_id_dict = {}
    edge_list = []
    for entry in file_couplings:

        from_node = get_or_create_node(node_name_dict, entry.entitiy)
        to_node = get_or_create_node(node_name_dict, entry.coupled)

        if (entry.degree >= str(minDegree)):

            node_id_dict[from_node.id] = from_node
            node_id_dict[to_node.id] = to_node
            edge_list.append(Edge(from_node.id, to_node.id, entry.degree + "%"))        
    return node_id_dict, edge_list

def get_or_create_node(nodes, name):
    """ Checks whether a node with the specified name exists in the
        dictionary. If not, a new node is created. 
        > Always returns a node."""
    node = nodes.get(name)
    if not node:
        node = Node(name)
        nodes[name] = node
    return node

def filter_nodes_and_edges(nodes, edges, filesOfInterest = None, minDegree = None):
    """ Filters the node dictionairy and the list of edges.
        > fileOfInterest: Array of filenames that shall be included in the graph.
        
        > minDegree: Number of the minimum degree of dependency between two file."""
    # Edge (A -> B, degree)
    # TODO fileOfInterest filter: Node A's filename must appear in filesOfInterest. If not, remove from node and edges
    # TODO minDegree: Remove all edges with a degree less than minDegree    
    return nodes, edges


def generate_graph(nodes, edges):
    """ Takes a dictionary of nodes and a list of edges. 
        > Returns a Digraph."""
    dot = Graph(comment="My comment")
    for node_id, node in nodes.items():
        dot.node(node_id, node.name)
    for edge in edges:
        dot.edge(edge.from_id, edge.to_id, edge.label)
    return dot

def cleanup_directory():
    if os.path.exists("analysis"):
        shutil.rmtree('analysis')

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print ("Usage error\n\tArg 1 > Path to the git repository.\n\tArg 2> Minimum degree of coupling. Integer 0-100. (optional)")
        exit(1)
    if not os.path.exists("analysis"):
        os.mkdir("analysis")

    path_repo = os.path.join(sys.argv[1], ".git")
    path_gitlog = os.path.join("analysis", "gitlog.log")
    path_coupling = os.path.join("analysis", "coupling.csv")
    path_codemaat = os.path.join("code-maat", "code-maat.jar")

    # Generate git log and save to file
    with open(path_gitlog, 'w') as f_gitlog:
        subprocess.call(["git", "--git-dir", path_repo, "log", "--all", "--numstat", "--date=short", "--pretty=format:--%h--%ad--%aN", "--no-renames"], stdout=f_gitlog)
    # Perform coupling analysis with code maat and save to file
    with open(path_coupling, 'w') as f_coupling:
        subprocess.call(["java", "-jar",  path_codemaat, "-l", path_gitlog, "-c", "git2", "-a", "coupling"], stdout=f_coupling)
    
    min_degree = 30
    if len(sys.argv) == 3:
        min_degree = sys.argv[2]
    
    couplings = read_coupling_csv(path_coupling)
    
    nodes, edges = get_nodes_and_edges(couplings, min_degree) 
    #nodes, edges = filter_nodes_and_edges(nodes, edges)
    
    graph = generate_graph(nodes, edges)
    try:
        graph.render('rendered/graph.gv', view=True)
    except ExecutableNotFound as ex:
        print("Error: Executable not found. Install GraphViz and add it to your PATH.")
    except Exception as ex:
        print("Error: Not handled")
        print (ex)
    finally:
        cleanup_directory()
