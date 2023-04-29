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


def analyze_graph(loc, loc_type, top_k=10, save=False):
    G = load_graph(loc, loc_type, reduced=True, projI=False, projR=False)
    Gi = load_graph(loc, loc_type, reduced=True, projI=True, projR=False)
    # Gr = load_graph(loc, loc_type, reduced=True, projI=False, projR=True)
    k = top_k

    print_colored('Diameter:', 'g')
    print(diameter(Gi))

    print_colored('Top ' + str(k) + ' in degree centrality: ', 'g')
    degree_cent = degree_centrality(Gi)
    res = print_top_k(G, degree_cent, k)
    # TODO: add saving res to text file

    print_colored('Top ' + str(k) + ' in betweenness centrality: ', 'g')
    betweenness = betweenness_centrality(Gi, weighted=True)
    res = print_top_k(G, betweenness, k)
    # TODO: add saving res to text file

    plot_degree_dist(Gi, show=True, save=False, save_name='')
    # TODO: add saving plots

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
    analyze_country = True
    analyze_region = False
    analyze_continent = False
    save_data = True
    countries = ['Argentine', 'Australian', 'Canadian', 'Chinese',
                 'English', 'French', 'German', 'Greek',
                 'Indian', 'Irish', 'Italian',
                 'Mexican', 'Nigerian', 'Thai', 'US']
    # countries = ['Argentine']
    regions = ['Australian', 'Canadian', 'Chinese and Mongolian',
               'French', 'Indian Subcontinent', 'Italian',
               'Mexican', 'South American', 'US']
    continents = ['Asian', 'European', 'Latin American', 'North American']

    if analyze_country:
        for country in countries:
            print_colored(country, 'y')
            analyze_graph(country, loc_type='country_data', top_k=10, save=save_data)
    if analyze_region:
        for region in regions:
            print_colored(region, 'y')
            analyze_graph(region, loc_type='region_data', top_k=10, save=save_data)
    if analyze_continent:
        for continent in continents:
            print_colored(continent, 'y')
            analyze_graph(continent, loc_type='continent_data', top_k=10, save=save_data)


if __name__ == "__main__":
    main()
