import networkx as nx
import networkx.algorithms.community as nx_comm
import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt
from tqdm import tqdm
import os
from ingredients_graph_processing import load_graph, save_graph
from colorama import init, Fore, Back, Style
from analysis_functions import *
from printing_functions import print_colored


def analyze_graph(loc, loc_type, top_k=10, show=True, save=False):
    G = load_graph(loc, loc_type, reduced=True, projI=False, projR=False)
    Gi = load_graph(loc, loc_type, reduced=True, projI=True, projR=False)
    k = top_k

    print_colored('Diameter:', 'g')
    diam = diameter(Gi)
    print(diam)

    print_colored('Top ' + str(k) + ' in degree centrality: ', 'g')
    degree_cent1 = degree_centrality(Gi)
    res1 = print_top_k(G, degree_cent1, k, verbose=False)
    if save:
        filename = os.path.join('results', 'degree_centrality', loc_type + '_ ' + loc + '_dc.txt')
        with open(filename, 'w') as f:
            for line in res1:
                f.write(f"{line}\n")

    print_colored('Top ' + str(k) + ' in betweenness centrality: ', 'g')
    betweenness1 = betweenness_centrality(Gi, weighted=True)
    res3 = print_top_k(G, betweenness1, k, verbose=False)
    if save:
        filename = os.path.join('results', 'betweenness_centrality', loc_type + '_ ' + loc + '_bc.txt')
        with open(filename, 'w') as f:
            for line in res3:
                f.write(f"{line}\n")

    filename = os.path.join('figures', 'degree_dist', loc_type + '_ ' + loc + '_dd.png')
    plot_degree_dist(Gi, show=show, save=save, save_name=filename)

    # wmin, cmin = 3, 3
    # Gi_wc = G_wc(Gi, wmin, cmin)
    # cset_wc = detect_comm_write_to_file(G, Gi_wc, wmin, cmin, loc, loc_type, name='normal')
    # print('Number of communities found: ', len(cset_wc))
    # filename = os.path.join('figures', 'communities', loc_type + '_ ' + loc + '.png')
    # plot_cset_hist(cset_wc, show, save, filename)
    return diam


# def common_ingredients():
#     ingredients = {
#         "6758": "water",
#         '8147': 'salt',
#         "7340": "pepper",
#         "8937": "black pepper",
#         "6647": "garlic",
#         '6848': "garlic clove",
#         '6448': 'onion',
#         '6190': "sugar",
#         '6145': "flour",
#         '8739': "oil",
#         '7740': "purpose flour"
#     }
#     return ingredients, ingredients.keys()
#
#
# def remove_common_ingredients(G):
#     _, nodes = common_ingredients()
#     G_ = deepcopy(G)
#     for node in nodes:
#         if G_.has_node(node):
#             G_.remove_node(node)
#     return G_


# #################################################################################################################### #
# MAIN - MAIN - MAIN - MAIN - MAIN - MAIN - MAIN - MAIN - MAIN - MAIN - MAIN - MAIN - MAIN - MAIN - MAIN - MAIN - MAIN #
# #################################################################################################################### #
def main():
    analyze_country = True
    analyze_region = True
    analyze_continent = True
    save_data = True
    show_plots = False
    top_k = 50
    countries = ['Argentine', 'Australian', 'Canadian', 'Chinese',
                 'English', 'French', 'German', 'Greek',
                 'Indian', 'Irish', 'Italian',
                 'Mexican', 'Nigerian', 'Thai', 'US']
    regions = ['Australian', 'Canadian', 'Chinese and Mongolian',
               'French', 'Indian Subcontinent', 'Italian',
               'Mexican', 'South American', 'US']
    continents = ['Asian', 'European', 'Latin American', 'North American']

    if analyze_country:
        all_diam = []
        for loc in countries:
            print_colored(loc, 'y')
            diam = analyze_graph(loc, loc_type='country_data', top_k=top_k, show=show_plots, save=save_data)
            all_diam.append(loc + ": " + str(diam))
        if save_data:
            filename = os.path.join('results', 'diameter', 'country_data_diam.txt')
            with open(filename, 'w') as f:
                for line in all_diam:
                    f.write(f"{line}\n")
    if analyze_region:
        all_diam = []
        for loc in regions:
            print_colored(loc, 'y')
            analyze_graph(loc, loc_type='region_data', top_k=top_k, show=show_plots, save=save_data)
            all_diam.append(loc + ": " + str(diam))
        if save_data:
            filename = os.path.join('results', 'diameter', 'region_data_diam.txt')
            with open(filename, 'w') as f:
                for line in all_diam:
                    f.write(f"{line}\n")
    if analyze_continent:
        all_diam = []
        for loc in continents:
            print_colored(loc, 'y')
            analyze_graph(loc, loc_type='continent_data', top_k=top_k, show=show_plots, save=save_data)
            all_diam.append(loc + ": " + str(diam))
        if save_data:
            filename = os.path.join('results', 'diameter', 'continent_data_diam.txt')
            with open(filename, 'w') as f:
                for line in all_diam:
                    f.write(f"{line}\n")


if __name__ == "__main__":
    main()
