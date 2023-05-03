import networkx as nx
import networkx.algorithms.community as nx_comm
import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt
import os


def diameter(G, weighted=False):
    """
    Finds the diameter of a networkx graph
    """
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
    ddist = np.zeros((max_degree + 1,))
    for d in deg_sequence:
        ddist[d] += 1
    if normalize:
        ddist = ddist / float(G.number_of_nodes())
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
        if 'weight' in d.keys() and d['weight'] < wmin:
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


def detect_comm_write_to_file(G_reduced, G_wc, wmin, cmin, loc, loc_type, name=''):
    cset = list(nx_comm.label_propagation_communities(G_wc))
    comms_file = os.path.join(loc_type,
                              loc + '_ingredients_communities_w' + str(wmin) + '_c' + str(cmin) + '_' + name + '.txt')
    with open(comms_file, 'w') as fout:
        for itr, comm in enumerate(cset):
            comm_titles = ['`' + G_reduced.nodes[c]['title'] + '`' for c in comm]
            fout.write(' '.join(comm_titles))
            if itr < len(cset) - 1:
                fout.write('\n')
    return cset


def modularity(G, c):
    d = dict()
    for k, v in enumerate(c):
        for n in v:
            d[n] = k
    L = 0
    for u, v, data in G.edges.data():
        L += data['weight']
    Q, Qmax = 0, 1
    for u in G.nodes():
        for v in G.nodes():
            if d[u] == d[v]:
                Auv = 0
                if G.has_edge(v, u):
                    Auv = G[v][u]['weight']
                Q += (Auv - G.in_degree(u, weight='weight') * G.out_degree(v, weight='weight') / L) / L
                Qmax -= (G.in_degree(u, weight='weight') * G.out_degree(v, weight='weight') / L) / L
    return Q, Qmax


def scalar_assortativity(G, d):
    x = np.zeros(G.number_of_nodes())
    for i, n in enumerate(G.nodes()):
        x[i] = d[n]

    A = np.array(nx.adjacency_matrix(G).todense().T)
    M = 2 * A.sum().sum()
    ki = A.sum(axis=1)  # row sum is in-degree
    ko = A.sum(axis=0)  # column sum is out-degree
    mu = (np.dot(ki, x) + np.dot(ko, x)) / M

    R, Rmax = 0, 0
    for i in range(G.number_of_nodes()):
        for j in range(G.number_of_nodes()):
            R += (A[i, j] * (x[i] - mu) * (x[j] - mu)) / M
            Rmax += (A[i, j] * (x[i] - mu) ** 2) / M

    return R, Rmax


# ############################### #
# Analysis Plotting/Printing Fxns #
# ############################### #
def plot_cset_hist(cset, show, save, filename):
    comm_sizes = [len(comm) for comm in cset]
    plt.hist(comm_sizes, 20)
    plt.xlabel('community sizes')
    if save:
        plt.savefig(filename)
    if show:
        plt.show()
    else:
        plt.close()


def print_top_k(G_reduced, v, k=5, verbose=True):
    """
    G_reduced: networkx graph that contains recipes with titles
    v: dictionary of node labels and some associated value (e.g. centrality) to sort the nodes
    k: number of nodes with the highest values in v to print
    """
    result = []
    top_k_nodes = [key for key, value in sorted(v.items(), key=lambda x: x[1], reverse=True)[:k]]
    top_k_values = [value for key, value in sorted(v.items(), key=lambda x: x[1], reverse=True)[:k]]
    if verbose:
        print(f"The top {k} nodes with the highest degree are: {top_k_nodes}")
    result.append("The top " + str(k) + " nodes with the highest degree are: ")
    for i, node in enumerate(top_k_nodes):
        if verbose:
            print(node, ' corresponds to: ', G_reduced.nodes[node]['title'])
        result.append(str(node) + ': ' + G_reduced.nodes[node]['title'] + ' (' + str(top_k_values[i]) + ')')
    return result


def plot_degree_dist(G, show=True, save=False, save_name=''):
    ddist = degree_distribution(G, normalize=False)
    cdist = cumulative_degree_distribution(G)
    k = np.arange(len(ddist))

    plt.figure(figsize=(8, 12))
    plt.subplot(211)
    plt.bar(k, ddist, width=0.8, bottom=0, color='b')

    plt.subplot(212)
    plt.loglog(k, cdist)
    plt.grid(True)
    if save:
        plt.savefig(save_name)
    if show:
        plt.show()
    else:
        plt.close()
