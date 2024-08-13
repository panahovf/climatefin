# In[1]:
# Date: July 28, 2024
# Project: Applying NGFS trends to FA data - Secondary energy / Power sector
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
# load power
df_power = pd.read_csv('1 - input/v3_power_Forward_Analytics2024.csv')   
df_power = df_power[df_power['status'] == "operating"]
df_power['countryiso3'] = df_power['countryiso3'].replace('TZ1', 'TZA') # this fixed an error in naming Tanzania


# -----------------------
# load growth projections
df_growth = pd.read_excel('2 - output/script 2/1.3 - GCAM - percent change.xlsx')


# ------------------------------------
# load NGFS secondary energy scenarios
df_ngfs_scenarios_cumulative = pd.read_excel('2 - output/script 2/4.2 - GCAM - emissions - scenarios - secondary - cumulative.xlsx')
df_ngfs_emissions = pd.read_excel('2 - output/script 2/1.2 - GCAM - filtered - emissions.xlsx')


# -------------------
# load region dataset
df_regions = pd.read_excel('1 - input/Country Datasets/country_gca_region.xlsx')










# In[]: SCREATE A DATA FRAME FOR SCONDARY EMISSION ONLY
#######################################################

# -------------------
# # subset growth to secondary only & remove 2020-2023 years --- i.e start from 2024
df_growth_secondary = df_growth[df_growth['Variable'].str.contains('Secondary')]
df_growth_secondary= df_growth_secondary.drop(columns = ['2020', '2021', '2022', '2023']) # removing 2020-2023
df_growth_secondary['2024'] = 0 # set all 2024 values to zero --- these will be filled by FA data


# -------------------
# # subset emissions to secondary only & remove 2020-2023 years --- i.e start from 2024
df_ngfs_emissions_secondary = df_ngfs_emissions[df_ngfs_emissions['Variable'].str.contains('Secondary')]
df_ngfs_emissions_secondary= df_ngfs_emissions_secondary.drop(columns = ['2020', '2021', '2022', '2023']) # removing 2020-2023









    
# In[4]: GET POWER BY SOURCE FOR MAPPING BASED ON SOURCE AND COUNTRY
####################################################################
# subset power plants by source

# -------------------
#coal
df_power_coal = df_power[df_power['subsector'] == 'Coal']
df_power_coal = df_power_coal.groupby(['countryiso3'])['annual_co2_calc'].sum()
df_power_coal = df_power_coal.reset_index()


# -------------------
#gas
df_power_gas = df_power[df_power['subsector'] == 'Gas']
df_power_gas = df_power_gas.groupby(['countryiso3'])['annual_co2_calc'].sum()
df_power_gas = df_power_gas.reset_index()


# -------------------
#oil
df_power_oil = df_power[df_power['subsector'] == 'Oil']
df_power_oil = df_power_oil.groupby(['countryiso3'])['annual_co2_calc'].sum()
df_power_oil = df_power_oil.reset_index()










# In[]: CHECK FOR COUNTRIES ACROSS BOTH DATASETS
################################################

# -------------------
# get list of NGFS countries
df_ngfs_countries = df_ngfs_emissions[df_ngfs_emissions['Scenario'] == 'Current Policies']
df_ngfs_countries = df_ngfs_countries[df_ngfs_countries['Variable'].str.contains('Secondary')]
df_ngfs_countries = df_ngfs_countries[['Region', 'Variable', '2024']]

df_ngfs_countries = df_ngfs_countries.pivot(index='Region', columns='Variable', values='2024')
df_ngfs_countries.reset_index(inplace = True)


# -------------------
# Get list of FA countries
df_fa_countries = df_power[['countryiso3']].drop_duplicates()
df_fa_countries.reset_index(drop=True, inplace = True)


# Add FA data into the country list above
df_fa_countries = pd.merge(df_fa_countries,df_power_coal,
                           on='countryiso3',
                           how='left')

df_fa_countries = pd.merge(df_fa_countries,df_power_gas,
                           on='countryiso3',
                           how='left')

df_fa_countries = pd.merge(df_fa_countries,df_power_oil,
                           on='countryiso3',
                           how='left')


# -------------------
# merge with NGFS data
df_merged_countries_raw = pd.merge(df_fa_countries, df_ngfs_countries,
                               left_on='countryiso3',
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
df_growth_secondary_coal = df_growth_secondary[df_growth_secondary['Variable'].str.contains('Coal')]

# Step 2: Create a mapping Series
co2_mapping = df_merged_countries_edited.set_index('country_NGFS')['coal_FA']

# Step 3: Map and substitute values in the '2020' column for the filtered DataFrame
df_growth_secondary_coal['2024'] = df_growth_secondary_coal['Region'].map(co2_mapping)

# Step 4: Update the original DataFrame
df_growth_secondary.update(df_growth_secondary_coal)


# -------------------
# gas
df_growth_secondary_gas = df_growth_secondary[df_growth_secondary['Variable'].str.contains('Gas')]
co2_mapping = df_merged_countries_edited.set_index('country_NGFS')['gas_FA']
df_growth_secondary_gas['2024'] = df_growth_secondary_gas['Region'].map(co2_mapping)
df_growth_secondary.update(df_growth_secondary_gas)


# -------------------
# oil
df_growth_secondary_oil = df_growth_secondary[df_growth_secondary['Variable'].str.contains('Oil')]
co2_mapping = df_merged_countries_edited.set_index('country_NGFS')['oil_FA']
df_growth_secondary_oil['2024'] = df_growth_secondary_oil['Region'].map(co2_mapping)
df_growth_secondary.update(df_growth_secondary_oil)


# -------------------
del co2_mapping, df_growth_secondary_coal, df_growth_secondary_gas, df_growth_secondary_oil
del df_power_coal, df_power_oil, df_power_gas
del df_fa_countries, df_ngfs_countries










# In[]: IF COUNTRY DOESNT HAVE A GROWTH TREND AT ALL USE 'small country trend'
##############################################################################

# Columns to check for zero values
year_columns = [str(year) for year in range(2025, 2101)]


# Iterate over unique combinations of Scenario and Variable
for scenario in df_growth_secondary['Scenario'].unique():
    for variable in df_growth_secondary['Variable'].unique():
        # Filter the DataFrame for the specific Scenario and Variable
        mask = (df_growth_secondary['Scenario'] == scenario) & (df_growth_secondary['Variable'] == variable)
        
        # Extract the "Downscaling|Countries without IEA statistics" values
        downscaling_values = df_growth_secondary.loc[(mask) & (df_growth_secondary['Region'] == 'Downscaling|Countries without IEA statistics'), year_columns].values
        
        # Find all regions where all values in the year columns are zero
        zero_mask = mask & (df_growth_secondary[year_columns] == 0).all(axis=1)
            
        # Replace the zero rows with the downscaling values
        df_growth_secondary.loc[zero_mask, year_columns] = downscaling_values


del mask, scenario, downscaling_values, variable, year_columns, zero_mask


# -------------------
# save this new edited annual growth file separately
df_growth_secondary_change = df_growth_secondary.copy()










# In[5]: PROJECT THE GROWTH TO ANNUAL EMISSIOSN
###############################################

# set years of analysis
year_columns = [str(year) for year in range(2024, 2051)]


# after this we get dataframe for secondary energy by source/country/scenario with annual emissions values
for i in range(1, len(year_columns)):
    previous_year = year_columns[i - 1]  # Get the previous year
    current_year = year_columns[i]       # Get the current year
    
    # Ensure the current year column exists before calculation
    if current_year in df_growth_secondary.columns:
        # Check for 'inf' values in the current year's percentage change column
        inf_mask = np.isinf(df_growth_secondary[current_year])
        
        # Update the current year's values based on the previous year where no 'inf' is present
        df_growth_secondary.loc[~inf_mask, current_year] = df_growth_secondary[previous_year] * (1 + df_growth_secondary[current_year] / 100)
        
        # For rows where 'inf' is present, replace with the corresponding value from df_actual_values
        df_growth_secondary.loc[inf_mask, current_year] = df_ngfs_emissions_secondary.loc[inf_mask, current_year]


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
df_growth_secondary_byscenario_annual = df_growth_secondary.groupby(['Scenario'])[year_columns50].sum()
df_growth_secondary_byscenario_annual.reset_index(inplace=True)

# cumulative
df_growth_secondary_byscenario_cumulative = df_growth_secondary_byscenario_annual.copy()
df_growth_secondary_byscenario_cumulative[year_columns50] = df_growth_secondary_byscenario_cumulative[year_columns50].cumsum(axis=1)
df_growth_secondary_byscenario_cumulative.reset_index(inplace=True)





#############################################################
# 2 --- FUEL TYPE -------------------------------------------
#############################################################

# -------------------
### net zero
# annual
df_growth_secondary_netzero_byfueltype_annual = df_growth_secondary[df_growth_secondary['Scenario'] == "Net Zero 2050"]
df_growth_secondary_netzero_byfueltype_annual = df_growth_secondary_netzero_byfueltype_annual.groupby(['fuel_type'])[year_columns50].sum()
df_growth_secondary_netzero_byfueltype_annual.reset_index(inplace=True)

# cumulative
df_growth_secondary_netzero_byfueltype_cumulative = df_growth_secondary_netzero_byfueltype_annual.copy()
df_growth_secondary_netzero_byfueltype_cumulative[year_columns50] = df_growth_secondary_netzero_byfueltype_cumulative[year_columns50].cumsum(axis=1)
df_growth_secondary_netzero_byfueltype_cumulative.reset_index(inplace=True) 


# -------------------
### current policies
# annual
df_growth_secondary_currentpolicy_byfueltype_annual = df_growth_secondary[df_growth_secondary['Scenario'] == "Current Policies"]
df_growth_secondary_currentpolicy_byfueltype_annual = df_growth_secondary_currentpolicy_byfueltype_annual.groupby(['fuel_type'])[year_columns50].sum()
df_growth_secondary_currentpolicy_byfueltype_annual.reset_index(inplace=True)

# cumulative
df_growth_secondary_currentpolicy_byfueltype_cumulative = df_growth_secondary_currentpolicy_byfueltype_annual.copy()
df_growth_secondary_currentpolicy_byfueltype_cumulative[year_columns50] = df_growth_secondary_currentpolicy_byfueltype_cumulative[year_columns50].cumsum(axis=1)
df_growth_secondary_currentpolicy_byfueltype_cumulative.reset_index(inplace=True) 





#############################################################
# 3 --- REGION ----------------------------------------------
#############################################################

# -------------------
### net zero
# annual
df_growth_secondary_netzero_byregion_annual = df_growth_secondary[df_growth_secondary['Scenario'] == "Net Zero 2050"]
df_growth_secondary_netzero_byregion_annual = df_growth_secondary_netzero_byregion_annual.groupby(['gca_region'])[year_columns50].sum()
df_growth_secondary_netzero_byregion_annual.reset_index(inplace=True)

# cumulative
df_growth_secondary_netzero_byregion_cumulative = df_growth_secondary_netzero_byregion_annual.copy()
df_growth_secondary_netzero_byregion_cumulative[year_columns50] = df_growth_secondary_netzero_byregion_cumulative[year_columns50].cumsum(axis=1)
df_growth_secondary_netzero_byregion_cumulative.reset_index(inplace=True) 


# -------------------
### current policies
# annual
df_growth_secondary_currentpolicy_byregion_annual = df_growth_secondary[df_growth_secondary['Scenario'] == "Current Policies"]
df_growth_secondary_currentpolicy_byregion_annual = df_growth_secondary_currentpolicy_byregion_annual.groupby(['gca_region'])[year_columns50].sum()
df_growth_secondary_currentpolicy_byregion_annual.reset_index(inplace=True)

# cumulative
df_growth_secondary_currentpolicy_byregion_cumulative = df_growth_secondary_currentpolicy_byregion_annual.copy()
df_growth_secondary_currentpolicy_byregion_cumulative[year_columns50] = df_growth_secondary_currentpolicy_byregion_cumulative[year_columns50].cumsum(axis=1)
df_growth_secondary_currentpolicy_byregion_cumulative.reset_index(inplace=True) 





#############################################################
# 4 --- DEVELOPMENT -----------------------------------------
#############################################################

# -------------------
### net zero
# annual
df_growth_secondary_netzero_bydev_annual = df_growth_secondary[df_growth_secondary['Scenario'] == "Net Zero 2050"]
df_growth_secondary_netzero_bydev_annual = df_growth_secondary_netzero_bydev_annual.groupby(['development_level'])[year_columns50].sum()
df_growth_secondary_netzero_bydev_annual.reset_index(inplace=True)

# cumulative
df_growth_secondary_netzero_bydev_cumulative = df_growth_secondary_netzero_bydev_annual.copy()
df_growth_secondary_netzero_bydev_cumulative[year_columns50] = df_growth_secondary_netzero_bydev_cumulative[year_columns50].cumsum(axis=1)
df_growth_secondary_netzero_bydev_cumulative.reset_index(inplace=True) 


# -------------------
### current policies
# annual
df_growth_secondary_currentpolicy_bydev_annual = df_growth_secondary[df_growth_secondary['Scenario'] == "Current Policies"]
df_growth_secondary_currentpolicy_bydev_annual = df_growth_secondary_currentpolicy_bydev_annual.groupby(['development_level'])[year_columns50].sum()
df_growth_secondary_currentpolicy_bydev_annual.reset_index(inplace=True)

# cumulative
df_growth_secondary_currentpolicy_bydev_cumulative = df_growth_secondary_currentpolicy_bydev_annual.copy()
df_growth_secondary_currentpolicy_bydev_cumulative[year_columns50] = df_growth_secondary_currentpolicy_bydev_cumulative[year_columns50].cumsum(axis=1)
df_growth_secondary_currentpolicy_bydev_cumulative.reset_index(inplace=True) 





#############################################################
# 5 --- BYCOUNTRY - TOP 15 ----------------------------------
#############################################################

# -------------------
### net zero
# annual
df_growth_secondary_netzero_bycountry_annual = df_growth_secondary[df_growth_secondary['Scenario'] == "Net Zero 2050"]
df_growth_secondary_netzero_bycountry_annual = df_growth_secondary_netzero_bycountry_annual.groupby(['Region'])[year_columns50].sum()
df_growth_secondary_netzero_bycountry_annual.reset_index(inplace=True)

# cumulative
df_growth_secondary_netzero_bycountry_cumulative = df_growth_secondary_netzero_bycountry_annual.copy()
df_growth_secondary_netzero_bycountry_cumulative[year_columns50] = df_growth_secondary_netzero_bycountry_cumulative[year_columns50].cumsum(axis=1)
df_growth_secondary_netzero_bycountry_cumulative.reset_index(inplace=True) 


### now get top 15 countries
# 1 --- cumulative
# sort by top 15 countries in 2050 --- CUMULATIVE
df_growth_secondary_netzero_bycountry_cumulative = df_growth_secondary_netzero_bycountry_cumulative.sort_values(by='2050', ascending=False)
df_top15_cumulative = df_growth_secondary_netzero_bycountry_cumulative.head(15)

# Sum the remaining countries into 'Other'
df_other_cumulative = df_growth_secondary_netzero_bycountry_cumulative.iloc[15:].copy()
df_other_cumulative_sum = df_other_cumulative[year_columns50].sum().to_frame().T
df_other_cumulative_sum['Region'] = 'Other'

# Combine the top 15 countries with the 'Other' row
df_top15_netzero_cumulative = pd.concat([df_top15_cumulative, df_other_cumulative_sum], ignore_index=True)

del df_other_cumulative, df_other_cumulative_sum, df_top15_cumulative


# 2 - annual
# sort by top 15 countries in 2050 --- ANNUAL --- using top15 from cumulative
top15_countries = df_top15_netzero_cumulative['Region'].head(15).tolist()
df_top15_annual = df_growth_secondary_netzero_bycountry_annual[df_growth_secondary_netzero_bycountry_annual['Region'].isin(top15_countries)]

#Sum the values of the remaining countries into 'Other'
df_other_annual = df_growth_secondary_netzero_bycountry_annual[~df_growth_secondary_netzero_bycountry_annual['Region'].isin(top15_countries)].copy()
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
df_growth_secondary_currentpolicy_bycountry_annual = df_growth_secondary[df_growth_secondary['Scenario'] == "Current Policies"]
df_growth_secondary_currentpolicy_bycountry_annual = df_growth_secondary_currentpolicy_bycountry_annual.groupby(['Region'])[year_columns50].sum()
df_growth_secondary_currentpolicy_bycountry_annual.reset_index(inplace=True)

# cumulative
df_growth_secondary_currentpolicy_bycountry_cumulative = df_growth_secondary_currentpolicy_bycountry_annual.copy()
df_growth_secondary_currentpolicy_bycountry_cumulative[year_columns50] = df_growth_secondary_currentpolicy_bycountry_cumulative[year_columns50].cumsum(axis=1)
df_growth_secondary_currentpolicy_bycountry_cumulative.reset_index(inplace=True) 


### now get top 15 countries
# 1 --- cumulative
# sort by top 15 countries in 2050 --- CUMULATIVE
df_growth_secondary_currentpolicy_bycountry_cumulative = df_growth_secondary_currentpolicy_bycountry_cumulative.sort_values(by='2050', ascending=False)
df_top15_cumulative = df_growth_secondary_currentpolicy_bycountry_cumulative.head(15)

# Sum the remaining countries into 'Other'
df_other_cumulative = df_growth_secondary_currentpolicy_bycountry_cumulative.iloc[15:].copy()
df_other_cumulative_sum = df_other_cumulative[year_columns50].sum().to_frame().T
df_other_cumulative_sum['Region'] = 'Other'

# Combine the top 15 countries with the 'Other' row
df_top15_currentpolicy_cumulative = pd.concat([df_top15_cumulative, df_other_cumulative_sum], ignore_index=True)

del df_other_cumulative, df_other_cumulative_sum, df_top15_cumulative


# 2 - annual
# sort by top 15 countries in 2050 --- ANNUAL --- using top15 from cumulative
top15_countries = df_top15_currentpolicy_cumulative['Region'].head(15).tolist()
df_top15_annual = df_growth_secondary_currentpolicy_bycountry_annual[df_growth_secondary_currentpolicy_bycountry_annual['Region'].isin(top15_countries)]

#Sum the values of the remaining countries into 'Other'
df_other_annual = df_growth_secondary_currentpolicy_bycountry_annual[~df_growth_secondary_currentpolicy_bycountry_annual['Region'].isin(top15_countries)].copy()
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










# In[12]:
# get cumulative by scenario for NGFS

# combine FA and NGFS
df_comparison_faVSngfs = df_growth_secondary_byscenario_cumulative[['Scenario', '2024', '2050']] # keep 2024 and 2050 in FA
temp = df_ngfs_scenarios_cumulative[['Scenario', '2024', '2050']] # create temporary 2024 & 2050 for NGFS


# merge them
df_comparison_faVSngfs = df_comparison_faVSngfs.merge(temp, on = 'Scenario', how = 'left')
del temp










# In[11]


#####################################################################
#####################################################################
#####################################################################
#####################################################################
########## PLOTS PLOTS PLOTS PLOTS PLOTS PLOTS PLOTS ################
#####################################################################
#####################################################################
#####################################################################
#####################################################################



# In[]: COMPARE FA VS NGFS in 2050

# Plot --- FA vs NGFS 2050
scenarios = df_comparison_faVSngfs['Scenario']
indices = np.arange(len(scenarios))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots(figsize=(12, 8))
real_data = ax.bar(indices - width/2, df_comparison_faVSngfs['2050_x'], width, label='Current power plants projected to 2050', color='#004c6d')
modeled_data = ax.bar(indices + width/2, df_comparison_faVSngfs['2050_y'], width, label='NGFS GCAM 6 Model 2050',color='#667c8e' )

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Emissions (GtCO2)')
plt.title('2050 Cumulative Emissions Comparison: Current Assets vs NGFS', fontsize=20, pad=30)
plt.text(0.5, 1.01, 'NGFS GCAM 6 Model vs projections on assets in operation based on NGFS growth rates', transform=ax.transAxes, ha='center', fontsize=10)

ax.set_xticks(indices)
ax.set_xticklabels(scenarios, rotation=45)
ax.set_xticklabels(scenarios, rotation=0, fontsize=10)  # No rotation and increased font size

# Formatter function to convert values to thousands
def thousands_formatter(x, pos):
    return f'{int(x/1000)}'    # the values are in Mt, but diving the axis by 1000 to show in Gt

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))


fig.tight_layout()
plt.show()










# In[8]:

##################################################################################################
##################### SECTION 1: BY SCENARIO VS CARBON BUDGET ####################################
##################################################################################################

# -------------------
# Plot 1.1 --- the annual emissions
plt.figure(figsize=(12, 8))

for scenario in df_growth_secondary_byscenario_annual['Scenario'].unique():
    plt.plot(year_columns50, df_growth_secondary_byscenario_annual[df_growth_secondary_byscenario_annual['Scenario'] == scenario][year_columns50].values[0], label=scenario)

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Add a vertical red line at 2050
#plt.axvline(x='2050', color='red', linestyle='--', linewidth=2, label='GCAM projection limit')

# Add horizontal grid lines
plt.grid(axis='both', which='both', linestyle='--', linewidth=0.7)

# Set y-axis limits
plt.ylim(0, 25000)

# Formatter function to convert values to thousands
def thousands_formatter(x, pos):
    return f'{int(x/1000)}'    # the values are in Mt, but diving the axis by 1000 to show in Gt

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

plt.xlabel('Year')
plt.ylabel('GtCO2')
plt.title('Annual Emissions from Power Sector', fontsize=20, pad=30)
plt.text(0.5, 1.01, 'Projections are based on NGFS GCAM6 model\'s growth rates applied to current assets in operation', transform=ax.transAxes, ha='center', fontsize=10)

plt.legend()
plt.show()





# -------------------
# Plot 1.2 --- the cumulative emissions
plt.figure(figsize=(12, 8))

for scenario in df_growth_secondary_byscenario_cumulative['Scenario'].unique():
    plt.plot(year_columns50, df_growth_secondary_byscenario_cumulative[df_growth_secondary_byscenario_cumulative['Scenario'] == scenario][year_columns50].values[0], label=scenario)

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Add a vertical red line at 2050
#plt.axvline(x='2050', color='red', linestyle='--', linewidth=2, label='GCAM projection limit')

# Add horizontal grid lines
plt.grid(axis='both', which='both', linestyle='--', linewidth=0.7)

# Set y-axis limits
plt.ylim(0, 500000)

# Formatter function to convert values to thousands
def thousands_formatter(x, pos):
    return f'{int(x/1000)}'    # the values are in Mt, but diving the axis by 1000 to show in Gt

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Add a shaded region between 400 and 580 on the y-axis
plt.axhspan(258000, 358000, color='#d4e157', alpha=0.5)
plt.text(5, 300000, 'Carbon budget: 1.5°C warming', color='black', fontsize=12, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5))

# Add a shaded region between 400 and 580 on the y-axis
plt.axhspan(408000, 508000, color='orange', alpha=0.3)
plt.text(15, 450000, '1.6°C warming', color='black', fontsize=12, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5))

plt.xlabel('Year')
plt.ylabel('GtCO2')
plt.title('Cumulative Emissions from Power Sector', fontsize=20, pad=30)
plt.text(0.5, 1.01, 'NGFS GCAM 6 Model projections on assets in operation; Carbon budget ranges indicate 50%-67% likelyhood for limiting global warming', transform=ax.transAxes, ha='center', fontsize=10)

plt.legend()
plt.show()










# In[8]:

##################################################################################################
##################### SECTION 2: BY FUEL TYPE VS CARBON BUDGET ###################################
##################################################################################################

# -------------------
### NET ZERO  
# Plot 2.1 --- the annual emissions
plt.figure(figsize=(12, 8))

# Create empty lists to hold lines and labels for the legend


for scenario in df_growth_secondary_netzero_byfueltype_annual['fuel_type'].unique():
    line, = plt.plot(
        year_columns50, 
        df_growth_secondary_netzero_byfueltype_annual[df_growth_secondary_netzero_byfueltype_annual['fuel_type'] == scenario][year_columns50].values[0], 
        label=scenario)

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Add a vertical red line at 2050
#plt.axvline(x='2050', color='red', linestyle='--', linewidth=2, label='GCAM projection limit')

# Add horizontal grid lines
plt.grid(axis='both', which='both', linestyle='--', linewidth=0.7)

# Set y-axis limits
plt.ylim(0, 12000)

# Formatter function to convert values to thousands
def thousands_formatter(x, pos):
    return f'{int(x/1000)}'    # the values are in Mt, but diving the axis by 1000 to show in Gt

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

plt.xlabel('Year',fontsize = 15 )
plt.ylabel('GtCO2', fontsize = 15)
plt.title('Annual Emissions from Power Sector', fontsize=25, pad=50)
plt.text(0.5, 1.05, 'Projections are based on current power plants in operation', transform=ax.transAxes, ha='center', fontsize=14)
plt.text(0.5, 1.01, 'NGFS GCAM6 model\'s growth rates are applied for projections; Scenario: Net Zero 2050', transform=ax.transAxes, ha='center', fontsize=12)

plt.legend(fontsize = 20)
plt.show()





# -------------------
# Plot 2.2 --- the cumulative emissions
plt.figure(figsize=(12, 8))

# Prepare the data for stackplot
scenarios = df_growth_secondary_netzero_byfueltype_cumulative['fuel_type'].unique()
values = [
    df_growth_secondary_netzero_byfueltype_cumulative[
        df_growth_secondary_netzero_byfueltype_cumulative['fuel_type'] == scenario
    ][year_columns50].values[0]
    for scenario in scenarios
]

# Plot the stacked area chart
plt.stackplot(year_columns50, values, labels=scenarios)

    
# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Add a vertical red line at 2050
#plt.axvline(x='2050', color='red', linestyle='--', linewidth=2, label='GCAM projection limit')

# Add horizontal grid lines
plt.grid(axis='both', which='both', linestyle='--', linewidth=0.7)

# Set y-axis limits
plt.ylim(0, 400000)

# Formatter function to convert values to thousands
def thousands_formatter(x, pos):
    return f'{int(x/1000)}'    # the values are in Mt, but diving the axis by 1000 to show in Gt

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Add a shaded region between 400 and 580 on the y-axis
plt.axhspan(258000, 358000, color='#d4e157', alpha=0.5)
plt.text(5, 300000, 'Carbon budget: 1.5°C warming', color='black', fontsize=15, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5))


plt.xlabel('Year',fontsize = 15 )
plt.ylabel('GtCO2', fontsize = 15)
plt.title('Cumulative Emissions from Power Sector', fontsize=25, pad=60)
plt.text(0.5, 1.09, 'Projections are based on current power plants in operation', transform=ax.transAxes, ha='center', fontsize=14)
plt.text(0.5, 1.05, 'NGFS GCAM6 model\'s growth rates are applied for projections; Scenario: Net Zero 2050', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.01, 'Carbon budget range represents 50%-67% likelyhood for global warming', transform=ax.transAxes, ha='center', fontsize=12)


plt.legend(fontsize = 20)
plt.show()





# -------------------
### CURRENT POLICY  
# Plot 2.3 --- the annual emissions
plt.figure(figsize=(12, 8))

for scenario in df_growth_secondary_currentpolicy_byfueltype_annual['fuel_type'].unique():
    line, = plt.plot(
        year_columns50, 
        df_growth_secondary_currentpolicy_byfueltype_annual[df_growth_secondary_currentpolicy_byfueltype_annual['fuel_type'] == scenario][year_columns50].values[0], 
        label= scenario)

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Add a vertical red line at 2050
#plt.axvline(x='2050', color='red', linestyle='--', linewidth=2, label='GCAM projection limit')

# Add horizontal grid lines
plt.grid(axis='both', which='both', linestyle='--', linewidth=0.7)

# Set y-axis limits
plt.ylim(0, 12000)

# Formatter function to convert values to thousands
def thousands_formatter(x, pos):
    return f'{int(x/1000)}'    # the values are in Mt, but diving the axis by 1000 to show in Gt

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

plt.xlabel('Year',fontsize = 15 )
plt.ylabel('GtCO2', fontsize = 15)
plt.title('Annual Emissions from Power Sector', fontsize=25, pad=50)
plt.text(0.5, 1.05, 'Projections are based on current power plants in operation', transform=ax.transAxes, ha='center', fontsize=14)
plt.text(0.5, 1.01, 'NGFS GCAM6 model\'s growth rates are applied for projections; Scenario: Current Policies', transform=ax.transAxes, ha='center', fontsize=12)

plt.legend(fontsize = 20)
plt.show()





# -------------------
# Plot 2.4 --- the cumulative emissions
plt.figure(figsize=(12, 8))

# Prepare the data for stackplot
scenarios = df_growth_secondary_currentpolicy_byfueltype_cumulative['fuel_type'].unique()
values = [
    df_growth_secondary_currentpolicy_byfueltype_cumulative[
        df_growth_secondary_currentpolicy_byfueltype_cumulative['fuel_type'] == scenario
    ][year_columns50].values[0]
    for scenario in scenarios
]

# Plot the stacked area chart
plt.stackplot(year_columns50, values, labels=scenarios)

    
# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Add a vertical red line at 2050
#plt.axvline(x='2050', color='red', linestyle='--', linewidth=2, label='GCAM projection limit')

# Add horizontal grid lines
plt.grid(axis='both', which='both', linestyle='--', linewidth=0.7)

# Set y-axis limits
plt.ylim(0, 400000)

# Formatter function to convert values to thousands
def thousands_formatter(x, pos):
    return f'{int(x/1000)}'    # the values are in Mt, but diving the axis by 1000 to show in Gt

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Add a shaded region between 400 and 580 on the y-axis
plt.axhspan(258000, 358000, color='#d4e157', alpha=0.5)
plt.text(5, 300000, 'Carbon budget: 1.5°C warming', color='black', fontsize=15, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5))

plt.xlabel('Year',fontsize = 15 )
plt.ylabel('GtCO2', fontsize = 15)
plt.title('Cumulative Emissions from Power Sector', fontsize=25, pad=60)
plt.text(0.5, 1.09, 'Projections are based on current power plants in operation', transform=ax.transAxes, ha='center', fontsize=14)
plt.text(0.5, 1.05, 'NGFS GCAM6 model\'s growth rates are applied for projections; Scenario: Net Zero 2050', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.01, 'Carbon budget range represents 50%-67% likelyhood for global warming', transform=ax.transAxes, ha='center', fontsize=12)


plt.legend(fontsize = 20)
plt.show()










# In[8]:

###############################################################################################
##################### SECTION 3: BY REGION VS CARBON BUDGET ###################################
###############################################################################################

# -------------------
### NET ZERO  
# Plot 3.1 --- the annual emissions
plt.figure(figsize=(12, 8))

for scenario in df_growth_secondary_netzero_byregion_annual['gca_region'].unique():
    plt.plot(year_columns50, df_growth_secondary_netzero_byregion_annual[df_growth_secondary_netzero_byregion_annual['gca_region'] == scenario][year_columns50].values[0], label=scenario)

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Add a vertical red line at 2050
#plt.axvline(x='2050', color='red', linestyle='--', linewidth=2, label='GCAM projection limit')

# Add horizontal grid lines
plt.grid(axis='both', which='both', linestyle='--', linewidth=0.7)

# Set y-axis limits
plt.ylim(0, 12000)

# Formatter function to convert values to thousands
def thousands_formatter(x, pos):
    return f'{int(x/1000)}'    # the values are in Mt, but diving the axis by 1000 to show in Gt

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

plt.xlabel('Year',fontsize = 15 )
plt.ylabel('GtCO2', fontsize = 15)
plt.title('Annual Emissions from Power Sector', fontsize=25, pad=50)
plt.text(0.5, 1.05, 'Projections are based on current power plants in operation', transform=ax.transAxes, ha='center', fontsize=14)
plt.text(0.5, 1.01, 'NGFS GCAM6 model\'s growth rates are applied for projections; Scenario: Net Zero 2050', transform=ax.transAxes, ha='center', fontsize=12)

plt.legend(fontsize = 15)
plt.show()





# -------------------
# Plot 3.2 --- the cumulative emissions
plt.figure(figsize=(12, 8))

# Prepare the data for stackplot
scenarios = df_growth_secondary_netzero_byregion_cumulative['gca_region'].unique()
values = [
    df_growth_secondary_netzero_byregion_cumulative[
        df_growth_secondary_netzero_byregion_cumulative['gca_region'] == scenario
    ][year_columns50].values[0]
    for scenario in scenarios
]

# Plot the stacked area chart
plt.stackplot(year_columns50, values, labels=scenarios)


# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Add a vertical red line at 2050
#plt.axvline(x='2050', color='red', linestyle='--', linewidth=2, label='GCAM projection limit')

# Add horizontal grid lines
plt.grid(axis='both', which='both', linestyle='--', linewidth=0.7)

# Set y-axis limits
plt.ylim(0, 400000)

# Formatter function to convert values to thousands
def thousands_formatter(x, pos):
    return f'{int(x/1000)}'    # the values are in Mt, but diving the axis by 1000 to show in Gt

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Add a shaded region between 400 and 580 on the y-axis
plt.axhspan(258000, 358000, color='#d4e157', alpha=0.5)
plt.text(5, 300000, 'Carbon budget: 1.5°C warming', color='black', fontsize=15, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5))

plt.xlabel('Year',fontsize = 15 )
plt.ylabel('GtCO2', fontsize = 15)
plt.title('Cumulative Emissions from Power Sector', fontsize=25, pad=60)
plt.text(0.5, 1.09, 'Projections are based on current power plants in operation', transform=ax.transAxes, ha='center', fontsize=14)
plt.text(0.5, 1.05, 'NGFS GCAM6 model\'s growth rates are applied for projections; Scenario: Net Zero 2050', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.01, 'Carbon budget range represents 50%-67% likelyhood for global warming', transform=ax.transAxes, ha='center', fontsize=12)

plt.legend(fontsize = 15, loc = 'upper right')
plt.show()





# -------------------
### CURRENT POLICY 
# Plot 3.3 --- the annual emissions
plt.figure(figsize=(12, 8))

for scenario in df_growth_secondary_currentpolicy_byregion_annual['gca_region'].unique():
    plt.plot(year_columns50, df_growth_secondary_currentpolicy_byregion_annual[df_growth_secondary_currentpolicy_byregion_annual['gca_region'] == scenario][year_columns50].values[0], label=scenario)

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Add a vertical red line at 2050
#plt.axvline(x='2050', color='red', linestyle='--', linewidth=2, label='GCAM projection limit')

# Add horizontal grid lines
plt.grid(axis='both', which='both', linestyle='--', linewidth=0.7)

# Set y-axis limits
plt.ylim(0, 12000)

# Formatter function to convert values to thousands
def thousands_formatter(x, pos):
    return f'{int(x/1000)}'    # the values are in Mt, but diving the axis by 1000 to show in Gt

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

plt.xlabel('Year',fontsize = 15 )
plt.ylabel('GtCO2', fontsize = 15)
plt.title('Annual Emissions from Power Sector', fontsize=25, pad=50)
plt.text(0.5, 1.05, 'Projections are based on current power plants in operation', transform=ax.transAxes, ha='center', fontsize=14)
plt.text(0.5, 1.01, 'NGFS GCAM6 model\'s growth rates are applied for projections; Scenario: Current Policies', transform=ax.transAxes, ha='center', fontsize=12)

plt.legend(fontsize = 15)
plt.show()





# -------------------
# Plot 3.4 --- the cumulative emissions
plt.figure(figsize=(12, 8))

# Prepare the data for stackplot
scenarios = df_growth_secondary_currentpolicy_byregion_cumulative['gca_region'].unique()
values = [
    df_growth_secondary_currentpolicy_byregion_cumulative[
        df_growth_secondary_currentpolicy_byregion_cumulative['gca_region'] == scenario
    ][year_columns50].values[0]
    for scenario in scenarios
]

# Plot the stacked area chart
plt.stackplot(year_columns50, values, labels=scenarios)


# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Add a vertical red line at 2050
#plt.axvline(x='2050', color='red', linestyle='--', linewidth=2, label='GCAM projection limit')

# Add horizontal grid lines
plt.grid(axis='both', which='both', linestyle='--', linewidth=0.7)

# Set y-axis limits
plt.ylim(0, 500000)

# Formatter function to convert values to thousands
def thousands_formatter(x, pos):
    return f'{int(x/1000)}'    # the values are in Mt, but diving the axis by 1000 to show in Gt

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Add a shaded region between 400 and 580 on the y-axis
plt.axhspan(258000, 358000, color='#d4e157', alpha=0.5)
plt.text(5, 300000, 'Carbon budget: 1.5°C warming', color='black', fontsize=15, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5))

plt.xlabel('Year',fontsize = 15 )
plt.ylabel('GtCO2', fontsize = 15)
plt.title('Cumulative Emissions from Power Sector', fontsize=25, pad=60)
plt.text(0.5, 1.09, 'Projections are based on current power plants in operation', transform=ax.transAxes, ha='center', fontsize=14)
plt.text(0.5, 1.05, 'NGFS GCAM6 model\'s growth rates are applied for projections; Scenario: Current Policies', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.01, 'Carbon budget range represents 50%-67% likelyhood for global warming', transform=ax.transAxes, ha='center', fontsize=12)

plt.legend(fontsize = 15)
plt.show()










# In[8]:

#################################################################################################
##################### SECTION 4: DEVELOPMENT VS CARBON BUDGET ###################################
#################################################################################################

# -------------------
### NET ZERO  
# Plot 4.1 --- the annual emissions
plt.figure(figsize=(12, 8))

for scenario in df_growth_secondary_netzero_bydev_annual['development_level'].unique():
    plt.plot(year_columns50, df_growth_secondary_netzero_bydev_annual[df_growth_secondary_netzero_bydev_annual['development_level'] == scenario][year_columns50].values[0], label=scenario)

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Add a vertical red line at 2050
#plt.axvline(x='2050', color='red', linestyle='--', linewidth=2, label='GCAM projection limit')

# Add horizontal grid lines
plt.grid(axis='both', which='both', linestyle='--', linewidth=0.7)

# Set y-axis limits
plt.ylim(0, 12000)

# Formatter function to convert values to thousands
def thousands_formatter(x, pos):
    return f'{int(x/1000)}'    # the values are in Mt, but diving the axis by 1000 to show in Gt

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

plt.xlabel('Year',fontsize = 15 )
plt.ylabel('GtCO2', fontsize = 15)
plt.title('Annual Emissions from Power Sector', fontsize=25, pad=50)
plt.text(0.5, 1.05, 'Projections are based on current power plants in operation', transform=ax.transAxes, ha='center', fontsize=14)
plt.text(0.5, 1.01, 'NGFS GCAM6 model\'s growth rates are applied for projections; Scenario: Net Zero 2050', transform=ax.transAxes, ha='center', fontsize=12)

plt.legend(fontsize = 15)
plt.show()





# -------------------
# Plot 4.2 --- the cumulative emissions
plt.figure(figsize=(12, 8))

# Prepare the data for stackplot
scenarios = df_growth_secondary_netzero_bydev_cumulative['development_level'].unique()
values = [
    df_growth_secondary_netzero_bydev_cumulative[
        df_growth_secondary_netzero_bydev_cumulative['development_level'] == scenario
    ][year_columns50].values[0]
    for scenario in scenarios
]

# Plot the stacked area chart
plt.stackplot(year_columns50, values, labels=scenarios)

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Add a vertical red line at 2050
#plt.axvline(x='2050', color='red', linestyle='--', linewidth=2, label='GCAM projection limit')

# Add horizontal grid lines
plt.grid(axis='both', which='both', linestyle='--', linewidth=0.7)

# Set y-axis limits
plt.ylim(0, 500000)

# Formatter function to convert values to thousands
def thousands_formatter(x, pos):
    return f'{int(x/1000)}'    # the values are in Mt, but diving the axis by 1000 to show in Gt

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Add a shaded region between 400 and 580 on the y-axis
plt.axhspan(258000, 358000, color='#d4e157', alpha=0.5)
plt.text(5, 300000, 'Carbon budget: 1.5°C warming', color='black', fontsize=15, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5))

plt.xlabel('Year',fontsize = 15 )
plt.ylabel('GtCO2', fontsize = 15)
plt.title('Cumulative Emissions from Power Sector', fontsize=25, pad=60)
plt.text(0.5, 1.09, 'Projections are based on current power plants in operation', transform=ax.transAxes, ha='center', fontsize=14)
plt.text(0.5, 1.05, 'NGFS GCAM6 model\'s growth rates are applied for projections; Scenario: Net Zero 2050', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.01, 'Carbon budget range represents 50%-67% likelyhood for global warming', transform=ax.transAxes, ha='center', fontsize=12)

plt.legend(fontsize = 15)
plt.show()





# -------------------
### CURRENT POLICY 
# Plot 4.3 --- the annual emissions
plt.figure(figsize=(12, 8))

for scenario in df_growth_secondary_currentpolicy_bydev_annual['development_level'].unique():
    plt.plot(year_columns50, df_growth_secondary_currentpolicy_bydev_annual[df_growth_secondary_currentpolicy_bydev_annual['development_level'] == scenario][year_columns50].values[0], label=scenario)

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Add a vertical red line at 2050
#plt.axvline(x='2050', color='red', linestyle='--', linewidth=2, label='GCAM projection limit')

# Add horizontal grid lines
plt.grid(axis='both', which='both', linestyle='--', linewidth=0.7)

# Set y-axis limits
plt.ylim(0, 12000)

# Formatter function to convert values to thousands
def thousands_formatter(x, pos):
    return f'{int(x/1000)}'    # the values are in Mt, but diving the axis by 1000 to show in Gt

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

plt.xlabel('Year',fontsize = 15 )
plt.ylabel('GtCO2', fontsize = 15)
plt.title('Annual Emissions from Power Sector', fontsize=25, pad=50)
plt.text(0.5, 1.05, 'Projections are based on current power plants in operation', transform=ax.transAxes, ha='center', fontsize=14)
plt.text(0.5, 1.01, 'NGFS GCAM6 model\'s growth rates are applied for projections; Scenario: Current Policies', transform=ax.transAxes, ha='center', fontsize=12)

plt.legend(fontsize = 15)
plt.show()





# -------------------
# Plot 4.4 --- the cumulative emissions
plt.figure(figsize=(12, 8))

# Prepare the data for stackplot
scenarios = df_growth_secondary_currentpolicy_bydev_cumulative['development_level'].unique()
values = [
    df_growth_secondary_currentpolicy_bydev_cumulative[
        df_growth_secondary_currentpolicy_bydev_cumulative['development_level'] == scenario
    ][year_columns50].values[0]
    for scenario in scenarios
]

# Plot the stacked area chart
plt.stackplot(year_columns50, values, labels=scenarios)

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Add a vertical red line at 2050
#plt.axvline(x='2050', color='red', linestyle='--', linewidth=2, label='GCAM projection limit')

# Add horizontal grid lines
plt.grid(axis='both', which='both', linestyle='--', linewidth=0.7)

# Set y-axis limits
plt.ylim(0, 400000)

# Formatter function to convert values to thousands
def thousands_formatter(x, pos):
    return f'{int(x/1000)}'    # the values are in Mt, but diving the axis by 1000 to show in Gt

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Add a shaded region between 400 and 580 on the y-axis
plt.axhspan(258000, 358000, color='#d4e157', alpha=0.5)
plt.text(5, 300000, 'Carbon budget: 1.5°C warming', color='black', fontsize=15, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5))

plt.xlabel('Year',fontsize = 15 )
plt.ylabel('GtCO2', fontsize = 15)
plt.title('Cumulative Emissions from Power Sector', fontsize=25, pad=60)
plt.text(0.5, 1.09, 'Projections are based on current power plants in operation', transform=ax.transAxes, ha='center', fontsize=14)
plt.text(0.5, 1.05, 'NGFS GCAM6 model\'s growth rates are applied for projections; Scenario: Current Policies', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.01, 'Carbon budget range represents 50%-67% likelyhood for global warming', transform=ax.transAxes, ha='center', fontsize=12)

plt.legend(fontsize = 15)
plt.show()










# In[8]:

##################################################################################################
##################### SECTION 5: BY TOP 15 VS CARBON BUDGET ######################################
##################################################################################################

# set colors
colors = cm.get_cmap('tab20', 16).colors


# -------------------
### NET ZERO  
# Plot 5.1 --- the annual emissions
plt.figure(figsize=(12, 8))

# Iterate over each scenario and plot with different colors
for i, scenario in enumerate(df_top15_netzero_annual['Country'].unique()):
    plt.plot(
        year_columns50, 
        df_top15_netzero_annual[df_top15_netzero_annual['Country'] == scenario][year_columns50].values[0], 
        label=scenario,
        color=colors[i]  # Use the i-th color from the color map
    )


# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Add a vertical red line at 2050
#plt.axvline(x='2050', color='red', linestyle='--', linewidth=2, label='GCAM projection limit')

# Add horizontal grid lines
plt.grid(axis='both', which='both', linestyle='--', linewidth=0.7)

# Set y-axis limits
plt.ylim(0, 6000)

# Formatter function to convert values to thousands
def thousands_formatter(x, pos):
    return f'{int(x/1000)}'    # the values are in Mt, but diving the axis by 1000 to show in Gt

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

plt.xlabel('Year',fontsize = 15 )
plt.ylabel('GtCO2', fontsize = 15)
plt.title('Annual Emissions from Power Sector', fontsize=25, pad=50)
plt.text(0.5, 1.05, 'Projections are based on current power plants in operation', transform=ax.transAxes, ha='center', fontsize=14)
plt.text(0.5, 1.01, 'NGFS GCAM6 model\'s growth rates are applied for projections; Scenario: Net Zero 2050', transform=ax.transAxes, ha='center', fontsize=12)

plt.legend(fontsize = 10)
plt.show()





# -------------------
# Plot 5.2 --- the cumulative emissions
plt.figure(figsize=(12, 8))

# Prepare the data for stackplot
scenarios = df_top15_netzero_cumulative['Country'].unique()
values = [
    df_top15_netzero_cumulative[
        df_top15_netzero_cumulative['Country'] == scenario
    ][year_columns50].values[0]
    for scenario in scenarios
]


# Plot the stacked area chart
plt.stackplot(year_columns50, values, labels=scenarios, colors=colors)

    
# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Add a vertical red line at 2050
#plt.axvline(x='2050', color='red', linestyle='--', linewidth=2, label='GCAM projection limit')

# Add horizontal grid lines
plt.grid(axis='both', which='both', linestyle='--', linewidth=0.7)

# Set y-axis limits
plt.ylim(0, 400000)

# Formatter function to convert values to thousands
def thousands_formatter(x, pos):
    return f'{int(x/1000)}'    # the values are in Mt, but diving the axis by 1000 to show in Gt

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Add a shaded region between 400 and 580 on the y-axis
plt.axhspan(258000, 358000, color='#d4e157', alpha=0.5)
plt.text(5, 300000, 'Carbon budget: 1.5°C warming', color='black', fontsize=15, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5))


plt.xlabel('Year',fontsize = 15 )
plt.ylabel('GtCO2', fontsize = 15)
plt.title('Cumulative Emissions from Power Sector', fontsize=25, pad=60)
plt.text(0.5, 1.09, 'Projections are based on current power plants in operation', transform=ax.transAxes, ha='center', fontsize=14)
plt.text(0.5, 1.05, 'NGFS GCAM6 model\'s growth rates are applied for projections; Scenario: Net Zero 2050', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.01, 'Carbon budget range represents 50%-67% likelyhood for global warming', transform=ax.transAxes, ha='center', fontsize=12)


plt.legend(fontsize = 10, loc = 'upper right')
plt.show()





# -------------------
### CURRENT POLICY  
# Plot 5.3 --- the annual emissions
plt.figure(figsize=(12, 8))

# Iterate over each scenario and plot with different colors
for i, scenario in enumerate(df_top15_currentpolicy_annual['Country'].unique()):
    plt.plot(
        year_columns50, 
        df_top15_currentpolicy_annual[df_top15_currentpolicy_annual['Country'] == scenario][year_columns50].values[0], 
        label=scenario,
        color=colors[i]  # Use the i-th color from the color map
    )


# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Add a vertical red line at 2050
#plt.axvline(x='2050', color='red', linestyle='--', linewidth=2, label='GCAM projection limit')

# Add horizontal grid lines
plt.grid(axis='both', which='both', linestyle='--', linewidth=0.7)

# Set y-axis limits
plt.ylim(0, 6000)

# Formatter function to convert values to thousands
def thousands_formatter(x, pos):
    return f'{int(x/1000)}'    # the values are in Mt, but diving the axis by 1000 to show in Gt

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

plt.xlabel('Year',fontsize = 15 )
plt.ylabel('GtCO2', fontsize = 15)
plt.title('Annual Emissions from Power Sector', fontsize=25, pad=50)
plt.text(0.5, 1.05, 'Projections are based on current power plants in operation', transform=ax.transAxes, ha='center', fontsize=14)
plt.text(0.5, 1.01, 'NGFS GCAM6 model\'s growth rates are applied for projections; Scenario: Current Policies', transform=ax.transAxes, ha='center', fontsize=12)

plt.legend(fontsize = 10)
plt.show()





# -------------------
# Plot 5.4 --- the cumulative emissions
plt.figure(figsize=(12, 8))

# Prepare the data for stackplot
scenarios = df_top15_currentpolicy_cumulative['Country'].unique()
values = [
    df_top15_currentpolicy_cumulative[
        df_top15_currentpolicy_cumulative['Country'] == scenario
    ][year_columns50].values[0]
    for scenario in scenarios
]


# Plot the stacked area chart
plt.stackplot(year_columns50, values, labels=scenarios, colors=colors)

    
# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Add a vertical red line at 2050
#plt.axvline(x='2050', color='red', linestyle='--', linewidth=2, label='GCAM projection limit')

# Add horizontal grid lines
plt.grid(axis='both', which='both', linestyle='--', linewidth=0.7)

# Set y-axis limits
plt.ylim(0, 400000)

# Formatter function to convert values to thousands
def thousands_formatter(x, pos):
    return f'{int(x/1000)}'    # the values are in Mt, but diving the axis by 1000 to show in Gt

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Add a shaded region between 400 and 580 on the y-axis
plt.axhspan(258000, 358000, color='#d4e157', alpha=0.5)
plt.text(12, 300000, 'Carbon budget: 1.5°C warming', color='black', fontsize=15, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5))


plt.xlabel('Year',fontsize = 15 )
plt.ylabel('GtCO2', fontsize = 15)
plt.title('Cumulative Emissions from Power Sector', fontsize=25, pad=60)
plt.text(0.5, 1.09, 'Projections are based on current power plants in operation', transform=ax.transAxes, ha='center', fontsize=14)
plt.text(0.5, 1.05, 'NGFS GCAM6 model\'s growth rates are applied for projections; Scenario: Current Policies', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.01, 'Carbon budget range represents 50%-67% likelyhood for global warming', transform=ax.transAxes, ha='center', fontsize=12)


plt.legend(fontsize = 10, loc = 'upper left')
plt.show()










# In[]

del ax, i, fig, indices, line, modeled_data, real_data, region_to_country, scenario, scenarios, width, values










# In[6]: # EXPORT DATA
######################################

# growth dataset 
df_growth_secondary.to_excel('2 - output/script 3.1/1.1 - Secondary - emissions FA - projection.xlsx', index=False)
df_growth_secondary_change.to_excel('2 - output/script 3.1/1.2 - Secondary - emissions FA - change.xlsx', index=False)
df_ngfs_emissions_secondary.to_excel('2 - output/script 3.1/1.3 - Secondary - emissions NGFS - projection.xlsx', index=False)


# by scenario
df_growth_secondary_byscenario_annual.to_excel('2 - output/script 3.1/2.1 - Secondary - by scenario - annual.xlsx', index=False)
df_growth_secondary_byscenario_cumulative.to_excel('2 - output/script 3.1/2.2 - Secondary - by scenario - cumulative.xlsx', index=False)

# by netzero - annual
df_growth_secondary_netzero_byfueltype_annual.to_excel('2 - output/script 3.1/3.1 - Secondary - netzero - annual - fueltype.xlsx', index=False)
df_growth_secondary_netzero_byregion_annual.to_excel('2 - output/script 3.1/3.2 - Secondary - netzero - annual - regions.xlsx', index=False)
df_growth_secondary_netzero_bydev_annual.to_excel('2 - output/script 3.1/3.3 - Secondary - netzero - annual - development.xlsx', index=False)
df_growth_secondary_netzero_bycountry_annual.to_excel('2 - output/script 3.1/3.4 - Secondary - netzero - annual - country.xlsx', index=False)

# by netzero - cumulative
df_growth_secondary_netzero_byfueltype_cumulative.to_excel('2 - output/script 3.1/4.1 - Secondary - netzero - cumulative - fueltype.xlsx', index=False)
df_growth_secondary_netzero_byregion_cumulative.to_excel('2 - output/script 3.1/4.2 - Secondary - netzero - cumulative - regions.xlsx', index=False)
df_growth_secondary_netzero_bydev_cumulative.to_excel('2 - output/script 3.1/4.3 - Secondary - netzero - cumulative - development.xlsx', index=False)
df_growth_secondary_netzero_bycountry_cumulative.to_excel('2 - output/script 3.1/4.4 - Secondary - netzero - cumulative - country.xlsx', index=False)

# by current policy - annual
df_growth_secondary_currentpolicy_byfueltype_annual.to_excel('2 - output/script 3.1/5.1 - Secondary - currentpolicy - annual - fueltype.xlsx', index=False)
df_growth_secondary_currentpolicy_byregion_annual.to_excel('2 - output/script 3.1/5.2 - Secondary - currentpolicy - annual - regions.xlsx', index=False)
df_growth_secondary_currentpolicy_bydev_annual.to_excel('2 - output/script 3.1/5.3 - Secondary - currentpolicy - annual - development.xlsx', index=False)
df_growth_secondary_currentpolicy_bycountry_annual.to_excel('2 - output/script 3.1/5.4 - Secondary - currentpolicy - annual - country.xlsx', index=False)

# by current policy - cumulative
df_growth_secondary_currentpolicy_byfueltype_cumulative.to_excel('2 - output/script 3.1/6.1 - Secondary - currentpolicy - cumulative - fueltype.xlsx', index=False)
df_growth_secondary_currentpolicy_byregion_cumulative.to_excel('2 - output/script 3.1/6.2 - Secondary - currentpolicy - cumulative - regions.xlsx', index=False)
df_growth_secondary_currentpolicy_bydev_cumulative.to_excel('2 - output/script 3.1/6.3 - Secondary - currentpolicy - cumulative - development.xlsx', index=False)
df_growth_secondary_currentpolicy_bycountry_cumulative.to_excel('2 - output/script 3.1/6.4 - Secondary - currentpolicy - cumulative - country.xlsx', index=False)

# countries 
df_merged_countries_raw.to_excel('2 - output/script 3.1/7.1 - Merged countries - raw.xlsx', index=False)
df_merged_countries_edited.to_excel('2 - output/script 3.1/7.2 - Merged countries - formatted.xlsx', index=False)





