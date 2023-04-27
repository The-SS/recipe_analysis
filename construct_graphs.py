import os

import pandas as pd
import networkx as nx
from tqdm import tqdm


def build_ingredients_graph(df, all_ingredients, save_gml=True, path=''):
    # create dictionary where ingredients are keys and the value is the index starting from final index in df
    ingredients_dict = {}
    ingredients_start_idx = len(df)
    for idx, ingri in enumerate(all_ingredients):
        ingredients_dict[ingri] = idx + ingredients_start_idx

    # initialize graph
    ingredients_graph = nx.Graph()

    # add nodes
    nodes = []
    # print('Ingredients node traversal')
    for idx, row in df.iterrows():
        # print(idx, '/', len(df) - 1)
        nodes.append((idx, {'url': int(row['url idx']), 'title': row['recipe title'],
                            'continent': row['continent'], 'region': row['region'], 'country': row['country']}))
    for idx, ingri in enumerate(all_ingredients):
        # there is a weird empty ingredient ''
        nodes.append((idx + ingredients_start_idx, {'title': ingri}))
    ingredients_graph.add_nodes_from(nodes)

    # add edges
    edges = []
    # print('Ingredients edge traversal')
    for idx, row in df.iterrows():
        # print(idx, '/', len(df) - 1)
        for ingri in row['ingredient information']:
            edges.append((idx, ingredients_dict[ingri]))
    ingredients_graph.add_edges_from(edges)
    if save_gml:
        # print('Saving ingredients gml')
        nx.write_gml(ingredients_graph, path + '_ingredients.gml')
    # print('Done')
    return ingredients_graph


def build_nutrients_graph(df, all_nutrients, save_gml=True, path=''):
    # create dictionary where ingredients are keys and the value is the index starting from final index in df
    nutrients_dict = {}
    nutrients_start_idx = len(df)
    for idx, ingri in enumerate(all_nutrients):
        nutrients_dict[ingri] = idx + nutrients_start_idx

    # initialize graph
    ingredients_graph = nx.Graph()

    # Nutrients Graph
    nutrients_graph = nx.Graph()

    # add nodes
    nodes = []
    # print('Nutrients node traversal')
    for idx, row in df.iterrows():
        # print(idx, '/', len(df) - 1)
        nodes.append((idx, {'url': int(row['url idx']), 'title': row['recipe title'],
                            'continent': row['continent'], 'region': row['region'], 'country': row['country']}))
    for idx, nutri in enumerate(all_nutrients):
        nodes.append((idx + nutrients_start_idx, {'title': nutri}))
    nutrients_graph.add_nodes_from(nodes)

    # add edges
    edges = []
    # print('Nutrients edge traversal')
    for idx, row in df.iterrows():
        # print(idx, '/', len(df) - 1)
        for nutri in row['normalized nutrients by energy']:
            if row['normalized nutrients by energy'][nutri] > 0:
                edges.append((idx, nutrients_dict[nutri], {'weight': row['normalized nutrients by energy'][nutri]}))
    nutrients_graph.add_edges_from(edges)

    if save_gml:
        # print('Saving nutrients gml')
        nx.write_gml(nutrients_graph, path + '_nutrients.gml')
    # print('Done')
    return ingredients_graph


def build_graphs(df, path=''):
    # load ingredients and nutrients and create dictionaries
    all_ingredients = set().union(*df['ingredient information'])
    all_nutrients = set().union(*df['normalized nutrients by energy'])
    print('')
    print('Num recipes: ', len(df))
    print('Num ingredients: ', len(all_ingredients))
    print('Num nutrients: ', len(all_nutrients))

    nutri_dict = {}
    nutri_start_idx = len(df)
    for idx, nutri in enumerate(all_nutrients):
        nutri_dict[nutri] = idx + nutri_start_idx

    ingredients_graph = build_ingredients_graph(df, all_ingredients, save_gml=True, path=path)
    nutrients_graph = build_nutrients_graph(df, all_nutrients, save_gml=True, path=path)

    return ingredients_graph, nutrients_graph


def build_graph_for_list(loc_list, loc_type):
    print('Building graphs from ' + loc_type)
    for loc in tqdm(loc_list, total=len(loc_list),
                    bar_format='{l_bar}{bar:30}{r_bar}', colour='white'):
        filename = os.path.join(loc_type, loc)
        df = pd.read_pickle(filename + '.pkl')
        build_graphs(df, path=filename)


def print_recipe_ing_nutri_nums(loc_list, loc_type):
    print('_________________________________')
    print('Building graphs from ' + loc_type)
    print('_________________________________')
    for loc in loc_list:
        filename = os.path.join(loc_type, loc)
        df = pd.read_pickle(filename + '.pkl')
        all_ingredients = set().union(*df['ingredient information'])
        all_nutrients = set().union(*df['normalized nutrients by energy'])
        print('~~~~~~~~')
        print('Num recipes: ', len(df))
        print('Num ingredients: ', len(all_ingredients))
        print('Num nutrients: ', len(all_nutrients))


def main():
    # read the data pkl file and build the nutrients and ingredients graphs
    countries = ['Argentine', 'Australian', 'Canadian', 'Chinese',
                 'English', 'French', 'German', 'Greek',
                 'Indian', 'Irish', 'Italian',
                 'Mexican', 'Nigerian', 'Thai', 'US']
    regions = ['Australian', 'Canadian', 'Chinese and Mongolian',
               'French', 'Indian Subcontinent', 'Italian',
               'Mexican', 'South American', 'US']
    continents = ['Asian', 'European', 'Latin American', 'North American']
    world = ['RDB_full_data_filtered']

    build_graph_for_list(countries, 'country_data')
    build_graph_for_list(regions, 'region_data')
    build_graph_for_list(continents, 'continent_data')
    build_graph_for_list(world, '')

    # # uncomment to print out information about the recipe-ingredients and recipe-nutrients graphs
    # print_recipe_ing_nutri_nums(countries, 'country_data')
    # print_recipe_ing_nutri_nums(regions, 'region_data')
    # print_recipe_ing_nutri_nums(continents, 'continent_data')
    # print_recipe_ing_nutri_nums(world, '')


if __name__ == "__main__":
    main()

