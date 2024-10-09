# In[1]:
# Date: Sep 2, 2024
# Project: Map pollution level in 2050 Poland: CP vs NZ 1.5C 67% adjusted
# Author: Farhad Panahov










# In[2]:
# load packages

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import FuncFormatter
import seaborn as sns
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point








# In[3]:
# directory & load data

directory = r'C:\Users\panah\OneDrive\Desktop\Work\3 - RA - Air pollution'
os.chdir(directory)
del directory


# --------------
# LOAD SCRIPT 6.1 DATA










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

# chart theme
sns.set_theme(style="ticks")


# Formatter function to convert values to thousands
def thousands_formatter(x, pos):
    return f'{int(x/1000)}'    # the values are in Mt, but diving the axis by 1000 to show in Gt


# set fossil fuel colors
colors = {'Coal': 'brown', 'Gas':  'blue', 'Oil': 'grey'}  # Define a color map for each fuel type


##################################################################################################
##################### SECTION 1: ANNUAL EMISSISON ################################################
##################################################################################################


# --------------
# 1.1 GERMANY
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the lines
plt.plot(df_country_deu.index, df_country_deu['ghg_annual_cp'], label='NGFS Current Policies')
plt.plot(df_country_deu.index, df_country_deu['ghg_annual_nz'], label='NGFS Net Zero 2050')
plt.plot(df_country_deu.index, df_country_deu['ghg_annual_nznew'], label='Carbon budget consistent Net Zero*')

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Set y-axis formatter to display values in thousands
ax = plt.gca()

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('MtCO2', fontsize = 15)
plt.title('Annual Emissions from Power Sector by Scenario: Germany', fontsize=20, pad=60)
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)
ax.legend(loc='upper right', fontsize=12)

plt.show()





# --------------
# 1.2 INDONESIA
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the lines
plt.plot(df_country_idn.index, df_country_idn['ghg_annual_cp'], label='NGFS Current Policies')
plt.plot(df_country_idn.index, df_country_idn['ghg_annual_nz'], label='NGFS Net Zero 2050')
plt.plot(df_country_idn.index, df_country_idn['ghg_annual_nznew'], label='Carbon budget consistent Net Zero*')

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Set y-axis formatter to display values in thousands
ax = plt.gca()

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('MtCO2', fontsize = 15)
plt.title('Annual Emissions from Power Sector by Scenario: Indonesia', fontsize=20, pad=60)
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)
ax.legend(loc='upper left', fontsize=12)

plt.show()





# --------------
# 1.3 INDIA
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the lines
plt.plot(df_country_ind.index, df_country_ind['ghg_annual_cp'], label='NGFS Current Policies')
plt.plot(df_country_ind.index, df_country_ind['ghg_annual_nz'], label='NGFS Net Zero 2050')
plt.plot(df_country_ind.index, df_country_ind['ghg_annual_nznew'], label='Carbon budget consistent Net Zero*')

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Set y-axis formatter to display values in thousands
ax = plt.gca()

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('MtCO2', fontsize = 15)
plt.title('Annual Emissions from Power Sector by Scenario: India', fontsize=20, pad=60)
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)
ax.legend(loc='upper left', fontsize=12)

plt.show()





# --------------
# 1.4 TURKEYE
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the lines
plt.plot(df_country_tur.index, df_country_tur['ghg_annual_cp'], label='NGFS Current Policies')
plt.plot(df_country_tur.index, df_country_tur['ghg_annual_nz'], label='NGFS Net Zero 2050')
plt.plot(df_country_tur.index, df_country_tur['ghg_annual_nznew'], label='Carbon budget consistent Net Zero*')

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Set y-axis formatter to display values in thousands
ax = plt.gca()

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('MtCO2', fontsize = 15)
plt.title('Annual Emissions from Power Sector by Scenario: Turkeye', fontsize=20, pad=60)
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)
ax.legend(loc='upper left', fontsize=12)

plt.show()





# --------------
# 1.5 USA
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the lines
plt.plot(df_country_usa.index, df_country_usa['ghg_annual_cp'], label='NGFS Current Policies')
plt.plot(df_country_usa.index, df_country_usa['ghg_annual_nz'], label='NGFS Net Zero 2050')
plt.plot(df_country_usa.index, df_country_usa['ghg_annual_nznew'], label='Carbon budget consistent Net Zero*')

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Set y-axis formatter to display values in thousands
ax = plt.gca()

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('MtCO2', fontsize = 15)
plt.title('Annual Emissions from Power Sector by Scenario: USA', fontsize=20, pad=60)
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)
ax.legend(loc='upper right', fontsize=12)

plt.show()





# --------------
# 1.6 VIETNAM
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the lines
plt.plot(df_country_vnm.index, df_country_vnm['ghg_annual_cp'], label='NGFS Current Policies')
plt.plot(df_country_vnm.index, df_country_vnm['ghg_annual_nz'], label='NGFS Net Zero 2050')
plt.plot(df_country_vnm.index, df_country_vnm['ghg_annual_nznew'], label='Carbon budget consistent Net Zero*')

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Set y-axis formatter to display values in thousands
ax = plt.gca()

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('MtCO2', fontsize = 15)
plt.title('Annual Emissions from Power Sector by Scenario: Vietnam', fontsize=20, pad=60)
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)
ax.legend(loc='upper left', fontsize=12)

plt.show()





# --------------
# 1.7 GLOBAL
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the lines
plt.plot(df_country_global.index, df_country_global['ghg_annual_cp'], label='NGFS Current Policies')
plt.plot(df_country_global.index, df_country_global['ghg_annual_nz'], label='NGFS Net Zero 2050')
plt.plot(df_country_global.index, df_country_global['ghg_annual_nznew'], label='Carbon budget consistent Net Zero*')

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Set y-axis formatter to display values in thousands
ax = plt.gca()

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('MtCO2', fontsize = 15)
plt.title('Annual Emissions from Power Sector by Scenario: Global', fontsize=20, pad=60)
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)
ax.legend(loc='upper left', fontsize=12)

plt.show()










##################################################################################################
##################### SECTION 2: CUMULATIVE EMISSISON ############################################
##################################################################################################

# --------------
# 2.1 GERMANY
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the lines
plt.plot(df_country_deu.index, df_country_deu['ghg_cumulative_cp'], label='NGFS Current Policies')
plt.plot(df_country_deu.index, df_country_deu['ghg_cumulative_nz'], label='NGFS Net Zero 2050')
plt.plot(df_country_deu.index, df_country_deu['ghg_cumulative_nznew'], label='Carbon budget consistent Net Zero*')

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('GtCO2', fontsize = 15)
plt.title('Cumulative Emissions from Power Sector by Scenario: Germany', fontsize=20, pad=60)
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)
ax.legend(loc='upper left', fontsize=12)

plt.show()





# --------------
# 2.2 INDONESIA
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the lines
plt.plot(df_country_idn.index, df_country_idn['ghg_cumulative_cp'], label='NGFS Current Policies')
plt.plot(df_country_idn.index, df_country_idn['ghg_cumulative_nz'], label='NGFS Net Zero 2050')
plt.plot(df_country_idn.index, df_country_idn['ghg_cumulative_nznew'], label='Carbon budget consistent Net Zero*')

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('GtCO2', fontsize = 15)
plt.title('Cumulative Emissions from Power Sector by Scenario: Indonesia', fontsize=20, pad=60)
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)
ax.legend(loc='upper left', fontsize=12)

plt.show()





# --------------
# 2.3 INDIA
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the lines
plt.plot(df_country_ind.index, df_country_ind['ghg_cumulative_cp'], label='NGFS Current Policies')
plt.plot(df_country_ind.index, df_country_ind['ghg_cumulative_nz'], label='NGFS Net Zero 2050')
plt.plot(df_country_ind.index, df_country_ind['ghg_cumulative_nznew'], label='Carbon budget consistent Net Zero*')

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('GtCO2', fontsize = 15)
plt.title('Cumulative Emissions from Power Sector by Scenario: India', fontsize=20, pad=60)
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)
ax.legend(loc='upper left', fontsize=12)

plt.show()





# --------------
# 2.4 TURKEYE
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the lines
plt.plot(df_country_tur.index, df_country_tur['ghg_cumulative_cp'], label='NGFS Current Policies')
plt.plot(df_country_tur.index, df_country_tur['ghg_cumulative_nz'], label='NGFS Net Zero 2050')
plt.plot(df_country_tur.index, df_country_tur['ghg_cumulative_nznew'], label='Carbon budget consistent Net Zero*')

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('GtCO2', fontsize = 15)
plt.title('Cumulative Emissions from Power Sector by Scenario: Turkeye', fontsize=20, pad=60)
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)
ax.legend(loc='upper left', fontsize=12)

plt.show()





# --------------
# 2.5 USA
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the lines
plt.plot(df_country_usa.index, df_country_usa['ghg_cumulative_cp'], label='NGFS Current Policies')
plt.plot(df_country_usa.index, df_country_usa['ghg_cumulative_nz'], label='NGFS Net Zero 2050')
plt.plot(df_country_usa.index, df_country_usa['ghg_cumulative_nznew'], label='Carbon budget consistent Net Zero*')

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('GtCO2', fontsize = 15)
plt.title('Cumulative Emissions from Power Sector by Scenario: USA', fontsize=20, pad=60)
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)
ax.legend(loc='upper left', fontsize=12)

plt.show()





# --------------
# 2.6 VIETNAM
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the lines
plt.plot(df_country_vnm.index, df_country_vnm['ghg_cumulative_cp'], label='NGFS Current Policies')
plt.plot(df_country_vnm.index, df_country_vnm['ghg_cumulative_nz'], label='NGFS Net Zero 2050')
plt.plot(df_country_vnm.index, df_country_vnm['ghg_cumulative_nznew'], label='Carbon budget consistent Net Zero*')

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('GtCO2', fontsize = 15)
plt.title('Cumulative Emissions from Power Sector by Scenario: Vietnam', fontsize=20, pad=60)
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)
ax.legend(loc='upper left', fontsize=12)

plt.show()




# --------------
# 2.7 GLOBAL
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the lines
plt.plot(df_country_global.index, df_country_global['ghg_cumulative_cp'], label='NGFS Current Policies')
plt.plot(df_country_global.index, df_country_global['ghg_cumulative_nz'], label='NGFS Net Zero 2050')
plt.plot(df_country_global.index, df_country_global['ghg_cumulative_nznew'], label='Carbon budget consistent Net Zero*')

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('GtCO2', fontsize = 15)
plt.title('Cumulative Emissions from Power Sector by Scenario: Global', fontsize=20, pad=60)
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)
ax.legend(loc='upper left', fontsize=12)

plt.show()










##################################################################################################
##################### SECTION 3: AVOIDED EMISSIONS ###############################################
##################################################################################################

# --------------
# 3.1 GERMANY
# Plotting
fig, ax1 = plt.subplots(figsize=(12, 8))

# Plot the first line on the primary y-axis
ax1.plot(df_country_deu.index, df_country_deu['ghg_annaul_avoided'], label='Annual avoided emissions (LHS)', color='blue')
ax1.set_ylabel('MtCO2 (Annual)', fontsize=15)

# Create a secondary y-axis
ax2 = ax1.twinx()
ax2.plot(df_country_deu.index, df_country_deu['ghg_cumulative_avoided'], label='Cumulative avoided emissions (RHS)', color='green')
ax2.set_ylabel('GtCO2 (Cumulative)', fontsize=15)
ax2.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Customize the x-axis to show ticks every 5 years
ax1.set_xticks([str(year) for year in range(2025, 2051, 5)])

# Set labels and title
plt.xlabel('Year', fontsize=15)
plt.title('Avoided Emissions from Power Sector in Germany: \n Current Policies vs Carbon Budget Consistent Net Zero*', fontsize=20, pad=60)

# Adding text
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', 
         transform=ax1.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelihood', 
         transform=ax1.transAxes, ha='center', fontsize=12)

# Adding legends for both lines
fig.legend(loc='upper left', fontsize=12, bbox_to_anchor=(0.13, 0.85))

# Show the plot
plt.show()





# --------------
# 3.2 INDONESIA
# Plotting
fig, ax1 = plt.subplots(figsize=(12, 8))

# Plot the first line on the primary y-axis
ax1.plot(df_country_idn.index, df_country_idn['ghg_annaul_avoided'], label='Annual avoided emissions (LHS)', color='blue')
ax1.set_ylabel('MtCO2 (Annual)', fontsize=15)

# Create a secondary y-axis
ax2 = ax1.twinx()
ax2.plot(df_country_idn.index, df_country_idn['ghg_cumulative_avoided'], label='Cumulative avoided emissions (RHS)', color='green')
ax2.set_ylabel('GtCO2 (Cumulative)', fontsize=15)
ax2.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Customize the x-axis to show ticks every 5 years
ax1.set_xticks([str(year) for year in range(2025, 2051, 5)])

# Set labels and title
plt.xlabel('Year', fontsize=15)
plt.title('Avoided Emissions from Power Sector in Indonesia: \n Current Policies vs Carbon Budget Consistent Net Zero*', fontsize=20, pad=60)

# Adding text
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', 
         transform=ax1.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelihood', 
         transform=ax1.transAxes, ha='center', fontsize=12)

# Adding legends for both lines
fig.legend(loc='upper left', fontsize=12, bbox_to_anchor=(0.13, 0.85))

# Show the plot
plt.show()





# --------------
# 3.3 INDIA
# Plotting
fig, ax1 = plt.subplots(figsize=(12, 8))

# Plot the first line on the primary y-axis
ax1.plot(df_country_ind.index, df_country_ind['ghg_annaul_avoided'], label='Annual avoided emissions (LHS)', color='blue')
ax1.set_ylabel('MtCO2 (Annual)', fontsize=15)

# Create a secondary y-axis
ax2 = ax1.twinx()
ax2.plot(df_country_ind.index, df_country_ind['ghg_cumulative_avoided'], label='Cumulative avoided emissions (RHS)', color='green')
ax2.set_ylabel('GtCO2 (Cumulative)', fontsize=15)
ax2.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Customize the x-axis to show ticks every 5 years
ax1.set_xticks([str(year) for year in range(2025, 2051, 5)])

# Set labels and title
plt.xlabel('Year', fontsize=15)
plt.title('Avoided Emissions from Power Sector in India: \n Current Policies vs Carbon Budget Consistent Net Zero*', fontsize=20, pad=60)

# Adding text
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', 
         transform=ax1.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelihood', 
         transform=ax1.transAxes, ha='center', fontsize=12)

# Adding legends for both lines
fig.legend(loc='upper left', fontsize=12, bbox_to_anchor=(0.13, 0.85))

# Show the plot
plt.show()





# --------------
# 3.4 TURKEYE
# Plotting
fig, ax1 = plt.subplots(figsize=(12, 8))

# Plot the first line on the primary y-axis
ax1.plot(df_country_tur.index, df_country_tur['ghg_annaul_avoided'], label='Annual avoided emissions (LHS)', color='blue')
ax1.set_ylabel('MtCO2 (Annual)', fontsize=15)

# Create a secondary y-axis
ax2 = ax1.twinx()
ax2.plot(df_country_tur.index, df_country_tur['ghg_cumulative_avoided'], label='Cumulative avoided emissions (RHS)', color='green')
ax2.set_ylabel('GtCO2 (Cumulative)', fontsize=15)
ax2.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Customize the x-axis to show ticks every 5 years
ax1.set_xticks([str(year) for year in range(2025, 2051, 5)])

# Set labels and title
plt.xlabel('Year', fontsize=15)
plt.title('Avoided Emissions from Power Sector in Turkeye: \n Current Policies vs Carbon Budget Consistent Net Zero*', fontsize=20, pad=60)

# Adding text
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', 
         transform=ax1.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelihood', 
         transform=ax1.transAxes, ha='center', fontsize=12)

# Adding legends for both lines
fig.legend(loc='upper left', fontsize=12, bbox_to_anchor=(0.13, 0.85))

# Show the plot
plt.show()





# --------------
# 3.5 USA
# Plotting
fig, ax1 = plt.subplots(figsize=(12, 8))

# Plot the first line on the primary y-axis
ax1.plot(df_country_usa.index, df_country_usa['ghg_annaul_avoided'], label='Annual avoided emissions (LHS)', color='blue')
ax1.set_ylabel('MtCO2 (Annual)', fontsize=15)

# Create a secondary y-axis
ax2 = ax1.twinx()
ax2.plot(df_country_usa.index, df_country_usa['ghg_cumulative_avoided'], label='Cumulative avoided emissions (RHS)', color='green')
ax2.set_ylabel('GtCO2 (Cumulative)', fontsize=15)
ax2.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Customize the x-axis to show ticks every 5 years
ax1.set_xticks([str(year) for year in range(2025, 2051, 5)])

# Set labels and title
plt.xlabel('Year', fontsize=15)
plt.title('Avoided Emissions from Power Sector in USA: \n Current Policies vs Carbon Budget Consistent Net Zero*', fontsize=20, pad=60)

# Adding text
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', 
         transform=ax1.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelihood', 
         transform=ax1.transAxes, ha='center', fontsize=12)

# Adding legends for both lines
fig.legend(loc='upper left', fontsize=12, bbox_to_anchor=(0.13, 0.85))

# Show the plot
plt.show()





# --------------
# 3.6 VIETNAM
# Plotting
fig, ax1 = plt.subplots(figsize=(12, 8))

# Plot the first line on the primary y-axis
ax1.plot(df_country_vnm.index, df_country_vnm['ghg_annaul_avoided'], label='Annual avoided emissions (LHS)', color='blue')
ax1.set_ylabel('MtCO2 (Annual)', fontsize=15)

# Create a secondary y-axis
ax2 = ax1.twinx()
ax2.plot(df_country_vnm.index, df_country_vnm['ghg_cumulative_avoided'], label='Cumulative avoided emissions (RHS)', color='green')
ax2.set_ylabel('GtCO2 (Cumulative)', fontsize=15)
ax2.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Customize the x-axis to show ticks every 5 years
ax1.set_xticks([str(year) for year in range(2025, 2051, 5)])

# Set labels and title
plt.xlabel('Year', fontsize=15)
plt.title('Avoided Emissions from Power Sector in Vietnam: \n Current Policies vs Carbon Budget Consistent Net Zero*', fontsize=20, pad=60)

# Adding text
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', 
         transform=ax1.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelihood', 
         transform=ax1.transAxes, ha='center', fontsize=12)

# Adding legends for both lines
fig.legend(loc='upper left', fontsize=12, bbox_to_anchor=(0.13, 0.85))

# Show the plot
plt.show()





# --------------
# 3.7 GLOBAL
# Plotting
fig, ax1 = plt.subplots(figsize=(12, 8))

# Plot the first line on the primary y-axis
ax1.plot(df_country_global.index, df_country_global['ghg_annaul_avoided'], label='Annual avoided emissions (LHS)', color='blue')
ax1.set_ylabel('MtCO2 (Annual)', fontsize=15)

# Create a secondary y-axis
ax2 = ax1.twinx()
ax2.plot(df_country_global.index, df_country_global['ghg_cumulative_avoided'], label='Cumulative avoided emissions (RHS)', color='green')
ax2.set_ylabel('GtCO2 (Cumulative)', fontsize=15)
ax2.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Customize the x-axis to show ticks every 5 years
ax1.set_xticks([str(year) for year in range(2025, 2051, 5)])

# Set labels and title
plt.xlabel('Year', fontsize=15)
plt.title('Avoided Emissions from Power Sector Globally: \n Current Policies vs Carbon Budget Consistent Net Zero*', fontsize=20, pad=60)

# Adding text
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', 
         transform=ax1.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelihood', 
         transform=ax1.transAxes, ha='center', fontsize=12)

# Adding legends for both lines
fig.legend(loc='upper left', fontsize=12, bbox_to_anchor=(0.13, 0.85))

# Show the plot
plt.show()










##################################################################################################
##################### SECTION 4: ANNUAL CAPACITY #################################################
##################################################################################################

# --------------
# 4.1 GERMANY
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the lines
plt.plot(df_country_deu.index, df_country_deu['capacity_annual_cp'], label='NGFS Current Policies')
plt.plot(df_country_deu.index, df_country_deu['capacity_annual_nz'], label='NGFS Net Zero 2050')
plt.plot(df_country_deu.index, df_country_deu['capacity_annual_nznew'], label='Carbon budget consistent Net Zero*')

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('GW', fontsize = 15)
plt.title('Annual Fossil Fuel Capacity in Power Sector by Scenario: Germany', fontsize=20, pad=60)
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)
ax.legend(loc='upper right', fontsize=12)

plt.show()





# --------------
# 4.2 INDONESIA
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the lines
plt.plot(df_country_idn.index, df_country_idn['capacity_annual_cp'], label='NGFS Current Policies')
plt.plot(df_country_idn.index, df_country_idn['capacity_annual_nz'], label='NGFS Net Zero 2050')
plt.plot(df_country_idn.index, df_country_idn['capacity_annual_nznew'], label='Carbon budget consistent Net Zero*')

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('GW', fontsize = 15)
plt.title('Annual Fossil Fuel Capacity in Power Sector by Scenario: Indonesia', fontsize=20, pad=60)
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)
ax.legend(loc='upper left', fontsize=12)

plt.show()





# --------------
# 4.3 INDIA
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the lines
plt.plot(df_country_ind.index, df_country_ind['capacity_annual_cp'], label='NGFS Current Policies')
plt.plot(df_country_ind.index, df_country_ind['capacity_annual_nz'], label='NGFS Net Zero 2050')
plt.plot(df_country_ind.index, df_country_ind['capacity_annual_nznew'], label='Carbon budget consistent Net Zero*')

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('GW', fontsize = 15)
plt.title('Annual Fossil Fuel Capacity in Power Sector by Scenario: India', fontsize=20, pad=60)
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)
ax.legend(loc='upper left', fontsize=12)

plt.show()





# --------------
# 4.4 TURKEYE
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the lines
plt.plot(df_country_tur.index, df_country_tur['capacity_annual_cp'], label='NGFS Current Policies')
plt.plot(df_country_tur.index, df_country_tur['capacity_annual_nz'], label='NGFS Net Zero 2050')
plt.plot(df_country_tur.index, df_country_tur['capacity_annual_nznew'], label='Carbon budget consistent Net Zero*')

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('GW', fontsize = 15)
plt.title('Annual Fossil Fuel Capacity in Power Sector by Scenario: Turkeye', fontsize=20, pad=60)
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)
ax.legend(loc='upper left', fontsize=12)

plt.show()




# --------------
# 4.5 USA
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the lines
plt.plot(df_country_usa.index, df_country_usa['capacity_annual_cp'], label='NGFS Current Policies')
plt.plot(df_country_usa.index, df_country_usa['capacity_annual_nz'], label='NGFS Net Zero 2050')
plt.plot(df_country_usa.index, df_country_usa['capacity_annual_nznew'], label='Carbon budget consistent Net Zero*')

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('GW', fontsize = 15)
plt.title('Annual Fossil Fuel Capacity in Power Sector by Scenario: USA', fontsize=20, pad=60)
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)
ax.legend(loc='upper right', fontsize=12)

plt.show()






# --------------
# 4.6 VIETNAM
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the lines
plt.plot(df_country_vnm.index, df_country_vnm['capacity_annual_cp'], label='NGFS Current Policies')
plt.plot(df_country_vnm.index, df_country_vnm['capacity_annual_nz'], label='NGFS Net Zero 2050')
plt.plot(df_country_vnm.index, df_country_vnm['capacity_annual_nznew'], label='Carbon budget consistent Net Zero*')

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('GW', fontsize = 15)
plt.title('Annual Fossil Fuel Capacity in Power Sector by Scenario: Vietnam', fontsize=20, pad=60)
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)
ax.legend(loc='upper left', fontsize=12)

plt.show()





# --------------
# 4.7 GLOBAL
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the lines
plt.plot(df_country_global.index, df_country_global['capacity_annual_cp'], label='NGFS Current Policies')
plt.plot(df_country_global.index, df_country_global['capacity_annual_nz'], label='NGFS Net Zero 2050')
plt.plot(df_country_global.index, df_country_global['capacity_annual_nznew'], label='Carbon budget consistent Net Zero*')

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('GW', fontsize = 15)
plt.title('Annual Fossil Fuel Capacity in Power Sector by Scenario: Global', fontsize=20, pad=60)
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)
ax.legend(loc='upper left', fontsize=12)

plt.show()










##################################################################################################
##################### SECTION 5: AVOIDED CAPACITY ################################################
##################################################################################################

# --------------
# 5.1 GERMANY
# Plotting
fig, ax1 = plt.subplots(figsize=(12, 8))

# Plot the first line on the primary y-axis
ax1.plot(df_country_deu.index, abs(df_country_deu['capacity_annaul_avoided']), label='Annual avoided capacity from fossil fuels (LHS)', color='blue')
ax1.set_ylabel('MW (Annual)', fontsize=15)

# Create a secondary y-axis
ax2 = ax1.twinx()
ax2.plot(df_country_deu.index, abs(df_country_deu['capacity_cumulative_avoided']), label='Cumulative avoided capacity from fossil fuels (RHS)', color='green')
ax2.set_ylabel('GW (Cumulative)', fontsize=15)
ax2.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Customize the x-axis to show ticks every 5 years
ax1.set_xticks([str(year) for year in range(2025, 2051, 5)])

# Set labels and title
plt.xlabel('Year', fontsize=15)
plt.title('Avoided Fossil Fuel Capacity in Power Sector in Germany: \n Current Policies vs Carbon Budget Consistent Net Zero*', fontsize=20, pad=60)

# Adding text
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', 
         transform=ax1.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelihood', 
         transform=ax1.transAxes, ha='center', fontsize=12)

# Adding legends for both lines
fig.legend(loc='upper left', fontsize=12, bbox_to_anchor=(0.13, 0.85))

# Show the plot
plt.show()




# --------------
# 5.2 INDONESIA
# Plotting
fig, ax1 = plt.subplots(figsize=(12, 8))

# Plot the first line on the primary y-axis
ax1.plot(df_country_idn.index, abs(df_country_idn['capacity_annaul_avoided']), label='Annual avoided capacity from fossil fuels (LHS)', color='blue')
ax1.set_ylabel('MW (Annual)', fontsize=15)

# Create a secondary y-axis
ax2 = ax1.twinx()
ax2.plot(df_country_idn.index, abs(df_country_idn['capacity_cumulative_avoided']), label='Cumulative avoided capacity from fossil fuels (RHS)', color='green')
ax2.set_ylabel('GW (Cumulative)', fontsize=15)
ax2.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Customize the x-axis to show ticks every 5 years
ax1.set_xticks([str(year) for year in range(2025, 2051, 5)])

# Set labels and title
plt.xlabel('Year', fontsize=15)
plt.title('Avoided Fossil Fuel Capacity in Power Sector in Indonesia: \n Current Policies vs Carbon Budget Consistent Net Zero*', fontsize=20, pad=60)

# Adding text
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', 
         transform=ax1.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelihood', 
         transform=ax1.transAxes, ha='center', fontsize=12)

# Adding legends for both lines
fig.legend(loc='upper left', fontsize=12, bbox_to_anchor=(0.13, 0.85))

# Show the plot
plt.show()





# --------------
# 5.3 INDIA
# Plotting
fig, ax1 = plt.subplots(figsize=(12, 8))

# Plot the first line on the primary y-axis
ax1.plot(df_country_ind.index, abs(df_country_ind['capacity_annaul_avoided']), label='Annual avoided capacity from fossil fuels (LHS)', color='blue')
ax1.set_ylabel('MW (Annual)', fontsize=15)

# Create a secondary y-axis
ax2 = ax1.twinx()
ax2.plot(df_country_ind.index, abs(df_country_ind['capacity_cumulative_avoided']), label='Cumulative avoided capacity from fossil fuels (RHS)', color='green')
ax2.set_ylabel('GW (Cumulative)', fontsize=15)
ax2.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Customize the x-axis to show ticks every 5 years
ax1.set_xticks([str(year) for year in range(2025, 2051, 5)])

# Set labels and title
plt.xlabel('Year', fontsize=15)
plt.title('Avoided Fossil Fuel Capacity in Power Sector in India: \n Current Policies vs Carbon Budget Consistent Net Zero*', fontsize=20, pad=60)

# Adding text
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', 
         transform=ax1.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelihood', 
         transform=ax1.transAxes, ha='center', fontsize=12)

# Adding legends for both lines
fig.legend(loc='upper left', fontsize=12, bbox_to_anchor=(0.13, 0.85))

# Show the plot
plt.show()





# --------------
# 5.4 TURKEYE
# Plotting
fig, ax1 = plt.subplots(figsize=(12, 8))

# Plot the first line on the primary y-axis
ax1.plot(df_country_tur.index, abs(df_country_tur['capacity_annaul_avoided']), label='Annual avoided capacity from fossil fuels (LHS)', color='blue')
ax1.set_ylabel('MW (Annual)', fontsize=15)

# Create a secondary y-axis
ax2 = ax1.twinx()
ax2.plot(df_country_tur.index, abs(df_country_tur['capacity_cumulative_avoided']), label='Cumulative avoided capacity from fossil fuels (RHS)', color='green')
ax2.set_ylabel('GW (Cumulative)', fontsize=15)
ax2.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Customize the x-axis to show ticks every 5 years
ax1.set_xticks([str(year) for year in range(2025, 2051, 5)])

# Set labels and title
plt.xlabel('Year', fontsize=15)
plt.title('Avoided Fossil Fuel Capacity in Power Sector in Turkeye: \n Current Policies vs Carbon Budget Consistent Net Zero*', fontsize=20, pad=60)

# Adding text
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', 
         transform=ax1.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelihood', 
         transform=ax1.transAxes, ha='center', fontsize=12)

# Adding legends for both lines
fig.legend(loc='upper left', fontsize=12, bbox_to_anchor=(0.13, 0.85))

# Show the plot
plt.show()





# --------------
# 5.5 USA
# Plotting
fig, ax1 = plt.subplots(figsize=(12, 8))

# Plot the first line on the primary y-axis
ax1.plot(df_country_usa.index, abs(df_country_usa['capacity_annaul_avoided']), label='Annual avoided capacity from fossil fuels (LHS)', color='blue')
ax1.set_ylabel('MW (Annual)', fontsize=15)

# Create a secondary y-axis
ax2 = ax1.twinx()
ax2.plot(df_country_usa.index, abs(df_country_usa['capacity_cumulative_avoided']), label='Cumulative avoided capacity from fossil fuels (RHS)', color='green')
ax2.set_ylabel('GW (Cumulative)', fontsize=15)
ax2.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Customize the x-axis to show ticks every 5 years
ax1.set_xticks([str(year) for year in range(2025, 2051, 5)])

# Set labels and title
plt.xlabel('Year', fontsize=15)
plt.title('Avoided Fossil Fuel Capacity in Power Sector in USA: \n Current Policies vs Carbon Budget Consistent Net Zero*', fontsize=20, pad=60)

# Adding text
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', 
         transform=ax1.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelihood', 
         transform=ax1.transAxes, ha='center', fontsize=12)

# Adding legends for both lines
fig.legend(loc='upper left', fontsize=12, bbox_to_anchor=(0.13, 0.85))

# Show the plot
plt.show()





# --------------
# 5.6 VIETNAM
# Plotting
fig, ax1 = plt.subplots(figsize=(12, 8))

# Plot the first line on the primary y-axis
ax1.plot(df_country_vnm.index, abs(df_country_vnm['capacity_annaul_avoided']), label='Annual avoided capacity from fossil fuels (LHS)', color='blue')
ax1.set_ylabel('MW (Annual)', fontsize=15)

# Create a secondary y-axis
ax2 = ax1.twinx()
ax2.plot(df_country_vnm.index, abs(df_country_vnm['capacity_cumulative_avoided']), label='Cumulative avoided capacity from fossil fuels (RHS)', color='green')
ax2.set_ylabel('GW (Cumulative)', fontsize=15)
ax2.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Customize the x-axis to show ticks every 5 years
ax1.set_xticks([str(year) for year in range(2025, 2051, 5)])

# Set labels and title
plt.xlabel('Year', fontsize=15)
plt.title('Avoided Fossil Fuel Capacity in Power Sector in Vietnam: \n Current Policies vs Carbon Budget Consistent Net Zero*', fontsize=20, pad=60)

# Adding text
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', 
         transform=ax1.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelihood', 
         transform=ax1.transAxes, ha='center', fontsize=12)

# Adding legends for both lines
fig.legend(loc='upper left', fontsize=12, bbox_to_anchor=(0.13, 0.85))

# Show the plot
plt.show()





# --------------
# 5.7 GLOBAL
# Plotting
fig, ax1 = plt.subplots(figsize=(12, 8))

# Plot the first line on the primary y-axis
ax1.plot(df_country_global.index, abs(df_country_global['capacity_annaul_avoided']), label='Annual avoided capacity from fossil fuels (LHS)', color='blue')
ax1.set_ylabel('MW (Annual)', fontsize=15)

# Create a secondary y-axis
ax2 = ax1.twinx()
ax2.plot(df_country_global.index, abs(df_country_global['capacity_cumulative_avoided']), label='Cumulative avoided capacity from fossil fuels (RHS)', color='green')
ax2.set_ylabel('GW (Cumulative)', fontsize=15)
ax2.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Customize the x-axis to show ticks every 5 years
ax1.set_xticks([str(year) for year in range(2025, 2051, 5)])

# Set labels and title
plt.xlabel('Year', fontsize=15)
plt.title('Avoided Fossil Fuel Capacity in Power Sector Globally: \n Current Policies vs Carbon Budget Consistent Net Zero*', fontsize=20, pad=60)

# Adding text
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', 
         transform=ax1.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelihood', 
         transform=ax1.transAxes, ha='center', fontsize=12)

# Adding legends for both lines
fig.legend(loc='upper left', fontsize=12, bbox_to_anchor=(0.13, 0.85))

# Show the plot
plt.show()










##################################################################################################
##################### SECTION 6: BY FUEL: EMISSIONS ##############################################
##################################################################################################

# --------------
# 6.1 GERMANY
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the lines
# Plot each fuel type
for fuel in df_emissions_currentpolicy_deu['fuel_type'].unique():
    fuel_data = df_emissions_currentpolicy_deu[df_emissions_currentpolicy_deu['fuel_type'] == fuel]
    plt.plot(years_columns, fuel_data.iloc[0,8:], color = colors.get(fuel, 'grey'), linestyle=':')  # Extract the correct row and year data

for fuel in df_emissions_nz1550v2_deu['fuel_type'].unique():
    fuel_data = df_emissions_nz1550v2_deu[df_emissions_nz1550v2_deu['fuel_type'] == fuel]
    plt.plot(years_columns, fuel_data.iloc[0,8:], label=fuel, color = colors.get(fuel, 'grey'))  # Extract the correct row and year data
    
# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Set y-axis formatter to display values in thousands
ax = plt.gca()

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('MtCO2', fontsize = 15)
plt.title('Annual Emissions from Power Sector by Scenario: Germany', fontsize=20, pad=60)
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.1, 0.96, 'Solid line:', transform=ax.transAxes, ha='center', fontsize=12, fontweight='bold')
plt.text(0.315, 0.96, 'Carbon budget consistent Net Zero*', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.1055, 0.93, 'Dotted line:', transform=ax.transAxes, ha='center', fontsize=12, fontweight='bold')
plt.text(0.235, 0.93, 'Current Policies', transform=ax.transAxes, ha='center', fontsize=12)
ax.legend(loc='upper right', fontsize=12)

plt.show()





# --------------
# 6.2 INDONESIA
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the lines
# Plot each fuel type
for fuel in df_emissions_currentpolicy_idn['fuel_type'].unique():
    fuel_data = df_emissions_currentpolicy_idn[df_emissions_currentpolicy_idn['fuel_type'] == fuel]
    plt.plot(years_columns, fuel_data.iloc[0,8:], color = colors.get(fuel, 'grey'), linestyle=':')  # Extract the correct row and year data

for fuel in df_emissions_nz1550v2_idn['fuel_type'].unique():
    fuel_data = df_emissions_nz1550v2_idn[df_emissions_nz1550v2_idn['fuel_type'] == fuel]
    plt.plot(years_columns, fuel_data.iloc[0,8:], label=fuel, color = colors.get(fuel, 'grey'))  # Extract the correct row and year data
    
# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Set y-axis formatter to display values in thousands
ax = plt.gca()

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('MtCO2', fontsize = 15)
plt.title('Annual Emissions from Power Sector by Scenario: Indonesia', fontsize=20, pad=60)
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.1, 0.96, 'Solid line:', transform=ax.transAxes, ha='center', fontsize=12, fontweight='bold')
plt.text(0.315, 0.96, 'Carbon budget consistent Net Zero*', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.1055, 0.93, 'Dotted line:', transform=ax.transAxes, ha='center', fontsize=12, fontweight='bold')
plt.text(0.235, 0.93, 'Current Policies', transform=ax.transAxes, ha='center', fontsize=12)
ax.legend(loc='upper right', fontsize=12)

plt.show()





# --------------
# 6.3 INDIA
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the lines
# Plot each fuel type
for fuel in df_emissions_currentpolicy_ind['fuel_type'].unique():
    fuel_data = df_emissions_currentpolicy_ind[df_emissions_currentpolicy_ind['fuel_type'] == fuel]
    plt.plot(years_columns, fuel_data.iloc[0,8:], color = colors.get(fuel, 'grey'), linestyle=':')  # Extract the correct row and year data

for fuel in df_emissions_nz1550v2_ind['fuel_type'].unique():
    fuel_data = df_emissions_nz1550v2_ind[df_emissions_nz1550v2_ind['fuel_type'] == fuel]
    plt.plot(years_columns, fuel_data.iloc[0,8:], label=fuel, color = colors.get(fuel, 'grey'))  # Extract the correct row and year data
    
# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Set y-axis formatter to display values in thousands
ax = plt.gca()

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('MtCO2', fontsize = 15)
plt.title('Annual Emissions from Power Sector by Scenario: India', fontsize=20, pad=60)
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.1, 0.96, 'Solid line:', transform=ax.transAxes, ha='center', fontsize=12, fontweight='bold')
plt.text(0.315, 0.96, 'Carbon budget consistent Net Zero*', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.1055, 0.93, 'Dotted line:', transform=ax.transAxes, ha='center', fontsize=12, fontweight='bold')
plt.text(0.235, 0.93, 'Current Policies', transform=ax.transAxes, ha='center', fontsize=12)
ax.legend(loc='upper right', fontsize=12)

plt.show()





# --------------
# 6.4 TURKEYE
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the lines
# Plot each fuel type
for fuel in df_emissions_currentpolicy_tur['fuel_type'].unique():
    fuel_data = df_emissions_currentpolicy_tur[df_emissions_currentpolicy_tur['fuel_type'] == fuel]
    plt.plot(years_columns, fuel_data.iloc[0,8:], color = colors.get(fuel, 'grey'), linestyle=':')  # Extract the correct row and year data

for fuel in df_emissions_nz1550v2_tur['fuel_type'].unique():
    fuel_data = df_emissions_nz1550v2_tur[df_emissions_nz1550v2_tur['fuel_type'] == fuel]
    plt.plot(years_columns, fuel_data.iloc[0,8:], label=fuel, color = colors.get(fuel, 'grey'))  # Extract the correct row and year data
    
# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Set y-axis formatter to display values in thousands
ax = plt.gca()

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('MtCO2', fontsize = 15)
plt.title('Annual Emissions from Power Sector by Scenario: Turkeye', fontsize=20, pad=60)
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.1, 0.96, 'Solid line:', transform=ax.transAxes, ha='center', fontsize=12, fontweight='bold')
plt.text(0.315, 0.96, 'Carbon budget consistent Net Zero*', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.1055, 0.93, 'Dotted line:', transform=ax.transAxes, ha='center', fontsize=12, fontweight='bold')
plt.text(0.235, 0.93, 'Current Policies', transform=ax.transAxes, ha='center', fontsize=12)
ax.legend(loc='upper right', fontsize=12)

plt.show()





# --------------
# 6.5 USA
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the lines
# Plot each fuel type
for fuel in df_emissions_currentpolicy_usa['fuel_type'].unique():
    fuel_data = df_emissions_currentpolicy_usa[df_emissions_currentpolicy_usa['fuel_type'] == fuel]
    plt.plot(years_columns, fuel_data.iloc[0,8:], color = colors.get(fuel, 'grey'), linestyle=':')  # Extract the correct row and year data

for fuel in df_emissions_nz1550v2_usa['fuel_type'].unique():
    fuel_data = df_emissions_nz1550v2_usa[df_emissions_nz1550v2_usa['fuel_type'] == fuel]
    plt.plot(years_columns, fuel_data.iloc[0,8:], label=fuel, color = colors.get(fuel, 'grey'))  # Extract the correct row and year data
    
# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Set y-axis formatter to display values in thousands
ax = plt.gca()

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('MtCO2', fontsize = 15)
plt.title('Annual Emissions from Power Sector by Scenario: USA', fontsize=20, pad=60)
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.1, 0.96, 'Solid line:', transform=ax.transAxes, ha='center', fontsize=12, fontweight='bold')
plt.text(0.315, 0.96, 'Carbon budget consistent Net Zero*', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.1055, 0.93, 'Dotted line:', transform=ax.transAxes, ha='center', fontsize=12, fontweight='bold')
plt.text(0.235, 0.93, 'Current Policies', transform=ax.transAxes, ha='center', fontsize=12)
ax.legend(loc='upper right', fontsize=12)

plt.show()





# --------------
# 6.6 VIETNAM
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the lines
# Plot each fuel type
for fuel in df_emissions_currentpolicy_vnm['fuel_type'].unique():
    fuel_data = df_emissions_currentpolicy_vnm[df_emissions_currentpolicy_vnm['fuel_type'] == fuel]
    plt.plot(years_columns, fuel_data.iloc[0,8:], color = colors.get(fuel, 'grey'), linestyle=':')  # Extract the correct row and year data

for fuel in df_emissions_nz1550v2_vnm['fuel_type'].unique():
    fuel_data = df_emissions_nz1550v2_vnm[df_emissions_nz1550v2_vnm['fuel_type'] == fuel]
    plt.plot(years_columns, fuel_data.iloc[0,8:], label=fuel, color = colors.get(fuel, 'grey'))  # Extract the correct row and year data
    
# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Set y-axis formatter to display values in thousands
ax = plt.gca()

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('MtCO2', fontsize = 15)
plt.title('Annual Emissions from Power Sector by Scenario: Vietnam', fontsize=20, pad=60)
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.1, 0.96, 'Solid line:', transform=ax.transAxes, ha='center', fontsize=12, fontweight='bold')
plt.text(0.315, 0.96, 'Carbon budget consistent Net Zero*', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.1055, 0.93, 'Dotted line:', transform=ax.transAxes, ha='center', fontsize=12, fontweight='bold')
plt.text(0.235, 0.93, 'Current Policies', transform=ax.transAxes, ha='center', fontsize=12)
ax.legend(loc='upper right', fontsize=12)

plt.show()





# --------------
# 6.7 GLOBAL
# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the lines
# Plot each fuel type
for fuel in df_emissions_currentpolicy_global['fuel_type'].unique():
    fuel_data = df_emissions_currentpolicy_global[df_emissions_currentpolicy_global['fuel_type'] == fuel]
    plt.plot(years_columns, fuel_data.iloc[0,1:], color = colors.get(fuel, 'grey'), linestyle=':')  # Extract the correct row and year data

for fuel in df_emissions_nz1550v2_global['fuel_type'].unique():
    fuel_data = df_emissions_nz1550v2_global[df_emissions_nz1550v2_global['fuel_type'] == fuel]
    plt.plot(years_columns, fuel_data.iloc[0,1:], label=fuel, color = colors.get(fuel, 'grey'))  # Extract the correct row and year data
    
# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Set y-axis formatter to display values in thousands
ax = plt.gca()

# Adding labels and legend
plt.xlabel('Year',fontsize = 15 )
plt.ylabel('MtCO2', fontsize = 15)
plt.title('Annual Emissions from Power Sector by Scenario: Global', fontsize=20, pad=60)
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelyhood', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.1, 0.96, 'Solid line:', transform=ax.transAxes, ha='center', fontsize=12, fontweight='bold')
plt.text(0.315, 0.96, 'Carbon budget consistent Net Zero*', transform=ax.transAxes, ha='center', fontsize=12)
plt.text(0.1055, 0.93, 'Dotted line:', transform=ax.transAxes, ha='center', fontsize=12, fontweight='bold')
plt.text(0.235, 0.93, 'Current Policies', transform=ax.transAxes, ha='center', fontsize=12)
ax.legend(loc='upper right', fontsize=12)

plt.show()










##################################################################################################
##################### SECTION 7: BY FUEL: AVOIDED CAPACITY --- ANNUAL & CUMULATIVE ###############
##################################################################################################

# --------------
# 7.1 GERMANY
# Plotting
fig, ax1 = plt.subplots(figsize=(12, 8))

# Plot the lines
# Plot the first set of lines (dotted) on the primary y-axis
for fuel in df_byfuel_avoided_annual_deu['fuel_type'].unique():
    fuel_data = df_byfuel_avoided_annual_deu[df_byfuel_avoided_annual_deu['fuel_type'] == fuel]
    ax1.plot(years_columns, abs(fuel_data.iloc[0, 8:]), color=colors.get(fuel, 'grey'), linestyle=':')

# Customize the x-axis for the primary y-axis
ax1.set_xticks([str(year) for year in range(2025, 2051, 5)])

ax1.set_xlabel('Year', fontsize=15)
ax1.set_ylabel('MtCO2 (Annual)', fontsize=15)
ax1.tick_params(axis='y', labelcolor='grey')

# Create a secondary y-axis
ax2 = ax1.twinx()

# Plot the second set of lines (solid) on the secondary y-axis
for fuel in df_byfuel_avoided_cumulative_deu['fuel_type'].unique():
    fuel_data = df_byfuel_avoided_cumulative_deu[df_byfuel_avoided_cumulative_deu['fuel_type'] == fuel]
    ax2.plot(years_columns, abs(fuel_data.iloc[0, 8:]), color=colors.get(fuel, 'grey'), label=fuel)

# Customize the secondary y-axis
ax2.set_ylabel('GtCO2 (Cumulative)', fontsize=15)
ax2.tick_params(axis='y', labelcolor='grey')
ax2.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Adding labels and titles
plt.title('Avoided Fossil Fuel Capacity in Power Sector in Germany: \n Current Policies vs Carbon Budget Consistent Net Zero*', fontsize=20, pad=60)

# Add legends for both axes
fig.legend(loc='lower right', fontsize=12, bbox_to_anchor=(0.9, 0.5))

# Adding text
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', 
         transform=ax1.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelihood', 
         transform=ax1.transAxes, ha='center', fontsize=12)
plt.text(0.1, 0.96, 'Solid line:', transform=ax1.transAxes, ha='center', fontsize=12, fontweight='bold')
plt.text(0.247, 0.96, 'Cumulative (RHS)', transform=ax1.transAxes, ha='center', fontsize=12)
plt.text(0.106, 0.93, 'Dotted line:', transform=ax1.transAxes, ha='center', fontsize=12, fontweight='bold')
plt.text(0.23, 0.93, 'Annual (LHS)', transform=ax1.transAxes, ha='center', fontsize=12)

# Show the plot
plt.show()





# --------------
# 7.2 INDONESIA
# Plotting
fig, ax1 = plt.subplots(figsize=(12, 8))

# Plot the lines
# Plot the first set of lines (dotted) on the primary y-axis
for fuel in df_byfuel_avoided_annual_idn['fuel_type'].unique():
    fuel_data = df_byfuel_avoided_annual_idn[df_byfuel_avoided_annual_idn['fuel_type'] == fuel]
    ax1.plot(years_columns, abs(fuel_data.iloc[0, 8:]), color=colors.get(fuel, 'grey'), linestyle=':')

# Customize the x-axis for the primary y-axis
ax1.set_xticks([str(year) for year in range(2025, 2051, 5)])

ax1.set_xlabel('Year', fontsize=15)
ax1.set_ylabel('MtCO2 (Annual)', fontsize=15)
ax1.tick_params(axis='y', labelcolor='grey')

# Create a secondary y-axis
ax2 = ax1.twinx()

# Plot the second set of lines (solid) on the secondary y-axis
for fuel in df_byfuel_avoided_cumulative_idn['fuel_type'].unique():
    fuel_data = df_byfuel_avoided_cumulative_idn[df_byfuel_avoided_cumulative_idn['fuel_type'] == fuel]
    ax2.plot(years_columns, abs(fuel_data.iloc[0, 8:]), color=colors.get(fuel, 'grey'), label=fuel)

# Customize the secondary y-axis
ax2.set_ylabel('GtCO2 (Cumulative)', fontsize=15)
ax2.tick_params(axis='y', labelcolor='grey')
ax2.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Adding labels and titles
plt.title('Avoided Fossil Fuel Capacity in Power Sector in Indonesia: \n Current Policies vs Carbon Budget Consistent Net Zero*', fontsize=20, pad=60)

# Add legends for both axes
fig.legend(loc='lower right', fontsize=12, bbox_to_anchor=(0.9, 0.5))

# Adding text
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', 
         transform=ax1.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelihood', 
         transform=ax1.transAxes, ha='center', fontsize=12)
plt.text(0.1, 0.96, 'Solid line:', transform=ax1.transAxes, ha='center', fontsize=12, fontweight='bold')
plt.text(0.247, 0.96, 'Cumulative (RHS)', transform=ax1.transAxes, ha='center', fontsize=12)
plt.text(0.106, 0.93, 'Dotted line:', transform=ax1.transAxes, ha='center', fontsize=12, fontweight='bold')
plt.text(0.23, 0.93, 'Annual (LHS)', transform=ax1.transAxes, ha='center', fontsize=12)

# Show the plot
plt.show()





# --------------
# 7.3 INDIA
# Plotting
fig, ax1 = plt.subplots(figsize=(12, 8))

# Plot the lines
# Plot the first set of lines (dotted) on the primary y-axis
for fuel in df_byfuel_avoided_annual_ind['fuel_type'].unique():
    fuel_data = df_byfuel_avoided_annual_ind[df_byfuel_avoided_annual_ind['fuel_type'] == fuel]
    ax1.plot(years_columns, abs(fuel_data.iloc[0, 8:]), color=colors.get(fuel, 'grey'), linestyle=':')

# Customize the x-axis for the primary y-axis
ax1.set_xticks([str(year) for year in range(2025, 2051, 5)])

ax1.set_xlabel('Year', fontsize=15)
ax1.set_ylabel('MtCO2 (Annual)', fontsize=15)
ax1.tick_params(axis='y', labelcolor='grey')

# Create a secondary y-axis
ax2 = ax1.twinx()

# Plot the second set of lines (solid) on the secondary y-axis
for fuel in df_byfuel_avoided_cumulative_ind['fuel_type'].unique():
    fuel_data = df_byfuel_avoided_cumulative_ind[df_byfuel_avoided_cumulative_ind['fuel_type'] == fuel]
    ax2.plot(years_columns, abs(fuel_data.iloc[0, 8:]), color=colors.get(fuel, 'grey'), label=fuel)

# Customize the secondary y-axis
ax2.set_ylabel('GtCO2 (Cumulative)', fontsize=15)
ax2.tick_params(axis='y', labelcolor='grey')
ax2.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Adding labels and titles
plt.title('Avoided Fossil Fuel Capacity in Power Sector in India: \n Current Policies vs Carbon Budget Consistent Net Zero*', fontsize=20, pad=60)

# Add legends for both axes
fig.legend(loc='lower right', fontsize=12, bbox_to_anchor=(0.9, 0.5))

# Adding text
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', 
         transform=ax1.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelihood', 
         transform=ax1.transAxes, ha='center', fontsize=12)
plt.text(0.1, 0.96, 'Solid line:', transform=ax1.transAxes, ha='center', fontsize=12, fontweight='bold')
plt.text(0.247, 0.96, 'Cumulative (RHS)', transform=ax1.transAxes, ha='center', fontsize=12)
plt.text(0.106, 0.93, 'Dotted line:', transform=ax1.transAxes, ha='center', fontsize=12, fontweight='bold')
plt.text(0.23, 0.93, 'Annual (LHS)', transform=ax1.transAxes, ha='center', fontsize=12)

# Show the plot
plt.show()





# --------------
# 7.4 TURKEYE
# Plotting
fig, ax1 = plt.subplots(figsize=(12, 8))

# Plot the lines
# Plot the first set of lines (dotted) on the primary y-axis
for fuel in df_byfuel_avoided_annual_tur['fuel_type'].unique():
    fuel_data = df_byfuel_avoided_annual_tur[df_byfuel_avoided_annual_tur['fuel_type'] == fuel]
    ax1.plot(years_columns, abs(fuel_data.iloc[0, 8:]), color=colors.get(fuel, 'grey'), linestyle=':')

# Customize the x-axis for the primary y-axis
ax1.set_xticks([str(year) for year in range(2025, 2051, 5)])

ax1.set_xlabel('Year', fontsize=15)
ax1.set_ylabel('MtCO2 (Annual)', fontsize=15)
ax1.tick_params(axis='y', labelcolor='grey')

# Create a secondary y-axis
ax2 = ax1.twinx()

# Plot the second set of lines (solid) on the secondary y-axis
for fuel in df_byfuel_avoided_cumulative_tur['fuel_type'].unique():
    fuel_data = df_byfuel_avoided_cumulative_tur[df_byfuel_avoided_cumulative_tur['fuel_type'] == fuel]
    ax2.plot(years_columns, abs(fuel_data.iloc[0, 8:]), color=colors.get(fuel, 'grey'), label=fuel)

# Customize the secondary y-axis
ax2.set_ylabel('GtCO2 (Cumulative)', fontsize=15)
ax2.tick_params(axis='y', labelcolor='grey')
ax2.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Adding labels and titles
plt.title('Avoided Fossil Fuel Capacity in Power Sector in Turkeye: \n Current Policies vs Carbon Budget Consistent Net Zero*', fontsize=20, pad=60)

# Add legends for both axes
fig.legend(loc='lower right', fontsize=12, bbox_to_anchor=(0.9, 0.5))

# Adding text
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', 
         transform=ax1.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelihood', 
         transform=ax1.transAxes, ha='center', fontsize=12)
plt.text(0.1, 0.96, 'Solid line:', transform=ax1.transAxes, ha='center', fontsize=12, fontweight='bold')
plt.text(0.247, 0.96, 'Cumulative (RHS)', transform=ax1.transAxes, ha='center', fontsize=12)
plt.text(0.106, 0.93, 'Dotted line:', transform=ax1.transAxes, ha='center', fontsize=12, fontweight='bold')
plt.text(0.23, 0.93, 'Annual (LHS)', transform=ax1.transAxes, ha='center', fontsize=12)

# Show the plot
plt.show()





# --------------
# 7.5 USA
# Plotting
fig, ax1 = plt.subplots(figsize=(12, 8))

# Plot the lines
# Plot the first set of lines (dotted) on the primary y-axis
for fuel in df_byfuel_avoided_annual_usa['fuel_type'].unique():
    fuel_data = df_byfuel_avoided_annual_usa[df_byfuel_avoided_annual_usa['fuel_type'] == fuel]
    ax1.plot(years_columns, abs(fuel_data.iloc[0, 8:]), color=colors.get(fuel, 'grey'), linestyle=':')

# Customize the x-axis for the primary y-axis
ax1.set_xticks([str(year) for year in range(2025, 2051, 5)])

ax1.set_xlabel('Year', fontsize=15)
ax1.set_ylabel('MtCO2 (Annual)', fontsize=15)
ax1.tick_params(axis='y', labelcolor='grey')

# Create a secondary y-axis
ax2 = ax1.twinx()

# Plot the second set of lines (solid) on the secondary y-axis
for fuel in df_byfuel_avoided_cumulative_usa['fuel_type'].unique():
    fuel_data = df_byfuel_avoided_cumulative_usa[df_byfuel_avoided_cumulative_usa['fuel_type'] == fuel]
    ax2.plot(years_columns, abs(fuel_data.iloc[0, 8:]), color=colors.get(fuel, 'grey'), label=fuel)

# Customize the secondary y-axis
ax2.set_ylabel('GtCO2 (Cumulative)', fontsize=15)
ax2.tick_params(axis='y', labelcolor='grey')
ax2.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Adding labels and titles
plt.title('Avoided Fossil Fuel Capacity in Power Sector in USA: \n Current Policies vs Carbon Budget Consistent Net Zero*', fontsize=20, pad=60)

# Add legends for both axes
fig.legend(loc='lower right', fontsize=12, bbox_to_anchor=(0.9, 0.5))

# Adding text
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', 
         transform=ax1.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelihood', 
         transform=ax1.transAxes, ha='center', fontsize=12)
plt.text(0.1, 0.96, 'Solid line:', transform=ax1.transAxes, ha='center', fontsize=12, fontweight='bold')
plt.text(0.247, 0.96, 'Cumulative (RHS)', transform=ax1.transAxes, ha='center', fontsize=12)
plt.text(0.106, 0.93, 'Dotted line:', transform=ax1.transAxes, ha='center', fontsize=12, fontweight='bold')
plt.text(0.23, 0.93, 'Annual (LHS)', transform=ax1.transAxes, ha='center', fontsize=12)

# Show the plot
plt.show()





# --------------
# 7.6 VIETNAM
# Plotting
fig, ax1 = plt.subplots(figsize=(12, 8))

# Plot the lines
# Plot the first set of lines (dotted) on the primary y-axis
for fuel in df_byfuel_avoided_annual_vnm['fuel_type'].unique():
    fuel_data = df_byfuel_avoided_annual_vnm[df_byfuel_avoided_annual_vnm['fuel_type'] == fuel]
    ax1.plot(years_columns, abs(fuel_data.iloc[0, 8:]), color=colors.get(fuel, 'grey'), linestyle=':')

# Customize the x-axis for the primary y-axis
ax1.set_xticks([str(year) for year in range(2025, 2051, 5)])

ax1.set_xlabel('Year', fontsize=15)
ax1.set_ylabel('MtCO2 (Annual)', fontsize=15)
ax1.tick_params(axis='y', labelcolor='grey')

# Create a secondary y-axis
ax2 = ax1.twinx()

# Plot the second set of lines (solid) on the secondary y-axis
for fuel in df_byfuel_avoided_cumulative_vnm['fuel_type'].unique():
    fuel_data = df_byfuel_avoided_cumulative_vnm[df_byfuel_avoided_cumulative_vnm['fuel_type'] == fuel]
    ax2.plot(years_columns, abs(fuel_data.iloc[0, 8:]), color=colors.get(fuel, 'grey'), label=fuel)

# Customize the secondary y-axis
ax2.set_ylabel('GtCO2 (Cumulative)', fontsize=15)
ax2.tick_params(axis='y', labelcolor='grey')
ax2.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Adding labels and titles
plt.title('Avoided Fossil Fuel Capacity in Power Sector in Vietnam: \n Current Policies vs Carbon Budget Consistent Net Zero*', fontsize=20, pad=60)

# Add legends for both axes
fig.legend(loc='lower right', fontsize=12, bbox_to_anchor=(0.9, 0.5))

# Adding text
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', 
         transform=ax1.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelihood', 
         transform=ax1.transAxes, ha='center', fontsize=12)
plt.text(0.1, 0.96, 'Solid line:', transform=ax1.transAxes, ha='center', fontsize=12, fontweight='bold')
plt.text(0.247, 0.96, 'Cumulative (RHS)', transform=ax1.transAxes, ha='center', fontsize=12)
plt.text(0.106, 0.93, 'Dotted line:', transform=ax1.transAxes, ha='center', fontsize=12, fontweight='bold')
plt.text(0.23, 0.93, 'Annual (LHS)', transform=ax1.transAxes, ha='center', fontsize=12)

# Show the plot
plt.show()





# --------------
# 7.7 GLOBAL
# Plotting
fig, ax1 = plt.subplots(figsize=(12, 8))

# Plot the lines
# Plot the first set of lines (dotted) on the primary y-axis
for fuel in df_byfuel_avoided_annual_global['fuel_type'].unique():
    fuel_data = df_byfuel_avoided_annual_global[df_byfuel_avoided_annual_global['fuel_type'] == fuel]
    ax1.plot(years_columns, abs(fuel_data.iloc[0, 1:]), color=colors.get(fuel, 'grey'), linestyle=':')

# Customize the x-axis for the primary y-axis
ax1.set_xticks([str(year) for year in range(2025, 2051, 5)])

ax1.set_xlabel('Year', fontsize=15)
ax1.set_ylabel('MtCO2 (Annual)', fontsize=15)
ax1.tick_params(axis='y', labelcolor='grey')

# Create a secondary y-axis
ax2 = ax1.twinx()

# Plot the second set of lines (solid) on the secondary y-axis
for fuel in df_byfuel_avoided_cumulative_global['fuel_type'].unique():
    fuel_data = df_byfuel_avoided_cumulative_global[df_byfuel_avoided_cumulative_global['fuel_type'] == fuel]
    ax2.plot(years_columns, abs(fuel_data.iloc[0, 1:]), color=colors.get(fuel, 'grey'), label=fuel)

# Customize the secondary y-axis
ax2.set_ylabel('GtCO2 (Cumulative)', fontsize=15)
ax2.tick_params(axis='y', labelcolor='grey')
ax2.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Adding labels and titles
plt.title('Avoided Fossil Fuel Capacity in Power Sector Globally: \n Current Policies vs Carbon Budget Consistent Net Zero*', fontsize=20, pad=60)

# Add legends for both axes
fig.legend(loc='lower right', fontsize=12, bbox_to_anchor=(0.9, 0.5))

# Adding text
plt.text(0.5, 1.09, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', 
         transform=ax1.transAxes, ha='center', fontsize=12)
plt.text(0.5, 1.02, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions with global carbon budget \n limiting warming to 1.5°C with 50% likelihood', 
         transform=ax1.transAxes, ha='center', fontsize=12)
plt.text(0.1, 0.96, 'Solid line:', transform=ax1.transAxes, ha='center', fontsize=12, fontweight='bold')
plt.text(0.247, 0.96, 'Cumulative (RHS)', transform=ax1.transAxes, ha='center', fontsize=12)
plt.text(0.106, 0.93, 'Dotted line:', transform=ax1.transAxes, ha='center', fontsize=12, fontweight='bold')
plt.text(0.23, 0.93, 'Annual (LHS)', transform=ax1.transAxes, ha='center', fontsize=12)

# Show the plot
plt.show()











