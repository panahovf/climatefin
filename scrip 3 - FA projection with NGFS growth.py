# In[1]:
# Date: July 28, 2024
# Project: Applying NGFS trends to FA data
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



# In[3]: LOADING DATA
##################################################
# directory & load data

directory = r'C:\Users\panah\OneDrive\Desktop\Work\2 - RA - Climate fin'
os.chdir(directory)
del directory


# --------------
# load oil & gas
df_power = pd.read_csv('1 - input/v3_power_Forward_Analytics2024.csv')   
df_power = df_power[df_power['status'] == "operating"]

df_growth = pd.read_excel('2 - output/script 2/1.3 - GCAM - percent change.xlsx')


# ------------------------------------
# load NGFS secondary energy scenarios
df_ngfs_scenarios_cumulative = pd.read_excel('2 - output/script 2/4.2 - GCAM - emissions - scenarios - secondary - cumulative.xlsx')
df_ngfs_emissions = pd.read_excel('2 - output/script 2/1.2 - GCAM - filtered - emissions.xlsx')


# ----------------------------
# load market and region datasets
df_developed = pd.read_excel('2 - output/script a - country codes/1 - developed.xlsx')
df_developing = pd.read_excel('2 - output/script a - country codes/2 - developing.xlsx')
df_emerging = pd.read_excel('2 - output/script a - country codes/3 - emerging.xlsx')
df_regions = pd.read_excel('1 - input/Country Datasets/country_gca_region.xlsx')



# In[]: SET THE REGIONS AND DDEVELOPMENT LEVELS
###############################################

df_growth_secondary = pd.merge(df_growth_secondary,
                             df_regions[['alpha-3', 'gca_region']],
                             left_on='Region',
                             right_on='alpha-3',
                             how='left')
    

    
    
# In[4]: GET POWER BY SOURCE FOR MAPPING BASED ON SOURCE AND COUNTRY
####################################################################
# subset power plants by source

#coal
df_power_coal = df_power[df_power['subsector'] == 'Coal']
df_power_coal = df_power_coal.groupby(['countryiso3'])['annual_co2_calc'].sum()
df_power_coal = df_power_coal.reset_index()


#gas
df_power_gas = df_power[df_power['subsector'] == 'Gas']
df_power_gas = df_power_gas.groupby(['countryiso3'])['annual_co2_calc'].sum()
df_power_gas = df_power_gas.reset_index()


#oil
df_power_oil = df_power[df_power['subsector'] == 'Oil']
df_power_oil = df_power_oil.groupby(['countryiso3'])['annual_co2_calc'].sum()
df_power_oil = df_power_oil.reset_index()


# subset growth to secondary only & remove 2020-2023 years --- i.e start from 2024
df_growth_secondary = df_growth[df_growth['Variable'].str.contains('Secondary')]
df_growth_secondary= df_growth_secondary.drop(columns = ['2020', '2021', '2022', '2023']) # removing 2020-2023
df_growth_secondary['2024'] = 0 # set all 2024 values to zero --- these will be filled by FA data



# In[]: CHECK FOR COUNTRIES ACROSS BOTH DATASETS
###################################################

# get list of NGFS countries
df_ngfs_countries = df_ngfs_emissions[df_ngfs_emissions['Scenario'] == 'Current Policies']
df_ngfs_countries = df_ngfs_countries[df_ngfs_countries['Variable'].str.contains('Secondary')]
df_ngfs_countries = df_ngfs_countries[['Region', 'Variable', '2024']]

df_ngfs_countries = df_ngfs_countries.pivot(index='Region', columns='Variable', values='2024')
df_ngfs_countries.reset_index(inplace = True)


# Get list of FA countries
df_fa_countries = df_power[['countryiso3']].drop_duplicates()
df_fa_countries.reset_index(drop=True, inplace = True)


# get FA data in to countries
df_fa_countries = pd.merge(df_fa_countries,df_power_coal,
                           on='countryiso3',
                           how='left')

df_fa_countries = pd.merge(df_fa_countries,df_power_gas,
                           on='countryiso3',
                           how='left')

df_fa_countries = pd.merge(df_fa_countries,df_power_oil,
                           on='countryiso3',
                           how='left')


# merge with NGFS data
df_merged_countries = pd.merge(df_fa_countries, df_ngfs_countries,
                               left_on='countryiso3',
                               right_on='Region',
                               how='outer')


# In[]: USE MAPPING TO ADD EMISSSONS VALUES TO YEAR 2024 BACK TO MASTER DATA
############################################################################
# Get power values added to 2020 of growth dataframe

# coal
# Step 1: Filter to include only rows where 'Variable' contains "coal"
df_growth_secondary_coal = df_growth_secondary[df_growth_secondary['Variable'].str.contains('Coal')]

# Step 2: Create a mapping Series
co2_mapping = df_power_coal.set_index('countryiso3')['annual_co2_calc']

# Step 3: Map and substitute values in the '2020' column for the filtered DataFrame
df_growth_secondary_coal['2024'] = df_growth_secondary_coal['Region'].map(co2_mapping)

# Step 4: Update the original DataFrame
df_growth_secondary.update(df_growth_secondary_coal)


# gas
df_growth_secondary_gas = df_growth_secondary[df_growth_secondary['Variable'].str.contains('Gas')]
co2_mapping = df_power_gas.set_index('countryiso3')['annual_co2_calc']
df_growth_secondary_gas['2024'] = df_growth_secondary_gas['Region'].map(co2_mapping)
df_growth_secondary.update(df_growth_secondary_gas)


# oil
df_growth_secondary_oil = df_growth_secondary[df_growth_secondary['Variable'].str.contains('Oil')]
co2_mapping = df_power_oil.set_index('countryiso3')['annual_co2_calc']
df_growth_secondary_oil['2024'] = df_growth_secondary_oil['Region'].map(co2_mapping)
df_growth_secondary.update(df_growth_secondary_oil)


del co2_mapping, df_growth_secondary_coal, df_growth_secondary_gas, df_growth_secondary_oil
del df_power_coal, df_power_oil, df_power_gas



# In[5]: PROJECT THE GROWTH TO ANNUAL EMISSIOSN
###############################################
# after this we get dataframe for secondary energy by source/country/scenario with annual emissions values

# create a loop to go through each year column
year_columns = [str(year) for year in range(2024, 2101)]
df_growth_secondary.replace([np.inf, -np.inf], 0, inplace=True) # there are some 'inf values --- replacing them with 0


for i in range(1, len(year_columns)):
    previous_year = year_columns[i - 1]  # Get the previous year
    current_year = year_columns[i]       # Get the current year
    # Update the current year's values based on the previous year
    df_growth_secondary[current_year] = df_growth_secondary[previous_year] * (1 + df_growth_secondary[current_year] / 100)


del i, current_year, previous_year, year_columns



# In[6]: NOW SLICE AND DICE THE DATA: by fuel type, region, develoment, etc.
# WE GET THESE BOTH ANNUAL AND CUMULATIVE
############################################################################
# set years 2024-2050    
year_columns = [str(year) for year in range(2024, 2051)]


# 1 --- SCENARIO:
# annual
df_growth_secondary_byscenario_annual = df_growth_secondary.groupby(['Scenario'])[year_columns].sum()
df_growth_secondary_byscenario_annual.reset_index(inplace=True)

# cumulative
df_growth_secondary_byscenario_cumulative = df_growth_secondary_byscenario_annual.copy()
df_growth_secondary_byscenario_cumulative[year_columns] = df_growth_secondary_byscenario_cumulative[year_columns].cumsum(axis=1)
df_growth_secondary_byscenario_cumulative.reset_index(inplace=True)



# 2 --- FUEL TYPE
### net zero
# annual
df_growth_secondary_byfueltype_annual = df_growth_secondary.groupby(['Variable'])[year_columns].sum()
df_growth_secondary_byfueltype_annual.reset_index(inplace=True)

# cumulative
df_growth_secondary_byfueltype_cumulative = df_growth_secondary_byfueltype_annual.copy()
df_growth_secondary_byfueltype_cumulative[year_columns] = df_growth_secondary_byfueltype_cumulative[year_columns].cumsum(axis=1)
df_growth_secondary_byfueltype_cumulative.reset_index(inplace=True) 



# 3 --- 


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
########## PLOTS PLOTS PLOTS PLOTS PLOTS PLOTS PLOTS ################
#####################################################################
#####################################################################



# In[8]:

##################################################################################################
##################### SECTION 1: BY SCENARIO VS CARBON BUDGET ####################################
##################################################################################################

  
# Plot 1 --- the cumulative emissions
plt.figure(figsize=(12, 8))

for scenario in df_growth_secondary_byscenario_cumulative['Scenario'].unique():
    plt.plot(year_columns, df_growth_secondary_byscenario_cumulative[df_growth_secondary_byscenario_cumulative['Scenario'] == scenario][year_columns].values[0], label=scenario)

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




# Plot 2 --- FA vs NGFS 2050
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





# In[6]:
# Export data

df_country_CO2factor_coal.to_excel('2 - output/script 1/1 - country_power_co2factor_coal.xlsx', index=False)
df_country_CO2factor_oil.to_excel('2 - output/script 1/2 - country_power_co2factor_oil.xlsx', index=False)
df_country_CO2factor_gas.to_excel('2 - output/script 1/3 - country_power_co2factor_gas.xlsx', index=False)






