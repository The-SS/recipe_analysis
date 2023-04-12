import pandas as pd
import networkx as nx

# read the data pkl file
df = pd.read_pickle('RDB_full_data_filtered.pkl')

# load ingredients and nutrients and create dictionaries
all_ingredients = set().union(*df['ingredient information'])
print('Num ingredients: ', len(all_ingredients))
all_nutrients = set().union(*df['normalized nutrients by energy'])
print('Num nutrients: ', len(all_nutrients))
ingri_dict = {}
ingri_start_idx = len(df)
for idx, ingri in enumerate(all_ingredients):
    ingri_dict[ingri] = idx + ingri_start_idx
nutri_dict = {}
nutri_start_idx = len(df)
for idx, nutri in enumerate(all_nutrients):
    nutri_dict[nutri] = idx + nutri_start_idx

# Ingredients Graph
ingri_graph = nx.Graph()
nodes = []
for idx, row in df.iterrows():
    print(idx, '/', len(df)-1)
    nodes.append((idx, {'url': int(row['url idx']), 'title': row['recipe title'],
                        'continent': row['continent'], 'region': row['region'], 'country': row['country']}))
ingri_start_idx = len(df)
for idx, ingri in enumerate(all_ingredients):
    # there is a weird empty ingredient ''
    nodes.append((idx + ingri_start_idx, {'title': ingri}))
ingri_graph.add_nodes_from(nodes)
edges = []
for idx, row in df.iterrows():
    print(idx, '/', len(df)-1)
    for ingri in row['ingredient information']:
        edges.append((idx, ingri_dict[ingri]))
ingri_graph.add_edges_from(edges)
nx.write_gml(ingri_graph, 'undir_ingri_graph.gml')

# Nutrients Graph
nutri_graph = nx.Graph()
nodes = nodes[0:len(df)]  # keep only the recipes nodes
nutri_start_idx = len(df)
for idx, nutri in enumerate(all_nutrients):
    nodes.append((idx + nutri_start_idx, {'title': nutri}))
nutri_graph.add_nodes_from(nodes)
edges = []
for idx, row in df.iterrows():
    print(idx, '/', len(df)-1)
    for nutri in row['normalized nutrients by energy']:
        if row['normalized nutrients by energy'][nutri] > 0:
            edges.append((idx, nutri_dict[nutri], {'weight': row['normalized nutrients by energy'][nutri]}))
nutri_graph.add_edges_from(edges)
nx.write_gml(nutri_graph, 'undir_nutri_graph.gml')

