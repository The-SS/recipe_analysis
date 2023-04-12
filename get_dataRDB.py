"""
Scrape RecipeDB for data.
A conda environment can be created using:
# conda create --name conda_env python=3.7 numpy pandas requests bs4

Simply change the start and end variables such that:
2610 <= start <= end <= 149191
and run the script.
"""
import time
import numpy as np
import requests
from bs4 import BeautifulSoup
import pandas as pd

# start: 2610: https://cosylab.iiitd.edu.in/recipedb/search_recipeInfo/2610
# end: 149191: https://cosylab.iiitd.edu.in/recipedb/search_recipeInfo/149191

df = pd.DataFrame({"url idx": [],
                   "status": [],
                   "recipe title": [],
                   "continent": [],
                   "region": [],
                   "country": [],
                   "recipe time": [],
                   "nutritional information": [],
                   "ingredient information": [],
                   })

t1_hist = []
t2_hist = []
t3_hist = []
t4_hist = []
total = []
start = 2610
end = 149191
count = end-start+1
iidx = 0
for idx in range(start, end+1):
    print(idx, ' ', iidx+1, '/', count)
    url_idx = str(idx)
    url = "https://cosylab.iiitd.edu.in/recipedb/search_recipeInfo/" + url_idx
    try:
        t0 = time.time()
        req = requests.get(url)
        content = req.text
        t1 = time.time() - t0
        t1_hist.append(t1)
        t0 = time.time()
        soup = BeautifulSoup(content, features="lxml")
        t2 = time.time() - t0
        t2_hist.append(t2)

        t0 = time.time()
        dish_name = soup.find_all('h3')[0].text
        recipe_time = soup.find_all('p')[2].text.split('\n')[0]
        nutri_table, ingri_table = soup.find_all('table')
        nutri_list = nutri_table.find_all('td')
        ingri_list = ingri_table.find_all('td')
        cuisine = soup.find_all('p')[0].text
        cuisine, region, country = cuisine.split(" >> ")
        country = country.split('\n')[0]

        nutri_list = [tag.text for tag in nutri_table.find_all('td')]
        nutri_dict = {}
        for i in range(len(nutri_list)//2):
            nutri_dict[nutri_list[2*i]] = nutri_list[2*i+1]
        ingri_list = [tag.text for tag in ingri_table.find_all('td')]
        ingri_dict = {}
        for i in range(len(ingri_list)//8):
            ingri_dict[ingri_list[8*i]] = {'quantity': ingri_list[8*i+1],
                                           'unit': ingri_list[8*i+2],
                                           'state': ingri_list[8*i+3],
                                           'energy (kcal)': ingri_list[8*i+4],
                                           'carbohydrates': ingri_list[8*i+5],
                                           'protein (g)': ingri_list[8*i+6],
                                           'lipid (fat) (g)': ingri_list[8*i+7]}
        ingri_names_list = [tag.text for tag in ingri_table.find_all('a')]
        t3 = time.time() - t0
        t3_hist.append(t3)

        t0 = time.time()
        row = [url_idx, 1, dish_name, cuisine, region, country, recipe_time, nutri_dict, ingri_dict]
        df.loc[iidx] = row
        iidx += 1
        t4 = time.time() - t0
        t4_hist.append(t4)
        print('total:', t1 + t2 + t3 + t4, 'sec')
        total.append(t1 + t2 + t3 + t4)
        print("~~~~~~~~~~~~~~~~~~~~~~")
    except:
        row = [url_idx, 0, '', '', '', '', '', '', '']
        df.loc[iidx] = row
        iidx += 1

print(np.mean(total))
print(np.var(total))

df.to_pickle('data_pkl/data_' + str(start) + '_' + str(end) + '.pkl')
df.to_csv('data_csv/data_' + str(start) + '_' + str(end) + '.csv')
