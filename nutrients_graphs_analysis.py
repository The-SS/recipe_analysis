import networkx as nx
import networkx.algorithms.community as nx_comm
import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt
from tqdm import tqdm
import os
from nutrients_graph_processing import load_nutri_graph, save_graph
from colorama import init, Fore, Back, Style
from radar_chart import radial_graph_plot
from itertools import combinations



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
def get_loc_weights(loc, loc_type, combs_list):
    G_reduced = load_nutri_graph(loc, loc_type, reduced=True, projN=False, projR=False)
    G = load_nutri_graph(loc, loc_type, reduced=True, projN=True, projR=False)
    nutrient_ids = []
    for node in G.nodes():
        nutrient_ids.append(node)
    node_title_dict = {}
    for node_id in nutrient_ids:
        node_title_dict[G_reduced.nodes[node_id]['title']] = node_id

    vals = []
    for comb in combs_list:
        try:
            v = G[node_title_dict[comb[0]]][node_title_dict[comb[1]]]['weight']
        except:
            v = 0
        vals.append(v)
    vm = max(vals)
    vals = list(np.array(vals) / vm)
    return vals


def categories(main_nutrients):
    combs_list = list(combinations(main_nutrients, 2))
    combs = combs_list[:]
    for i, comb in enumerate(combs):
        combs[i] = comb[0] + '-' + comb[1]
    return combs, combs_list


def plot_fig(vals, combs, title, filename, save):
    radial_graph_plot(vals, combs, title, filename, save)


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

    main_nutrients = ['Total fats (g)', 'Protein (g)', 'Carbohydrates (g)',
                      'Sugars, total (g)', 'Fiber, total dietary (g)']
    main_nutrients_labels = ['Proteins', 'Carbs', 'Fats', 'Fiber', 'Sugar']

    _, combs_list = categories(main_nutrients)
    combs, _ = categories(main_nutrients_labels)

    vals_dic = {}
    for loc in countries:
        print_colored(loc, 'y')
        vals = get_loc_weights(loc, 'country_data', combs_list)
        vals_dic[loc] = vals
        # filename = 'figures/country_' + loc + '_nutrients.png'
        # title = 'Nutrients for country ' + loc + ' data'
        # plot_fig({loc: vals}, combs, title, filename, save=True)
    filename = 'figures/country_nutrients.png'
    title = 'Nutrients for country data'
    plot_fig(vals_dic, combs, title, filename, save=True)

    vals_dic = {}
    for loc in regions:
        print_colored(loc, 'y')
        vals = get_loc_weights(loc, 'region_data', combs_list)
        vals_dic[loc] = vals
        # filename = 'figures/region_' + loc + '_nutrients.png'
        # title = 'Nutrients for region ' + loc + ' data'
        # plot_fig({loc: vals}, combs, title, filename, save=True)
    filename = 'figures/region_nutrients.png'
    title = 'Nutrients for regions data'
    plot_fig(vals_dic, combs, title, filename, save=True)

    vals_dic = {}
    for loc in continents:
        print_colored(loc, 'y')
        vals = get_loc_weights(loc, 'continent_data', combs_list)
        vals_dic[loc] = vals
        # filename = 'figures/continent_' + loc + '_nutrients.png'
        # title = 'Nutrients for continent ' + loc + ' data'
        # plot_fig({loc: vals}, combs, title, filename, save=True)
    filename = 'figures/continent_nutrients.png'
    title = 'Nutrients for continents data!'
    plot_fig(vals_dic, combs, title, filename, save=True)

    # print('Done')


if __name__ == "__main__":
    main()
