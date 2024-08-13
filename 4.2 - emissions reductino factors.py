# In[1]:
# Date: Aug 11, 2024
# Project: Identify scale value to be aligned with carbon budget
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
# load emissions data
df_emissions_secondary = pd.read_excel("2 - output/script 3.1/1.1 - Secondary - emissions FA - projection.xlsx")
df_emissions_primary = pd.read_excel("2 - output/script 3.2/1.1 - Primary - emissions FA - projection.xlsx")


# --------------
# load percent change dataset
df_change_secondary = pd.read_excel("2 - output/script 3.1/1.2 - Secondary - emissions FA - change.xlsx")
df_change_primary = pd.read_excel("2 - output/script 3.2/1.2 - Primary - emissions FA - change.xlsx")


# --------------
# load ngfs growth for total energy
df_ngfs_total_annual = pd.read_excel('2 - output/script 2/1.5 - GCAM - emissions - energy.xlsx')
df_ngfs_total_annual= df_ngfs_total_annual.drop(columns = ['2020', '2021', '2022', '2023']) # removing 2020-2023


# --------------
# load ngfs secondary emissions
df_ngfs_secondary = pd.read_excel("2 - output/script 3.1/1.3 - Secondary - emissions NGFS - projection.xlsx")
df_ngfs_primary = pd.read_excel("2 - output/script 3.2/1.3 - Primary - emissions NGFS - projection.xlsx")


# --------------
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
df_ngfs_primary= df_ngfs_primary.drop(columns = drop_columns) # removing 2050-2100

del drop_columns










# In[4]: DIVIDE BY SCENARIOS
############################

# --------------
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


# --------------
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


# --------------
# DO THE SAME TO THE NGFS
# secondary
df_ngfs_secondary_currentpolicy = df_ngfs_secondary[df_ngfs_secondary['Scenario'] == "Current Policies"]
df_ngfs_secondary_currentpolicy.reset_index(drop=True, inplace=True)

df_ngfs_secondary_netzero = df_ngfs_secondary[df_ngfs_secondary['Scenario'] == "Net Zero 2050"]
df_ngfs_secondary_netzero.reset_index(drop=True, inplace=True)

# primary
df_ngfs_primary_currentpolicy = df_ngfs_primary[df_ngfs_primary['Scenario'] == "Current Policies"]
df_ngfs_primary_currentpolicy.reset_index(drop=True, inplace=True)

df_ngfs_primary_netzero = df_ngfs_primary[df_ngfs_primary['Scenario'] == "Net Zero 2050"]
df_ngfs_primary_netzero.reset_index(drop=True, inplace=True)


# --------------
del df_change_primary, df_change_secondary, df_emissions_primary, df_emissions_secondary, df_ngfs_secondary, df_ngfs_primary










# In[4]: GET NGFS TOTAL ENERGY EMISSIONS GROWTH RATES
#####################################################

# --------------
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


# --------------
del df_ngfs_total_annual, df_total_annual










# In[]: GET RESIDUAL EMISSIONS
##############################

# --------------
# current policies --- emissions & percent change
df_residual_currentpolicy = df_total_annual_currentpolicy[year_columns] - df_emissions_secondary_currentpolicy[year_columns].sum() - df_emissions_primary_currentpolicy[year_columns].sum()
df_residual_currentpolicy_change = df_residual_currentpolicy.pct_change(axis = 1) * 100


# --------------
# netzero --- emissions & percent change
df_residual_netzero = df_total_annual_netzero[year_columns] - df_emissions_secondary_netzero[year_columns].sum() - df_emissions_primary_netzero[year_columns].sum()
df_residual_netzero_change = df_residual_netzero.pct_change(axis = 1) * 100










# In[]: GET CUMULATIVE EMISSIONS & ESTABLISH REDUCTION FACTORS

year_columns = [str(year) for year in range(2024, 2051)]


# --------------
# current policy --- # cumulative
df_total_cumulative_currentpolicy = df_total_annual_currentpolicy.copy()
df_total_cumulative_currentpolicy[year_columns] = df_total_cumulative_currentpolicy[year_columns].cumsum(axis=1)

var_total2050_currentpolicy = df_total_cumulative_currentpolicy['2050'].values[0] / 1000
# print(var_total2050_currentpolicy)
# 1062.135498610886

df_ratio_currentpolicy = df_carbon_bugdet.copy()
df_ratio_currentpolicy['Likelyhood 50%'] = var_total2050_currentpolicy/df_ratio_currentpolicy['Likelyhood 50%']
df_ratio_currentpolicy['Likelyhood 67%'] = var_total2050_currentpolicy/df_ratio_currentpolicy['Likelyhood 67%']

# print(df_ratio_currentpolicy)
#   Unnamed: 0  Likelyhood 50%  Likelyhood 67%
# 0      1.5°C        2.966859        4.116804
# 1      1.6°C        2.090818        2.603273
# 2      1.7°C        1.500191        1.903469
# 3      1.8°C        1.237920        1.500191
# 4      1.9°C        0.917215        1.237920
# 5        2°C        0.879251        1.053706




# --------------
# netzero --- # cumulative
df_total_cumulative_netzero = df_total_annual_netzero.copy()
df_total_cumulative_netzero[year_columns] = df_total_cumulative_netzero[year_columns].cumsum(axis=1)

var_total2050_netzero = df_total_cumulative_netzero['2050'].values[0] / 1000
# print(var_total2050_netzero)
# 469.5038277453807

df_ratio_netzero = df_carbon_bugdet.copy()
df_ratio_netzero['Likelyhood 50%'] = var_total2050_netzero/df_ratio_netzero['Likelyhood 50%']
df_ratio_netzero['Likelyhood 67%'] = var_total2050_netzero/df_ratio_netzero['Likelyhood 67%']

# print(df_ratio_netzero)
#   Unnamed: 0  Likelyhood 50%  Likelyhood 67%
# 0      1.5°C        1.311463        1.819782
# 1      1.6°C        0.924220        1.150745
# 2      1.7°C        0.663141        0.841405
# 3      1.8°C        0.547207        0.663141
# 4      1.9°C        0.405444        0.547207
# 5        2°C        0.388662        0.465778










# In[]: FIND NEW GROWTH RATES
#############################

year_columns2 = [str(year) for year in range(2025, 2051)]


# create a reductino factor matric
df_reduction_netzero = df_ratio_netzero.copy()
df_reduction_netzero.iloc[:, [1, 2]] = 1


########################################################
#  1. NET ZERO: 1.5C 50% -------------------------------
########################################################

# --------------
# set total variable
target_value = df_carbon_bugdet['Likelyhood 50%'][0] * 1000
tolerance = 0.01 * target_value # 1% +- buffer zone

# Start with an initial guess --- % over carbon budget
reduction_start = df_ratio_netzero['Likelyhood 50%'][0] - 1

# Set initial bounds for the reduction factor --- it will iterate across all vallues by 0.001 increment --- exhaustive approach
lower_bound = round(reduction_start / 10, 3)
upper_bound = round(reduction_start * 10, 3)
print((upper_bound - lower_bound)/0.001)
# 3084
# this shows how many iterations will run

# Step size for iterating over 3 decimal places
step_size = 0.001

# set iteration variable
iteration = 0


# --------------
# Iterate over the range with the specified step size
for reduction_start in np.arange(lower_bound, upper_bound, step_size):
    iteration += 1

    ### secondary
    # this piece updates annual percent change values by reduction factor
    # if annual change is positive, leave as is
    # if annual change is negative, update, but lowest it can go is -100%
    df_temp_secondary_netzero = df_change_secondary_netzero.copy()
    df_temp_secondary_netzero[year_columns2] = np.where(
        df_change_secondary_netzero[year_columns2] < 0,
        (df_change_secondary_netzero[year_columns2] * reduction_start).clip(lower=-100),
        df_change_secondary_netzero[year_columns2]
    )
    
    
    # save annual changes in a separate dataframe
    df_temp_secondary_netzero_change = df_temp_secondary_netzero.copy()
    
    
    # now compute a new annaul emissions data
    for i in range(1, len(year_columns)):
        previous_year = year_columns[i - 1]
        current_year = year_columns[i]
    
        if current_year in df_temp_secondary_netzero.columns:
            inf_mask = np.isinf(df_temp_secondary_netzero[current_year])
            df_temp_secondary_netzero.loc[~inf_mask, current_year] = df_temp_secondary_netzero[previous_year] * (1 + df_temp_secondary_netzero[current_year] / 100)
            df_temp_secondary_netzero.loc[inf_mask, current_year] = df_ngfs_secondary_netzero.loc[inf_mask, current_year]


    del i, current_year, previous_year, inf_mask


    ### primary
    df_temp_primary_netzero = df_change_primary_netzero.copy()
    df_temp_primary_netzero[year_columns2] = np.where(
        df_change_primary_netzero[year_columns2] < 0,
        (df_change_primary_netzero[year_columns2] * reduction_start).clip(lower=-100),
        df_change_primary_netzero[year_columns2]
    )


    df_temp_primary_netzero_change = df_temp_primary_netzero.copy()


    for i in range(1, len(year_columns)):
        previous_year = year_columns[i - 1]
        current_year = year_columns[i]
    
        if current_year in df_temp_primary_netzero.columns:
            inf_mask = np.isinf(df_temp_primary_netzero[current_year])
            df_temp_primary_netzero.loc[~inf_mask, current_year] = df_temp_primary_netzero[previous_year] * (1 + df_temp_primary_netzero[current_year] / 100)
            df_temp_primary_netzero.loc[inf_mask, current_year] = df_ngfs_primary_netzero.loc[inf_mask, current_year]


    del i, current_year, previous_year, inf_mask



    ### residual 
    df_temp_residual_netzero = df_residual_netzero_change.copy()
    df_temp_residual_netzero[year_columns2] = np.where(
        df_residual_netzero_change[year_columns2] < 0,
        (df_residual_netzero_change[year_columns2] * reduction_start).clip(lower=-100),
        df_residual_netzero_change[year_columns2]
    )


    df_temp_residual_netzero_change = df_temp_residual_netzero.copy()
    df_temp_residual_netzero['2024'] = df_residual_netzero['2024'].values


    for i in range(1, len(year_columns)):
        previous_year = year_columns[i - 1]
        current_year = year_columns[i]
       
        df_temp_residual_netzero[current_year] = df_temp_residual_netzero[previous_year] * (1 + df_temp_residual_netzero[current_year] / 100)


    del i, current_year, previous_year

    

    # get total emissions --- cumulative across all --- secondary, extraction, residual 
    var_temp_total_secondary = df_temp_secondary_netzero[year_columns].sum().sum()
    var_temp_total_primary = df_temp_primary_netzero[year_columns].sum().sum()
    var_temp_total_residiaul = df_temp_residual_netzero[year_columns].sum().sum()
    var_temp_total_all = var_temp_total_primary + var_temp_total_secondary + var_temp_total_residiaul



    # when within tolerance/buffer --- stop
    if abs(var_temp_total_all - target_value) <= tolerance:
        print(f"Converged at reduction_start = {reduction_start} in {iteration} iterations")
        break

else:
    print("No suitable reduction factor found within the bounds.")


# Converged at reduction_start = 1.7990000000000015 in 1769 iterations


# --------------
# add the factor to the dataframe
df_reduction_netzero['Likelyhood 50%'][0] = reduction_start


# --------------
# save the annual changes datasets
df_nz15_50_secondary_change = df_temp_secondary_netzero_change
df_nz15_50_secondary = df_temp_secondary_netzero

df_nz15_50_primary_change = df_temp_primary_netzero_change
df_nz15_50_primary = df_temp_primary_netzero

df_nz15_50_residual_change = df_temp_residual_netzero_change
df_nz15_50_residual = df_temp_residual_netzero


# --------------
del iteration, lower_bound, reduction_start, step_size, target_value, tolerance, upper_bound
del var_temp_total_all, var_temp_total_primary, var_temp_total_secondary, var_temp_total_residiaul










########################################################
#  2. NET ZERO: 1.5C 67% -------------------------------
########################################################

# --------------
# set total variable
target_value = df_carbon_bugdet['Likelyhood 67%'][0] * 1000
tolerance = 0.01 * target_value # 1% +- buffer zone

# Start with an initial guess --- % over carbon budget
reduction_start = df_ratio_netzero['Likelyhood 67%'][0] - 1

# Set initial bounds for the reduction factor --- it will iterate across all vallues by 0.001 increment --- exhaustive approach
lower_bound = round(reduction_start / 10, 3)
upper_bound = round(reduction_start * 10, 3)
print((upper_bound - lower_bound)/0.001)
# 8115
# this shows how many iterations will run

# Step size for iterating over 3 decimal places
step_size = 0.001

# set iteration variable
iteration = 0


# --------------
# Iterate over the range with the specified step size
for reduction_start in np.arange(lower_bound, upper_bound, step_size):
    iteration += 1

    ### secondary
    # this piece updates annual percent change values by reduction factor
    # if annual change is positive, leave as is
    # if annual change is negative, update, but lowest it can go is -100%
    df_temp_secondary_netzero = df_change_secondary_netzero.copy()
    df_temp_secondary_netzero[year_columns2] = np.where(
        df_change_secondary_netzero[year_columns2] < 0,
        (df_change_secondary_netzero[year_columns2] * reduction_start).clip(lower=-100),
        df_change_secondary_netzero[year_columns2]
    )
    
    
    # save annual changes in a separate dataframe
    df_temp_secondary_netzero_change = df_temp_secondary_netzero.copy()
    
    
    # now compute a new annaul emissions data
    for i in range(1, len(year_columns)):
        previous_year = year_columns[i - 1]
        current_year = year_columns[i]
    
        if current_year in df_temp_secondary_netzero.columns:
            inf_mask = np.isinf(df_temp_secondary_netzero[current_year])
            df_temp_secondary_netzero.loc[~inf_mask, current_year] = df_temp_secondary_netzero[previous_year] * (1 + df_temp_secondary_netzero[current_year] / 100)
            df_temp_secondary_netzero.loc[inf_mask, current_year] = df_ngfs_secondary_netzero.loc[inf_mask, current_year]


    del i, current_year, previous_year, inf_mask


    ### primary
    df_temp_primary_netzero = df_change_primary_netzero.copy()
    df_temp_primary_netzero[year_columns2] = np.where(
        df_change_primary_netzero[year_columns2] < 0,
        (df_change_primary_netzero[year_columns2] * reduction_start).clip(lower=-100),
        df_change_primary_netzero[year_columns2]
    )


    df_temp_primary_netzero_change = df_temp_primary_netzero.copy()


    for i in range(1, len(year_columns)):
        previous_year = year_columns[i - 1]
        current_year = year_columns[i]
    
        if current_year in df_temp_primary_netzero.columns:
            inf_mask = np.isinf(df_temp_primary_netzero[current_year])
            df_temp_primary_netzero.loc[~inf_mask, current_year] = df_temp_primary_netzero[previous_year] * (1 + df_temp_primary_netzero[current_year] / 100)
            df_temp_primary_netzero.loc[inf_mask, current_year] = df_ngfs_primary_netzero.loc[inf_mask, current_year]


    del i, current_year, previous_year, inf_mask



    ### residual 
    df_temp_residual_netzero = df_residual_netzero_change.copy()
    df_temp_residual_netzero[year_columns2] = np.where(
        df_residual_netzero_change[year_columns2] < 0,
        (df_residual_netzero_change[year_columns2] * reduction_start).clip(lower=-100),
        df_residual_netzero_change[year_columns2]
    )


    df_temp_residual_netzero_change = df_temp_residual_netzero.copy()
    df_temp_residual_netzero['2024'] = df_residual_netzero['2024'].values


    for i in range(1, len(year_columns)):
        previous_year = year_columns[i - 1]
        current_year = year_columns[i]
       
        df_temp_residual_netzero[current_year] = df_temp_residual_netzero[previous_year] * (1 + df_temp_residual_netzero[current_year] / 100)


    del i, current_year, previous_year

    

    # get total emissions --- cumulative across all --- secondary, extraction, residual 
    var_temp_total_secondary = df_temp_secondary_netzero[year_columns].sum().sum()
    var_temp_total_primary = df_temp_primary_netzero[year_columns].sum().sum()
    var_temp_total_residiaul = df_temp_residual_netzero[year_columns].sum().sum()
    var_temp_total_all = var_temp_total_primary + var_temp_total_secondary + var_temp_total_residiaul



    # when within tolerance/buffer --- stop
    if abs(var_temp_total_all - target_value) <= tolerance:
        print(f"Converged at reduction_start = {reduction_start} in {iteration} iterations")
        break

else:
    print("No suitable reduction factor found within the bounds.")


# Converged at reduction_start = 3.4920000000000027 in 3411 iterations


# --------------
# add the factor to the dataframe
df_reduction_netzero['Likelyhood 67%'][0] = reduction_start


# --------------
# save the annual changes datasets
df_nz15_67_secondary_change = df_temp_secondary_netzero_change
df_nz15_67_secondary = df_temp_secondary_netzero

df_nz15_67_primary_change = df_temp_primary_netzero_change
df_nz15_67_primary = df_temp_primary_netzero

df_nz15_67_residual_change = df_temp_residual_netzero_change
df_nz15_67_residual = df_temp_residual_netzero


# --------------
del iteration, lower_bound, reduction_start, step_size, target_value, tolerance, upper_bound
del var_temp_total_all, var_temp_total_primary, var_temp_total_secondary, var_temp_total_residiaul










########################################################
#  3. NET ZERO: 1.6C 67% -------------------------------
########################################################

# --------------
# set total variable
target_value = df_carbon_bugdet['Likelyhood 67%'][1] * 1000
tolerance = 0.01 * target_value # 1% +- buffer zone

# Start with an initial guess --- % over carbon budget
reduction_start = df_ratio_netzero['Likelyhood 67%'][1] - 1

# Set initial bounds for the reduction factor --- it will iterate across all vallues by 0.001 increment --- exhaustive approach
lower_bound = round(reduction_start / 10, 3)
upper_bound = round(reduction_start * 10, 3)
print((upper_bound - lower_bound)/0.001)
# 1492
# this shows how many iterations will run

# Step size for iterating over 3 decimal places
step_size = 0.001

# set iteration variable
iteration = 0


# --------------
# Iterate over the range with the specified step size
for reduction_start in np.arange(lower_bound, upper_bound, step_size):
    iteration += 1

    ### secondary
    # this piece updates annual percent change values by reduction factor
    # if annual change is positive, leave as is
    # if annual change is negative, update, but lowest it can go is -100%
    df_temp_secondary_netzero = df_change_secondary_netzero.copy()
    df_temp_secondary_netzero[year_columns2] = np.where(
        df_change_secondary_netzero[year_columns2] < 0,
        (df_change_secondary_netzero[year_columns2] * reduction_start).clip(lower=-100),
        df_change_secondary_netzero[year_columns2]
    )
    
    
    # save annual changes in a separate dataframe
    df_temp_secondary_netzero_change = df_temp_secondary_netzero.copy()
    
    
    # now compute a new annaul emissions data
    for i in range(1, len(year_columns)):
        previous_year = year_columns[i - 1]
        current_year = year_columns[i]
    
        if current_year in df_temp_secondary_netzero.columns:
            inf_mask = np.isinf(df_temp_secondary_netzero[current_year])
            df_temp_secondary_netzero.loc[~inf_mask, current_year] = df_temp_secondary_netzero[previous_year] * (1 + df_temp_secondary_netzero[current_year] / 100)
            df_temp_secondary_netzero.loc[inf_mask, current_year] = df_ngfs_secondary_netzero.loc[inf_mask, current_year]


    del i, current_year, previous_year, inf_mask


    ### primary
    df_temp_primary_netzero = df_change_primary_netzero.copy()
    df_temp_primary_netzero[year_columns2] = np.where(
        df_change_primary_netzero[year_columns2] < 0,
        (df_change_primary_netzero[year_columns2] * reduction_start).clip(lower=-100),
        df_change_primary_netzero[year_columns2]
    )


    df_temp_primary_netzero_change = df_temp_primary_netzero.copy()


    for i in range(1, len(year_columns)):
        previous_year = year_columns[i - 1]
        current_year = year_columns[i]
    
        if current_year in df_temp_primary_netzero.columns:
            inf_mask = np.isinf(df_temp_primary_netzero[current_year])
            df_temp_primary_netzero.loc[~inf_mask, current_year] = df_temp_primary_netzero[previous_year] * (1 + df_temp_primary_netzero[current_year] / 100)
            df_temp_primary_netzero.loc[inf_mask, current_year] = df_ngfs_primary_netzero.loc[inf_mask, current_year]


    del i, current_year, previous_year, inf_mask



    ### residual 
    df_temp_residual_netzero = df_residual_netzero_change.copy()
    df_temp_residual_netzero[year_columns2] = np.where(
        df_residual_netzero_change[year_columns2] < 0,
        (df_residual_netzero_change[year_columns2] * reduction_start).clip(lower=-100),
        df_residual_netzero_change[year_columns2]
    )


    df_temp_residual_netzero_change = df_temp_residual_netzero.copy()
    df_temp_residual_netzero['2024'] = df_residual_netzero['2024'].values


    for i in range(1, len(year_columns)):
        previous_year = year_columns[i - 1]
        current_year = year_columns[i]
       
        df_temp_residual_netzero[current_year] = df_temp_residual_netzero[previous_year] * (1 + df_temp_residual_netzero[current_year] / 100)


    del i, current_year, previous_year

    

    # get total emissions --- cumulative across all --- secondary, extraction, residual 
    var_temp_total_secondary = df_temp_secondary_netzero[year_columns].sum().sum()
    var_temp_total_primary = df_temp_primary_netzero[year_columns].sum().sum()
    var_temp_total_residiaul = df_temp_residual_netzero[year_columns].sum().sum()
    var_temp_total_all = var_temp_total_primary + var_temp_total_secondary + var_temp_total_residiaul



    # when within tolerance/buffer --- stop
    if abs(var_temp_total_all - target_value) <= tolerance:
        print(f"Converged at reduction_start = {reduction_start} in {iteration} iterations")
        break

else:
    print("No suitable reduction factor found within the bounds.")


# Converged at reduction_start = 1.3700000000000012 in 1356 iterations


# --------------
# add the factor to the dataframe
df_reduction_netzero['Likelyhood 67%'][1] = reduction_start


# --------------
# save the annual changes datasets
df_nz16_67_secondary_change = df_temp_secondary_netzero_change
df_nz16_67_secondary = df_temp_secondary_netzero

df_nz16_67_primary_change = df_temp_primary_netzero_change
df_nz16_67_primary = df_temp_primary_netzero

df_nz16_67_residual_change = df_temp_residual_netzero_change
df_nz16_67_residual = df_temp_residual_netzero


# --------------
del iteration, lower_bound, reduction_start, step_size, target_value, tolerance, upper_bound
del var_temp_total_all, var_temp_total_primary, var_temp_total_secondary, var_temp_total_residiaul










# In[]
# export data

# --------------
df_reduction_netzero.to_excel('2 - output/script 4.2/1.1 - Net Zero - Reduction factors.xlsx', index=False)


# --------------
# Net zero 1.5C 50%
# emissions
df_nz15_50_secondary.to_excel('2 - output/script 4.2/2.1 - NZ-15-50 - Secondary.xlsx', index=False)
df_nz15_50_primary.to_excel('2 - output/script 4.2/2.2 - NZ-15-50 - Primary.xlsx', index=False)
df_nz15_50_residual.to_excel('2 - output/script 4.2/2.3 - NZ-15-50 - Residual.xlsx', index=False)

# change
df_nz15_50_secondary_change.to_excel('2 - output/script 4.2/2.4 - NZ-15-50 - Secondary - Change.xlsx', index=False)
df_nz15_50_primary_change.to_excel('2 - output/script 4.2/2.5 - NZ-15-50 - Primary - Change.xlsx', index=False)
df_nz15_50_residual_change.to_excel('2 - output/script 4.2/2.6 - NZ-15-50 - Residual - Change.xlsx', index=False)


# --------------
# Net zero 1.5C 67%
# emissions
df_nz15_67_secondary.to_excel('2 - output/script 4.2/3.1 - NZ-15-67 - Secondary.xlsx', index=False)
df_nz15_67_primary.to_excel('2 - output/script 4.2/3.2 - NZ-15-67 - Primary.xlsx', index=False)
df_nz15_67_residual.to_excel('2 - output/script 4.2/3.3 - NZ-15-67 - Residual.xlsx', index=False)

# change
df_nz15_67_secondary_change.to_excel('2 - output/script 4.2/3.4 - NZ-15-67 - Secondary - Change.xlsx', index=False)
df_nz15_67_primary_change.to_excel('2 - output/script 4.2/3.5 - NZ-15-67 - Primary - Change.xlsx', index=False)
df_nz15_67_residual_change.to_excel('2 - output/script 4.2/3.6 - NZ-15-67 - Residual - Change.xlsx', index=False)


# --------------
# Net zero 1.6C 67%
# emissions
df_nz16_67_secondary.to_excel('2 - output/script 4.2/4.1 - NZ-16-67 - Secondary.xlsx', index=False)
df_nz16_67_primary.to_excel('2 - output/script 4.2/4.2 - NZ-16-67 - Primary.xlsx', index=False)
df_nz16_67_residual.to_excel('2 - output/script 4.2/4.3 - NZ-16-67 - Residual.xlsx', index=False)

# change
df_nz16_67_secondary_change.to_excel('2 - output/script 4.2/4.4 - NZ-16-67 - Secondary - Change.xlsx', index=False)
df_nz16_67_primary_change.to_excel('2 - output/script 4.2/4.5 - NZ-16-67 - Primary - Change.xlsx', index=False)
df_nz16_67_residual_change.to_excel('2 - output/script 4.2/4.6 - NZ-16-67 - Residual - Change.xlsx', index=False)







