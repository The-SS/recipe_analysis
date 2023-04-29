import networkx as nx
import networkx.algorithms.community as nx_comm
import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt
import os


def diameter(G, weighted=False):
    if weighted:
        return nx.diameter(G, weight='weight')
    else:
        return nx.diameter(G)


def betweenness_centrality(G, weighted=True):
    if weighted:
        betweenness = nx.betweenness_centrality(G, k=None, normalized=True, weight='weight', endpoints=False, seed=None)
        return betweenness
    else:
        betweenness = nx.betweenness_centrality(G, k=None, normalized=True, weight=None, endpoints=False, seed=None)
        return betweenness


def degree_centrality(G):
    return dict(G.degree())


def degree_sequence(G):
    """
    returns the degree sequence of G
    """
    return [d for n, d in G.degree()]


def degree_distribution(G, normalize=True):
    """
    Returns the degree distribution of G with the option of normalizing it by the total number of nodes
    """
    deg_sequence = degree_sequence(G)
    max_degree = max(deg_sequence)
    ddist = np.zeros((max_degree+1,))
    for d in deg_sequence:
        ddist[d] += 1
    if normalize:
        ddist = ddist/float(G.number_of_nodes())
    return ddist


def cumulative_degree_distribution(G):
    """
    returns the cumulative degree distribution of G
    """
    ddist = degree_distribution(G)
    cdist = [ddist[k:].sum() for k in range(len(ddist))]
    return cdist


def G_wc(G, wmin, cmin):
    """
    G: graph
    wmin: minimum weight between nodes
    cmin: minimum community size
    """
    # deepcopy of the graph
    G_wc = deepcopy(G)

    # remove edges will low weight
    uv_pairs = []
    for u, v, d in G_wc.edges(data=True):
        if hasattr(d, 'weight') and d['weight'] < wmin:
            uv_pairs.append([u, v])
    for uv in uv_pairs:
        G_wc.remove_edge(uv[0], uv[1])

    print('Number of edges in original graph: ', G.number_of_edges())
    print('Number of edges after removing edges: ', G_wc.number_of_edges())

    # remove nodes in small small components
    comp_gen = nx.connected_components(G_wc)
    nodes_to_remove = []
    for comp in comp_gen:
        if len(comp) < cmin:
            for node in comp:
                nodes_to_remove.append(node)
    for node in nodes_to_remove:
        G_wc.remove_node(node)
    print('Number of nodes in original graph: ', G.number_of_nodes())
    print('Number of nodes after removing nodes: ', G_wc.number_of_nodes())

    return G_wc


def detect_comm_write_to_file(G_reduced, G_wc, wmin, cmin, loc, loc_type):
    cset = list(nx_comm.label_propagation_communities(G_wc))
    comms_file = os.path.join(loc_type, loc + '_ingredients_communities_w' + str(wmin) + '_c' + str(cmin) + '.txt')
    with open(comms_file, 'w') as fout:
        for itr, comm in enumerate(cset):
            comm_titles = ['`' + G_reduced.nodes[c]['title'] + '`' for c in comm]
            fout.write(' '.join(comm_titles))
            if itr < len(cset)-1:
                fout.write('\n')
    return cset


# ###################### #
# Analysis Plotting Fxns #
# ###################### #
def plot_cset_hist(cset):
    comm_sizes = [len(comm) for comm in cset]
    plt.hist(comm_sizes, 20)
    plt.xlabel('community sizes')
    plt.show()




