"""
Load the downloaded pkl files and combine them into a single file
"""
import pandas as pd

dfs = []
dfs.append(pd.read_pickle('data_pkl/data_0_2609.pkl'))
dfs.append(pd.read_pickle('data_pkl/data_2610_2630.pkl'))
dfs.append(pd.read_pickle('data_pkl/data_2631_2700.pkl'))
dfs.append(pd.read_pickle('data_pkl/data_2701_3000.pkl'))
dfs.append(pd.read_pickle('data_pkl/data_3001_7000.pkl'))
dfs.append(pd.read_pickle('data_pkl/data_7001_10000.pkl'))
dfs.append(pd.read_pickle('data_pkl/data_10001_15000.pkl'))
dfs.append(pd.read_pickle('data_pkl/data_15001_20000.pkl'))
dfs.append(pd.read_pickle('data_pkl/data_20001_25000.pkl'))
dfs.append(pd.read_pickle('data_pkl/data_25001_30000.pkl'))
dfs.append(pd.read_pickle('data_pkl/data_30001_35000.pkl'))
dfs.append(pd.read_pickle('data_pkl/data_35001_40000.pkl'))
dfs.append(pd.read_pickle('data_pkl/data_40001_45000.pkl'))
dfs.append(pd.read_pickle('data_pkl/data_45001_50000.pkl'))
dfs.append(pd.read_pickle('data_pkl/data_50001_55000.pkl'))
dfs.append(pd.read_pickle('data_pkl/data_55001_70000.pkl'))
dfs.append(pd.read_pickle('data_pkl/data_70001_85000.pkl'))
dfs.append(pd.read_pickle('data_pkl/data_85001_100000.pkl'))
dfs.append(pd.read_pickle('data_pkl/data_100001_115000.pkl'))
dfs.append(pd.read_pickle('data_pkl/data_115001_130000.pkl'))
dfs.append(pd.read_pickle('data_pkl/data_130001_150000.pkl'))

total = 0
for idx, df in enumerate(dfs):
    s = sum(df.status)
    print('df', idx, ': ', s)
    total += s
print('Total: ', total)

full_df = pd.concat(dfs, ignore_index=True)
full_df_filtered = full_df[full_df['status'] > 0]
full_df_filtered.reset_index(drop=True, inplace=True)
# full_df_filtered = full_df_filtered.rename(columns={'cuisine': 'continent'})

full_df_filtered.to_pickle('RDB_full_data' + '.pkl')
full_df_filtered.to_csv('RDB_full_data' + '.csv')
