# In[1]:
# Date: Oct 31, 2024
# Project: Incorporating AI growth to NGFS scenarios --- getting avoided fossil fuels capacity
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
# FORWARD ANALYTICS DATA
df_power_coal = pd.read_excel('2 - output/script 1/4 - power - coal.xlsx')
df_power_gas = pd.read_excel('2 - output/script 1/5 - power - gas.xlsx')
df_power_oil = pd.read_excel('2 - output/script 1/6 - power - oil.xlsx')


# ---------------------------- 
# LOAD FA AI SCENARIOS
df_electricity_cpfaai_b = pd.read_excel('2 - output/script 7.1 - ai scenarios - electricity generation/7.2.2 - electricity generation - by country and type - cp fa ai - base.xlsx')
df_electricity_cpfaai_h = pd.read_excel('2 - output/script 7.1 - ai scenarios - electricity generation/7.2.3 - electricity generation - by country and type - cp fa ai - high.xlsx')
df_electricity_cpfaai_l = pd.read_excel('2 - output/script 7.1 - ai scenarios - electricity generation/7.2.4 - electricity generation - by country and type - cp fa ai - low.xlsx')


# ---------------------------- 
# LOAD NZ 1.5C 50% SCENARIO & CP SCENARIOS
df_nz1550v2_emissions = pd.read_excel('2 - output/script 4.2/6.1 - NZ-15-50 - v2 - Secondary - annual.xlsx')








# In[5]: SET YEAR COLUMNS
########################################################
years_2024 = [str(year) for year in range(2024, 2051)]






# In[5]: BRING DEVELPOMENT LEVELS FOR EMDE REGION
####################################

# Create mappings for development_level and gca_region based on df_nz1550v2_emissions
development_level_mapping = df_nz1550v2_emissions.set_index('Region')['development_level'].to_dict()
gca_region_mapping = df_nz1550v2_emissions.set_index('Region')['gca_region'].to_dict()

# List of DataFrames to work with
dataframes = [df_electricity_cpfaai_b, df_electricity_cpfaai_h, df_electricity_cpfaai_l]


# Loop over each DataFrame to add the new columns and rearrange them
for idx, df in enumerate(dataframes):
    # Add the new columns using the mappings
    df['gca_region'] = df['Region'].map(gca_region_mapping)
    df['development_level'] = df['Region'].map(development_level_mapping)
    
    
# delete
del dataframes, development_level_mapping, df, gca_region_mapping, idx







# In[5]: FILTER FOR FOSSIL FUELS ONLY
########################################################

# Define the list of variables to filter by
filter_variables = [
    'Secondary Energy|Electricity|Coal',
    'Secondary Energy|Electricity|Oil',
    'Secondary Energy|Electricity|Gas'
]

# Filter each DataFrame
df_electricity_cpfaai_b = df_electricity_cpfaai_b[df_electricity_cpfaai_b['Variable'].isin(filter_variables)]
df_electricity_cpfaai_h = df_electricity_cpfaai_h[df_electricity_cpfaai_h['Variable'].isin(filter_variables)]
df_electricity_cpfaai_l = df_electricity_cpfaai_l[df_electricity_cpfaai_l['Variable'].isin(filter_variables)]


# delete
del filter_variables










# In[4]: GET UTILIZATION FACTORS
##################################

# --------------
# get capacity factors by country (utilization factor)
# this function creates a weighted average by countries (emissions by activity)
def weighted_avg_utilization(group):
    return (group['capacity_factor'] * group['activity']).sum() / group['activity'].sum()


# apply the function
df_power_coal_utilization = df_power_coal.groupby('countryiso3').apply(weighted_avg_utilization).reset_index().set_index('countryiso3')[0].to_dict()
df_power_gas_utilization = df_power_gas.groupby('countryiso3').apply(weighted_avg_utilization).reset_index().set_index('countryiso3')[0].to_dict()
df_power_oil_utilization = df_power_oil.groupby('countryiso3').apply(weighted_avg_utilization).reset_index().set_index('countryiso3')[0].to_dict()


# global average
df_power_coal_utilization_global = weighted_avg_utilization(df_power_coal)
df_power_gas_utilization_global = weighted_avg_utilization(df_power_gas)
df_power_oil_utilization_global = weighted_avg_utilization(df_power_oil)











# In[5]: SET DICTIONARIES 
####################################
# --------------
# Define the list of fuel types to apply the calculation to
fuel_types = ["Secondary Energy|Electricity|Coal", "Secondary Energy|Electricity|Oil", "Secondary Energy|Electricity|Gas"]
global_utilization  = {"Secondary Energy|Electricity|Coal": df_power_coal_utilization_global, "Secondary Energy|Electricity|Oil": df_power_oil_utilization_global, "Secondary Energy|Electricity|Gas": df_power_gas_utilization_global}
utilization_factors = {"Secondary Energy|Electricity|Coal": df_power_coal_utilization, "Secondary Energy|Electricity|Oil": df_power_oil_utilization,"Secondary Energy|Electricity|Gas": df_power_gas_utilization}










# In[5]: CONVERT TWH to GHG
####################################

# Total Capacity MW = TWH*(10^6) / (24*365) / intensity factor
# utilziation factors are country and fuel type specific


# --------------
# create new data frames
df_capacity_total_cpfaai_b = df_electricity_cpfaai_b.copy()
df_capacity_total_cpfaai_h = df_electricity_cpfaai_h.copy()
df_capacity_total_cpfaai_l = df_electricity_cpfaai_l.copy()

df_capacity_used_cpfaai_b = df_electricity_cpfaai_b.copy()
df_capacity_used_cpfaai_h = df_electricity_cpfaai_h.copy()
df_capacity_used_cpfaai_l = df_electricity_cpfaai_l.copy()

# --------------
# Define the list of dataframes to apply the calculation to
dataframes_capacity_total = [df_capacity_total_cpfaai_b, df_capacity_total_cpfaai_h, df_capacity_total_cpfaai_l]
dataframes_capacity_used = [df_capacity_used_cpfaai_b, df_capacity_used_cpfaai_h, df_capacity_used_cpfaai_l]



# --------------
# Loop over each DataFrame and fuel type
for df in dataframes_capacity_total:
    for fuel in fuel_types:
        # Create a mask for rows with the specific fuel type
        fuel_mask = df['Variable'] == fuel
        
        # Create a mask for regions marked as "Downscaling|Countries without IEA statistics"
        global_region_mask = df['Region'] == "Downscaling|Countries without IEA statistics"
        
        # Calculate capacity for rows with the specified fuel type, using region-specific or global utilization
        df.loc[fuel_mask & ~global_region_mask, years_2024] = (
            df.loc[fuel_mask & ~global_region_mask, years_2024]
            .mul(10**6)      # converts to MW
            .div(24*365)
            .div(df['Region'].map(utilization_factors[fuel]), axis=0)   # Use intensity factors
        )
        
        # Apply the global utilization factor for "Downscaling|Countries without IEA statistics"
        df.loc[fuel_mask & global_region_mask, years_2024] = (
            df.loc[fuel_mask & global_region_mask, years_2024]
            .mul(10**6)      # converts to MW
            .div(24*365)
            .div(global_utilization[fuel])  # Use utilization factors
        )
    
    # Set the unit for the entire DataFrame to "MW"
    df['Unit'] = "MW"





# --------------
# Loop over each DataFrame and fuel type
for df in dataframes_capacity_used:
    df[years_2024] = df[years_2024].mul(10**6).div(24*365)     # first converts TWh to MWh and theny to MW
    df['Unit'] = "MW (used)"








# In[5]: DELETE EXTRAS
####################################

# delete
del df, dataframes_capacity_total, dataframes_capacity_used, fuel_types, fuel, fuel_mask, global_region_mask,
del global_utilization, utilization_factors
del df_power_coal_utilization, df_power_coal_utilization_global, df_power_gas_utilization, df_power_gas_utilization_global, df_power_oil_utilization, df_power_oil_utilization_global
del df_electricity_cpfaai_b, df_electricity_cpfaai_h, df_electricity_cpfaai_l
del df_power_coal, df_power_gas, df_power_oil














# In[10]:
# Export data

# total capacity - by coutnry
df_capacity_total_cpfaai_b.to_excel('2 - output/script 7.3 - ai scenarios - capacity/7.1.1 - capacity total - by country - cpfaai - base.xlsx', index=False)
df_capacity_total_cpfaai_h.to_excel('2 - output/script 7.3 - ai scenarios - capacity/7.1.2 - capacity total - by country - cpfaai - high.xlsx', index=False)
df_capacity_total_cpfaai_l.to_excel('2 - output/script 7.3 - ai scenarios - capacity/7.1.3 - capacity total - by country - cpfaai - low.xlsx', index=False)


# used capacity - by coutnry
df_capacity_used_cpfaai_b.to_excel('2 - output/script 7.3 - ai scenarios - capacity/7.2.1 - capacity used - by country - cpfaai - base.xlsx', index=False)
df_capacity_used_cpfaai_h.to_excel('2 - output/script 7.3 - ai scenarios - capacity/7.2.2 - capacity used - by country - cpfaai - high.xlsx', index=False)
df_capacity_used_cpfaai_l.to_excel('2 - output/script 7.3 - ai scenarios - capacity/7.2.3 - capacity used - by country - cpfaai - low.xlsx', index=False)


