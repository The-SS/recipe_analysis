import networkx as nx
import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt


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


def remove_recipes_and_ingredients_with_small_degree(G, dmin_r=1, dmin_i=1):
    to_remove_recipes = get_recipes_with_low_degree(G, dmin_r)
    G.remove_nodes_from(to_remove_recipes)

    to_remove = get_ingredients_with_low_degree(G, dmin_i)
    G.remove_nodes_from(to_remove)

    G = remove_degree_zero_nodes(G)

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


def main():
    ig = nx.read_gml('country_data/Argentine_ingredients.gml')
    ig = nx.read_gml('country_data/Australian_ingredients.gml')
    ig = nx.read_gml('country_data/Canadian_ingredients.gml')
    ig = nx.read_gml('country_data/Chinese_ingredients.gml')
    ig = nx.read_gml('country_data/English_ingredients.gml')
    ig = nx.read_gml('country_data/French_ingredients.gml')
    ig = nx.read_gml('country_data/German_ingredients.gml')
    # ig = nx.read_gml('country_data/Greek_ingredients.gml')
    # ig = nx.read_gml('country_data/Indian_ingredients.gml')
    # ig = nx.read_gml('country_data/Italian_ingredients.gml')
    # ig = nx.read_gml('country_data/Irish_ingredients.gml')
    # ig = nx.read_gml('country_data/Mexican_ingredients.gml')
    # ig = nx.read_gml('country_data/Nigerian_ingredients.gml')
    # ig = nx.read_gml('country_data/Thai_ingredients.gml')
    # ig = nx.read_gml('country_data/US_ingredients.gml')

    print('Number of nodes: ', ig.number_of_nodes())
    print('Number of edges: ', ig.number_of_edges())
    ig = remove_recipes_and_ingredients_with_small_degree(ig, dmin_r=5, dmin_i=3)
    print('Post Processing:')
    print('Number of nodes: ', ig.number_of_nodes())
    print('Number of edges: ', ig.number_of_edges())
    # nx.draw_networkx(ig)
    # plt.show()

    recipe_graph, ingredients_graph = project_on_recipes(ig)

    degree_sequence = sorted([d for n, d in ingredients_graph.degree()], reverse=True)
    degree_hist = nx.degree_histogram(ingredients_graph)
    plt.bar(range(len(degree_hist)), degree_hist)
    plt.xlabel("Degree")
    plt.ylabel("Frequency")
    plt.title("Degree Distribution")
    plt.show()

    # get node with highest degree
    degree_dict = dict(ingredients_graph.degree())
    node, degree = max(degree_dict.items(), key=lambda x: x[1])
    print(f"Node {node} has the highest degree of {degree}")
    print('This corresponds to: ', ig.nodes[node]['title'])

    k = 10
    degree_dict = dict(ingredients_graph.degree())
    top_k_nodes = [key for key, value in sorted(degree_dict.items(), key=lambda x: x[1], reverse=True)[:k]]
    print(f"The top {k} nodes with the highest degree are: {top_k_nodes}")
    for node in top_k_nodes:
        print('This corresponds to: ', ig.nodes[node]['title'])

    print('Done')


if __name__ == "__main__":
    main()
