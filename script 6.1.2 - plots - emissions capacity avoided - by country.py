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
import matplotlib.gridspec as gridspec
import scienceplots
import seaborn as sns
from matplotlib.ticker import MaxNLocator







# In[3]:
# directory & load data

directory = r'C:\Users\panah\OneDrive\Desktop\Work\2 - RA - Climate fin'
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

# Style
plt.style.use(['science'])

# Disable LaTeX rendering to avoid LaTeX-related errors
plt.rcParams['text.usetex'] = False

# Font and sizes
plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 10,
    'legend.fontsize': 8,
})


# Formatter function to convert values to thousands
# the values are in Mt, but diving the axis by 1000 to show in Gt
def thousands_formatter_0dec(x, pos):
    return f'{x/1000:.0f}'

def thousands_formatter_1dec(x, pos):
    return f'{x/1000:.1f}'

def thousands_formatter_2dec(x, pos):
    return f'{x/1000:.2f}'


# colors
colors = {
    'Coal': '#2E2E2E',  # Dark Gray/Black for Coal
    'Oil': '#A52A2A',  # Brown for Oil
    'Gas': '#87CEEB',  # Light Blue for Natural Gas
    'Current Policies': '#4169E1',  # Royal Blue for Current Policies
    'Net Zero 2050': '#FF8C00',  # Dark Orange for Net Zero 2050
    'Carbon Budget Consistent Net Zero': '#32CD32',  # Lime Green for Carbon Budget Consistent Net Zero
    'Annual': '#1E90FF',  # Dodger Blue for Annual Avoided Emissions
    'Cumulative': '#228B22'  # Forest Green for Cumulative Avoided Emissions
}        

    








##################################################################################################
##################### SECTION 1: ANNUAL EMISSISON ################################################
##################################################################################################

# Layout: 2 rows, 5 columns grid
fig = plt.figure(figsize=(15, 9))  # Adjusted figure size
gs = fig.add_gridspec(2, 5, height_ratios=[1, 1], width_ratios=[1, 1, 1, 1, 1])

# Function to plot each country
def plot_country(ax, df_country, country_name, loc, ylabel=None):
    ax.plot(df_country.index, df_country['ghg_annual_cp'], label='NGFS Current Policies', color=colors['Current Policies'])
    ax.plot(df_country.index, df_country['ghg_annual_nz'], label='NGFS Net Zero 2050', color=colors['Net Zero 2050'])
    ax.plot(df_country.index, df_country['ghg_annual_nznew'], label='Carbon budget consistent Net Zero*', color=colors['Carbon Budget Consistent Net Zero'])
    ax.set_xticks([str(year) for year in range(2030, 2051, 10)])
    ax.set_title(f'{country_name}', fontsize=14, fontweight='bold', pad=10)
    ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter_2dec))

    # Set the y-axis label if specified
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=12)
    
# Plot countries in a 5x2 layout

# First row
ax_global = fig.add_subplot(gs[0, 0])
plot_country(ax_global, df_country_global, 'Global', 'upper left', ylabel='GtCO2eq')

ax_emde = fig.add_subplot(gs[0, 1])
plot_country(ax_emde, df_country_emde, 'EMDEs', 'upper right')

ax_ind = fig.add_subplot(gs[0, 2])
plot_country(ax_ind, df_country_ind, 'India', 'upper left')

ax_usa = fig.add_subplot(gs[0, 3])
plot_country(ax_usa, df_country_usa, 'USA', 'upper left')

ax_vnm = fig.add_subplot(gs[0, 4])
plot_country(ax_vnm, df_country_vnm, 'Vietnam', 'upper left')

# Second row
ax_idn = fig.add_subplot(gs[1, 0])
plot_country(ax_idn, df_country_idn, 'Indonesia', 'upper left', ylabel='GtCO2eq')

ax_tur = fig.add_subplot(gs[1, 1])
plot_country(ax_tur, df_country_tur, 'Türkiye', 'upper right')

ax_deu = fig.add_subplot(gs[1, 2])
plot_country(ax_deu, df_country_deu, 'Germany', 'upper left')

ax_pol = fig.add_subplot(gs[1, 3])
plot_country(ax_pol, df_country_pol, 'Poland', 'upper left')

# Placeholder for additional chart
ax_kaz = fig.add_subplot(gs[1, 4])
plot_country(ax_kaz, df_country_kaz, 'Kazakhstan', 'upper left')  # Replace df_country_new with actual data

# Main title
fig.suptitle('Annual Emissions from Power Sector by Scenario', fontsize=16, fontweight='bold', y=0.98)

# Subtitle
fig.text(0.5, 0.93, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', ha='center', fontsize=12)
fig.text(0.5, 0.88, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions \n with global carbon budget limiting warming to 1.5°C with 50% likelihood', ha='center', fontsize=12)

# Legend for all charts
handles, labels = ax_emde.get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', ncol=3, bbox_to_anchor=(0.5, 0.05), fontsize=10)

# Adjust layout
plt.subplots_adjust(top=0.82, bottom=0.15, hspace=0.6, wspace=0.3)

# Show the plot
plt.show()










##################################################################################################
##################### SECTION 2: CUMULATIVE EMISSISON ############################################
##################################################################################################

# Layout: 2 rows, 5 columns grid
fig = plt.figure(figsize=(15, 9))  # Adjusted figure size
gs = fig.add_gridspec(2, 5, height_ratios=[1, 1], width_ratios=[1, 1, 1, 1, 1])

# Function to plot each country
def plot_country(ax, df_country, country_name, loc, ylabel=None):
    ax.plot(df_country.index, df_country['ghg_cumulative_cp'], label='NGFS Current Policies', color=colors['Current Policies'])
    ax.plot(df_country.index, df_country['ghg_cumulative_nz'], label='NGFS Net Zero 2050', color=colors['Net Zero 2050'])
    ax.plot(df_country.index, df_country['ghg_cumulative_nznew'], label='Carbon budget consistent Net Zero*', color=colors['Carbon Budget Consistent Net Zero'])
    ax.set_xticks([str(year) for year in range(2030, 2051, 10)])
    ax.set_title(f'{country_name}', fontsize=14, fontweight='bold', pad=10)
    ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter_1dec))

    # Set the y-axis label if specified
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=12)
    
# Plot countries in a 5x2 layout

# First row
ax_global = fig.add_subplot(gs[0, 0])
plot_country(ax_global, df_country_global, 'Global', 'upper left', ylabel='GtCO2eq')

ax_emde = fig.add_subplot(gs[0, 1])
plot_country(ax_emde, df_country_emde, 'EMDEs', 'upper right')

ax_ind = fig.add_subplot(gs[0, 2])
plot_country(ax_ind, df_country_ind, 'India', 'upper left')

ax_usa = fig.add_subplot(gs[0, 3])
plot_country(ax_usa, df_country_usa, 'USA', 'upper left')

ax_vnm = fig.add_subplot(gs[0, 4])
plot_country(ax_vnm, df_country_vnm, 'Vietnam', 'upper left')

# Second row
ax_idn = fig.add_subplot(gs[1, 0])
plot_country(ax_idn, df_country_idn, 'Indonesia', 'upper left', ylabel='GtCO2eq')

ax_tur = fig.add_subplot(gs[1, 1])
plot_country(ax_tur, df_country_tur, 'Türkiye', 'upper right')

ax_deu = fig.add_subplot(gs[1, 2])
plot_country(ax_deu, df_country_deu, 'Germany', 'upper left')

ax_pol = fig.add_subplot(gs[1, 3])
plot_country(ax_pol, df_country_pol, 'Poland', 'upper left')

# Placeholder for additional chart
ax_kaz = fig.add_subplot(gs[1, 4])
plot_country(ax_kaz, df_country_kaz, 'Kazakhstan', 'upper left')  # Replace df_country_new with actual data

# Main title
fig.suptitle('Cumulative Emissions from Power Sector by Scenario', fontsize=16, fontweight='bold', y=0.98)

# Subtitle
fig.text(0.5, 0.93, 'Cumulative emissions from current power plants in operation, using NGFS GCAM6 growth rates', ha='center', fontsize=12)
fig.text(0.5, 0.88, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions \n with global carbon budget limiting warming to 1.5°C with 50% likelihood', ha='center', fontsize=12)

# Legend for all charts
handles, labels = ax_emde.get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', ncol=3, bbox_to_anchor=(0.5, 0.05), fontsize=10)

# Adjust layout
plt.subplots_adjust(top=0.82, bottom=0.15, hspace=0.6, wspace=0.3)

# Show the plot
plt.show()










##################################################################################################
##################### SECTION 3: AVOIDED EMISSIONS ###############################################
##################################################################################################

# --------------
# ANNUAL

# Layout: 2 rows, 5 columns grid
fig = plt.figure(figsize=(15, 9))  # Adjusted figure size
gs = fig.add_gridspec(2, 5, height_ratios=[1, 1], width_ratios=[1, 1, 1, 1, 1])

# Function to plot each country with annual avoided emissions
def plot_country(ax, df_country, country_name, loc, ylabel=None):
    ax.plot(df_country.index, df_country['ghg_annaul_avoided'], color=colors['Annual'])
    ax.set_xticks([str(year) for year in range(2030, 2051, 10)])
    ax.set_title(f'{country_name}', fontsize=14, fontweight='bold', pad=10)
    ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter_2dec))

    # Set the y-axis label if specified
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=12)

# Plot countries in a 5x2 layout for annual avoided emissions

# First row
ax_global = fig.add_subplot(gs[0, 0])
plot_country(ax_global, df_country_global, 'Global', 'upper left', ylabel='GtCO2eq')

ax_emde = fig.add_subplot(gs[0, 1])
plot_country(ax_emde, df_country_emde, 'EMDEs', 'upper right')

ax_ind = fig.add_subplot(gs[0, 2])
plot_country(ax_ind, df_country_ind, 'India', 'upper left')

ax_usa = fig.add_subplot(gs[0, 3])
plot_country(ax_usa, df_country_usa, 'USA', 'upper left')

ax_vnm = fig.add_subplot(gs[0, 4])
plot_country(ax_vnm, df_country_vnm, 'Vietnam', 'upper left')

# Second row
ax_idn = fig.add_subplot(gs[1, 0])
plot_country(ax_idn, df_country_idn, 'Indonesia', 'upper left', ylabel='GtCO2eq')

ax_tur = fig.add_subplot(gs[1, 1])
plot_country(ax_tur, df_country_tur, 'Türkiye', 'upper right')

ax_deu = fig.add_subplot(gs[1, 2])
plot_country(ax_deu, df_country_deu, 'Germany', 'upper left')

ax_pol = fig.add_subplot(gs[1, 3])
plot_country(ax_pol, df_country_pol, 'Poland', 'upper left')

# Placeholder for additional chart
ax_kaz = fig.add_subplot(gs[1, 4])
plot_country(ax_kaz, df_country_kaz, 'Kazakhstan', 'upper left')  # Replace with actual data

# Main title
fig.suptitle('Annual Avoided Emissions from Power Sector by Scenario:\n Current Policies vs Carbon Budget Consistent Net Zero*', fontsize=16, fontweight='bold', y=0.98)

# Subtitle
fig.text(0.5, 0.90, 'Emissions from current power plants in operation projected using NGFS GCAM6 model growth rates', ha='center', fontsize=12)
fig.text(0.5, 0.85, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions \n with global carbon budget limiting warming to 1.5°C with 50% likelihood', ha='center', fontsize=12)

# Legend for all charts
handles, labels = ax_global.get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', ncol=3, bbox_to_anchor=(0.5, 0.07), fontsize=10)

# Adjust layout to bring the second row slightly higher
plt.subplots_adjust(top=0.78, bottom=0.15, hspace=0.45, wspace=0.3)

# Show the plot
plt.show()





# --------------
# CUMULATIVE

# Layout: 2 rows, 5 columns grid
fig = plt.figure(figsize=(15, 9))  # Adjusted figure size for 2x5 layout
gs = fig.add_gridspec(2, 5, height_ratios=[1, 1], width_ratios=[1, 1, 1, 1, 1])

# Function to plot each country with cumulative avoided emissions
def plot_country(ax, df_country, country_name, loc, ylabel=None):
    ax.plot(df_country.index, df_country['ghg_cumulative_avoided'], color=colors['Cumulative'])
    ax.set_xticks([str(year) for year in range(2030, 2051, 10)])
    ax.set_title(f'{country_name}', fontsize=14, fontweight='bold', pad=10)
    ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter_1dec))

    # Set the y-axis label if specified
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=12)
    
# Plot countries in a 5x2 layout for cumulative avoided emissions

# First row
ax_global = fig.add_subplot(gs[0, 0])
plot_country(ax_global, df_country_global, 'Global', 'upper left', ylabel='GtCO2')

ax_emde = fig.add_subplot(gs[0, 1])
plot_country(ax_emde, df_country_emde, 'EMDEs', 'upper right')

ax_ind = fig.add_subplot(gs[0, 2])
plot_country(ax_ind, df_country_ind, 'India', 'upper left')

ax_usa = fig.add_subplot(gs[0, 3])
plot_country(ax_usa, df_country_usa, 'USA', 'upper left')

ax_vnm = fig.add_subplot(gs[0, 4])
plot_country(ax_vnm, df_country_vnm, 'Vietnam', 'upper left')

# Second row
ax_idn = fig.add_subplot(gs[1, 0])
plot_country(ax_idn, df_country_idn, 'Indonesia', 'upper left', ylabel='GtCO2')

ax_tur = fig.add_subplot(gs[1, 1])
plot_country(ax_tur, df_country_tur, 'Türkiye', 'upper right')

ax_deu = fig.add_subplot(gs[1, 2])
plot_country(ax_deu, df_country_deu, 'Germany', 'upper left')

ax_pol = fig.add_subplot(gs[1, 3])
plot_country(ax_pol, df_country_pol, 'Poland', 'upper left')

# Placeholder for additional chart
ax_kaz = fig.add_subplot(gs[1, 4])
plot_country(ax_kaz, df_country_kaz, 'Kazakhstan', 'upper left')  # Replace with actual data if needed

# Main title
fig.suptitle('Cumulative Avoided Emissions from Power Sector by Scenario:\n Current Policies vs Carbon Budget Consistent Net Zero*', fontsize=16, fontweight='bold', y=0.98)

# Subtitle
fig.text(0.5, 0.90, 'Emissions from current power plants in operation projected using NGFS GCAM6 model growth rates', ha='center', fontsize=12)
fig.text(0.5, 0.85, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions \n with global carbon budget limiting warming to 1.5°C with 50% likelihood', ha='center', fontsize=12)

# Legend for all charts
handles, labels = ax_global.get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', ncol=3, bbox_to_anchor=(0.5, 0.07), fontsize=10)

# Adjust layout to bring the second row slightly higher
plt.subplots_adjust(top=0.78, bottom=0.15, hspace=0.45, wspace=0.3)

# Show the plot
plt.show()










##################################################################################################
##################### SECTION 4: ANNUAL CAPACITY #################################################
##################################################################################################

# Layout: 2 rows, 5 columns grid
fig = plt.figure(figsize=(15, 9))  # Adjusted figure size for 2x5 layout
gs = fig.add_gridspec(2, 5, height_ratios=[1, 1], width_ratios=[1, 1, 1, 1, 1])

# Function to plot each country with annual fossil fuel capacity
def plot_country(ax, df_country, country_name, loc, ylabel=None):
    ax.plot(df_country.index, df_country['capacity_annual_cp'], label='NGFS Current Policies', color=colors['Current Policies'])
    ax.plot(df_country.index, df_country['capacity_annual_nz'], label='NGFS Net Zero 2050', color=colors['Net Zero 2050'])
    ax.plot(df_country.index, df_country['capacity_annual_nznew'], label='Carbon budget consistent Net Zero*', color=colors['Carbon Budget Consistent Net Zero'])
    ax.set_xticks([str(year) for year in range(2030, 2051, 10)])
    ax.set_title(f'{country_name}', fontsize=14, fontweight='bold', pad=10)
    ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter_0dec))

    # Set the y-axis label if specified
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=12)
    
# Plot countries in a 5x2 layout for fossil fuel capacity

# First row
ax_global = fig.add_subplot(gs[0, 0])
plot_country(ax_global, df_country_global, 'Global', 'upper left', ylabel='GW')

ax_emde = fig.add_subplot(gs[0, 1])
plot_country(ax_emde, df_country_emde, 'EMDEs', 'upper right')

ax_ind = fig.add_subplot(gs[0, 2])
plot_country(ax_ind, df_country_ind, 'India', 'upper left')

ax_usa = fig.add_subplot(gs[0, 3])
plot_country(ax_usa, df_country_usa, 'USA', 'upper left')

ax_vnm = fig.add_subplot(gs[0, 4])
plot_country(ax_vnm, df_country_vnm, 'Vietnam', 'upper left')

# Second row
ax_idn = fig.add_subplot(gs[1, 0])
plot_country(ax_idn, df_country_idn, 'Indonesia', 'upper left', ylabel='GW')

ax_tur = fig.add_subplot(gs[1, 1])
plot_country(ax_tur, df_country_tur, 'Türkiye', 'upper right')

ax_deu = fig.add_subplot(gs[1, 2])
plot_country(ax_deu, df_country_deu, 'Germany', 'upper left')

ax_pol = fig.add_subplot(gs[1, 3])
plot_country(ax_pol, df_country_pol, 'Poland', 'upper left')

# Placeholder for additional chart
ax_kaz = fig.add_subplot(gs[1, 4])
plot_country(ax_kaz, df_country_kaz, 'Kazakhstan', 'upper left')  # Replace with actual data if needed

# Main title
fig.suptitle('Annual Fossil Fuel Capacity in Power Sector by Scenario', fontsize=16, fontweight='bold', y=0.98)

# Subtitle
fig.text(0.5, 0.93, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', ha='center', fontsize=12)
fig.text(0.5, 0.88, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions \n with global carbon budget limiting warming to 1.5°C with 50% likelihood', ha='center', fontsize=12)

# Legend for all charts
handles, labels = ax_global.get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', ncol=3, bbox_to_anchor=(0.5, 0.07), fontsize=10)

# Adjust layout to bring the second row slightly higher
plt.subplots_adjust(top=0.82, bottom=0.15, hspace=0.45, wspace=0.3)

# Show the plot
plt.show()










##################################################################################################
##################### SECTION 5: AVOIDED CAPACITY ################################################
##################################################################################################

# --------------
# ANNUAL

# Layout: 2 rows, 5 columns grid
fig = plt.figure(figsize=(15, 9))  # Adjusted figure size for 2x5 layout
gs = fig.add_gridspec(2, 5, height_ratios=[1, 1], width_ratios=[1, 1, 1, 1, 1])

# Function to plot each country with annual avoided fossil fuel capacity
def plot_country(ax, df_country, country_name, loc, ylabel=None):
    ax.plot(df_country.index, abs(df_country['capacity_annaul_avoided']), color=colors['Annual'])
    ax.set_xticks([str(year) for year in range(2030, 2051, 10)])
    ax.set_title(f'{country_name}', fontsize=14, fontweight='bold', pad=10)
    ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter_0dec))

    # Set the y-axis label if specified
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=12)
    
# Plot countries in a 5x2 layout for annual avoided fossil fuel capacity

# First row
ax_global = fig.add_subplot(gs[0, 0])
plot_country(ax_global, df_country_global, 'Global', 'upper left', ylabel='GW')

ax_emde = fig.add_subplot(gs[0, 1])
plot_country(ax_emde, df_country_emde, 'EMDEs', 'upper right')

ax_ind = fig.add_subplot(gs[0, 2])
plot_country(ax_ind, df_country_ind, 'India', 'upper left')

ax_usa = fig.add_subplot(gs[0, 3])
plot_country(ax_usa, df_country_usa, 'USA', 'upper left')

ax_vnm = fig.add_subplot(gs[0, 4])
plot_country(ax_vnm, df_country_vnm, 'Vietnam', 'upper left')

# Second row
ax_idn = fig.add_subplot(gs[1, 0])
plot_country(ax_idn, df_country_idn, 'Indonesia', 'upper left', ylabel='GW')

ax_tur = fig.add_subplot(gs[1, 1])
plot_country(ax_tur, df_country_tur, 'Türkiye', 'upper right')

ax_deu = fig.add_subplot(gs[1, 2])
plot_country(ax_deu, df_country_deu, 'Germany', 'upper left')

ax_pol = fig.add_subplot(gs[1, 3])
plot_country(ax_pol, df_country_pol, 'Poland', 'upper left')

# Placeholder for additional chart
ax_kaz = fig.add_subplot(gs[1, 4])
plot_country(ax_kaz, df_country_kaz, 'Kazakhstan', 'upper left')  # Replace with actual data if needed

# Main title
fig.suptitle('Annual Avoided Fossil Fuel Capacity in Power Sector:\n Current Policies vs Carbon Budget Consistent Net Zero*', fontsize=16, fontweight='bold', y=0.98)

# Subtitle
fig.text(0.5, 0.90, 'Avoided fossil fuel capacity from current power plants in operation, projected with NGFS GCAM6 model', ha='center', fontsize=12)
fig.text(0.5, 0.85, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions \n with global carbon budget limiting warming to 1.5°C with 50% likelihood', ha='center', fontsize=12)

# Legend for all charts
handles, labels = ax_global.get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', ncol=3, bbox_to_anchor=(0.5, 0.07), fontsize=10)

# Adjust layout to bring the second row slightly higher
plt.subplots_adjust(top=0.78, bottom=0.15, hspace=0.45, wspace=0.3)

# Show the plot
plt.show()







# --------------
# CUMULATIVE

# Layout: 2 rows, 5 columns grid
fig = plt.figure(figsize=(15, 9))  # Adjusted figure size for 2x5 layout
gs = fig.add_gridspec(2, 5, height_ratios=[1, 1], width_ratios=[1, 1, 1, 1, 1])

# Function to plot each country with cumulative avoided fossil fuel capacity
def plot_country(ax, df_country, country_name, ylabel=None):
    ax.plot(df_country.index, abs(df_country['capacity_cumulative_avoided']), color=colors['Cumulative'])
    ax.set_xticks([str(year) for year in range(2030, 2051, 10)])
    ax.set_title(f'{country_name}', fontsize=14, fontweight='bold', pad=10)
    ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter_0dec))

    # Set the y-axis label if specified
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=12)

# Plot countries in a 5x2 layout for cumulative avoided fossil fuel capacity

# First row
ax_global = fig.add_subplot(gs[0, 0])
plot_country(ax_global, df_country_global, 'Global', ylabel='GW')

ax_emde = fig.add_subplot(gs[0, 1])
plot_country(ax_emde, df_country_emde, 'EMDEs')

ax_ind = fig.add_subplot(gs[0, 2])
plot_country(ax_ind, df_country_ind, 'India')

ax_usa = fig.add_subplot(gs[0, 3])
plot_country(ax_usa, df_country_usa, 'USA')

ax_vnm = fig.add_subplot(gs[0, 4])
plot_country(ax_vnm, df_country_vnm, 'Vietnam')

# Second row
ax_idn = fig.add_subplot(gs[1, 0])
plot_country(ax_idn, df_country_idn, 'Indonesia', ylabel='GW')

ax_tur = fig.add_subplot(gs[1, 1])
plot_country(ax_tur, df_country_tur, 'Türkiye')

ax_deu = fig.add_subplot(gs[1, 2])
plot_country(ax_deu, df_country_deu, 'Germany')

ax_pol = fig.add_subplot(gs[1, 3])
plot_country(ax_pol, df_country_pol, 'Poland')

# Placeholder for additional chart
ax_kaz = fig.add_subplot(gs[1, 4])
plot_country(ax_kaz, df_country_kaz, 'Kazakhstan')  # Replace with actual data if needed

# Main title
fig.suptitle('Cumulative Avoided Fossil Fuel Capacity in Power Sector:\n Current Policies vs Carbon Budget Consistent Net Zero*', fontsize=16, fontweight='bold', y=0.98)

# Subtitle
fig.text(0.5, 0.90, 'Avoided fossil fuel capacity from current power plants in operation, projected with NGFS GCAM6 model', ha='center', fontsize=12)
fig.text(0.5, 0.85, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions \n with global carbon budget limiting warming to 1.5°C with 50% likelihood', ha='center', fontsize=12)

# Legend for all charts
handles, labels = ax_global.get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', ncol=3, bbox_to_anchor=(0.5, 0.07), fontsize=10)

# Adjust layout to bring the second row slightly higher
plt.subplots_adjust(top=0.78, bottom=0.15, hspace=0.45, wspace=0.3)

# Show the plot
plt.show()







##################################################################################################
##################### SECTION 6: BY FUEL: EMISSIONS ##############################################
##################################################################################################

# Ensure the years_columns array has the correct length for country data
years_columns_countries = years_columns[:len(df_emissions_currentpolicy_deu.columns[8:])]
years_columns_global = years_columns[:len(df_emissions_currentpolicy_global.columns[1:])]  # For global & emde, adjust the slicing

# Function to plot emissions by fuel type for each country or global
def plot_country_emissions(ax, df_current_policy, df_nz_policy, country_name, ylabel=None, is_global=False):
    # Adjust starting column based on whether it's global or country data
    start_col = 1 if is_global else 8  # Use 1 for global, 8 for countries
    years_columns = years_columns_global if is_global else years_columns_countries
    
    # Plot Current Policies (dotted lines)
    for fuel in df_current_policy['fuel_type'].unique():
        fuel_data = df_current_policy[df_current_policy['fuel_type'] == fuel]
        ax.plot(years_columns, fuel_data.iloc[0, start_col:], color=colors.get(fuel, 'grey'), linestyle=':', label=None)

    # Plot Net Zero Policy (solid lines)
    for fuel in df_nz_policy['fuel_type'].unique():
        fuel_data = df_nz_policy[df_nz_policy['fuel_type'] == fuel]
        ax.plot(years_columns, fuel_data.iloc[0, start_col:], color=colors.get(fuel, 'grey'), label=fuel)

    # Customize the x-axis to show ticks every 5 years
    ax.set_xticks([str(year) for year in range(2030, 2051, 10)])
    ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter_2dec))

    # Set title
    ax.set_title(f'{country_name}', fontsize=14, fontweight='bold', pad=10)

    # Set the y-axis label if specified
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=12)

# Layout: 2 rows, 5 columns grid
fig = plt.figure(figsize=(15, 9))  # Adjusted figure size for 2x5 layout
gs = fig.add_gridspec(2, 5, height_ratios=[1, 1], width_ratios=[1, 1, 1, 1, 1])

# First row
ax_global = fig.add_subplot(gs[0, 0])
plot_country_emissions(ax_global, df_emissions_currentpolicy_global, df_emissions_nz1550v2_global, 'Global', ylabel="GtCO2eq", is_global=True)

ax_emde = fig.add_subplot(gs[0, 1])
plot_country_emissions(ax_emde, df_emissions_currentpolicy_emde, df_emissions_nz1550v2_emde, 'EMDEs', is_global=True)

ax_ind = fig.add_subplot(gs[0, 2])
plot_country_emissions(ax_ind, df_emissions_currentpolicy_ind, df_emissions_nz1550v2_ind, 'India')

ax_usa = fig.add_subplot(gs[0, 3])
plot_country_emissions(ax_usa, df_emissions_currentpolicy_usa, df_emissions_nz1550v2_usa, 'USA')

ax_vnm = fig.add_subplot(gs[0, 4])
plot_country_emissions(ax_vnm, df_emissions_currentpolicy_vnm, df_emissions_nz1550v2_vnm, 'Vietnam')

# Second row
ax_idn = fig.add_subplot(gs[1, 0])
plot_country_emissions(ax_idn, df_emissions_currentpolicy_idn, df_emissions_nz1550v2_idn, 'Indonesia', ylabel="GtCO2eq")

ax_tur = fig.add_subplot(gs[1, 1])
plot_country_emissions(ax_tur, df_emissions_currentpolicy_tur, df_emissions_nz1550v2_tur, 'Türkiye')

ax_deu = fig.add_subplot(gs[1, 2])
plot_country_emissions(ax_deu, df_emissions_currentpolicy_deu, df_emissions_nz1550v2_deu, 'Germany')

ax_pol = fig.add_subplot(gs[1, 3])
plot_country_emissions(ax_pol, df_emissions_currentpolicy_pol, df_emissions_nz1550v2_pol, 'Poland')

ax_kaz = fig.add_subplot(gs[1, 4])
plot_country_emissions(ax_kaz, df_emissions_currentpolicy_kaz, df_emissions_nz1550v2_kaz, 'Kazakhstan')

# Main title
fig.suptitle('Annual Emissions from Power Sector by Scenario and Fuel Type', fontsize=16, fontweight='bold', y=0.98)

# Subtitle
fig.text(0.5, 0.93, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', ha='center', fontsize=12)
fig.text(0.5, 0.90, 'Solid line: Carbon budget consistent Net Zero* | Dotted line: Current Policies', ha='center', fontsize=12)
fig.text(0.5, 0.85, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions \n with global carbon budget limiting warming to 1.5°C with 50% likelihood', ha='center', fontsize=12)


# Legend for all charts (handles from one plot)
handles, labels = ax_global.get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', ncol=3, bbox_to_anchor=(0.5, 0.07), fontsize=10)

# Adjust the spacing to move the charts lower and create space between rows
plt.subplots_adjust(top=0.78, bottom=0.15, hspace=0.45, wspace=0.3)

# Show the plot
plt.show()













##################################################################################################
##################### SECTION 7: BY FUEL: AVOIDED CAPACITY --- ANNUAL & CUMULATIVE ###############
##################################################################################################

# --------------
# ANNUAL

# Ensure the years_columns array has the correct length for country and global data
years_columns_countries = years_columns[:len(df_byfuel_avoided_annual_deu.columns[8:])]
years_columns_global = years_columns[:len(df_byfuel_avoided_annual_global.columns[1:])]  # For global, adjust the slicing

# Function to plot avoided emissions by fuel type for each country or global
def plot_country_avoided_emissions(ax, df_annual, country_name, ylabel=None, is_global=False):
    # Adjust starting column based on whether it's global or country data
    start_col = 1 if is_global else 8  # Use 1 for global, 8 for countries
    years_columns = years_columns_global if is_global else years_columns_countries
    
    # Plot Annual avoided emissions (dotted lines) on primary y-axis
    for fuel in df_annual['fuel_type'].unique():
        fuel_data = df_annual[df_annual['fuel_type'] == fuel]
        ax.plot(years_columns, abs(fuel_data.iloc[0, start_col:]), color=colors.get(fuel, 'grey'), label=fuel)

    # Customize the x-axis for primary y-axis
    ax.set_xticks([str(year) for year in range(2030, 2051, 10)])
    ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter_0dec))

    # Set the title and labels
    ax.set_title(f'{country_name}', fontsize=14, fontweight='bold', pad=10)
    
    # Set the y-axis label if specified
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=12)

# Layout: 2 rows, 5 columns grid
fig = plt.figure(figsize=(15, 9))  # Adjusted figure size for 2x5 layout
gs = fig.add_gridspec(2, 5, height_ratios=[1, 1], width_ratios=[1, 1, 1, 1, 1])

# First row
ax_global = fig.add_subplot(gs[0, 0])
plot_country_avoided_emissions(ax_global, df_byfuel_avoided_annual_global, 'Global', ylabel="GW", is_global=True)

ax_emde = fig.add_subplot(gs[0, 1])
plot_country_avoided_emissions(ax_emde, df_byfuel_avoided_annual_emde, 'EMDEs', is_global=True)

ax_ind = fig.add_subplot(gs[0, 2])
plot_country_avoided_emissions(ax_ind, df_byfuel_avoided_annual_ind, 'India')

ax_usa = fig.add_subplot(gs[0, 3])
plot_country_avoided_emissions(ax_usa, df_byfuel_avoided_annual_usa, 'USA')

ax_vnm = fig.add_subplot(gs[0, 4])
plot_country_avoided_emissions(ax_vnm, df_byfuel_avoided_annual_vnm, 'Vietnam')

# Second row
ax_idn = fig.add_subplot(gs[1, 0])
plot_country_avoided_emissions(ax_idn, df_byfuel_avoided_annual_idn, 'Indonesia', ylabel="GW")

ax_tur = fig.add_subplot(gs[1, 1])
plot_country_avoided_emissions(ax_tur, df_byfuel_avoided_annual_tur, 'Türkiye')

ax_deu = fig.add_subplot(gs[1, 2])
plot_country_avoided_emissions(ax_deu, df_byfuel_avoided_annual_deu, 'Germany')

ax_pol = fig.add_subplot(gs[1, 3])
plot_country_avoided_emissions(ax_pol, df_byfuel_avoided_annual_pol, 'Poland')

ax_kaz = fig.add_subplot(gs[1, 4])
plot_country_avoided_emissions(ax_kaz, df_byfuel_avoided_annual_kaz, 'Kazakhstan')

# Main title
fig.suptitle('Annual Avoided Fossil Fuel Capacity in Power Sector:\n Current Policies vs Carbon Budget Consistent Net Zero*', fontsize=16, fontweight='bold', y=0.98)

# Subtitle
fig.text(0.5, 0.90, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', ha='center', fontsize=12)
fig.text(0.5, 0.85, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions \n with global carbon budget limiting warming to 1.5°C with 50% likelihood', ha='center', fontsize=12)

# Legend for all charts (handles from one plot)
handles, labels = ax_global.get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', ncol=3, bbox_to_anchor=(0.5, 0.07), fontsize=10)

# Adjust layout to bring the second row slightly higher
plt.subplots_adjust(top=0.78, bottom=0.15, hspace=0.45, wspace=0.3)

# Show the plot
plt.show()





# --------------
# CUMULATIVE

# Ensure the years_columns array has the correct length for country and global data
years_columns_countries = years_columns[:len(df_byfuel_avoided_annual_deu.columns[8:])]
years_columns_global = years_columns[:len(df_byfuel_avoided_annual_global.columns[1:])]  # For global, adjust the slicing

# Function to plot avoided emissions by fuel type for each country or global
def plot_country_avoided_emissions(ax, df_cumulative, country_name, ylabel=None, is_global=False):
    # Adjust starting column based on whether it's global or country data
    start_col = 1 if is_global else 8
    years_columns = years_columns_global if is_global else years_columns_countries
    
    # Plot cumulative avoided emissions for each fuel type
    for fuel in df_cumulative['fuel_type'].unique():
        fuel_data = df_cumulative[df_cumulative['fuel_type'] == fuel]
        ax.plot(years_columns, abs(fuel_data.iloc[0, start_col:]), color=colors.get(fuel, 'grey'), label=fuel)

    # Customize the x-axis and format y-axis
    ax.set_xticks([str(year) for year in range(2030, 2051, 10)])
    ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter_0dec))

    # Set the title and labels
    ax.set_title(f'{country_name}', fontsize=14, fontweight='bold', pad=10)
    
    # Set the y-axis label if specified
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=12)

# Layout: 2 rows, 5 columns grid
fig = plt.figure(figsize=(15, 9))  # Adjusted figure size for 2x5 layout
gs = fig.add_gridspec(2, 5, height_ratios=[1, 1], width_ratios=[1, 1, 1, 1, 1])

# First row
ax_global = fig.add_subplot(gs[0, 0])
plot_country_avoided_emissions(ax_global, df_byfuel_avoided_cumulative_global, 'Global', ylabel="GW", is_global=True)

ax_emde = fig.add_subplot(gs[0, 1])
plot_country_avoided_emissions(ax_emde, df_byfuel_avoided_cumulative_emde, 'EMDEs', is_global=True)

ax_ind = fig.add_subplot(gs[0, 2])
plot_country_avoided_emissions(ax_ind, df_byfuel_avoided_cumulative_ind, 'India')

ax_usa = fig.add_subplot(gs[0, 3])
plot_country_avoided_emissions(ax_usa, df_byfuel_avoided_cumulative_usa, 'USA')

ax_vnm = fig.add_subplot(gs[0, 4])
plot_country_avoided_emissions(ax_vnm, df_byfuel_avoided_cumulative_vnm, 'Vietnam')

# Second row
ax_idn = fig.add_subplot(gs[1, 0])
plot_country_avoided_emissions(ax_idn, df_byfuel_avoided_cumulative_idn, 'Indonesia', ylabel="GW")

ax_tur = fig.add_subplot(gs[1, 1])
plot_country_avoided_emissions(ax_tur, df_byfuel_avoided_cumulative_tur, 'Türkiye')

ax_deu = fig.add_subplot(gs[1, 2])
plot_country_avoided_emissions(ax_deu, df_byfuel_avoided_cumulative_deu, 'Germany')

ax_pol = fig.add_subplot(gs[1, 3])
plot_country_avoided_emissions(ax_pol, df_byfuel_avoided_cumulative_pol, 'Poland')

ax_kaz = fig.add_subplot(gs[1, 4])
plot_country_avoided_emissions(ax_kaz, df_byfuel_avoided_cumulative_kaz, 'Kazakhstan')

# Main title
fig.suptitle('Cumulative Avoided Fossil Fuel Capacity in Power Sector:\n Current Policies vs Carbon Budget Consistent Net Zero*', fontsize=16, fontweight='bold', y=0.98)

# Subtitle
fig.text(0.5, 0.90, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', ha='center', fontsize=12)
fig.text(0.5, 0.85, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions \n with global carbon budget limiting warming to 1.5°C with 50% likelihood', ha='center', fontsize=12)

# Legend for all charts (handles from one plot)
handles, labels = ax_global.get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', ncol=3, bbox_to_anchor=(0.5, 0.07), fontsize=10)

# Adjust layout to bring the second row slightly higher
plt.subplots_adjust(top=0.78, bottom=0.15, hspace=0.45, wspace=0.3)

# Show the plot
plt.show()



