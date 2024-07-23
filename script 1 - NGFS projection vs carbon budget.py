# In[1]:
# Date: July 22, 2024
# Project: NGFS emissions projections vs Carbon Budget
# Author: Farhad Panahov


# Task #1: The datapoints are provided in 5 year intervals, ending in 2050
#   - Iterpolate linear trend line
#   - Obtain YoY % change 



# Task #2: For Primary Energy convert units and values to emissions
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
# 1 EJ = 27.93 million cubic meters of natural gas
# 1 m3 = 1.932 kg CO2



# Task #3: For Secondary Energy convert units and values to emissions 
# https://www.eia.gov/environment/emissions/co2_vol_mass.php
# https://www.convertunits.com/from/EJ/to/megawatt-hour
# https://www.eia.gov/tools/faqs/faq.php?id=74&t=11 
# 1 EJ = 277777777.77778 MWh
# 1 kWh = 2.3 pounds CO2 from coal
# 1 kWh = 0.97 pounds CO2 from NG
# 1 kWh = 2.38 pounds CO2 from Oil



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

directory = r'C:\Users\panah\OneDrive\Desktop\Work\2 - RA - Climate fin'
os.chdir(directory)


GCAM = "1 - input/Downscaled_GCAM 6.0 NGFS_data.xlsx"
df_gcam = pd.read_excel(GCAM)      #input the name of the Excel file
del GCAM



# In[4]:
# filter, and create %change df

df_gcam_filtered = df_gcam.loc[(df_gcam['Variable'] == 'Primary Energy|Gas') |  (df_gcam['Variable'] == 'Primary Energy|Oil')| (df_gcam['Variable'] == 'Primary Energy|Coal')| (df_gcam['Variable'] == 'Secondary Energy|Electricity|Coal')| (df_gcam['Variable'] == 'Secondary Energy|Electricity|Gas')|(df_gcam['Variable'] == 'Secondary Energy|Electricity|Oil')]


# Interpolate the NaN values in the specific columns
years = [str(year) for year in range(2020, 2101)]
df_gcam_filtered[years] = df_gcam_filtered[years].interpolate(method='linear', axis=1)
df_gcam_years = df_gcam_filtered[years]
#df_gcam_years.to_excel('Interpolated-GCAM.xlsx', index=False)
    

# Calculate yearly percent change for each row
pct_change_df = df_gcam_years.pct_change(axis=1) * 100
pct_change_df = pct_change_df.fillna(0)
del df_gcam_years, years


#First concatenate extrapolated data with filtered data frame
first_5_columns = df_gcam_filtered.iloc[:, :5]
df_gcam_change = pd.concat([first_5_columns, pct_change_df], axis=1)
del first_5_columns, pct_change_df



# In[5]:
# Convert primary energy to emissions    
    
# Define the constant to multiply for unit conversion
emissions_factor_coal = 34120842.37536*1.10231*1764.83 / 10**3 / 10**6    #EJ to Tonne to Short Ton to KgCO2 to tCO2 to MtCO2 --- final unit: MtCO2
emissions_factor_oil = 163452108.5322*0.43 / 10**6                       #EJ to barrel to tCO2 to Mt --- final unit: MtCO2
emissions_factor_gas = 27.93*10**6*1.932 / 10**3 / 10**6                  #EJ to million cubic meters of natural gas to tCO2 to Mt --- final unit: MtCO2


df_gcam_emissions = df_gcam_filtered
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


del emissions_factor_gas, emissions_factor_oil, emissions_factor_coal



# In[6]:
# Convert secondary energy to emissions
    
#Unit conversion for secondary energy sources
emissions_factor_MWh_coal = 277777777.77778 * 1000 * 2.3 * 0.453592 / 10**3 / 10**6         # final unit: MtCO2
emissions_factor_MWh_oil = 277777777.77778 * 1000 * 2.38 * 0.453592 / 10**3 / 10**6         # final unit: MtCO2
emissions_factor_MWh_ng = 277777777.77778 * 1000 * 0.97 * 0.453592 / 10**3  / 10**6       # final unit: MtCO2


# Iterate over the DataFrame 
for index, row in df_gcam_emissions.iterrows():
  
    if row['Variable'] == 'Secondary Energy|Electricity|Coal':
        #print(row)
        df_gcam_emissions.loc[index, df_gcam_emissions.columns[5:]] *= emissions_factor_MWh_coal      #Multiply columns starting from Year 2020
        df_gcam_emissions.loc[index, 'Unit'] = 'MtCO2'                                             # Change the unit    
    
    if row['Variable'] == 'Secondary Energy|Electricity|Gas':
        #print(row)
        df_gcam_emissions.loc[index, df_gcam_emissions.columns[5:]] *= emissions_factor_MWh_ng       #Multiply columns starting from column 6
        df_gcam_emissions.loc[index, 'Unit'] = 'MtCO2'           # Change the value in column 5

    if row['Variable'] == 'Secondary Energy|Electricity|Oil':
        #print(row)
        df_gcam_emissions.loc[index, df_gcam_emissions.columns[5:]] *= emissions_factor_MWh_oil       #Multiply columns starting from Year 2020
        df_gcam_emissions.loc[index, 'Unit'] = 'MtCO2'                         # Change the unit    


del emissions_factor_MWh_coal, emissions_factor_MWh_ng, emissions_factor_MWh_oil, index, row



# In[7]:
# Get overall emissions
    
year_columns = [str(year) for year in range(2020, 2101)]

df_global_byscenario = df_gcam_emissions.groupby(['Scenario'])[year_columns].sum()
df_global_bysource = df_gcam_emissions[df_gcam_emissions['Scenario'] == 'Current Policies'].groupby(['Variable'])[year_columns].sum()

# create cumulative emissions
df_global_cumulative = df_global_byscenario
df_global_cumulative[year_columns] = df_global_byscenario[year_columns].cumsum(axis=1)
df_global_cumulative = df_global_cumulative.reset_index()



# In[8]:
# Plot # 1 --- Scenarios & Carbon budget
    
# Plot the cumulative emissions
plt.figure(figsize=(12, 8))

for scenario in df_global_cumulative['Scenario'].unique():
    plt.plot(year_columns, df_global_cumulative[df_global_cumulative['Scenario'] == scenario][year_columns].values[0], label=scenario)

# Customize the x-axis to show ticks every 10 years
plt.xticks([str(year) for year in range(2020, 2101, 10)])

# Add a vertical red line at 2050
plt.axvline(x='2050', color='red', linestyle='--', linewidth=2, label='GCAM projection limit')

# Add horizontal grid lines
plt.grid(axis='both', which='both', linestyle='--', linewidth=0.7)

# Set y-axis limits
plt.ylim(0, 1500000)

# Formatter function to convert values to thousands
def thousands_formatter(x, pos):
    return f'{int(x/1000)}'    # the values are in Mt, but diving the axis by 1000 to show in Gt

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Add a shaded region between 400 and 580 on the y-axis
plt.axhspan(400000, 580000, color='red', alpha=0.3)

plt.text(40, 490000, 'Carbon budget', color='black', fontsize=12, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.5))

plt.xlabel('Year')
plt.ylabel('GtCO2')
plt.title('Cumulative Emissions from Energy Sector')
plt.legend()



# In[9]:
# Plot # 2 --- Emissins by source
    
# Plot the bargraph by source of energy emissions
plt.figure(figsize=(12, 8))
df_global_bysource['2020'].plot(kind = 'barh', color = 'skyblue')

plt.xlabel('Mt CO2 in 2020')
plt.title('Energy sector emissions by source')



# In[10]:
# Export data

df_gcam_change.to_excel('2 - output/1 - GCAM - percent change.xlsx', index=False)
df_gcam_filtered.to_excel('2 - output/2 - GCAM - filtered - prim and secon energy.xlsx', index=False)
df_gcam_emissions.to_excel('2 - output/3 - GCAM - emissions.xlsx', index=False)
df_global_byscenario.to_excel('2 - output/4 - GCAM - global annual ghg - by scenario.xlsx', index=False)
df_global_bysource.to_excel('2 - output/5 - GCAM - global annual ghg - by source.xlsx', index=False)
df_global_cumulative.to_excel('2 - output/6 - GCAM - global cumulative ghg.xlsx', index=False)


