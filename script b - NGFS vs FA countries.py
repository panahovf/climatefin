# In[1]:
# Date: Aug 4, 2024
# Project: Identify countries existing within NGFS projections and FA data
# Author: Farhad Panahov


# In[2]:
# load packages


import os
import pandas as pd
import geopandas as gpd
from scipy.interpolate import interp1d
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import FuncFormatter



# In[3]:
# directory & load data

directory = r'C:\Users\panah\OneDrive\Desktop\Work\2 - RA - Climate fin'
os.chdir(directory)
del directory


# all countries
df_all_countries = pd.read_excel("1 - input/Country Datasets/country_gca_region.xlsx")      #input the name of the Excel file

# NGFS
df_ngfs = pd.read_excel("1 - input/Downscaled_GCAM 6.0 NGFS_data.xlsx")      #input the name of the Excel file

# power data
df_fa_power = pd.read_csv('1 - input/v3_power_Forward_Analytics2024.csv')   



# In[4]:
# Edit NGFS data: get countries for secondary data for "current policies"

# current policies
df_ngfs_CP = df_ngfs[df_ngfs['Scenario'] == 'Current Policies']

# secondary energy for
# coal
df_ngfs_CP_coal = df_ngfs_CP[df_ngfs_CP['Variable'] == 'Secondary Energy|Electricity|Coal']

# gas
df_ngfs_CP_gas = df_ngfs_CP[df_ngfs_CP['Variable'] == 'Secondary Energy|Electricity|Gas']

# oil
df_ngfs_CP_oil = df_ngfs_CP[df_ngfs_CP['Variable'] == 'Secondary Energy|Electricity|Oil']


# In[5]:
# Export data

df_developed.to_excel('2 - output/script a - country codes/1 - developed.xlsx', index=False)
df_developing.to_excel('2 - output/script a - country codes/2 - developing.xlsx', index=False)
df_emerging.to_excel('2 - output/script a - country codes/3 - emerging.xlsx', index=False)






