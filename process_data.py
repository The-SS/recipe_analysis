import matplotlib.pyplot as plt
import pandas as pd
import os


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
    for idx, nutrients in enumerate(df['nutritional information']):
        print(idx, '/', len(df) - 1)
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


def generate_country_dfs(df, min_recip=0):
    # Group the dataframe by country
    grouped = df.groupby('country')

    # Create a list of dataframes for each group
    country_dfs = {}
    for country, data in grouped:
        if len(data) >= min_recip:  # only include countries with a minimum number of recipes
            country_dfs[country] = data.reset_index(drop=True)
    return country_dfs


def save_country_dfs(country_dfs, path=''):
    if path != '' and not os.path.exists(path):
        os.makedirs(path)

    for country in country_dfs.keys():
        print('saving ', country, ' data')
        save_name = os.path.join(path, country)
        country_dfs[country].to_pickle(save_name + '.pkl')
        # country_dfs[country].to_csv(save_name + '.csv')


def plt_country_recipe_count(df):
    country_counts = df['country'].value_counts()
    # print(list(country_counts.keys()))

    recipe_count = list(country_counts.values)

    plt.hist(recipe_count, 300)
    plt.show()


def main():
    df = pd.read_pickle('RDB_full_data.pkl')

    unique_continents, unique_countries, unique_regions = get_unique_labels(df, True)
    all_ingredients, all_nutrients = get_unique_ingri_and_nutri(df, True)
    df = generate_normalized_nutri_info(df)

    plt_country_recipe_count(df)

    country_dfs = generate_country_dfs(df, min_recip=2500)
    save_country_dfs(country_dfs, path='country_data')


    df.to_pickle('RDB_full_data_filtered' + '.pkl')
    df.to_csv('RDB_full_data_filtered' + '.csv')


if __name__ == "__main__":
    main()
