

def find_degree_one_nodes(G):
    # Calculate the degree of each node in the graph
    degree_dict = dict(G.degree())

    # Identify the nodes with degree one
    degree_one_nodes = [node for node, degree in degree_dict.items() if degree == 1]

    return degree_one_nodes
