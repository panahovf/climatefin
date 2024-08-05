# In[1]:
# Date: July 28, 2024
# Project: Country level emissions intensity data for power sector from FA data
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

directory = r'C:\Users\panah\OneDrive\Desktop\Work\2 - RA - Climate fin'
os.chdir(directory)
del directory


# load power data
df_power_all = pd.read_csv("1 - input/v3_power_Forward_Analytics2024.csv")



# In[4]:

# filter by operating
df_power_all = df_power_all[df_power_all['status'] == "operating"]    

# break oil and gas separately
df_power_oil = df_power_all[df_power_all['subsector'] == "Oil"]
df_power_gas = df_power_all[df_power_all['subsector'] == "Gas"]
df_power_coal = df_power_all[df_power_all['subsector'] == "Coal"]

# create emissions factor in coal dataset MTCO2 per MWH
df_power_coal['emissions_factor_perMWh'] = df_power_coal['annual_co2_calc']/df_power_coal['activity']


# In[5.1]:
# create a function to get weighted average for emissions intensity
# OIL --- million tonnes of CO2 per MWh

def weighted_avg_oil(group):
    return (group['emission_factor'] * group['activity']).sum() / group['activity'].sum()


# Group by country
df_country_CO2factor_oil = df_power_oil.groupby('countryiso3').apply(weighted_avg_oil)


# Change the name for the column
df_country_CO2factor_oil.name = 'O&G_WA_Emissions_Factor'


# Reset the index
df_country_CO2factor_oil = df_country_CO2factor_oil.reset_index()



# In[5.2]:
# create a function to get weighted average for emissions intensity
# GAS --- million tonnes of CO2 per MWh

def weighted_avg_gas(group):
    return (group['emission_factor'] * group['activity']).sum() / group['activity'].sum()


# Group by country
df_country_CO2factor_gas = df_power_gas.groupby('countryiso3').apply(weighted_avg_gas)


# Change the name for the column
df_country_CO2factor_gas.name = 'O&G_WA_Emissions_Factor'


# Reset the index
df_country_CO2factor_gas = df_country_CO2factor_gas.reset_index()



# In[5]:
# create a function to get weighted average for emissions intensity
# COAL --- million tonnes of CO2 per MWh --- USING CALCULATED CO2 PER MWH

def weighted_avg_coal(group):
    return (group['emissions_factor_perMWh'] * group['activity']).sum() / group['activity'].sum()


# Group by country
df_country_CO2factor_coal = df_power_coal.groupby('countryiso3').apply(weighted_avg_coal)


# Change the name for the column
df_country_CO2factor_coal.name = 'Coal_WA_Emissions_Factor'


# Reset the index
df_country_CO2factor_coal = df_country_CO2factor_coal.reset_index()



# In[6]:
# Export data

df_country_CO2factor_coal.to_excel('2 - output/script 1/1 - country_power_co2factor_coal.xlsx', index=False)
df_country_CO2factor_oil.to_excel('2 - output/script 1/2 - country_power_co2factor_oil.xlsx', index=False)
df_country_CO2factor_gas.to_excel('2 - output/script 1/3 - country_power_co2factor_gas.xlsx', index=False)






