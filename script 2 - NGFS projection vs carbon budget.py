# In[1]:
# Date: July 22, 2024
# Project: NGFS emissions projections vs Carbon Budget
# Author: Farhad Panahov




# Task #1: The datapoints are provided in 5 year intervals, ending in 2050
#   - Iterpolate linear trend line
#   - Obtain YoY % change 




# Task #2: For Secondary Energy
# I am using FA data to identify country specific emissions intensity values. 
# Oil and Gas are constant. Coal has some variation across countries
# We follow following formula:
# Alissa Kleinnijenhuis: annual CO2 (in million tonnes) = capacity * capacity factor * heat rate (in Btu per kWh) * emission factor (kg of CO2 per TJ) * 9.2427 x 10^-12
# Prevous script gets a product of 'heat rate' and 'emissinos factor' (weighted for counties by activity)
# Here below we incorporate chaging EJ to MWh, and then MWh to Capacity X Capacity Factor
# MWh is C X CF over 24 hours and 365 days





# Task #3: For Primary Energy convert units and values to emissions
#   - Change EJ/year to emissions 

# COAL
# https://www.convertunits.com/from/EJ/to/tonne+of+coal+equivalent
# https://www.eia.gov/environment/emissions/co2_vol_mass.php
# 1 EJ to tonne of coal equivalent = 34120842.37536 tonne of coal equivalent = 34.1208423754 million tonnes of coal; 
# 1 tonne of coal = 1.10231 short ton
# 1764.83 kgCO2 per short ton

#OIL
# https://www.epa.gov/energy/greenhouse-gases-equivalencies-calculator-calculations-and-references
# 1 EJ = 163452108.5322 barrel of oil (BOE) = 163.4521085322 million barrels; 
# 0.43 metric tons CO2/barrel

#NG
# https://www.enbridgegas.com/ontario/business-industrial/incentives-conservation/energy-calculators/Greenhouse-Gas-Emissions#:~:text=It%20is%20also%20assumed%20that,2%2C%20page%20254%2D255.
# https://www.eia.gov/environment/emissions/co2_vol_mass.php
# 1 EJ = 27.93 billion cubic meters of natural gas
# 1 m3 = 1.932 kg CO2




# Task #4: Compare emissions globally to carbon budget
#   - Carbon budget is 400-580 Gt CO2 (https://www.ipcc.ch/sr15/chapter/chapter-2/)
#   - "This assessment suggests a remaining budget of about 420 GtCO2 for a two-thirds chance of limiting warming to 1.5°C, and of about 580 GtCO2 for an even chance"

 

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
df_gcam = pd.read_excel('1 - input/Downscaled_GCAM 6.0 NGFS_data.xlsx')      #input the name of the Excel file


# ----------------------------
# load country power sector OIL&GAS and COAL emissions intensity data
# original intensity is given in million tonnes of CO2 per MWh; this section already converts it from MWh to EJ by multiplying to 277777777.778

# https://www.convertunits.com/from/EJ/to/MWh
# coal
co2_factor_coal = pd.read_excel('2 - output/script 1/1 - country_power_co2factor_coal.xlsx')
co2_factor_coal.columns = ['Region', 'factor']
co2_factor_coal['factor'] = co2_factor_coal['factor'] * (277777777.778) 

# oil
co2_factor_oil = pd.read_excel('2 - output/script 1/2 - country_power_co2factor_oil.xlsx')
co2_factor_oil.columns = ['Region', 'factor']
co2_factor_oil['factor'] = co2_factor_oil['factor'] * (277777777.778)

# gas
co2_factor_gas = pd.read_excel('2 - output/script 1/3 - country_power_co2factor_gas.xlsx')
co2_factor_gas.columns = ['Region', 'factor']
co2_factor_gas['factor'] = co2_factor_gas['factor'] * (277777777.778)


# ----------------------------
# load market and region datasets
df_regions = pd.read_excel('1 - input/Country Datasets/country_gca_region.xlsx')



# In[5]: Task #1: The datapoints are provided in 5 year intervals, ending in 2050
#################################################################################
#   - Iterpolate linear trend line
#   - Obtain YoY % change 

# filter
df_gcam_filtered = df_gcam.loc[(df_gcam['Variable'] == 'Primary Energy|Gas') |  (df_gcam['Variable'] == 'Primary Energy|Oil')| (df_gcam['Variable'] == 'Primary Energy|Coal')| (df_gcam['Variable'] == 'Secondary Energy|Electricity|Coal')| (df_gcam['Variable'] == 'Secondary Energy|Electricity|Gas')|(df_gcam['Variable'] == 'Secondary Energy|Electricity|Oil')]


# Interpolate the NaN values in the specific columns
years = [str(year) for year in range(2020, 2101)]
df_gcam_filtered[years] = df_gcam_filtered[years].interpolate(method='linear', axis=1)
df_gcam_years = df_gcam_filtered[years]
    

# Calculate yearly percent change for each row
pct_change_df = df_gcam_years.pct_change(axis=1) * 100
pct_change_df = pct_change_df.fillna(0)
del df_gcam_years, years


#First concatenate extrapolated data with filtered data frame
first_5_columns = df_gcam_filtered.iloc[:, :5]
df_gcam_change = pd.concat([first_5_columns, pct_change_df], axis=1)
del first_5_columns, pct_change_df



# In[6]: Task #2: For Secondary Energy - use country specific emissions factors to get GHG levels
####################################################################################################

# get list of countries for coal and oilgas secondary energy
gcam_countries = df_gcam_filtered.loc[(df_gcam['Variable'] == 'Secondary Energy|Electricity|Gas')|(df_gcam['Variable'] == 'Secondary Energy|Electricity|Oil')| (df_gcam['Variable'] == 'Secondary Energy|Electricity|Coal')]
gcam_countries = gcam_countries[['Region']].drop_duplicates()


# create a single GCAM country dataframe with emissions intensity factors for power sector
gcam_countries = gcam_countries.merge(co2_factor_coal, on='Region', how='left')
gcam_countries = gcam_countries.merge(co2_factor_oil, on='Region', how='left')
gcam_countries = gcam_countries.merge(co2_factor_gas, on='Region', how='left')
gcam_countries.columns = ['Region', 'coal','oil','gas']


# set average factors to countries with no actual values in FA data
gcam_countries['coal'].fillna(value=gcam_countries['coal'].mean(), inplace=True)
gcam_countries['oil'].fillna(value=gcam_countries['oil'].mean(), inplace=True)
gcam_countries['gas'].fillna(value=gcam_countries['gas'].mean(), inplace=True)



# In[7]:
# Convert secondary energy to emissions

# get copy dataframe
df_gcam_emissions = df_gcam_filtered.copy()


# Create Country X Factor dictionary for matching countries
emissions_factor_coal = gcam_countries.set_index('Region')['coal'].to_dict()
emissions_factor_gas = gcam_countries.set_index('Region')['gas'].to_dict()
emissions_factor_oil = gcam_countries.set_index('Region')['oil'].to_dict()


# Process each row in df_gcam_emissions
for index, row in df_gcam_emissions.iterrows():
    # Determine the factor based on the Variable and Region
    if row['Variable'] == 'Secondary Energy|Electricity|Coal':
        factor = emissions_factor_coal.get(row['Region'])  
    elif row['Variable'] == 'Secondary Energy|Electricity|Gas':
        factor = emissions_factor_gas.get(row['Region'])
    elif row['Variable'] == 'Secondary Energy|Electricity|Oil':
        factor = emissions_factor_oil.get(row['Region'])
    else:
        factor = 1  # If none of the conditions match, no multiplication is done

    # Apply the factor to the yearly columns and update the unit
    if factor != 1:  # Only apply if the factor is found and relevant
        df_gcam_emissions.loc[index, df_gcam_emissions.columns[5:]] *= factor
        df_gcam_emissions.loc[index, 'Unit'] = 'MtCO2'


del factor, index, row, co2_factor_coal, co2_factor_oil, co2_factor_gas
del emissions_factor_gas, emissions_factor_oil, emissions_factor_coal



# In[8]: # Task #3: For Primary Energy convert units and values to emissions
############################################################################

# Convert primary energy to emissions    
    
# Define the constant to multiply for unit conversion
emissions_factor_coal = 34120842.37536*1.10231*1764.83 / 10**3 / 10**6    #EJ to Tonne to Short Ton to KgCO2 to tCO2 to MtCO2 --- final unit: MtCO2
emissions_factor_oil = 163452108.5322*0.43 / 10**6                       #EJ to barrel to tCO2 to Mt --- final unit: MtCO2
emissions_factor_gas = 27.93*10**9*1.932 / 10**3 / 10**6                  #EJ to million cubic meters of natural gas to tCO2 to Mt --- final unit: MtCO2


# Iterate over the DataFrame 
for index, row in df_gcam_emissions.iterrows():
  
    if row['Variable'] == 'Primary Energy|Coal':
        #print(row)
        df_gcam_emissions.loc[index, df_gcam_emissions.columns[5:]] *= emissions_factor_coal      #Multiply columns starting from Year 2020
        df_gcam_emissions.loc[index, 'Unit'] = 'MtCO2'                                             # Change the unit    
    
    if row['Variable'] == 'Primary Energy|Gas':
        #print(row)
        df_gcam_emissions.loc[index, df_gcam_emissions.columns[5:]] *= emissions_factor_gas       #Multiply columns starting from column 6
        df_gcam_emissions.loc[index, 'Unit'] = 'MtCO2'           # Change the value in column 5

    if row['Variable'] == 'Primary Energy|Oil':
        #print(row)
        df_gcam_emissions.loc[index, df_gcam_emissions.columns[5:]] *= emissions_factor_oil       #Multiply columns starting from Year 2020
        df_gcam_emissions.loc[index, 'Unit'] = 'MtCO2'                         # Change the unit    


del index, row
del emissions_factor_gas, emissions_factor_oil, emissions_factor_coal



# In[9]: GET REGIONS, FUEL TYPE
##################################################

# set years 2024-2050    
year_columns = [str(year) for year in range(2024, 2051)]


# 1 --- PRIMARY vs SECONDARY BY SCENARIO
########################################

# get by scenario & energy type (primary vs secondary)
df_emissions_global_byscenario = df_gcam_emissions.groupby(['Scenario', 'Variable'])[year_columns].sum()
df_emissions_global_byscenario.reset_index(inplace=True)


# primary
df_emissions_global_byscenario_primary = df_emissions_global_byscenario[df_emissions_global_byscenario['Variable'].str.contains('Primary')]
df_emissions_global_byscenario_primary = df_emissions_global_byscenario_primary.groupby(['Scenario'])[year_columns].sum()
df_emissions_global_byscenario_primary = df_emissions_global_byscenario_primary.reset_index()


# secondary
df_emissions_global_byscenario_secondary = df_emissions_global_byscenario[df_emissions_global_byscenario['Variable'].str.contains('Secondary')]
df_emissions_global_byscenario_secondary = df_emissions_global_byscenario_secondary.groupby(['Scenario'])[year_columns].sum()
df_emissions_global_byscenario_secondary = df_emissions_global_byscenario_secondary.reset_index()





# 2 --- BY REGIONS AND SCENARIO --- FOR PRIMARY AND SECONDARY
# get the regions & create 4 dataframes for scenarios
df_emissions_byregion = df_gcam_emissions.copy()      # create a new dataframe
df_emissions_byregion = pd.merge(df_emissions_byregion,
                             df_regions[['alpha-3', 'gca_region']],
                             left_on='Region',
                             right_on='alpha-3',
                             how='left')        # get the region names

df_emissions_byregion['gca_region'] = df_emissions_byregion['gca_region'].fillna('Other')


# regions by scenarios
df_emissions_byregion_currentpolicy = df_emissions_byregion[df_emissions_byregion['Scenario'] == 'Current Policies'].groupby(['gca_region','Variable'])[year_columns].sum()
df_emissions_byregion_netzero = df_emissions_byregion[df_emissions_byregion['Scenario'] == 'Net Zero 2050'].groupby(['gca_region','Variable'])[year_columns].sum()
df_emissions_byregion_below2 = df_emissions_byregion[df_emissions_byregion['Scenario'] == 'Below 2°C'].groupby(['gca_region','Variable'])[year_columns].sum()
df_emissions_byregion_ndc = df_emissions_byregion[df_emissions_byregion['Scenario'] == 'Nationally Determined Contributions (NDCs)'].groupby(['gca_region','Variable'])[year_columns].sum()


# reginos by scenario by primary vs secondary
df_emissions_byregion_currentpolicy.reset_index(inplace=True)
df_emissions_byregion_currentpolicy_primary = df_emissions_byregion_currentpolicy[df_emissions_byregion_currentpolicy['Variable'].str.contains('Primary')]
df_emissions_byregion_currentpolicy_secondary = df_emissions_byregion_currentpolicy[df_emissions_byregion_currentpolicy['Variable'].str.contains('Secondary')]

df_emissions_byregion_netzero.reset_index(inplace=True)
df_emissions_byregion_netzero_primary = df_emissions_byregion_netzero[df_emissions_byregion_netzero['Variable'].str.contains('Primary')]
df_emissions_byregion_netzero_secondary = df_emissions_byregion_netzero[df_emissions_byregion_netzero['Variable'].str.contains('Secondary')]

df_emissions_byregion_below2.reset_index(inplace=True)
df_emissions_byregion_below2_primary = df_emissions_byregion_below2[df_emissions_byregion_below2['Variable'].str.contains('Primary')]
df_emissions_byregion_below2_secondary = df_emissions_byregion_below2[df_emissions_byregion_below2['Variable'].str.contains('Secondary')]

df_emissions_byregion_ndc.reset_index(inplace=True)
df_emissions_byregion_ndc_primary = df_emissions_byregion_ndc[df_emissions_byregion_ndc['Variable'].str.contains('Primary')]
df_emissions_byregion_ndc_secondary = df_emissions_byregion_ndc[df_emissions_byregion_ndc['Variable'].str.contains('Secondary')]


del df_emissions_byregion_currentpolicy, df_emissions_byregion_netzero, df_emissions_byregion_below2, df_emissions_byregion_ndc



# In[12]: CUMULATIVE EMISSIONS
##############################

# 1 --- get cumulative by primary vs secondarry by scenario

# primary
df_emissions_global_byscenario_primary_cumulative = df_emissions_global_byscenario_primary.copy()
df_emissions_global_byscenario_primary_cumulative[year_columns] = df_emissions_global_byscenario_primary[year_columns].cumsum(axis=1)
df_emissions_global_byscenario_primary_cumulative = df_emissions_global_byscenario_primary_cumulative.reset_index()


# secondary
df_emissions_global_byscenario_secondary_cumulative = df_emissions_global_byscenario_secondary.copy()
df_emissions_global_byscenario_secondary_cumulative[year_columns] = df_emissions_global_byscenario_secondary[year_columns].cumsum(axis=1)
df_emissions_global_byscenario_secondary_cumulative = df_emissions_global_byscenario_secondary_cumulative.reset_index()




# 2 --- get cumulative by primary vs secondarry by scenario & REGIONS
# PRIMARY
# CurrentPolicy
df_emissions_byregion_currentpolicy_primary_cumulative = df_emissions_byregion_currentpolicy_primary.copy()
df_emissions_byregion_currentpolicy_primary_cumulative[year_columns] = df_emissions_byregion_currentpolicy_primary[year_columns].cumsum(axis=1)
df_emissions_byregion_currentpolicy_primary_cumulative = df_emissions_byregion_currentpolicy_primary_cumulative.reset_index()

# NetZero
df_emissions_byregion_netzero_primary_cumulative = df_emissions_byregion_netzero_primary.copy()
df_emissions_byregion_netzero_primary_cumulative[year_columns] = df_emissions_byregion_netzero_primary[year_columns].cumsum(axis=1)
df_emissions_byregion_netzero_primary_cumulative = df_emissions_byregion_netzero_primary_cumulative.reset_index()

# Below2
df_emissions_byregion_below2_primary_cumulative = df_emissions_byregion_below2_primary.copy()
df_emissions_byregion_below2_primary_cumulative[year_columns] = df_emissions_byregion_below2_primary[year_columns].cumsum(axis=1)
df_emissions_byregion_below2_primary_cumulative = df_emissions_byregion_below2_primary_cumulative.reset_index()

# NDC
df_emissions_byregion_ndc_primary_cumulative = df_emissions_byregion_ndc_primary.copy()
df_emissions_byregion_ndc_primary_cumulative[year_columns] = df_emissions_byregion_ndc_primary[year_columns].cumsum(axis=1)
df_emissions_byregion_ndc_primary_cumulative = df_emissions_byregion_ndc_primary_cumulative.reset_index()



# SECONDARY
# CurrentPolicy
df_emissions_byregion_currentpolicy_secondary_cumulative = df_emissions_byregion_currentpolicy_secondary.copy()
df_emissions_byregion_currentpolicy_secondary_cumulative[year_columns] = df_emissions_byregion_currentpolicy_secondary[year_columns].cumsum(axis=1)
df_emissions_byregion_currentpolicy_secondary_cumulative = df_emissions_byregion_currentpolicy_secondary_cumulative.reset_index()

# NetZero
df_emissions_byregion_netzero_secondary_cumulative = df_emissions_byregion_netzero_secondary.copy()
df_emissions_byregion_netzero_secondary_cumulative[year_columns] = df_emissions_byregion_netzero_secondary[year_columns].cumsum(axis=1)
df_emissions_byregion_netzero_secondary_cumulative = df_emissions_byregion_netzero_secondary_cumulative.reset_index()

# Below2
df_emissions_byregion_below2_secondary_cumulative = df_emissions_byregion_below2_secondary.copy()
df_emissions_byregion_below2_secondary_cumulative[year_columns] = df_emissions_byregion_below2_secondary[year_columns].cumsum(axis=1)
df_emissions_byregion_below2_secondary_cumulative = df_emissions_byregion_below2_secondary_cumulative.reset_index()

# NDC
df_emissions_byregion_ndc_secondary_cumulative = df_emissions_byregion_ndc_secondary.copy()
df_emissions_byregion_ndc_secondary_cumulative[year_columns] = df_emissions_byregion_ndc_secondary[year_columns].cumsum(axis=1)
df_emissions_byregion_ndc_secondary_cumulative = df_emissions_byregion_ndc_secondary_cumulative.reset_index()





# In[10]: Get overall emissions for 2020 for comparisons
########################################################

year_columns2 = [str(year) for year in range(2020, 2021)]
df_emissions_global_bysource = df_gcam_emissions[df_gcam_emissions['Scenario'] == 'Current Policies'].groupby(['Variable'])[year_columns2].sum()


# create a dataset with emissions from NGFS
df_gcam_ghg = df_gcam.loc[(df_gcam['Variable'] == 'Emissions|CO2')]
df_gcam_ghg_energy = df_gcam.loc[(df_gcam['Variable'] == 'Emissions|CO2|Energy')]

# estimates as given in NGFS dataset
df_gcam_ghg = df_gcam_ghg.groupby(['Scenario'])[year_columns2].sum()
df_gcam_ghg_energy = df_gcam_ghg_energy.groupby(['Scenario'])[year_columns2].sum()

# ghg total: 35901.2    & ghg energy 34989.8


# manual comparison dataframe
# Creating a DataFrame with specified rows and columns
# for secondary
# print(df_emissions_global_bysource)
df_comparison_secondary = {
    'NGFS': [10.490, 2.908, 0.652],  # Initial values for NGFS --- df_emissions_blobal_bysource above
    'Ford Analytics': [10.085, 3.41, 0.641]  # Initial values from Moritz
}

# Define the index for the rows corresponding to coal, oil, and gas
df_comparison_secondary = pd.DataFrame(df_comparison_secondary, index=['Coal', 'Gas', 'Oil'])


# for total energy
df_comparison_primary = {
    'NGFS': [10.984, 8.0908, 13.743],  # Initial values for NGFS
    'IEA': [14.308, 7.168, 10.307],     # IEA https://www.iea.org/data-and-statistics/data-tools/greenhouse-gas-emissions-from-energy-data-explorer
    'OWID':[14.23,7.56,10.9] # OurWorldInData https://ourworldindata.org/emissions-by-fuel
}

# Define the index for the rows corresponding to coal, oil, and gas
df_comparison_primary = pd.DataFrame(df_comparison_primary, index=['Coal', 'Gas', 'Oil'])


# for total emissions
df_comparison_total = {
    'GHG': [33.617,34.989, 35.901, 32.319, 35.01]  # Current policy primary energy = 33617.8 --- see df_global_byscenario_primary
     # IEA https://www.iea.org/data-and-statistics/data-tools/greenhouse-gas-emissions-from-energy-data-explorer
     # OurWorldInData https://ourworldindata.org/emissions-by-fuel
}

# Define the index for the rows corresponding to coal, oil, and gas
df_comparison_total = pd.DataFrame(df_comparison_total, index=['NGFS Primary Energy','NGFS Energy', 'NGFS Total', 'EIA Fuel Combustion', 'OWID Fossil Fuels'])


# for OIL/GAS/COAL emissions by regions
df_comparison_total_regions = {
    'NGFS Primary Energy': [1.125,18.783, 4.651, 4.857],  # Current policy primary energy --- see df_emissions_byregion_currentpolicy_primary)cumulative_REGION
    'OWID (Coal,Oil,Gas)': [1.276, 20.18, 4.85, 6.08 ] # only Oil, Coal, Gas: https://ourworldindata.org/emissions-by-fuel
}

# Define the index for the rows corresponding to coal, oil, and gas
df_comparison_total_regions = pd.DataFrame(df_comparison_total_regions, index=['Africa','Asia', 'Europe', 'North America'])





# In[11]


#####################################################################
#####################################################################
########## PLOTS PLOTS PLOTS PLOTS PLOTS PLOTS PLOTS ################
#####################################################################
#####################################################################



# In[8]:

##################################################################################################
##################### SECTION 1: PRIMARY & SECONDARY BY SCENARIO VS CARBON BUDGET ################
##################################################################################################

# Plot # 1 --- Primary
    
# Plot the cumulative emissions
plt.figure(figsize=(12, 8))

for scenario in df_emissions_global_byscenario_primary_cumulative['Scenario'].unique():
    plt.plot(year_columns, df_emissions_global_byscenario_primary_cumulative[df_emissions_global_byscenario_primary_cumulative['Scenario'] == scenario][year_columns].values[0],
             label=scenario)

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Add a vertical red line at 2050
#plt.axvline(x='2050', color='red', linestyle='--', linewidth=2, label='GCAM projection limit')

# Add horizontal grid lines
plt.grid(axis='both', which='both', linestyle='--', linewidth=0.7)

# Set y-axis limits
plt.ylim(0, 1000000)

# Formatter function to convert values to thousands
def thousands_formatter(x, pos):
    return f'{int(x/1000)}'    # the values are in Mt, but diving the axis by 1000 to show in Gt

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Add a shaded region between 400 and 580 on the y-axis
plt.axhspan(258000, 358000, color='#d4e157', alpha=0.5)
plt.text(1.5, 300000, '1.5°C warming', color='black', fontsize=12, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5))

# Add a shaded region between 400 and 580 on the y-axis
plt.axhspan(408000, 508000, color='orange', alpha=0.3)
plt.text(5, 450000, '1.6°C warming', color='black', fontsize=12, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5))

# Add a shaded region between 400 and 580 on the y-axis
plt.axhspan(558000, 708000, color='red', alpha=0.3)
plt.text(10, 625000, 'Carbon budget: 1.7°C warming', color='black', fontsize=12, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5))

plt.xlabel('Year')
plt.ylabel('GtCO2')
plt.title('Cumulative Emissions from Energy Sector', fontsize=20, pad=30)
plt.text(0.5, 1.01, 'NGFS GCAM 6 Model; Carbon budget ranges indicate 50%-67% likelyhood for limiting global warming', transform=ax.transAxes, ha='center', fontsize=10)

plt.legend()
plt.show()





# Plot # 2 --- Secondary
    
# Plot the cumulative emissions
plt.figure(figsize=(12, 8))

for scenario in df_emissions_global_byscenario_secondary_cumulative['Scenario'].unique():
    plt.plot(year_columns, df_emissions_global_byscenario_secondary_cumulative[df_emissions_global_byscenario_secondary_cumulative['Scenario'] == scenario][year_columns].values[0], label=scenario)

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Add a vertical red line at 2050
#plt.axvline(x='2050', color='red', linestyle='--', linewidth=2, label='GCAM projection limit')

# Add horizontal grid lines
plt.grid(axis='both', which='both', linestyle='--', linewidth=0.7)

# Set y-axis limits
plt.ylim(0, 1000000)

# Formatter function to convert values to thousands
def thousands_formatter(x, pos):
    return f'{int(x/1000)}'    # the values are in Mt, but diving the axis by 1000 to show in Gt

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Add a shaded region between 400 and 580 on the y-axis
plt.axhspan(258000, 358000, color='#d4e157', alpha=0.5)
plt.text(1.5, 300000, '1.5°C warming', color='black', fontsize=12, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5))

# Add a shaded region between 400 and 580 on the y-axis
plt.axhspan(408000, 508000, color='orange', alpha=0.3)
plt.text(5, 450000, '1.6°C warming', color='black', fontsize=12, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5))

# Add a shaded region between 400 and 580 on the y-axis
plt.axhspan(558000, 708000, color='red', alpha=0.3)
plt.text(10, 625000, 'Carbon budget: 1.7°C warming', color='black', fontsize=12, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5))

plt.xlabel('Year')
plt.ylabel('GtCO2')
plt.title('Cumulative Emissions from Power Sector', fontsize=20, pad=30)
plt.text(0.5, 1.01, 'NGFS GCAM 6 Model; Carbon budget ranges indicate 50%-67% likelyhood for limiting global warming', transform=ax.transAxes, ha='center', fontsize=10)

plt.legend()
plt.show()





# Plot # 2 --- Secondary V2
    
# Plot the cumulative emissions
plt.figure(figsize=(12, 8))

for scenario in df_emissions_global_byscenario_secondary_cumulative['Scenario'].unique():
    plt.plot(year_columns, df_emissions_global_byscenario_secondary_cumulative[df_emissions_global_byscenario_secondary_cumulative['Scenario'] == scenario][year_columns].values[0], label=scenario)

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
plt.text(0.5, 1.01, 'NGFS GCAM 6 Model; Carbon budget ranges indicate 50%-67% likelyhood for limiting global warming', transform=ax.transAxes, ha='center', fontsize=10)

plt.legend()
plt.show()






# In[8]:

##################################################################################################
##################### SECTION 2: SCENARIOS BY REGIONS ############################################
##################################################################################################

# Plot # 1 --- Current Policy

# get cumulative emissions by region
df_emissions_byregion_currentpolicy_primary_cumulative_REGION = df_emissions_byregion_currentpolicy_primary_cumulative.groupby(['gca_region'])[year_columns].sum()
df_emissions_byregion_currentpolicy_primary_cumulative_REGION = df_emissions_byregion_currentpolicy_primary_cumulative_REGION.T # # Transpose the DataFrame to make regions columns and years as rows


# Plotting
colors = ['#003f5c', '#374c80', '#7a5195', '#bc5090', '#ef5675', '#ff764a', '#ffa600']

plt.figure(figsize=(12, 8))
plt.stackplot(df_emissions_byregion_currentpolicy_primary_cumulative_REGION.index, 
              [df_emissions_byregion_currentpolicy_primary_cumulative_REGION[region] for region in df_emissions_byregion_currentpolicy_primary_cumulative_REGION.columns],
              labels=df_emissions_byregion_currentpolicy_primary_cumulative_REGION.columns,
              colors=colors)

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Add horizontal grid lines
plt.grid(axis='both', which='both', linestyle='--', linewidth=0.7)

# Set y-axis limits
plt.ylim(0, 1000000)

# Formatter function to convert values to thousands
def thousands_formatter(x, pos):
    return f'{int(x/1000)}'    # the values are in Mt, but diving the axis by 1000 to show in Gt

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

plt.xlabel('Year')
plt.ylabel('GtCO2')
plt.title('Cumulative Emissions from Energy Sector: Current Policies', fontsize=20, pad=30)
plt.text(0.5, 1.01, 'NGFS GCAM 6 Model', transform=ax.transAxes, ha='center', fontsize=10)

plt.legend(loc='upper left')
plt.show()




# Plot # 2 --- NDC

# get cumulative emissions by region
df_emissions_byregion_ndc_primary_cumulative_REGION = df_emissions_byregion_ndc_primary_cumulative.groupby(['gca_region'])[year_columns].sum()
df_emissions_byregion_ndc_primary_cumulative_REGION = df_emissions_byregion_ndc_primary_cumulative_REGION.T # # Transpose the DataFrame to make regions columns and years as rows


# Plotting
colors = ['#003f5c', '#374c80', '#7a5195', '#bc5090', '#ef5675', '#ff764a', '#ffa600']

plt.figure(figsize=(12, 8))
plt.stackplot(df_emissions_byregion_ndc_primary_cumulative_REGION.index, 
              [df_emissions_byregion_ndc_primary_cumulative_REGION[region] for region in df_emissions_byregion_ndc_primary_cumulative_REGION.columns],
              labels=df_emissions_byregion_ndc_primary_cumulative_REGION.columns,
              colors=colors)

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Add horizontal grid lines
plt.grid(axis='both', which='both', linestyle='--', linewidth=0.7)

# Set y-axis limits
plt.ylim(0, 1000000)

# Formatter function to convert values to thousands
def thousands_formatter(x, pos):
    return f'{int(x/1000)}'    # the values are in Mt, but diving the axis by 1000 to show in Gt

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

plt.xlabel('Year')
plt.ylabel('GtCO2')
plt.title('Cumulative Emissions from Energy Sector: NDCs', fontsize=20, pad=30)
plt.text(0.5, 1.01, 'NGFS GCAM 6 Model', transform=ax.transAxes, ha='center', fontsize=10)

plt.legend(loc='upper left')
plt.show()





# Plot # 3 --- BELOW 2

# get cumulative emissions by region
df_emissions_byregion_below2_primary_cumulative_REGION = df_emissions_byregion_below2_primary_cumulative.groupby(['gca_region'])[year_columns].sum()
df_emissions_byregion_below2_primary_cumulative_REGION = df_emissions_byregion_below2_primary_cumulative_REGION.T # # Transpose the DataFrame to make regions columns and years as rows


# Plotting
colors = ['#003f5c', '#374c80', '#7a5195', '#bc5090', '#ef5675', '#ff764a', '#ffa600']

plt.figure(figsize=(12, 8))
plt.stackplot(df_emissions_byregion_below2_primary_cumulative_REGION.index, 
              [df_emissions_byregion_below2_primary_cumulative_REGION[region] for region in df_emissions_byregion_below2_primary_cumulative_REGION.columns],
              labels=df_emissions_byregion_below2_primary_cumulative_REGION.columns,
              colors=colors)

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Add horizontal grid lines
plt.grid(axis='both', which='both', linestyle='--', linewidth=0.7)

# Set y-axis limits
plt.ylim(0, 1000000)

# Formatter function to convert values to thousands
def thousands_formatter(x, pos):
    return f'{int(x/1000)}'    # the values are in Mt, but diving the axis by 1000 to show in Gt

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

plt.xlabel('Year')
plt.ylabel('GtCO2')
plt.title('Cumulative Emissions from Energy Sector: Below 2°C', fontsize=20, pad=30)
plt.text(0.5, 1.01, 'NGFS GCAM 6 Model', transform=ax.transAxes, ha='center', fontsize=10)

plt.legend(loc='upper left')
plt.show()





# Plot # 4 --- NetZero

# get cumulative emissions by region
df_emissions_byregion_netzero_primary_cumulative_REGION = df_emissions_byregion_netzero_primary_cumulative.groupby(['gca_region'])[year_columns].sum()
df_emissions_byregion_netzero_primary_cumulative_REGION = df_emissions_byregion_netzero_primary_cumulative_REGION.T # # Transpose the DataFrame to make regions columns and years as rows


# Plotting
colors = ['#003f5c', '#374c80', '#7a5195', '#bc5090', '#ef5675', '#ff764a', '#ffa600']

plt.figure(figsize=(12, 8))
plt.stackplot(df_emissions_byregion_netzero_primary_cumulative_REGION.index, 
              [df_emissions_byregion_netzero_primary_cumulative_REGION[region] for region in df_emissions_byregion_netzero_primary_cumulative_REGION.columns],
              labels=df_emissions_byregion_netzero_primary_cumulative_REGION.columns,
              colors=colors)

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Add horizontal grid lines
plt.grid(axis='both', which='both', linestyle='--', linewidth=0.7)

# Set y-axis limits
plt.ylim(0, 1000000)

# Formatter function to convert values to thousands
def thousands_formatter(x, pos):
    return f'{int(x/1000)}'    # the values are in Mt, but diving the axis by 1000 to show in Gt

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

plt.xlabel('Year')
plt.ylabel('GtCO2')
plt.title('Cumulative Emissions from Energy Sector: Net Zero 2050', fontsize=20, pad=30)
plt.text(0.5, 1.01, 'NGFS GCAM 6 Model', transform=ax.transAxes, ha='center', fontsize=10)

plt.legend(loc='upper left')
plt.show()





# In[8]:

##################################################################################################
##################### SECTION 2: SCENARIOS BY REGIONS ############################################
##################################################################################################

# Plot # 1 --- Primary energy

# Plotting
ax = df_comparison_primary.plot(kind='bar', figsize=(10, 7), color=['#004c6d', '#7d93a6', '#c9c9c9'])
plt.title('Emissions from Energy Sector', fontsize=20, pad=30)
plt.text(0.5, 1.01, 'Year 2020; NGFS GCAM 6 Model', transform=ax.transAxes, ha='center', fontsize=10)
ax.set_xlabel('Energy Sources', fontsize=12)
ax.set_ylabel('Emissions (GtCO2)', fontsize=12)
ax.set_xticklabels(df_comparison_primary.index, rotation=0)
ax.grid(True, linestyle='--', which='both', axis='y', alpha=0.7)
plt.legend(title='Data Source')
plt.show()


# Plot # 2 --- Secondary energy

# Plotting
ax = df_comparison_secondary.plot(kind='bar', figsize=(10, 7), color=['#006eac', '#00d1ff'])
plt.title('Emissions from Power Sector', fontsize=20, pad=30)
plt.text(0.5, 1.01, 'NGFS GCAM 6 Model Year 2020', transform=ax.transAxes, ha='center', fontsize=10)
ax.set_xlabel('Energy Sources', fontsize=12)
ax.set_ylabel('Emissions (GtCO2)', fontsize=12)
ax.set_xticklabels(df_comparison_secondary.index, rotation=0)
ax.grid(True, linestyle='--', which='both', axis='y', alpha=0.7)
plt.legend(title='Data Source')
plt.show()


# Plot # 3 --- Total

# Plotting
ax = df_comparison_total.plot(kind='bar', figsize=(10, 7), color=['#8cbcac'], legend=False)
plt.title('Emissions Comparison', fontsize=20, pad=30)
plt.text(0.5, 1.01, 'Year 2020; NGFS GCAM 6 Model', transform=ax.transAxes, ha='center', fontsize=10)
ax.set_ylabel('Emissions (GtCO2)', fontsize=12)
ax.set_xticklabels(df_comparison_total.index, rotation=0)
ax.grid(True, linestyle='--', which='both', axis='y', alpha=0.7)
plt.show()


 
# Plot # 4 --- REGIONS

# Plotting
ax = df_comparison_total_regions.plot(kind='bar', figsize=(10, 7), color=['#006eac','#8fb5d3'], legend=False)
plt.title('Emissions Comparison', fontsize=20, pad=30)
plt.text(0.5, 1.01, 'NGFS GCAM 6 Model 2024 estimate; OWID 2022 estimate', transform=ax.transAxes, ha='center', fontsize=10)
ax.set_ylabel('Emissions (GtCO2)', fontsize=12)
ax.set_xticklabels(df_comparison_total_regions.index, rotation=0)
ax.grid(True, linestyle='--', which='both', axis='y', alpha=0.7)
plt.legend(title='Data Source')
plt.show()



# In[10]:
# Export data

df_gcam_filtered.to_excel('2 - output/script 2/1.1 - GCAM - filtered.xlsx', index=False)
df_gcam_emissions.to_excel('2 - output/script 2/1.2 - GCAM - filtered - emissions.xlsx', index=False)
df_gcam_change.to_excel('2 - output/script 2/1.3 - GCAM - percent change.xlsx', index=False)
gcam_countries.to_excel('2 - output/script 2/1.4 - GCAM - countries - emissions intensity based on FA.xlsx', index=False)

df_emissions_global_bysource.to_excel('2 - output/script 2/2.1 - GCAM - emissions - bysource.xlsx', index = False)
df_emissions_byregion.to_excel('2 - output/script 2/2.2 - GCAM - emissions - byregion.xlsx', index = False)
df_gcam_ghg.to_excel('2 - output/script 2/2.3 - GCAM - emissions - ghg as given.xlsx', index = False)
df_gcam_ghg_energy.to_excel('2 - output/script 2/2.4 - GCAM - emissions - ghg as given - energy.xlsx', index = False)

df_emissions_global_byscenario_primary.to_excel('2 - output/script 2/3.1 - GCAM - emissions - scenarios - primary.xlsx', index = False)
df_emissions_global_byscenario_primary_cumulative.to_excel('2 - output/script 2/3.2 - GCAM - emissions - scenarios - primary - cumulative.xlsx', index = False)

df_emissions_global_byscenario_secondary.to_excel('2 - output/script 2/4.1 - GCAM - emissions - scenarios - secondary.xlsx', index = False)
df_emissions_global_byscenario_secondary_cumulative.to_excel('2 - output/script 2/4.2 - GCAM - emissions - scenarios - secondary - cumulative.xlsx', index = False)

df_comparison_total.to_excel('2 - output/script 2/5.1 - GCAM - comparison - total.xlsx', index=False)
df_comparison_total_regions.to_excel('2 - output/script 2/5.2 - GCAM - comparison - total - by regions.xlsx', index=False)
df_comparison_primary.to_excel('2 - output/script 2/5.3 - GCAM - comparison - primary.xlsx', index=False)
df_comparison_secondary.to_excel('2 - output/script 2/5.4 - GCAM - comparison - secondary.xlsx', index=False)

df_emissions_byregion_currentpolicy_primary.to_excel('2 - output/script 2/6.1 - GCAM - emissions - current policy - primary.xlsx', index=False)
df_emissions_byregion_currentpolicy_secondary.to_excel('2 - output/script 2/6.2 - GCAM - emissions - current policy - secondary.xlsx', index=False)

df_emissions_byregion_netzero_primary.to_excel('2 - output/script 2/7.1 - GCAM - emissions - netzero - primary.xlsx', index=False)
df_emissions_byregion_netzero_secondary.to_excel('2 - output/script 2/7.2 - GCAM - emissions - netzero - secondary.xlsx', index=False)

