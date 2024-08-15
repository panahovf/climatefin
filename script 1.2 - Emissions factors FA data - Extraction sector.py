# In[1]:
# Date: July 28, 2024
# Project: Country level emissions intensity data for extraction sector from FA data
# Author: Farhad Panahov


# Task: Identify weighted average emissions intensity in power for Oil and Gas by country


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
# load oil gas coal extraction data
df_extraction = pd.read_csv("1 - input/v2_extraction_operating_ForwardAnalytics2024.csv")










# In[4]: FILTER DATA
####################

# ----------------------------
# oil
df_extraction_oil = df_extraction[df_extraction['subsector_extraction'] == "Oil"]

# gas
df_extraction_gas = df_extraction[df_extraction['subsector_extraction'] == "Gas"]

# coal
df_extraction_coal = df_extraction[df_extraction['subsector_extraction']=='Coal']


# ----------------------------
del df_extraction










# In[5.1]:
# create a function to get weighted average for emissions intensity
# OIL --- million tonnes of CO2 per production --- million bbl/y

def weighted_avg_oil(group):
    return (group['emissions_co2e_million_tonnes'] * group['activity']).sum() / group['activity'].sum()


# Group by country
df_country_CO2factor_oil = df_extraction_oil.groupby('country_iso_3').apply(weighted_avg_oil)


# Change the name for the column
df_country_CO2factor_oil.name = 'Oil_WA_Emissions_Factor'


# Reset the index
df_country_CO2factor_oil = df_country_CO2factor_oil.reset_index()










# In[5.2]:
# create a function to get weighted average for emissions intensity
# GAS --- million tonnes of CO2 per production --- million m3/y

def weighted_avg_gas(group):
    return (group['emissions_co2e_million_tonnes'] * group['activity']).sum() / group['activity'].sum()


# Group by country
df_country_CO2factor_gas = df_extraction_gas.groupby('country_iso_3').apply(weighted_avg_gas)


# Change the name for the column
df_country_CO2factor_gas.name = 'Gas_WA_Emissions_Factor'


# Reset the index
df_country_CO2factor_gas = df_country_CO2factor_gas.reset_index()










# In[5.3]:
# create a function to get weighted average for emissions intensity
# COAL --- million tonnes of CO2 per production --- mtpa

def weighted_avg_coal(group):
    return (group['emissions_co2e_million_tonnes'] * group['activity']).sum() / group['activity'].sum()


# Group by country
df_country_CO2factor_coal = df_extraction_coal.groupby('country_iso_3').apply(weighted_avg_coal)


# Change the name for the column
df_country_CO2factor_coal.name = 'Coal_WA_Emissions_Factor'


# Reset the index
df_country_CO2factor_coal = df_country_CO2factor_coal.reset_index()










# In[6]:
# Export data

df_country_CO2factor_coal.to_excel('2 - output/script 1/1 - country_extraction_co2factor_coal.xlsx', index=False)
df_country_CO2factor_oil.to_excel('2 - output/script 1/2 - country_extraction_co2factor_oil.xlsx', index=False)
df_country_CO2factor_gas.to_excel('2 - output/script 1/3 - country_extraction_co2factor_gas.xlsx', index=False)

df_extraction_coal.to_excel('2 - output/script 1/4 - extraction_coal.xlsx', index=False)
df_extraction_gas.to_excel('2 - output/script 1/5 - extraction_gas.xlsx', index=False)
df_extraction_oil.to_excel('2 - output/script 1/6 - extraction_oil.xlsx', index=False)





