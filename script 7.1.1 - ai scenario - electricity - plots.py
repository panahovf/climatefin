# In[1]:
# Date: Nov 8, 2024
# Project: Plot AI scenarios - electricity generation
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
# LOAD SCRIPT 7.1 DATA



# In[]:
# Get required dataframes for plots

# Placeholder data
# Calculate the yearly totals for each DataFrame
def calculate_totals(df):
    return df[years_2024].sum()


# Sum across each year to get the total electricity for each dataset
totals_cpfa = calculate_totals(df_electricity_cpfa_global)
totals_b = calculate_totals(df_electricity_cpfaai_b_global)
totals_h = calculate_totals(df_electricity_cpfaai_h_global)
totals_l = calculate_totals(df_electricity_cpfaai_l_global)


# Create a DataFrame that contains all these totals
df_totals = pd.DataFrame({
    'Current Policies': totals_cpfa,
    'AI scenario: Base case': totals_b,
    'AI scenario: High case': totals_h,
    'AI scenario: Low case': totals_l,

})








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


# colors
colors = {
    'Current Policies': '#2E2E2E',  # Dark Gray/Black for Coal
    'AI scenario: Base case': '#4169E1',  # Brown for Oil
    'AI scenario: High case': '#FF8C00',  # Light Blue for Natural Gas
    'AI scenario: Low case': '#32CD32',  # Royal Blue for Current Policies
}   





###################################################################################################
##################### SECTION 1: ANNUAL GENERATION ################################################
###################################################################################################

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

ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter_coma))

# Adding labels and title
plt.xlabel('Year', fontsize=15)
plt.ylabel('TWh', fontsize=15)
plt.title('Total Electricity Production by Scenario', fontsize=20, pad=40)
plt.text(0.5, 1.01, 'Power generation from current power plants in operation are projected \n using growth rates from NGFS GCAM6 model', transform=ax.transAxes, ha='center', fontsize=12)

# legend
plt.legend(loc='best', fontsize=12)

# Show the plot
# plt.grid(True)
# #plt.tight_layout()
plt.show()






