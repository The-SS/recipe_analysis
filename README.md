# Recipe Analysis

These scripts require the following dependencies:
- numpy
- pandas
- requests
- bs4.

They have been tested with Python 3.7.
A conda environment can be created using:
``` 
conda create --name conda_env python=3.7 numpy pandas requests bs4
```

## Data download
https://cosylab.iiitd.edu.in/recipedb/ can be scraped using the `get_dataRDB.py` script.
The URL indices start at `2610` and end at `149191`. 
Within this range, some URLs do not contain information. 
These are filtered out later.

To use the script:
1. Change the `start` and `end` variables such that: `2610 <= start <= end <= 149191`
2. Run the script

Copies of this script can be made and started independently to scrape the website faster.
If the URL is found, the time taken by the request and processing of the data is printed. 
Otherwise, only the URL index is printed.  

## Combining the data
Once the data is downloaded, the `combine_pkl_files.py` script can be customized and ran to combine all data
into a single pandas dataframe.

To customize the script:
1. Edit the `read_pickle` statements to add all generated dataframes into a single list.
2. Run the script

This will merge all dataframes into one and remove URLs that could not be reached.
The resulting dataframe is saved in the current directory.

## Processing the data
The `process_data.py` script provides:
1. some examples of reading and compiling some results
2. some data processing and filtering for the data to build a graph.
3. saving of data for specific locations with a large enough number of recipes.

The full filtered data is saved to the same directory.
The country data is saved to the `country_data` directory.
The region data is saved to the `region_data` directory.
The continent data is saved to the `continent_data` directory.
The world data is saved to the root directory.
The script can be executed without any modifications.

## Building the graphs
The `construct_graphs.py` script is used to build two graphs:
1. An unweighted undirected graph between recipes and ingredients with `_ingredients` appended to the original file name.
2. A weighted undirected graph between recipes and nutrients (normalized by energy) with `_nutrients` appended to the original file name.

Two `.gml` files are saved to the same directory where the `.pkl` file resides.
The script can be executed without any modifications.


## Processing the graphs
### Ingredients Graphs
The `ingredients_graph_processing.py` script processes the graph by 
1. Removing recipes with a small number of ingredients
2. Removing ingredients that are only used a few number of times (and those that have a name less than 2 characters long)
3. Creating a bipartite graph for the remaining recipes and ingredients
4. Creating the 1-mode projections onto the recipes and ingredients

The script prints out some data (number of nodes/edges before/after the removal of nodes).

The script saves three `.gml` files: one for the reduced graph, one for the projection on ingredients, and one for the projection on the recipes. 
Simply update the list of locations and run the script.

### Nutrients Graphs
The `nutrients_graph_processing.py` script processes the graph by 
1. Using the recipes from the "Ingredients Graphs" section
2. Only keeping five nutrients: Fats, Protein, Carbs, Sugars, Fiber
3. Reweighing the edges to percentage weight of the five nutrients 
4. Removing edges with low weight
5. Creating a bipartite graph for the remaining nutrients and ingredients
6. Creating the 1-mode projections onto the nutrients and ingredients

The script prints out some data (number of nodes/edges before/after the removal of nodes).

The script saves three `.gml` files: one for the reduced graph, one for the projection on nutrients, and one for the projection on the recipes. 
Simply update the list of locations and run the script.

## Analyzing the graphs
### `ingredients_graphs_analysis`
Analyzes the ingredients graphs' 1-mode projection on the ingredients generating details about
- graph diameters
- degree centrality
- betweenness centrality
- degree distribution

### `ingredients_graphs_analysis_result_plots_and_tabels`
Plots graphs and saves tables for results from `ingredients_graphs_analysis.py`

### `nutrients_graphs_analysis`
Analyzes the nutrients graphs' 1-mode projection on the nutrients generating details about
- recipes that have only one main nutrient
- recipes that connect two nutrients
- radar and matrix graphs of the nutrition content of each graph (normalized) 

