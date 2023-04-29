import networkx as nx
import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt
from tqdm import tqdm
import os
from nutrients_graph_processing import load_nutri_graph
from printing_functions import print_colored
from plotting_functions import radial_graph_plot, matrix_plot
from itertools import combinations
from graph_processing_funtions import find_degree_one_nodes


# ############################# #
# Functions that do many things #
# ############################# #

def categories(main_nutrients):
    combs_list = list(combinations(main_nutrients, 2))
    combs = combs_list[:]
    for i, comb in enumerate(combs):
        combs[i] = comb[0] + '-' + comb[1]
    return combs, combs_list


def get_loc_weights(loc, loc_type, combs_list, nutrients):
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

    self_vals = {}
    deg_one_nodes = find_degree_one_nodes(G_reduced)
    for node in deg_one_nodes:
        if 'url' in G_reduced.nodes[node]:  # recipe node
            neighbor = list(G_reduced.neighbors(node))[0]
            if neighbor in self_vals:
                self_vals[neighbor] += 1
            else:
                self_vals[neighbor] = 1
    self_vals_nutrients = {}
    for nutrient in nutrients:
        nutrient_id = node_title_dict[nutrient]
        if nutrient_id in self_vals:
            self_vals_nutrients[nutrient] = self_vals[nutrient_id]
        else:
            self_vals_nutrients[nutrient] = 0
    self_vals = list(self_vals_nutrients.values())
    vm = max(max(vals), max(self_vals))
    vals = list(np.array(vals) / vm)
    self_vals = list(np.array(self_vals) / vm)
    return vals, self_vals


def plot_nutrients_analysis(loc_list, loc_type, individual_plots, combs, combs_list,
                            main_nutrients, main_nutrients_labels, save_plots, show_plots, verbose=False):
    vals_dic = {}
    for loc in tqdm(loc_list, total=len(loc_list), bar_format='{l_bar}{bar:30}{r_bar}', colour='white'):
        if verbose:
            print_colored(loc, 'y')
        vals, self_vals = get_loc_weights(loc, loc_type + '_data', combs_list, main_nutrients)
        vals_dic[loc] = vals
        if individual_plots:
            filename_r = 'figures/' + loc_type + '_' + loc + '_nutrients_radar.png'
            filename_m = 'figures/' + loc_type + '_' + loc + '_nutrients_matrix.png'
            title = 'Nutrients for ' + loc_type + ' ' + loc + ' data'
            radial_graph_plot({loc: vals}, combs, title, filename_r, save_plots, show_plots)
            matrix_plot(vals, self_vals, main_nutrients_labels, title, filename_m, save_plots, show_plots)
    filename = 'figures/' + loc_type + '_nutrients_radar.png'
    title = 'Nutrients for ' + loc_type + ' data'
    radial_graph_plot(vals_dic, combs, title, filename, save_plots, show_plots)


# #################################################################################################################### #
# MAIN - MAIN - MAIN - MAIN - MAIN - MAIN - MAIN - MAIN - MAIN - MAIN - MAIN - MAIN - MAIN - MAIN - MAIN - MAIN - MAIN #
# #################################################################################################################### #
def main():
    analyze_country = True
    analyze_region = True
    analyze_continent = True
    individual_plots = True
    save_plots = True
    show_plots = False
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

    if analyze_country:
        plot_nutrients_analysis(countries, 'country', individual_plots, combs, combs_list,
                                main_nutrients, main_nutrients_labels, save_plots, show_plots)

    if analyze_region:
        plot_nutrients_analysis(regions, 'region', individual_plots, combs, combs_list,
                                main_nutrients, main_nutrients_labels, save_plots, show_plots)

    if analyze_continent:
        plot_nutrients_analysis(continents, 'continent', individual_plots, combs, combs_list,
                                main_nutrients, main_nutrients_labels, save_plots, show_plots)


if __name__ == "__main__":
    main()
