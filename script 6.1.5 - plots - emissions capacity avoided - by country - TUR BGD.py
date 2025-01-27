# In[1]:
# Date: Sep 2, 2024
# Project: Plots: Global + DEV + DOP + 8 countries
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

    







# In[11]
##################################################################################################
##################### SECTION 1: ANNUAL EMISSISON ################################################
##################################################################################################

# --------------
# Function to plot a region or country
def plot_region(ax, df_country, region_name, ylabel=None):
    ax.plot(df_country.index, df_country['ghg_annual_cp'], label='NGFS Current Policies', color=colors['Current Policies'])
    ax.plot(df_country.index, df_country['ghg_annual_nz'], label='NGFS Net Zero 2050', color=colors['Net Zero 2050'])
    ax.plot(df_country.index, df_country['ghg_annual_nznew'], label='Carbon budget consistent Net Zero*', color=colors['Carbon Budget Consistent Net Zero'])
    ax.set_xticks([str(year) for year in range(2030, 2051, 10)])
    ax.set_title(f'{region_name}', fontsize=12, fontweight='bold', pad=10)
    ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter_2dec))
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=10)

# First Graph: Global, DOPUNFCCC, DEVUNFCCC
fig1, axes1 = plt.subplots(1, 3, figsize=(12, 5))
plot_region(axes1[0], df_country_global, 'Global', ylabel='GtCO2eq')
plot_region(axes1[1], df_country_dopunfccc, 'Developed Countries')
plot_region(axes1[2], df_country_devunfccc, 'Developing Countries')

# Main title for the first graph
fig1.suptitle('Annual Emissions from Power Sector by Scenario', fontsize=16, fontweight='bold', y=0.98)

# Subtitle
#fig1.text(0.5, 0.93, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', ha='center', fontsize=12)
#fig1.text(0.5, 0.88, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions \n with global carbon budget limiting warming to 1.5°C with 50% likelihood', ha='center', fontsize=12)

# Legend for the first graph
handles1, labels1 = axes1[0].get_legend_handles_labels()
fig1.legend(handles1, labels1, loc='lower center', ncol=3, bbox_to_anchor=(0.5, -0.05), fontsize=10)

# Adjust layout
fig1.subplots_adjust(top=0.85, bottom=0.15, hspace=0.4, wspace=0.4)

# Show the first graph
plt.show()


# -------------------------
# Second Graph: 8 Countries
fig2 = plt.figure(figsize=(12, 6))  # Adjusted figure size
gs2 = fig2.add_gridspec(2, 4, height_ratios=[1, 1], width_ratios=[1, 1, 1, 1])

# First row
#plot_region(fig2.add_subplot(gs2[0, 0]), df_country_ind, 'India', ylabel='GtCO2eq')
#plot_region(fig2.add_subplot(gs2[0, 1]), df_country_idn, 'Indonesia')
plot_region(fig2.add_subplot(gs2[0, 2]), df_country_tur, 'Türkiye', ylabel='GtCO2eq')
#plot_region(fig2.add_subplot(gs2[0, 3]), df_country_mex, 'Mexico')

# Second row
#plot_region(fig2.add_subplot(gs2[1, 0]), df_country_vnm, 'Viet Nam', ylabel='GtCO2eq')
#plot_region(fig2.add_subplot(gs2[1, 1]), df_country_irn, 'Iran')
plot_region(fig2.add_subplot(gs2[1, 2]), df_country_bgd, 'Bangladesh', ylabel='GtCO2eq')
#plot_region(fig2.add_subplot(gs2[1, 3]), df_country_egy, 'Egypt')

# Main title for the second graph
fig2.suptitle('Annual Emissions from Power Sector by Scenario', fontsize=16, fontweight='bold', y=0.98)

# Subtitle
#fig2.text(0.5, 0.93, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', ha='center', fontsize=12)
#fig2.text(0.5, 0.88, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions \n with global carbon budget limiting warming to 1.5°C with 50% likelihood', ha='center', fontsize=12)

# Legend for the second graph
handles2, labels2 = fig2.axes[0].get_legend_handles_labels()
fig2.legend(handles2, labels2, loc='lower center', ncol=3, bbox_to_anchor=(0.5, -0.05), fontsize=10)

# Adjust layout
plt.subplots_adjust(top=0.85, bottom=0.12, hspace=0.6, wspace=0.4)

# Show the second graph
plt.show()










# In[11]
##################################################################################################
##################### SECTION 2: CUMULATIVE EMISSISON ############################################
##################################################################################################

# --------------
# Function to plot a region or country
def plot_region(ax, df_country, region_name, ylabel=None):
    ax.plot(df_country.index, df_country['ghg_cumulative_cp'], label='NGFS Current Policies', color=colors['Current Policies'])
    ax.plot(df_country.index, df_country['ghg_cumulative_nz'], label='NGFS Net Zero 2050', color=colors['Net Zero 2050'])
    ax.plot(df_country.index, df_country['ghg_cumulative_nznew'], label='Carbon budget consistent Net Zero*', color=colors['Carbon Budget Consistent Net Zero'])
    ax.set_xticks([str(year) for year in range(2030, 2051, 10)])
    ax.set_title(f'{region_name}', fontsize=12, fontweight='bold', pad=10)
    ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter_1dec))
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=10)

# First Graph: Global, DOPUNFCCC, DEVUNFCCC
fig1, axes1 = plt.subplots(1, 3, figsize=(12, 5))
plot_region(axes1[0], df_country_global, 'Global', ylabel='GtCO2eq')
plot_region(axes1[1], df_country_dopunfccc, 'Developed Countries')
plot_region(axes1[2], df_country_devunfccc, 'Developing Countries')

# Main title for the first graph
fig1.suptitle('Cumulative Emissions from Power Sector by Scenario', fontsize=16, fontweight='bold', y=0.98)

# Subtitle
#fig.text(0.5, 0.93, 'Cumulative emissions from current power plants in operation, using NGFS GCAM6 growth rates', ha='center', fontsize=12)
#fig.text(0.5, 0.88, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions \n with global carbon budget limiting warming to 1.5°C with 50% likelihood', ha='center', fontsize=12)

# Legend for the first graph
handles1, labels1 = axes1[0].get_legend_handles_labels()
fig1.legend(handles1, labels1, loc='lower center', ncol=3, bbox_to_anchor=(0.5, -0.05), fontsize=10)

# Adjust layout
fig1.subplots_adjust(top=0.85, bottom=0.15, hspace=0.4, wspace=0.4)

# Show the first graph
plt.show()


# -------------------------
# Second Graph: 8 Countries
fig2 = plt.figure(figsize=(12, 6))  # Adjusted figure size
gs2 = fig2.add_gridspec(2, 4, height_ratios=[1, 1], width_ratios=[1, 1, 1, 1])

# First row
#plot_region(fig2.add_subplot(gs2[0, 0]), df_country_ind, 'India', ylabel='GtCO2eq')
#plot_region(fig2.add_subplot(gs2[0, 1]), df_country_idn, 'Indonesia')
plot_region(fig2.add_subplot(gs2[0, 2]), df_country_tur, 'Türkiye', ylabel='GtCO2eq')
#plot_region(fig2.add_subplot(gs2[0, 3]), df_country_mex, 'Mexico')

# Second row
#plot_region(fig2.add_subplot(gs2[1, 0]), df_country_vnm, 'Viet Nam', ylabel='GtCO2eq')
#plot_region(fig2.add_subplot(gs2[1, 1]), df_country_irn, 'Iran')
plot_region(fig2.add_subplot(gs2[1, 2]), df_country_bgd, 'Bangladesh', ylabel='GtCO2eq')
#plot_region(fig2.add_subplot(gs2[1, 3]), df_country_egy, 'Egypt')

# Main title for the second graph
fig2.suptitle('Cumulative Emissions from Power Sector by Scenario', fontsize=16, fontweight='bold', y=0.98)

# Subtitle
#fig2.text(0.5, 0.93, 'Cumulative emissions from current power plants in operation, using NGFS GCAM6 growth rates', ha='center', fontsize=12)
#fig2.text(0.5, 0.88, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions \n with global carbon budget limiting warming to 1.5°C with 50% likelihood', ha='center', fontsize=12)

# Legend for the second graph
handles2, labels2 = fig2.axes[0].get_legend_handles_labels()
fig2.legend(handles2, labels2, loc='lower center', ncol=3, bbox_to_anchor=(0.5, -0.05), fontsize=10)

# Adjust layout
plt.subplots_adjust(top=0.85, bottom=0.12, hspace=0.6, wspace=0.4)

# Show the second graph
plt.show()










# In[11]
##################################################################################################
##################### SECTION 3: AVOIDED EMISSIONS ###############################################
##################################################################################################

# Function to plot both annual and cumulative avoided emissions on the same axes
def plot_combined(ax, df_country, region_name, ylabel_left=None, ylabel_right=None):
    # Plot annual avoided emissions on the left y-axis
    line1, = ax.plot(df_country.index, df_country['ghg_annaul_avoided'], label='Annual Avoided Emissions', color=colors['Annual'])
    ax.set_xticks([str(year) for year in range(2030, 2051, 10)])
    ax.set_title(f'{region_name}', fontsize=12, fontweight='bold', pad=10)
    ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter_2dec))
    if ylabel_left:
        ax.set_ylabel(ylabel_left, fontsize=10)

    # Create a twin y-axis for cumulative avoided emissions
    ax2 = ax.twinx()
    line2, = ax2.plot(df_country.index, df_country['ghg_cumulative_avoided'], label='Cumulative Avoided Emissions', color=colors['Cumulative'], linestyle='--')
    ax2.yaxis.set_major_formatter(FuncFormatter(thousands_formatter_1dec))
    if ylabel_right:
        ax2.set_ylabel(ylabel_right, fontsize=10)

    return [line1, line2]

# -------------------------
# First Graph: Global, DOPUNFCCC, DEVUNFCCC
fig1, axes1 = plt.subplots(1, 3, figsize=(12, 5))

# Collect handles for the legend
handles = []
handles += plot_combined(axes1[0], df_country_global, 'Global', ylabel_left='Annual (GtCO2eq)')
handles += plot_combined(axes1[1], df_country_dopunfccc, 'Developed Countries')
handles += plot_combined(axes1[2], df_country_devunfccc, 'Developing Countries', ylabel_right='Cumulative (GtCO2)')

# Main title for the first graph
fig1.suptitle('Avoided Emissions from Power Sector by Scenario:\n Current Policies vs Carbon Budget Consistent Net Zero', fontsize=16, fontweight='bold', y=0.98)

# Subtitle
#fig1.text(0.5, 0.90, 'Emissions from current power plants in operation projected using NGFS GCAM6 model growth rates', ha='center', fontsize=12)
#fig1.text(0.5, 0.85, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions \n with global carbon budget limiting warming to 1.5°C with 50% likelihood', ha='center', fontsize=12)


# Single legend for the first graph
labels = ['Annual Avoided Emissions (Left axis)', 'Cumulative Avoided Emissions (Right axis)']
fig1.legend(handles, labels, loc='lower center', ncol=2, bbox_to_anchor=(0.5, -0.1), fontsize=10)

# Adjust layout
fig1.subplots_adjust(top=0.80, bottom=0.05, hspace=0.4, wspace=0.6)
plt.show()



# -------------------------
# Second Graph: 8 Countries
fig2 = plt.figure(figsize=(12, 6))  # Adjusted figure size
gs2 = fig2.add_gridspec(2, 4, height_ratios=[1, 1], width_ratios=[1, 1, 1, 1])

# Collect handles for the legend
handles = []

# First row
#handles += plot_combined(fig2.add_subplot(gs2[0, 0]), df_country_ind, 'India', ylabel_left='Annual (GtCO2eq)')
#handles += plot_combined(fig2.add_subplot(gs2[0, 1]), df_country_idn, 'Indonesia')
handles += plot_combined(fig2.add_subplot(gs2[0, 2]), df_country_tur, 'Türkiye', ylabel_left='Annual (GtCO2eq)', ylabel_right='Cumulative (GtCO2)')
#handles += plot_combined(fig2.add_subplot(gs2[0, 3]), df_country_mex, 'Mexico', ylabel_right='Cumulative (GtCO2)')

# Second row
#handles += plot_combined(fig2.add_subplot(gs2[1, 0]), df_country_vnm, 'Viet Nam', ylabel_left='Annual (GtCO2eq)')
#handles += plot_combined(fig2.add_subplot(gs2[1, 1]), df_country_irn, 'Iran')
handles += plot_combined(fig2.add_subplot(gs2[1, 2]), df_country_bgd, 'Bangladesh', ylabel_left='Annual (GtCO2eq)', ylabel_right='Cumulative (GtCO2)')
#handles += plot_combined(fig2.add_subplot(gs2[1, 3]), df_country_egy, 'Egypt', ylabel_right='Cumulative (GtCO2)')

# Main title for the second graph
fig2.suptitle('Avoided Emissions from Power Sector by Scenario:\n Current Policies vs Carbon Budget Consistent Net Zero', fontsize=16, fontweight='bold', y=0.98)

# Subtitle
#fig2.text(0.5, 0.90, 'Emissions from current power plants in operation projected using NGFS GCAM6 model growth rates', ha='center', fontsize=12)
#fig2.text(0.5, 0.85, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions \n with global carbon budget limiting warming to 1.5°C with 50% likelihood', ha='center', fontsize=12)


# Single legend for the second graph
labels = ['Annual Avoided Emissions (Left axis)', 'Cumulative Avoided Emissions (Right axis)']
fig2.legend(handles, labels, loc='lower center', ncol=2, bbox_to_anchor=(0.5, -0.1), fontsize=10)

# Adjust layout
plt.subplots_adjust(top=0.8, bottom=0.05, hspace=0.4, wspace=0.6)
plt.show()










# In[11]
##################################################################################################
##################### SECTION 4: ANNUAL CAPACITY #################################################
##################################################################################################

# # --------------
# # Layout: 2 rows, 5 columns grid
# fig = plt.figure(figsize=(15, 9))  # Adjusted figure size for 2x5 layout
# gs = fig.add_gridspec(2, 5, height_ratios=[1, 1], width_ratios=[1, 1, 1, 1, 1])

# # Function to plot each country with annual fossil fuel capacity
# def plot_country(ax, df_country, country_name, loc, ylabel=None):
#     ax.plot(df_country.index, df_country['capacity_annual_cp'], label='NGFS Current Policies', color=colors['Current Policies'])
#     ax.plot(df_country.index, df_country['capacity_annual_nz'], label='NGFS Net Zero 2050', color=colors['Net Zero 2050'])
#     ax.plot(df_country.index, df_country['capacity_annual_nznew'], label='Carbon budget consistent Net Zero*', color=colors['Carbon Budget Consistent Net Zero'])
#     ax.set_xticks([str(year) for year in range(2030, 2051, 10)])
#     ax.set_title(f'{country_name}', fontsize=14, fontweight='bold', pad=10)
#     ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter_0dec))

#     # Set the y-axis label if specified
#     if ylabel:
#         ax.set_ylabel(ylabel, fontsize=12)
    
# # Plot countries in a 5x2 layout for fossil fuel capacity

# # First row
# ax_global = fig.add_subplot(gs[0, 0])
# plot_country(ax_global, df_country_global, 'Global', 'upper left', ylabel='GW')

# ax_emde = fig.add_subplot(gs[0, 1])
# plot_country(ax_emde, df_country_emde, 'EMDEs', 'upper right')

# ax_ind = fig.add_subplot(gs[0, 2])
# plot_country(ax_ind, df_country_ind, 'India', 'upper left')

# ax_usa = fig.add_subplot(gs[0, 3])
# plot_country(ax_usa, df_country_usa, 'USA', 'upper left')

# ax_vnm = fig.add_subplot(gs[0, 4])
# plot_country(ax_vnm, df_country_vnm, 'Vietnam', 'upper left')

# # Second row
# ax_idn = fig.add_subplot(gs[1, 0])
# plot_country(ax_idn, df_country_idn, 'Indonesia', 'upper left', ylabel='GW')

# ax_tur = fig.add_subplot(gs[1, 1])
# plot_country(ax_tur, df_country_tur, 'Türkiye', 'upper right')

# ax_deu = fig.add_subplot(gs[1, 2])
# plot_country(ax_deu, df_country_deu, 'Germany', 'upper left')

# ax_pol = fig.add_subplot(gs[1, 3])
# plot_country(ax_pol, df_country_pol, 'Poland', 'upper left')

# # Placeholder for additional chart
# ax_kaz = fig.add_subplot(gs[1, 4])
# plot_country(ax_kaz, df_country_kaz, 'Kazakhstan', 'upper left')  # Replace with actual data if needed

# # Main title
# fig.suptitle('Annual Fossil Fuel Capacity in Power Sector by Scenario', fontsize=16, fontweight='bold', y=0.98)

# # Subtitle
# fig.text(0.5, 0.93, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', ha='center', fontsize=12)
# fig.text(0.5, 0.88, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions \n with global carbon budget limiting warming to 1.5°C with 50% likelihood', ha='center', fontsize=12)

# # Legend for all charts
# handles, labels = ax_global.get_legend_handles_labels()
# fig.legend(handles, labels, loc='lower center', ncol=3, bbox_to_anchor=(0.5, 0.07), fontsize=10)

# # Adjust layout to bring the second row slightly higher
# plt.subplots_adjust(top=0.82, bottom=0.15, hspace=0.45, wspace=0.3)

# # Show the plot
# plt.show()










# In[11]
##################################################################################################
##################### SECTION 5: AVOIDED CAPACITY ################################################
##################################################################################################

# Function to plot both annual and cumulative avoided emissions on the same axes
def plot_combined(ax, df_country, region_name, ylabel_left=None, ylabel_right=None):
    # Plot annual avoided emissions on the left y-axis
    line1, = ax.plot(df_country.index, abs(df_country['capacity_annaul_avoided']), label='Annual Avoided Capacity', color=colors['Annual'])
    ax.set_xticks([str(year) for year in range(2030, 2051, 10)])
    ax.set_title(f'{region_name}', fontsize=12, fontweight='bold', pad=10)
    ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter_0dec))
    if ylabel_left:
        ax.set_ylabel(ylabel_left, fontsize=10)

    # Create a twin y-axis for cumulative avoided emissions
    ax2 = ax.twinx()
    line2, = ax2.plot(df_country.index, abs(df_country['capacity_cumulative_avoided']), label='Cumulative Avoided Capacity', color=colors['Cumulative'], linestyle='--')
    ax2.yaxis.set_major_formatter(FuncFormatter(thousands_formatter_0dec))
    if ylabel_right:
        ax2.set_ylabel(ylabel_right, fontsize=10)

    return [line1, line2]

# -------------------------
# First Graph: Global, DOPUNFCCC, DEVUNFCCC
fig1, axes1 = plt.subplots(1, 3, figsize=(12, 5))

# Collect handles for the legend
handles = []
handles += plot_combined(axes1[0], df_country_global, 'Global', ylabel_left='Annual (GW)')
handles += plot_combined(axes1[1], df_country_dopunfccc, 'Developed Countries')
handles += plot_combined(axes1[2], df_country_devunfccc, 'Developing Countries', ylabel_right='Cumulative (GW)')

# Main title for the first graph
fig1.suptitle('Avoided Fossil Fuel Capacity in Power Sector:\n Current Policies vs Carbon Budget Consistent Net Zero', fontsize=16, fontweight='bold', y=0.98)

# Subtitle
#fig1.text(0.5, 0.90, 'Emissions from current power plants in operation projected using NGFS GCAM6 model growth rates', ha='center', fontsize=12)
#fig1.text(0.5, 0.85, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions \n with global carbon budget limiting warming to 1.5°C with 50% likelihood', ha='center', fontsize=12)


# Single legend for the first graph
labels = ['Annual Avoided Capacity (Left axis)', 'Cumulative Avoided Capacity (Right axis)']
fig1.legend(handles, labels, loc='lower center', ncol=2, bbox_to_anchor=(0.5, -0.1), fontsize=10)

# Adjust layout
fig1.subplots_adjust(top=0.80, bottom=0.05, hspace=0.4, wspace=0.6)
plt.show()



# -------------------------
# Second Graph: 8 Countries
fig2 = plt.figure(figsize=(12, 6))  # Adjusted figure size
gs2 = fig2.add_gridspec(2, 4, height_ratios=[1, 1], width_ratios=[1, 1, 1, 1])

# Collect handles for the legend
handles = []

# First row
#handles += plot_combined(fig2.add_subplot(gs2[0, 0]), df_country_ind, 'India', ylabel_left='Annual (GW)')
#handles += plot_combined(fig2.add_subplot(gs2[0, 1]), df_country_idn, 'Indonesia')
handles += plot_combined(fig2.add_subplot(gs2[0, 2]), df_country_tur, 'Türkiye', ylabel_left='Annual (GW)', ylabel_right='Cumulative (GW)')
#handles += plot_combined(fig2.add_subplot(gs2[0, 3]), df_country_mex, 'Mexico', ylabel_right='Cumulative (GW)')

# Second row
#handles += plot_combined(fig2.add_subplot(gs2[1, 0]), df_country_vnm, 'Viet Nam', ylabel_left='Annual (GW)')
#handles += plot_combined(fig2.add_subplot(gs2[1, 1]), df_country_irn, 'Iran')
handles += plot_combined(fig2.add_subplot(gs2[1, 2]), df_country_bgd, 'Bangladesh', ylabel_left='Annual (GW)', ylabel_right='Cumulative (GW)')
#handles += plot_combined(fig2.add_subplot(gs2[1, 3]), df_country_egy, 'Egypt', ylabel_right='Cumulative (GW)')

# Main title for the second graph
fig2.suptitle('Avoided Fossil Fuel Capacity in Power Sector:\n Current Policies vs Carbon Budget Consistent Net Zero', fontsize=16, fontweight='bold', y=0.98)

# Subtitle
#fig2.text(0.5, 0.90, 'Emissions from current power plants in operation projected using NGFS GCAM6 model growth rates', ha='center', fontsize=12)
#fig2.text(0.5, 0.85, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions \n with global carbon budget limiting warming to 1.5°C with 50% likelihood', ha='center', fontsize=12)


# Single legend for the second graph
labels = ['Annual Avoided Capacity (Left axis)', 'Cumulative Avoided Capacity (Right axis)']
fig2.legend(handles, labels, loc='lower center', ncol=2, bbox_to_anchor=(0.5, -0.1), fontsize=10)

# Adjust layout
plt.subplots_adjust(top=0.8, bottom=0.05, hspace=0.4, wspace=0.6)
plt.show()










# In[11]
##################################################################################################
##################### SECTION 6: BY FUEL: EMISSIONS ##############################################
##################################################################################################

# --------------
# Ensure the years_columns array has the correct length for country data
years_columns_countries = years_columns[:len(df_emissions_currentpolicy_chn.columns[8:])]
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




# --------------
# First Graph: Global, DOPUNFCCC, DEVUNFCCC
fig = plt.figure(figsize=(12, 5))  # Adjusted figure size for 2x5 layout
gs = fig.add_gridspec(1, 3, height_ratios=[1], width_ratios=[1, 1, 1])


# First row
ax_global = fig.add_subplot(gs[0, 0])
plot_country_emissions(ax_global, df_emissions_currentpolicy_global, df_emissions_nz1550v2_global, 'Global', ylabel="GtCO2eq", is_global= True)

ax_dopunfccc = fig.add_subplot(gs[0, 1])
plot_country_emissions(ax_dopunfccc, df_emissions_currentpolicy_dopunfccc, df_emissions_nz1550v2_dopunfccc, 'Developed Countries', is_global= True)

ax_devunfccc = fig.add_subplot(gs[0, 2])
plot_country_emissions(ax_devunfccc, df_emissions_currentpolicy_devunfccc, df_emissions_nz1550v2_devunfccc, 'Developing Countries', is_global= True)

# Main title
fig.suptitle('Annual Emissions from Power Sector by Scenario and Fuel Type', fontsize=16, fontweight='bold', y=0.98)

# Subtitle
#fig.text(0.5, 0.93, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', ha='center', fontsize=12)
#fig.text(0.5, 0.90, 'Solid line: Carbon budget consistent Net Zero* | Dotted line: Current Policies', ha='center', fontsize=12)
#fig.text(0.5, 0.85, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions \n with global carbon budget limiting warming to 1.5°C with 50% likelihood', ha='center', fontsize=12)

# Legend for all charts (handles from one plot)
handles, labels = ax_chn.get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', ncol=3, bbox_to_anchor=(0.5, -0.05), fontsize=10)

# Adjust the spacing to move the charts lower and create space between rows
plt.subplots_adjust(top=0.85, bottom=0.15, hspace=0.4, wspace=0.4)

# Show the plot
plt.show()



# --------------
# Second Graph: 8 Countries
fig = plt.figure(figsize=(12, 6))  # Adjusted figure size for 2x5 layout
gs = fig.add_gridspec(2, 4, height_ratios=[1, 1], width_ratios=[1, 1, 1, 1])


# First row
#ax_ind = fig.add_subplot(gs[0, 0])
#plot_country_emissions(ax_ind, df_emissions_currentpolicy_ind, df_emissions_nz1550v2_ind, 'India', ylabel="GtCO2eq")

#ax_idn = fig.add_subplot(gs[0, 1])
#plot_country_emissions(ax_idn, df_emissions_currentpolicy_idn, df_emissions_nz1550v2_idn, 'Indonesia')

ax_tur = fig.add_subplot(gs[0, 2])
plot_country_emissions(ax_tur, df_emissions_currentpolicy_tur, df_emissions_nz1550v2_tur, 'Türkiye', ylabel="GtCO2eq")

#ax_mex = fig.add_subplot(gs[0, 3])
#plot_country_emissions(ax_mex, df_emissions_currentpolicy_mex, df_emissions_nz1550v2_mex, 'Mexico')

# Second row
#ax_vnm = fig.add_subplot(gs[1, 0])
#plot_country_emissions(ax_vnm, df_emissions_currentpolicy_vnm, df_emissions_nz1550v2_vnm, 'Viet Nam', ylabel="GtCO2eq")

#ax_irn = fig.add_subplot(gs[1, 1])
#plot_country_emissions(ax_irn, df_emissions_currentpolicy_irn, df_emissions_nz1550v2_irn, 'Iran')

ax_bgd = fig.add_subplot(gs[1, 2])
plot_country_emissions(ax_bgd, df_emissions_currentpolicy_bgd, df_emissions_nz1550v2_bgd, 'Bangladesh', ylabel="GtCO2eq")

#ax_egy = fig.add_subplot(gs[1, 3])
#plot_country_emissions(ax_egy, df_emissions_currentpolicy_egy, df_emissions_nz1550v2_egy, 'Egypt')

# Main title
fig.suptitle('Annual Emissions from Power Sector by Scenario and Fuel Type', fontsize=16, fontweight='bold', y=0.98)

# Subtitle
#fig.text(0.5, 0.93, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', ha='center', fontsize=12)
#fig.text(0.5, 0.90, 'Solid line: Carbon budget consistent Net Zero* | Dotted line: Current Policies', ha='center', fontsize=12)
#fig.text(0.5, 0.85, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions \n with global carbon budget limiting warming to 1.5°C with 50% likelihood', ha='center', fontsize=12)

# Legend for all charts (handles from one plot)
handles, labels = ax_chn.get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', ncol=3, bbox_to_anchor=(0.5, -0.05), fontsize=10)

# Adjust the spacing to move the charts lower and create space between rows
plt.subplots_adjust(top=0.85, bottom=0.12, hspace=0.6, wspace=0.4)

# Show the plot
plt.show()












# In[11]
##################################################################################################
##################### SECTION 7: BY FUEL: AVOIDED CAPACITY --- ANNUAL & CUMULATIVE ###############
##################################################################################################

# --------------
# ANNUAL
# Ensure the years_columns array has the correct length for country and global data
years_columns_countries = years_columns[:len(df_byfuel_avoided_annual_chn.columns[8:])]
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


# --------------
# First Graph: Global, DOPUNFCCC, DEVUNFCCC
fig = plt.figure(figsize=(12, 5))  # Adjusted figure size for 2x5 layout
gs = fig.add_gridspec(1, 3, height_ratios=[1], width_ratios=[1, 1, 1])


# First row
ax_global = fig.add_subplot(gs[0, 0])
plot_country_avoided_emissions(ax_global, df_byfuel_avoided_annual_global, 'Global', ylabel="GW", is_global= True)

ax_dopunfccc = fig.add_subplot(gs[0, 1])
plot_country_avoided_emissions(ax_dopunfccc, df_byfuel_avoided_annual_dopunfccc, 'Developed Countries', is_global= True)

ax_devunfccc = fig.add_subplot(gs[0, 2])
plot_country_avoided_emissions(ax_devunfccc, df_byfuel_avoided_annual_devunfccc, 'Developing Countries', is_global= True)

# Main title
fig.suptitle('Annual Avoided Fossil Fuel Capacity in Power Sector:\n Current Policies vs Carbon Budget Consistent Net Zero', fontsize=16, fontweight='bold', y=0.98)

# Subtitle
#fig.text(0.5, 0.93, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', ha='center', fontsize=12)
#fig.text(0.5, 0.90, 'Solid line: Carbon budget consistent Net Zero* | Dotted line: Current Policies', ha='center', fontsize=12)
#fig.text(0.5, 0.85, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions \n with global carbon budget limiting warming to 1.5°C with 50% likelihood', ha='center', fontsize=12)

# Legend for all charts (handles from one plot)
handles, labels = ax_chn.get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', ncol=3, bbox_to_anchor=(0.5, -0.1), fontsize=10)

# Adjust the spacing to move the charts lower and create space between rows
plt.subplots_adjust(top=0.80, bottom=0.05, hspace=0.4, wspace=0.6)

# Show the plot
plt.show()



# --------------
# Second Graph: 8 Countries
fig = plt.figure(figsize=(12, 6))  # Adjusted figure size for 2x5 layout
gs = fig.add_gridspec(2, 4, height_ratios=[1, 1], width_ratios=[1, 1, 1, 1])


# First row
#ax_ind = fig.add_subplot(gs[0, 0])
#plot_country_avoided_emissions(ax_ind, df_byfuel_avoided_annual_ind, 'India', ylabel="GW")

#ax_idn = fig.add_subplot(gs[0, 1])
#plot_country_avoided_emissions(ax_idn, df_byfuel_avoided_annual_idn, 'Indonesia')

ax_tur = fig.add_subplot(gs[0, 2])
plot_country_avoided_emissions(ax_tur, df_byfuel_avoided_annual_tur, 'Türkiye', ylabel="GW")

#ax_mex = fig.add_subplot(gs[0, 3])
#plot_country_avoided_emissions(ax_mex, df_byfuel_avoided_annual_mex, 'Mexico')

# Second row
#ax_vnm = fig.add_subplot(gs[1, 0])
#plot_country_avoided_emissions(ax_vnm, df_byfuel_avoided_annual_vnm, 'Viet Nam', ylabel="GW")

#ax_irn = fig.add_subplot(gs[1, 1])
#plot_country_avoided_emissions(ax_irn, df_byfuel_avoided_annual_irn, 'Iran')

ax_bgd = fig.add_subplot(gs[1, 2])
plot_country_avoided_emissions(ax_bgd, df_byfuel_avoided_annual_bgd, 'Bangladesh', ylabel="GW")

#ax_egy = fig.add_subplot(gs[1, 3])
#plot_country_avoided_emissions(ax_egy, df_byfuel_avoided_annual_egy, 'Egypt')

# Main title
fig.suptitle('Annual Avoided Fossil Fuel Capacity in Power Sector:\n Current Policies vs Carbon Budget Consistent Net Zero', fontsize=16, fontweight='bold', y=0.98)

# Subtitle
#fig.text(0.5, 0.93, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', ha='center', fontsize=12)
#fig.text(0.5, 0.90, 'Solid line: Carbon budget consistent Net Zero* | Dotted line: Current Policies', ha='center', fontsize=12)
#fig.text(0.5, 0.85, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions \n with global carbon budget limiting warming to 1.5°C with 50% likelihood', ha='center', fontsize=12)

# Legend for all charts (handles from one plot)
handles, labels = ax_chn.get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', ncol=3, bbox_to_anchor=(0.5, -0.1), fontsize=10)

# Adjust the spacing to move the charts lower and create space between rows
plt.subplots_adjust(top=0.80, bottom=0.05, hspace=0.4, wspace=0.6)

# Show the plot
plt.show()








# --------------
# CUMULATIVE
# Ensure the years_columns array has the correct length for country and global data
years_columns_countries = years_columns[:len(df_byfuel_avoided_annual_chn.columns[8:])]
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


# --------------
# First Graph: Global, DOPUNFCCC, DEVUNFCCC
fig = plt.figure(figsize=(12, 5))  # Adjusted figure size for 2x5 layout
gs = fig.add_gridspec(1, 3, height_ratios=[1], width_ratios=[1, 1, 1])


# First row
ax_global = fig.add_subplot(gs[0, 0])
plot_country_avoided_emissions(ax_global, df_byfuel_avoided_cumulative_global, 'Global', ylabel="GW", is_global= True)

ax_dopunfccc = fig.add_subplot(gs[0, 1])
plot_country_avoided_emissions(ax_dopunfccc, df_byfuel_avoided_cumulative_dopunfccc, 'Developed Countries', is_global= True)

ax_devunfccc = fig.add_subplot(gs[0, 2])
plot_country_avoided_emissions(ax_devunfccc, df_byfuel_avoided_cumulative_devunfccc, 'Developing Countries', is_global= True)

# Main title
fig.suptitle('Cumulative Avoided Fossil Fuel Capacity in Power Sector:\n Current Policies vs Carbon Budget Consistent Net Zero', fontsize=16, fontweight='bold', y=0.98)

# Subtitle
#fig.text(0.5, 0.93, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', ha='center', fontsize=12)
#fig.text(0.5, 0.90, 'Solid line: Carbon budget consistent Net Zero* | Dotted line: Current Policies', ha='center', fontsize=12)
#fig.text(0.5, 0.85, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions \n with global carbon budget limiting warming to 1.5°C with 50% likelihood', ha='center', fontsize=12)

# Legend for all charts (handles from one plot)
handles, labels = ax_chn.get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', ncol=3, bbox_to_anchor=(0.5, -0.1), fontsize=10)

# Adjust the spacing to move the charts lower and create space between rows
plt.subplots_adjust(top=0.80, bottom=0.05, hspace=0.4, wspace=0.6)

# Show the plot
plt.show()



# --------------
# Second Graph: 8 Countries
fig = plt.figure(figsize=(12, 6))  # Adjusted figure size for 2x5 layout
gs = fig.add_gridspec(2, 4, height_ratios=[1, 1], width_ratios=[1, 1, 1, 1])


# First row
#ax_ind = fig.add_subplot(gs[0, 0])
#plot_country_avoided_emissions(ax_ind, df_byfuel_avoided_cumulative_ind, 'India', ylabel="GW")

#ax_idn = fig.add_subplot(gs[0, 1])
#plot_country_avoided_emissions(ax_idn, df_byfuel_avoided_cumulative_idn, 'Indonesia')

ax_tur = fig.add_subplot(gs[0, 2])
plot_country_avoided_emissions(ax_tur, df_byfuel_avoided_cumulative_tur, 'Türkiye', ylabel="GW")

#ax_mex = fig.add_subplot(gs[0, 3])
#plot_country_avoided_emissions(ax_mex, df_byfuel_avoided_cumulative_mex, 'Mexico')

# Second row
#ax_vnm = fig.add_subplot(gs[1, 0])
#plot_country_avoided_emissions(ax_vnm, df_byfuel_avoided_cumulative_vnm, 'Viet Nam', ylabel="GW")

#ax_irn = fig.add_subplot(gs[1, 1])
#plot_country_avoided_emissions(ax_irn, df_byfuel_avoided_cumulative_irn, 'Iran')

ax_bgd = fig.add_subplot(gs[1, 2])
plot_country_avoided_emissions(ax_bgd, df_byfuel_avoided_cumulative_bgd, 'Bangladesh', ylabel="GW")

#ax_egy = fig.add_subplot(gs[1, 3])
#plot_country_avoided_emissions(ax_egy, df_byfuel_avoided_cumulative_egy, 'Egypt')

# Main title
fig.suptitle('Cumulative Avoided Fossil Fuel Capacity in Power Sector:\n Current Policies vs Carbon Budget Consistent Net Zero', fontsize=16, fontweight='bold', y=0.98)

# Subtitle
#fig.text(0.5, 0.93, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', ha='center', fontsize=12)
#fig.text(0.5, 0.90, 'Solid line: Carbon budget consistent Net Zero* | Dotted line: Current Policies', ha='center', fontsize=12)
#fig.text(0.5, 0.85, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions \n with global carbon budget limiting warming to 1.5°C with 50% likelihood', ha='center', fontsize=12)

# Legend for all charts (handles from one plot)
handles, labels = ax_chn.get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', ncol=3, bbox_to_anchor=(0.5, -0.1), fontsize=10)

# Adjust the spacing to move the charts lower and create space between rows
plt.subplots_adjust(top=0.80, bottom=0.05, hspace=0.4, wspace=0.6)

# Show the plot
plt.show()




