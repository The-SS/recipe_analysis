import networkx as nx
import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt
from tqdm import tqdm
import os


# ########################## #
# Graph processing functions #
# ########################## #
def get_all_other_nutrients(G, main_nutrients):
    """
    returns a list of all nutrients that are not in the list of passed main nutrients
    """
    to_remove = set()
    for node in G.nodes:  # loop through nodes
        if 'url' not in G.nodes[node] and G.nodes[node]['title'] not in main_nutrients:
            # node is a nutrient AND nutrient is not one of the main_nutrients
            to_remove.add(node)
    return to_remove


def get_all_recipes_not_in_ingredients_graph(G, G_ing):
    """
    returns a list of all recipes that are not in the ingredients graph
    """
    to_remove = set()
    chosen_recipes = set()
    for node in G_ing:
        if 'url' in G_ing.nodes[node]:  # chosen recipe
            chosen_recipes.add(G.nodes[node]['title'])
    for node in G.nodes:  # loop through nodes
        if 'url' in G.nodes[node] and G.nodes[node]['title'] not in chosen_recipes:
            # node is a recipe AND recipe is not chosen
            to_remove.add(node)
    return to_remove


def reweigh_graph(G):
    for node in G:
        if 'url' in G.nodes[node]:  # chosen recipe
            neighbors = list(G.neighbors(node))
            total = 0
            for nutri in neighbors:
                total += G[node][nutri]['weight']
            for nutri in neighbors:
                G[node][nutri]['weight'] /= total
    return G


def get_low_weight_edges(G, wmin):
    to_remove = set()
    for u, v, weight in G.edges.data('weight'):
        if weight < wmin:
            to_remove.add((u, v))
    return to_remove


def remove_nodes_and_edges(G, G_ing, main_nutrients=['Total fats (g)', 'Protein (g)', 'Carbohydrates (g)'],
                           wmin=1, verbose=False):
    if verbose:
        print('Before processing: ')
        print('Number of nodes: ', G.number_of_nodes())
        print('Number of edges: ', G.number_of_edges())

    to_remove_nutrients = get_all_other_nutrients(G, main_nutrients)
    G.remove_nodes_from(to_remove_nutrients)

    to_remove_recipes = get_all_recipes_not_in_ingredients_graph(G,G_ing)
    G.remove_nodes_from(to_remove_recipes)

    G = reweigh_graph(G)

    to_remove_edges = get_low_weight_edges(G, wmin)
    G.remove_edges_from(to_remove_edges)

    if verbose:
        print('Post Processing:')
        print('Number of nodes: ', G.number_of_nodes())
        print('Number of edges: ', G.number_of_edges())

    return G


def create_bipartite_graph_and_project_it(G):
    recipes = [node for node in G.nodes if 'url' in G.nodes[node]]
    nutrients = [node for node in G.nodes if 'url' not in G.nodes[node]]
    edges = G.edges()

    # Create a bipartite graph
    BG = nx.Graph()
    BG.add_nodes_from(recipes, bipartite=0)  # add recipe nodes
    BG.add_nodes_from(nutrients, bipartite=1)  # add nutrients nodes
    BG.add_edges_from(edges)  # add edges between recipes and nutrients

    # Perform one-mode projections
    recipe_nodes = {n for n, d in BG.nodes(data=True) if d["bipartite"] == 0}  # identify recipe nodes
    recipe_projection = nx.bipartite.weighted_projected_graph(BG, recipe_nodes)

    nutrients_nodes = {n for n, d in BG.nodes(data=True) if d["bipartite"] == 1}  # identify nutrients nodes
    nutrients_projection = nx.bipartite.weighted_projected_graph(BG, nutrients_nodes)

    return recipe_projection, nutrients_projection


# ####################### #
# Load and Save functions #
# ####################### #
def load_ingredients_and_nutrients_graphs(loc, loc_type):
    """
    Loads a nutrients and ingredients_reduced graphs.
    """
    G_nut_file = os.path.join(loc_type, loc + '_nutrients')
    G_ing_file = os.path.join(loc_type, loc + '_ingredients' + '_reduced')
    G = nx.read_gml(G_nut_file + '.gml')
    G_ing = nx.read_gml(G_ing_file + '.gml')
    return G, G_ing


def load_nutri_graph(loc, loc_type, reduced=False, projN=False, projR=False):
    """
    Loads a single graph. Supports normal graph and reduced versions (including projected)
    """
    loc += '_nutrients'
    if reduced:
        loc += '_reduced'
        if projN:
            loc += '_nutProjN'
        elif projR:
            loc += '_nutProjR'
    filename = os.path.join(loc_type, loc)
    return nx.read_gml(filename + '.gml')


def save_graph(loc, loc_type, graph, graph_type=''):
    """
    Save a single graph
    """
    loc += '_nutrients'
    filename = os.path.join(loc_type, loc)
    nx.write_gml(graph, filename + graph_type + '.gml')


def save_reduced_graphs(loc_list, loc_type, loc_graphs):
    """
    Save a list of graphs
    """
    for loc, G in zip(loc_list, loc_graphs):
        save_graph(loc, loc_type, G, graph_type='_reduced')


# ############################# #
# Functions that do many things #
# ############################# #
def load_reduce_save(loc, loc_type, main_nutrients, wmin, verbose=False, save=True):
    G, G_ing = load_ingredients_and_nutrients_graphs(loc, loc_type)
    G = remove_nodes_and_edges(G, G_ing, main_nutrients, wmin, verbose)
    if save:
        save_graph(loc, loc_type, G, graph_type='_reduced')
    return G


def load_reduced_project_save(loc, loc_type, save=True):
    graph = load_nutri_graph(loc, loc_type, reduced=True)
    recipe_graph, nutrients_graph = create_bipartite_graph_and_project_it(graph)
    if save:
        save_graph(loc, loc_type, recipe_graph, graph_type='_reduced_nutProjR')
        save_graph(loc, loc_type, nutrients_graph, graph_type='_reduced_nutProjN')


# #################################################################################################################### #
# MAIN - MAIN - MAIN - MAIN - MAIN - MAIN - MAIN - MAIN - MAIN - MAIN - MAIN - MAIN - MAIN - MAIN - MAIN - MAIN - MAIN #
# #################################################################################################################### #
def main():
    main_nutrients = ['Total fats (g)', 'Protein (g)', 'Carbohydrates (g)',
                      'Sugars, total (g)', 'Fiber, total dietary (g)']
    wmin = 0.15
    gen_country = False
    gen_region = False
    gen_continent = True
    countries = ['Argentine', 'Australian', 'Canadian', 'Chinese',
                 'English', 'French', 'German', 'Greek',
                 'Indian', 'Irish', 'Italian',
                 'Mexican', 'Nigerian', 'Thai', 'US']
    regions = ['Australian', 'Canadian', 'Chinese and Mongolian',
               'French', 'Indian Subcontinent', 'Italian',
               'Mexican', 'South American', 'US']
    continents = ['Asian', 'European', 'Latin American', 'North American']

    if gen_country:
        for loc in tqdm(countries, total=len(countries), bar_format='{l_bar}{bar:30}{r_bar}', colour='white'):
            load_reduce_save(loc, 'country_data', main_nutrients, wmin, verbose=True, save=True)
    if gen_region:
        for loc in tqdm(regions, total=len(regions), bar_format='{l_bar}{bar:30}{r_bar}', colour='white'):
            load_reduce_save(loc, 'region_data', main_nutrients, wmin, verbose=True, save=True)
    if gen_continent:
        for loc in tqdm(continents, total=len(continents), bar_format='{l_bar}{bar:30}{r_bar}', colour='white'):
            load_reduce_save(loc, 'continent_data', main_nutrients, wmin, verbose=True, save=True)

    if gen_country:
        for loc in tqdm(countries, total=len(countries), bar_format='{l_bar}{bar:30}{r_bar}', colour='white'):
            load_reduced_project_save(loc, 'country_data', save=True)
    if gen_region:
        for loc in tqdm(regions, total=len(regions), bar_format='{l_bar}{bar:30}{r_bar}', colour='white'):
            load_reduced_project_save(loc, 'region_data', save=True)
    if gen_continent:
        for loc in tqdm(continents, total=len(continents), bar_format='{l_bar}{bar:30}{r_bar}', colour='white'):
            load_reduced_project_save(loc, 'continent_data', save=True)


if __name__ == "__main__":
    main()
