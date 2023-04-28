import networkx as nx
import networkx.algorithms.community as nx_comm
import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt
from tqdm import tqdm
import os
from ingredients_graph_processing import load_graph, save_graph
from colorama import init, Fore, Back, Style


# ################## #
# Analysis Functions #
# ################## #
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


def plot_cset_hist(cset):
    comm_sizes = [len(comm) for comm in cset]
    plt.hist(comm_sizes, 20)
    plt.xlabel('community sizes')
    plt.show()


# ################## #
# Printing Functions #
# ################## #


def print_colored(msg, color=''):
    if color == 'g':
        print(Fore.GREEN + msg + Style.RESET_ALL)
    elif color == 'r':
        print(Fore.RED + msg + Style.RESET_ALL)
    elif color == 'b':
        print(Fore.BLUE + msg + Style.RESET_ALL)
    elif color == 'y':
        print(Fore.YELLOW + msg + Style.RESET_ALL)
    elif color == 'm':
        print(Fore.MAGENTA + msg + Style.RESET_ALL)
    elif color == 'c':
        print(Fore.CYAN + msg + Style.RESET_ALL)
    else:
        print(Style.RESET_ALL + msg)


def print_top_k(G_reduced, v, k=5):
    top_k_nodes = [key for key, value in sorted(v.items(), key=lambda x: x[1], reverse=True)[:k]]
    print(f"The top {k} nodes with the highest degree are: {top_k_nodes}")
    for node in top_k_nodes:
        print(node, ' corresponds to: ', G_reduced.nodes[node]['title'])


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
    if show:
        plt.show()


# ############################# #
# Functions that do many things #
# ############################# #
def analyze_graph(loc, loc_type, top_k=10):
    G = load_graph(loc, loc_type, reduced=True, projI=False, projR=False)
    Gi = load_graph(loc, loc_type, reduced=True, projI=True, projR=False)
    # Gr = load_graph(loc, loc_type, reduced=True, projI=False, projR=True)
    k = top_k

    print_colored('Diameter:', 'g')
    print(diameter(Gi))

    print_colored('Top ' + str(k) + ' in degree centrality: ', 'g')
    degree_cent = degree_centrality(Gi)
    print_top_k(G, degree_cent, k)

    print_colored('Top ' + str(k) + ' in betweenness centrality: ', 'g')
    betweenness = betweenness_centrality(Gi, weighted=True)
    print_top_k(G, betweenness, k)

    plot_degree_dist(Gi, show=True, save=False, save_name='')

    wmin, cmin = 1, 1
    Gi_wc = G_wc(Gi, wmin, cmin)
    cset_wc = detect_comm_write_to_file(G, Gi_wc, wmin, cmin, loc, loc_type)
    print('Number of communities found: ', len(cset_wc))
    plot_cset_hist(cset_wc)
    plt.show()






# #################################################################################################################### #
# MAIN - MAIN - MAIN - MAIN - MAIN - MAIN - MAIN - MAIN - MAIN - MAIN - MAIN - MAIN - MAIN - MAIN - MAIN - MAIN - MAIN #
# #################################################################################################################### #
def main():
    countries = ['Argentine', 'Australian', 'Canadian', 'Chinese',
                 'English', 'French', 'German', 'Greek',
                 'Indian', 'Irish', 'Italian',
                 'Mexican', 'Nigerian', 'Thai', 'US']
    regions = ['Australian', 'Canadian', 'Chinese and Mongolian',
               'French', 'Indian Subcontinent', 'Italian',
               'Mexican', 'South American', 'US']
    continents = ['Asian', 'European', 'Latin American', 'North American']

    for country in countries:
        print_colored(country, 'y')
        analyze_graph(country, loc_type='country_data', top_k=10)
    # for region in regions:
    #     print_colored(region, 'y')
    #     analyze_graph(region, loc_type='region_data', top_k=10)
    # for continent in continents:
    #     print_colored(continent, 'y')
    #     analyze_graph(continent, loc_type='continent_data', top_k=10)

    # degree_sequence = sorted([d for n, d in ingredients_graph.degree()], reverse=True)
    # degree_hist = nx.degree_histogram(ingredients_graph)
    # plt.bar(range(len(degree_hist)), degree_hist)
    # plt.xlabel("Degree")
    # plt.ylabel("Frequency")
    # plt.title("Degree Distribution")
    # plt.show()
    #
    # # get node with highest degree
    # degree_dict = dict(ingredients_graph.degree())
    # node, degree = max(degree_dict.items(), key=lambda x: x[1])
    # print(f"Node {node} has the highest degree of {degree}")
    # print('This corresponds to: ', ig.nodes[node]['title'])
    #
    # k = 10
    # degree_dict = dict(ingredients_graph.degree())
    # top_k_nodes = [key for key, value in sorted(degree_dict.items(), key=lambda x: x[1], reverse=True)[:k]]
    # print(f"The top {k} nodes with the highest degree are: {top_k_nodes}")
    # for node in top_k_nodes:
    #     print('This corresponds to: ', ig.nodes[node]['title'])
    #
    # print('Done')


if __name__ == "__main__":
    main()
