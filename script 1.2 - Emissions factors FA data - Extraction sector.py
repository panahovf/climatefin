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
# load oilgas extraction data
df_extraction_oilgas = pd.read_csv("1 - input/v3_oil_gas_extraction_ForwardAnalytics2024.csv")


# ----------------------------
# load coal extraction data
df_extraction_coal = pd.read_csv("1 - input/v1coal-extraction_ForwardAnalytics2024.csv")










# In[4]: FILTER DATA
####################

# ----------------------------
### OIL GAS
df_extraction_oilgas = df_extraction_oilgas[df_extraction_oilgas['status'] == "operating"]  # filter by operating
df_extraction_oilgas = df_extraction_oilgas[df_extraction_oilgas['latest_year'] == 1]    # keep only latest year


# break oil and gas separately
df_extraction_oil = df_extraction_oilgas[df_extraction_oilgas['subsector'] == "oil"]
df_extraction_gas = df_extraction_oilgas[df_extraction_oilgas['subsector'] == "gas"]


del df_extraction_oilgas


### COAL
df_extraction_coal = df_extraction_coal[df_extraction_coal['status']=='Operating']  # filter only operating plants
df_extraction_coal['emissionsco2e20years'] = pd.to_numeric(df_extraction_coal['emissionsco2e20years'], errors='coerce')   # 
df_extraction_coal['activity'] = pd.to_numeric(df_extraction_coal['activity'], errors='coerce')   # 










# In[5.1]:
# create a function to get weighted average for emissions intensity
# OIL --- million tonnes of CO2 per production --- million bbl/y

def weighted_avg_oil(group):
    return (group['annual_co2_calc_20yr'] * group['activity']).sum() / group['activity'].sum()


# Group by country
df_country_CO2factor_oil = df_extraction_oil.groupby('countryiso3').apply(weighted_avg_oil)


# Change the name for the column
df_country_CO2factor_oil.name = 'Oil_WA_Emissions_Factor'


# Reset the index
df_country_CO2factor_oil = df_country_CO2factor_oil.reset_index()










# In[5.2]:
# create a function to get weighted average for emissions intensity
# GAS --- million tonnes of CO2 per production --- million m3/y

def weighted_avg_gas(group):
    return (group['annual_co2_calc_20yr'] * group['activity']).sum() / group['activity'].sum()


# Group by country
df_country_CO2factor_gas = df_extraction_gas.groupby('countryiso3').apply(weighted_avg_gas)


# Change the name for the column
df_country_CO2factor_gas.name = 'Gas_WA_Emissions_Factor'


# Reset the index
df_country_CO2factor_gas = df_country_CO2factor_gas.reset_index()










# In[5.3]:
# create a function to get weighted average for emissions intensity
# COAL --- million tonnes of CO2 per production --- mtpa

def weighted_avg_coal(group):
    return (group['emissionsco2e20years'] * group['activity']).sum() / group['activity'].sum()


# Group by country
df_country_CO2factor_coal = df_extraction_coal.groupby('countryiso3').apply(weighted_avg_coal)


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





