# In[1]:
# Date: July 28, 2024
# Project: Applying NGFS trends to FA data - Primary energy / Extraction sector
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
import matplotlib.cm as cm










# In[3]: LOADING DATA
##################################################
# directory & load data

directory = r'C:\Users\panah\OneDrive\Desktop\Work\2 - RA - Climate fin'
os.chdir(directory)
del directory


# --------------
# load oilgas and caol
df_extraction_coal = pd.read_excel('2 - output/script 1/4 - extraction_coal.xlsx')   
df_extraction_gas = pd.read_excel('2 - output/script 1/5 - extraction_gas.xlsx')   
df_extraction_oil = pd.read_excel('2 - output/script 1/6 - extraction_oil.xlsx')   

df_extraction_coal['countryiso3'] = df_extraction_coal['countryiso3'].replace('TZ1', 'TZA') # this fixed an error in naming Tanzania
df_extraction_gas['countryiso3'] = df_extraction_gas['countryiso3'].replace('TZ1', 'TZA') # this fixed an error in naming Tanzania
df_extraction_oil['countryiso3'] = df_extraction_oil['countryiso3'].replace('TZ1', 'TZA') # this fixed an error in naming Tanzania


# -----------------------
# load growth projections
df_growth = pd.read_excel('2 - output/script 2/1.3 - GCAM - percent change.xlsx')


# ------------------------------------
# load NGFS secondary energy scenarios
#df_ngfs_scenarios_cumulative = pd.read_excel('2 - output/script 2/4.2 - GCAM - emissions - scenarios - secondary - cumulative.xlsx')
df_ngfs_emissions = pd.read_excel('2 - output/script 2/1.2 - GCAM - filtered - emissions.xlsx')


# -------------------
# load region dataset
df_regions = pd.read_excel('1 - input/Country Datasets/country_gca_region.xlsx')










# In[]: SCREATE A DATA FRAME FOR PRIMARY EMISSION ONLY
#######################################################

# -------------------
# # subset growth to secondary only & remove 2020-2023 years --- i.e start from 2024
df_growth_primary = df_growth[df_growth['Variable'].str.contains('Primary')]
df_growth_primary= df_growth_primary.drop(columns = ['2020', '2021', '2022', '2023']) # removing 2020-2023
df_growth_primary['2024'] = 0 # set all 2024 values to zero --- these will be filled by FA data


# -------------------
# # subset emissions to secondary only & remove 2020-2023 years --- i.e start from 2024
df_ngfs_emissions_primary = df_ngfs_emissions[df_ngfs_emissions['Variable'].str.contains('Primary')]
df_ngfs_emissions_primary= df_ngfs_emissions_primary.drop(columns = ['2020', '2021', '2022', '2023']) # removing 2020-2023









    
# In[4]: GET POWER BY SOURCE FOR MAPPING BASED ON SOURCE AND COUNTRY
####################################################################
# subset plants by source

# -------------------
#coal
df_extraction_coal = df_extraction_coal.groupby(['countryiso3'])['emissionsco2e20years'].sum()
df_extraction_coal = df_extraction_coal.reset_index()


#gas
df_extraction_gas = df_extraction_gas.groupby(['countryiso3'])['annual_co2_calc_20yr'].sum()
df_extraction_gas = df_extraction_gas.reset_index()


#oil
df_extraction_oil = df_extraction_oil.groupby(['countryiso3'])['annual_co2_calc_20yr'].sum()
df_extraction_oil = df_extraction_oil.reset_index()


# -------------------
# total
df_extraction_total = pd.merge(df_extraction_coal, df_extraction_gas,
                               on='countryiso3',
                               how='outer')

df_extraction_total = pd.merge(df_extraction_total, df_extraction_oil,
                               on='countryiso3',
                               how='outer')

# df names
df_extraction_total.columns = ['country_FA', 'coal_FA', 'gas_FA', 'oil_FA']










# In[]: CHECK FOR COUNTRIES ACROSS BOTH DATASETS
################################################

# -------------------
# get list of NGFS countries
df_ngfs_countries = df_ngfs_emissions[df_ngfs_emissions['Scenario'] == 'Current Policies']
df_ngfs_countries = df_ngfs_countries[df_ngfs_countries['Variable'].str.contains('Primary')]
df_ngfs_countries = df_ngfs_countries[['Region', 'Variable', '2024']]

df_ngfs_countries = df_ngfs_countries.pivot(index='Region', columns='Variable', values='2024')
df_ngfs_countries.reset_index(inplace = True)


# -------------------
# merge NGFS data with FA countries
df_merged_countries_raw = pd.merge(df_extraction_total, df_ngfs_countries,
                               left_on='country_FA',
                               right_on='Region',
                               how='outer')

# df names
df_merged_countries_raw.columns = ['country_FA', 'coal_FA', 'gas_FA', 'oil_FA', 'country_NGFS',
                               'coal_NGFS', 'gas_NGFS', 'oil_NGFS']










# In[]: GET NEW MERGED COUTNTRY DATAFRAME
#########################################

# get new dataframe
df_merged_countries_edited = df_merged_countries_raw.copy()

# remove 'unknown' from FA country list
df_merged_countries_edited = df_merged_countries_edited[df_merged_countries_edited['country_FA'] != 'unknown']

# for countries in FA that dont have NGFS equivalent, set them as 'Downscaling|Countries without IEA statistics'
df_merged_countries_edited['country_NGFS'] = df_merged_countries_edited['country_NGFS'].replace(np.nan, 'Downscaling|Countries without IEA statistics')

# here is list of countries that are in NGFS but dont exist in FA:
    # CIV (Côte d'Ivoire), HTI (Haiti), SDN (Sudan)
# remove NA's in FA country list
df_merged_countries_edited = df_merged_countries_edited[df_merged_countries_edited['country_FA'].notna()]

# group by NGFS countries --- Now all FA countries have an equivalent from NGFS
df_merged_countries_edited = df_merged_countries_edited.groupby('country_NGFS')[['coal_FA', 'gas_FA', 'oil_FA']].sum()
df_merged_countries_edited.reset_index(inplace = True)










# In[]: USE MAPPING TO ADD EMISSSONS VALUES TO YEAR 2024 BACK TO MASTER DATA
############################################################################
# Get power values added to 2020 of growth dataframe

# -------------------
# coal
# Step 1: Filter to include only rows where 'Variable' contains "coal"
df_growth_extraction_coal = df_growth_primary[df_growth_primary['Variable'].str.contains('Coal')]

# Step 2: Create a mapping Series
co2_mapping = df_merged_countries_edited.set_index('country_NGFS')['coal_FA']

# Step 3: Map and substitute values in the '2020' column for the filtered DataFrame
df_growth_extraction_coal['2024'] = df_growth_extraction_coal['Region'].map(co2_mapping)

# Step 4: Update the original DataFrame
df_growth_primary.update(df_growth_extraction_coal)


# -------------------
# gas
df_growth_primary_gas = df_growth_primary[df_growth_primary['Variable'].str.contains('Gas')]
co2_mapping = df_merged_countries_edited.set_index('country_NGFS')['gas_FA']
df_growth_primary_gas['2024'] = df_growth_primary_gas['Region'].map(co2_mapping)
df_growth_primary.update(df_growth_primary_gas)


# -------------------
# oil
df_growth_primary_oil = df_growth_primary[df_growth_primary['Variable'].str.contains('Oil')]
co2_mapping = df_merged_countries_edited.set_index('country_NGFS')['oil_FA']
df_growth_primary_oil['2024'] = df_growth_primary_oil['Region'].map(co2_mapping)
df_growth_primary.update(df_growth_primary_oil)


# -------------------
del co2_mapping, df_growth_extraction_coal, df_growth_primary_gas, df_growth_primary_oil
del df_extraction_coal, df_extraction_oil, df_extraction_gas
del df_extraction_total, df_ngfs_countries










# In[]: IF COUNTRY DOESNT HAVE A GROWTH TREND AT ALL USE 'small country trend'
##############################################################################

# Columns to check for zero values
year_columns = [str(year) for year in range(2025, 2101)]


# Iterate over unique combinations of Scenario and Variable
for scenario in df_growth_primary['Scenario'].unique():
    for variable in df_growth_primary['Variable'].unique():
        # Filter the DataFrame for the specific Scenario and Variable
        mask = (df_growth_primary['Scenario'] == scenario) & (df_growth_primary['Variable'] == variable)
        
        # Extract the "Downscaling|Countries without IEA statistics" values
        downscaling_values = df_growth_primary.loc[(mask) & (df_growth_primary['Region'] == 'Downscaling|Countries without IEA statistics'), year_columns].values
        
        # Find all regions where all values in the year columns are zero
        zero_mask = mask & (df_growth_primary[year_columns] == 0).all(axis=1)
            
        # Replace the zero rows with the downscaling values
        df_growth_primary.loc[zero_mask, year_columns] = downscaling_values


del mask, scenario, downscaling_values, variable, year_columns, zero_mask


# -------------------
# save this new edited annual growth file separately
df_growth_primary_change = df_growth_primary.copy()










# In[5]: PROJECT THE GROWTH TO ANNUAL EMISSIOSN
###############################################

# set years of analysis
year_columns = [str(year) for year in range(2024, 2051)]


# after this we get dataframe for secondary energy by source/country/scenario with annual emissions values
for i in range(1, len(year_columns)):
    previous_year = year_columns[i - 1]  # Get the previous year
    current_year = year_columns[i]       # Get the current year
    
    # Ensure the current year column exists before calculation
    if current_year in df_growth_primary.columns:
        # Check for 'inf' values in the current year's percentage change column
        inf_mask = np.isinf(df_growth_primary[current_year])
        
        # Update the current year's values based on the previous year where no 'inf' is present
        df_growth_primary.loc[~inf_mask, current_year] = df_growth_primary[previous_year] * (1 + df_growth_primary[current_year] / 100)
        
        # For rows where 'inf' is present, replace with the corresponding value from df_actual_values
        df_growth_primary.loc[inf_mask, current_year] = df_ngfs_emissions_primary.loc[inf_mask, current_year]


del i, current_year, previous_year, inf_mask, year_columns










# In[6]: NOW SLICE AND DICE THE DATA: by fuel type, region, develoment, etc.
# WE GET THESE BOTH ANNUAL AND CUMULATIVE
############################################################################

# set years 2024-2050    
year_columns50 = [str(year) for year in range(2024, 2051)]


#############################################################
# 1 --- SCENARIO --------------------------------------------
#############################################################

# annual
df_growth_primary_byscenario_annual = df_growth_primary.groupby(['Scenario'])[year_columns50].sum()
df_growth_primary_byscenario_annual.reset_index(inplace=True)

# cumulative
df_growth_primary_byscenario_cumulative = df_growth_primary_byscenario_annual.copy()
df_growth_primary_byscenario_cumulative[year_columns50] = df_growth_primary_byscenario_cumulative[year_columns50].cumsum(axis=1)
df_growth_primary_byscenario_cumulative.reset_index(inplace=True)





#############################################################
# 2 --- FUEL TYPE -------------------------------------------
#############################################################

# -------------------
### net zero
# annual
df_growth_primary_netzero_byfueltype_annual = df_growth_primary[df_growth_primary['Scenario'] == "Net Zero 2050"]
df_growth_primary_netzero_byfueltype_annual = df_growth_primary_netzero_byfueltype_annual.groupby(['fuel_type'])[year_columns50].sum()
df_growth_primary_netzero_byfueltype_annual.reset_index(inplace=True)

# cumulative
df_growth_primary_netzero_byfueltype_cumulative = df_growth_primary_netzero_byfueltype_annual.copy()
df_growth_primary_netzero_byfueltype_cumulative[year_columns50] = df_growth_primary_netzero_byfueltype_cumulative[year_columns50].cumsum(axis=1)
df_growth_primary_netzero_byfueltype_cumulative.reset_index(inplace=True) 


# -------------------
### current policies
# annual
df_growth_primary_currentpolicy_byfueltype_annual = df_growth_primary[df_growth_primary['Scenario'] == "Current Policies"]
df_growth_primary_currentpolicy_byfueltype_annual = df_growth_primary_currentpolicy_byfueltype_annual.groupby(['fuel_type'])[year_columns50].sum()
df_growth_primary_currentpolicy_byfueltype_annual.reset_index(inplace=True)

# cumulative
df_growth_primary_currentpolicy_byfueltype_cumulative = df_growth_primary_currentpolicy_byfueltype_annual.copy()
df_growth_primary_currentpolicy_byfueltype_cumulative[year_columns50] = df_growth_primary_currentpolicy_byfueltype_cumulative[year_columns50].cumsum(axis=1)
df_growth_primary_currentpolicy_byfueltype_cumulative.reset_index(inplace=True) 





#############################################################
# 3 --- REGION ----------------------------------------------
#############################################################

# -------------------
### net zero
# annual
df_growth_primary_netzero_byregion_annual = df_growth_primary[df_growth_primary['Scenario'] == "Net Zero 2050"]
df_growth_primary_netzero_byregion_annual = df_growth_primary_netzero_byregion_annual.groupby(['gca_region'])[year_columns50].sum()
df_growth_primary_netzero_byregion_annual.reset_index(inplace=True)

# cumulative
df_growth_primary_netzero_byregion_cumulative = df_growth_primary_netzero_byregion_annual.copy()
df_growth_primary_netzero_byregion_cumulative[year_columns50] = df_growth_primary_netzero_byregion_cumulative[year_columns50].cumsum(axis=1)
df_growth_primary_netzero_byregion_cumulative.reset_index(inplace=True) 


# -------------------
### current policies
# annual
df_growth_primary_currentpolicy_byregion_annual = df_growth_primary[df_growth_primary['Scenario'] == "Current Policies"]
df_growth_primary_currentpolicy_byregion_annual = df_growth_primary_currentpolicy_byregion_annual.groupby(['gca_region'])[year_columns50].sum()
df_growth_primary_currentpolicy_byregion_annual.reset_index(inplace=True)

# cumulative
df_growth_primary_currentpolicy_byregion_cumulative = df_growth_primary_currentpolicy_byregion_annual.copy()
df_growth_primary_currentpolicy_byregion_cumulative[year_columns50] = df_growth_primary_currentpolicy_byregion_cumulative[year_columns50].cumsum(axis=1)
df_growth_primary_currentpolicy_byregion_cumulative.reset_index(inplace=True) 





#############################################################
# 4 --- DEVELOPMENT -----------------------------------------
#############################################################

# -------------------
### net zero
# annual
df_growth_primary_netzero_bydev_annual = df_growth_primary[df_growth_primary['Scenario'] == "Net Zero 2050"]
df_growth_primary_netzero_bydev_annual = df_growth_primary_netzero_bydev_annual.groupby(['development_level'])[year_columns50].sum()
df_growth_primary_netzero_bydev_annual.reset_index(inplace=True)

# cumulative
df_growth_primary_netzero_bydev_cumulative = df_growth_primary_netzero_bydev_annual.copy()
df_growth_primary_netzero_bydev_cumulative[year_columns50] = df_growth_primary_netzero_bydev_cumulative[year_columns50].cumsum(axis=1)
df_growth_primary_netzero_bydev_cumulative.reset_index(inplace=True) 


# -------------------
### current policies
# annual
df_growth_primary_currentpolicy_bydev_annual = df_growth_primary[df_growth_primary['Scenario'] == "Current Policies"]
df_growth_primary_currentpolicy_bydev_annual = df_growth_primary_currentpolicy_bydev_annual.groupby(['development_level'])[year_columns50].sum()
df_growth_primary_currentpolicy_bydev_annual.reset_index(inplace=True)

# cumulative
df_growth_primary_currentpolicy_bydev_cumulative = df_growth_primary_currentpolicy_bydev_annual.copy()
df_growth_primary_currentpolicy_bydev_cumulative[year_columns50] = df_growth_primary_currentpolicy_bydev_cumulative[year_columns50].cumsum(axis=1)
df_growth_primary_currentpolicy_bydev_cumulative.reset_index(inplace=True) 





#############################################################
# 5 --- BYCOUNTRY - TOP 15 ----------------------------------
#############################################################

# -------------------
### net zero
# annual
df_growth_primary_netzero_bycountry_annual = df_growth_primary[df_growth_primary['Scenario'] == "Net Zero 2050"]
df_growth_primary_netzero_bycountry_annual = df_growth_primary_netzero_bycountry_annual.groupby(['Region'])[year_columns50].sum()
df_growth_primary_netzero_bycountry_annual.reset_index(inplace=True)

# cumulative
df_growth_primary_netzero_bycountry_cumulative = df_growth_primary_netzero_bycountry_annual.copy()
df_growth_primary_netzero_bycountry_cumulative[year_columns50] = df_growth_primary_netzero_bycountry_cumulative[year_columns50].cumsum(axis=1)
df_growth_primary_netzero_bycountry_cumulative.reset_index(inplace=True) 


### NOW GET TOP 15 COUNTRIES
# 1 --- cumulative
# sort by top 15 countries in 2050 --- CUMULATIVE
df_growth_primary_netzero_bycountry_cumulative = df_growth_primary_netzero_bycountry_cumulative.sort_values(by='2050', ascending=False)
df_top15_cumulative = df_growth_primary_netzero_bycountry_cumulative.head(15)

# Sum the remaining countries into 'Other'
df_other_cumulative = df_growth_primary_netzero_bycountry_cumulative.iloc[15:].copy()
df_other_cumulative_sum = df_other_cumulative[year_columns50].sum().to_frame().T
df_other_cumulative_sum['Region'] = 'Other'

# Combine the top 15 countries with the 'Other' row
df_top15_netzero_cumulative = pd.concat([df_top15_cumulative, df_other_cumulative_sum], ignore_index=True)

del df_other_cumulative, df_other_cumulative_sum, df_top15_cumulative


# 2 - annual
# sort by top 15 countries in 2050 --- ANNUAL --- using top15 from cumulative
top15_countries = df_top15_netzero_cumulative['Region'].head(15).tolist()
df_top15_annual = df_growth_primary_netzero_bycountry_annual[df_growth_primary_netzero_bycountry_annual['Region'].isin(top15_countries)]

#Sum the values of the remaining countries into 'Other'
df_other_annual = df_growth_primary_netzero_bycountry_annual[~df_growth_primary_netzero_bycountry_annual['Region'].isin(top15_countries)].copy()
df_other_annual_sum = df_other_annual[year_columns50].sum().to_frame().T
df_other_annual_sum['Region'] = 'Other'

# Combine the top 15 countries with the 'Other' row
df_top15_netzero_annual = pd.concat([df_top15_annual, df_other_annual_sum], ignore_index=True)
df_top15_netzero_annual = df_top15_netzero_annual.sort_values(by='2050', ascending=False)


del df_other_annual, df_other_annual_sum, df_top15_annual
del top15_countries





# -------------------
### current policies
# annual
df_growth_primary_currentpolicy_bycountry_annual = df_growth_primary[df_growth_primary['Scenario'] == "Current Policies"]
df_growth_primary_currentpolicy_bycountry_annual = df_growth_primary_currentpolicy_bycountry_annual.groupby(['Region'])[year_columns50].sum()
df_growth_primary_currentpolicy_bycountry_annual.reset_index(inplace=True)

# cumulative
df_growth_primary_currentpolicy_bycountry_cumulative = df_growth_primary_currentpolicy_bycountry_annual.copy()
df_growth_primary_currentpolicy_bycountry_cumulative[year_columns50] = df_growth_primary_currentpolicy_bycountry_cumulative[year_columns50].cumsum(axis=1)
df_growth_primary_currentpolicy_bycountry_cumulative.reset_index(inplace=True) 


### NOW GET TOP 15 COUNTRIES
# 1 --- cumulative
# sort by top 15 countries in 2050 --- CUMULATIVE
df_growth_primary_currentpolicy_bycountry_cumulative = df_growth_primary_currentpolicy_bycountry_cumulative.sort_values(by='2050', ascending=False)
df_top15_cumulative = df_growth_primary_currentpolicy_bycountry_cumulative.head(15)

# Sum the remaining countries into 'Other'
df_other_cumulative = df_growth_primary_currentpolicy_bycountry_cumulative.iloc[15:].copy()
df_other_cumulative_sum = df_other_cumulative[year_columns50].sum().to_frame().T
df_other_cumulative_sum['Region'] = 'Other'

# Combine the top 15 countries with the 'Other' row
df_top15_currentpolicy_cumulative = pd.concat([df_top15_cumulative, df_other_cumulative_sum], ignore_index=True)

del df_other_cumulative, df_other_cumulative_sum, df_top15_cumulative


# 2 - annual
# sort by top 15 countries in 2050 --- ANNUAL --- using top15 from cumulative
top15_countries = df_top15_currentpolicy_cumulative['Region'].head(15).tolist()
df_top15_annual = df_growth_primary_currentpolicy_bycountry_annual[df_growth_primary_currentpolicy_bycountry_annual['Region'].isin(top15_countries)]

#Sum the values of the remaining countries into 'Other'
df_other_annual = df_growth_primary_currentpolicy_bycountry_annual[~df_growth_primary_currentpolicy_bycountry_annual['Region'].isin(top15_countries)].copy()
df_other_annual_sum = df_other_annual[year_columns50].sum().to_frame().T
df_other_annual_sum['Region'] = 'Other'

# Combine the top 15 countries with the 'Other' row
df_top15_currentpolicy_annual = pd.concat([df_top15_annual, df_other_annual_sum], ignore_index=True)
df_top15_currentpolicy_annual = df_top15_currentpolicy_annual.sort_values(by='2050', ascending=False)


del df_other_annual, df_other_annual_sum, df_top15_annual
del top15_countries


# -------------------
# add country names
region_to_country = pd.Series(df_regions['name'].values, index=df_regions['alpha-3']).to_dict()

df_top15_netzero_annual['Country'] = df_top15_netzero_annual['Region'].map(region_to_country)
df_top15_netzero_annual['Country'].fillna('Other', inplace=True)

df_top15_netzero_cumulative['Country'] = df_top15_netzero_cumulative['Region'].map(region_to_country)
df_top15_netzero_cumulative['Country'].fillna('Other', inplace=True)

df_top15_currentpolicy_annual['Country'] = df_top15_currentpolicy_annual['Region'].map(region_to_country)
df_top15_currentpolicy_annual['Country'].fillna('Other', inplace=True)

df_top15_currentpolicy_cumulative['Country'] = df_top15_currentpolicy_cumulative['Region'].map(region_to_country)
df_top15_currentpolicy_cumulative['Country'].fillna('Other', inplace=True)











# In[6]: # EXPORT DATA
######################################

# growth dataset 
df_growth_primary.to_excel('2 - output/script 3.2/1.1 - Primary - emissions FA - projection.xlsx', index=False)
df_growth_primary_change.to_excel('2 - output/script 3.2/1.2 - Primary - emissions FA - change.xlsx', index=False)
df_ngfs_emissions_primary.to_excel('2 - output/script 3.2/1.3 - Primary - emissions NGFS - projection.xlsx', index=False)


# by scenario
df_growth_primary_byscenario_annual.to_excel('2 - output/script 3.2/2.1 - Primary - by scenario - annual.xlsx', index=False)
df_growth_primary_byscenario_cumulative.to_excel('2 - output/script 3.2/2.2 - Primary - by scenario - cumulative.xlsx', index=False)

# by netzero - annual
df_growth_primary_netzero_byfueltype_annual.to_excel('2 - output/script 3.2/3.1 - Primary - netzero - annual - fueltype.xlsx', index=False)
df_growth_primary_netzero_byregion_annual.to_excel('2 - output/script 3.2/3.2 - Primary - netzero - annual - regions.xlsx', index=False)
df_growth_primary_netzero_bydev_annual.to_excel('2 - output/script 3.2/3.3 - Primary - netzero - annual - development.xlsx', index=False)
df_growth_primary_netzero_bycountry_annual.to_excel('2 - output/script 3.2/3.4 - Primary - netzero - annual - country.xlsx', index=False)

# by netzero - cumulative
df_growth_primary_netzero_byfueltype_cumulative.to_excel('2 - output/script 3.2/4.1 - Primary - netzero - cumulative - fueltype.xlsx', index=False)
df_growth_primary_netzero_byregion_cumulative.to_excel('2 - output/script 3.2/4.2 - Primary - netzero - cumulative - regions.xlsx', index=False)
df_growth_primary_netzero_bydev_cumulative.to_excel('2 - output/script 3.2/4.3 - Primary - netzero - cumulative - development.xlsx', index=False)
df_growth_primary_netzero_bycountry_cumulative.to_excel('2 - output/script 3.2/4.4 - Primary - netzero - cumulative - country.xlsx', index=False)

# by current policy - annual
df_growth_primary_currentpolicy_byfueltype_annual.to_excel('2 - output/script 3.2/5.1 - Primary - currentpolicy - annual - fueltype.xlsx', index=False)
df_growth_primary_currentpolicy_byregion_annual.to_excel('2 - output/script 3.2/5.2 - Primary - currentpolicy - annual - regions.xlsx', index=False)
df_growth_primary_currentpolicy_bydev_annual.to_excel('2 - output/script 3.2/5.3 - Primary - currentpolicy - annual - development.xlsx', index=False)
df_growth_primary_currentpolicy_bycountry_annual.to_excel('2 - output/script 3.2/5.4 - Primary - currentpolicy - annual - country.xlsx', index=False)

# by current policy - cumulative
df_growth_primary_currentpolicy_byfueltype_cumulative.to_excel('2 - output/script 3.2/6.1 - Primary - currentpolicy - cumulative - fueltype.xlsx', index=False)
df_growth_primary_currentpolicy_byregion_cumulative.to_excel('2 - output/script 3.2/6.2 - Primary - currentpolicy - cumulative - regions.xlsx', index=False)
df_growth_primary_currentpolicy_bydev_cumulative.to_excel('2 - output/script 3.2/6.3 - Primary - currentpolicy - cumulative - development.xlsx', index=False)
df_growth_primary_currentpolicy_bycountry_cumulative.to_excel('2 - output/script 3.2/6.4 - Primary - currentpolicy - cumulative - country.xlsx', index=False)

# countries 
df_merged_countries_raw.to_excel('2 - output/script 3.2/7.1 - Merged countries - raw.xlsx', index=False)
df_merged_countries_edited.to_excel('2 - output/script 3.2/7.2 - Merged countries - formatted.xlsx', index=False)





