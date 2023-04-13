import os

import pandas as pd
import networkx as nx


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
    for idx, row in df.iterrows():
        print(idx, '/', len(df) - 1)
        nodes.append((idx, {'url': int(row['url idx']), 'title': row['recipe title'],
                            'continent': row['continent'], 'region': row['region'], 'country': row['country']}))
    for idx, ingri in enumerate(all_ingredients):
        # there is a weird empty ingredient ''
        nodes.append((idx + ingredients_start_idx, {'title': ingri}))
    ingredients_graph.add_nodes_from(nodes)

    # add edges
    edges = []
    for idx, row in df.iterrows():
        print(idx, '/', len(df) - 1)
        for ingri in row['ingredient information']:
            edges.append((idx, ingredients_dict[ingri]))
    ingredients_graph.add_edges_from(edges)
    if save_gml:
        nx.write_gml(ingredients_graph, path + '_ingredients.gml')
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
    for idx, row in df.iterrows():
        print(idx, '/', len(df) - 1)
        nodes.append((idx, {'url': int(row['url idx']), 'title': row['recipe title'],
                            'continent': row['continent'], 'region': row['region'], 'country': row['country']}))
    for idx, nutri in enumerate(all_nutrients):
        nodes.append((idx + nutrients_start_idx, {'title': nutri}))
    nutrients_graph.add_nodes_from(nodes)

    # add edges
    edges = []
    for idx, row in df.iterrows():
        print(idx, '/', len(df) - 1)
        for nutri in row['normalized nutrients by energy']:
            if row['normalized nutrients by energy'][nutri] > 0:
                edges.append((idx, nutrients_dict[nutri], {'weight': row['normalized nutrients by energy'][nutri]}))
    nutrients_graph.add_edges_from(edges)

    if save_gml:
        nx.write_gml(nutrients_graph, path + '_nutrients.gml')

    return ingredients_graph


def build_graphs(df, path=''):
    # load ingredients and nutrients and create dictionaries
    all_ingredients = set().union(*df['ingredient information'])
    all_nutrients = set().union(*df['normalized nutrients by energy'])
    print('Num ingredients: ', len(all_ingredients))
    print('Num nutrients: ', len(all_nutrients))

    nutri_dict = {}
    nutri_start_idx = len(df)
    for idx, nutri in enumerate(all_nutrients):
        nutri_dict[nutri] = idx + nutri_start_idx

    ingredients_graph = build_ingredients_graph(df, all_ingredients, save_gml=True, path=path)
    nutrients_graph = build_nutrients_graph(df, all_nutrients, save_gml=True, path=path)

    return ingredients_graph, nutrients_graph


def main():
    # read the data pkl file
    # df = pd.read_pickle('RDB_full_data_filtered.pkl')
    # file_name = 'RDB_full_data_filtered'
    file_name = 'country_data/Argentine'
    file_name = 'country_data/Australian'
    file_name = 'country_data/Canadian'
    file_name = 'country_data/Chinese'
    file_name = 'country_data/English'
    file_name = 'country_data/French'
    file_name = 'country_data/German'
    file_name = 'country_data/Greek'
    file_name = 'country_data/Indian'
    file_name = 'country_data/Irish'
    file_name = 'country_data/Italian'
    file_name = 'country_data/Mexican'
    file_name = 'country_data/Nigerian'
    file_name = 'country_data/Thai'
    file_name = 'country_data/US'
    df = pd.read_pickle(file_name + '.pkl')
    build_graphs(df, path=file_name)


if __name__ == "__main__":
    main()

