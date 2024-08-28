# In[1]:
# Date: Aug 27, 2024
# Project: Plotting emissions results for Poland --- Extraction
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
import seaborn as sns










# In[3]:
# directory & load data

directory = r'C:\Users\panah\OneDrive\Desktop\Work\2 - RA - Climate fin'
os.chdir(directory)
del directory


# --------------
# load data from SCRIPT 4.2
# first set the following function to avoid error --- this is a function within a chart
def thousands_formatter(x, pos):
    return f'{int(x/1000)}' 
# now data is loaded


# --------------
# LOAD POWER DATA
df_extraction_coal = pd.read_excel('2 - output/script 1/4 - extraction_coal.xlsx')
df_extraction_gas = pd.read_excel('2 - output/script 1/5 - extraction_gas.xlsx')
df_extraction_oil = pd.read_excel('2 - output/script 1/6 - extraction_oil.xlsx')










# In[4]: DELETE ALL UNNECESSARY ITEMS
#####################################

# --------------
# remove all variables
del ax, bottom, df_carbon_bugdet, extraction_colors, fig, fuel, power_colors
del var_total2050_currentpolicy, var_total2050_netzero, year_columns, year_columns2


# remove secondary related dataframes
del df_change_secondary_currentpolicy, df_change_secondary_netzero
del df_emissions_secondary_currentpolicy, df_emissions_secondary_netzero
del df_ngfs_secondary_currentpolicy, df_ngfs_secondary_netzero


# remove NZ15 50% primary, residual, total, and aggregate secondary
del df_nz15_50_secondary_change_v1, df_nz15_50_secondary_change_v2, df_nz15_50_secondary_v1
del df_nz15_50_secondary_v1_annual, df_nz15_50_secondary_v1_total
del df_nz15_50_secondary_v2, df_nz15_50_secondary_v2_total
del df_nz15_50_residual_change_v1, df_nz15_50_residual_change_v2
del df_nz15_50_residual_v1, df_nz15_50_residual_v2, df_nz15_50_residual_v1_total, df_nz15_50_residual_v2_total
del df_nz15_50_primary_v1_annual, df_nz15_50_primary_v1_total, df_nz15_50_primary_v2_total
del df_nz15_50_total_v1, df_nz15_50_total_v1_annual, df_nz15_50_total_v2


# remove NZ15 67% primary, residual, total, and aggregate secondary
del df_nz15_67_secondary_change_v1, df_nz15_67_secondary_change_v2, df_nz15_67_secondary_v1, df_nz15_67_secondary_v1_annual, df_nz15_67_secondary_v1_total
del df_nz15_67_secondary_v2, df_nz15_67_secondary_v2_total
del df_nz15_67_residual_change_v1, df_nz15_67_residual_change_v2, df_nz15_67_residual_v1, df_nz15_67_residual_v1_total, df_nz15_67_residual_v2_total, df_nz15_67_residual_v2
del df_nz15_67_primary_v1_annual, df_nz15_67_primary_v1_total, df_nz15_67_primary_v2_total 
del df_nz15_67_total_v1, df_nz15_67_total_v2, df_nz15_67_total_v1_annual 


# remove NZ16 50% primary, residual, total, and aggregate secondary
del df_nz16_67_secondary_change_v1, df_nz16_67_secondary_change_v2, df_nz16_67_secondary_v1,df_nz16_67_secondary_v2
del df_nz16_67_secondary_v1_annual, df_nz16_67_secondary_v1_total, df_nz16_67_secondary_v2_total
del df_nz16_67_residual_change_v1, df_nz16_67_residual_change_v2, df_nz16_67_residual_v1, df_nz16_67_residual_v2, df_nz16_67_residual_v1_total, df_nz16_67_residual_v2_total 
del df_nz16_67_primary_v1_annual, df_nz16_67_primary_v1_total, df_nz16_67_primary_v2_total 
del df_nz16_67_total_v1, df_nz16_67_total_v2, df_nz16_67_total_v1_annual 


# remove ratios, and resicuals
del df_ratio_currentpolicy, df_ratio_netzero, df_reduction_netzero_v1, df_reduction_netzero_v2 
del df_residual_currentpolicy, df_residual_currentpolicy_change, df_residual_netzero, df_residual_netzero_change


# remove temporary data frames
del df_temp_primary_netzero, df_temp_primary_netzero_change, df_temp_residual_netzero, df_temp_residual_netzero_change
del df_temp_secondary_netzero, df_temp_secondary_netzero_change


# remove total emissions, changes, and ngfs related data
del df_total_annual_netzero, df_total_annual_currentpolicy, df_total_cumulative_currentpolicy, df_total_cumulative_netzero
del df_change_primary_currentpolicy, df_change_primary_netzero
del df_ngfs_annual_change, df_ngfs_primary_currentpolicy, df_ngfs_primary_netzero


# keep only VERSION 2 (remove V1)
del df_nz15_50_primary_change_v1, df_nz15_50_primary_v1, df_nz15_67_primary_change_v1, df_nz15_67_primary_v1, df_nz16_67_primary_change_v1, df_nz16_67_primary_v1


# remove NZ 1.6C scenario
del df_nz16_67_primary_v2, df_nz16_67_primary_change_v2


# remove 'annual change' dataframe
del df_nz15_67_primary_change_v2, df_nz15_50_primary_change_v2










# In[4]: FILTER FOR POLAND
############################

# --------------
# Case 1: Current policy
df_poland_currentpolicy = df_emissions_primary_currentpolicy[df_emissions_primary_currentpolicy["Region"] == "POL"]


# --------------
# Case 2: Netzero
df_poland_netzero = df_emissions_primary_netzero[df_emissions_primary_netzero["Region"] == "POL"]


# --------------
# Case 3: Netzero 1.5C 50% & 67% adjusted
df_poland_nz15_50 = df_nz15_50_primary_v2[df_nz15_50_primary_v2["Region"] == "POL"]
df_poland_nz15_67 = df_nz15_67_primary_v2[df_nz15_67_primary_v2["Region"] == "POL"]










# In[4]: GET GHG INTENTITY FACTORS
##################################

# --------------
# first set intensity variable --- GHG / Production
df_extraction_coal['intensity'] = df_extraction_coal['emissions_co2e_million_tonnes'] / df_extraction_coal['activity']
df_extraction_gas['intensity'] = df_extraction_gas['emissions_co2e_million_tonnes'] / df_extraction_gas['activity']
df_extraction_oil['intensity'] = df_extraction_oil['emissions_co2e_million_tonnes'] / df_extraction_oil['activity']


# --------------
# get emissions intensity for POLAND
# this function creates a weighted average by countries (emissions by activity)
def weighted_avg_intensity(group):
    return (group['intensity'] * group['activity']).sum() / group['activity'].sum()


# apply the function
df_extraction_coal_intensity = df_extraction_coal.groupby('country_iso_3').apply(weighted_avg_intensity)
df_extraction_gas_intenstiy = df_extraction_gas.groupby('country_iso_3').apply(weighted_avg_intensity)
df_extraction_oil_intenstiy = df_extraction_oil.groupby('country_iso_3').apply(weighted_avg_intensity)










# In[4]: CONVERT EMISSIONS TO GENERATION
########################################

# Divide emissions by the intensity factors to get production values
# GHG / (GHG/Production) = Production
# Production:
#   Coal: Mtpa
#   Gas: million m³/y
#   Oil: million bbl/y


# --------------
# get intensity factor values for poland
intensity_coal = df_extraction_coal_intensity["POL"]
intensity_gas = df_extraction_gas_intenstiy["POL"]
intensity_oil = df_extraction_oil_intenstiy["POL"]


del df_extraction_coal_intensity, df_extraction_gas_intenstiy, df_extraction_oil_intenstiy
del df_extraction_coal, df_extraction_gas, df_extraction_oil





########################################################
#  1. CURRENT POLICY -----------------------------------
########################################################

df_poland_currentpolicy_production = df_poland_currentpolicy.copy() # create a new df


# --------------
# Production
# 1 - coal
df_poland_currentpolicy_production.loc[df_poland_currentpolicy_production['fuel_type'] == "Coal", common_years] = ( 
    df_poland_currentpolicy_production.loc[df_poland_currentpolicy_production['fuel_type'] == "Coal", common_years]
    .div(intensity_coal)
    )


# 2 - gas
df_poland_currentpolicy_production.loc[df_poland_currentpolicy_production['fuel_type'] == "Gas", common_years] = ( 
    df_poland_currentpolicy_production.loc[df_poland_currentpolicy_production['fuel_type'] == "Gas", common_years]
    .div(intensity_gas)
    )


# 3 - oil
df_poland_currentpolicy_production.loc[df_poland_currentpolicy_production['fuel_type'] == "Oil", common_years] = ( 
    df_poland_currentpolicy_production.loc[df_poland_currentpolicy_production['fuel_type'] == "Oil", common_years]
    .div(intensity_oil)
    )





########################################################
#  2. NET ZERO -----------------------------------------
########################################################

df_poland_netzero_production = df_poland_netzero.copy() # create a new df


# --------------
# Production
# 1 - coal
df_poland_netzero_production.loc[df_poland_netzero_production['fuel_type'] == "Coal", common_years] = ( 
    df_poland_netzero_production.loc[df_poland_netzero_production['fuel_type'] == "Coal", common_years]
    .div(intensity_coal)
    )


# 2 - gas
df_poland_netzero_production.loc[df_poland_netzero_production['fuel_type'] == "Gas", common_years] = ( 
    df_poland_netzero_production.loc[df_poland_netzero_production['fuel_type'] == "Gas", common_years]
    .div(intensity_gas)
    )


# 3 - oil
df_poland_netzero_production.loc[df_poland_netzero_production['fuel_type'] == "Oil", common_years] = ( 
    df_poland_netzero_production.loc[df_poland_netzero_production['fuel_type'] == "Oil", common_years]
    .div(intensity_oil)
    )





########################################################
#  3. NET ZERO 1.5C 67% adjusted -----------------------
########################################################

df_poland_nz15_67_production = df_poland_nz15_67.copy() # create a new df


# --------------
# Production
# 1 - coal
df_poland_nz15_67_production.loc[df_poland_nz15_67_production['fuel_type'] == "Coal", common_years] = ( 
    df_poland_nz15_67_production.loc[df_poland_nz15_67_production['fuel_type'] == "Coal", common_years]
    .div(intensity_coal)
    )


# 2 - gas
df_poland_nz15_67_production.loc[df_poland_nz15_67_production['fuel_type'] == "Gas", common_years] = ( 
    df_poland_nz15_67_production.loc[df_poland_nz15_67_production['fuel_type'] == "Gas", common_years]
    .div(intensity_gas)
    )


# 3 - oil
df_poland_nz15_67_production.loc[df_poland_nz15_67_production['fuel_type'] == "Oil", common_years] = ( 
    df_poland_nz15_67_production.loc[df_poland_nz15_67_production['fuel_type'] == "Oil", common_years]
    .div(intensity_oil)
    )





########################################################
#  4. NET ZERO 1.5C 50% adjusted -----------------------
########################################################

df_poland_nz15_50_production = df_poland_nz15_50.copy() # create a new df


# --------------
# Production
# 1 - coal
df_poland_nz15_50_production.loc[df_poland_nz15_50_production['fuel_type'] == "Coal", common_years] = ( 
    df_poland_nz15_50_production.loc[df_poland_nz15_50_production['fuel_type'] == "Coal", common_years]
    .div(intensity_coal)
    )


# 2 - gas
df_poland_nz15_50_production.loc[df_poland_nz15_50_production['fuel_type'] == "Gas", common_years] = ( 
    df_poland_nz15_50_production.loc[df_poland_nz15_50_production['fuel_type'] == "Gas", common_years]
    .div(intensity_gas)
    )


# 3 - oil
df_poland_nz15_50_production.loc[df_poland_nz15_50_production['fuel_type'] == "Oil", common_years] = ( 
    df_poland_nz15_50_production.loc[df_poland_nz15_50_production['fuel_type'] == "Oil", common_years]
    .div(intensity_oil)
    )





# delete extras
del intensity_coal, intensity_gas, intensity_oil










# In[4]: GET YEARS OVER YEAR ABSOLUTE DIFFERENCES
#################################################

# --------------
# emissions
df_poland_currentpolicy_diff = df_poland_currentpolicy.copy()
df_poland_currentpolicy_diff[common_years] = df_poland_currentpolicy_diff[common_years].diff(axis=1)

df_poland_netzero_diff = df_poland_netzero.copy()
df_poland_netzero_diff[common_years] = df_poland_netzero_diff[common_years].diff(axis=1)

df_poland_nz15_67_diff = df_poland_nz15_67.copy()
df_poland_nz15_67_diff[common_years] = df_poland_nz15_67_diff[common_years].diff(axis=1)

df_poland_nz15_50_diff = df_poland_nz15_50.copy()
df_poland_nz15_50_diff[common_years] = df_poland_nz15_50_diff[common_years].diff(axis=1)


# put these all together
temp_currentpolicy = df_poland_currentpolicy_diff[common_years].sum(axis=0)
temp_netzero = df_poland_netzero_diff[common_years].sum(axis=0)
temp_nz15_67 = df_poland_nz15_67_diff[common_years].sum(axis=0)
temp_nz15_50 = df_poland_nz15_50_diff[common_years].sum(axis=0)

# create dataframe to host the scenarios
df_poland_reduction_emissions = pd.DataFrame(columns=['scenario'] + common_years.tolist())

# add above scenarios
df_poland_reduction_emissions = pd.concat(
    [df_poland_reduction_emissions, 
     pd.DataFrame(data={'scenario': ['Current Policies'], **temp_currentpolicy.to_dict()}),
     pd.DataFrame(data={'scenario': ['Net Zero'], **temp_netzero.to_dict()}),
     pd.DataFrame(data={'scenario': ['Modified Net Zero: 1.5°C 67% likelyhood'], **temp_nz15_67.to_dict()}),
     pd.DataFrame(data={'scenario': ['Modified Net Zero: 1.5°C 50% likelyhood'], **temp_nz15_50.to_dict()})],
    ignore_index=True
)

# cumulative
df_poland_reduction_cumulative_emissions = df_poland_reduction_emissions.copy()
df_poland_reduction_cumulative_emissions[common_years] = df_poland_reduction_cumulative_emissions[common_years].cumsum(axis=1)


# delete extras
del temp_currentpolicy, temp_netzero, temp_nz15_50, temp_nz15_67





# --------------
# Production changes

# create diff datasets for each scenario
df_poland_currentpolicy_production_diff = df_poland_currentpolicy_production.copy()
df_poland_currentpolicy_production_diff[common_years] = df_poland_currentpolicy_production_diff[common_years].diff(axis=1)

df_poland_netzero_production_diff = df_poland_netzero_production.copy()
df_poland_netzero_production_diff[common_years] = df_poland_netzero_production_diff[common_years].diff(axis=1)

df_poland_nz15_67_production_diff = df_poland_nz15_67_production.copy()
df_poland_nz15_67_production_diff[common_years] = df_poland_nz15_67_production_diff[common_years].diff(axis=1)

df_poland_nz15_50_production_diff = df_poland_nz15_50_production.copy()
df_poland_nz15_50_production_diff[common_years] = df_poland_nz15_50_production_diff[common_years].diff(axis=1)


# now combine scenarios by fuel type
# 1 - coal
# create dataframe to host the scenarios
df_poland_production_diff_coal = df_poland_reduction_emissions.copy()


# add diff scenarios
df_poland_production_diff_coal.loc[df_poland_production_diff_coal['scenario'] == "Current Policies", common_years] = (
    df_poland_currentpolicy_production_diff.loc[df_poland_currentpolicy_production_diff['fuel_type'] == "Coal", common_years].values
    )

df_poland_production_diff_coal.loc[df_poland_production_diff_coal['scenario'] == "Net Zero", common_years] = (
    df_poland_netzero_production_diff.loc[df_poland_netzero_production_diff['fuel_type'] == "Coal", common_years].values
    )

df_poland_production_diff_coal.loc[df_poland_production_diff_coal['scenario'] == "Modified Net Zero: 1.5°C 67% likelyhood", common_years] = (
    df_poland_nz15_67_production_diff.loc[df_poland_nz15_67_production_diff['fuel_type'] == "Coal", common_years].values
    )

df_poland_production_diff_coal.loc[df_poland_production_diff_coal['scenario'] == "Modified Net Zero: 1.5°C 50% likelyhood", common_years] = (
    df_poland_nz15_50_production_diff.loc[df_poland_nz15_50_production_diff['fuel_type'] == "Coal", common_years].values
    )


# cumulative
df_poland_production_diff_cumulative_coal = df_poland_production_diff_coal.copy()
df_poland_production_diff_cumulative_coal[common_years] = df_poland_production_diff_cumulative_coal[common_years].cumsum(axis=1)



# 2 - gas
# create dataframe to host the scenarios
df_poland_production_diff_gas = df_poland_reduction_emissions.copy()


# add diff scenarios
df_poland_production_diff_gas.loc[df_poland_production_diff_gas['scenario'] == "Current Policies", common_years] = (
    df_poland_currentpolicy_production_diff.loc[df_poland_currentpolicy_production_diff['fuel_type'] == "Gas", common_years].values
    )

df_poland_production_diff_gas.loc[df_poland_production_diff_gas['scenario'] == "Net Zero", common_years] = (
    df_poland_netzero_production_diff.loc[df_poland_netzero_production_diff['fuel_type'] == "Gas", common_years].values
    )

df_poland_production_diff_gas.loc[df_poland_production_diff_gas['scenario'] == "Modified Net Zero: 1.5°C 67% likelyhood", common_years] = (
    df_poland_nz15_67_production_diff.loc[df_poland_nz15_67_production_diff['fuel_type'] == "Gas", common_years].values
    )

df_poland_production_diff_gas.loc[df_poland_production_diff_gas['scenario'] == "Modified Net Zero: 1.5°C 50% likelyhood", common_years] = (
    df_poland_nz15_50_production_diff.loc[df_poland_nz15_50_production_diff['fuel_type'] == "Gas", common_years].values
    )


# cumulative
df_poland_production_diff_cumulative_gas = df_poland_production_diff_gas.copy()
df_poland_production_diff_cumulative_gas[common_years] = df_poland_production_diff_cumulative_gas[common_years].cumsum(axis=1)



# 3 - oil
# create dataframe to host the scenarios
df_poland_production_diff_oil = df_poland_reduction_emissions.copy()


# add diff scenarios
df_poland_production_diff_oil.loc[df_poland_production_diff_oil['scenario'] == "Current Policies", common_years] = (
    df_poland_currentpolicy_production_diff.loc[df_poland_currentpolicy_production_diff['fuel_type'] == "Oil", common_years].values
    )

df_poland_production_diff_oil.loc[df_poland_production_diff_oil['scenario'] == "Net Zero", common_years] = (
    df_poland_netzero_production_diff.loc[df_poland_netzero_production_diff['fuel_type'] == "Oil", common_years].values
    )

df_poland_production_diff_oil.loc[df_poland_production_diff_oil['scenario'] == "Modified Net Zero: 1.5°C 67% likelyhood", common_years] = (
    df_poland_nz15_67_production_diff.loc[df_poland_nz15_67_production_diff['fuel_type'] == "Oil", common_years].values
    )

df_poland_production_diff_oil.loc[df_poland_production_diff_oil['scenario'] == "Modified Net Zero: 1.5°C 50% likelyhood", common_years] = (
    df_poland_nz15_50_production_diff.loc[df_poland_nz15_50_production_diff['fuel_type'] == "Oil", common_years].values
    )


# cumulative
df_poland_production_diff_cumulative_oil = df_poland_production_diff_oil.copy()
df_poland_production_diff_cumulative_oil[common_years] = df_poland_production_diff_cumulative_oil[common_years].cumsum(axis=1)





# --------------
# Production levels

# 1 - coal
# create dataframe to host the scenarios
df_poland_production_coal = df_poland_reduction_emissions.copy()


# add diff scenarios
df_poland_production_coal.loc[df_poland_production_coal['scenario'] == "Current Policies", common_years] = (
    df_poland_currentpolicy_production.loc[df_poland_currentpolicy_production['fuel_type'] == "Coal", common_years].values
    )

df_poland_production_coal.loc[df_poland_production_coal['scenario'] == "Net Zero", common_years] = (
    df_poland_netzero_production.loc[df_poland_netzero_production['fuel_type'] == "Coal", common_years].values
    )

df_poland_production_coal.loc[df_poland_production_coal['scenario'] == "Modified Net Zero: 1.5°C 67% likelyhood", common_years] = (
    df_poland_nz15_67_production.loc[df_poland_nz15_67_production['fuel_type'] == "Coal", common_years].values
    )

df_poland_production_coal.loc[df_poland_production_coal['scenario'] == "Modified Net Zero: 1.5°C 50% likelyhood", common_years] = (
    df_poland_nz15_50_production.loc[df_poland_nz15_50_production['fuel_type'] == "Coal", common_years].values
    )


# cumulative
df_poland_production_cumulative_coal = df_poland_production_coal.copy()
df_poland_production_cumulative_coal[common_years] = df_poland_production_cumulative_coal[common_years].cumsum(axis=1)




# 2 - gas
# create dataframe to host the scenarios
df_poland_production_gas = df_poland_reduction_emissions.copy()


# add diff scenarios
df_poland_production_gas.loc[df_poland_production_gas['scenario'] == "Current Policies", common_years] = (
    df_poland_currentpolicy_production.loc[df_poland_currentpolicy_production['fuel_type'] == "Gas", common_years].values
    )

df_poland_production_gas.loc[df_poland_production_gas['scenario'] == "Net Zero", common_years] = (
    df_poland_netzero_production.loc[df_poland_netzero_production['fuel_type'] == "Gas", common_years].values
    )

df_poland_production_gas.loc[df_poland_production_gas['scenario'] == "Modified Net Zero: 1.5°C 67% likelyhood", common_years] = (
    df_poland_nz15_67_production.loc[df_poland_nz15_67_production['fuel_type'] == "Gas", common_years].values
    )

df_poland_production_gas.loc[df_poland_production_gas['scenario'] == "Modified Net Zero: 1.5°C 50% likelyhood", common_years] = (
    df_poland_nz15_50_production.loc[df_poland_nz15_50_production['fuel_type'] == "Gas", common_years].values
    )


# cumulative
df_poland_production_cumulative_gas = df_poland_production_gas.copy()
df_poland_production_cumulative_gas[common_years] = df_poland_production_cumulative_gas[common_years].cumsum(axis=1)





# 3 - oil
# create dataframe to host the scenarios
df_poland_production_oil = df_poland_reduction_emissions.copy()


# add diff scenarios
df_poland_production_oil.loc[df_poland_production_oil['scenario'] == "Current Policies", common_years] = (
    df_poland_currentpolicy_production.loc[df_poland_currentpolicy_production['fuel_type'] == "Oil", common_years].values
    )

df_poland_production_oil.loc[df_poland_production_oil['scenario'] == "Net Zero", common_years] = (
    df_poland_netzero_production.loc[df_poland_netzero_production['fuel_type'] == "Oil", common_years].values
    )

df_poland_production_oil.loc[df_poland_production_oil['scenario'] == "Modified Net Zero: 1.5°C 67% likelyhood", common_years] = (
    df_poland_nz15_67_production.loc[df_poland_nz15_67_production['fuel_type'] == "Oil", common_years].values
    )

df_poland_production_oil.loc[df_poland_production_oil['scenario'] == "Modified Net Zero: 1.5°C 50% likelyhood", common_years] = (
    df_poland_nz15_50_production.loc[df_poland_nz15_50_production['fuel_type'] == "Oil", common_years].values
    )


# cumulative
df_poland_production_cumulative_oil = df_poland_production_oil.copy()
df_poland_production_cumulative_oil[common_years] = df_poland_production_cumulative_oil[common_years].cumsum(axis=1)










# In[4]: GET AVOIDED EMISSIONS / CAPACITY / USED CAPACITY: BAU vs NZ 50%
########################################################################

# --------------
# Emissions
# get total annual emissions from CP & NZ15 50% and their diff
temp_currentpolicy = df_poland_currentpolicy[common_years].sum(axis=0)
temp_nz50 = df_poland_nz15_50[common_years].sum(axis=0)
temp_avoided = temp_currentpolicy - temp_nz50

# create a data frame - annual
df_poland_avoided_emissions = pd.DataFrame(data={'scenario': ['Avoided emissions'], **temp_avoided.to_dict()})

# cumulative
df_poland_avoided_cumulative_emissions = df_poland_avoided_emissions.copy()
df_poland_avoided_cumulative_emissions[common_years] = df_poland_avoided_cumulative_emissions[common_years].cumsum(axis=1)


# delete extras
del temp_currentpolicy, temp_avoided, temp_nz50










# In[]


#####################################################################
#####################################################################
#####################################################################
#####################################################################
########## PLOTS PLOTS PLOTS PLOTS PLOTS PLOTS PLOTS ################
#####################################################################
#####################################################################
#####################################################################
#####################################################################

# In[6]:  PREPARE DATASETS
###########################

# --------------
# get cumulative emissions dataframes
df_poland_currentpolicy_cumulative = df_poland_currentpolicy.copy()
df_poland_currentpolicy_cumulative[common_years] = df_poland_currentpolicy_cumulative[common_years].cumsum(axis=1)

df_poland_netzero_cumulative = df_poland_netzero.copy()
df_poland_netzero_cumulative[common_years] = df_poland_netzero_cumulative[common_years].cumsum(axis=1)

df_poland_nz15_67_cumulative = df_poland_nz15_67.copy()
df_poland_nz15_67_cumulative[common_years] = df_poland_nz15_67_cumulative[common_years].cumsum(axis=1)

df_poland_nz15_50_cumulative = df_poland_nz15_50.copy()
df_poland_nz15_50_cumulative[common_years] = df_poland_nz15_50_cumulative[common_years].cumsum(axis=1)


# --------------
# Define colors for extraction and power components
colors = {'Coal': '#255e7e', 'Gas': '#991f17', 'Oil':"#DE8F6E"}


# --------------
# set theme to seaborn
sns.set_theme(style="ticks")










# In[8]:

##################################################################################################
##################### EMISSION BY SCENARIOS ######################################################
##################################################################################################


# --------------
### 1. CUMULATIVE

# --------------
# 1.1 CURRENT POLICY
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the stacked areas for components of df_poland_currentpolicy_cumulative
bottom = pd.Series(0, index=common_years)

for fuel in df_poland_currentpolicy_cumulative['fuel_type'].unique():

    # Select the data for the current fuel type
    fuel_data = df_poland_currentpolicy_cumulative[df_poland_currentpolicy_cumulative['fuel_type'] == fuel][common_years]
    
    # Plot the stacked area
    ax.fill_between(common_years, bottom, bottom + fuel_data.iloc[0], 
                    label=f'{fuel}', color=colors.get(fuel, 'gray'), alpha=0.7)
    
    # Update the bottom for the next stacked area
    bottom += fuel_data.iloc[0]

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Set y-axis formatter to display values in thousands
ax = plt.gca()

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('MtCO2', fontsize = 15)
plt.title('Poland Current Policies: Cumulative Emissions from Fossil Fuel Extraction', fontsize=20, pad=60)
plt.text(0.5, 1.05, 'Emissions from current fossil fuel extraction facilities in operation are projected using growth rates \n from NGFS GCAM6 model', transform=ax.transAxes, ha='center', fontsize=12)

ax.legend(loc='upper left', fontsize=12)

plt.show()





# --------------
# 1.2 NET ZERO
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the stacked areas for components of df_poland_currentpolicy_cumulative
bottom = pd.Series(0, index=common_years)

for fuel in df_poland_netzero_cumulative['fuel_type'].unique():

    # Select the data for the current fuel type
    fuel_data = df_poland_netzero_cumulative[df_poland_netzero_cumulative['fuel_type'] == fuel][common_years]
    
    # Plot the stacked area
    ax.fill_between(common_years, bottom, bottom + fuel_data.iloc[0], 
                    label=f'{fuel}', color=colors.get(fuel, 'gray'), alpha=0.7)
    
    # Update the bottom for the next stacked area
    bottom += fuel_data.iloc[0]

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Set y-axis formatter to display values in thousands
ax = plt.gca()

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('MtCO2', fontsize = 15)
plt.title('Poland Net Zero: Cumulative Emissions from Fossil Fuel Extraction', fontsize=20, pad=60)
plt.text(0.5, 1.05, 'Emissions from current fossil fuel extraction in operation are projected using growth rates \n from NGFS GCAM6 model', transform=ax.transAxes, ha='center', fontsize=12)

ax.legend(loc='upper left', fontsize=12)

plt.show()





# --------------
# 1.3 NET ZERO 1.5C 67% aligned
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the stacked areas for components of df_poland_currentpolicy_cumulative
bottom = pd.Series(0, index=common_years)

for fuel in df_poland_nz15_67_cumulative['fuel_type'].unique():

    # Select the data for the current fuel type
    fuel_data = df_poland_nz15_67_cumulative[df_poland_nz15_67_cumulative['fuel_type'] == fuel][common_years]
    
    # Plot the stacked area
    ax.fill_between(common_years, bottom, bottom + fuel_data.iloc[0], 
                    label=f'{fuel}', color=colors.get(fuel, 'gray'), alpha=0.7)
    
    # Update the bottom for the next stacked area
    bottom += fuel_data.iloc[0]

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Set y-axis formatter to display values in thousands
ax = plt.gca()

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('MtCO2', fontsize = 15)
plt.title('Poland Modified Net Zero: Cumulative Emissions from Fossil Fuel Extraction', fontsize=20, pad=60)
plt.text(0.5, 1.03, 'Emissions from current fossil fuel extraction in operation are projected using modified growth rates \n from NGFS GCAM6 model to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 67% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)

ax.legend(loc='upper left', fontsize=12)

plt.show()





# --------------
# 1.4 NET ZERO 1.5C 50% aligned
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the stacked areas for components of df_poland_currentpolicy_cumulative
bottom = pd.Series(0, index=common_years)

for fuel in df_poland_nz15_50_cumulative['fuel_type'].unique():

    # Select the data for the current fuel type
    fuel_data = df_poland_nz15_50_cumulative[df_poland_nz15_50_cumulative['fuel_type'] == fuel][common_years]
    
    # Plot the stacked area
    ax.fill_between(common_years, bottom, bottom + fuel_data.iloc[0], 
                    label=f'{fuel}', color=colors.get(fuel, 'gray'), alpha=0.7)
    
    # Update the bottom for the next stacked area
    bottom += fuel_data.iloc[0]

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Set y-axis formatter to display values in thousands
ax = plt.gca()

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('MtCO2', fontsize = 15)
plt.title('Poland Modified Net Zero: Cumulative Emissions from Fossil Fuel Extraction', fontsize=20, pad=60)
plt.text(0.5, 1.03, 'Emissions from current fossil fuel extraction in operation are projected using modified growth rates \n from NGFS GCAM6 model to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)

ax.legend(loc='upper left', fontsize=12)

plt.show()










# --------------
### 2 . ANNUAL

# --------------
# 2.1 CURRENT POLICY
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the stacked areas for components of df_poland_currentpolicy_cumulative
bottom = pd.Series(0, index=common_years)

for fuel in df_poland_currentpolicy['fuel_type'].unique():

    # Select the data for the current fuel type
    fuel_data = df_poland_currentpolicy[df_poland_currentpolicy['fuel_type'] == fuel][common_years]
    
    # Plot the stacked area
    ax.fill_between(common_years, bottom, bottom + fuel_data.iloc[0], 
                    label=f'{fuel}', color=colors.get(fuel, 'gray'), alpha=0.7)
    
    # Update the bottom for the next stacked area
    bottom += fuel_data.iloc[0]

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Set y-axis formatter to display values in thousands
ax = plt.gca()

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('MtCO2', fontsize = 15)
plt.title('Poland Current Policies: Annual Emissions from Fossil Fuel Extraction', fontsize=20, pad=60)
plt.text(0.5, 1.05, 'Emissions from current fossil fuel extraction in operation are projected using growth rates \n from NGFS GCAM6 model', transform=ax.transAxes, ha='center', fontsize=12)

ax.legend(loc='upper left', fontsize=12)

plt.show()





# --------------
# 2.2 NET ZERO
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the stacked areas for components of df_poland_currentpolicy_cumulative
bottom = pd.Series(0, index=common_years)

for fuel in df_poland_netzero['fuel_type'].unique():

    # Select the data for the current fuel type
    fuel_data = df_poland_netzero[df_poland_netzero['fuel_type'] == fuel][common_years]
    
    # Plot the stacked area
    ax.fill_between(common_years, bottom, bottom + fuel_data.iloc[0], 
                    label=f'{fuel}', color=colors.get(fuel, 'gray'), alpha=0.7)
    
    # Update the bottom for the next stacked area
    bottom += fuel_data.iloc[0]

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Set y-axis formatter to display values in thousands
ax = plt.gca()

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('MtCO2', fontsize = 15)
plt.title('Poland Net Zero: Annual Emissions from Fossil Fuel Extraction', fontsize=20, pad=60)
plt.text(0.5, 1.05, 'Emissions from current fossil fuel extraction in operation are projected using growth rates \n from NGFS GCAM6 model', transform=ax.transAxes, ha='center', fontsize=12)

ax.legend(loc='upper left', fontsize=12)

plt.show()





# --------------
# 2.3 NET ZERO 1.5C 67% aligned
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the stacked areas for components of df_poland_currentpolicy_cumulative
bottom = pd.Series(0, index=common_years)

for fuel in df_poland_nz15_67['fuel_type'].unique():

    # Select the data for the current fuel type
    fuel_data = df_poland_nz15_67[df_poland_nz15_67['fuel_type'] == fuel][common_years]
    
    # Plot the stacked area
    ax.fill_between(common_years, bottom, bottom + fuel_data.iloc[0], 
                    label=f'{fuel}', color=colors.get(fuel, 'gray'), alpha=0.7)
    
    # Update the bottom for the next stacked area
    bottom += fuel_data.iloc[0]

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Set y-axis formatter to display values in thousands
ax = plt.gca()

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('MtCO2', fontsize = 15)
plt.title('Poland Modified Net Zero: Annual Emissions from Fossil Fuel Extraction', fontsize=20, pad=60)
plt.text(0.5, 1.03, 'Emissions from current fossil fuel extraction in operation are projected using modified growth rates \n from NGFS GCAM6 model to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 67% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)

ax.legend(loc='upper left', fontsize=12)

plt.show()





# --------------
# 2.4 NET ZERO 1.5C 50% aligned
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the stacked areas for components of df_poland_currentpolicy_cumulative
bottom = pd.Series(0, index=common_years)

for fuel in df_poland_nz15_50['fuel_type'].unique():

    # Select the data for the current fuel type
    fuel_data = df_poland_nz15_50[df_poland_nz15_50['fuel_type'] == fuel][common_years]
    
    # Plot the stacked area
    ax.fill_between(common_years, bottom, bottom + fuel_data.iloc[0], 
                    label=f'{fuel}', color=colors.get(fuel, 'gray'), alpha=0.7)
    
    # Update the bottom for the next stacked area
    bottom += fuel_data.iloc[0]

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Set y-axis formatter to display values in thousands
ax = plt.gca()

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('MtCO2', fontsize = 15)
plt.title('Poland Modified Net Zero: Annual Emissions from Fossil Fuel Extraction', fontsize=20, pad=60)
plt.text(0.5, 1.03, 'Emissions from current fossil fuel extraction in operation are projected using modified growth rates \n from NGFS GCAM6 model to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)

ax.legend(loc='upper left', fontsize=12)

plt.show()










# In[8]:


##################################################################################################
##################### AVOIDED GHG & CAPACITY #####################################################
##################################################################################################

# Extract the columns from the DataFrame
years = df_poland_avoided_emissions.columns[1:]  # All columns except 'scenario'


# --------------
### 1 . EMISSIONS

# --------------
# 3.1 Emissions - ANNUAL

# get the valies
values = df_poland_avoided_emissions.iloc[0, 1:]  # The first row, all columns except 'scenario'

# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the line graph
ax.plot(years, values, linestyle='-', color='#52796f')

# Customize the x-axis to show ticks every year
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Add labels and title
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('MtCO2', fontsize = 15)
plt.title('Poland Annual Avoided Emissions: Current Policies vs Net Zero*', fontsize=20, pad=60)
plt.text(0.5, 1.05, 'Net Zero scenario has been adjusted from NGFS GCAM6 model to align global cumulative \n emissions with global carbon budget limiting warming to 1.5°C with 50% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)

# Display the plot
plt.show()





# --------------
# 3.2 Emissions - CUMULATIVE

# get the valies
values = df_poland_avoided_cumulative_emissions.iloc[0, 1:]  # The first row, all columns except 'scenario'

# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the line graph
ax.plot(years, values, linestyle='-', color='#52796f')

# Customize the x-axis to show ticks every year
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Add labels and title
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('MtCO2', fontsize = 15)
plt.title('Poland Cumulative Avoided Emissions: Current Policies vs Net Zero*', fontsize=20, pad=60)
plt.text(0.5, 1.05, 'Net Zero scenario has been adjusted from NGFS GCAM6 model to align global cumulative \n emissions with global carbon budget limiting warming to 1.5°C with 50% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)

# Display the plot
plt.show()










# In[8]:


##################################################################################################
##################### ANNUAL REDUCTIONS ##########################################################
##################################################################################################

# Extract the columns from the DataFrame
years = df_poland_reduction_emissions.columns[1:]  # All columns except 'scenario'

# colors
scenario_colors = ['#415a77', '#48cae4', '#606c38', '#283618']


# --------------
### 1 . EMISSIONS

# --------------
# 4.1 Emissions - ANNUAL

# Create the plot
fig, ax = plt.subplots(figsize=(12, 8))

# Plot each scenario as a separate line
for i, row in df_poland_reduction_emissions.iterrows():
    ax.plot(years, row[1:], label=row['scenario'], color=scenario_colors[i])

# Customize the x-axis to show ticks every year
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Add labels and title
plt.xlabel('Year', fontsize=15)
plt.ylabel('MtCO2', fontsize=15)  # Adjust the label to the correct metric
plt.title('Poland: Year-over-year Emissions Change', fontsize=20, pad=60)
plt.text(0.5, 1.05, 'Net Zero scenario has been adjusted from NGFS GCAM6 model to align global cumulative \n emissions with global carbon budget limiting warming to 1.5°C with 50% & 67% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)

# Add a legend
ax.legend(loc='best', fontsize=12)

# Display the plot
plt.show()





# --------------
# 4.2 Emissions - CUMULATIVE

# Create the plot
fig, ax = plt.subplots(figsize=(12, 8))

# Plot each scenario as a separate line
for i, row in df_poland_reduction_cumulative_emissions.iterrows():
    ax.plot(years, row[1:], label=row['scenario'], color=scenario_colors[i])

# Customize the x-axis to show ticks every year
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Add labels and title
plt.xlabel('Year', fontsize=15)
plt.ylabel('MtCO2', fontsize=15)  # Adjust the label to the correct metric
plt.title('Poland: Cumulative Year-over-year Emissions Change', fontsize=20, pad=60)
plt.text(0.5, 1.05, 'Net Zero scenario has been adjusted from NGFS GCAM6 model to align global cumulative \n emissions with global carbon budget limiting warming to 1.5°C with 50% & 67% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)

# Add a legend
ax.legend(loc='best', fontsize=12)

# Display the plot
plt.show()





##################################################################################################
##################### ANNUAL REDUCTIONS BY FUELS #################################################
##################################################################################################

# --------------
### 1 . coal

# --------------
# 5.1 coal - ANNUAL

# Create the plot
fig, ax = plt.subplots(figsize=(12, 8))

# Plot each scenario as a separate line
for i, row in df_poland_production_diff_coal.iterrows():
    ax.plot(years, row[1:], label=row['scenario'], color=scenario_colors[i])

# Customize the x-axis to show ticks every year
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Add labels and title
plt.xlabel('Year', fontsize=15)
plt.ylabel('Million tons per annum', fontsize=15)  # Adjust the label to the correct metric
plt.title('Poland Coal Extraction: Year-over-year Production Change', fontsize=20, pad=60)
plt.text(0.5, 1.05, 'Net Zero scenario has been adjusted from NGFS GCAM6 model to align global cumulative \n emissions with global carbon budget limiting warming to 1.5°C with 50% & 67% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)

# Add a legend
ax.legend(loc='best', fontsize=12)

# Display the plot
plt.show()





# --------------
# 5.2 coal - CUMULATIVE

# Create the plot
fig, ax = plt.subplots(figsize=(12, 8))

# Plot each scenario as a separate line
for i, row in df_poland_production_diff_cumulative_coal.iterrows():
    ax.plot(years, row[1:], label=row['scenario'], color=scenario_colors[i])

# Customize the x-axis to show ticks every year
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Add labels and title
plt.xlabel('Year', fontsize=15)
plt.ylabel('Million tons per annum', fontsize=15)  # Adjust the label to the correct metric
plt.title('Poland Coal Extraction: Cumulative Year-over-year Production Change', fontsize=20, pad=60)
plt.text(0.5, 1.05, 'Net Zero scenario has been adjusted from NGFS GCAM6 model to align global cumulative \n emissions with global carbon budget limiting warming to 1.5°C with 50% & 67% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)

# Add a legend
ax.legend(loc='best', fontsize=12)

# Display the plot
plt.show()





# --------------
### 2 . gas

# --------------
# 5.3 gas - ANNUAL

# Create the plot
fig, ax = plt.subplots(figsize=(12, 8))

# Plot each scenario as a separate line
for i, row in df_poland_production_diff_gas.iterrows():
    ax.plot(years, row[1:], label=row['scenario'], color=scenario_colors[i])

# Customize the x-axis to show ticks every year
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Add labels and title
plt.xlabel('Year', fontsize=15)
plt.ylabel('Million m³/y', fontsize=15)  # Adjust the label to the correct metric
plt.title('Poland Gas Extraction: Year-over-year Production Change', fontsize=20, pad=60)
plt.text(0.5, 1.05, 'Net Zero scenario has been adjusted from NGFS GCAM6 model to align global cumulative \n emissions with global carbon budget limiting warming to 1.5°C with 50% & 67% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)

# Add a legend
ax.legend(loc='best', fontsize=12)

# Display the plot
plt.show()





# --------------
# 5.4 gas - CUMULATIVE

# Create the plot
fig, ax = plt.subplots(figsize=(12, 8))

# Plot each scenario as a separate line
for i, row in df_poland_production_diff_cumulative_gas.iterrows():
    ax.plot(years, row[1:], label=row['scenario'], color=scenario_colors[i])

# Customize the x-axis to show ticks every year
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Add labels and title
plt.xlabel('Year', fontsize=15)
plt.ylabel('Million m³/y', fontsize=15)  # Adjust the label to the correct metric
plt.title('Poland Gas Extraction: Cumulative Year-over-year Production Change', fontsize=20, pad=60)
plt.text(0.5, 1.05, 'Net Zero scenario has been adjusted from NGFS GCAM6 model to align global cumulative \n emissions with global carbon budget limiting warming to 1.5°C with 50% & 67% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)

# Add a legend
ax.legend(loc='best', fontsize=12)

# Display the plot
plt.show()





# --------------
### 3 . oil

# --------------
# 5.5 oil - ANNUAL

# Create the plot
fig, ax = plt.subplots(figsize=(12, 8))

# Plot each scenario as a separate line
for i, row in df_poland_production_diff_oil.iterrows():
    ax.plot(years, row[1:], label=row['scenario'], color=scenario_colors[i])

# Customize the x-axis to show ticks every year
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Add labels and title
plt.xlabel('Year', fontsize=15)
plt.ylabel('Million bbl/y', fontsize=15)  # Adjust the label to the correct metric
plt.title('Poland Oil Extraction: Year-over-year Production Change', fontsize=20, pad=60)
plt.text(0.5, 1.05, 'Net Zero scenario has been adjusted from NGFS GCAM6 model to align global cumulative \n emissions with global carbon budget limiting warming to 1.5°C with 50% & 67% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)

# Add a legend
ax.legend(loc='best', fontsize=12)

# Display the plot
plt.show()





# --------------
# 5.6 oil - CUMULATIVE

# Create the plot
fig, ax = plt.subplots(figsize=(12, 8))

# Plot each scenario as a separate line
for i, row in df_poland_production_diff_cumulative_oil.iterrows():
    ax.plot(years, row[1:], label=row['scenario'], color=scenario_colors[i])

# Customize the x-axis to show ticks every year
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Add labels and title
plt.xlabel('Year', fontsize=15)
plt.ylabel('Million bbl/y', fontsize=15)  # Adjust the label to the correct metric
plt.title('Poland Oil Extraction: Cumulative Year-over-year Production Change', fontsize=20, pad=60)
plt.text(0.5, 1.05, 'Net Zero scenario has been adjusted from NGFS GCAM6 model to align global cumulative \n emissions with global carbon budget limiting warming to 1.5°C with 50% & 67% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)

# Add a legend
ax.legend(loc='best', fontsize=12)

# Display the plot
plt.show()










##################################################################################################
##################### ANNUAL REDUCTIONS BY FUELS #################################################
##################################################################################################

# --------------
### 1 . coal

# --------------
# 6.1 coal - ANNUAL

# Create the plot
fig, ax = plt.subplots(figsize=(12, 8))

# Plot each scenario as a separate line
for i, row in df_poland_production_coal.iterrows():
    ax.plot(years, row[1:], label=row['scenario'], color=scenario_colors[i])

# Customize the x-axis to show ticks every year
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Add labels and title
plt.xlabel('Year', fontsize=15)
plt.ylabel('Million tons per annum', fontsize=15)  # Adjust the label to the correct metric
plt.title('Poland Coal Extraction: Annual Production Levels', fontsize=20, pad=60)
plt.text(0.5, 1.05, 'Net Zero scenario has been adjusted from NGFS GCAM6 model to align global cumulative \n emissions with global carbon budget limiting warming to 1.5°C with 50% & 67% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)

# Add a legend
ax.legend(loc='best', fontsize=12)

# Display the plot
plt.show()





# --------------
# 6.2 coal - CUMULATIVE

# Create the plot
fig, ax = plt.subplots(figsize=(12, 8))

# Plot each scenario as a separate line
for i, row in df_poland_production_cumulative_coal.iterrows():
    ax.plot(years, row[1:], label=row['scenario'], color=scenario_colors[i])

# Customize the x-axis to show ticks every year
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Add labels and title
plt.xlabel('Year', fontsize=15)
plt.ylabel('Million tons per annum', fontsize=15)  # Adjust the label to the correct metric
plt.title('Poland Coal Extraction: Cumulative Production Levels', fontsize=20, pad=60)
plt.text(0.5, 1.05, 'Net Zero scenario has been adjusted from NGFS GCAM6 model to align global cumulative \n emissions with global carbon budget limiting warming to 1.5°C with 50% & 67% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)

# Add a legend
ax.legend(loc='best', fontsize=12)

# Display the plot
plt.show()





# --------------
### 2 . gas

# --------------
# 5.3 gas - ANNUAL

# Create the plot
fig, ax = plt.subplots(figsize=(12, 8))

# Plot each scenario as a separate line
for i, row in df_poland_production_gas.iterrows():
    ax.plot(years, row[1:], label=row['scenario'], color=scenario_colors[i])

# Customize the x-axis to show ticks every year
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Add labels and title
plt.xlabel('Year', fontsize=15)
plt.ylabel('Million m³/y', fontsize=15)  # Adjust the label to the correct metric
plt.title('Poland Gas Extraction: Annual Production Levels', fontsize=20, pad=60)
plt.text(0.5, 1.05, 'Net Zero scenario has been adjusted from NGFS GCAM6 model to align global cumulative \n emissions with global carbon budget limiting warming to 1.5°C with 50% & 67% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)

# Add a legend
ax.legend(loc='best', fontsize=12)

# Display the plot
plt.show()





# --------------
# 5.4 gas - CUMULATIVE

# Create the plot
fig, ax = plt.subplots(figsize=(12, 8))

# Plot each scenario as a separate line
for i, row in df_poland_production_cumulative_gas.iterrows():
    ax.plot(years, row[1:], label=row['scenario'], color=scenario_colors[i])

# Customize the x-axis to show ticks every year
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Add labels and title
plt.xlabel('Year', fontsize=15)
plt.ylabel('Million m³/y', fontsize=15)  # Adjust the label to the correct metric
plt.title('Poland Gas Extraction: Cumulative Production Levels', fontsize=20, pad=60)
plt.text(0.5, 1.05, 'Net Zero scenario has been adjusted from NGFS GCAM6 model to align global cumulative \n emissions with global carbon budget limiting warming to 1.5°C with 50% & 67% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)

# Add a legend
ax.legend(loc='best', fontsize=12)

# Display the plot
plt.show()





# --------------
### 3 . oil

# --------------
# 5.5 oil - ANNUAL

# Create the plot
fig, ax = plt.subplots(figsize=(12, 8))

# Plot each scenario as a separate line
for i, row in df_poland_production_oil.iterrows():
    ax.plot(years, row[1:], label=row['scenario'], color=scenario_colors[i])

# Customize the x-axis to show ticks every year
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Add labels and title
plt.xlabel('Year', fontsize=15)
plt.ylabel('Million bbl/y', fontsize=15)  # Adjust the label to the correct metric
plt.title('Poland Oil Extraction: Annual Production Levels', fontsize=20, pad=60)
plt.text(0.5, 1.05, 'Net Zero scenario has been adjusted from NGFS GCAM6 model to align global cumulative \n emissions with global carbon budget limiting warming to 1.5°C with 50% & 67% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)

# Add a legend
ax.legend(loc='best', fontsize=12)

# Display the plot
plt.show()





# --------------
# 5.6 oil - CUMULATIVE

# Create the plot
fig, ax = plt.subplots(figsize=(12, 8))

# Plot each scenario as a separate line
for i, row in df_poland_production_cumulative_oil.iterrows():
    ax.plot(years, row[1:], label=row['scenario'], color=scenario_colors[i])

# Customize the x-axis to show ticks every year
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Add labels and title
plt.xlabel('Year', fontsize=15)
plt.ylabel('Million bbl/y', fontsize=15)  # Adjust the label to the correct metric
plt.title('Poland Oil Extraction: Cumulative Production Levels', fontsize=20, pad=60)
plt.text(0.5, 1.05, 'Net Zero scenario has been adjusted from NGFS GCAM6 model to align global cumulative \n emissions with global carbon budget limiting warming to 1.5°C with 50% & 67% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)

# Add a legend
ax.legend(loc='best', fontsize=12)

# Display the plot
plt.show()










# In[]

# export data

# --------------
# current policies
df_poland_currentpolicy.to_excel('2 - output/script 5.2/1.1 - annual emissions - current policy.xlsx', index = False)
df_poland_currentpolicy_cumulative.to_excel('2 - output/script 5.2/1.2 - cumulative emissions - current policy.xlsx', index = False)
df_poland_currentpolicy_diff.to_excel('2 - output/script 5.2/1.3 - annual emissions diff - current policy.xlsx', index = False)


# --------------
# netzero
df_poland_netzero.to_excel('2 - output/script 5.2/2.1 - annual emissions - netzero.xlsx', index = False)
df_poland_netzero_cumulative.to_excel('2 - output/script 5.2/2.2 - cumulative emissions - netzero.xlsx', index = False)
df_poland_netzero_diff.to_excel('2 - output/script 5.2/2.3 - annual emissions diff - netzero.xlsx', index = False)


# --------------
# netzero 1.5C 67% adjusted
df_poland_nz15_67.to_excel('2 - output/script 5.2/3.1 - annual emissions - netzero modified 15C 67%.xlsx', index = False)
df_poland_nz15_67_cumulative.to_excel('2 - output/script 5.2/3.2 - cumulative emissions - netzero modified 15C 67%.xlsx', index = False)
df_poland_nz15_67_diff.to_excel('2 - output/script 5.2/3.3 - annual emissions diff - netzero modified 15C 67%.xlsx', index = False)


# --------------
# netzero 1.5C 50% adjusted
df_poland_nz15_50.to_excel('2 - output/script 5.2/4.1 - annual emissions - netzero modified 15C 50%.xlsx', index = False)
df_poland_nz15_50_cumulative.to_excel('2 - output/script 5.2/4.2 - cumulative emissions - netzero modified 15C 50%.xlsx', index = False)
df_poland_nz15_50_diff.to_excel('2 - output/script 5.2/4.3 - annual emissions diff - netzero modified 15C 50%.xlsx', index = False)


# --------------
# avoided
df_poland_avoided_emissions.to_excel('2 - output/script 5.2/5.1 - avoided emissions - cp vs nz15 50%.xlsx', index = False)
df_poland_avoided_cumulative_emissions.to_excel('2 - output/script 5.2/5.2 - avoided emissions - cp vs nz15 50% - cumulative.xlsx', index = False)


# --------------
# reduction/change YoY
df_poland_reduction_emissions.to_excel('2 - output/script 5.2/6.1 - YoY emissions.xlsx', index = False)
df_poland_reduction_cumulative_emissions.to_excel('2 - output/script 5.2/6.2 - YoY emissions - cumulative.xlsx', index = False)


# --------------
# production by scenario
df_poland_currentpolicy_production.to_excel('2 - output/script 5.2/7.1 - production - current policy.xlsx', index = False)
df_poland_netzero_production.to_excel('2 - output/script 5.2/7.2 - production - netzero.xlsx', index = False)
df_poland_nz15_67_production.to_excel('2 - output/script 5.2/7.3 - production - nz 15 67.xlsx', index = False)
df_poland_nz15_50_production.to_excel('2 - output/script 5.2/7.4 - production - nz 15 50.xlsx', index = False)


# --------------
# production change by scenario
df_poland_currentpolicy_production_diff.to_excel('2 - output/script 5.2/8.1 - production - annual change - current policy.xlsx', index = False)
df_poland_netzero_production_diff.to_excel('2 - output/script 5.2/8.2 - production - annual change - netzero.xlsx', index = False)
df_poland_nz15_67_production_diff.to_excel('2 - output/script 5.2/8.3 - production - annual change - nz 15 67.xlsx', index = False)
df_poland_nz15_50_production_diff.to_excel('2 - output/script 5.2/8.4 - production - annual change - nz 15 50.xlsx', index = False)


# --------------
# production change by scenario
df_poland_production_diff_coal.to_excel('2 - output/script 5.2/9.1 - production - annual change - coal.xlsx', index = False)
df_poland_production_diff_gas.to_excel('2 - output/script 5.2/9.2 - production - annual change - gas.xlsx', index = False)
df_poland_production_diff_oil.to_excel('2 - output/script 5.2/9.3 - production - annual change - oil.xlsx', index = False)

df_poland_production_diff_cumulative_coal.to_excel('2 - output/script 5.2/9.4 - production - annual change - cumulative - coal.xlsx', index = False)
df_poland_production_diff_cumulative_gas.to_excel('2 - output/script 5.2/9.5 - production - annual change - cumulative - gas.xlsx', index = False)
df_poland_production_diff_cumulative_oil.to_excel('2 - output/script 5.2/9.6 - production - annual change - cumulative - oil.xlsx', index = False)

