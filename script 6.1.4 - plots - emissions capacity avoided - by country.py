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
from matplotlib.lines import Line2D










# In[3]:
# directory & load data

# --------------
# LOAD DATA










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
def plot1_annual_emissions(ax, df_country, region_name, ylabel=None):
    ax.plot(df_country.index, df_country['ghg_annual_cp'], label='NGFS Current Policies', color=colors['Current Policies'])
    ax.plot(df_country.index, df_country['ghg_annual_nz'], label='NGFS Net Zero 2050', color=colors['Net Zero 2050'])
    ax.plot(df_country.index, df_country['ghg_annual_nznew'], label='Carbon Budget Consistent Net Zero', color=colors['Carbon Budget Consistent Net Zero'])
    ax.set_xticks([str(year) for year in range(2030, 2051, 10)])
    ax.set_title(f'{region_name}', fontsize=12, fontweight='bold', pad=10)
    ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter_2dec))
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=10)


# --------------
# First Graph: Global, DOPUNFCCC, DEVUNFCCC
fig1, axes1 = plt.subplots(1, 3, figsize=(12, 5))
plot1_annual_emissions(axes1[0], df_country_global, 'Global', ylabel='GtCO2eq')
plot1_annual_emissions(axes1[1], df_country_dopunfccc, 'Developed Countries')
plot1_annual_emissions(axes1[2], df_country_devunfccc, 'Developing Countries')

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


# --------------
# Second Graph: 8 Countries
fig2 = plt.figure(figsize=(12, 6))  # Adjusted figure size
gs2 = fig2.add_gridspec(2, 4, height_ratios=[1, 1], width_ratios=[1, 1, 1, 1])

# First row
plot1_annual_emissions(fig2.add_subplot(gs2[0, 0]), df_country_ind, 'India', ylabel='GtCO2eq')
plot1_annual_emissions(fig2.add_subplot(gs2[0, 1]), df_country_idn, 'Indonesia')
plot1_annual_emissions(fig2.add_subplot(gs2[0, 2]), df_country_zaf, 'South Africa')
plot1_annual_emissions(fig2.add_subplot(gs2[0, 3]), df_country_mex, 'Mexico')

# Second row
plot1_annual_emissions(fig2.add_subplot(gs2[1, 0]), df_country_vnm, 'Viet Nam', ylabel='GtCO2eq')
plot1_annual_emissions(fig2.add_subplot(gs2[1, 1]), df_country_irn, 'Iran')
plot1_annual_emissions(fig2.add_subplot(gs2[1, 2]), df_country_tha, 'Thailand')
plot1_annual_emissions(fig2.add_subplot(gs2[1, 3]), df_country_egy, 'Egypt')

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
def plot2_cumulative_emissions(ax, df_country, region_name, ylabel=None):
    ax.plot(df_country.index, df_country['ghg_cumulative_cp'], label='NGFS Current Policies', color=colors['Current Policies'])
    ax.plot(df_country.index, df_country['ghg_cumulative_nz'], label='NGFS Net Zero 2050', color=colors['Net Zero 2050'])
    ax.plot(df_country.index, df_country['ghg_cumulative_nznew'], label='Carbon Budget Consistent Net Zero', color=colors['Carbon Budget Consistent Net Zero'])
    ax.set_xticks([str(year) for year in range(2030, 2051, 10)])
    ax.set_title(f'{region_name}', fontsize=12, fontweight='bold', pad=10)
    ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter_1dec))
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=10)


# --------------
# First Graph: Global, DOPUNFCCC, DEVUNFCCC
fig1, axes1 = plt.subplots(1, 3, figsize=(12, 5))
plot2_cumulative_emissions(axes1[0], df_country_global, 'Global', ylabel='GtCO2eq')
plot2_cumulative_emissions(axes1[1], df_country_dopunfccc, 'Developed Countries')
plot2_cumulative_emissions(axes1[2], df_country_devunfccc, 'Developing Countries')

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


# --------------
# Second Graph: 8 Countries
fig2 = plt.figure(figsize=(12, 6))  # Adjusted figure size
gs2 = fig2.add_gridspec(2, 4, height_ratios=[1, 1], width_ratios=[1, 1, 1, 1])

# First row
plot2_cumulative_emissions(fig2.add_subplot(gs2[0, 0]), df_country_ind, 'India', ylabel='GtCO2eq')
plot2_cumulative_emissions(fig2.add_subplot(gs2[0, 1]), df_country_idn, 'Indonesia')
plot2_cumulative_emissions(fig2.add_subplot(gs2[0, 2]), df_country_zaf, 'South Africa')
plot2_cumulative_emissions(fig2.add_subplot(gs2[0, 3]), df_country_mex, 'Mexico')

# Second row
plot2_cumulative_emissions(fig2.add_subplot(gs2[1, 0]), df_country_vnm, 'Viet Nam', ylabel='GtCO2eq')
plot2_cumulative_emissions(fig2.add_subplot(gs2[1, 1]), df_country_irn, 'Iran')
plot2_cumulative_emissions(fig2.add_subplot(gs2[1, 2]), df_country_tha, 'Thailand')
plot2_cumulative_emissions(fig2.add_subplot(gs2[1, 3]), df_country_egy, 'Egypt')

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

# --------------
# Function to plot both annual and cumulative avoided emissions on the same axes
def plot3_avoided_capacity(ax, df_country, region_name, ylabel_left=None, ylabel_right=None):
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


# --------------
# First Graph: Global, DOPUNFCCC, DEVUNFCCC
fig1, axes1 = plt.subplots(1, 3, figsize=(12, 5))

# Collect handles for the legend
handles = []
handles += plot3_avoided_capacity(axes1[0], df_country_global, 'Global', ylabel_left='Annual (GtCO2eq)')
handles += plot3_avoided_capacity(axes1[1], df_country_dopunfccc, 'Developed Countries')
handles += plot3_avoided_capacity(axes1[2], df_country_devunfccc, 'Developing Countries', ylabel_right='Cumulative (GtCO2)')

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


# --------------
# Second Graph: 8 Countries
fig2 = plt.figure(figsize=(12, 6))  # Adjusted figure size
gs2 = fig2.add_gridspec(2, 4, height_ratios=[1, 1], width_ratios=[1, 1, 1, 1])

# Collect handles for the legend
handles = []

# First row
handles += plot3_avoided_capacity(fig2.add_subplot(gs2[0, 0]), df_country_ind, 'India', ylabel_left='Annual (GtCO2eq)')
handles += plot3_avoided_capacity(fig2.add_subplot(gs2[0, 1]), df_country_idn, 'Indonesia')
handles += plot3_avoided_capacity(fig2.add_subplot(gs2[0, 2]), df_country_zaf, 'South Africa')
handles += plot3_avoided_capacity(fig2.add_subplot(gs2[0, 3]), df_country_mex, 'Mexico', ylabel_right='Cumulative (GtCO2)')

# Second row
handles += plot3_avoided_capacity(fig2.add_subplot(gs2[1, 0]), df_country_vnm, 'Viet Nam', ylabel_left='Annual (GtCO2eq)')
handles += plot3_avoided_capacity(fig2.add_subplot(gs2[1, 1]), df_country_irn, 'Iran')
handles += plot3_avoided_capacity(fig2.add_subplot(gs2[1, 2]), df_country_tha, 'Thailand')
handles += plot3_avoided_capacity(fig2.add_subplot(gs2[1, 3]), df_country_egy, 'Egypt', ylabel_right='Cumulative (GtCO2)')

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

# --------------
# Function to plot a region or country
def plot4_annual_capacity(ax, df_country, region_name, ylabel=None):
    ax.plot(df_country.index, df_country['capacity_annual_cp'], label='NGFS Current Policies', color=colors['Current Policies'])
    ax.plot(df_country.index, df_country['capacity_annual_nz'], label='NGFS Net Zero 2050', color=colors['Net Zero 2050'])
    ax.plot(df_country.index, df_country['capacity_annual_nznew'], label='Carbon Budget Consistent Net Zero', color=colors['Carbon Budget Consistent Net Zero'])
    ax.set_xticks([str(year) for year in range(2030, 2051, 10)])
    ax.set_title(f'{region_name}', fontsize=12, fontweight='bold', pad=10)
    ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter_2dec))
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=10)


# --------------
# First Graph: Global, DOPUNFCCC, DEVUNFCCC
fig1, axes1 = plt.subplots(1, 3, figsize=(12, 5))
plot4_annual_capacity(axes1[0], df_country_global, 'Global', ylabel='GW')
plot4_annual_capacity(axes1[1], df_country_dopunfccc, 'Developed Countries')
plot4_annual_capacity(axes1[2], df_country_devunfccc, 'Developing Countries')

# Main title for the first graph
fig1.suptitle('Annual Fossil Fuel Capacity in Power Sector by Scenario', fontsize=16, fontweight='bold', y=0.98)

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


# --------------
# Second Graph: 8 Countries
fig2 = plt.figure(figsize=(12, 6))  # Adjusted figure size
gs2 = fig2.add_gridspec(2, 4, height_ratios=[1, 1], width_ratios=[1, 1, 1, 1])

# First row
plot4_annual_capacity(fig2.add_subplot(gs2[0, 0]), df_country_ind, 'India', ylabel='GW')
plot4_annual_capacity(fig2.add_subplot(gs2[0, 1]), df_country_idn, 'Indonesia')
plot4_annual_capacity(fig2.add_subplot(gs2[0, 2]), df_country_zaf, 'South Africa')
plot4_annual_capacity(fig2.add_subplot(gs2[0, 3]), df_country_mex, 'Mexico')

# Second row
plot4_annual_capacity(fig2.add_subplot(gs2[1, 0]), df_country_vnm, 'Viet Nam', ylabel='GW')
plot4_annual_capacity(fig2.add_subplot(gs2[1, 1]), df_country_irn, 'Iran')
plot4_annual_capacity(fig2.add_subplot(gs2[1, 2]), df_country_tha, 'Thailand')
plot4_annual_capacity(fig2.add_subplot(gs2[1, 3]), df_country_egy, 'Egypt')

# Main title for the second graph
fig2.suptitle('Annual Fossil Fuel Capacity in Power Sector by Scenario', fontsize=16, fontweight='bold', y=0.98)

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
##################### SECTION 5: CAPACITY REDUCTION ##############################################
##################################################################################################

# --------------
# Function to plot both annual and cumulative avoided emissions on the same axes
def plot5_capacity_reduction(ax, df_country, region_name, ylabel_left=None, ylabel_right=None):
    # Plot annual avoided emissions on the left y-axis
    line1, = ax.plot(df_country.index, df_country['capacity_annaul_reduction']*(-1), color=colors['Annual'])
    ax.set_xticks([str(year) for year in range(2030, 2051, 10)])
    ax.set_title(f'{region_name}', fontsize=12, fontweight='bold', pad=10)
    ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter_0dec))
    if ylabel_left:
        ax.set_ylabel(ylabel_left, fontsize=10)

    # Create a twin y-axis for cumulative avoided emissions
    ax2 = ax.twinx()
    line2, = ax2.plot(df_country.index, df_country['capacity_cumulative_reduction']*(-1), color=colors['Cumulative'], linestyle='--')
    ax2.yaxis.set_major_formatter(FuncFormatter(thousands_formatter_0dec))
    if ylabel_right:
        ax2.set_ylabel(ylabel_right, fontsize=10)

    return [line1, line2]


# --------------
# First Graph: Global, DOPUNFCCC, DEVUNFCCC
fig1, axes1 = plt.subplots(1, 3, figsize=(12, 5))

# Collect handles for the legend
handles = []
handles += plot5_capacity_reduction(axes1[0], df_country_global, 'Global', ylabel_left='Annual (GW)')
handles += plot5_capacity_reduction(axes1[1], df_country_dopunfccc, 'Developed Countries')
handles += plot5_capacity_reduction(axes1[2], df_country_devunfccc, 'Developing Countries', ylabel_right='Cumulative (GW)')

# Main title for the first graph
fig1.suptitle('Fossil Fuel Capacity Reduction in Power Sector: \n Carbon Budget Consistent Net Zero', fontsize=16, fontweight='bold', y=0.98)

# Subtitle
#fig1.text(0.5, 0.90, 'Emissions from current power plants in operation projected using NGFS GCAM6 model growth rates', ha='center', fontsize=12)
#fig1.text(0.5, 0.85, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions \n with global carbon budget limiting warming to 1.5°C with 50% likelihood', ha='center', fontsize=12)


# Single legend for the first graph
labels = ['Annual Capacity Reduction (Left axis)', 'Cumulative Capacity Reduction (Right axis)']
fig1.legend(handles, labels, loc='lower center', ncol=2, bbox_to_anchor=(0.5, -0.1), fontsize=10)

# Adjust layout
fig1.subplots_adjust(top=0.80, bottom=0.05, hspace=0.4, wspace=0.6)
plt.show()


# --------------
# Second Graph: 8 Countries
fig2 = plt.figure(figsize=(12, 6))  # Adjusted figure size
gs2 = fig2.add_gridspec(2, 4, height_ratios=[1, 1], width_ratios=[1, 1, 1, 1])

# Collect handles for the legend
handles = []

# First row
handles += plot5_capacity_reduction(fig2.add_subplot(gs2[0, 0]), df_country_ind, 'India', ylabel_left='Annual (GW)')
handles += plot5_capacity_reduction(fig2.add_subplot(gs2[0, 1]), df_country_idn, 'Indonesia')
handles += plot5_capacity_reduction(fig2.add_subplot(gs2[0, 2]), df_country_zaf, 'South Africa')
handles += plot5_capacity_reduction(fig2.add_subplot(gs2[0, 3]), df_country_mex, 'Mexico', ylabel_right='Cumulative (GW)')

# Second row
handles += plot5_capacity_reduction(fig2.add_subplot(gs2[1, 0]), df_country_vnm, 'Viet Nam', ylabel_left='Annual (GW)')
handles += plot5_capacity_reduction(fig2.add_subplot(gs2[1, 1]), df_country_irn, 'Iran')
handles += plot5_capacity_reduction(fig2.add_subplot(gs2[1, 2]), df_country_tha, 'Thailand')
handles += plot5_capacity_reduction(fig2.add_subplot(gs2[1, 3]), df_country_egy, 'Egypt', ylabel_right='Cumulative (GW)')

# Main title for the second graph
fig2.suptitle('Fossil Fuel Capacity Reduction in Power Sector: \n Carbon Budget Consistent Net Zero', fontsize=16, fontweight='bold', y=0.98)

# Subtitle
#fig2.text(0.5, 0.90, 'Emissions from current power plants in operation projected using NGFS GCAM6 model growth rates', ha='center', fontsize=12)
#fig2.text(0.5, 0.85, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions \n with global carbon budget limiting warming to 1.5°C with 50% likelihood', ha='center', fontsize=12)


# Single legend for the second graph
labels = ['Annual Capacity Reduction (Left axis)', 'Cumulative Capacity Reduction (Right axis)']
fig2.legend(handles, labels, loc='lower center', ncol=2, bbox_to_anchor=(0.5, -0.1), fontsize=10)

# Adjust layout
plt.subplots_adjust(top=0.8, bottom=0.05, hspace=0.4, wspace=0.6)
plt.show()










# In[11]
##################################################################################################
##################### SECTION 6: BY FUEL: EMISSIONS ##############################################
##################################################################################################

# --------------
# Function to plot emissions by fuel type for each country or global
def plot6_emissions_byfuel(ax, df_current_policy, df_nz_policy, country_name, ylabel=None, is_global=False):
    # Adjust starting column based on whether it's global or country data
    start_col = 1 if is_global else 8  # Use 1 for global, 8 for countries
    
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
plot6_emissions_byfuel(ax_global, df_emissions_currentpolicy_global, df_emissions_nz1550v2_global, 'Global', ylabel="GtCO2eq", is_global= True)

ax_dopunfccc = fig.add_subplot(gs[0, 1])
plot6_emissions_byfuel(ax_dopunfccc, df_emissions_currentpolicy_dopunfccc, df_emissions_nz1550v2_dopunfccc, 'Developed Countries', is_global= True)

ax_devunfccc = fig.add_subplot(gs[0, 2])
plot6_emissions_byfuel(ax_devunfccc, df_emissions_currentpolicy_devunfccc, df_emissions_nz1550v2_devunfccc, 'Developing Countries', is_global= True)

# Main title
fig.suptitle('Annual Emissions from Power Sector by Scenario and Fuel Type', fontsize=16, fontweight='bold', y=0.98)

# Subtitle
#fig.text(0.5, 0.93, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', ha='center', fontsize=12)
#fig.text(0.5, 0.90, 'Solid line: Carbon budget consistent Net Zero* | Dotted line: Current Policies', ha='center', fontsize=12)
#fig.text(0.5, 0.85, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions \n with global carbon budget limiting warming to 1.5°C with 50% likelihood', ha='center', fontsize=12)

# Legend for all charts (handles from one plot)
handles, labels = ax_global.get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', ncol=3, bbox_to_anchor=(0.5, -0.1), fontsize=10)

# Add a second legend for line styles
solid_line = Line2D([0], [0], color='black', lw=2, linestyle='-')
dashed_line = Line2D([0], [0], color='black', lw=2, linestyle='--')
fig.legend([solid_line, dashed_line], ['Carbon Budget Consistent Net Zero', 'Current Policies'], 
           loc='upper center', ncol=2, bbox_to_anchor=(0.5, -0.1), fontsize=10)

plt.subplots_adjust(top=0.80, bottom=0.05, hspace=0.4, wspace=0.6)

# Show the plot
plt.show()


# --------------
# Second Graph: 8 Countries
fig = plt.figure(figsize=(12, 6))  # Adjusted figure size for 2x5 layout
gs = fig.add_gridspec(2, 4, height_ratios=[1, 1], width_ratios=[1, 1, 1, 1])


# First row
ax_ind = fig.add_subplot(gs[0, 0])
plot6_emissions_byfuel(ax_ind, df_emissions_currentpolicy_ind, df_emissions_nz1550v2_ind, 'India', ylabel="GtCO2eq")

ax_idn = fig.add_subplot(gs[0, 1])
plot6_emissions_byfuel(ax_idn, df_emissions_currentpolicy_idn, df_emissions_nz1550v2_idn, 'Indonesia')

ax_zaf = fig.add_subplot(gs[0, 2])
plot6_emissions_byfuel(ax_zaf, df_emissions_currentpolicy_zaf, df_emissions_nz1550v2_zaf, 'South Africa')

ax_mex = fig.add_subplot(gs[0, 3])
plot6_emissions_byfuel(ax_mex, df_emissions_currentpolicy_mex, df_emissions_nz1550v2_mex, 'Mexico')

# Second row
ax_vnm = fig.add_subplot(gs[1, 0])
plot6_emissions_byfuel(ax_vnm, df_emissions_currentpolicy_vnm, df_emissions_nz1550v2_vnm, 'Viet Nam', ylabel="GtCO2eq")

ax_irn = fig.add_subplot(gs[1, 1])
plot6_emissions_byfuel(ax_irn, df_emissions_currentpolicy_irn, df_emissions_nz1550v2_irn, 'Iran')

ax_tha = fig.add_subplot(gs[1, 2])
plot6_emissions_byfuel(ax_tha, df_emissions_currentpolicy_tha, df_emissions_nz1550v2_tha, 'Thailand')

ax_egy = fig.add_subplot(gs[1, 3])
plot6_emissions_byfuel(ax_egy, df_emissions_currentpolicy_egy, df_emissions_nz1550v2_egy, 'Egypt')

# Main title
fig.suptitle('Annual Emissions from Power Sector by Scenario and Fuel Type', fontsize=16, fontweight='bold', y=0.98)

# Subtitle
#fig.text(0.5, 0.93, 'Emissions from current power plants in operation are projected using growth rates from NGFS GCAM6 model', ha='center', fontsize=12)
#fig.text(0.5, 0.90, 'Solid line: Carbon budget consistent Net Zero* | Dotted line: Current Policies', ha='center', fontsize=12)
#fig.text(0.5, 0.85, '*Annual growth rates from NGFS GCAM6 model are modified to align global cumulative emissions \n with global carbon budget limiting warming to 1.5°C with 50% likelihood', ha='center', fontsize=12)

# Legend for all charts (handles from one plot)
handles, labels = ax_ind.get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', ncol=3, bbox_to_anchor=(0.5, -0.1), fontsize=10)

# Add a second legend for line styles
solid_line = Line2D([0], [0], color='black', lw=2, linestyle='-')
dashed_line = Line2D([0], [0], color='black', lw=2, linestyle='--')
fig.legend([solid_line, dashed_line], ['Carbon Budget Consistent Net Zero', 'Current Policies'], 
           loc='upper center', ncol=2, bbox_to_anchor=(0.5, -0.1), fontsize=10)

# Adjust the spacing to move the charts lower and create space between rows
plt.subplots_adjust(top=0.80, bottom=0.05, hspace=0.4, wspace=0.6)

# Show the plot
plt.show()












# In[11]
##################################################################################################
##################### SECTION 7: BY FUEL: CAPACITY REDUCTION --- ANNUAL & CUMULATIVE #############
##################################################################################################

# Function to plot both annual and cumulative avoided emissions on the same axes
def plot7_capacity_reduction_byfuel(ax, df_annual, df_cumulative, region_name, ylabel_left=None, ylabel_right=None, is_global=False):
    # Adjust starting columns for annual and cumulative data
    start_col_annual = 1 if is_global else 8
    start_col_cumulative = 1 if is_global else 8
    #years_columns = years_columns_global if is_global else years_columns_countries

    # Plot Annual avoided emissions on the left y-axis
    for fuel in df_annual['fuel_type'].unique():
        fuel_data = df_annual[df_annual['fuel_type'] == fuel]
        ax.plot(years_columns, fuel_data.iloc[0, start_col_annual:]*(-1), label=f'{fuel}', color=colors.get(fuel, 'grey'))

    ax.set_xticks([str(year) for year in range(2030, 2051, 10)])
    ax.set_title(f'{region_name}', fontsize=12, fontweight='bold', pad=10)
    ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter_0dec))
    if ylabel_left:
        ax.set_ylabel(ylabel_left, fontsize=10)

    # Create a twin y-axis for cumulative avoided emissions
    ax2 = ax.twinx()
    for fuel in df_cumulative['fuel_type'].unique():
        fuel_data = df_cumulative[df_cumulative['fuel_type'] == fuel]
        ax2.plot(years_columns, fuel_data.iloc[0, start_col_cumulative:]*(-1), label=f'Cumulative: {fuel}', color=colors.get(fuel, 'grey'), linestyle='--')

    ax2.yaxis.set_major_formatter(FuncFormatter(thousands_formatter_0dec))
    if ylabel_right:
        ax2.set_ylabel(ylabel_right, fontsize=10)

    return ax, ax2

# -------------------------
# First Graph: Global, Developed, Developing
fig, axes = plt.subplots(1, 3, figsize=(12, 5))

# Plot for Global
plot7_capacity_reduction_byfuel(axes[0], df_byfuel_avoided_annual_global, df_byfuel_avoided_cumulative_global,
                        'Global', ylabel_left='Annual (GW)', is_global=True)

# Plot for Developed Countries
plot7_capacity_reduction_byfuel(axes[1], df_byfuel_avoided_annual_dopunfccc, df_byfuel_avoided_cumulative_dopunfccc,
                        'Developed Countries', is_global=True)

# Plot for Developing Countries
plot7_capacity_reduction_byfuel(axes[2], df_byfuel_avoided_annual_devunfccc, df_byfuel_avoided_cumulative_devunfccc,
                        'Developing Countries', ylabel_right='Cumulative (GW)', is_global=True)

# Main title
fig.suptitle('Fossil Fuel Capacity Reduction in Power Sector:\n Current Policies vs Carbon Budget Consistent Net Zero', fontsize=16, fontweight='bold', y=0.98)

# Global legend for first graph
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', ncol=3, bbox_to_anchor=(0.5, -0.1), fontsize=10)

# Add a second legend for line styles
solid_line = Line2D([0], [0], color='black', lw=2, linestyle='-')
dashed_line = Line2D([0], [0], color='black', lw=2, linestyle='--')
fig.legend([solid_line, dashed_line], ['Annual Capacity Reduction (Left axis)', 'Cumulative Capacity Reduction (Right axes)'], 
           loc='upper center', ncol=2, bbox_to_anchor=(0.5, -0.1), fontsize=10)

plt.subplots_adjust(top=0.80, bottom=0.05, hspace=0.4, wspace=0.6)
plt.show()


# -------------------------
# Second Graph: 8 Countries
fig = plt.figure(figsize=(12, 6))  # Adjusted figure size for grid layout
gs = fig.add_gridspec(2, 4, height_ratios=[1, 1], width_ratios=[1, 1, 1, 1])

# Plot for each country
plot7_capacity_reduction_byfuel(fig.add_subplot(gs[0, 0]), df_byfuel_avoided_annual_ind, df_byfuel_avoided_cumulative_ind,
                        'India', ylabel_left='Annual (GW)')

plot7_capacity_reduction_byfuel(fig.add_subplot(gs[0, 1]), df_byfuel_avoided_annual_idn, df_byfuel_avoided_cumulative_idn,
                        'Indonesia')

plot7_capacity_reduction_byfuel(fig.add_subplot(gs[0, 2]), df_byfuel_avoided_annual_zaf, df_byfuel_avoided_cumulative_zaf,
                        'South Africa')

plot7_capacity_reduction_byfuel(fig.add_subplot(gs[0, 3]), df_byfuel_avoided_annual_mex, df_byfuel_avoided_cumulative_mex,
                        'Mexico', ylabel_right='Cumulative (GW)')

plot7_capacity_reduction_byfuel(fig.add_subplot(gs[1, 0]), df_byfuel_avoided_annual_vnm, df_byfuel_avoided_cumulative_vnm,
                        'Viet Nam', ylabel_left='Annual (GW)')

plot7_capacity_reduction_byfuel(fig.add_subplot(gs[1, 1]), df_byfuel_avoided_annual_irn, df_byfuel_avoided_cumulative_irn,
                        'Iran')

plot7_capacity_reduction_byfuel(fig.add_subplot(gs[1, 2]), df_byfuel_avoided_annual_tha, df_byfuel_avoided_cumulative_tha,
                        'Thailand')

plot7_capacity_reduction_byfuel(fig.add_subplot(gs[1, 3]), df_byfuel_avoided_annual_egy, df_byfuel_avoided_cumulative_egy,
                        'Egypt', ylabel_right='Cumulative (GW)')

# Main title for the second graph
fig.suptitle('Fossil Fuel Capacity Reduction in Power Sector:\n Current Policies vs Carbon Budget Consistent Net Zero', fontsize=16, fontweight='bold', y=0.98)

# Global legend for second graph
handles, labels = fig.get_axes()[0].get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', ncol=3, bbox_to_anchor=(0.5, -0.1), fontsize=10)

# Add a second legend for line styles
solid_line = Line2D([0], [0], color='black', lw=2, linestyle='-')
dashed_line = Line2D([0], [0], color='black', lw=2, linestyle='--')
fig.legend([solid_line, dashed_line], ['Annual Capacity Reduction (Left axis)', 'Cumulative Capacity Reduction (Right axes)'], 
           loc='upper center', ncol=2, bbox_to_anchor=(0.5, -0.1), fontsize=10)

plt.subplots_adjust(top=0.80, bottom=0.05, hspace=0.4, wspace=0.6)
plt.show()


