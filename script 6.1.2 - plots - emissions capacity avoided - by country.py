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

# Style
plt.style.use(['science'])

# Disable LaTeX rendering to avoid LaTeX-related errors
plt.rcParams['text.usetex'] = False

# Formatter function to convert values to thousands
def thousands_formatter_1dec(x, pos):
    return f'{x/1000:.1f}'   # the values are in Mt, but diving the axis by 1000 to show in Gt

def thousands_formatter_0dec(x, pos):
    return f'{x/1000:.0f}'

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

# Font and sizes
plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 10,
    'legend.fontsize': 8,
})

# Layout: 3 rows, 4 columns grid with custom ratios
fig = plt.figure(figsize=(12, 8))  # Increased figure size
gs = fig.add_gridspec(3, 4, height_ratios=[1, 1, 0.2], width_ratios=[2, 1, 1, 1])

# Function to plot each country
def plot_country(ax, df_country, country_name, loc,  ylabel=None):
    ax.plot(df_country.index, df_country['ghg_annual_cp'], label='NGFS Current Policies', color = colors['Current Policies'])
    ax.plot(df_country.index, df_country['ghg_annual_nz'], label='NGFS Net Zero 2050', color = colors['Net Zero 2050'])
    ax.plot(df_country.index, df_country['ghg_annual_nznew'], label='Carbon budget consistent Net Zero*', color = colors['Carbon Budget Consistent Net Zero'])
    ax.set_xticks([str(year) for year in range(2030, 2051, 10)])
    ax.set_title(f'{country_name}', fontsize=14, fontweight='bold', pad=10)  # Country names bold
    ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter_1dec))

    # Set the y-axis label if specified
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=12)
    
    
# Global chart (spanning 2 rows)
ax_global = fig.add_subplot(gs[0:2, 0])  # Span the first two rows
plot_country(ax_global, df_country_global, 'Global', 'upper left', ylabel='GtCO2')

# Germany
ax_deu = fig.add_subplot(gs[0, 1])
plot_country(ax_deu, df_country_deu, 'Germany', 'upper right')

# Indonesia
ax_idn = fig.add_subplot(gs[0, 2])
plot_country(ax_idn, df_country_idn, 'Indonesia', 'upper left')

# India
ax_ind = fig.add_subplot(gs[0, 3])
plot_country(ax_ind, df_country_ind, 'India', 'upper left')

# Turkiye
ax_tur = fig.add_subplot(gs[1, 1])
plot_country(ax_tur, df_country_tur, 'Turkiye', 'upper left')

# USA
ax_usa = fig.add_subplot(gs[1, 2])
plot_country(ax_usa, df_country_usa, 'USA', 'upper right')

# Vietnam
ax_vnm = fig.add_subplot(gs[1, 3])
plot_country(ax_vnm, df_country_vnm, 'Vietnam', 'upper left')

# Main title
fig.suptitle('Annual Emissions from Power Sector by Scenario', fontsize=16, fontweight='bold', y=0.98)

# Subtitle
fig.text(0.5, 0.92, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', ha='center', fontsize=12)
fig.text(0.5, 0.86, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions \n with global carbon budget limiting warming to 1.5°C with 50% likelihood', ha='center', fontsize=12)

# Legend for all charts
handles, labels = ax_global.get_legend_handles_labels()  # Get the legend handles and labels from one of the axes
fig.legend(handles, labels, loc='lower center', ncol=9, bbox_to_anchor=(0.5, 0.15), fontsize=10)

# Move the charts lower
plt.subplots_adjust(top=0.79, bottom=0.13, hspace=0.6, wspace=0.3)  # Increased spacing between rows

# Show the plot
plt.show()










##################################################################################################
##################### SECTION 2: CUMULATIVE EMISSISON ############################################
##################################################################################################

# Font and sizes
plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 10,
    'legend.fontsize': 8,
})

# Layout: 3 rows, 4 columns grid with custom ratios
fig = plt.figure(figsize=(12, 8))  # Increased figure size
gs = fig.add_gridspec(3, 4, height_ratios=[1, 1, 0.2], width_ratios=[2, 1, 1, 1])

# Function to plot each country
def plot_country(ax, df_country, country_name, loc,  ylabel=None):
    ax.plot(df_country.index, df_country['ghg_cumulative_cp'], label='NGFS Current Policies', color = colors['Current Policies'])
    ax.plot(df_country.index, df_country['ghg_cumulative_nz'], label='NGFS Net Zero 2050', color = colors['Net Zero 2050'])
    ax.plot(df_country.index, df_country['ghg_cumulative_nznew'], label='Carbon budget consistent Net Zero*', color = colors['Carbon Budget Consistent Net Zero'])
    ax.set_xticks([str(year) for year in range(2030, 2051, 10)])
    ax.set_title(f'{country_name}', fontsize=14, fontweight='bold', pad=10)  # Country names bold
    ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter_0dec))

    # Set the y-axis label if specified
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=12)
    
    
# Global chart (spanning 2 rows)
ax_global = fig.add_subplot(gs[0:2, 0])  # Span the first two rows
plot_country(ax_global, df_country_global, 'Global', 'upper left', ylabel='GtCO2')

# Germany
ax_deu = fig.add_subplot(gs[0, 1])
plot_country(ax_deu, df_country_deu, 'Germany', 'upper right')

# Indonesia
ax_idn = fig.add_subplot(gs[0, 2])
plot_country(ax_idn, df_country_idn, 'Indonesia', 'upper left')

# India
ax_ind = fig.add_subplot(gs[0, 3])
plot_country(ax_ind, df_country_ind, 'India', 'upper left')

# Turkiye
ax_tur = fig.add_subplot(gs[1, 1])
plot_country(ax_tur, df_country_tur, 'Turkiye', 'upper left')

# USA
ax_usa = fig.add_subplot(gs[1, 2])
plot_country(ax_usa, df_country_usa, 'USA', 'upper right')

# Vietnam
ax_vnm = fig.add_subplot(gs[1, 3])
plot_country(ax_vnm, df_country_vnm, 'Vietnam', 'upper left')

# Main title
fig.suptitle('Cumulative Emissions from Power Sector by Scenario', fontsize=16, fontweight='bold', y=0.98)

# Subtitle
fig.text(0.5, 0.92, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', ha='center', fontsize=12)
fig.text(0.5, 0.86, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions \n with global carbon budget limiting warming to 1.5°C with 50% likelihood', ha='center', fontsize=12)

# Legend for all charts
handles, labels = ax_global.get_legend_handles_labels()  # Get the legend handles and labels from one of the axes
fig.legend(handles, labels, loc='lower center', ncol=9, bbox_to_anchor=(0.5, 0.15), fontsize=10)

# Move the charts lower
plt.subplots_adjust(top=0.79, bottom=0.13, hspace=0.6, wspace=0.3)  # Increased spacing between rows

# Show the plot
plt.show()













##################################################################################################
##################### SECTION 3: AVOIDED EMISSIONS ###############################################
##################################################################################################

# --------------
# ANNUAL

# Font and sizes
plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 10,
    'legend.fontsize': 8,
})

# Layout: 3 rows, 4 columns grid with custom ratios
fig = plt.figure(figsize=(12, 8))  # Increased figure size
gs = fig.add_gridspec(3, 4, height_ratios=[1, 1, 0.2], width_ratios=[2, 1, 1, 1])

# Function to plot each country
def plot_country(ax, df_country, country_name, loc,  ylabel=None):
    ax.plot(df_country.index, df_country['ghg_annaul_avoided'], color = colors['Annual'])
    ax.set_xticks([str(year) for year in range(2030, 2051, 10)])
    ax.set_title(f'{country_name}', fontsize=14, fontweight='bold', pad=10)  # Country names bold
    ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter_1dec))

    # Set the y-axis label if specified
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=12)
    
    
# Global chart (spanning 2 rows)
ax_global = fig.add_subplot(gs[0:2, 0])  # Span the first two rows
plot_country(ax_global, df_country_global, 'Global', 'upper left', ylabel='GtCO2')

# Germany
ax_deu = fig.add_subplot(gs[0, 1])
plot_country(ax_deu, df_country_deu, 'Germany', 'upper right')

# Indonesia
ax_idn = fig.add_subplot(gs[0, 2])
plot_country(ax_idn, df_country_idn, 'Indonesia', 'upper left')

# India
ax_ind = fig.add_subplot(gs[0, 3])
plot_country(ax_ind, df_country_ind, 'India', 'upper left')

# Turkiye
ax_tur = fig.add_subplot(gs[1, 1])
plot_country(ax_tur, df_country_tur, 'Turkiye', 'upper left')

# USA
ax_usa = fig.add_subplot(gs[1, 2])
plot_country(ax_usa, df_country_usa, 'USA', 'upper right')

# Vietnam
ax_vnm = fig.add_subplot(gs[1, 3])
plot_country(ax_vnm, df_country_vnm, 'Vietnam', 'upper left')

# Main title
fig.suptitle('Annual Avoided Emissions from Power Sector by Scenario:\n Current Policies vs Carbon Budget Consistent Net Zero*', fontsize=16, fontweight='bold', y=0.98)

# Subtitle
fig.text(0.5, 0.88, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', ha='center', fontsize=12)
fig.text(0.5, 0.82, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions \n with global carbon budget limiting warming to 1.5°C with 50% likelihood', ha='center', fontsize=12)

# Legend for all charts
handles, labels = ax_global.get_legend_handles_labels()  # Get the legend handles and labels from one of the axes
fig.legend(handles, labels, loc='lower center', ncol=9, bbox_to_anchor=(0.5, 0.15), fontsize=10)

# Move the charts lower
plt.subplots_adjust(top=0.75, bottom=0.1, hspace=0.6, wspace=0.3)  # Increased spacing between rows

# Show the plot
plt.show()





# --------------
# CUMULATIVE

# Font and sizes
plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 10,
    'legend.fontsize': 8,
})

# Layout: 3 rows, 4 columns grid with custom ratios
fig = plt.figure(figsize=(12, 8))  # Increased figure size
gs = fig.add_gridspec(3, 4, height_ratios=[1, 1, 0.2], width_ratios=[2, 1, 1, 1])

# Function to plot each country
def plot_country(ax, df_country, country_name, loc,  ylabel=None):
    ax.plot(df_country.index, df_country['ghg_cumulative_avoided'], color = colors['Cumulative'])
    ax.set_xticks([str(year) for year in range(2030, 2051, 10)])
    ax.set_title(f'{country_name}', fontsize=14, fontweight='bold', pad=10)  # Country names bold
    ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter_0dec))

    # Set the y-axis label if specified
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=12)
    
    
# Global chart (spanning 2 rows)
ax_global = fig.add_subplot(gs[0:2, 0])  # Span the first two rows
plot_country(ax_global, df_country_global, 'Global', 'upper left', ylabel='GtCO2')

# Germany
ax_deu = fig.add_subplot(gs[0, 1])
plot_country(ax_deu, df_country_deu, 'Germany', 'upper right')

# Indonesia
ax_idn = fig.add_subplot(gs[0, 2])
plot_country(ax_idn, df_country_idn, 'Indonesia', 'upper left')

# India
ax_ind = fig.add_subplot(gs[0, 3])
plot_country(ax_ind, df_country_ind, 'India', 'upper left')

# Turkiye
ax_tur = fig.add_subplot(gs[1, 1])
plot_country(ax_tur, df_country_tur, 'Turkiye', 'upper left')

# USA
ax_usa = fig.add_subplot(gs[1, 2])
plot_country(ax_usa, df_country_usa, 'USA', 'upper right')

# Vietnam
ax_vnm = fig.add_subplot(gs[1, 3])
plot_country(ax_vnm, df_country_vnm, 'Vietnam', 'upper left')

# Main title
fig.suptitle('Cumulative Avoided Emissions from Power Sector by Scenario:\n Current Policies vs Carbon Budget Consistent Net Zero*', fontsize=16, fontweight='bold', y=0.98)

# Subtitle
fig.text(0.5, 0.88, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', ha='center', fontsize=12)
fig.text(0.5, 0.82, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions \n with global carbon budget limiting warming to 1.5°C with 50% likelihood', ha='center', fontsize=12)

# Legend for all charts
handles, labels = ax_global.get_legend_handles_labels()  # Get the legend handles and labels from one of the axes
fig.legend(handles, labels, loc='lower center', ncol=9, bbox_to_anchor=(0.5, 0.15), fontsize=10)

# Move the charts lower
plt.subplots_adjust(top=0.75, bottom=0.1, hspace=0.6, wspace=0.3)  # Increased spacing between rows

# Show the plot
plt.show()










##################################################################################################
##################### SECTION 4: ANNUAL CAPACITY #################################################
##################################################################################################

# Font and sizes
plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 10,
    'legend.fontsize': 8,
})

# Layout: 3 rows, 4 columns grid with custom ratios
fig = plt.figure(figsize=(12, 8))  # Increased figure size
gs = fig.add_gridspec(3, 4, height_ratios=[1, 1, 0.2], width_ratios=[2, 1, 1, 1])

# Function to plot each country
def plot_country(ax, df_country, country_name, loc,  ylabel=None):
    ax.plot(df_country.index, df_country['capacity_annual_cp'], label='NGFS Current Policies', color = colors['Current Policies'])
    ax.plot(df_country.index, df_country['capacity_annual_nz'], label='NGFS Net Zero 2050', color = colors['Net Zero 2050'])
    ax.plot(df_country.index, df_country['capacity_annual_nznew'], label='Carbon budget consistent Net Zero*', color = colors['Carbon Budget Consistent Net Zero'])
    ax.set_xticks([str(year) for year in range(2030, 2051, 10)])
    ax.set_title(f'{country_name}', fontsize=14, fontweight='bold', pad=10)  # Country names bold
    ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter_0dec))

    # Set the y-axis label if specified
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=12)
    
    
# Global chart (spanning 2 rows)
ax_global = fig.add_subplot(gs[0:2, 0])  # Span the first two rows
plot_country(ax_global, df_country_global, 'Global', 'upper left', ylabel='GW')

# Germany
ax_deu = fig.add_subplot(gs[0, 1])
plot_country(ax_deu, df_country_deu, 'Germany', 'upper right')

# Indonesia
ax_idn = fig.add_subplot(gs[0, 2])
plot_country(ax_idn, df_country_idn, 'Indonesia', 'upper left')

# India
ax_ind = fig.add_subplot(gs[0, 3])
plot_country(ax_ind, df_country_ind, 'India', 'upper left')

# Turkiye
ax_tur = fig.add_subplot(gs[1, 1])
plot_country(ax_tur, df_country_tur, 'Turkiye', 'upper left')

# USA
ax_usa = fig.add_subplot(gs[1, 2])
plot_country(ax_usa, df_country_usa, 'USA', 'upper right')

# Vietnam
ax_vnm = fig.add_subplot(gs[1, 3])
plot_country(ax_vnm, df_country_vnm, 'Vietnam', 'upper left')

# Main title
fig.suptitle('Annual Fossil Fuel Capacity in Power Sector by Scenario', fontsize=16, fontweight='bold', y=0.98)

# Subtitle
fig.text(0.5, 0.92, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', ha='center', fontsize=12)
fig.text(0.5, 0.86, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions \n with global carbon budget limiting warming to 1.5°C with 50% likelihood', ha='center', fontsize=12)

# Legend for all charts
handles, labels = ax_global.get_legend_handles_labels()  # Get the legend handles and labels from one of the axes
fig.legend(handles, labels, loc='lower center', ncol=9, bbox_to_anchor=(0.5, 0.15), fontsize=10)

# Move the charts lower
plt.subplots_adjust(top=0.79, bottom=0.13, hspace=0.6, wspace=0.3)  # Increased spacing between rows

# Show the plot
plt.show()













##################################################################################################
##################### SECTION 5: AVOIDED CAPACITY ################################################
##################################################################################################


# --------------
# ANNUAL

# Font and sizes
plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 10,
    'legend.fontsize': 8,
})

# Layout: 3 rows, 4 columns grid with custom ratios
fig = plt.figure(figsize=(12, 8))  # Increased figure size
gs = fig.add_gridspec(3, 4, height_ratios=[1, 1, 0.2], width_ratios=[2, 1, 1, 1])

# Function to plot each country
def plot_country(ax, df_country, country_name, loc,  ylabel=None):
    ax.plot(df_country.index, abs(df_country['capacity_annaul_avoided']), color = colors['Annual'])
    ax.set_xticks([str(year) for year in range(2030, 2051, 10)])
    ax.set_title(f'{country_name}', fontsize=14, fontweight='bold', pad=10)  # Country names bold
    ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter_0dec))

    # Set the y-axis label if specified
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=12)
    
    
# Global chart (spanning 2 rows)
ax_global = fig.add_subplot(gs[0:2, 0])  # Span the first two rows
plot_country(ax_global, df_country_global, 'Global', 'upper left', ylabel='GW')

# Germany
ax_deu = fig.add_subplot(gs[0, 1])
plot_country(ax_deu, df_country_deu, 'Germany', 'upper right')

# Indonesia
ax_idn = fig.add_subplot(gs[0, 2])
plot_country(ax_idn, df_country_idn, 'Indonesia', 'upper left')

# India
ax_ind = fig.add_subplot(gs[0, 3])
plot_country(ax_ind, df_country_ind, 'India', 'upper left')

# Turkiye
ax_tur = fig.add_subplot(gs[1, 1])
plot_country(ax_tur, df_country_tur, 'Turkiye', 'upper left')

# USA
ax_usa = fig.add_subplot(gs[1, 2])
plot_country(ax_usa, df_country_usa, 'USA', 'upper right')

# Vietnam
ax_vnm = fig.add_subplot(gs[1, 3])
plot_country(ax_vnm, df_country_vnm, 'Vietnam', 'upper left')

# Main title
fig.suptitle('Annual Avoided Fossil Fuel Capacity in Power Sector:\n Current Policies vs Carbon Budget Consistent Net Zero*', fontsize=16, fontweight='bold', y=0.98)

# Subtitle
fig.text(0.5, 0.88, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', ha='center', fontsize=12)
fig.text(0.5, 0.82, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions \n with global carbon budget limiting warming to 1.5°C with 50% likelihood', ha='center', fontsize=12)

# Legend for all charts
handles, labels = ax_global.get_legend_handles_labels()  # Get the legend handles and labels from one of the axes
fig.legend(handles, labels, loc='lower center', ncol=9, bbox_to_anchor=(0.5, 0.15), fontsize=10)

# Move the charts lower
plt.subplots_adjust(top=0.75, bottom=0.1, hspace=0.6, wspace=0.3)  # Increased spacing between rows

# Show the plot
plt.show()





# --------------
# CUMULATIVE

# Font and sizes
plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 10,
    'legend.fontsize': 8,
})

# Layout: 3 rows, 4 columns grid with custom ratios
fig = plt.figure(figsize=(12, 8))  # Increased figure size
gs = fig.add_gridspec(3, 4, height_ratios=[1, 1, 0.2], width_ratios=[2, 1, 1, 1])

# Function to plot each country
def plot_country(ax, df_country, country_name, loc,  ylabel=None):
    ax.plot(df_country.index, abs(df_country['capacity_cumulative_avoided']), color = colors['Cumulative'])
    ax.set_xticks([str(year) for year in range(2030, 2051, 10)])
    ax.set_title(f'{country_name}', fontsize=14, fontweight='bold', pad=10)  # Country names bold
    ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter_0dec))

    # Set the y-axis label if specified
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=12)
    
    
# Global chart (spanning 2 rows)
ax_global = fig.add_subplot(gs[0:2, 0])  # Span the first two rows
plot_country(ax_global, df_country_global, 'Global', 'upper left', ylabel='GW')

# Germany
ax_deu = fig.add_subplot(gs[0, 1])
plot_country(ax_deu, df_country_deu, 'Germany', 'upper right')

# Indonesia
ax_idn = fig.add_subplot(gs[0, 2])
plot_country(ax_idn, df_country_idn, 'Indonesia', 'upper left')

# India
ax_ind = fig.add_subplot(gs[0, 3])
plot_country(ax_ind, df_country_ind, 'India', 'upper left')

# Turkiye
ax_tur = fig.add_subplot(gs[1, 1])
plot_country(ax_tur, df_country_tur, 'Turkiye', 'upper left')

# USA
ax_usa = fig.add_subplot(gs[1, 2])
plot_country(ax_usa, df_country_usa, 'USA', 'upper right')

# Vietnam
ax_vnm = fig.add_subplot(gs[1, 3])
plot_country(ax_vnm, df_country_vnm, 'Vietnam', 'upper left')

# Main title
fig.suptitle('Cumulative Avoided Fossil Fuel Capacity in Power Sector:\n Current Policies vs Carbon Budget Consistent Net Zero*', fontsize=16, fontweight='bold', y=0.98)

# Subtitle
fig.text(0.5, 0.88, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', ha='center', fontsize=12)
fig.text(0.5, 0.82, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions \n with global carbon budget limiting warming to 1.5°C with 50% likelihood', ha='center', fontsize=12)

# Legend for all charts
handles, labels = ax_global.get_legend_handles_labels()  # Get the legend handles and labels from one of the axes
fig.legend(handles, labels, loc='lower center', ncol=9, bbox_to_anchor=(0.5, 0.15), fontsize=10)

# Move the charts lower
plt.subplots_adjust(top=0.75, bottom=0.1, hspace=0.6, wspace=0.3)  # Increased spacing between rows

# Show the plot
plt.show()










##################################################################################################
##################### SECTION 6: BY FUEL: EMISSIONS ##############################################
##################################################################################################


# Ensure the years_columns array has the correct length for country data
years_columns_countries = years_columns[:len(df_emissions_currentpolicy_deu.columns[8:])]
years_columns_global = years_columns[:len(df_emissions_currentpolicy_global.columns[1:])]  # For global, adjust the slicing


# Function to plot emissions by fuel type for each country or global
def plot_country_emissions(ax, df_current_policy, df_nz_policy, country_name, is_global=False):
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
    ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter_1dec))

    
    # Set title
    ax.set_title(f'{country_name}', fontsize=14, fontweight='bold', pad=10)

    # Set y-axis label only for the global chart
    if is_global:
        ax.set_ylabel('GtCO2', fontsize=12)

# Layout: 2 rows, 4 columns grid with custom ratios
fig = plt.figure(figsize=(12, 8))
gs = fig.add_gridspec(3, 4, height_ratios=[1, 1, 0.2], width_ratios=[2, 1, 1, 1])

# Global plot (spanning 2 rows)
ax_global = fig.add_subplot(gs[0:2, 0])
plot_country_emissions(ax_global, df_emissions_currentpolicy_global, df_emissions_nz1550v2_global, 'Global', is_global=True)


# Germany
ax_deu = fig.add_subplot(gs[0, 1])
plot_country_emissions(ax_deu, df_emissions_currentpolicy_deu, df_emissions_nz1550v2_deu, 'Germany')

# Indonesia
ax_idn = fig.add_subplot(gs[0, 2])
plot_country_emissions(ax_idn, df_emissions_currentpolicy_idn, df_emissions_nz1550v2_idn, 'Indonesia')

# India
ax_ind = fig.add_subplot(gs[0, 3])
plot_country_emissions(ax_ind, df_emissions_currentpolicy_ind, df_emissions_nz1550v2_ind, 'India')

# Turkiye
ax_tur = fig.add_subplot(gs[1, 1])
plot_country_emissions(ax_tur, df_emissions_currentpolicy_tur, df_emissions_nz1550v2_tur, 'Turkiye')

# USA
ax_usa = fig.add_subplot(gs[1, 2])
plot_country_emissions(ax_usa, df_emissions_currentpolicy_usa, df_emissions_nz1550v2_usa, 'USA')

# Vietnam
ax_vnm = fig.add_subplot(gs[1, 3])
plot_country_emissions(ax_vnm, df_emissions_currentpolicy_vnm, df_emissions_nz1550v2_vnm, 'Vietnam')

# Main title
fig.suptitle('Annual Emissions from Power Sector by Scenario and Fuel Type', fontsize=16, fontweight='bold', y=0.98)

# Subtitle
fig.text(0.5, 0.92, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', ha='center', fontsize=12)
fig.text(0.5, 0.88, 'Solid line: Carbon budget consistent Net Zero* | Dotted line: Current Policies', ha='center', fontsize=12)
fig.text(0.5, 0.82, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions \n with global carbon budget limiting warming to 1.5°C with 50% likelihood', ha='center', fontsize=12)


# Legend for all charts (handles from one plot)
handles, labels = ax_global.get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', ncol=9, bbox_to_anchor=(0.5, 0.15), fontsize=10)

# Adjust the spacing to move the charts lower and create space between rows
plt.subplots_adjust(top=0.75, bottom=0.13, hspace=0.6, wspace=0.3)

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
def plot_country_avoided_emissions(ax, df_annual, country_name, is_global=False):
    # Adjust starting column based on whether it's global or country data
    start_col = 1 if is_global else 8  # Use 1 for global, 8 for countries
    years_columns = years_columns_global if is_global else years_columns_countries
    
    # Plot Annual avoided emissions (dotted lines) on primary y-axis
    for fuel in df_annual['fuel_type'].unique():
        fuel_data = df_annual[df_annual['fuel_type'] == fuel]
        # Add the 'label' parameter to capture the fuel name for the legend
        ax.plot(years_columns, abs(fuel_data.iloc[0, start_col:]), color=colors.get(fuel, 'grey'), label=fuel)

    # Customize the x-axis for primary y-axis
    ax.set_xticks([str(year) for year in range(2030, 2051, 10)])
    ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter_0dec))

    # Set the title and labels
    ax.set_title(f'{country_name}', fontsize=14, fontweight='bold', pad=10)
    
    # Only add y-label to the global chart
    if is_global:
        ax.set_ylabel('GW', fontsize=12)
    

# Layout: 3 rows, 4 columns grid with custom ratios
fig = plt.figure(figsize=(12, 8))
gs = fig.add_gridspec(3, 4, height_ratios=[1, 1, 0.2], width_ratios=[2, 1, 1, 1])

# Global plot (spanning 2 rows)
ax_global = fig.add_subplot(gs[0:2, 0])
plot_country_avoided_emissions(ax_global, df_byfuel_avoided_annual_global, 'Global', is_global=True)

# Germany
ax_deu = fig.add_subplot(gs[0, 1])
plot_country_avoided_emissions(ax_deu, df_byfuel_avoided_annual_deu, 'Germany')

# Indonesia
ax_idn = fig.add_subplot(gs[0, 2])
plot_country_avoided_emissions(ax_idn, df_byfuel_avoided_annual_idn, 'Indonesia')

# India
ax_ind = fig.add_subplot(gs[0, 3])
plot_country_avoided_emissions(ax_ind, df_byfuel_avoided_annual_ind, 'India')

# Turkiye
ax_tur = fig.add_subplot(gs[1, 1])
plot_country_avoided_emissions(ax_tur, df_byfuel_avoided_annual_tur, 'Turkiye')

# USA
ax_usa = fig.add_subplot(gs[1, 2])
plot_country_avoided_emissions(ax_usa, df_byfuel_avoided_annual_usa, 'USA')

# Vietnam
ax_vnm = fig.add_subplot(gs[1, 3])
plot_country_avoided_emissions(ax_vnm, df_byfuel_avoided_annual_vnm, 'Vietnam')

# Main title
fig.suptitle('Annual Avoided Fossil Fuel Capacity in Power Sector:\n Current Policies vs Carbon Budget Consistent Net Zero*', fontsize=16, fontweight='bold', y=0.98)

# Subtitle
fig.text(0.5, 0.88, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', ha='center', fontsize=12)
fig.text(0.5, 0.82, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions \n with global carbon budget limiting warming to 1.5°C with 50% likelihood', ha='center', fontsize=12)


# Legend for all charts (handles from one plot)
handles, labels = ax_global.get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', ncol=9, bbox_to_anchor=(0.5, 0.15), fontsize=10)

# Adjust the spacing to move the charts lower and create space between rows
plt.subplots_adjust(top=0.75, bottom=0.13, hspace=0.6, wspace=0.3)

# Show the plot
plt.show()





# --------------
# CUMULATIVE

# Ensure the years_columns array has the correct length for country and global data
years_columns_countries = years_columns[:len(df_byfuel_avoided_annual_deu.columns[8:])]
years_columns_global = years_columns[:len(df_byfuel_avoided_annual_global.columns[1:])]  # For global, adjust the slicing

# Function to plot avoided emissions by fuel type for each country or global
def plot_country_avoided_emissions(ax, df_cumulative, country_name, is_global=False):
    # Adjust starting column based on whether it's global or country data
    start_col = 1 if is_global else 8  # Use 1 for global, 8 for countries
    years_columns = years_columns_global if is_global else years_columns_countries
    
    # Plot Annual avoided emissions (dotted lines) on primary y-axis
    for fuel in df_cumulative['fuel_type'].unique():
        fuel_data = df_cumulative[df_cumulative['fuel_type'] == fuel]
        # Add the 'label' parameter to capture the fuel name for the legend
        ax.plot(years_columns, abs(fuel_data.iloc[0, start_col:]), color=colors.get(fuel, 'grey'), label=fuel)

    # Customize the x-axis for primary y-axis
    ax.set_xticks([str(year) for year in range(2030, 2051, 10)])
    ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter_0dec))

    # Set the title and labels
    ax.set_title(f'{country_name}', fontsize=14, fontweight='bold', pad=10)
    
    # Only add y-label to the global chart
    if is_global:
        ax.set_ylabel('GW', fontsize=12)
    

# Layout: 3 rows, 4 columns grid with custom ratios
fig = plt.figure(figsize=(12, 8))
gs = fig.add_gridspec(3, 4, height_ratios=[1, 1, 0.2], width_ratios=[2, 1, 1, 1])

# Global plot (spanning 2 rows)
ax_global = fig.add_subplot(gs[0:2, 0])
plot_country_avoided_emissions(ax_global, df_byfuel_avoided_cumulative_global, 'Global', is_global=True)

# Germany
ax_deu = fig.add_subplot(gs[0, 1])
plot_country_avoided_emissions(ax_deu, df_byfuel_avoided_cumulative_deu, 'Germany')

# Indonesia
ax_idn = fig.add_subplot(gs[0, 2])
plot_country_avoided_emissions(ax_idn, df_byfuel_avoided_cumulative_idn, 'Indonesia')

# India
ax_ind = fig.add_subplot(gs[0, 3])
plot_country_avoided_emissions(ax_ind, df_byfuel_avoided_cumulative_ind, 'India')

# Turkiye
ax_tur = fig.add_subplot(gs[1, 1])
plot_country_avoided_emissions(ax_tur, df_byfuel_avoided_cumulative_tur, 'Turkiye')

# USA
ax_usa = fig.add_subplot(gs[1, 2])
plot_country_avoided_emissions(ax_usa, df_byfuel_avoided_cumulative_usa, 'USA')

# Vietnam
ax_vnm = fig.add_subplot(gs[1, 3])
plot_country_avoided_emissions(ax_vnm, df_byfuel_avoided_cumulative_vnm, 'Vietnam')

# Main title
fig.suptitle('Cumulative Avoided Fossil Fuel Capacity in Power Sector:\n Current Policies vs Carbon Budget Consistent Net Zero*', fontsize=16, fontweight='bold', y=0.98)

# Subtitle
fig.text(0.5, 0.88, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', ha='center', fontsize=12)
fig.text(0.5, 0.82, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions \n with global carbon budget limiting warming to 1.5°C with 50% likelihood', ha='center', fontsize=12)


# Legend for all charts (handles from one plot)
handles, labels = ax_global.get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', ncol=9, bbox_to_anchor=(0.5, 0.15), fontsize=10)

# Adjust the spacing to move the charts lower and create space between rows
plt.subplots_adjust(top=0.75, bottom=0.13, hspace=0.6, wspace=0.3)

# Show the plot
plt.show()


















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











