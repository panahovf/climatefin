# In[1]:
# Date: Nov 8, 2024
# Project: Plot AI scenarios - emissions
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
from matplotlib.lines import Line2D # Modify the legend to show AI and CP in separate columns








# In[3]:
# directory & load data

directory = r'C:\Users\panah\OneDrive\Desktop\Work\2 - RA - Climate fin'
os.chdir(directory)
del directory


# --------------
# LOAD SCRIPT 7.2 DATA



# In[]:
# Get required dataframes for plots

# --------------
# THIS GIVES ANNUAL EMISSONS FOR EACH SCENARIO
# Calculate the yearly totals for each DataFrame
def calculate_totals(df):
    return df[years_2024].sum()


# Sum across each year to get the total electricity for each dataset
totals_cpfa = df_cp_emissions[years_2024].sum()
totals_b = df_emissions_cpfaai_b[years_2024].sum()
totals_h = df_emissions_cpfaai_h[years_2024].sum()
totals_l = df_emissions_cpfaai_l[years_2024].sum()

# Create a DataFrame that contains all these totals
df_totals = pd.DataFrame({
    'Current Policies': totals_cpfa,
    'AI scenario: Base case': totals_b,
    'AI scenario: High case': totals_h,
    'AI scenario: Low case': totals_l,

})

# Sum across each year to get the total electricity for each dataset - cumulative
totals_cpfa_cumulative = totals_cpfa.cumsum(axis=0)
totals_b_cumulative = totals_b.cumsum(axis=0)
totals_h_cumulative = totals_h.cumsum(axis=0)
totals_l_cumulative = totals_l.cumsum(axis=0)

# Create a DataFrame that contains all these totals
df_totals_cumulative = pd.DataFrame({
    'Current Policies': totals_cpfa_cumulative,
    'AI scenario: Base case': totals_b_cumulative,
    'AI scenario: High case': totals_h_cumulative,
    'AI scenario: Low case': totals_l_cumulative,

})





# --------------
# THIS GIVES ANNUAL & CUMULATIVE EMISSONS FOR EACH SCENARIO BY FUEL TYPE

# Sum across each year to get the total electricity for each dataset
totals_cpfa_byfuel = df_cp_emissions.groupby(['Variable'])[years_2024].sum()
totals_b_byfuel = df_emissions_cpfaai_b.groupby(['Variable'])[years_2024].sum()
totals_h_byfuel = df_emissions_cpfaai_h.groupby(['Variable'])[years_2024].sum()
totals_l_byfuel = df_emissions_cpfaai_l.groupby(['Variable'])[years_2024].sum()


# Calculate cumulative totals for each scenario
totals_cpfa_byfuel_cumulative = totals_cpfa_byfuel.cumsum(axis=1)
totals_b_byfuel_cumulative = totals_b_byfuel.cumsum(axis=1)
totals_h_byfuel_cumulative = totals_h_byfuel.cumsum(axis=1)
totals_l_byfuel_cumulative = totals_l_byfuel.cumsum(axis=1)








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


# Formatter function to convert values to thousands with commas
def thousands_formatter_coma(x, pos):
    return f'{x:,.0f}'


# Formatter function to convert values to thousands
def thousands_formatter(x, pos):
    return f'{int(x/1000)}'    # the values are in Mt, but diving the axis by 1000 to show in Gt


# colors
colors = {
    'Current Policies': '#2E2E2E',  # Dark Gray/Black for Coal
    'AI scenario: Base case': '#4169E1',  # Brown for Oil
    'AI scenario: High case': '#FF8C00',  # Light Blue for Natural Gas
    'AI scenario: Low case': '#32CD32',  # Royal Blue for Current Policies
}   


# colors
power_colors = {
    'Coal': '#2E2E2E',  # Dark Gray/Black for Coal
    'Oil': '#A52A2A',  # Brown for Oil
    'Gas': '#87CEEB',  # Light Blue for Natural Gas
}

power_colors2 = {
    'Coal': '#1A1A1A',  # Dark Gray/Black for Coal
    'Oil': '#5C1A1A',  # Brown for Oil
    'Gas': '#104E8B',  # Light Blue for Natural Gas
} 







##################################################################################################
##################### SECTION 1: ANNUAL EMISSIONS ################################################
##################################################################################################

# Font and sizes
plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 10,
    'legend.fontsize': 8,
})

# Plotting the totals for each scenario
plt.figure(figsize=(12, 8))

for column in df_totals.columns:
    if column == 'Current Policies':
        plt.plot(df_totals.index, df_totals[column], label=column, color=colors[column], linewidth=2, linestyle='--')
    else:
        plt.plot(df_totals.index, df_totals[column], label=column, color=colors[column], linewidth=2)

# Customize the x-axis to show every year
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Set y-axis formatter to display values with commas
ax = plt.gca()
ax.tick_params(axis='x', which='both', top=False)  # Disable ticks on top of the plot frame

ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Adding labels and title
plt.xlabel('Year', fontsize=15)
plt.ylabel('GtCO2eq', fontsize=15)
plt.title('Annual Emissions in Power Sector by Scenario', fontsize=20, pad=40)
plt.text(0.5, 1.01, 'Emissions from current power plants in operation are projected \n using growth rates from NGFS GCAM6 model', transform=ax.transAxes, ha='center', fontsize=12)

# legend
plt.legend(loc='best', fontsize=12)

# Show the plot
# plt.grid(True)
# #plt.tight_layout()
plt.show()




##################################################################################################
##################### SECTION 2: CUMULATIVE EMISSIONS ############################################
##################################################################################################

# Font and sizes
plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 10,
    'legend.fontsize': 8,
})

# Plotting the totals for each scenario
plt.figure(figsize=(12, 8))

for column in df_totals_cumulative.columns:
    if column == 'Current Policies':
        plt.plot(df_totals_cumulative.index, df_totals_cumulative[column], label=column, color=colors[column], linewidth=2, linestyle='--')
    else:
        plt.plot(df_totals_cumulative.index, df_totals_cumulative[column], label=column, color=colors[column], linewidth=2)

# Customize the x-axis to show every year
plt.xticks([str(year) for year in range(2025, 2051, 5)])

# Set y-axis formatter to display values with commas
ax = plt.gca()
ax.tick_params(axis='x', which='both', top=False)  # Disable ticks on top of the plot frame

ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Adding labels and title
plt.xlabel('Year', fontsize=15)
plt.ylabel('GtCO2eq', fontsize=15)
plt.title('Cumulative Emissions in Power Sector by Scenario', fontsize=20, pad=40)
plt.text(0.5, 1.01, 'Emissions from current power plants in operation are projected \n using growth rates from NGFS GCAM6 model', transform=ax.transAxes, ha='center', fontsize=12)

# legend
plt.legend(loc='best', fontsize=12)

# Show the plot
# plt.grid(True)
# #plt.tight_layout()
plt.show()



##################################################################################################
##################### SECTION 2: EMISSIONS BY FUEL TYPE --- ANNUAL ###############################
##################################################################################################

# Font and sizes
plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 10,
    'legend.fontsize': 8,
})

# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the stacked areas for components of df_extraction_annual_currentpolicy
bottom = pd.Series(0, index=years_2024)
for fuel in totals_b_byfuel.index:
    simplified_label = fuel.split('|')[-1]  # Extracting the last part of the string, which is the fuel name
    ax.fill_between(years_2024, bottom, bottom + totals_b_byfuel.loc[fuel],
                    label=simplified_label, color = power_colors[simplified_label], alpha = 0.7)
    bottom += totals_b_byfuel.loc[fuel]

# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])


# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.tick_params(axis='x', which='both', top=False)  # Disable x-axis ticks at the top of the plot

ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

# Adding labels and legend
plt.xlabel('Year', fontsize=15)
plt.ylabel('GtCO2eq', fontsize=15)
plt.title('Power Sector Emissions by Fossil Fuels: AI base case scenario', fontsize=20, pad=40)
plt.text(0.5, 1.01, 'Emissions from current power plants in operation are projected \n using growth rates from NGFS GCAM6 model', transform=ax.transAxes, ha='center', fontsize=12)
ax.legend(loc='upper left', fontsize = 12)

plt.show()







# # Font and sizes
# plt.rcParams.update({
#     'font.family': 'DejaVu Sans',
#     'font.size': 10,
#     'legend.fontsize': 8,
# })

# # Layout: 2 rows, 2 columns grid for the 4 scenarios
# fig, axs = plt.subplots(2, 2, figsize=(16, 12))
# plt.subplots_adjust(hspace=0.4, wspace=0.3)


# # define plot function
# def plot_scenario(ax, df_scenario):
#     # Setting up the y-axis formatting
#     ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))
    
#     # Start with zero at the bottom of each stack
#     bottom = pd.Series(0, index=years_2024)
    
#     # Stack each fuel in the scenario
#     for fuel in df_scenario.index:
#         simplified_label = fuel.split('|')[-1]  # Extract the fuel name
#         ax.fill_between(
#             years_2024, bottom, bottom + df_scenario.loc[fuel],
#             label=simplified_label, color=power_colors[simplified_label])
#         bottom += df_scenario.loc[fuel]
    
#     # Set x-axis ticks and labels
#     ax.set_xticks([str(year) for year in range(2025, 2051, 5)])
#     ax.tick_params(axis='x', which='both', top=False)  # Disable x-axis ticks at the top of the plot
    
#     # Labels, legend, and title
#     ax.set_xlabel('Year', fontsize=15)
#     ax.set_ylabel('GtCO2', fontsize=15)
#     ax.legend(loc='upper left', fontsize=12)
#     ax.set_title('Total Emissions by Fuel', fontsize=14, fontweight='bold', pad=10)


# # Plotting each scenario in the respective subplot
# plot_scenario(axs[0, 0], totals_cpfa_byfuel)
# plot_scenario(axs[0, 1], totals_b_byfuel)
# plot_scenario(axs[1, 0], totals_h_byfuel)
# plot_scenario(axs[1, 1], totals_l_byfuel)

# # Main title
# fig.suptitle('Power Sector Emissions by Fuel for Each Scenario', fontsize=18, fontweight='bold', y=0.98)

# # Show the plot
# plt.show()










##################################################################################################
##################### SECTION 3: EMISSIONS BY FUEL TYPE: AI vs CP --- ANNUAL #####################
##################################################################################################


# fuel list
fuels = ['Secondary Energy|Electricity|Coal', 'Secondary Energy|Electricity|Gas',
       'Secondary Energy|Electricity|Oil']


# Font and sizes
plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 10,
    'legend.fontsize': 8,
})

# Plotting
fig, ax = plt.subplots(figsize=(12, 8))


# --------------
#Pplot AI base case as stacked area
area_bottom = pd.Series(0, index=totals_b_byfuel.columns)

for fuel in fuels:
    simplified_label = fuel.split('|')[-1]  # Extracting the last part of the string, which is the fuel name
    
    # Plot areas for AI Base Case
    ax.fill_between(totals_h_byfuel.columns, area_bottom, area_bottom + totals_h_byfuel.loc[fuel],
                    label=simplified_label, color=power_colors[simplified_label], alpha=0.7)
    area_bottom += totals_h_byfuel.loc[fuel]



# --------------
# Plot lines for CP scenario, ensuring that each line is stacked on top of the respective area: NG Line starts on top of Coal Area
# this way we can observe differences by fuel type
line_bottom = pd.Series(0, index=totals_b_byfuel.columns)

for fuel in fuels:
    simplified_label = fuel.split('|')[-1]
    # Plot lines for CP scenario on top of the respective stacked areas
    ax.plot(totals_cpfa_byfuel.columns, line_bottom + totals_cpfa_byfuel.loc[fuel],
            label=simplified_label, color=power_colors2[simplified_label], linewidth=2, linestyle='--')
    line_bottom += totals_h_byfuel.loc[fuel]


# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])


# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.tick_params(axis='x', which='both', top=False)  # Disable x-axis ticks at the top of the plot
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x / 1000)}'))


# Adding labels and legend
plt.xlabel('Year', fontsize=15)
plt.ylabel('GtCO2eq', fontsize=15)
plt.title('Power Sector Emissions by Fossil Fuels', fontsize=20, pad=40)
plt.text(0.5, 1.01, 'Emissions from current power plants in operation are projected \n using growth rates from NGFS GCAM6 model', transform=ax.transAxes, ha='center', fontsize=12)


# Create a combined legend with AI and CP elements separately
ai_legend_elements = [Line2D([0], [0], color=power_colors[fuel.split('|')[-1]], lw=4, alpha=0.7, label=f'{fuel.split("|")[-1]}') for fuel in fuels]
cp_legend_elements = [Line2D([0], [0], color=power_colors[fuel.split('|')[-1]], lw=2, linestyle='--', label=f'{fuel.split("|")[-1]}') for fuel in fuels]

# Display both legends using the ax object
first_legend = ax.legend(handles=ai_legend_elements, loc='upper left', title='AI High Case', fontsize=10, title_fontsize=12, bbox_to_anchor=(0, 1))
ax.add_artist(first_legend)  # Add the first legend explicitly
ax.legend(handles=cp_legend_elements, loc='upper left', title='Current Policies', fontsize=10, title_fontsize=12, bbox_to_anchor=(0.15, 1))


plt.show()










##################################################################################################
##################### SECTION 4: EMISSIONS BY FUEL TYPE: AI vs CP --- CUMULATIVE #################
##################################################################################################


# fuel list
fuels = ['Secondary Energy|Electricity|Coal', 'Secondary Energy|Electricity|Gas',
       'Secondary Energy|Electricity|Oil']


# Font and sizes
plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 10,
    'legend.fontsize': 8,
})

# Plotting
fig, ax = plt.subplots(figsize=(12, 8))


# --------------
#Pplot AI base case as stacked area
area_bottom = pd.Series(0, index=totals_b_byfuel.columns)

for fuel in fuels:
    simplified_label = fuel.split('|')[-1]  # Extracting the last part of the string, which is the fuel name
    
    # Plot areas for AI Base Case
    ax.fill_between(totals_h_byfuel_cumulative.columns, area_bottom, area_bottom + totals_h_byfuel_cumulative.loc[fuel],
                    label=simplified_label, color=power_colors[simplified_label], alpha=0.7)
    area_bottom += totals_h_byfuel_cumulative.loc[fuel]



# --------------
# Plot lines for CP scenario, ensuring that each line is stacked on top of the respective area: NG Line starts on top of Coal Area
# this way we can observe differences by fuel type
line_bottom = pd.Series(0, index=totals_b_byfuel.columns)

for fuel in fuels:
    simplified_label = fuel.split('|')[-1]
    # Plot lines for CP scenario on top of the respective stacked areas
    ax.plot(totals_cpfa_byfuel_cumulative.columns, line_bottom + totals_cpfa_byfuel_cumulative.loc[fuel],
            label=simplified_label, color=power_colors2[simplified_label], linewidth=2, linestyle='--')
    line_bottom += totals_h_byfuel_cumulative.loc[fuel]


# Customize the x-axis to show ticks every 5 years
plt.xticks([str(year) for year in range(2025, 2051, 5)])


# Set y-axis formatter to display values in thousands
ax = plt.gca()
ax.tick_params(axis='x', which='both', top=False)  # Disable x-axis ticks at the top of the plot
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x / 1000)}'))


# Adding labels and legend
plt.xlabel('Year', fontsize=15)
plt.ylabel('GtCO2eq', fontsize=15)
plt.title('Cumulative Power Sector Emissions by Fossil Fuels', fontsize=20, pad=40)
plt.text(0.5, 1.01, 'Emissions from current power plants in operation are projected \n using growth rates from NGFS GCAM6 model', transform=ax.transAxes, ha='center', fontsize=12)


# Create a combined legend with AI and CP elements separately
ai_legend_elements = [Line2D([0], [0], color=power_colors[fuel.split('|')[-1]], lw=4, alpha=0.7, label=f'{fuel.split("|")[-1]}') for fuel in fuels]
cp_legend_elements = [Line2D([0], [0], color=power_colors[fuel.split('|')[-1]], lw=2, linestyle='--', label=f'{fuel.split("|")[-1]}') for fuel in fuels]

# Display both legends using the ax object
first_legend = ax.legend(handles=ai_legend_elements, loc='upper left', title='AI High Case', fontsize=10, title_fontsize=12, bbox_to_anchor=(0, 1))
ax.add_artist(first_legend)  # Add the first legend explicitly
ax.legend(handles=cp_legend_elements, loc='upper left', title='Current Policies', fontsize=10, title_fontsize=12, bbox_to_anchor=(0.15, 1))


plt.show()











