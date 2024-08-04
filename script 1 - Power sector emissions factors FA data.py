# In[1]:
# Date: July 28, 2024
# Project: Country level emissions intensity data for power sector from FA data
# Author: Farhad Panahov


# Task #1: Identify weighted average emissions intensity in power for Oil and Gas by country


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


# load oil & gas
oilgas = "1 - input/power-oil-and-gas-activity_V.02.csv"
df_oilgas = pd.read_csv(oilgas)      #input the name of the Excel file


# break oil and gas separately
df_oil = df_oilgas.loc[(df_oilgas['Sub_sector'] == "Oil")]
df_gas = df_oilgas.loc[(df_oilgas['Sub_sector'] == "Gas")]

# load coal
coal = "1 - input/power-coal.xlsx"
df_coal = pd.read_excel(coal)      #input the name of the Excel file
df_coal = df_coal.loc[df_coal['Status'] == 'operating']
df_coal['new_factor'] = df_coal['Emission Factor'] * df_coal['Heat rate']

del oilgas, coal, directory, df_oilgas



# In[4]:
# create a function to get weighted average for emissions intensity
# OIL --- million tonnes of CO2 per MWh

def weighted_avg_oil(group):
    return (group['Emission_Factor'] * group['Activity']).sum() / group['Activity'].sum()


# Group by country
df_country_CO2factor_oil = df_oil.groupby('Country__Iso_3_').apply(weighted_avg_oil)


# Change the name for the column
df_country_CO2factor_oil.name = 'O&G_WA_Emissions_Factor'


# Reset the index
df_country_CO2factor_oil = df_country_CO2factor_oil.reset_index()



# In[5]:
# create a function to get weighted average for emissions intensity
# GAS --- million tonnes of CO2 per MWh

def weighted_avg_gas(group):
    return (group['Emission_Factor'] * group['Activity']).sum() / group['Activity'].sum()


# Group by country
df_country_CO2factor_gas = df_gas.groupby('Country__Iso_3_').apply(weighted_avg_gas)


# Change the name for the column
df_country_CO2factor_gas.name = 'O&G_WA_Emissions_Factor'


# Reset the index
df_country_CO2factor_gas = df_country_CO2factor_gas.reset_index()



# In[5]:
# create a function to get weighted average for emissions intensity
# COAL --- kg of CO2 per TJ

def weighted_avg_coal(group):
    return (group['new_factor'] * group['Activity']).sum() / group['Activity'].sum()


# Group by country
df_country_CO2factor_coal = df_coal.groupby('Country (Iso-3)').apply(weighted_avg_coal)


# Change the name for the column
df_country_CO2factor_coal.name = 'Coal_WA_Emissions_Factor'


# Reset the index
df_country_CO2factor_coal = df_country_CO2factor_coal.reset_index()



# In[6]:
# Export data

df_country_CO2factor_coal.to_excel('2 - output/script 1/1 - country_power_co2factor_coal.xlsx', index=False)
df_country_CO2factor_oil.to_excel('2 - output/script 1/2 - country_power_co2factor_oil.xlsx', index=False)
df_country_CO2factor_gas.to_excel('2 - output/script 1/3 - country_power_co2factor_gas.xlsx', index=False)






