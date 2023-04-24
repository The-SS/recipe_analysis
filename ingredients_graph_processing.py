import networkx as nx
import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt
from tqdm import tqdm
import os


# ########################## #
# Graph processing functions #
# ########################## #
def remove_degree_zero_nodes(G):
    to_remove = [node for node in G.nodes if G.degree[node] == 0]
    G.remove_nodes_from(to_remove)
    return G


def get_recipes_with_low_degree(G, dmin):
    to_remove_recipes = set()
    for node in G.nodes:  # loop through nodes
        if 'url' in G.nodes[node]:  # node is a recipe
            if G.degree(node) < dmin:
                to_remove_recipes.add(node)
        else:
            # node is an ingredients. ingredient nodes always follow the recipes --> stop
            break
    return to_remove_recipes


def get_ingredients_with_low_degree(G, dmin):
    to_remove = set()
    for node in G.nodes:  # loop through nodes
        if 'url' not in G.nodes[node]:  # node is an ingredient
            if len(G.nodes[node]['title']) < 2 or G.degree(node) < dmin:
                # remove node if its name is less than 2 characters long
                # or if the degree is less than the minimum threshold
                to_remove.add(node)
                for recip in G.neighbors(node):
                    if 'url' in G.nodes[recip]:
                        to_remove.add(recip)
    return to_remove


def remove_recipes_and_ingredients_with_small_degree(G, dmin_r=1, dmin_i=1, verbose=False):
    if verbose:
        print('Before processing: ')
        print('Number of nodes: ', G.number_of_nodes())
        print('Number of edges: ', G.number_of_edges())

    to_remove_recipes = get_recipes_with_low_degree(G, dmin_r)
    G.remove_nodes_from(to_remove_recipes)

    to_remove = get_ingredients_with_low_degree(G, dmin_i)
    G.remove_nodes_from(to_remove)

    G = remove_degree_zero_nodes(G)

    if verbose:
        print('Post Processing:')
        print('Number of nodes: ', G.number_of_nodes())
        print('Number of edges: ', G.number_of_edges())

    return G


def project_on_recipes(G):
    recipes = [node for node in G.nodes if 'url' in G.nodes[node]]
    ingredients = [node for node in G.nodes if 'url' not in G.nodes[node]]
    edges = G.edges()

    # Create a bipartite graph
    BG = nx.Graph()
    BG.add_nodes_from(recipes, bipartite=0)  # add recipe nodes
    BG.add_nodes_from(ingredients, bipartite=1)  # add ingredient nodes
    BG.add_edges_from(edges)  # add edges between recipes and ingredients

    # Perform one-mode projection onto recipe nodes
    recipe_nodes = {n for n, d in BG.nodes(data=True) if d["bipartite"] == 0}  # identify recipe nodes
    recipe_projection = nx.bipartite.weighted_projected_graph(BG, recipe_nodes)

    ingredients_nodes = {n for n, d in BG.nodes(data=True) if d["bipartite"] == 1}  # identify recipe nodes
    ingredients_projection = nx.bipartite.weighted_projected_graph(BG, ingredients_nodes)

    return recipe_projection, ingredients_projection


# ####################### #
# Load and Save functions #
# ####################### #
def load_graph(loc, loc_type, reduced=False):
    """
    Loads a single graph. Supports normal graph and reduced versions
    """
    loc += '_ingredients'
    if reduced:
        loc += '_reduced'
    filename = os.path.join(loc_type, loc)
    return nx.read_gml(filename + '.gml')


def load_graphs_list(loc_list, loc_type, reduced=False):
    """
    Loads a list of graphs
    """
    loc_graphs = []
    for loc in tqdm(loc_list, total=len(loc_list), bar_format='{l_bar}{bar:30}{r_bar}', colour='white'):
        loc_graphs.append(load_graph(loc, loc_type, reduced))
    return loc_graphs


def save_graph(loc, loc_type, graph, graph_type=''):
    """
    Save a single graph
    """
    loc += '_ingredients'
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
def load_reduce_save(loc, loc_type, dmin_r=1, dmin_i=1, verbose=False, save=True):
    graph = load_graph(loc, loc_type)
    graph = remove_recipes_and_ingredients_with_small_degree(graph, dmin_r, dmin_i, verbose)
    if save:
        save_graph(loc, loc_type, graph, graph_type='_reduced')
    return graph


def load_reduced_project_save(loc, loc_type, save=True):
    graph = load_graph(loc, loc_type, reduced=True)
    recipe_graph, ingredients_graph = project_on_recipes(graph)
    if save:
        save_graph(loc, loc_type, recipe_graph, graph_type='_reduced_ingProjR')
        save_graph(loc, loc_type, ingredients_graph, graph_type='_reduced_ingProjI')


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

    for loc in tqdm(countries, total=len(countries), bar_format='{l_bar}{bar:30}{r_bar}', colour='white'):
        if loc in ['Italian', 'Mexican']:
            dmin_r, dmin_i = 5, 25
        else:
            dmin_r, dmin_i = 5, 3
        load_reduce_save(loc, 'country_data', dmin_r, dmin_i, verbose=True, save=True)
    for loc in tqdm(regions, total=len(regions), bar_format='{l_bar}{bar:30}{r_bar}', colour='white'):
        if loc in ['Italian', 'Mexican']:
            dmin_r, dmin_i = 5, 40
        else:
            dmin_r, dmin_i = 5, 7
        load_reduce_save(loc, 'region_data', dmin_r, dmin_i, verbose=True, save=True)
    for loc in tqdm(continents, total=len(continents), bar_format='{l_bar}{bar:30}{r_bar}', colour='white'):
        if loc == 'North American':
            dmin_r, dmin_i = 10, 40
        else:
            dmin_r, dmin_i = 10, 70
        load_reduce_save(loc, 'continent_data', dmin_r, dmin_i, verbose=True, save=True)

    for loc in tqdm(countries, total=len(countries), bar_format='{l_bar}{bar:30}{r_bar}', colour='white'):
        load_reduced_project_save(loc, 'country_data', save=True)
    for loc in tqdm(regions, total=len(regions), bar_format='{l_bar}{bar:30}{r_bar}', colour='white'):
        load_reduced_project_save(loc, 'region_data', save=True)
    for loc in tqdm(continents, total=len(continents), bar_format='{l_bar}{bar:30}{r_bar}', colour='white'):
        load_reduced_project_save(loc, 'continent_data', save=True)


if __name__ == "__main__":
    main()
