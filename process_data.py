import matplotlib.pyplot as plt
import pandas as pd
import os
from tqdm import tqdm


def get_unique_labels(df, verbose=False):
    unique_continents = pd.unique(df['continent'])
    unique_countries = pd.unique(df['country'])
    unique_regions = pd.unique(df['region'])

    if verbose:
        print('Num continents: ', len(unique_continents))
        print('Continents: ', unique_continents)

        print('Num countries: ', len(unique_countries))
        print('Countries: ', unique_countries)

        print('Num regions: ', len(unique_regions))
        print('Regions: ', unique_regions)

    return unique_continents, unique_countries, unique_regions


def get_unique_ingri_and_nutri(df, verbose=False):
    all_ingredients = set().union(*df['ingredient information'])
    all_nutrients = set().union(*df['nutritional information'])

    if verbose:
        print('Num ingredients: ', len(all_ingredients))
        print('Num nutrients: ', len(all_nutrients))

    return all_ingredients, all_nutrients


def generate_normalized_nutri_info(df):
    normalized_nutrients_by_kcal = []
    for idx, nutrients in tqdm(enumerate(df['nutritional information']), total=len(df),
                               bar_format='{l_bar}{bar:30}{r_bar}', colour='white'):
        nutrients_normalized = {}
        for nutrient in nutrients:
            if nutrients[nutrient] in {'', ' ', '-', '0'}:
                nutrients_normalized[nutrient] = 0
            elif float(nutrients['Energy (kcal)']) == 0:
                nutrients_normalized[nutrient] = float(nutrients[nutrient])
            else:
                nutrients_normalized[nutrient] = float(nutrients[nutrient]) / float(nutrients['Energy (kcal)'])
        normalized_nutrients_by_kcal.append(nutrients_normalized)
    df['normalized nutrients by energy'] = normalized_nutrients_by_kcal
    return df


def generate_location_dfs(df, min_recip=0, location_type='country'):
    """
    Generates a dictionary of dataframes based on location
    df: dataframe with all the data
    min_recip: minimum number of recipes for the location to generate a dataframe for it
    location_type: type of location ('country', 'region', 'continent')
    """
    # Group the dataframe by location
    if location_type in ['country', 'region', 'continent']:
        grouped = df.groupby(location_type)
    else:
        raise ValueError('Unsupported location type.')

    # Create a list of dataframes for each group
    location_dfs = {}
    for location, data in grouped:
        if len(data) >= min_recip:  # only include locations with a minimum number of recipes
            location_dfs[location] = data.reset_index(drop=True)
    return location_dfs


def save_location_dfs(dfs_dict, path='', save_type='pkl'):
    """
    save dataframes in a dictionary of dataframes
    dfs_dict: dictionary of dataframes
    path: save path
    save_type: file type for saving the dataframe ('pkl', 'csv')
    """
    if path != '' and not os.path.exists(path):
        os.makedirs(path)

    print('Saving dataframe dictionary entries. ')
    loc_list = []
    for location in tqdm(dfs_dict.keys(), total=len(dfs_dict),
                         bar_format='{l_bar}{bar:30}{r_bar}', colour='white'):
        loc_list.append(location)
        save_name = os.path.join(path, location)
        if save_type == 'pkl':
            dfs_dict[location].to_pickle(save_name + '.pkl')
        elif save_type == 'csv':
            dfs_dict[location].to_csv(save_name + '.csv')
        else:
            raise ValueError('Unsupported save type')
    print('Saved dataframes for the following locations: ', loc_list)


def plt_location_recipe_count(df, location_type='country'):
    """
    Plot histogram of number of recipes per location
    df: full dataframe
    location_type: type of location ('country', 'region', 'continent')
    """
    if location_type in ['country', 'region', 'continent']:
        location_counts = df[location_type].value_counts()
    else:
        raise ValueError('Unsupported location type.')

    recipe_count = list(location_counts.values)

    plt.hist(recipe_count, 300)
    plt.title(location_type + ' num recipes')
    plt.show()


def main():
    df = pd.read_pickle('RDB_full_data.pkl')

    # get info about unique continents, countries, and regions
    unique_continents, unique_countries, unique_regions = get_unique_labels(df, True)

    # get info about ingredients and nutrients
    all_ingredients, all_nutrients = get_unique_ingri_and_nutri(df, True)

    # normalize dataframe nutritional info
    df = generate_normalized_nutri_info(df)
    # # save the normalized dataframe
    # print('Saving full edited dataframe... ')
    # df.to_pickle('RDB_full_data_filtered' + '.pkl')
    # # df.to_csv('RDB_full_data_filtered' + '.csv')
    # print('Done!')

    plt_location_recipe_count(df, 'country')
    plt_location_recipe_count(df, 'region')
    plt_location_recipe_count(df, 'continent')

    # # generate and save dataframes per country
    # country_dfs = generate_location_dfs(df, min_recip=2500, location_type='country')
    # save_location_dfs(country_dfs, path='country_data', save_type='pkl')

    # generate and save dataframes per region
    region_dfs = generate_location_dfs(df, min_recip=5000, location_type='region')
    save_location_dfs(region_dfs, path='region_data', save_type='pkl')

    # generate and save dataframes per continent
    continent_dfs = generate_location_dfs(df, min_recip=10000, location_type='continent')
    save_location_dfs(continent_dfs, path='continent_data', save_type='pkl')


if __name__ == "__main__":
    main()
