"""
Computes similarity measures between graphs
"""
from copy import deepcopy

import numpy as np
from analysis_functions import modularity
from networkx.algorithms.community import modularity as nx_modularity
from ingredients_graph_processing import load_graph
import os
import pandas as pd
import networkx as nx
import random
from tqdm import tqdm
from plotting_functions import modularity_plot, modularity_bootstrap_plot
from scipy.stats import mode



def tag_graph(G, Gi, df):
    to_remove = []
    for node in Gi.nodes():
        remove = False
        ingredient_name = G.nodes[node]['title']
        nnode = list(G.neighbors(node))[0]  # recipe that uses this ingredient
        recipe_name = G.nodes[nnode]['title']
        df_idx_list = list(df.index[df['recipe title'] == recipe_name])
        ingredient_nutrients = {}
        for df_idx in df_idx_list:
            try:
                row = df.iloc[[df_idx]]
                ingredient_nutrients = list(row['ingredient information'])[0][ingredient_name]
            except:
                to_remove.append(node)
                continue
        if len(ingredient_nutrients) == 0:
            to_remove.append(node)
            remove = True
        else:
            fats = float(ingredient_nutrients['lipid (fat) (g)']) if ingredient_nutrients['lipid (fat) (g)'] != '-' else 0
            carbs = float(ingredient_nutrients['carbohydrates']) if ingredient_nutrients['carbohydrates'] != '-' else 0
            protein = float(ingredient_nutrients['protein (g)']) if ingredient_nutrients['protein (g)'] != '-' else 0
            if fats > carbs and fats > protein:
                nut = 'fats'
            elif carbs > fats and carbs > protein:
                nut = 'carbs'
            elif protein > fats and protein > carbs:
                nut = 'protein'
            else:
                to_remove.append(node)
                remove = True
        if not remove:
            nx.set_node_attributes(Gi, {node: {'title': ingredient_name, 'main nutrient': nut}})

    Gi_new = deepcopy(Gi)
    Gi_new.remove_nodes_from(to_remove)
    return Gi_new


def get_modularity_classes(G):
    classes = {'fats': set(), 'carbs': set(), 'protein': set()}
    for node in G.nodes:
        classes[G.nodes[node]['main nutrient']].add(node)
    return classes


def downsample_graph_nodes(G, frac_remain=0.1):
    nodes = G.nodes()
    n_final = int(np.ceil(len(nodes) * frac_remain))
    downsampled_nodes = random.sample(nodes, n_final)
    G_sampled = G.subgraph(downsampled_nodes)
    return G_sampled


def compute_modularity(loc, loc_type, frac_remain_list, bootstrap=False):
    """
    Computes modularity
    """
    # load and tag the graphs
    G_orig = load_graph(loc, loc_type + '_data', reduced=True, projI=False, projR=False)
    G_i = load_graph(loc, loc_type + '_data', reduced=True, projI=True, projR=False)
    filename = os.path.join(loc_type + "_data", loc)
    df = pd.read_pickle(filename + '.pkl')
    G = tag_graph(G_orig, G_i, df)
    c = get_modularity_classes(G)
    Q_nx = nx_modularity(G, c.values(), weight='weight')

    Q_nx_samp_list = []
    Q_bootstrap = {}
    for frac_remain in frac_remain_list:
        G_samp = downsample_graph_nodes(G, frac_remain=frac_remain)
        c_samp = get_modularity_classes(G_samp)
        Q_nx_samp_list.append(nx_modularity(G_samp, c_samp.values(), weight='weight'))
        if not bootstrap:
            continue
        Q_bootstrap[str(frac_remain)] = []
        for _ in range(10):
            G_samp = downsample_graph_nodes(G, frac_remain=frac_remain)
            c_samp = get_modularity_classes(G_samp)
            Q_bootstrap[str(frac_remain)].append(nx_modularity(G_samp, c_samp.values(), weight='weight'))
    return Q_nx, Q_nx_samp_list, Q_bootstrap


def modularity_analysis(loc_list, loc_type, save_plots, show_plots, bootstrap=False):
    Q = []
    Q_samp_lists = []
    Q_bootstraps = []
    frac_remain_list = [0.5, 0.8, 0.99]
    for _ in frac_remain_list:
        Q_samp_lists.append([])
    for loc in tqdm(loc_list, total=len(loc_list), bar_format='{l_bar}{bar:30}{r_bar}', colour='white'):
        Q_loc, Qsamp_loc, Q_bootstrap = compute_modularity(loc, loc_type, frac_remain_list, bootstrap)
        Q.append(Q_loc)
        for Qs, Qs_loc in zip(Q_samp_lists, Qsamp_loc):
            Qs.append(Qs_loc)
        Q_bootstraps.append(Q_bootstrap)
    if save_plots:
        filename = os.path.join('figures', 'modularity', loc_type + '_' + 'full_vs_sampled.png')
    else:
        filename = None
    legend = ['Q']
    legend.extend(['Q_sampled_' + str(frac) for frac in frac_remain_list])
    y = [Q]
    y.extend(Q_samp_lists)
    modularity_plot(y, loc_list, legend, title='full vs sampled', save_path=filename, show=show_plots)

    if bootstrap:
        bootstrap_trace = {'mode': [], 'min': [], 'max': []}
        bootstrap_traces = {}
        for frac_remain in frac_remain_list:
            bootstrap_traces[str(frac_remain)] = deepcopy(bootstrap_trace)
        for Q_bootstrap in Q_bootstraps:
            for k, vals in Q_bootstrap.items():
                bootstrap_traces[k]['mode'].append(np.mean(vals))
                bootstrap_traces[k]['min'].append(min(vals))
                bootstrap_traces[k]['max'].append(max(vals))
        modularity_bootstrap_plot(Q, bootstrap_traces, loc_list, 'full vs sampled', filename, False)


def main():
    save_plots = True
    show_plots = False
    bootstrap = True
    countries = ['Argentine', 'Australian', 'Canadian', 'Chinese',
                 'English', 'French', 'German', 'Greek',
                 'Indian', 'Irish', 'Italian',
                 'Mexican', 'Nigerian', 'Thai', 'US']
    regions = ['Australian', 'Canadian', 'Chinese and Mongolian',
               'French', 'Indian Subcontinent', 'Italian',
               'Mexican', 'South American', 'US']
    continents = ['Asian', 'European', 'Latin American', 'North American']

    loc_type = 'country'
    modularity_analysis(countries, loc_type, save_plots, show_plots, bootstrap)

    loc_type = 'region'
    modularity_analysis(regions, loc_type, save_plots, show_plots, bootstrap)

    loc_type = 'continent'
    modularity_analysis(continents, loc_type, save_plots, show_plots, bootstrap)


if __name__ == "__main__":
    main()
