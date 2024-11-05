# In[1]:
# Date: Oct 31, 2024
# Project: Incorporating AI growth to NGFS scenarios
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
# NGFS GCAM 6
df_gcam = pd.read_excel('1 - input/Downscaled_GCAM 6.0 NGFS_data.xlsx')    


# ---------------------------- 
# FORWARD ANALYTICS DATA
df_fa_power = pd.read_csv("1 - input/v3_power_Forward_Analytics2024.csv")
df_fa_power = df_fa_power[df_fa_power['status'] == "operating"] # filter right away for operating plants only









# In[5]: SET YEAR COLUMNS
########################################################
years_2020 = [str(year) for year in range(2020, 2051)]
years_2022 = [str(year) for year in range(2022, 2051)]
years_2024 = [str(year) for year in range(2024, 2051)]










# In[5]: FILTER GCAM DATA + MAKE EXTRA EDITS + CREATIONS
########################################################

# ---------------------
# filter to only keep electricity (secondary energy) by source
df_gcam_filtered = df_gcam.loc[(df_gcam['Variable'] == 'Secondary Energy|Electricity|Biomass')| 
                               (df_gcam['Variable'] == 'Secondary Energy|Electricity|Coal')| (df_gcam['Variable'] == 'Secondary Energy|Electricity|Gas')| 
                               (df_gcam['Variable'] == 'Secondary Energy|Electricity|Hydro')|(df_gcam['Variable'] == 'Secondary Energy|Electricity|Oil') |
                               (df_gcam['Variable'] == 'Secondary Energy|Electricity|Solar')|(df_gcam['Variable'] == 'Secondary Energy|Electricity|Wind') | 
                               (df_gcam['Variable'] == 'Secondary Energy|Electricity|Geothermal')|(df_gcam['Variable'] == 'Secondary Energy|Electricity|Nuclear')]


# ---------------------
# extrapolate values
df_gcam_filtered[years_2020] = df_gcam_filtered[years_2020].interpolate(method='linear', axis=1)


# ---------------------
# filter gcam years
metadata_columns = ['Model', 'Scenario', 'Region', 'Variable', 'Unit']
df_gcam_filtered = df_gcam_filtered[metadata_columns + years_2020]


# delete
del metadata_columns



# ---------------------
# remove extra regions
df_gcam_filtered = df_gcam_filtered[~df_gcam_filtered['Region'].isin(['EU27', 'World'])]

# reset index
df_gcam_filtered = df_gcam_filtered.reset_index(drop=True)



# ---------------------
# get total electricity disctribution share by country
df_electricity_cp = df_gcam_filtered[(df_gcam_filtered['Variable'] != "Secondary Energy|Electricity") &
                                  (df_gcam_filtered['Scenario'] == "Current Policies")]

# conver EJ to TWh by multiplying to 277.777778
# https://www.convertunits.com/from/exajoule/to/terawatt+hours
df_electricity_cp[years_2020] = df_electricity_cp[years_2020] * 277.777778
df_electricity_cp['Unit'] = "TWh"

# reset index
df_electricity_cp = df_electricity_cp.reset_index(drop=True)


# create global trends
df_electricity_cp_global = df_electricity_cp.groupby('Variable')[years_2020].sum().reset_index()



# ---------------------
# get shares
df_electricity_cp_share = df_electricity_cp.copy()
df_electricity_cp_share[years_2020] =  df_electricity_cp_share[years_2020] / df_electricity_cp[years_2020].sum()
df_electricity_cp_share['Unit'] = "Share of global"










# In[5]: Create AI demand dataframe
####################################

# ---------------------
# create AI electricity demand data frame
df_ai = pd.DataFrame(columns=['case'] + years_2022)


# ---------------------
# get values: https://iea.blob.core.windows.net/assets/18f3ed24-4b26-4c83-a3d2-8a1be51c8cc8/Electricity2024-Analysisandforecastto2026.pdf
# artificial intelligence to range between 620-1 050 TWh in 2026, with our base case for demand at just over 800 TWh – up from 460 TWh in 2022.
data = {
    'case': ['high', 'low', 'base'],
    '2022': [460, 460, 460],
    '2026': [1050, 620, 800]
}

# Create a temporary dataframe for the known demand scenarios
df_temp = pd.DataFrame(data)

# Merge the temporary dataframe with the original structure (filling in NaNs for the missing years)
df_ai = pd.concat([df_ai, df_temp], ignore_index=True)


# ---------------------
# Interpolate the NaN values in the specific columns
df_ai['slope'] = (df_ai['2026'] - df_ai['2022']) / (2026-2022)  # Slope = change over 2 years (2026-2024)

# Extrapolate the values for years 2022 to 2050 using the slope
for year in range(2023, 2051):
    df_ai[str(year)] = df_ai['2022'] + df_ai['slope'] * (year - 2022)

# Remove the temporary 'slope' column
df_ai = df_ai.drop(columns=['slope'])

# delete
del year, data, df_temp











# In[5]: WORK WITH FA DATA
####################################

# -------------------
#CHECK FOR COUNTRIES ACROSS BOTH DATASETS


# -------------------
# get list of NGFS countries
df_ngfs_countries = pd.DataFrame(df_electricity_cp['Region'].unique(), columns=['ngfs'])



# -------------------
# Get list of FA countries
df_fa_power.loc[df_fa_power['countryiso3'] == "TZ1", 'countryiso3'] = "TZA"    # known edit in the data
df_fa_countries = df_fa_power.groupby(['countryiso3', 'subsector'])['activity'].sum().reset_index()
df_fa_countries = df_fa_countries[df_fa_countries['countryiso3'] != "unknown"]   # remove 'unknown' 



# -------------------
# merge with NGFS data
df_merged_countries_raw = pd.merge(df_fa_countries, df_ngfs_countries,
                               left_on='countryiso3',
                               right_on='ngfs',
                               how='outer')



# -------------------
# run checks
temp_df_fa_missing = df_merged_countries_raw[df_merged_countries_raw['countryiso3'].isna()]['ngfs'].unique()
print(temp_df_fa_missing)
#['Downscaling|Countries without IEA statistics']
# NOTE: above shows that all NGFS countries exist in FA dataset

temp_df_ngfs_missing = df_merged_countries_raw[df_merged_countries_raw['ngfs'].isna()]['countryiso3'].unique()
print(temp_df_ngfs_missing)
# ['ABW' 'AFG' 'AND' 'ASM' 'ATG' 'BDI' 'BFA' 'BHS' 'BMU' 'BRB' 'BTN' 'CAF'
#  'COM' 'CYM' 'DJI' 'DMA' 'ESH' 'FJI' 'GGY' 'GIN' 'GLP' 'GNB' 'GNQ' 'GRD'
#  'GRL' 'GUF' 'GUM' 'GUY' 'IMN' 'JEY' 'KNA' 'KOS' 'LAO' 'LBR' 'LCA' 'LSO'
#  'MAC' 'MDG' 'MDV' 'MRT' 'MSR' 'MTQ' 'MWI' 'NCL' 'PNG' 'PRI' 'PRK' 'RWA'
#  'SLE' 'SOM' 'SSD' 'SWZ' 'SYC' 'TCD' 'TLS' 'TON']
# NOTE: countries that are in FA but do not exist in NGFS will be assigned "Downscaling|Countries without IEA statistics" trend

# delete
del temp_df_fa_missing, temp_df_ngfs_missing


# -------------------
# assing --- see above
df_merged_countries_final = df_merged_countries_raw.copy()
df_merged_countries_final['ngfs_assigned'] = df_merged_countries_final['ngfs']
df_merged_countries_final.loc[df_merged_countries_final['ngfs_assigned'].isna(),'ngfs_assigned'] = 'Downscaling|Countries without IEA statistics'
df_merged_countries_final = df_merged_countries_final.groupby(['ngfs_assigned', 'subsector'])['activity'].sum().reset_index()


# delete
del df_fa_countries, df_ngfs_countries









# In[5]: CONVERT NGFS DATA WITH FA
####################################

# ---------------------
# THIS GETS NGFS ANNUAL YOY % CHANGE DF

# Calculate yearly percent change for each row
df_gcam_years = df_electricity_cp[years_2024]
pct_change_df = df_gcam_years.pct_change(axis=1) * 100
pct_change_df = pct_change_df.fillna(0)
del df_gcam_years

#First concatenate extrapolated data with filtered data frame
first_5_columns = df_electricity_cp.iloc[:, :5]
df_electricity_cp_change = pd.concat([first_5_columns, pct_change_df], axis=1)
del first_5_columns, pct_change_df



# ---------------------
# aLLIGNED SUBSECTOR/VARIABLE --- FUEL TYPE
print(df_electricity_cp['Variable'].unique())
# ['Secondary Energy|Electricity|Biomass'
#  'Secondary Energy|Electricity|Coal' 'Secondary Energy|Electricity|Gas'
#  'Secondary Energy|Electricity|Hydro' 'Secondary Energy|Electricity|Oil'
#  'Secondary Energy|Electricity|Solar' 'Secondary Energy|Electricity|Wind'
#  'Secondary Energy|Electricity|Geothermal'
#  'Secondary Energy|Electricity|Nuclear']

print(df_merged_countries_final['subsector'].unique())
# ['Bioenerge' 'Gas' 'Hydropower' 'Oil' 'Solar' 'Wind' 'Coal' 'Nuclear'
#  'Other' 'Geothermal ']


df_merged_countries_final.loc[df_merged_countries_final['subsector'] == 'Bioenerge', 'subsector'] = 'Secondary Energy|Electricity|Biomass'
df_merged_countries_final.loc[df_merged_countries_final['subsector'] == 'Gas', 'subsector'] = 'Secondary Energy|Electricity|Gas'
df_merged_countries_final.loc[df_merged_countries_final['subsector'] == 'Hydropower', 'subsector'] = 'Secondary Energy|Electricity|Hydro'
df_merged_countries_final.loc[df_merged_countries_final['subsector'] == 'Oil', 'subsector'] = 'Secondary Energy|Electricity|Oil'
df_merged_countries_final.loc[df_merged_countries_final['subsector'] == 'Solar', 'subsector'] = 'Secondary Energy|Electricity|Solar'
df_merged_countries_final.loc[df_merged_countries_final['subsector'] == 'Wind', 'subsector'] = 'Secondary Energy|Electricity|Wind'
df_merged_countries_final.loc[df_merged_countries_final['subsector'] == 'Coal', 'subsector'] = 'Secondary Energy|Electricity|Coal'
df_merged_countries_final.loc[df_merged_countries_final['subsector'] == 'Nuclear', 'subsector'] = 'Secondary Energy|Electricity|Nuclear'
df_merged_countries_final.loc[df_merged_countries_final['subsector'] == 'Geothermal ', 'subsector'] = 'Secondary Energy|Electricity|Geothermal'



# ---------------------
# MATCHING --- assigne FA values to 2024 in NGFS mathing country and fuel
df_electricity_cpfa = df_electricity_cp_change.copy()
activity_mapping = df_merged_countries_final.set_index(['ngfs_assigned', 'subsector'])['activity']    # Step 1: Set up the mapping for 'activity' values based on 'ngfs_assigned' and 'subsector'
df_electricity_cpfa['2024'] = df_electricity_cpfa.set_index(['Region', 'Variable']).index.map(activity_mapping)   # Step 2: Update '2024' in the second DataFrame based on the mapping
df_electricity_cpfa['2024'] = df_electricity_cpfa['2024'] / 10**6   # convert to TWh
df_electricity_cpfa.loc[df_electricity_cpfa['2024'].isna(), '2024'] = 0 

del activity_mapping



# ---------------------
# Now extend into 2050

# after this we get dataframe for secondary energy by source/country/scenario with annual emissions values
for i in range(1, len(years_2024)):
    
    previous_year = years_2024[i - 1]  # Get the previous year
    current_year = years_2024[i]       # Get the current year
    
    # Ensure the current year column exists before calculation
    if current_year in df_electricity_cpfa.columns:
        # Check for 'inf' values in the current year's percentage change column
        inf_mask = np.isinf(df_electricity_cpfa[current_year])
        
        # Update the current year's values based on the previous year where no 'inf' is present
        df_electricity_cpfa.loc[~inf_mask, current_year] = df_electricity_cpfa[previous_year] * (1 + df_electricity_cpfa[current_year] / 100)
        
        # For rows where 'inf' is present, replace with the corresponding value from df_actual_values
        df_electricity_cpfa.loc[inf_mask, current_year] = df_electricity_cp.loc[inf_mask, current_year]

# delete
del i, previous_year, current_year, inf_mask, 



# ---------------------
# get shares
df_electricity_cpfa_share = df_electricity_cpfa.copy()
df_electricity_cpfa_share[years_2024] =  df_electricity_cpfa_share[years_2024] / df_electricity_cpfa[years_2024].sum()
df_electricity_cpfa_share['Unit'] = "Share of global"







# In[5]: Create AI + CP SCENARIOS
####################################

# ---------------------
# add ai demand to Current Policies
df_electricity_cpai_h = df_electricity_cp.copy()
df_electricity_cpai_l = df_electricity_cp.copy()
df_electricity_cpai_b = df_electricity_cp.copy()
df_electricity_cpfaai_h = df_electricity_cpfa.copy()
df_electricity_cpfaai_l = df_electricity_cpfa.copy()
df_electricity_cpfaai_b = df_electricity_cpfa.copy()

# formula: 
# Generation_CP (t) + share of global electricity_CP (t-1)  X [ AI_t - AI_2024]

# 1 - NGFS
for year in years_2022:
    prev_year = str(int(year) - 1)
    df_electricity_cpai_h[year] = df_electricity_cp[year] + df_electricity_cp_share[prev_year] * (df_ai.loc[df_ai['case'] == "high", year].values[0] - df_ai.loc[df_ai['case'] == "high", "2022"].values[0])
    df_electricity_cpai_l[year] = df_electricity_cp[year] + df_electricity_cp_share[prev_year] * (df_ai.loc[df_ai['case'] == "low", year].values[0] - df_ai.loc[df_ai['case'] == "low", "2022"].values[0])
    df_electricity_cpai_b[year] = df_electricity_cp[year] + df_electricity_cp_share[prev_year] * (df_ai.loc[df_ai['case'] == "base", year].values[0] - df_ai.loc[df_ai['case'] == "base", "2022"].values[0])

del year, prev_year


# 2 - FA
for year in years_2024[1:]:   # this starting from 2025 (since 2024 is first year)
    prev_year = str(int(year) - 1)
    df_electricity_cpfaai_h[year] = df_electricity_cpfa[year] + df_electricity_cpfa_share[prev_year] * (df_ai.loc[df_ai['case'] == "high", year].values[0] - df_ai.loc[df_ai['case'] == "high", "2024"].values[0])
    df_electricity_cpfaai_l[year] = df_electricity_cpfa[year] + df_electricity_cpfa_share[prev_year] * (df_ai.loc[df_ai['case'] == "low", year].values[0] - df_ai.loc[df_ai['case'] == "low", "2024"].values[0])
    df_electricity_cpfaai_b[year] = df_electricity_cpfa[year] + df_electricity_cpfa_share[prev_year] * (df_ai.loc[df_ai['case'] == "base", year].values[0] - df_ai.loc[df_ai['case'] == "base", "2024"].values[0])

del year, prev_year


# ---------------------
# get global trends
df_electricity_cpai_h_global = df_electricity_cpai_h.groupby('Variable')[years_2020].sum().reset_index()
df_electricity_cpai_l_global = df_electricity_cpai_l.groupby('Variable')[years_2020].sum().reset_index()
df_electricity_cpai_b_global = df_electricity_cpai_b.groupby('Variable')[years_2020].sum().reset_index()

df_electricity_cpfaai_h_global = df_electricity_cpfaai_h.groupby('Variable')[years_2024].sum().reset_index()
df_electricity_cpfaai_l_global = df_electricity_cpfaai_l.groupby('Variable')[years_2024].sum().reset_index()
df_electricity_cpfaai_b_global = df_electricity_cpfaai_b.groupby('Variable')[years_2024].sum().reset_index()








# In[5]: COMPARISON TABLES
####################################

# ---------------------
# 2024
temp_cp_2020 = round(df_electricity_cp.groupby('Variable')['2020'].sum().rename('NGFS 2020'), 1)
temp_cp_2024 = round(df_electricity_cp.groupby('Variable')['2024'].sum().rename('NGFS 2024'), 1)
temp_cpfa_2024 = round(df_electricity_cpfa.groupby('Variable')['2024'].sum().rename('FA'), 1)

# Merge the two Series into a single DataFrame
df_comparison_2024 = pd.concat([temp_cp_2020, temp_cp_2024, temp_cpfa_2024], axis=1).fillna(0)

# Display the resulting DataFrame
print(df_comparison_2024)

#                                         NGFS 2020  NGFS 2024      FA
# Variable                                                             
# Secondary Energy|Electricity|Biomass         542.9      539.9   371.7
# Secondary Energy|Electricity|Coal          10065.5    10489.6  9976.0
# Secondary Energy|Electricity|Gas            6176.5     6317.3  7751.0
# Secondary Energy|Electricity|Geothermal      244.2      371.8   104.1
# Secondary Energy|Electricity|Hydro          4357.7     4431.0  7872.2
# Secondary Energy|Electricity|Nuclear        2629.3     2469.7  3863.2
# Secondary Energy|Electricity|Oil             557.5      582.5   593.5
# Secondary Energy|Electricity|Solar          3050.3     7273.7  1106.9
# Secondary Energy|Electricity|Wind           4382.6     7836.6  2111.9



# ---------------------
# 2050
temp_cp_2050 = round(df_electricity_cp.groupby('Variable')['2050'].sum().rename('NGFS'), 1)
temp_cpfa_2050 = round(df_electricity_cpfa.groupby('Variable')['2050'].sum().rename('FA'), 1)

# Merge the two Series into a single DataFrame
df_comparison_2050 = pd.concat([temp_cp_2050, temp_cpfa_2050], axis=1).fillna(0)

# Display the resulting DataFrame
print(df_comparison_2050)

#                                             NGFS       FA
# Variable                                                 
# Secondary Energy|Electricity|Biomass       709.6    389.8
# Secondary Energy|Electricity|Coal         9769.7   9092.5
# Secondary Energy|Electricity|Gas         10594.6  13544.0
# Secondary Energy|Electricity|Geothermal    692.3    174.9
# Secondary Energy|Electricity|Hydro        4758.4   8195.2
# Secondary Energy|Electricity|Nuclear       968.3   1309.1
# Secondary Energy|Electricity|Oil          1624.0   2019.6
# Secondary Energy|Electricity|Solar       13376.7   2281.0
# Secondary Energy|Electricity|Wind        15615.9   3930.7


# delete
del temp_cp_2020, temp_cp_2024, temp_cp_2050, temp_cpfa_2024, temp_cpfa_2050










# In[5]: Create AI + CP SCENARIOS
####################################

del df_gcam
del df_fa_power
del df_gcam_filtered










# In[10]:
# Export data

# electricity by country and type --- CP
df_electricity_cp.to_excel('2 - output/script 7.1 - ai scenarios - electricity generation/7.1.1 - electricity generation - by country and type - cp.xlsx', index=False)
df_electricity_cpai_b.to_excel('2 - output/script 7.1 - ai scenarios - electricity generation/7.1.2 - electricity generation - by country and type - cp ai - base.xlsx', index=False)
df_electricity_cpai_h.to_excel('2 - output/script 7.1 - ai scenarios - electricity generation/7.1.3 - electricity generation - by country and type - cp ai - high.xlsx', index=False)
df_electricity_cpai_l.to_excel('2 - output/script 7.1 - ai scenarios - electricity generation/7.1.4 - electricity generation - by country and type - cp ai - low.xlsx', index=False)

# electricity by country and type --- CP FA
df_electricity_cpfa.to_excel('2 - output/script 7.1 - ai scenarios - electricity generation/7.2.1 - electricity generation - by country and type - cp fa.xlsx', index=False)
df_electricity_cpfaai_b.to_excel('2 - output/script 7.1 - ai scenarios - electricity generation/7.2.2 - electricity generation - by country and type - cp fa ai - base.xlsx', index=False)
df_electricity_cpfaai_h.to_excel('2 - output/script 7.1 - ai scenarios - electricity generation/7.2.3 - electricity generation - by country and type - cp fa ai - high.xlsx', index=False)
df_electricity_cpfaai_l.to_excel('2 - output/script 7.1 - ai scenarios - electricity generation/7.2.4 - electricity generation - by country and type - cp fa ai - low.xlsx', index=False)



# electricity global by type --- CP
df_electricity_cp_global.to_excel('2 - output/script 7.1 - ai scenarios - electricity generation/7.3.1 - electricity generation - global by type - cp.xlsx', index=False)
df_electricity_cpai_b_global.to_excel('2 - output/script 7.1 - ai scenarios - electricity generation/7.3.2 - electricity generation - global by type - cp ai - base.xlsx', index=False)
df_electricity_cpai_h_global.to_excel('2 - output/script 7.1 - ai scenarios - electricity generation/7.3.3 - electricity generation - global by type - cp ai - high.xlsx', index=False)
df_electricity_cpai_l_global.to_excel('2 - output/script 7.1 - ai scenarios - electricity generation/7.3.4 - electricity generation - global by type - cp ai - low.xlsx', index=False)

# electricity global by type --- CP FA
df_electricity_cp_global.to_excel('2 - output/script 7.1 - ai scenarios - electricity generation/7.4.1 - electricity generation - global by type - cp fa.xlsx', index=False)
df_electricity_cpai_b_global.to_excel('2 - output/script 7.1 - ai scenarios - electricity generation/7.4.2 - electricity generation - global by type - cp fa ai - base.xlsx', index=False)
df_electricity_cpai_h_global.to_excel('2 - output/script 7.1 - ai scenarios - electricity generation/7.4.3 - electricity generation - global by type - cp fa ai - high.xlsx', index=False)
df_electricity_cpai_l_global.to_excel('2 - output/script 7.1 - ai scenarios - electricity generation/7.4.4 - electricity generation - global by type - cp fa ai - low.xlsx', index=False)


# other data
df_electricity_cp_share.to_excel('2 - output/script 7.1 - ai scenarios - electricity generation/7.5.1 - electricity generation - by country and type - cp - share.xlsx', index=False)
df_ai.to_excel('2 - output/script 7.1 - ai scenarios - electricity generation/7.5.2 - electricity generation - ai.xlsx', index=False)

# comparison tablea
df_comparison_2024.to_excel('2 - output/script 7.1 - ai scenarios - electricity generation/7.6.1 - comparison table - ngfs vs fa - 2024.xlsx', index=False)
df_comparison_2050.to_excel('2 - output/script 7.1 - ai scenarios - electricity generation/7.6.2 - comparison table - ngfs vs fa - 2050.xlsx', index=False)






















