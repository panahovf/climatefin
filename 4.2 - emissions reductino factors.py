# In[1]:
# Date: Aug 11, 2024
# Project: Compary global secondary+primary energy to carbon budgets and get reduction factors
# Author: Farhad Panahov


# Task: Identify scale value to be aligned with carbon budget


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


# load emissions data
df_emissions_secondary = pd.read_excel("2 - output/script 3.1/1.1 - Secondary - emissions FA - projection.xlsx")
df_emissions_primary = pd.read_excel("2 - output/script 3.2/1.1 - Primary - emissions FA - projection.xlsx")


# load percent change dataset
df_change_secondary = pd.read_excel("2 - output/script 3.1/1.2 - Secondary - emissions FA - change.xlsx")
df_change_primary = pd.read_excel("2 - output/script 3.2/1.2 - Primary - emissions FA - change.xlsx")

    
# load ngfs growth for total energy
df_ngfs_total_annual = pd.read_excel('2 - output/script 2/1.5 - GCAM - emissions - energy.xlsx')
df_ngfs_total_annual= df_ngfs_total_annual.drop(columns = ['2020', '2021', '2022', '2023']) # removing 2020-2023


# load ngfs secondary emissions
df_ngfs_secondary = pd.read_excel("2 - output/script 3.1/1.3 - Secondary - emissions NGFS - projection.xlsx")


# carbon budget
df_carbon_bugdet = pd.read_excel('1 - input/updated_carbon_budget_processed - 2024.xlsx')





# In[4]: DROP 2050-2100
############################

# drop 2051-2100
drop_columns = [str(year) for year in range(2051, 2101)]

df_emissions_secondary= df_emissions_secondary.drop(columns = drop_columns) # removing 2050-2100
df_emissions_primary= df_emissions_primary.drop(columns = drop_columns) # removing 2050-2100
df_change_secondary= df_change_secondary.drop(columns = drop_columns) # removing 2050-2100
df_change_primary= df_change_primary.drop(columns = drop_columns) # removing 2050-2100
df_ngfs_total_annual= df_ngfs_total_annual.drop(columns = drop_columns) # removing 2050-2100
df_ngfs_secondary= df_ngfs_secondary.drop(columns = drop_columns) # removing 2050-2100

del drop_columns



# In[4]: DIVIDE BY SCENARIOS
############################

# current policies
#secondary
df_emissions_secondary_currentpolicy = df_emissions_secondary[df_emissions_secondary['Scenario'] == "Current Policies"]
df_emissions_secondary_currentpolicy.reset_index(drop=True, inplace=True)

df_change_secondary_currentpolicy = df_change_secondary[df_change_secondary['Scenario'] == "Current Policies"]
df_change_secondary_currentpolicy.reset_index(drop=True, inplace=True)

# primary
df_emissions_primary_currentpolicy = df_emissions_primary[df_emissions_primary['Scenario'] == "Current Policies"]
df_emissions_primary_currentpolicy.reset_index(drop=True, inplace=True)

df_change_primary_currentpolicy = df_change_primary[df_change_primary['Scenario'] == "Current Policies"]
df_change_primary_currentpolicy.reset_index(drop=True, inplace=True)


# net zero
#secondary
df_emissions_secondary_netzero = df_emissions_secondary[df_emissions_secondary['Scenario'] == "Net Zero 2050"]
df_emissions_secondary_netzero.reset_index(drop=True, inplace=True)

df_change_secondary_netzero = df_change_secondary[df_change_secondary['Scenario'] == "Net Zero 2050"]
df_change_secondary_netzero.reset_index(drop=True, inplace=True)

# primary
df_emissions_primary_netzero = df_emissions_primary[df_emissions_primary['Scenario'] == "Net Zero 2050"]
df_emissions_primary_netzero.reset_index(drop=True, inplace=True)

df_change_primary_netzero = df_change_primary[df_change_primary['Scenario'] == "Net Zero 2050"]
df_change_primary_netzero.reset_index(drop=True, inplace=True)


# DO THE SAME TO THE NGFS SECONDARY only
df_ngfs_secondary_currentpolicy = df_ngfs_secondary[df_ngfs_secondary['Scenario'] == "Current Policies"]
df_ngfs_secondary_currentpolicy.reset_index(drop=True, inplace=True)

df_ngfs_secondary_netzero = df_ngfs_secondary[df_ngfs_secondary['Scenario'] == "Net Zero 2050"]
df_ngfs_secondary_netzero.reset_index(drop=True, inplace=True)



del df_change_primary, df_change_secondary, df_emissions_primary, df_emissions_secondary, df_ngfs_secondary





# In[4]: GET TOTAL EMISSIONS
############################

#-----------------------------
# GET TOTALS FOR ALL SCENARIOS

# select years
year_columns = [str(year) for year in range(2024, 2051)]

# get total NGFS by scenario
df_ngfs_total_annual = df_ngfs_total_annual.groupby('Scenario')[year_columns].sum()

# get % change annually
# Calculate yearly percent change for each row
df_ngfs_annual_change = df_ngfs_total_annual.pct_change(axis=1) * 100
df_total_annual = df_ngfs_annual_change.copy()

# remove 2020-22
# set 2023 energy emissions at 37.4 GT CO2
# https://www.iea.org/reports/co2-emissions-in-2023/executive-summary
df_total_annual['2024'] = 37400 # set





# In[5]: PROJECT THE GROWTH TO ANNUAL EMISSIOSN
###############################################

# after this we get dataframe for secondary energy by source/country/scenario with annual emissions values
for i in range(1, len(year_columns)):
    previous_year = year_columns[i - 1]  # Get the previous year
    current_year = year_columns[i]       # Get the current year
    # Update the current year's values based on the previous year
    df_total_annual[current_year] = df_total_annual[previous_year] * (1 + df_total_annual[current_year] / 100)


del i, current_year, previous_year

df_total_annual.reset_index(inplace=True)


# -------------
# GET SCENARIOS
df_total_annual_currentpolicy = df_total_annual[df_total_annual['Scenario'] == "Current Policies"]
df_total_annual_netzero = df_total_annual[df_total_annual['Scenario'] == "Net Zero 2050"]


del df_ngfs_total_annual, df_total_annual




# In[]: GET RESIDUAL EMISSIONS
##############################

# current policies --- emissions & percent change
df_residual_currentpolicy = df_total_annual_currentpolicy[year_columns] - df_emissions_secondary_currentpolicy[year_columns].sum() - df_emissions_primary_currentpolicy[year_columns].sum()
df_residual_currentpolicy_change = df_residual_currentpolicy.pct_change(axis = 1) * 100


# netzero --- emissions & percent change
df_residual_netzero = df_total_annual_netzero[year_columns] - df_emissions_secondary_netzero[year_columns].sum() - df_emissions_primary_netzero[year_columns].sum()
df_residual_netzero_change = df_residual_netzero.pct_change(axis = 1) * 100






# In[]: GET CUMULATIVE EMISSIONS

year_columns = [str(year) for year in range(2024, 2051)]

##############
# current policy --- # cumulative
df_total_cumulative_currentpolicy = df_total_annual_currentpolicy.copy()
df_total_cumulative_currentpolicy[year_columns] = df_total_cumulative_currentpolicy[year_columns].cumsum(axis=1)

var_total2050_currentpolicy = df_total_cumulative_currentpolicy['2050'].values[0] / 1000

df_reduction_currentpolicy = df_carbon_bugdet.copy()
df_reduction_currentpolicy['Likelyhood 50%'] = var_total2050_currentpolicy/df_reduction_currentpolicy['Likelyhood 50%']
df_reduction_currentpolicy['Likelyhood 67%'] = var_total2050_currentpolicy/df_reduction_currentpolicy['Likelyhood 67%']



# netzero --- # cumulative
df_total_cumulative_netzero = df_total_annual_netzero.copy()
df_total_cumulative_netzero[year_columns] = df_total_cumulative_netzero[year_columns].cumsum(axis=1)

var_total2050_netzero = df_total_cumulative_netzero['2050'].values[0] / 1000

df_reduction_netzero = df_carbon_bugdet.copy()
df_reduction_netzero['Likelyhood 50%'] = var_total2050_netzero/df_reduction_netzero['Likelyhood 50%']
df_reduction_netzero['Likelyhood 67%'] = var_total2050_netzero/df_reduction_netzero['Likelyhood 67%']






# In[]: GET MASTER DATASETS

# current policy
df_master_currentpolicy = pd.concat([df_change_currentpolicy, df_residual_currentpolicy_change], ignore_index=True)
df_master_currentpolicy['Variable'].fillna("Other energy sources", inplace=True)
df_master_currentpolicy.loc[df_master_currentpolicy['Variable'] == "Other energy sources", '2024'] = df_residual_currentpolicy['2024'].values


# net zero
df_master_netzero = pd.concat([df_change_netzero, df_residual_netzero_change], ignore_index=True)
df_master_netzero['Variable'].fillna("Other energy sources", inplace=True)
df_master_netzero.loc[df_master_netzero['Variable'] == "Other energy sources", '2024'] = df_residual_netzero['2024'].values








# In[]: FIND NEW GROWTH RATES

year_columns2 = [str(year) for year in range(2025, 2051)]

#  NET ZERO
reduction_start = df_reduction_netzero['Likelyhood 50%'][0]

# Create a copy of the original DataFrame
df_temp_netzero = df_master_netzero.copy()

# Perform the division on the specified columns
df_temp_netzero[year_columns2] = df_master_netzero[year_columns2] / reduction_start


# GET CUMULATIVE EMISSIONS
# after this we get dataframe for secondary energy by source/country/scenario with annual emissions values
for i in range(1, len(year_columns)):
    previous_year = year_columns[i - 1]  # Get the previous year
    current_year = year_columns[i]       # Get the current year
    
    # Ensure the current year column exists before calculation
    if current_year in df_temp_netzero.columns:
        # Check for 'inf' values in the current year's percentage change column
        inf_mask = np.isinf(df_temp_netzero[current_year])
        
        # Update the current year's values based on the previous year where no 'inf' is present
        df_temp_netzero.loc[~inf_mask, current_year] = df_temp_netzero[previous_year] * (1 + df_temp_netzero[current_year] / 100)
        
        # For rows where 'inf' is present, replace with the corresponding value from df_actual_values
        df_temp_netzero.loc[inf_mask, current_year] = df_ngfs_emissions_secondary.loc[inf_mask, current_year]


del i, current_year, previous_year, inf_mask, year_columns







# In[11]


#####################################################################
#####################################################################
########## PLOTS PLOTS PLOTS PLOTS PLOTS PLOTS PLOTS ################
#####################################################################
#####################################################################



# In[6]:  PREPARE DATASETS
###########################

# Ensure all DataFrames have the same year columns
common_years = df_total_annual_currentpolicy.columns.intersection(df_power_annual_currentpolicy.columns).intersection(df_extraction_annual_currentpolicy.columns).intersection(df_residual_annual_currentpolicy.columns)


# Align all DataFrames to have the same year columns
df_total_annual_currentpolicy = df_total_annual_currentpolicy[common_years]
df_power_annual_currentpolicy = df_power_annual_currentpolicy[common_years]
df_extraction_annual_currentpolicy = df_extraction_annual_currentpolicy[common_years]
df_residual_annual_currentpolicy = df_residual_annual_currentpolicy[common_years]


# Align all DataFrames to have the same year columns
df_total_cumulative_netzero = df_total_cumulative_netzero[common_years]
df_power_cumulative_netzero = df_power_cumulative_netzero[common_years]
df_extraction_cumulative_netzero = df_extraction_cumulative_netzero[common_years]
df_residual_cumulative_netzero = df_residual_cumulative_netzero[common_years]


# Define colors for extraction and power components
extraction_colors = {'Coal': '#991f17', 'Gas': '#b04238', 'Oil': '#c86558'}
power_colors = {'Coal': '#255e7e', 'Gas': '#3d708f', 'Oil': '#6996b3'}


# In[8]:

##################################################################################################
##################### SECTION 1: CURRENT POLICIES ################################################
##################################################################################################


##############
# ANNUAL
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the stacked areas for components of df_extraction_annual_currentpolicy
bottom = pd.Series(0, index=common_years)
for fuel in df_extraction_annual_currentpolicy.index:
    ax.fill_between(common_years, bottom, bottom + df_extraction_annual_currentpolicy.loc[fuel], 
                    label=f'{fuel} (extraction)', color=extraction_colors[fuel], alpha=0.7)
    bottom += df_extraction_annual_currentpolicy.loc[fuel]

# Plot the stacked areas for components of df_power_annual_currentpolicy on top of df_extraction_annual_currentpolicy
for fuel in df_power_annual_currentpolicy.index:
    ax.fill_between(common_years, bottom, bottom + df_power_annual_currentpolicy.loc[fuel], 
                    label=f'{fuel} (power)', color=power_colors[fuel], alpha=0.7)
    bottom += df_power_annual_currentpolicy.loc[fuel]

# Plot the stacked area for df_residual with a dotted texture
ax.fill_between(common_years, bottom, bottom + df_residual_annual_currentpolicy.loc['Current Policies'], 
                label='Other energy sources',color='#a4a2a8', alpha=0.5, hatch='.')

# Plot the line for df_total_annual_currentpolicy
df_total_annual_currentpolicy.loc['Current Policies'].plot(kind='line', ax=ax, 
                                                           color='black', linewidth=2, label='Total energy emissions')

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Formatter function to convert values to thousands
def thousands_formatter(x, pos):
    return f'{int(x/1000)}'    # the values are in Mt, but diving the axis by 1000 to show in Gt

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Adding labels and legend
plt.xlabel('Year', fontsize=15)
plt.ylabel('GtCO2', fontsize=15)
plt.title('Annual Emissions from Energy Sector', fontsize=20, pad=30)
plt.text(0.5, 1.01, 'NGFS GCAM6 model\'s growth rates are applied for projections; Scenario: Current Policies', transform=ax.transAxes, ha='center', fontsize=12)
ax.legend(loc='best', fontsize = 12)

plt.show()





#################
# CUMULATIVE
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the stacked areas for components of df_extraction_annual_currentpolicy
bottom = pd.Series(0, index=common_years)
for fuel in df_extraction_cumulative_currentpolicy.index:
    ax.fill_between(common_years, bottom, bottom + df_extraction_cumulative_currentpolicy.loc[fuel], 
                    label=f'{fuel} (extraction)', color=extraction_colors[fuel], alpha=0.7)
    bottom += df_extraction_cumulative_currentpolicy.loc[fuel]

# Plot the stacked areas for components of df_power_annual_currentpolicy on top of df_extraction_annual_currentpolicy
for fuel in df_power_cumulative_currentpolicy.index:
    ax.fill_between(common_years, bottom, bottom + df_power_cumulative_currentpolicy.loc[fuel], 
                    label=f'{fuel} (power)', color=power_colors[fuel], alpha=0.7)
    bottom += df_power_cumulative_currentpolicy.loc[fuel]

# Plot the stacked area for df_residual with a dotted texture
ax.fill_between(common_years, bottom, bottom + df_residual_cumulative_currentpolicy.loc['Current Policies'], 
                label='Other energy sources', color='#a4a2a8', alpha=0.5, hatch='.')

# Plot the line for df_total_annual_currentpolicy
df_total_cumulative_currentpolicy.loc['Current Policies'].plot(kind='line', ax=ax, 
                                                           color='black', linewidth=2, label='Total energy emissions')

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Formatter function to convert values to thousands
def thousands_formatter(x, pos):
    return f'{int(x/1000)}'    # the values are in Mt, but diving the axis by 1000 to show in Gt

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Add a shaded region between 400 and 580 on the y-axis
plt.axhspan(258000, 358000, color='#aebe8b', alpha=0.5)
plt.text(1.5, 300000, '1.5°C warming', color='black', fontsize=12, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5))

# Add a shaded region between 400 and 580 on the y-axis
plt.axhspan(408000, 508000, color='#e7daaf', alpha=0.3)
plt.text(5, 450000, '1.6°C warming', color='black', fontsize=12, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5))

# Add a shaded region between 400 and 580 on the y-axis
plt.axhspan(558000, 708000, color='#e4b07a', alpha=0.5)
plt.text(10, 625000, 'Carbon budget: 1.7°C warming', color='black', fontsize=12, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5))

# Add a shaded region between 400 and 580 on the y-axis
plt.axhspan(708000, 858000, color='#e57e5c', alpha=0.5)
plt.text(15, 775000, '1.8°C warming', color='black', fontsize=12, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5))

# Add a shaded region between 400 and 580 on the y-axis
plt.axhspan(858000, 1158000, color='#e36258', alpha=0.5)
plt.text(19, 950000, '1.9°C warming', color='black', fontsize=12, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5))

# Add a shaded region between 400 and 580 on the y-axis
plt.axhspan(1008000, 1208000, color='#de425b', alpha=0.5)
plt.text(22, 1200000, '2.0°C warming', color='black', fontsize=12, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5))


# Adding labels and legend
plt.xlabel('Year', fontsize=15)
plt.ylabel('GtCO2', fontsize=15)
plt.title('Cumulative emissions from energy sector', fontsize=20, pad=30)
plt.text(0.5, 1.01, 'NGFS GCAM6 model\'s growth rates are applied for projections; Scenario: Current Policies', transform=ax.transAxes, ha='center', fontsize=12)
ax.legend(loc='upper left', fontsize=15)


plt.show()





# In[]
##################################################################################################
##################### SECTION 2: NET ZERO 2050 ###################################################
##################################################################################################


##############
# ANNUAL
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the stacked areas for components of df_extraction_annual_currentpolicy
bottom = pd.Series(0, index=common_years)
for fuel in df_extraction_annual_netzero.index:
    ax.fill_between(common_years, bottom, bottom + df_extraction_annual_netzero.loc[fuel], 
                    label=f'{fuel} (extraction)', color=extraction_colors[fuel], alpha=0.7)
    bottom += df_extraction_annual_netzero.loc[fuel]

# Plot the stacked areas for components of df_power_annual_currentpolicy on top of df_extraction_annual_currentpolicy
for fuel in df_power_annual_netzero.index:
    ax.fill_between(common_years, bottom, bottom + df_power_annual_netzero.loc[fuel], 
                    label=f'{fuel} (power)', color=power_colors[fuel], alpha=0.7)
    bottom += df_power_annual_netzero.loc[fuel]

# Plot the stacked area for df_residual with a dotted texture
ax.fill_between(common_years, bottom, bottom + df_residual_annual_netzero.loc['Net Zero 2050'], 
                label='Other energy sources',color='#a4a2a8', alpha=0.5, hatch='.')

# Plot the line for df_total_annual_currentpolicy
df_total_annual_netzero.loc['Net Zero 2050'].plot(kind='line', ax=ax, 
                                                           color='black', linewidth=2, label='Total energy emissions')

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Formatter function to convert values to thousands
def thousands_formatter(x, pos):
    return f'{int(x/1000)}'    # the values are in Mt, but diving the axis by 1000 to show in Gt

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Adding labels and legend
plt.xlabel('Year', fontsize=15)
plt.ylabel('GtCO2', fontsize=15)
plt.title('Annual Emissions from Energy Sector', fontsize=20, pad=30)
plt.text(0.5, 1.01, 'NGFS GCAM6 model\'s growth rates are applied for projections; Scenario: Net Zero 2050', transform=ax.transAxes, ha='center', fontsize=12)
ax.legend(loc='best', fontsize = 12)

plt.show()





#################
# CUMULATIVE
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the stacked areas for components of df_extraction_annual_currentpolicy
bottom = pd.Series(0, index=common_years)
for fuel in df_extraction_cumulative_netzero.index:
    ax.fill_between(common_years, bottom, bottom + df_extraction_cumulative_netzero.loc[fuel], 
                    label=f'{fuel} (extraction)', color=extraction_colors[fuel], alpha=0.7)
    bottom += df_extraction_cumulative_netzero.loc[fuel]

# Plot the stacked areas for components of df_power_annual_currentpolicy on top of df_extraction_annual_currentpolicy
for fuel in df_power_cumulative_netzero.index:
    ax.fill_between(common_years, bottom, bottom + df_power_cumulative_netzero.loc[fuel], 
                    label=f'{fuel} (power)', color=power_colors[fuel], alpha=0.7)
    bottom += df_power_cumulative_netzero.loc[fuel]

# Plot the stacked area for df_residual with a dotted texture
ax.fill_between(common_years, bottom, bottom + df_residual_cumulative_netzero.loc['Net Zero 2050'], 
                label='Other energy sources', color='#a4a2a8', alpha=0.5, hatch='.')

# Plot the line for df_total_annual_currentpolicy
df_total_cumulative_netzero.loc['Net Zero 2050'].plot(kind='line', ax=ax, 
                                                           color='black', linewidth=2, label='Total energy emissions')

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Formatter function to convert values to thousands
def thousands_formatter(x, pos):
    return f'{int(x/1000)}'    # the values are in Mt, but diving the axis by 1000 to show in Gt

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Add a shaded region between 400 and 580 on the y-axis
plt.axhspan(258000, 358000, color='#aebe8b', alpha=0.5)
plt.text(1.5, 300000, '1.5°C warming', color='black', fontsize=12, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5))

# Add a shaded region between 400 and 580 on the y-axis
plt.axhspan(408000, 508000, color='#e7daaf', alpha=0.3)
plt.text(5, 450000, '1.6°C warming', color='black', fontsize=12, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5))

# Add a shaded region between 400 and 580 on the y-axis
plt.axhspan(558000, 708000, color='#e4b07a', alpha=0.5)
plt.text(10, 625000, 'Carbon budget: 1.7°C warming', color='black', fontsize=12, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5))

# Add a shaded region between 400 and 580 on the y-axis
plt.axhspan(708000, 858000, color='#e57e5c', alpha=0.5)
plt.text(15, 775000, '1.8°C warming', color='black', fontsize=12, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5))

# Add a shaded region between 400 and 580 on the y-axis
plt.axhspan(858000, 1158000, color='#e36258', alpha=0.5)
plt.text(19, 950000, '1.9°C warming', color='black', fontsize=12, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5))

# Add a shaded region between 400 and 580 on the y-axis
plt.axhspan(1008000, 1208000, color='#de425b', alpha=0.5)
plt.text(22, 1200000, '2.0°C warming', color='black', fontsize=12, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5))


# Adding labels and legend
plt.xlabel('Year', fontsize=15)
plt.ylabel('GtCO2', fontsize=15)
plt.title('Cumulative Emissions from Energy Sector', fontsize=20, pad=30)
plt.text(0.5, 1.01, 'NGFS GCAM6 model\'s growth rates are applied for projections; Scenario: Net Zero 2050', transform=ax.transAxes, ha='center', fontsize=12)
ax.legend(loc='upper left')


plt.show()