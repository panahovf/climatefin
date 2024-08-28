# In[1]:
# Date: Aug 25, 2024
# Project: Plotting emissions results for Poland
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


# --------------
# load data from SCRIPT 4.2
# first set the following function to avoid error --- this is a function within a chart
def thousands_formatter(x, pos):
    return f'{int(x/1000)}' 
# now data is loaded


# --------------
# LOAD POWER DATA
df_power_coal = pd.read_excel('2 - output/script 1/4 - power - coal.xlsx')
df_power_gas = pd.read_excel('2 - output/script 1/5 - power - gas.xlsx')
df_power_oil = pd.read_excel('2 - output/script 1/6 - power - oil.xlsx')










# In[4]: DELETE ALL UNNECESSARY ITEMS
#####################################

# --------------
# remove all variables
del ax, bottom, df_carbon_bugdet, extraction_colors, fig, fuel, power_colors
del var_total2050_currentpolicy, var_total2050_netzero, year_columns, year_columns2


# remove primary related dataframes
del df_change_primary_currentpolicy, df_change_primary_netzero
del df_emissions_primary_currentpolicy, df_emissions_primary_netzero
del df_ngfs_primary_currentpolicy, df_ngfs_primary_netzero


# remove NZ15 50% primary, residual, total, and aggregate secondary
del df_nz15_50_primary_change_v1, df_nz15_50_primary_change_v2, df_nz15_50_primary_v1
del df_nz15_50_primary_v1_annual, df_nz15_50_primary_v1_total
del df_nz15_50_primary_v2, df_nz15_50_primary_v2_total
del df_nz15_50_residual_change_v1, df_nz15_50_residual_change_v2
del df_nz15_50_residual_v1, df_nz15_50_residual_v2, df_nz15_50_residual_v1_total, df_nz15_50_residual_v2_total
del df_nz15_50_secondary_v1_annual, df_nz15_50_secondary_v1_total, df_nz15_50_secondary_v2_total
del df_nz15_50_total_v1, df_nz15_50_total_v1_annual, df_nz15_50_total_v2


# remove NZ15 67% primary, residual, total, and aggregate secondary
del df_nz15_67_primary_change_v1, df_nz15_67_primary_change_v2, df_nz15_67_primary_v1, df_nz15_67_primary_v1_annual, df_nz15_67_primary_v1_total
del df_nz15_67_primary_v2, df_nz15_67_primary_v2_total
del df_nz15_67_residual_change_v1, df_nz15_67_residual_change_v2, df_nz15_67_residual_v1, df_nz15_67_residual_v1_total, df_nz15_67_residual_v2_total, df_nz15_67_residual_v2
del df_nz15_67_secondary_v1_annual, df_nz15_67_secondary_v1_total, df_nz15_67_secondary_v2_total 
del df_nz15_67_total_v1, df_nz15_67_total_v2, df_nz15_67_total_v1_annual 


# remove NZ16 50% primary, residual, total, and aggregate secondary
del df_nz16_67_primary_change_v1, df_nz16_67_primary_change_v2, df_nz16_67_primary_v1,df_nz16_67_primary_v2
del df_nz16_67_primary_v1_annual, df_nz16_67_primary_v1_total, df_nz16_67_primary_v2_total
del df_nz16_67_residual_change_v1, df_nz16_67_residual_change_v2, df_nz16_67_residual_v1, df_nz16_67_residual_v2, df_nz16_67_residual_v1_total, df_nz16_67_residual_v2_total 
del df_nz16_67_secondary_v1_annual, df_nz16_67_secondary_v1_total, df_nz16_67_secondary_v2_total 
del df_nz16_67_total_v1, df_nz16_67_total_v2, df_nz16_67_total_v1_annual 


# remove ratios, and resicuals
del df_ratio_currentpolicy, df_ratio_netzero, df_reduction_netzero_v1, df_reduction_netzero_v2 
del df_residual_currentpolicy, df_residual_currentpolicy_change, df_residual_netzero, df_residual_netzero_change


# remove temporary data frames
del df_temp_primary_netzero, df_temp_primary_netzero_change, df_temp_residual_netzero, df_temp_residual_netzero_change
del df_temp_secondary_netzero, df_temp_secondary_netzero_change


# remove total emissions, changes, and ngfs related data
del df_total_annual_netzero, df_total_annual_currentpolicy, df_total_cumulative_currentpolicy, df_total_cumulative_netzero
del df_change_secondary_currentpolicy, df_change_secondary_netzero
del df_ngfs_annual_change, df_ngfs_secondary_currentpolicy, df_ngfs_secondary_netzero


# keep only VERSION 2 (remove V1)
del df_nz15_50_secondary_change_v1, df_nz15_50_secondary_v1, df_nz15_67_secondary_change_v1, df_nz15_67_secondary_v1, df_nz16_67_secondary_change_v1, df_nz16_67_secondary_v1


# remove NZ 1.6C scenario
del df_nz16_67_secondary_v2, df_nz16_67_secondary_change_v2


# remove 'annual change' dataframe
del df_nz15_67_secondary_change_v2, df_nz15_50_secondary_change_v2










# In[4]: FILTER FOR POLAND
############################

# --------------
# Case 1: Current policy
df_poland_currentpolicy = df_emissions_secondary_currentpolicy[df_emissions_secondary_currentpolicy["Region"] == "POL"]


# --------------
# Case 2: Netzero
df_poland_netzero = df_emissions_secondary_netzero[df_emissions_secondary_netzero["Region"] == "POL"]


# --------------
# Case 3: Netzero 1.5C 50% & 67% adjusted
df_poland_nz15_50 = df_nz15_50_secondary_v2[df_nz15_50_secondary_v2["Region"] == "POL"]
df_poland_nz15_67 = df_nz15_67_secondary_v2[df_nz15_67_secondary_v2["Region"] == "POL"]










# In[4]: GET GHG INTENTITY FACTORS
##################################

# --------------
# get emissions intensity for POLAND
# this function creates a weighted average by countries (emissions by activity)
def weighted_avg_intensity_coal(group):
    return (group['emissions_factor_perMWh'] * group['activity']).sum() / group['activity'].sum()

def weighted_avg_intensity_gas_oil(group):
    return (group['emission_factor'] * group['activity']).sum() / group['activity'].sum()



# apply the function
df_power_coal_intensity = df_power_coal.groupby('countryiso3').apply(weighted_avg_intensity_coal)
df_power_gas_intenstiy = df_power_gas.groupby('countryiso3').apply(weighted_avg_intensity_gas_oil)
df_power_oil_intenstiy = df_power_oil.groupby('countryiso3').apply(weighted_avg_intensity_gas_oil)










# In[4]: GET GHG INTENTITY FACTORS
##################################

# --------------
# get capacity factors for POLAND (utilization factor)
# this function creates a weighted average by countries (emissions by activity)
def weighted_avg_utilization_coal(group):
    return (group['capacity_factor'] * group['activity']).sum() / group['activity'].sum()


# apply the function
df_power_coal_utilization = df_power_coal.groupby('countryiso3').apply(weighted_avg_utilization_coal)
df_power_gas_utilization = df_power_gas.groupby('countryiso3').apply(weighted_avg_utilization_coal)
df_power_oil_utilization = df_power_oil.groupby('countryiso3').apply(weighted_avg_utilization_coal)










# In[4]: CONVERT EMISSIONS TO GENERATION
########################################

# Divide emissions by the intensity factors to get MWh
# GHG / (GHG/MWh) = MWh
# For used capacity: divide total generation by (24x365)
# For total capacity: divide used capacity by the capacity factor (or utilization factor)


# --------------
# get intensity and utilization factor values for poland
intensity_coal = df_power_coal_intensity["POL"]
intensity_gas = df_power_gas_intenstiy["POL"]
intensity_oil = df_power_oil_intenstiy["POL"] # ERRROR NO --- NO OIL IN POLAND

utilization_coal = df_power_coal_utilization["POL"]
utilization_gas = df_power_gas_utilization["POL"]
utilization_oil = df_power_oil_utilization["POL"] # ERRROR NO --- NO OIL IN POLAND


del df_power_coal_intensity, df_power_coal_utilization, df_power_gas_intenstiy, df_power_gas_utilization, df_power_oil_intenstiy, df_power_oil_utilization
del df_power_coal, df_power_gas, df_power_oil





########################################################
#  1. CURRENT POLICY -----------------------------------
########################################################

df_poland_currentpolicy_usedcapacity = df_poland_currentpolicy.copy() # create a new df
df_poland_currentpolicy_totalcapacity = df_poland_currentpolicy.copy() # create a new df


# --------------
# used capacity
# 1 - coal
df_poland_currentpolicy_usedcapacity.loc[df_poland_currentpolicy_usedcapacity['fuel_type'] == "Coal", common_years] = ( 
    df_poland_currentpolicy_usedcapacity.loc[df_poland_currentpolicy_usedcapacity['fuel_type'] == "Coal", common_years]
    .div(intensity_coal)
    .div((24*365))
    )


# 2 - gas
df_poland_currentpolicy_usedcapacity.loc[df_poland_currentpolicy_usedcapacity['fuel_type'] == "Gas", common_years] = ( 
    df_poland_currentpolicy_usedcapacity.loc[df_poland_currentpolicy_usedcapacity['fuel_type'] == "Gas", common_years]
    .div(intensity_gas)
    .div((24*365))
    )


# --------------
# total capacity
# 1 - coal
df_poland_currentpolicy_totalcapacity.loc[df_poland_currentpolicy_totalcapacity['fuel_type'] == "Coal", common_years] = ( 
    df_poland_currentpolicy_totalcapacity.loc[df_poland_currentpolicy_totalcapacity['fuel_type'] == "Coal", common_years]
    .div(intensity_coal)
    .div((24*365))
    .div(utilization_coal)
    )


# 2 - gas
df_poland_currentpolicy_totalcapacity.loc[df_poland_currentpolicy_totalcapacity['fuel_type'] == "Gas", common_years] = ( 
    df_poland_currentpolicy_totalcapacity.loc[df_poland_currentpolicy_totalcapacity['fuel_type'] == "Gas", common_years]
    .div(intensity_gas)
    .div((24*365))
    .div(utilization_gas)
    )





########################################################
#  2. NET ZERO -----------------------------------------
########################################################

df_poland_netzero_usedcapacity = df_poland_netzero.copy() # create a new df
df_poland_netzero_totalcapacity = df_poland_netzero.copy() # create a new df


# --------------
# used capacity
# 1 - coal
df_poland_netzero_usedcapacity.loc[df_poland_netzero_usedcapacity['fuel_type'] == "Coal", common_years] = ( 
    df_poland_netzero_usedcapacity.loc[df_poland_netzero_usedcapacity['fuel_type'] == "Coal", common_years]
    .div(intensity_coal)
    .div((24*365))
    )


# 2 - gas
df_poland_netzero_usedcapacity.loc[df_poland_netzero_usedcapacity['fuel_type'] == "Gas", common_years] = ( 
    df_poland_netzero_usedcapacity.loc[df_poland_netzero_usedcapacity['fuel_type'] == "Gas", common_years]
    .div(intensity_gas)
    .div((24*365))
    )


# --------------
# total capacity
# 1 - coal
df_poland_netzero_totalcapacity.loc[df_poland_netzero_totalcapacity['fuel_type'] == "Coal", common_years] = ( 
    df_poland_netzero_totalcapacity.loc[df_poland_netzero_totalcapacity['fuel_type'] == "Coal", common_years]
    .div(intensity_coal)
    .div((24*365))
    .div(utilization_coal)
    )


# 2 - gas
df_poland_netzero_totalcapacity.loc[df_poland_netzero_totalcapacity['fuel_type'] == "Gas", common_years] = ( 
    df_poland_netzero_totalcapacity.loc[df_poland_netzero_totalcapacity['fuel_type'] == "Gas", common_years]
    .div(intensity_gas)
    .div((24*365))
    .div(utilization_gas)
    )





########################################################
#  3. NET ZERO 1.5C 67% adjusted -----------------------
########################################################

df_poland_nz15_67_usedcapacity = df_poland_nz15_67.copy() # create a new df
df_poland_nz15_67_totalcapacity = df_poland_nz15_67.copy() # create a new df


# --------------
# used capacity
# 1 - coal
df_poland_nz15_67_usedcapacity.loc[df_poland_nz15_67_usedcapacity['fuel_type'] == "Coal", common_years] = ( 
    df_poland_nz15_67_usedcapacity.loc[df_poland_nz15_67_usedcapacity['fuel_type'] == "Coal", common_years]
    .div(intensity_coal)
    .div((24*365))
    )


# 2 - gas
df_poland_nz15_67_usedcapacity.loc[df_poland_nz15_67_usedcapacity['fuel_type'] == "Gas", common_years] = ( 
    df_poland_nz15_67_usedcapacity.loc[df_poland_nz15_67_usedcapacity['fuel_type'] == "Gas", common_years]
    .div(intensity_gas)
    .div((24*365))
    )


# --------------
# total capacity
# 1 - coal
df_poland_nz15_67_totalcapacity.loc[df_poland_nz15_67_totalcapacity['fuel_type'] == "Coal", common_years] = ( 
    df_poland_nz15_67_totalcapacity.loc[df_poland_nz15_67_totalcapacity['fuel_type'] == "Coal", common_years]
    .div(intensity_coal)
    .div((24*365))
    .div(utilization_coal)
    )


# 2 - gas
df_poland_nz15_67_totalcapacity.loc[df_poland_nz15_67_totalcapacity['fuel_type'] == "Gas", common_years] = ( 
    df_poland_nz15_67_totalcapacity.loc[df_poland_nz15_67_totalcapacity['fuel_type'] == "Gas", common_years]
    .div(intensity_gas)
    .div((24*365))
    .div(utilization_gas)
    )





########################################################
#  4. NET ZERO 1.5C 50% adjusted -----------------------
########################################################

df_poland_nz15_50_usedcapacity = df_poland_nz15_50.copy() # create a new df
df_poland_nz15_50_totalcapacity = df_poland_nz15_50.copy() # create a new df


# --------------
# used capacity
# 1 - coal
df_poland_nz15_50_usedcapacity.loc[df_poland_nz15_50_usedcapacity['fuel_type'] == "Coal", common_years] = ( 
    df_poland_nz15_50_usedcapacity.loc[df_poland_nz15_50_usedcapacity['fuel_type'] == "Coal", common_years]
    .div(intensity_coal)
    .div((24*365))
    )


# 2 - gas
df_poland_nz15_50_usedcapacity.loc[df_poland_nz15_50_usedcapacity['fuel_type'] == "Gas", common_years] = ( 
    df_poland_nz15_50_usedcapacity.loc[df_poland_nz15_50_usedcapacity['fuel_type'] == "Gas", common_years]
    .div(intensity_gas)
    .div((24*365))
    )


# --------------
# total capacity
# 1 - coal
df_poland_nz15_50_totalcapacity.loc[df_poland_nz15_50_totalcapacity['fuel_type'] == "Coal", common_years] = ( 
    df_poland_nz15_50_totalcapacity.loc[df_poland_nz15_50_totalcapacity['fuel_type'] == "Coal", common_years]
    .div(intensity_coal)
    .div((24*365))
    .div(utilization_coal)
    )


# 2 - gas
df_poland_nz15_50_totalcapacity.loc[df_poland_nz15_50_totalcapacity['fuel_type'] == "Gas", common_years] = ( 
    df_poland_nz15_50_totalcapacity.loc[df_poland_nz15_50_totalcapacity['fuel_type'] == "Gas", common_years]
    .div(intensity_gas)
    .div((24*365))
    .div(utilization_gas)
    )




# delete extras
del intensity_coal, intensity_gas
del utilization_coal, utilization_gas










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





# --------------
# total capacity
df_poland_currentpolicy_totalcapacity_diff = df_poland_currentpolicy_totalcapacity.copy()
df_poland_currentpolicy_totalcapacity_diff[common_years] = df_poland_currentpolicy_totalcapacity_diff[common_years].diff(axis=1)

df_poland_netzero_totalcapacity_diff = df_poland_netzero_totalcapacity.copy()
df_poland_netzero_totalcapacity_diff[common_years] = df_poland_netzero_totalcapacity_diff[common_years].diff(axis=1)

df_poland_nz15_67_totalcapacity_diff = df_poland_nz15_67_totalcapacity.copy()
df_poland_nz15_67_totalcapacity_diff[common_years] = df_poland_nz15_67_totalcapacity_diff[common_years].diff(axis=1)

df_poland_nz15_50_totalcapacity_diff = df_poland_nz15_50_totalcapacity.copy()
df_poland_nz15_50_totalcapacity_diff[common_years] = df_poland_nz15_50_totalcapacity_diff[common_years].diff(axis=1)


# put these all together
temp_currentpolicy = df_poland_currentpolicy_totalcapacity_diff[common_years].sum(axis=0)
temp_netzero = df_poland_netzero_totalcapacity_diff[common_years].sum(axis=0)
temp_nz15_67 = df_poland_nz15_67_totalcapacity_diff[common_years].sum(axis=0)
temp_nz15_50 = df_poland_nz15_50_totalcapacity_diff[common_years].sum(axis=0)

# create dataframe to host the scenarios
df_poland_reduction_totalcapacity = pd.DataFrame(columns=['scenario'] + common_years.tolist())

# add above scenarios
df_poland_reduction_totalcapacity = pd.concat(
    [df_poland_reduction_totalcapacity, 
     pd.DataFrame(data={'scenario': ['Current Policies'], **temp_currentpolicy.to_dict()}),
     pd.DataFrame(data={'scenario': ['Net Zero'], **temp_netzero.to_dict()}),
     pd.DataFrame(data={'scenario': ['Modified Net Zero: 1.5°C 67% likelyhood'], **temp_nz15_67.to_dict()}),
     pd.DataFrame(data={'scenario': ['Modified Net Zero: 1.5°C 50% likelyhood'], **temp_nz15_50.to_dict()})],
    ignore_index=True
)

# cumulative
df_poland_reduction_cumulative_totalcapacity = df_poland_reduction_totalcapacity.copy()
df_poland_reduction_cumulative_totalcapacity[common_years] = df_poland_reduction_cumulative_totalcapacity[common_years].cumsum(axis=1)





# --------------
# used capacity
df_poland_currentpolicy_usedcapacity_diff = df_poland_currentpolicy_usedcapacity.copy()
df_poland_currentpolicy_usedcapacity_diff[common_years] = df_poland_currentpolicy_usedcapacity_diff[common_years].diff(axis=1)

df_poland_netzero_usedcapacity_diff = df_poland_netzero_usedcapacity.copy()
df_poland_netzero_usedcapacity_diff[common_years] = df_poland_netzero_usedcapacity_diff[common_years].diff(axis=1)

df_poland_nz15_67_usedcapacity_diff = df_poland_nz15_67_usedcapacity.copy()
df_poland_nz15_67_usedcapacity_diff[common_years] = df_poland_nz15_67_usedcapacity_diff[common_years].diff(axis=1)

df_poland_nz15_50_usedcapacity_diff = df_poland_nz15_50_usedcapacity.copy()
df_poland_nz15_50_usedcapacity_diff[common_years] = df_poland_nz15_50_usedcapacity_diff[common_years].diff(axis=1)


# put these all together
temp_currentpolicy = df_poland_currentpolicy_usedcapacity_diff[common_years].sum(axis=0)
temp_netzero = df_poland_netzero_usedcapacity_diff[common_years].sum(axis=0)
temp_nz15_67 = df_poland_nz15_67_usedcapacity_diff[common_years].sum(axis=0)
temp_nz15_50 = df_poland_nz15_50_usedcapacity_diff[common_years].sum(axis=0)

# create dataframe to host the scenarios
df_poland_reduction_usedcapacity = pd.DataFrame(columns=['scenario'] + common_years.tolist())

# add above scenarios
df_poland_reduction_usedcapacity = pd.concat(
    [df_poland_reduction_usedcapacity, 
     pd.DataFrame(data={'scenario': ['Current Policies'], **temp_currentpolicy.to_dict()}),
     pd.DataFrame(data={'scenario': ['Net Zero'], **temp_netzero.to_dict()}),
     pd.DataFrame(data={'scenario': ['Modified Net Zero: 1.5°C 67% likelyhood'], **temp_nz15_67.to_dict()}),
     pd.DataFrame(data={'scenario': ['Modified Net Zero: 1.5°C 50% likelyhood'], **temp_nz15_50.to_dict()})],
    ignore_index=True
)

# cumulative
df_poland_reduction_cumulative_usedcapacity = df_poland_reduction_usedcapacity.copy()
df_poland_reduction_cumulative_usedcapacity[common_years] = df_poland_reduction_cumulative_usedcapacity[common_years].cumsum(axis=1)


# delete extras
del temp_currentpolicy, temp_netzero, temp_nz15_50, temp_nz15_67










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


# --------------
# Used capacity
temp_currentpolicy = df_poland_currentpolicy_usedcapacity[common_years].sum(axis=0)
temp_nz50 = df_poland_nz15_50_usedcapacity[common_years].sum(axis=0)
temp_avoided = temp_currentpolicy - temp_nz50

# create a data frame - annual
df_poland_avoided_usedcapacity = pd.DataFrame(data={'scenario': ['Avoided used capacity'], **temp_avoided.to_dict()})

# cumulative
df_poland_avoided_cumulative_usedcapacity = df_poland_avoided_usedcapacity.copy()
df_poland_avoided_cumulative_usedcapacity[common_years] = df_poland_avoided_cumulative_usedcapacity[common_years].cumsum(axis=1)


# --------------
# Total capacity
temp_currentpolicy = df_poland_currentpolicy_totalcapacity[common_years].sum(axis=0)
temp_nz50 = df_poland_nz15_50_totalcapacity[common_years].sum(axis=0)
temp_avoided = temp_currentpolicy - temp_nz50

# create a data frame - annual
df_poland_avoided_totalcapacity = pd.DataFrame(data={'scenario': ['Avoided total capacity'], **temp_avoided.to_dict()})

# cumulative
df_poland_avoided_cumulative_totalcapacity = df_poland_avoided_totalcapacity.copy()
df_poland_avoided_cumulative_totalcapacity[common_years] = df_poland_avoided_cumulative_totalcapacity[common_years].cumsum(axis=1)


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
power_colors = {'Coal': '#255e7e', 'Gas': '#991f17'}










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
    if fuel == 'Oil':
        continue  # Skip plotting for 'Oil'

    # Select the data for the current fuel type
    fuel_data = df_poland_currentpolicy_cumulative[df_poland_currentpolicy_cumulative['fuel_type'] == fuel][common_years]
    
    # Plot the stacked area
    ax.fill_between(common_years, bottom, bottom + fuel_data.iloc[0], 
                    label=f'{fuel}', color=power_colors.get(fuel, 'gray'), alpha=0.7)
    
    # Update the bottom for the next stacked area
    bottom += fuel_data.iloc[0]

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Set y-axis formatter to display values in thousands
ax = plt.gca()

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('MtCO2', fontsize = 15)
plt.title('Poland Current Policies: Cumulative Emissions from Power Sector', fontsize=20, pad=60)
plt.text(0.5, 1.05, 'Emissions from current power plants in operation are projected using growth rates \n from NGFS GCAM6 model', transform=ax.transAxes, ha='center', fontsize=12)

ax.legend(loc='upper left', fontsize=12)

plt.show()





# --------------
# 1.2 NET ZERO
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the stacked areas for components of df_poland_currentpolicy_cumulative
bottom = pd.Series(0, index=common_years)

for fuel in df_poland_netzero_cumulative['fuel_type'].unique():
    if fuel == 'Oil':
        continue  # Skip plotting for 'Oil'

    # Select the data for the current fuel type
    fuel_data = df_poland_netzero_cumulative[df_poland_netzero_cumulative['fuel_type'] == fuel][common_years]
    
    # Plot the stacked area
    ax.fill_between(common_years, bottom, bottom + fuel_data.iloc[0], 
                    label=f'{fuel}', color=power_colors.get(fuel, 'gray'), alpha=0.7)
    
    # Update the bottom for the next stacked area
    bottom += fuel_data.iloc[0]

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Set y-axis formatter to display values in thousands
ax = plt.gca()

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('MtCO2', fontsize = 15)
plt.title('Poland Net Zero: Cumulative Emissions from Power Sector', fontsize=20, pad=60)
plt.text(0.5, 1.05, 'Emissions from current power plants in operation are projected using growth rates \n from NGFS GCAM6 model', transform=ax.transAxes, ha='center', fontsize=12)

ax.legend(loc='upper left', fontsize=12)

plt.show()





# --------------
# 1.3 NET ZERO 1.5C 67% aligned
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the stacked areas for components of df_poland_currentpolicy_cumulative
bottom = pd.Series(0, index=common_years)

for fuel in df_poland_nz15_67_cumulative['fuel_type'].unique():
    if fuel == 'Oil':
        continue  # Skip plotting for 'Oil'

    # Select the data for the current fuel type
    fuel_data = df_poland_nz15_67_cumulative[df_poland_nz15_67_cumulative['fuel_type'] == fuel][common_years]
    
    # Plot the stacked area
    ax.fill_between(common_years, bottom, bottom + fuel_data.iloc[0], 
                    label=f'{fuel}', color=power_colors.get(fuel, 'gray'), alpha=0.7)
    
    # Update the bottom for the next stacked area
    bottom += fuel_data.iloc[0]

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Set y-axis formatter to display values in thousands
ax = plt.gca()

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('MtCO2', fontsize = 15)
plt.title('Poland Modified Net Zero: Cumulative Emissions from Power Sector', fontsize=20, pad=60)
plt.text(0.5, 1.03, 'Emissions from current power plants in operation are projected using modified growth rates \n from NGFS GCAM6 model to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 67% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)

ax.legend(loc='upper left', fontsize=12)

plt.show()





# --------------
# 1.4 NET ZERO 1.5C 50% aligned
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the stacked areas for components of df_poland_currentpolicy_cumulative
bottom = pd.Series(0, index=common_years)

for fuel in df_poland_nz15_50_cumulative['fuel_type'].unique():
    if fuel == 'Oil':
        continue  # Skip plotting for 'Oil'

    # Select the data for the current fuel type
    fuel_data = df_poland_nz15_50_cumulative[df_poland_nz15_50_cumulative['fuel_type'] == fuel][common_years]
    
    # Plot the stacked area
    ax.fill_between(common_years, bottom, bottom + fuel_data.iloc[0], 
                    label=f'{fuel}', color=power_colors.get(fuel, 'gray'), alpha=0.7)
    
    # Update the bottom for the next stacked area
    bottom += fuel_data.iloc[0]

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Set y-axis formatter to display values in thousands
ax = plt.gca()

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('MtCO2', fontsize = 15)
plt.title('Poland Modified Net Zero: Cumulative Emissions from Power Sector', fontsize=20, pad=60)
plt.text(0.5, 1.03, 'Emissions from current power plants in operation are projected using modified growth rates \n from NGFS GCAM6 model to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)

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
    if fuel == 'Oil':
        continue  # Skip plotting for 'Oil'

    # Select the data for the current fuel type
    fuel_data = df_poland_currentpolicy[df_poland_currentpolicy['fuel_type'] == fuel][common_years]
    
    # Plot the stacked area
    ax.fill_between(common_years, bottom, bottom + fuel_data.iloc[0], 
                    label=f'{fuel}', color=power_colors.get(fuel, 'gray'), alpha=0.7)
    
    # Update the bottom for the next stacked area
    bottom += fuel_data.iloc[0]

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Set y-axis formatter to display values in thousands
ax = plt.gca()

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('MtCO2', fontsize = 15)
plt.title('Poland Current Policies: Annual Emissions from Power Sector', fontsize=20, pad=60)
plt.text(0.5, 1.05, 'Emissions from current power plants in operation are projected using growth rates \n from NGFS GCAM6 model', transform=ax.transAxes, ha='center', fontsize=12)

ax.legend(loc='upper left', fontsize=12)

plt.show()





# --------------
# 2.2 NET ZERO
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the stacked areas for components of df_poland_currentpolicy_cumulative
bottom = pd.Series(0, index=common_years)

for fuel in df_poland_netzero['fuel_type'].unique():
    if fuel == 'Oil':
        continue  # Skip plotting for 'Oil'

    # Select the data for the current fuel type
    fuel_data = df_poland_netzero[df_poland_netzero['fuel_type'] == fuel][common_years]
    
    # Plot the stacked area
    ax.fill_between(common_years, bottom, bottom + fuel_data.iloc[0], 
                    label=f'{fuel}', color=power_colors.get(fuel, 'gray'), alpha=0.7)
    
    # Update the bottom for the next stacked area
    bottom += fuel_data.iloc[0]

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Set y-axis formatter to display values in thousands
ax = plt.gca()

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('MtCO2', fontsize = 15)
plt.title('Poland Net Zero: Annual Emissions from Power Sector', fontsize=20, pad=60)
plt.text(0.5, 1.05, 'Emissions from current power plants in operation are projected using growth rates \n from NGFS GCAM6 model', transform=ax.transAxes, ha='center', fontsize=12)

ax.legend(loc='upper left', fontsize=12)

plt.show()





# --------------
# 2.3 NET ZERO 1.5C 67% aligned
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the stacked areas for components of df_poland_currentpolicy_cumulative
bottom = pd.Series(0, index=common_years)

for fuel in df_poland_nz15_67['fuel_type'].unique():
    if fuel == 'Oil':
        continue  # Skip plotting for 'Oil'

    # Select the data for the current fuel type
    fuel_data = df_poland_nz15_67[df_poland_nz15_67['fuel_type'] == fuel][common_years]
    
    # Plot the stacked area
    ax.fill_between(common_years, bottom, bottom + fuel_data.iloc[0], 
                    label=f'{fuel}', color=power_colors.get(fuel, 'gray'), alpha=0.7)
    
    # Update the bottom for the next stacked area
    bottom += fuel_data.iloc[0]

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Set y-axis formatter to display values in thousands
ax = plt.gca()

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('MtCO2', fontsize = 15)
plt.title('Poland Modified Net Zero: Annual Emissions from Power Sector', fontsize=20, pad=60)
plt.text(0.5, 1.03, 'Emissions from current power plants in operation are projected using modified growth rates \n from NGFS GCAM6 model to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 67% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)

ax.legend(loc='upper left', fontsize=12)

plt.show()





# --------------
# 2.4 NET ZERO 1.5C 50% aligned
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the stacked areas for components of df_poland_currentpolicy_cumulative
bottom = pd.Series(0, index=common_years)

for fuel in df_poland_nz15_50['fuel_type'].unique():
    if fuel == 'Oil':
        continue  # Skip plotting for 'Oil'

    # Select the data for the current fuel type
    fuel_data = df_poland_nz15_50[df_poland_nz15_50['fuel_type'] == fuel][common_years]
    
    # Plot the stacked area
    ax.fill_between(common_years, bottom, bottom + fuel_data.iloc[0], 
                    label=f'{fuel}', color=power_colors.get(fuel, 'gray'), alpha=0.7)
    
    # Update the bottom for the next stacked area
    bottom += fuel_data.iloc[0]

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Set y-axis formatter to display values in thousands
ax = plt.gca()

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('MtCO2', fontsize = 15)
plt.title('Poland Modified Net Zero: Annual Emissions from Power Sector', fontsize=20, pad=60)
plt.text(0.5, 1.03, 'Emissions from current power plants in operation are projected using modified growth rates \n from NGFS GCAM6 model to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)

ax.legend(loc='upper left', fontsize=12)

plt.show()










# In[8]:

##################################################################################################
##################### USED CAPACITY ##############################################################
##################################################################################################


# --------------
# 3.1 CURRENT POLICY
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the stacked areas for components of df_poland_currentpolicy_cumulative
bottom = pd.Series(0, index=common_years)

for fuel in df_poland_currentpolicy_usedcapacity['fuel_type'].unique():
    if fuel == 'Oil':
        continue  # Skip plotting for 'Oil'

    # Select the data for the current fuel type
    fuel_data = df_poland_currentpolicy_usedcapacity[df_poland_currentpolicy_usedcapacity['fuel_type'] == fuel][common_years]
    
    # Plot the stacked area
    ax.fill_between(common_years, bottom, bottom + fuel_data.iloc[0], 
                    label=f'{fuel}', color=power_colors.get(fuel, 'gray'), alpha=0.7)
    
    # Update the bottom for the next stacked area
    bottom += fuel_data.iloc[0]

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Formatter function to convert values to thousands
def thousands_formatter(x, pos):
    return f'{int(x/1000)}'    # the values are in Mt, but diving the axis by 1000 to show in Gt

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('GW', fontsize = 15)
plt.title('Poland Current Policies: Used Capacity from Power Plants', fontsize=20, pad=60)
plt.text(0.5, 1.05, 'Capacity from current power plants in operation are projected using growth rates \n from NGFS GCAM6 model', transform=ax.transAxes, ha='center', fontsize=12)

ax.legend(loc='upper left', fontsize=12)

plt.show()





# --------------
# 3.2 NET ZERO
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the stacked areas for components of df_poland_currentpolicy_cumulative
bottom = pd.Series(0, index=common_years)

for fuel in df_poland_netzero_usedcapacity['fuel_type'].unique():
    if fuel == 'Oil':
        continue  # Skip plotting for 'Oil'

    # Select the data for the current fuel type
    fuel_data = df_poland_netzero_usedcapacity[df_poland_netzero_usedcapacity['fuel_type'] == fuel][common_years]
    
    # Plot the stacked area
    ax.fill_between(common_years, bottom, bottom + fuel_data.iloc[0], 
                    label=f'{fuel}', color=power_colors.get(fuel, 'gray'), alpha=0.7)
    
    # Update the bottom for the next stacked area
    bottom += fuel_data.iloc[0]

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Formatter function to convert values to thousands
def thousands_formatter(x, pos):
    return f'{int(x/1000)}'    # the values are in Mt, but diving the axis by 1000 to show in Gt

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('GW', fontsize = 15)
plt.title('Poland Net Zero: Used Capacity from Power Plants', fontsize=20, pad=60)
plt.text(0.5, 1.05, 'Capacity from current power plants in operation are projected using growth rates \n from NGFS GCAM6 model', transform=ax.transAxes, ha='center', fontsize=12)

ax.legend(loc='upper left', fontsize=12)

plt.show()





# --------------
# 3.3 NET ZERO 1.5C 67%
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the stacked areas for components of df_poland_currentpolicy_cumulative
bottom = pd.Series(0, index=common_years)

for fuel in df_poland_nz15_67_usedcapacity['fuel_type'].unique():
    if fuel == 'Oil':
        continue  # Skip plotting for 'Oil'

    # Select the data for the current fuel type
    fuel_data = df_poland_nz15_67_usedcapacity[df_poland_nz15_67_usedcapacity['fuel_type'] == fuel][common_years]
    
    # Plot the stacked area
    ax.fill_between(common_years, bottom, bottom + fuel_data.iloc[0], 
                    label=f'{fuel}', color=power_colors.get(fuel, 'gray'), alpha=0.7)
    
    # Update the bottom for the next stacked area
    bottom += fuel_data.iloc[0]

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Formatter function to convert values to thousands
def thousands_formatter(x, pos):
    return f'{int(x/1000)}'    # the values are in Mt, but diving the axis by 1000 to show in Gt

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))
# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('GW', fontsize = 15)
plt.title('Poland Modified Net Zero: Used Capacity from Power Plants', fontsize=20, pad=60)
plt.text(0.5, 1.03, 'Capacity from current power plants in operation are projected using modified growth rates \n from NGFS GCAM6 model to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 67% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)

ax.legend(loc='upper left', fontsize=12)

plt.show()





# --------------
# 3.4 NET ZERO 1.5C 50%
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the stacked areas for components of df_poland_currentpolicy_cumulative
bottom = pd.Series(0, index=common_years)

for fuel in df_poland_nz15_50_usedcapacity['fuel_type'].unique():
    if fuel == 'Oil':
        continue  # Skip plotting for 'Oil'

    # Select the data for the current fuel type
    fuel_data = df_poland_nz15_50_usedcapacity[df_poland_nz15_50_usedcapacity['fuel_type'] == fuel][common_years]
    
    # Plot the stacked area
    ax.fill_between(common_years, bottom, bottom + fuel_data.iloc[0], 
                    label=f'{fuel}', color=power_colors.get(fuel, 'gray'), alpha=0.7)
    
    # Update the bottom for the next stacked area
    bottom += fuel_data.iloc[0]

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Formatter function to convert values to thousands
def thousands_formatter(x, pos):
    return f'{int(x/1000)}'    # the values are in Mt, but diving the axis by 1000 to show in Gt

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('GW', fontsize = 15)
plt.title('Poland Modified Net Zero: Used Capacity from Power Plants', fontsize=20, pad=60)
plt.text(0.5, 1.03, 'Capacity from current power plants in operation are projected using modified growth rates \n from NGFS GCAM6 model to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)

ax.legend(loc='upper left', fontsize=12)

plt.show()










# In[8]:

##################################################################################################
##################### TOTAL CAPACITY #############################################################
##################################################################################################


# --------------
# 4.1 CURRENT POLICY
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the stacked areas for components of df_poland_currentpolicy_cumulative
bottom = pd.Series(0, index=common_years)

for fuel in df_poland_currentpolicy_totalcapacity['fuel_type'].unique():
    if fuel == 'Oil':
        continue  # Skip plotting for 'Oil'

    # Select the data for the current fuel type
    fuel_data = df_poland_currentpolicy_totalcapacity[df_poland_currentpolicy_totalcapacity['fuel_type'] == fuel][common_years]
    
    # Plot the stacked area
    ax.fill_between(common_years, bottom, bottom + fuel_data.iloc[0], 
                    label=f'{fuel}', color=power_colors.get(fuel, 'gray'), alpha=0.7)
    
    # Update the bottom for the next stacked area
    bottom += fuel_data.iloc[0]

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Formatter function to convert values to thousands
def thousands_formatter(x, pos):
    return f'{int(x/1000)}'    # the values are in Mt, but diving the axis by 1000 to show in Gt

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('GW', fontsize = 15)
plt.title('Poland Current Policies: Total Capacity from Power Plants', fontsize=20, pad=60)
plt.text(0.5, 1.05, 'Capacity from current power plants in operation are projected using growth rates \n from NGFS GCAM6 model', transform=ax.transAxes, ha='center', fontsize=12)

ax.legend(loc='upper left', fontsize=12)

plt.show()





# --------------
# 4.2 NET ZERO
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the stacked areas for components of df_poland_currentpolicy_cumulative
bottom = pd.Series(0, index=common_years)

for fuel in df_poland_netzero_totalcapacity['fuel_type'].unique():
    if fuel == 'Oil':
        continue  # Skip plotting for 'Oil'

    # Select the data for the current fuel type
    fuel_data = df_poland_netzero_totalcapacity[df_poland_netzero_totalcapacity['fuel_type'] == fuel][common_years]
    
    # Plot the stacked area
    ax.fill_between(common_years, bottom, bottom + fuel_data.iloc[0], 
                    label=f'{fuel}', color=power_colors.get(fuel, 'gray'), alpha=0.7)
    
    # Update the bottom for the next stacked area
    bottom += fuel_data.iloc[0]

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Formatter function to convert values to thousands
def thousands_formatter(x, pos):
    return f'{int(x/1000)}'    # the values are in Mt, but diving the axis by 1000 to show in Gt

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('GW', fontsize = 15)
plt.title('Poland Net Zero: Total Capacity from Power Plants', fontsize=20, pad=60)
plt.text(0.5, 1.05, 'Capacity from current power plants in operation are projected using growth rates \n from NGFS GCAM6 model', transform=ax.transAxes, ha='center', fontsize=12)

ax.legend(loc='upper left', fontsize=12)

plt.show()





# --------------
# 4.3 NET ZERO 1.5C 67%
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the stacked areas for components of df_poland_currentpolicy_cumulative
bottom = pd.Series(0, index=common_years)

for fuel in df_poland_nz15_67_totalcapacity['fuel_type'].unique():
    if fuel == 'Oil':
        continue  # Skip plotting for 'Oil'

    # Select the data for the current fuel type
    fuel_data = df_poland_nz15_67_totalcapacity[df_poland_nz15_67_totalcapacity['fuel_type'] == fuel][common_years]
    
    # Plot the stacked area
    ax.fill_between(common_years, bottom, bottom + fuel_data.iloc[0], 
                    label=f'{fuel}', color=power_colors.get(fuel, 'gray'), alpha=0.7)
    
    # Update the bottom for the next stacked area
    bottom += fuel_data.iloc[0]

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Formatter function to convert values to thousands
def thousands_formatter(x, pos):
    return f'{int(x/1000)}'    # the values are in Mt, but diving the axis by 1000 to show in Gt

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('GW', fontsize = 15)
plt.title('Poland Modified Net Zero: Total Capacity from Power Plants', fontsize=20, pad=60)
plt.text(0.5, 1.03, 'Capacity from current power plants in operation are projected using modified growth rates \n from NGFS GCAM6 model to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 67% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)

ax.legend(loc='upper left', fontsize=12)

plt.show()





# --------------
# 4.4 NET ZERO 1.5C 50%
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the stacked areas for components of df_poland_currentpolicy_cumulative
bottom = pd.Series(0, index=common_years)

for fuel in df_poland_nz15_50_totalcapacity['fuel_type'].unique():
    if fuel == 'Oil':
        continue  # Skip plotting for 'Oil'

    # Select the data for the current fuel type
    fuel_data = df_poland_nz15_50_totalcapacity[df_poland_nz15_50_totalcapacity['fuel_type'] == fuel][common_years]
    
    # Plot the stacked area
    ax.fill_between(common_years, bottom, bottom + fuel_data.iloc[0], 
                    label=f'{fuel}', color=power_colors.get(fuel, 'gray'), alpha=0.7)
    
    # Update the bottom for the next stacked area
    bottom += fuel_data.iloc[0]

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Formatter function to convert values to thousands
def thousands_formatter(x, pos):
    return f'{int(x/1000)}'    # the values are in Mt, but diving the axis by 1000 to show in Gt

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('GW', fontsize = 15)
plt.title('Poland Modified Net Zero: Total Capacity from Power Plants', fontsize=20, pad=60)
plt.text(0.5, 1.03, 'Capacity from current power plants in operation are projected using modified growth rates \n from NGFS GCAM6 model to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)

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
# 5.1 Emissions - ANNUAL

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
# 5.2 Emissions - CUMULATIVE

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









# --------------
### 2 . USED CAPACITY

# --------------
# 6.1 Used Capacity - ANNUAL

# get the valies
values = df_poland_avoided_usedcapacity.iloc[0, 1:]  # The first row, all columns except 'scenario'

# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the line graph
ax.plot(years, values, linestyle='-', color='#52796f')

# Customize the x-axis to show ticks every year
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Formatter function to convert values to thousands
def thousands_formatter(x, pos):
    return f'{int(x/1000)}'    # the values are in Mt, but diving the axis by 1000 to show in Gt

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Add labels and title
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('GW', fontsize = 15)
plt.title('Poland Annual Avoided Used Capacity: Current Policies vs Net Zero*', fontsize=20, pad=60)
plt.text(0.5, 1.05, 'Net Zero scenario has been adjusted from NGFS GCAM6 model to align global cumulative \n emissions with global carbon budget limiting warming to 1.5°C with 50% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)

# Display the plot
plt.show()





# --------------
# 6.2 Used Capacity - CUMULATIVE

# get the valies
values = df_poland_avoided_cumulative_usedcapacity.iloc[0, 1:]  # The first row, all columns except 'scenario'

# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the line graph
ax.plot(years, values, linestyle='-', color='#52796f')

# Customize the x-axis to show ticks every year
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Formatter function to convert values to thousands
def thousands_formatter(x, pos):
    return f'{int(x/1000)}'    # the values are in Mt, but diving the axis by 1000 to show in Gt

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Add labels and title
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('GW', fontsize = 15)
plt.title('Poland Cumulative Avoided Used Capacity: Current Policies vs Net Zero*', fontsize=20, pad=60)
plt.text(0.5, 1.05, 'Net Zero scenario has been adjusted from NGFS GCAM6 model to align global cumulative \n emissions with global carbon budget limiting warming to 1.5°C with 50% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)

# Display the plot
plt.show()










# --------------
### 3 . TOTAL CAPACITY

# --------------
# 7.1 Total Capacity - ANNUAL

# get the valies
values = df_poland_avoided_totalcapacity.iloc[0, 1:]  # The first row, all columns except 'scenario'

# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the line graph
ax.plot(years, values, linestyle='-', color='#52796f')

# Customize the x-axis to show ticks every year
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Formatter function to convert values to thousands
def thousands_formatter(x, pos):
    return f'{int(x/1000)}'    # the values are in Mt, but diving the axis by 1000 to show in Gt

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Add labels and title
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('GW', fontsize = 15)
plt.title('Poland Annual Avoided Total Capacity: Current Policies vs Net Zero*', fontsize=20, pad=60)
plt.text(0.5, 1.05, 'Net Zero scenario has been adjusted from NGFS GCAM6 model to align global cumulative \n emissions with global carbon budget limiting warming to 1.5°C with 50% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)

# Display the plot
plt.show()





# --------------
# 7.2 Total Capacity - CUMULATIVE

# get the valies
values = df_poland_avoided_cumulative_totalcapacity.iloc[0, 1:]  # The first row, all columns except 'scenario'

# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the line graph
ax.plot(years, values, linestyle='-', color='#52796f')

# Customize the x-axis to show ticks every year
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Formatter function to convert values to thousands
def thousands_formatter(x, pos):
    return f'{int(x/1000)}'    # the values are in Mt, but diving the axis by 1000 to show in Gt

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Add labels and title
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('GW', fontsize = 15)
plt.title('Poland Cumulative Avoided Total Capacity: Current Policies vs Net Zero*', fontsize=20, pad=60)
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
# 8.1 Emissions - ANNUAL

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
# 8.2 Emissions - CUMULATIVE

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









# --------------
### 2 . USED CAPACITY

# --------------
# 8.3 Used Capacity - ANNUAL

# Create the plot
fig, ax = plt.subplots(figsize=(12, 8))

# Plot each scenario as a separate line
for i, row in df_poland_reduction_usedcapacity.iterrows():
    ax.plot(years, row[1:], label=row['scenario'], color=scenario_colors[i])

# Customize the x-axis to show ticks every year
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Formatter function to convert values to thousands
def thousands_formatter(x, pos):
    return f'{int(x/1000)}'    # the values are in Mt, but diving the axis by 1000 to show in Gt

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Add labels and title
plt.xlabel('Year', fontsize=15)
plt.ylabel('GW', fontsize=15)  # Adjust the label to the correct metric
plt.title('Poland: Year-over-year Used Capacity Change', fontsize=20, pad=60)
plt.text(0.5, 1.05, 'Net Zero scenario has been adjusted from NGFS GCAM6 model to align global cumulative \n emissions with global carbon budget limiting warming to 1.5°C with 50% & 67% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)

# Add a legend
ax.legend(loc='best', fontsize=12)

# Display the plot
plt.show()





# --------------
# 8.4 Used capacity - CUMULATIVE

# Create the plot
fig, ax = plt.subplots(figsize=(12, 8))

# Plot each scenario as a separate line
for i, row in df_poland_reduction_cumulative_usedcapacity.iterrows():
    ax.plot(years, row[1:], label=row['scenario'], color=scenario_colors[i])

# Customize the x-axis to show ticks every year
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Formatter function to convert values to thousands
def thousands_formatter(x, pos):
    return f'{int(x/1000)}'    # the values are in Mt, but diving the axis by 1000 to show in Gt

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Add labels and title
plt.xlabel('Year', fontsize=15)
plt.ylabel('GW', fontsize=15)  # Adjust the label to the correct metric
plt.title('Poland: Cumulative Year-over-year Used Capacity Change', fontsize=20, pad=60)
plt.text(0.5, 1.05, 'Net Zero scenario has been adjusted from NGFS GCAM6 model to align global cumulative \n emissions with global carbon budget limiting warming to 1.5°C with 50% & 67% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)

# Add a legend
ax.legend(loc='best', fontsize=12)

# Display the plot
plt.show()










# --------------
### 3 . TOTAL CAPACITY

# --------------
# 8.5 Total Capacity - ANNUAL

# Create the plot
fig, ax = plt.subplots(figsize=(12, 8))

# Plot each scenario as a separate line
for i, row in df_poland_reduction_totalcapacity.iterrows():
    ax.plot(years, row[1:], label=row['scenario'], color=scenario_colors[i])

# Customize the x-axis to show ticks every year
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Formatter function to convert values to thousands
def thousands_formatter(x, pos):
    return f'{int(x/1000)}'    # the values are in Mt, but diving the axis by 1000 to show in Gt

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Add labels and title
plt.xlabel('Year', fontsize=15)
plt.ylabel('GW', fontsize=15)  # Adjust the label to the correct metric
plt.title('Poland: Year-over-year Total Capacity Change', fontsize=20, pad=60)
plt.text(0.5, 1.05, 'Net Zero scenario has been adjusted from NGFS GCAM6 model to align global cumulative \n emissions with global carbon budget limiting warming to 1.5°C with 50% & 67% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)

# Add a legend
ax.legend(loc='best', fontsize=12)

# Display the plot
plt.show()





# --------------
# 8.6 total capacity - CUMULATIVE

# Create the plot
fig, ax = plt.subplots(figsize=(12, 8))

# Plot each scenario as a separate line
for i, row in df_poland_reduction_cumulative_totalcapacity.iterrows():
    ax.plot(years, row[1:], label=row['scenario'], color=scenario_colors[i])

# Customize the x-axis to show ticks every year
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Formatter function to convert values to thousands
def thousands_formatter(x, pos):
    return f'{int(x/1000)}'    # the values are in Mt, but diving the axis by 1000 to show in Gt

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Add labels and title
plt.xlabel('Year', fontsize=15)
plt.ylabel('GW', fontsize=15)  # Adjust the label to the correct metric
plt.title('Poland: Cumulative Year-over-year Total Capacity Change', fontsize=20, pad=60)
plt.text(0.5, 1.05, 'Net Zero scenario has been adjusted from NGFS GCAM6 model to align global cumulative \n emissions with global carbon budget limiting warming to 1.5°C with 50% & 67% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)

# Add a legend
ax.legend(loc='best', fontsize=12)

# Display the plot
plt.show()











# In[]

# export data

# --------------
# current policies
df_poland_currentpolicy.to_excel('2 - output/script 5/1.1 - annual emissions - current policy.xlsx', index = False)
df_poland_currentpolicy_cumulative.to_excel('2 - output/script 5/1.2 - cumulative emissions - current policy.xlsx', index = False)
df_poland_currentpolicy_totalcapacity.to_excel('2 - output/script 5/1.3 - total capacity - current policy.xlsx', index = False)
df_poland_currentpolicy_usedcapacity.to_excel('2 - output/script 5/1.4 - used capacity - current policy.xlsx', index = False)
df_poland_currentpolicy_diff.to_excel('2 - output/script 5/1.5 - annual emissions diff - current policy.xlsx', index = False)
df_poland_currentpolicy_totalcapacity_diff.to_excel('2 - output/script 5/1.6 - total capacity diff - current policy.xlsx', index = False)
df_poland_currentpolicy_usedcapacity_diff.to_excel('2 - output/script 5/1.7 - used capacity diff - current policy.xlsx', index = False)


# --------------
# netzero
df_poland_netzero.to_excel('2 - output/script 5/2.1 - annual emissions - netzero.xlsx', index = False)
df_poland_netzero_cumulative.to_excel('2 - output/script 5/2.2 - cumulative emissions - netzero.xlsx', index = False)
df_poland_netzero_totalcapacity.to_excel('2 - output/script 5/2.3 - total capacity - netzero.xlsx', index = False)
df_poland_netzero_usedcapacity.to_excel('2 - output/script 5/2.4 - used capacity - netzero.xlsx', index = False)
df_poland_netzero_diff.to_excel('2 - output/script 5/2.5 - annual emissions diff - netzero.xlsx', index = False)
df_poland_netzero_totalcapacity_diff.to_excel('2 - output/script 5/2.6 - total capacity diff - netzero.xlsx', index = False)
df_poland_netzero_usedcapacity_diff.to_excel('2 - output/script 5/2.7 - used capacity diff - netzero.xlsx', index = False)


# --------------
# netzero 1.5C 67% adjusted
df_poland_nz15_67.to_excel('2 - output/script 5/3.1 - annual emissions - netzero modified 15C 67%.xlsx', index = False)
df_poland_nz15_67_cumulative.to_excel('2 - output/script 5/3.2 - cumulative emissions - netzero modified 15C 67%.xlsx', index = False)
df_poland_nz15_67_totalcapacity.to_excel('2 - output/script 5/3.3 - total capacity - netzero modified 15C 67%.xlsx', index = False)
df_poland_nz15_67_usedcapacity.to_excel('2 - output/script 5/3.4 - used capacity - netzero modified 15C 67%.xlsx', index = False)
df_poland_nz15_67_diff.to_excel('2 - output/script 5/3.5 - annual emissions diff - netzero modified 15C 67%.xlsx', index = False)
df_poland_nz15_67_totalcapacity_diff.to_excel('2 - output/script 5/3.6 - total capacity diff - netzero modified 15C 67%.xlsx', index = False)
df_poland_nz15_67_usedcapacity_diff.to_excel('2 - output/script 5/3.7 - used capacity diff - netzero modified 15C 67%.xlsx', index = False)


# --------------
# netzero 1.5C 50% adjusted
df_poland_nz15_50.to_excel('2 - output/script 5/4.1 - annual emissions - netzero modified 15C 50%.xlsx', index = False)
df_poland_nz15_50_cumulative.to_excel('2 - output/script 5/4.2 - cumulative emissions - netzero modified 15C 50%.xlsx', index = False)
df_poland_nz15_50_totalcapacity.to_excel('2 - output/script 5/4.3 - total capacity - netzero modified 15C 50%.xlsx', index = False)
df_poland_nz15_50_usedcapacity.to_excel('2 - output/script 5/4.4 - used capacity - netzero modified 15C 50%.xlsx', index = False)
df_poland_nz15_50_diff.to_excel('2 - output/script 5/4.5 - annual emissions diff - netzero modified 15C 50%.xlsx', index = False)
df_poland_nz15_50_totalcapacity_diff.to_excel('2 - output/script 5/4.6 - total capacity diff - netzero modified 15C 50%.xlsx', index = False)
df_poland_nz15_50_usedcapacity_diff.to_excel('2 - output/script 5/4.7 - used capacity diff - netzero modified 15C 50%.xlsx', index = False)


# --------------
# avoided
df_poland_avoided_emissions.to_excel('2 - output/script 5/5.1 - avoided emissions - cp vs nz15 50%.xlsx', index = False)
df_poland_avoided_totalcapacity.to_excel('2 - output/script 5/5.2 - avoided total capacity - cp vs nz15 50%.xlsx', index = False)
df_poland_avoided_usedcapacity.to_excel('2 - output/script 5/5.3 - avoided used capacity - cp vs nz15 50%.xlsx', index = False)

df_poland_avoided_cumulative_emissions.to_excel('2 - output/script 5/5.4 - avoided emissions - cp vs nz15 50% - cumulative.xlsx', index = False)
df_poland_avoided_cumulative_totalcapacity.to_excel('2 - output/script 5/5.5 - avoided total capacity - cp vs nz15 50% - cumulative.xlsx', index = False)
df_poland_avoided_cumulative_usedcapacity.to_excel('2 - output/script 5/5.6 - avoided used capacity - cp vs nz15 50% - cumulative.xlsx', index = False)


# --------------
# reduction/change YoY
df_poland_reduction_emissions.to_excel('2 - output/script 5/6.1 - YoY emissions.xlsx', index = False)
df_poland_reduction_totalcapacity.to_excel('2 - output/script 5/6.2 - YoY total capacity.xlsx', index = False)
df_poland_reduction_usedcapacity.to_excel('2 - output/script 5/6.3 - YoY used capacity.xlsx', index = False)

df_poland_reduction_cumulative_emissions.to_excel('2 - output/script 5/6.4 - YoY emissions - cumulative.xlsx', index = False)
df_poland_reduction_cumulative_totalcapacity.to_excel('2 - output/script 5/6.5 - YoY total capacity - cumulative.xlsx', index = False)
df_poland_reduction_cumulative_usedcapacity.to_excel('2 - output/script 5/6.6 - YoY used capacity - cumulative.xlsx', index = False)










