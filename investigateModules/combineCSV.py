import pandas as pd
import numpy as np
import os
import re

folder_data = '/Users/heikokromer/02_SolarAnalytics/modulData'

# list of files
files = os.listdir(folder_data)
files = [f for f in files if f.endswith('.csv')]
files = [f for f in files if not f.endswith('solarData.csv')]

df = pd.DataFrame()
for file in files:
	df_t = pd.read_csv('{}/{}'.format(folder_data,file))
	df = df.append(df_t)

# change columns to only contain identifier
cols = df.columns

id_cols = [re.findall(r'(1.1.\d+) E',c)[0] for c in cols[1:]]

my_cols = [cols[0]]

[my_cols.append(i) for i in id_cols]

df.columns = my_cols

outfile = '2018-07_solarData.csv'
df.to_csv('{}/{}'.format(folder_data,outfile))