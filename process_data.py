import pandas as pd

df = pd.read_pickle('RDB_full_data.pkl')

unique_continents = pd.unique(df['continent'])
unique_countries = pd.unique(df['country'])
unique_regions = pd.unique(df['region'])

print('Num continents: ', len(unique_continents))
print('Continents: ', unique_continents)

print('Num countries: ', len(unique_countries))
print('Countries: ', unique_countries)

print('Num regions: ', len(unique_regions))
print('Regions: ', unique_regions)

all_ingredients = set().union(*df['ingredient information'])
print('Num ingredients: ', len(all_ingredients))

all_nutrients = set().union(*df['nutritional information'])
print('Num nutrients: ', len(all_nutrients))

normalized_nutrients_by_kcal = []
for idx, nutrients in enumerate(df['nutritional information']):
    print(idx, '/', len(df)-1)
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

df.to_pickle('RDB_full_data_filtered' + '.pkl')
df.to_csv('RDB_full_data_filtered' + '.csv')






