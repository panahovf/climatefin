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


# keep only NZ15 67% adjustment scenario
del df_nz15_50_secondary_v2, df_nz15_50_secondary_change_v2, df_nz16_67_secondary_v2, df_nz16_67_secondary_change_v2


# remove 'annual change' dataframe
del df_nz15_67_secondary_change_v2










# In[4]: FILTER FOR POLAND
############################

# --------------
# Case 1: Current policy
df_poland_currentpolicy = df_emissions_secondary_currentpolicy[df_emissions_secondary_currentpolicy["Region"] == "POL"]


# --------------
# Case 2: Netzero
df_poland_netzero = df_emissions_secondary_netzero[df_emissions_secondary_netzero["Region"] == "POL"]


# --------------
# Case 3: Netzero 1.6C 67% adjusted
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


# --------------
# total capacity
df_poland_currentpolicy_totalcapacity_diff = df_poland_currentpolicy_totalcapacity.copy()
df_poland_currentpolicy_totalcapacity_diff[common_years] = df_poland_currentpolicy_totalcapacity_diff[common_years].diff(axis=1)

df_poland_netzero_totalcapacity_diff = df_poland_netzero_totalcapacity.copy()
df_poland_netzero_totalcapacity_diff[common_years] = df_poland_netzero_totalcapacity_diff[common_years].diff(axis=1)

df_poland_nz15_67_totalcapacity_diff = df_poland_nz15_67_totalcapacity.copy()
df_poland_nz15_67_totalcapacity_diff[common_years] = df_poland_nz15_67_totalcapacity_diff[common_years].diff(axis=1)


# --------------
# used capacity
df_poland_currentpolicy_usedcapacity_diff = df_poland_currentpolicy_usedcapacity.copy()
df_poland_currentpolicy_usedcapacity_diff[common_years] = df_poland_currentpolicy_usedcapacity_diff[common_years].diff(axis=1)

df_poland_netzero_usedcapacity_diff = df_poland_netzero_usedcapacity.copy()
df_poland_netzero_usedcapacity_diff[common_years] = df_poland_netzero_usedcapacity_diff[common_years].diff(axis=1)

df_poland_nz15_67_usedcapacity_diff = df_poland_nz15_67_usedcapacity.copy()
df_poland_nz15_67_usedcapacity_diff[common_years] = df_poland_nz15_67_usedcapacity_diff[common_years].diff(axis=1)










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

# Set y-axis formatter to display values in thousands
ax = plt.gca()

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('MW', fontsize = 15)
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

# Set y-axis formatter to display values in thousands
ax = plt.gca()

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('MW', fontsize = 15)
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

# Set y-axis formatter to display values in thousands
ax = plt.gca()

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('MW', fontsize = 15)
plt.title('Poland Modified Net Zero: Used Capacity from Power Plants', fontsize=20, pad=60)
plt.text(0.5, 1.03, 'Capacity from current power plants in operation are projected using modified growth rates \n from NGFS GCAM6 model to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 67% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)

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

# Set y-axis formatter to display values in thousands
ax = plt.gca()

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('MW', fontsize = 15)
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

# Set y-axis formatter to display values in thousands
ax = plt.gca()

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('MW', fontsize = 15)
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

# Set y-axis formatter to display values in thousands
ax = plt.gca()

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('MW', fontsize = 15)
plt.title('Poland Modified Net Zero: Total Capacity from Power Plants', fontsize=20, pad=60)
plt.text(0.5, 1.03, 'Capacity from current power plants in operation are projected using modified growth rates \n from NGFS GCAM6 model to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 67% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)

ax.legend(loc='upper left', fontsize=12)

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


