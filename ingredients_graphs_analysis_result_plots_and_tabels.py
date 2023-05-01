import csv

from plotting_functions import *
import os


def plot_graph_diameter_results(show=True, save=False):
    path = os.path.join('results', 'diameter')
    country_data = os.path.join(path, 'country_data_diam.txt')
    region_data = os.path.join(path, 'region_data_diam.txt')
    continent_data = os.path.join(path, 'continent_data_diam.txt')
    diameters_plot(country_data, 'Countries', show_plot=show, save_plot=save)
    diameters_plot(region_data, 'Regions', show_plot=show, save_plot=save)
    diameters_plot(continent_data, 'Continent', show_plot=show, save_plot=save)


def table_graph_centralities(centrality_file, loc_type):
    directory_path = os.path.join('results', centrality_file)
    loc_type += '_ '

    # Create a dictionary to store the extracted data
    data_dict = {}

    # Loop through all files in the directory
    for file_name in os.listdir(directory_path):
        if file_name.startswith(loc_type) and file_name.endswith('.txt'):
            # Extract the location name from the file name
            location_name = file_name[len(loc_type):-len('_--.txt')]

            # Open the file and extract the data
            with open(os.path.join(directory_path, file_name), 'r') as file:
                file_lines = file.readlines()
                data_dict[location_name] = {}
                for line in file_lines[1:]:
                    parts = line.strip().split(':')
                    name = parts[1].split('(')[0].strip()
                    value = parts[1].split('(')[1].split(')')[0].strip()
                    data_dict[location_name][name] = value

    # Save the extracted data to a CSV file
    csv_path = os.path.join(directory_path, loc_type[:-1] + 'data.csv')
    with open(csv_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        # Write the data rows
        for location_name, data in data_dict.items():
            row_values = [location_name] + [f"{name} ({value})" for name, value in data.items()]
            writer.writerow(row_values)


def main():
    plot_graph_diameter_results(show=False, save=True)

    table_graph_centralities('degree_centrality', 'country_data')
    table_graph_centralities('degree_centrality', 'region_data')
    table_graph_centralities('degree_centrality', 'continent_data')

    table_graph_centralities('betweenness_centrality', 'country_data')
    table_graph_centralities('betweenness_centrality', 'region_data')
    table_graph_centralities('betweenness_centrality', 'continent_data')



if __name__ == "__main__":
    main()
