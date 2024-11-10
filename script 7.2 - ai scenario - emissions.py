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
df_cp_emissions = pd.read_excel('2 - output/script 4.2/9.1 - Current policy - Secondary - annual.xlsx')







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










# In[4]: GET GHG INTENTITY FACTORS
##################################

# --------------
# get emissions intensity by country
# this function creates a weighted average by countries (emissions by activity)
def weighted_avg_intensity_coal(group):
    return (group['emissions_factor_perMWh'] * group['activity']).sum() / group['activity'].sum()

def weighted_avg_intensity_gas_oil(group):
    return (group['emission_factor'] * group['activity']).sum() / group['activity'].sum()



# apply the function --- this also directs them to dictionaries
df_power_coal_intensity = df_power_coal.groupby('countryiso3').apply(weighted_avg_intensity_coal).reset_index().set_index('countryiso3')[0].to_dict()
df_power_gas_intensity = df_power_gas.groupby('countryiso3').apply(weighted_avg_intensity_gas_oil).reset_index().set_index('countryiso3')[0].to_dict()
df_power_oil_intensity = df_power_oil.groupby('countryiso3').apply(weighted_avg_intensity_gas_oil).reset_index().set_index('countryiso3')[0].to_dict()


# global average
df_power_coal_intensity_global = weighted_avg_intensity_coal(df_power_coal)
df_power_gas_intensity_global = weighted_avg_intensity_gas_oil(df_power_gas)
df_power_oil_intensity_global = weighted_avg_intensity_gas_oil(df_power_oil)










# In[5]: SET DICTIONARIES 
####################################
# --------------
# Define the list of fuel types to apply the calculation to
fuel_types = ["Secondary Energy|Electricity|Coal", "Secondary Energy|Electricity|Oil", "Secondary Energy|Electricity|Gas"]
global_intensities  = {"Secondary Energy|Electricity|Coal": df_power_coal_intensity_global, "Secondary Energy|Electricity|Oil": df_power_oil_intensity_global, "Secondary Energy|Electricity|Gas": df_power_gas_intensity_global}
intensity_factors = {"Secondary Energy|Electricity|Coal": df_power_coal_intensity, "Secondary Energy|Electricity|Oil": df_power_oil_intensity,"Secondary Energy|Electricity|Gas": df_power_gas_intensity}










# In[5]: CONVERT TWH to GHG
####################################

# GHG = TWH * intensity factor
# utilziation factors are country and fuel type specific


# --------------
# create new data frames
df_emissions_cpfaai_b = df_electricity_cpfaai_b.copy()
df_emissions_cpfaai_h = df_electricity_cpfaai_h.copy()
df_emissions_cpfaai_l = df_electricity_cpfaai_l.copy()



# --------------
# Define the list of dataframes to apply the calculation to
dataframes = [df_emissions_cpfaai_b, df_emissions_cpfaai_h, df_emissions_cpfaai_l]



# --------------
# Loop over each DataFrame and fuel type
for df in dataframes:
    for fuel in fuel_types:
        # Create a mask for rows with the specific fuel type
        fuel_mask = df['Variable'] == fuel
        
        # Create a mask for regions marked as "Downscaling|Countries without IEA statistics"
        global_region_mask = df['Region'] == "Downscaling|Countries without IEA statistics"
        
        # Calculate capacity for rows with the specified fuel type, using region-specific or global utilization
        df.loc[fuel_mask & ~global_region_mask, years_2024] = (
            df.loc[fuel_mask & ~global_region_mask, years_2024]
            .mul(10**6)      # converts to MW
            .mul(df['Region'].map(intensity_factors[fuel]), axis=0)   # Use intensity factors
        )
        
        # Apply the global utilization factor for "Downscaling|Countries without IEA statistics"
        df.loc[fuel_mask & global_region_mask, years_2024] = (
            df.loc[fuel_mask & global_region_mask, years_2024]
            .mul(10**6)      # converts to MW
            .mul(global_intensities[fuel])  # Use intensity factors
        )
    
    # Set the unit for the entire DataFrame to "MW"
    df['Unit'] = "Mt CO2"











# In[5]: DELETE EXTRAS
####################################

# delete
del df, dataframes, fuel_types, fuel, fuel_mask, global_region_mask,
del global_intensities, intensity_factors
del df_power_coal_intensity, df_power_coal_intensity_global, df_power_gas_intensity, df_power_gas_intensity_global, df_power_oil_intensity, df_power_oil_intensity_global
del df_electricity_cpfaai_b, df_electricity_cpfaai_h, df_electricity_cpfaai_l
del df_power_coal, df_power_gas, df_power_oil










# In[5]: AVOIDED EMISSIONS
# ####################################

# # --------------
# # get dataframes
# df_avoidedghg_cpfaai_b = df_emissions_cpfaai_b.reset_index(drop=True)
# df_avoidedghg_cpfaai_h = df_emissions_cpfaai_h.reset_index(drop=True)
# df_avoidedghg_cpfaai_l = df_emissions_cpfaai_l.reset_index(drop=True)


# # --------------
# # Define the list of dataframes to apply the calculation to
# dataframes = [df_avoidedghg_cpfaai_b, df_avoidedghg_cpfaai_h, df_avoidedghg_cpfaai_l]



# # --------------
# # Loop over each DataFrame
# for df in dataframes:
#     for year in years_2024:
        
#         df[year] = df[year] - df_nz1550v2_emissions.loc[
#             (df_nz1550v2_emissions['Region'] == df['Region']) & 
#             (df_nz1550v2_emissions['Variable'] == df['Variable']), year].values
        
#         df['2024'] = 0
    

# # delete
# del df, year, dataframes






# In[5]: AVOIDED EMISSIONS BY COUNTRY * REGION
# ####################################

# # Define the list of dataframes to apply the calculation to
# dataframes = [df_avoidedghg_cpfaai_b, df_avoidedghg_cpfaai_h, df_avoidedghg_cpfaai_l]

# # List of countries to include in the summary
# temp_countries = ['DEU', 'IND', 'IDN', 'TUR', 'USA', 'VNM', 'POL', 'KAZ']

# # Variables to store each output DataFrame separately
# summary_base, summary_high, summary_low = None, None, None


# # Loop over each DataFrame in dataframes
# summary_dfs = []  # To store the resulting dataframes
# for df in dataframes:
#     # Step 1: Group by 'Region' and sum across rows for each country in temp_countries
#     country_data = df[df['Region'].isin(temp_countries)].groupby('Region')[years_2024].sum()

#     # Step 2: Calculate EMDE sum by filtering for 'emerging' and 'developing' development levels and summing across rows
#     emde_data = df[df['development_level'].isin(['Emerging', 'Developing'])][years_2024].sum().to_frame().T
#     emde_data.index = ['EMDE']  # Rename the index to 'EMDE'

#     # Step 3: Calculate Global sum across all regions and years
#     global_data = df[years_2024].sum().to_frame().T
#     global_data.index = ['Global']  # Rename the index to 'Global'

#     # Step 4: Concatenate country data, EMDE, and Global to form the final summary table
#     summary_table = pd.concat([country_data, emde_data, global_data])

#     # Append each summary table to the list
#     summary_dfs.append(summary_table)

# # Unpack summary_dfs to get the final three separate DataFrames
# summary_base, summary_high, summary_low = summary_dfs

# summary_base = summary_base.reset_index()
# summary_high = summary_high.reset_index()
# summary_low = summary_low.reset_index()


# # delete
# del df, dataframes, temp_countries, summary_dfs, summary_table, emde_data, global_data, country_data










# In[10]:
# Export data

# # avoided capacity - by coutnry
# df_avoidedghg_cpfaai_b.to_excel('2 - output/script 7.2 - ai scenarios - avoided emissions/7.1.1 - avoided ghg - by country - cpfaai - base.xlsx', index=False)
# df_avoidedghg_cpfaai_h.to_excel('2 - output/script 7.2 - ai scenarios - avoided emissions/7.1.2 - avoided ghg - by country - cpfaai - high.xlsx', index=False)
# df_avoidedghg_cpfaai_l.to_excel('2 - output/script 7.2 - ai scenarios - avoided emissions/7.1.3 - avoided ghg - by country - cpfaai - low.xlsx', index=False)

# # avoided capacity - summary tabels
# summary_base.to_excel('2 - output/script 7.2 - ai scenarios - avoided emissions/7.2.1 - avoided ghg - summary - cpfaai - base.xlsx', index=False)
# summary_high.to_excel('2 - output/script 7.2 - ai scenarios - avoided emissions/7.2.2 - avoided ghg - summary - cpfaai - high.xlsx', index=False)
# summary_low.to_excel('2 - output/script 7.2 - ai scenarios - avoided emissions/7.2.3 - avoided ghg - summary - cpfaai - low.xlsx', index=False)


# emissions - by country & fuel type
df_emissions_cpfaai_b.to_excel('2 - output/script 7.2 - ai scenarios - emissions/7.1.1 - emissions - by country - cpfaai - base.xlsx', index=False)
df_emissions_cpfaai_h.to_excel('2 - output/script 7.2 - ai scenarios - emissions/7.1.2 - emissions - by country - cpfaai - high.xlsx', index=False)
df_emissions_cpfaai_l.to_excel('2 - output/script 7.2 - ai scenarios - emissions/7.1.3 - emissions - by country - cpfaai - low.xlsx', index=False)





