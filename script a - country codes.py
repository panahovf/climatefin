# In[1]:
# Date: July 28, 2024
# Project: Get region and markets data and set 3 letter country codes
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

# ----------------------------
directory = r'C:\Users\panah\OneDrive\Desktop\Work\2 - RA - Climate fin'
os.chdir(directory)
del directory


# ----------------------------
# markets
df_developed = pd.read_csv("1 - input/Country Datasets/developed.csv")      #input the name of the Excel file
df_developing = pd.read_csv("1 - input/Country Datasets/developing.csv")      #input the name of the Excel file
df_emerging = pd.read_csv("1 - input/Country Datasets/emerging.csv")      #input the name of the Excel file


# ----------------------------
# regions
df_regions = pd.read_excel("1 - input/Country Datasets/country_gca_region.xlsx")      #input the name of the Excel file










# In[4]:
# import the 3 letter country names to market datasets
    
df_developed = pd.merge(df_developed, 
                        df_regions[['alpha-2', 'alpha-3']], 
                        on='alpha-2', 
                        how='left')
    

df_developing = pd.merge(df_developing, 
                        df_regions[['alpha-2', 'alpha-3']], 
                        on='alpha-2', 
                        how='left')


df_emerging = pd.merge(df_emerging, 
                        df_regions[['alpha-2', 'alpha-3']], 
                        on='alpha-2', 
                        how='left')










# In[5]:
# Export data

df_developed.to_excel('2 - output/script a - country codes/1 - developed.xlsx', index=False)
df_developing.to_excel('2 - output/script a - country codes/2 - developing.xlsx', index=False)
df_emerging.to_excel('2 - output/script a - country codes/3 - emerging.xlsx', index=False)






