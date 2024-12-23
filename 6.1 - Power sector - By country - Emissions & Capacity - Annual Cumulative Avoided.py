# In[1]:
# Date: Sep 15, 2024
# Project: Emissions & capacity by scenario (CP, NGFS NZ, Modified NZ 1.5C 50%) for Global, India, US, Vietnam, Turkeye, Indonesia, Germany
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










# In[3]:
# directory & load data

directory = r'C:\Users\panah\OneDrive\Desktop\Work\2 - RA - Climate fin'
os.chdir(directory)
del directory


# --------------
# LOAD EMISSIONS DATA - POWER
df_emissions_currentpolicy = pd.read_excel('2 - output/script 4.2/9.1 - Current policy - Secondary - annual.xlsx')
df_emissions_netzero = pd.read_excel('2 - output/script 4.2/9.2 - Net zero - Secondary - annual.xlsx')
df_emissions_nz1550v2 = pd.read_excel('2 - output/script 4.2/6.1 - NZ-15-50 - v2 - Secondary - annual.xlsx')


# --------------
# LOAD POWER DATA
df_power_coal = pd.read_excel('2 - output/script 1/4 - power - coal.xlsx')
df_power_gas = pd.read_excel('2 - output/script 1/5 - power - gas.xlsx')
df_power_oil = pd.read_excel('2 - output/script 1/6 - power - oil.xlsx')





# In[4]: FILTER FOR COUNTIES
############################

# Get list of EMDE countries

# load datasets
temp_directory = r'C:\Users\panah\OneDrive\Desktop\Work\2 - RA - Climate fin\2 - output\script a - country codes'
df_country_developing = pd.read_excel(temp_directory + r'\2 - developing.xlsx')
df_country_emerging = pd.read_excel(temp_directory + r'\3 - emerging.xlsx')

df_country_unfccc = pd.read_excel('1 - input/Country Datasets/UNFCCC classification.xlsx')
df_country_unfccc_dev = df_country_unfccc[df_country_unfccc['classification'] == "Developing"]

# get and combine lists
v_countrycodes_developing = list(df_country_developing['alpha-3'].unique())
v_countrycodes_emerging = list(df_country_emerging['alpha-3'].unique())
v_countrycodes_emde = v_countrycodes_developing + v_countrycodes_emerging

v_countrycodes_unfccc_dev = list(df_country_unfccc_dev['iso_3'].unique())

# delete
del temp_directory, df_country_developing, df_country_emerging, df_country_unfccc, df_country_unfccc_dev, v_countrycodes_developing, v_countrycodes_emerging





# In[4]: FILTER FOR COUNTIES
############################


# set years columns
years_columns = [str(year) for year in range(2024, 2051)]


# --------------
# Case 1: Current policy
df_emissions_currentpolicy_usa = df_emissions_currentpolicy[df_emissions_currentpolicy["Region"] == "USA"]
df_emissions_currentpolicy_tur = df_emissions_currentpolicy[df_emissions_currentpolicy["Region"] == "TUR"]
df_emissions_currentpolicy_ind = df_emissions_currentpolicy[df_emissions_currentpolicy["Region"] == "IND"]
df_emissions_currentpolicy_idn = df_emissions_currentpolicy[df_emissions_currentpolicy["Region"] == "IDN"]
df_emissions_currentpolicy_vnm = df_emissions_currentpolicy[df_emissions_currentpolicy["Region"] == "VNM"]
df_emissions_currentpolicy_deu = df_emissions_currentpolicy[df_emissions_currentpolicy["Region"] == "DEU"]
df_emissions_currentpolicy_pol = df_emissions_currentpolicy[df_emissions_currentpolicy["Region"] == "POL"]
df_emissions_currentpolicy_kaz = df_emissions_currentpolicy[df_emissions_currentpolicy["Region"] == "KAZ"]
df_emissions_currentpolicy_zaf = df_emissions_currentpolicy[df_emissions_currentpolicy["Region"] == "ZAF"]
df_emissions_currentpolicy_bgd = df_emissions_currentpolicy[df_emissions_currentpolicy["Region"] == "BGD"]
df_emissions_currentpolicy_emde = df_emissions_currentpolicy[df_emissions_currentpolicy["Region"].isin(v_countrycodes_emde)].groupby('fuel_type')[years_columns].sum().reset_index()
df_emissions_currentpolicy_devunfccc = df_emissions_currentpolicy[df_emissions_currentpolicy["Region"].isin(v_countrycodes_unfccc_dev)].groupby('fuel_type')[years_columns].sum().reset_index()
df_emissions_currentpolicy_global = df_emissions_currentpolicy.groupby('fuel_type')[years_columns].sum().reset_index()


# --------------
# Case 2: Netzero
df_emissions_netzero_usa = df_emissions_netzero[df_emissions_netzero["Region"] == "USA"]
df_emissions_netzero_tur = df_emissions_netzero[df_emissions_netzero["Region"] == "TUR"]
df_emissions_netzero_ind = df_emissions_netzero[df_emissions_netzero["Region"] == "IND"]
df_emissions_netzero_idn = df_emissions_netzero[df_emissions_netzero["Region"] == "IDN"]
df_emissions_netzero_vnm = df_emissions_netzero[df_emissions_netzero["Region"] == "VNM"]
df_emissions_netzero_deu = df_emissions_netzero[df_emissions_netzero["Region"] == "DEU"]
df_emissions_netzero_pol = df_emissions_netzero[df_emissions_netzero["Region"] == "POL"]
df_emissions_netzero_kaz = df_emissions_netzero[df_emissions_netzero["Region"] == "KAZ"]
df_emissions_netzero_zaf = df_emissions_netzero[df_emissions_netzero["Region"] == "ZAF"]
df_emissions_netzero_bgd = df_emissions_netzero[df_emissions_netzero["Region"] == "BGD"]
df_emissions_netzero_emde = df_emissions_netzero[df_emissions_netzero["Region"].isin(v_countrycodes_emde)].groupby('fuel_type')[years_columns].sum().reset_index()
df_emissions_netzero_devunfccc = df_emissions_netzero[df_emissions_netzero["Region"].isin(v_countrycodes_unfccc_dev)].groupby('fuel_type')[years_columns].sum().reset_index()
df_emissions_netzero_global = df_emissions_netzero.groupby('fuel_type')[years_columns].sum().reset_index()



# --------------
# Case 3: Netzero 1.5C 50% adjusted
df_emissions_nz1550v2_usa = df_emissions_nz1550v2[df_emissions_nz1550v2["Region"] == "USA"]
df_emissions_nz1550v2_tur = df_emissions_nz1550v2[df_emissions_nz1550v2["Region"] == "TUR"]
df_emissions_nz1550v2_ind = df_emissions_nz1550v2[df_emissions_nz1550v2["Region"] == "IND"]
df_emissions_nz1550v2_idn = df_emissions_nz1550v2[df_emissions_nz1550v2["Region"] == "IDN"]
df_emissions_nz1550v2_vnm = df_emissions_nz1550v2[df_emissions_nz1550v2["Region"] == "VNM"]
df_emissions_nz1550v2_deu = df_emissions_nz1550v2[df_emissions_nz1550v2["Region"] == "DEU"]
df_emissions_nz1550v2_pol = df_emissions_nz1550v2[df_emissions_nz1550v2["Region"] == "POL"]
df_emissions_nz1550v2_kaz = df_emissions_nz1550v2[df_emissions_nz1550v2["Region"] == "KAZ"]
df_emissions_nz1550v2_zaf = df_emissions_nz1550v2[df_emissions_nz1550v2["Region"] == "ZAF"]
df_emissions_nz1550v2_bgd = df_emissions_nz1550v2[df_emissions_nz1550v2["Region"] == "BGD"]
df_emissions_nz1550v2_emde = df_emissions_nz1550v2[df_emissions_nz1550v2["Region"].isin(v_countrycodes_emde)].groupby('fuel_type')[years_columns].sum().reset_index()
df_emissions_nz1550v2_devunfccc = df_emissions_nz1550v2[df_emissions_nz1550v2["Region"].isin(v_countrycodes_unfccc_dev)].groupby('fuel_type')[years_columns].sum().reset_index()
df_emissions_nz1550v2_global = df_emissions_nz1550v2.groupby('fuel_type')[years_columns].sum().reset_index()










# In[4]: GET GHG INTENTITY FACTORS
##################################

# --------------
# get emissions intensity by country
# this function creates a weighted average by countries (emissions by activity)
def weighted_avg_intensity_coal(group):
    return (group['emissions_factor_perMWh'] * group['activity']).sum() / group['activity'].sum()

def weighted_avg_intensity_gas_oil(group):
    return (group['emission_factor'] * group['activity']).sum() / group['activity'].sum()



# apply the function --- this also directs them to dictionaries
df_power_coal_intensity = df_power_coal.groupby('countryiso3').apply(weighted_avg_intensity_coal).reset_index().set_index('countryiso3')[0].to_dict()
df_power_gas_intensity = df_power_gas.groupby('countryiso3').apply(weighted_avg_intensity_gas_oil).reset_index().set_index('countryiso3')[0].to_dict()
df_power_oil_intensity = df_power_oil.groupby('countryiso3').apply(weighted_avg_intensity_gas_oil).reset_index().set_index('countryiso3')[0].to_dict()










# In[4]: GET GHG UTILIZATION FACTORS
####################################

# --------------
# get capacity factors by country (utilization factor)
# this function creates a weighted average by countries (emissions by activity)
def weighted_avg_utilization_coal(group):
    return (group['capacity_factor'] * group['activity']).sum() / group['activity'].sum()


# apply the function
df_power_coal_utilization = df_power_coal.groupby('countryiso3').apply(weighted_avg_utilization_coal).reset_index().set_index('countryiso3')[0].to_dict()
df_power_gas_utilization = df_power_gas.groupby('countryiso3').apply(weighted_avg_utilization_coal).reset_index().set_index('countryiso3')[0].to_dict()
df_power_oil_utilization = df_power_oil.groupby('countryiso3').apply(weighted_avg_utilization_coal).reset_index().set_index('countryiso3')[0].to_dict()










# In[4]: CONVERT EMISSIONS TO GENERATION
########################################

# Divide emissions by the intensity factors to get MWh
# GHG / (GHG/MWh) = MWh
# For used capacity: divide total generation by (24x365)
# For total capacity: divide used capacity by the capacity factor (or utilization factor)


# create dataframes
df_totalcapacity_currentpolicy_deu = df_emissions_currentpolicy_deu.copy()
df_totalcapacity_currentpolicy_idn = df_emissions_currentpolicy_idn.copy()
df_totalcapacity_currentpolicy_ind = df_emissions_currentpolicy_ind.copy()
df_totalcapacity_currentpolicy_tur = df_emissions_currentpolicy_tur.copy()
df_totalcapacity_currentpolicy_usa = df_emissions_currentpolicy_usa.copy()
df_totalcapacity_currentpolicy_vnm = df_emissions_currentpolicy_vnm.copy()
df_totalcapacity_currentpolicy_pol = df_emissions_currentpolicy_pol.copy()
df_totalcapacity_currentpolicy_kaz = df_emissions_currentpolicy_kaz.copy()
df_totalcapacity_currentpolicy_zaf = df_emissions_currentpolicy_zaf.copy()
df_totalcapacity_currentpolicy_bgd = df_emissions_currentpolicy_bgd.copy()
df_totalcapacity_currentpolicy_emde = df_emissions_currentpolicy.copy()[df_emissions_currentpolicy['Region'].isin(v_countrycodes_emde)]
df_totalcapacity_currentpolicy_devunfccc = df_emissions_currentpolicy.copy()[df_emissions_currentpolicy['Region'].isin(v_countrycodes_unfccc_dev)]
df_totalcapacity_currentpolicy_global = df_emissions_currentpolicy.copy()


df_totalcapacity_netzero_deu = df_emissions_netzero_deu.copy()
df_totalcapacity_netzero_idn = df_emissions_netzero_idn.copy()
df_totalcapacity_netzero_ind = df_emissions_netzero_ind.copy()
df_totalcapacity_netzero_tur = df_emissions_netzero_tur.copy()
df_totalcapacity_netzero_usa = df_emissions_netzero_usa.copy()
df_totalcapacity_netzero_vnm = df_emissions_netzero_vnm.copy()
df_totalcapacity_netzero_pol = df_emissions_netzero_pol.copy()
df_totalcapacity_netzero_kaz = df_emissions_netzero_kaz.copy()
df_totalcapacity_netzero_zaf = df_emissions_netzero_zaf.copy()
df_totalcapacity_netzero_bgd = df_emissions_netzero_bgd.copy()
df_totalcapacity_netzero_emde = df_emissions_netzero.copy()[df_emissions_netzero['Region'].isin(v_countrycodes_emde)]
df_totalcapacity_netzero_devunfccc = df_emissions_netzero.copy()[df_emissions_netzero['Region'].isin(v_countrycodes_unfccc_dev)]
df_totalcapacity_netzero_global = df_emissions_netzero.copy()


df_totalcapacity_nz1550v2_deu = df_emissions_nz1550v2_deu.copy()
df_totalcapacity_nz1550v2_idn = df_emissions_nz1550v2_idn.copy()
df_totalcapacity_nz1550v2_ind = df_emissions_nz1550v2_ind.copy()
df_totalcapacity_nz1550v2_tur = df_emissions_nz1550v2_tur.copy()
df_totalcapacity_nz1550v2_usa = df_emissions_nz1550v2_usa.copy()
df_totalcapacity_nz1550v2_vnm = df_emissions_nz1550v2_vnm.copy()
df_totalcapacity_nz1550v2_pol = df_emissions_nz1550v2_pol.copy()
df_totalcapacity_nz1550v2_kaz = df_emissions_nz1550v2_kaz.copy()
df_totalcapacity_nz1550v2_zaf = df_emissions_nz1550v2_zaf.copy()
df_totalcapacity_nz1550v2_bgd = df_emissions_nz1550v2_bgd.copy()
df_totalcapacity_nz1550v2_emde = df_emissions_nz1550v2.copy()[df_emissions_nz1550v2['Region'].isin(v_countrycodes_emde)]
df_totalcapacity_nz1550v2_devunfccc = df_emissions_nz1550v2.copy()[df_emissions_nz1550v2['Region'].isin(v_countrycodes_unfccc_dev)]
df_totalcapacity_nz1550v2_global = df_emissions_nz1550v2.copy()





########################################################
#  1. CURRENT POLICY -----------------------------------
########################################################

# --------------
# total capacity
# 1 - coal
df_totalcapacity_currentpolicy_deu.loc[df_totalcapacity_currentpolicy_deu['fuel_type'] == "Coal", years_columns] = ( 
    df_totalcapacity_currentpolicy_deu.loc[df_totalcapacity_currentpolicy_deu['fuel_type'] == "Coal", years_columns]
    .div(df_totalcapacity_currentpolicy_deu['Region'].map(df_power_coal_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_currentpolicy_deu['Region'].map(df_power_coal_utilization), axis=0)
    )

df_totalcapacity_currentpolicy_idn.loc[df_totalcapacity_currentpolicy_idn['fuel_type'] == "Coal", years_columns] = ( 
    df_totalcapacity_currentpolicy_idn.loc[df_totalcapacity_currentpolicy_idn['fuel_type'] == "Coal", years_columns]
    .div(df_totalcapacity_currentpolicy_idn['Region'].map(df_power_coal_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_currentpolicy_idn['Region'].map(df_power_coal_utilization), axis=0)
    )

df_totalcapacity_currentpolicy_ind.loc[df_totalcapacity_currentpolicy_ind['fuel_type'] == "Coal", years_columns] = ( 
    df_totalcapacity_currentpolicy_ind.loc[df_totalcapacity_currentpolicy_ind['fuel_type'] == "Coal", years_columns]
    .div(df_totalcapacity_currentpolicy_ind['Region'].map(df_power_coal_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_currentpolicy_ind['Region'].map(df_power_coal_utilization), axis=0)
    )

df_totalcapacity_currentpolicy_tur.loc[df_totalcapacity_currentpolicy_tur['fuel_type'] == "Coal", years_columns] = ( 
    df_totalcapacity_currentpolicy_tur.loc[df_totalcapacity_currentpolicy_tur['fuel_type'] == "Coal", years_columns]
    .div(df_totalcapacity_currentpolicy_tur['Region'].map(df_power_coal_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_currentpolicy_tur['Region'].map(df_power_coal_utilization), axis=0)
    )

df_totalcapacity_currentpolicy_usa.loc[df_totalcapacity_currentpolicy_usa['fuel_type'] == "Coal", years_columns] = ( 
    df_totalcapacity_currentpolicy_usa.loc[df_totalcapacity_currentpolicy_usa['fuel_type'] == "Coal", years_columns]
    .div(df_totalcapacity_currentpolicy_usa['Region'].map(df_power_coal_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_currentpolicy_usa['Region'].map(df_power_coal_utilization), axis=0)
    )

df_totalcapacity_currentpolicy_vnm.loc[df_totalcapacity_currentpolicy_vnm['fuel_type'] == "Coal", years_columns] = ( 
    df_totalcapacity_currentpolicy_vnm.loc[df_totalcapacity_currentpolicy_vnm['fuel_type'] == "Coal", years_columns]
    .div(df_totalcapacity_currentpolicy_vnm['Region'].map(df_power_coal_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_currentpolicy_vnm['Region'].map(df_power_coal_utilization), axis=0)
    )

df_totalcapacity_currentpolicy_pol.loc[df_totalcapacity_currentpolicy_pol['fuel_type'] == "Coal", years_columns] = ( 
    df_totalcapacity_currentpolicy_pol.loc[df_totalcapacity_currentpolicy_pol['fuel_type'] == "Coal", years_columns]
    .div(df_totalcapacity_currentpolicy_pol['Region'].map(df_power_coal_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_currentpolicy_pol['Region'].map(df_power_coal_utilization), axis=0)
    )

df_totalcapacity_currentpolicy_kaz.loc[df_totalcapacity_currentpolicy_kaz['fuel_type'] == "Coal", years_columns] = ( 
    df_totalcapacity_currentpolicy_kaz.loc[df_totalcapacity_currentpolicy_kaz['fuel_type'] == "Coal", years_columns]
    .div(df_totalcapacity_currentpolicy_kaz['Region'].map(df_power_coal_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_currentpolicy_kaz['Region'].map(df_power_coal_utilization), axis=0)
    )

df_totalcapacity_currentpolicy_zaf.loc[df_totalcapacity_currentpolicy_zaf['fuel_type'] == "Coal", years_columns] = ( 
    df_totalcapacity_currentpolicy_zaf.loc[df_totalcapacity_currentpolicy_zaf['fuel_type'] == "Coal", years_columns]
    .div(df_totalcapacity_currentpolicy_zaf['Region'].map(df_power_coal_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_currentpolicy_zaf['Region'].map(df_power_coal_utilization), axis=0)
    )

df_totalcapacity_currentpolicy_bgd.loc[df_totalcapacity_currentpolicy_bgd['fuel_type'] == "Coal", years_columns] = ( 
    df_totalcapacity_currentpolicy_bgd.loc[df_totalcapacity_currentpolicy_bgd['fuel_type'] == "Coal", years_columns]
    .div(df_totalcapacity_currentpolicy_bgd['Region'].map(df_power_coal_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_currentpolicy_bgd['Region'].map(df_power_coal_utilization), axis=0)
    )

df_totalcapacity_currentpolicy_emde.loc[df_totalcapacity_currentpolicy_emde['fuel_type'] == "Coal", years_columns] = ( 
    df_totalcapacity_currentpolicy_emde.loc[df_totalcapacity_currentpolicy_emde['fuel_type'] == "Coal", years_columns]
    .div(df_totalcapacity_currentpolicy_emde['Region'].map(df_power_coal_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_currentpolicy_emde['Region'].map(df_power_coal_utilization), axis=0)
    )

df_totalcapacity_currentpolicy_devunfccc.loc[df_totalcapacity_currentpolicy_devunfccc['fuel_type'] == "Coal", years_columns] = ( 
    df_totalcapacity_currentpolicy_devunfccc.loc[df_totalcapacity_currentpolicy_devunfccc['fuel_type'] == "Coal", years_columns]
    .div(df_totalcapacity_currentpolicy_devunfccc['Region'].map(df_power_coal_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_currentpolicy_devunfccc['Region'].map(df_power_coal_utilization), axis=0)
    )

df_totalcapacity_currentpolicy_global.loc[df_totalcapacity_currentpolicy_global['fuel_type'] == "Coal", years_columns] = ( 
    df_totalcapacity_currentpolicy_global.loc[df_totalcapacity_currentpolicy_global['fuel_type'] == "Coal", years_columns]
    .div(df_totalcapacity_currentpolicy_global['Region'].map(df_power_coal_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_currentpolicy_global['Region'].map(df_power_coal_utilization), axis=0)
    )



# 2 - gas
df_totalcapacity_currentpolicy_deu.loc[df_totalcapacity_currentpolicy_deu['fuel_type'] == "Gas", years_columns] = ( 
    df_totalcapacity_currentpolicy_deu.loc[df_totalcapacity_currentpolicy_deu['fuel_type'] == "Gas", years_columns]
    .div(df_totalcapacity_currentpolicy_deu['Region'].map(df_power_gas_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_currentpolicy_deu['Region'].map(df_power_gas_utilization), axis=0)
    )

df_totalcapacity_currentpolicy_idn.loc[df_totalcapacity_currentpolicy_idn['fuel_type'] == "Gas", years_columns] = ( 
    df_totalcapacity_currentpolicy_idn.loc[df_totalcapacity_currentpolicy_idn['fuel_type'] == "Gas", years_columns]
    .div(df_totalcapacity_currentpolicy_idn['Region'].map(df_power_gas_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_currentpolicy_idn['Region'].map(df_power_gas_utilization), axis=0)
    )

df_totalcapacity_currentpolicy_ind.loc[df_totalcapacity_currentpolicy_ind['fuel_type'] == "Gas", years_columns] = ( 
    df_totalcapacity_currentpolicy_ind.loc[df_totalcapacity_currentpolicy_ind['fuel_type'] == "Gas", years_columns]
    .div(df_totalcapacity_currentpolicy_ind['Region'].map(df_power_gas_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_currentpolicy_ind['Region'].map(df_power_gas_utilization), axis=0)
    )

df_totalcapacity_currentpolicy_tur.loc[df_totalcapacity_currentpolicy_tur['fuel_type'] == "Gas", years_columns] = ( 
    df_totalcapacity_currentpolicy_tur.loc[df_totalcapacity_currentpolicy_tur['fuel_type'] == "Gas", years_columns]
    .div(df_totalcapacity_currentpolicy_tur['Region'].map(df_power_gas_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_currentpolicy_tur['Region'].map(df_power_gas_utilization), axis=0)
    )

df_totalcapacity_currentpolicy_usa.loc[df_totalcapacity_currentpolicy_usa['fuel_type'] == "Gas", years_columns] = ( 
    df_totalcapacity_currentpolicy_usa.loc[df_totalcapacity_currentpolicy_usa['fuel_type'] == "Gas", years_columns]
    .div(df_totalcapacity_currentpolicy_usa['Region'].map(df_power_gas_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_currentpolicy_usa['Region'].map(df_power_gas_utilization), axis=0)
    )

df_totalcapacity_currentpolicy_vnm.loc[df_totalcapacity_currentpolicy_vnm['fuel_type'] == "Gas", years_columns] = ( 
    df_totalcapacity_currentpolicy_vnm.loc[df_totalcapacity_currentpolicy_vnm['fuel_type'] == "Gas", years_columns]
    .div(df_totalcapacity_currentpolicy_vnm['Region'].map(df_power_gas_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_currentpolicy_vnm['Region'].map(df_power_gas_utilization), axis=0)
    )

df_totalcapacity_currentpolicy_pol.loc[df_totalcapacity_currentpolicy_pol['fuel_type'] == "Gas", years_columns] = ( 
    df_totalcapacity_currentpolicy_pol.loc[df_totalcapacity_currentpolicy_pol['fuel_type'] == "Gas", years_columns]
    .div(df_totalcapacity_currentpolicy_pol['Region'].map(df_power_gas_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_currentpolicy_pol['Region'].map(df_power_gas_utilization), axis=0)
    )

df_totalcapacity_currentpolicy_kaz.loc[df_totalcapacity_currentpolicy_kaz['fuel_type'] == "Gas", years_columns] = ( 
    df_totalcapacity_currentpolicy_kaz.loc[df_totalcapacity_currentpolicy_kaz['fuel_type'] == "Gas", years_columns]
    .div(df_totalcapacity_currentpolicy_kaz['Region'].map(df_power_gas_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_currentpolicy_kaz['Region'].map(df_power_gas_utilization), axis=0)
    )

df_totalcapacity_currentpolicy_zaf.loc[df_totalcapacity_currentpolicy_zaf['fuel_type'] == "Gas", years_columns] = ( 
    df_totalcapacity_currentpolicy_zaf.loc[df_totalcapacity_currentpolicy_zaf['fuel_type'] == "Gas", years_columns]
    .div(df_totalcapacity_currentpolicy_zaf['Region'].map(df_power_gas_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_currentpolicy_zaf['Region'].map(df_power_gas_utilization), axis=0)
    )

df_totalcapacity_currentpolicy_bgd.loc[df_totalcapacity_currentpolicy_bgd['fuel_type'] == "Gas", years_columns] = ( 
    df_totalcapacity_currentpolicy_bgd.loc[df_totalcapacity_currentpolicy_bgd['fuel_type'] == "Gas", years_columns]
    .div(df_totalcapacity_currentpolicy_bgd['Region'].map(df_power_gas_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_currentpolicy_bgd['Region'].map(df_power_gas_utilization), axis=0)
    )

df_totalcapacity_currentpolicy_emde.loc[df_totalcapacity_currentpolicy_emde['fuel_type'] == "Gas", years_columns] = ( 
    df_totalcapacity_currentpolicy_emde.loc[df_totalcapacity_currentpolicy_emde['fuel_type'] == "Gas", years_columns]
    .div(df_totalcapacity_currentpolicy_emde['Region'].map(df_power_gas_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_currentpolicy_emde['Region'].map(df_power_gas_utilization), axis=0)
    )

df_totalcapacity_currentpolicy_devunfccc.loc[df_totalcapacity_currentpolicy_devunfccc['fuel_type'] == "Gas", years_columns] = ( 
    df_totalcapacity_currentpolicy_devunfccc.loc[df_totalcapacity_currentpolicy_devunfccc['fuel_type'] == "Gas", years_columns]
    .div(df_totalcapacity_currentpolicy_devunfccc['Region'].map(df_power_gas_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_currentpolicy_devunfccc['Region'].map(df_power_gas_utilization), axis=0)
    )

df_totalcapacity_currentpolicy_global.loc[df_totalcapacity_currentpolicy_global['fuel_type'] == "Gas", years_columns] = ( 
    df_totalcapacity_currentpolicy_global.loc[df_totalcapacity_currentpolicy_global['fuel_type'] == "Gas", years_columns]
    .div(df_totalcapacity_currentpolicy_global['Region'].map(df_power_gas_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_currentpolicy_global['Region'].map(df_power_gas_utilization), axis=0)
    )


# 3 - oil
df_totalcapacity_currentpolicy_deu.loc[df_totalcapacity_currentpolicy_deu['fuel_type'] == "Oil", years_columns] = ( 
    df_totalcapacity_currentpolicy_deu.loc[df_totalcapacity_currentpolicy_deu['fuel_type'] == "Oil", years_columns]
    .div(df_totalcapacity_currentpolicy_deu['Region'].map(df_power_oil_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_currentpolicy_deu['Region'].map(df_power_oil_utilization), axis=0)
    )

df_totalcapacity_currentpolicy_idn.loc[df_totalcapacity_currentpolicy_idn['fuel_type'] == "Oil", years_columns] = ( 
    df_totalcapacity_currentpolicy_idn.loc[df_totalcapacity_currentpolicy_idn['fuel_type'] == "Oil", years_columns]
    .div(df_totalcapacity_currentpolicy_idn['Region'].map(df_power_oil_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_currentpolicy_idn['Region'].map(df_power_oil_utilization), axis=0)
    )

df_totalcapacity_currentpolicy_ind.loc[df_totalcapacity_currentpolicy_ind['fuel_type'] == "Oil", years_columns] = ( 
    df_totalcapacity_currentpolicy_ind.loc[df_totalcapacity_currentpolicy_ind['fuel_type'] == "Oil", years_columns]
    .div(df_totalcapacity_currentpolicy_ind['Region'].map(df_power_oil_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_currentpolicy_ind['Region'].map(df_power_oil_utilization), axis=0)
    )

df_totalcapacity_currentpolicy_tur.loc[df_totalcapacity_currentpolicy_tur['fuel_type'] == "Oil", years_columns] = ( 
    df_totalcapacity_currentpolicy_tur.loc[df_totalcapacity_currentpolicy_tur['fuel_type'] == "Oil", years_columns]
    .div(df_totalcapacity_currentpolicy_tur['Region'].map(df_power_oil_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_currentpolicy_tur['Region'].map(df_power_oil_utilization), axis=0)
    )

df_totalcapacity_currentpolicy_usa.loc[df_totalcapacity_currentpolicy_usa['fuel_type'] == "Oil", years_columns] = ( 
    df_totalcapacity_currentpolicy_usa.loc[df_totalcapacity_currentpolicy_usa['fuel_type'] == "Oil", years_columns]
    .div(df_totalcapacity_currentpolicy_usa['Region'].map(df_power_oil_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_currentpolicy_usa['Region'].map(df_power_oil_utilization), axis=0)
    )

df_totalcapacity_currentpolicy_vnm.loc[df_totalcapacity_currentpolicy_vnm['fuel_type'] == "Oil", years_columns] = ( 
    df_totalcapacity_currentpolicy_vnm.loc[df_totalcapacity_currentpolicy_vnm['fuel_type'] == "Oil", years_columns]
    .div(df_totalcapacity_currentpolicy_vnm['Region'].map(df_power_oil_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_currentpolicy_vnm['Region'].map(df_power_oil_utilization), axis=0)
    )

df_totalcapacity_currentpolicy_pol.loc[df_totalcapacity_currentpolicy_pol['fuel_type'] == "Oil", years_columns] = ( 
    df_totalcapacity_currentpolicy_pol.loc[df_totalcapacity_currentpolicy_pol['fuel_type'] == "Oil", years_columns]
    .div(df_totalcapacity_currentpolicy_pol['Region'].map(df_power_oil_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_currentpolicy_pol['Region'].map(df_power_oil_utilization), axis=0)
    )

df_totalcapacity_currentpolicy_kaz.loc[df_totalcapacity_currentpolicy_kaz['fuel_type'] == "Oil", years_columns] = ( 
    df_totalcapacity_currentpolicy_kaz.loc[df_totalcapacity_currentpolicy_kaz['fuel_type'] == "Oil", years_columns]
    .div(df_totalcapacity_currentpolicy_kaz['Region'].map(df_power_oil_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_currentpolicy_kaz['Region'].map(df_power_oil_utilization), axis=0)
    )

df_totalcapacity_currentpolicy_zaf.loc[df_totalcapacity_currentpolicy_zaf['fuel_type'] == "Oil", years_columns] = ( 
    df_totalcapacity_currentpolicy_zaf.loc[df_totalcapacity_currentpolicy_zaf['fuel_type'] == "Oil", years_columns]
    .div(df_totalcapacity_currentpolicy_zaf['Region'].map(df_power_oil_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_currentpolicy_zaf['Region'].map(df_power_oil_utilization), axis=0)
    )

df_totalcapacity_currentpolicy_bgd.loc[df_totalcapacity_currentpolicy_bgd['fuel_type'] == "Oil", years_columns] = ( 
    df_totalcapacity_currentpolicy_bgd.loc[df_totalcapacity_currentpolicy_bgd['fuel_type'] == "Oil", years_columns]
    .div(df_totalcapacity_currentpolicy_bgd['Region'].map(df_power_oil_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_currentpolicy_bgd['Region'].map(df_power_oil_utilization), axis=0)
    )

df_totalcapacity_currentpolicy_emde.loc[df_totalcapacity_currentpolicy_emde['fuel_type'] == "Oil", years_columns] = ( 
    df_totalcapacity_currentpolicy_emde.loc[df_totalcapacity_currentpolicy_emde['fuel_type'] == "Oil", years_columns]
    .div(df_totalcapacity_currentpolicy_emde['Region'].map(df_power_oil_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_currentpolicy_emde['Region'].map(df_power_oil_utilization), axis=0)
    )
df_totalcapacity_currentpolicy_emde = df_totalcapacity_currentpolicy_emde.groupby('fuel_type')[years_columns].sum().reset_index()

df_totalcapacity_currentpolicy_devunfccc.loc[df_totalcapacity_currentpolicy_devunfccc['fuel_type'] == "Oil", years_columns] = ( 
    df_totalcapacity_currentpolicy_devunfccc.loc[df_totalcapacity_currentpolicy_devunfccc['fuel_type'] == "Oil", years_columns]
    .div(df_totalcapacity_currentpolicy_devunfccc['Region'].map(df_power_oil_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_currentpolicy_devunfccc['Region'].map(df_power_oil_utilization), axis=0)
    )
df_totalcapacity_currentpolicy_devunfccc = df_totalcapacity_currentpolicy_devunfccc.groupby('fuel_type')[years_columns].sum().reset_index()

df_totalcapacity_currentpolicy_global.loc[df_totalcapacity_currentpolicy_global['fuel_type'] == "Oil", years_columns] = ( 
    df_totalcapacity_currentpolicy_global.loc[df_totalcapacity_currentpolicy_global['fuel_type'] == "Oil", years_columns]
    .div(df_totalcapacity_currentpolicy_global['Region'].map(df_power_oil_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_currentpolicy_global['Region'].map(df_power_oil_utilization), axis=0)
    )
df_totalcapacity_currentpolicy_global = df_totalcapacity_currentpolicy_global.groupby('fuel_type')[years_columns].sum().reset_index()




########################################################
#  2. NET ZERO -----------------------------------------
########################################################

# --------------
# total capacity
# 1 - coal
df_totalcapacity_netzero_deu.loc[df_totalcapacity_netzero_deu['fuel_type'] == "Coal", years_columns] = ( 
    df_totalcapacity_netzero_deu.loc[df_totalcapacity_netzero_deu['fuel_type'] == "Coal", years_columns]
    .div(df_totalcapacity_netzero_deu['Region'].map(df_power_coal_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_netzero_deu['Region'].map(df_power_coal_utilization), axis=0)
    )

df_totalcapacity_netzero_idn.loc[df_totalcapacity_netzero_idn['fuel_type'] == "Coal", years_columns] = ( 
    df_totalcapacity_netzero_idn.loc[df_totalcapacity_netzero_idn['fuel_type'] == "Coal", years_columns]
    .div(df_totalcapacity_netzero_idn['Region'].map(df_power_coal_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_netzero_idn['Region'].map(df_power_coal_utilization), axis=0)
    )

df_totalcapacity_netzero_ind.loc[df_totalcapacity_netzero_ind['fuel_type'] == "Coal", years_columns] = ( 
    df_totalcapacity_netzero_ind.loc[df_totalcapacity_netzero_ind['fuel_type'] == "Coal", years_columns]
    .div(df_totalcapacity_netzero_ind['Region'].map(df_power_coal_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_netzero_ind['Region'].map(df_power_coal_utilization), axis=0)
    )

df_totalcapacity_netzero_tur.loc[df_totalcapacity_netzero_tur['fuel_type'] == "Coal", years_columns] = ( 
    df_totalcapacity_netzero_tur.loc[df_totalcapacity_netzero_tur['fuel_type'] == "Coal", years_columns]
    .div(df_totalcapacity_netzero_tur['Region'].map(df_power_coal_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_netzero_tur['Region'].map(df_power_coal_utilization), axis=0)
    )

df_totalcapacity_netzero_usa.loc[df_totalcapacity_netzero_usa['fuel_type'] == "Coal", years_columns] = ( 
    df_totalcapacity_netzero_usa.loc[df_totalcapacity_netzero_usa['fuel_type'] == "Coal", years_columns]
    .div(df_totalcapacity_netzero_usa['Region'].map(df_power_coal_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_netzero_usa['Region'].map(df_power_coal_utilization), axis=0)
    )

df_totalcapacity_netzero_vnm.loc[df_totalcapacity_netzero_vnm['fuel_type'] == "Coal", years_columns] = ( 
    df_totalcapacity_netzero_vnm.loc[df_totalcapacity_netzero_vnm['fuel_type'] == "Coal", years_columns]
    .div(df_totalcapacity_netzero_vnm['Region'].map(df_power_coal_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_netzero_vnm['Region'].map(df_power_coal_utilization), axis=0)
    )

df_totalcapacity_netzero_pol.loc[df_totalcapacity_netzero_pol['fuel_type'] == "Coal", years_columns] = ( 
    df_totalcapacity_netzero_pol.loc[df_totalcapacity_netzero_pol['fuel_type'] == "Coal", years_columns]
    .div(df_totalcapacity_netzero_pol['Region'].map(df_power_coal_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_netzero_pol['Region'].map(df_power_coal_utilization), axis=0)
    )

df_totalcapacity_netzero_kaz.loc[df_totalcapacity_netzero_kaz['fuel_type'] == "Coal", years_columns] = ( 
    df_totalcapacity_netzero_kaz.loc[df_totalcapacity_netzero_kaz['fuel_type'] == "Coal", years_columns]
    .div(df_totalcapacity_netzero_kaz['Region'].map(df_power_coal_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_netzero_kaz['Region'].map(df_power_coal_utilization), axis=0)
    )

df_totalcapacity_netzero_zaf.loc[df_totalcapacity_netzero_zaf['fuel_type'] == "Coal", years_columns] = ( 
    df_totalcapacity_netzero_zaf.loc[df_totalcapacity_netzero_zaf['fuel_type'] == "Coal", years_columns]
    .div(df_totalcapacity_netzero_zaf['Region'].map(df_power_coal_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_netzero_zaf['Region'].map(df_power_coal_utilization), axis=0)
    )

df_totalcapacity_netzero_bgd.loc[df_totalcapacity_netzero_bgd['fuel_type'] == "Coal", years_columns] = ( 
    df_totalcapacity_netzero_bgd.loc[df_totalcapacity_netzero_bgd['fuel_type'] == "Coal", years_columns]
    .div(df_totalcapacity_netzero_bgd['Region'].map(df_power_coal_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_netzero_bgd['Region'].map(df_power_coal_utilization), axis=0)
    )

df_totalcapacity_netzero_emde.loc[df_totalcapacity_netzero_emde['fuel_type'] == "Coal", years_columns] = ( 
    df_totalcapacity_netzero_emde.loc[df_totalcapacity_netzero_emde['fuel_type'] == "Coal", years_columns]
    .div(df_totalcapacity_netzero_emde['Region'].map(df_power_coal_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_netzero_emde['Region'].map(df_power_coal_utilization), axis=0)
    )

df_totalcapacity_netzero_devunfccc.loc[df_totalcapacity_netzero_devunfccc['fuel_type'] == "Coal", years_columns] = ( 
    df_totalcapacity_netzero_devunfccc.loc[df_totalcapacity_netzero_devunfccc['fuel_type'] == "Coal", years_columns]
    .div(df_totalcapacity_netzero_devunfccc['Region'].map(df_power_coal_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_netzero_devunfccc['Region'].map(df_power_coal_utilization), axis=0)
    )

df_totalcapacity_netzero_global.loc[df_totalcapacity_netzero_global['fuel_type'] == "Coal", years_columns] = ( 
    df_totalcapacity_netzero_global.loc[df_totalcapacity_netzero_global['fuel_type'] == "Coal", years_columns]
    .div(df_totalcapacity_netzero_global['Region'].map(df_power_coal_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_netzero_global['Region'].map(df_power_coal_utilization), axis=0)
    )



# 2 - gas
df_totalcapacity_netzero_deu.loc[df_totalcapacity_netzero_deu['fuel_type'] == "Gas", years_columns] = ( 
    df_totalcapacity_netzero_deu.loc[df_totalcapacity_netzero_deu['fuel_type'] == "Gas", years_columns]
    .div(df_totalcapacity_netzero_deu['Region'].map(df_power_gas_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_netzero_deu['Region'].map(df_power_gas_utilization), axis=0)
    )

df_totalcapacity_netzero_idn.loc[df_totalcapacity_netzero_idn['fuel_type'] == "Gas", years_columns] = ( 
    df_totalcapacity_netzero_idn.loc[df_totalcapacity_netzero_idn['fuel_type'] == "Gas", years_columns]
    .div(df_totalcapacity_netzero_idn['Region'].map(df_power_gas_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_netzero_idn['Region'].map(df_power_gas_utilization), axis=0)
    )

df_totalcapacity_netzero_ind.loc[df_totalcapacity_netzero_ind['fuel_type'] == "Gas", years_columns] = ( 
    df_totalcapacity_netzero_ind.loc[df_totalcapacity_netzero_ind['fuel_type'] == "Gas", years_columns]
    .div(df_totalcapacity_netzero_ind['Region'].map(df_power_gas_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_netzero_ind['Region'].map(df_power_gas_utilization), axis=0)
    )

df_totalcapacity_netzero_tur.loc[df_totalcapacity_netzero_tur['fuel_type'] == "Gas", years_columns] = ( 
    df_totalcapacity_netzero_tur.loc[df_totalcapacity_currentpolicy_tur['fuel_type'] == "Gas", years_columns]
    .div(df_totalcapacity_netzero_tur['Region'].map(df_power_gas_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_netzero_tur['Region'].map(df_power_gas_utilization), axis=0)
    )

df_totalcapacity_netzero_usa.loc[df_totalcapacity_netzero_usa['fuel_type'] == "Gas", years_columns] = ( 
    df_totalcapacity_netzero_usa.loc[df_totalcapacity_netzero_usa['fuel_type'] == "Gas", years_columns]
    .div(df_totalcapacity_netzero_usa['Region'].map(df_power_gas_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_netzero_usa['Region'].map(df_power_gas_utilization), axis=0)
    )

df_totalcapacity_netzero_vnm.loc[df_totalcapacity_netzero_vnm['fuel_type'] == "Gas", years_columns] = ( 
    df_totalcapacity_netzero_vnm.loc[df_totalcapacity_netzero_vnm['fuel_type'] == "Gas", years_columns]
    .div(df_totalcapacity_netzero_vnm['Region'].map(df_power_gas_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_netzero_vnm['Region'].map(df_power_gas_utilization), axis=0)
    )

df_totalcapacity_netzero_pol.loc[df_totalcapacity_netzero_pol['fuel_type'] == "Gas", years_columns] = ( 
    df_totalcapacity_netzero_pol.loc[df_totalcapacity_netzero_pol['fuel_type'] == "Gas", years_columns]
    .div(df_totalcapacity_netzero_pol['Region'].map(df_power_gas_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_netzero_pol['Region'].map(df_power_gas_utilization), axis=0)
    )

df_totalcapacity_netzero_kaz.loc[df_totalcapacity_netzero_kaz['fuel_type'] == "Gas", years_columns] = ( 
    df_totalcapacity_netzero_kaz.loc[df_totalcapacity_netzero_kaz['fuel_type'] == "Gas", years_columns]
    .div(df_totalcapacity_netzero_kaz['Region'].map(df_power_gas_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_netzero_kaz['Region'].map(df_power_gas_utilization), axis=0)
    )

df_totalcapacity_netzero_zaf.loc[df_totalcapacity_netzero_zaf['fuel_type'] == "Gas", years_columns] = ( 
    df_totalcapacity_netzero_zaf.loc[df_totalcapacity_netzero_zaf['fuel_type'] == "Gas", years_columns]
    .div(df_totalcapacity_netzero_zaf['Region'].map(df_power_gas_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_netzero_zaf['Region'].map(df_power_gas_utilization), axis=0)
    )

df_totalcapacity_netzero_bgd.loc[df_totalcapacity_netzero_bgd['fuel_type'] == "Gas", years_columns] = ( 
    df_totalcapacity_netzero_bgd.loc[df_totalcapacity_netzero_bgd['fuel_type'] == "Gas", years_columns]
    .div(df_totalcapacity_netzero_bgd['Region'].map(df_power_gas_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_netzero_bgd['Region'].map(df_power_gas_utilization), axis=0)
    )

df_totalcapacity_netzero_emde.loc[df_totalcapacity_netzero_emde['fuel_type'] == "Gas", years_columns] = ( 
    df_totalcapacity_netzero_emde.loc[df_totalcapacity_netzero_emde['fuel_type'] == "Gas", years_columns]
    .div(df_totalcapacity_netzero_emde['Region'].map(df_power_gas_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_netzero_emde['Region'].map(df_power_gas_utilization), axis=0)
    )

df_totalcapacity_netzero_devunfccc.loc[df_totalcapacity_netzero_devunfccc['fuel_type'] == "Gas", years_columns] = ( 
    df_totalcapacity_netzero_devunfccc.loc[df_totalcapacity_netzero_devunfccc['fuel_type'] == "Gas", years_columns]
    .div(df_totalcapacity_netzero_devunfccc['Region'].map(df_power_gas_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_netzero_devunfccc['Region'].map(df_power_gas_utilization), axis=0)
    )

df_totalcapacity_netzero_global.loc[df_totalcapacity_netzero_global['fuel_type'] == "Gas", years_columns] = ( 
    df_totalcapacity_netzero_global.loc[df_totalcapacity_netzero_global['fuel_type'] == "Gas", years_columns]
    .div(df_totalcapacity_netzero_global['Region'].map(df_power_gas_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_netzero_global['Region'].map(df_power_gas_utilization), axis=0)
    )


# 3 - oil
df_totalcapacity_netzero_deu.loc[df_totalcapacity_netzero_deu['fuel_type'] == "Oil", years_columns] = ( 
    df_totalcapacity_netzero_deu.loc[df_totalcapacity_netzero_deu['fuel_type'] == "Oil", years_columns]
    .div(df_totalcapacity_netzero_deu['Region'].map(df_power_oil_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_netzero_deu['Region'].map(df_power_oil_utilization), axis=0)
    )

df_totalcapacity_netzero_idn.loc[df_totalcapacity_netzero_idn['fuel_type'] == "Oil", years_columns] = ( 
    df_totalcapacity_netzero_idn.loc[df_totalcapacity_netzero_idn['fuel_type'] == "Oil", years_columns]
    .div(df_totalcapacity_netzero_idn['Region'].map(df_power_oil_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_netzero_idn['Region'].map(df_power_oil_utilization), axis=0)
    )

df_totalcapacity_netzero_ind.loc[df_totalcapacity_netzero_ind['fuel_type'] == "Oil", years_columns] = ( 
    df_totalcapacity_netzero_ind.loc[df_totalcapacity_netzero_ind['fuel_type'] == "Oil", years_columns]
    .div(df_totalcapacity_netzero_ind['Region'].map(df_power_oil_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_netzero_ind['Region'].map(df_power_oil_utilization), axis=0)
    )

df_totalcapacity_netzero_tur.loc[df_totalcapacity_netzero_tur['fuel_type'] == "Oil", years_columns] = ( 
    df_totalcapacity_netzero_tur.loc[df_totalcapacity_netzero_tur['fuel_type'] == "Oil", years_columns]
    .div(df_totalcapacity_netzero_tur['Region'].map(df_power_oil_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_netzero_tur['Region'].map(df_power_oil_utilization), axis=0)
    )

df_totalcapacity_netzero_usa.loc[df_totalcapacity_netzero_usa['fuel_type'] == "Oil", years_columns] = ( 
    df_totalcapacity_netzero_usa.loc[df_totalcapacity_netzero_usa['fuel_type'] == "Oil", years_columns]
    .div(df_totalcapacity_netzero_usa['Region'].map(df_power_oil_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_netzero_usa['Region'].map(df_power_oil_utilization), axis=0)
    )

df_totalcapacity_netzero_vnm.loc[df_totalcapacity_netzero_vnm['fuel_type'] == "Oil", years_columns] = ( 
    df_totalcapacity_netzero_vnm.loc[df_totalcapacity_netzero_vnm['fuel_type'] == "Oil", years_columns]
    .div(df_totalcapacity_netzero_vnm['Region'].map(df_power_oil_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_netzero_vnm['Region'].map(df_power_oil_utilization), axis=0)
    )

df_totalcapacity_netzero_pol.loc[df_totalcapacity_netzero_pol['fuel_type'] == "Oil", years_columns] = ( 
    df_totalcapacity_netzero_pol.loc[df_totalcapacity_netzero_pol['fuel_type'] == "Oil", years_columns]
    .div(df_totalcapacity_netzero_pol['Region'].map(df_power_oil_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_netzero_pol['Region'].map(df_power_oil_utilization), axis=0)
    )

df_totalcapacity_netzero_kaz.loc[df_totalcapacity_netzero_kaz['fuel_type'] == "Oil", years_columns] = ( 
    df_totalcapacity_netzero_kaz.loc[df_totalcapacity_netzero_kaz['fuel_type'] == "Oil", years_columns]
    .div(df_totalcapacity_netzero_kaz['Region'].map(df_power_oil_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_netzero_kaz['Region'].map(df_power_oil_utilization), axis=0)
    )

df_totalcapacity_netzero_zaf.loc[df_totalcapacity_netzero_zaf['fuel_type'] == "Oil", years_columns] = ( 
    df_totalcapacity_netzero_zaf.loc[df_totalcapacity_netzero_zaf['fuel_type'] == "Oil", years_columns]
    .div(df_totalcapacity_netzero_zaf['Region'].map(df_power_oil_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_netzero_zaf['Region'].map(df_power_oil_utilization), axis=0)
    )

df_totalcapacity_netzero_bgd.loc[df_totalcapacity_netzero_bgd['fuel_type'] == "Oil", years_columns] = ( 
    df_totalcapacity_netzero_bgd.loc[df_totalcapacity_netzero_bgd['fuel_type'] == "Oil", years_columns]
    .div(df_totalcapacity_netzero_bgd['Region'].map(df_power_oil_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_netzero_bgd['Region'].map(df_power_oil_utilization), axis=0)
    )

df_totalcapacity_netzero_emde.loc[df_totalcapacity_netzero_emde['fuel_type'] == "Oil", years_columns] = ( 
    df_totalcapacity_netzero_emde.loc[df_totalcapacity_netzero_emde['fuel_type'] == "Oil", years_columns]
    .div(df_totalcapacity_netzero_emde['Region'].map(df_power_oil_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_netzero_emde['Region'].map(df_power_oil_utilization), axis=0)
    )
df_totalcapacity_netzero_emde = df_totalcapacity_netzero_emde.groupby('fuel_type')[years_columns].sum().reset_index()

df_totalcapacity_netzero_devunfccc.loc[df_totalcapacity_netzero_devunfccc['fuel_type'] == "Oil", years_columns] = ( 
    df_totalcapacity_netzero_devunfccc.loc[df_totalcapacity_netzero_devunfccc['fuel_type'] == "Oil", years_columns]
    .div(df_totalcapacity_netzero_devunfccc['Region'].map(df_power_oil_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_netzero_devunfccc['Region'].map(df_power_oil_utilization), axis=0)
    )
df_totalcapacity_netzero_devunfccc = df_totalcapacity_netzero_devunfccc.groupby('fuel_type')[years_columns].sum().reset_index()

df_totalcapacity_netzero_global.loc[df_totalcapacity_netzero_global['fuel_type'] == "Oil", years_columns] = ( 
    df_totalcapacity_netzero_global.loc[df_totalcapacity_netzero_global['fuel_type'] == "Oil", years_columns]
    .div(df_totalcapacity_netzero_global['Region'].map(df_power_oil_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_netzero_global['Region'].map(df_power_oil_utilization), axis=0)
    )
df_totalcapacity_netzero_global = df_totalcapacity_netzero_global.groupby('fuel_type')[years_columns].sum().reset_index()





########################################################
#  3. NET ZERO 1.5C 50% adjusted -----------------------
########################################################

# --------------
# total capacity
# 1 - coal
df_totalcapacity_nz1550v2_deu.loc[df_totalcapacity_nz1550v2_deu['fuel_type'] == "Coal", years_columns] = ( 
    df_totalcapacity_nz1550v2_deu.loc[df_totalcapacity_nz1550v2_deu['fuel_type'] == "Coal", years_columns]
    .div(df_totalcapacity_nz1550v2_deu['Region'].map(df_power_coal_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_nz1550v2_deu['Region'].map(df_power_coal_utilization), axis=0)
    )

df_totalcapacity_nz1550v2_idn.loc[df_totalcapacity_nz1550v2_idn['fuel_type'] == "Coal", years_columns] = ( 
    df_totalcapacity_nz1550v2_idn.loc[df_totalcapacity_nz1550v2_idn['fuel_type'] == "Coal", years_columns]
    .div(df_totalcapacity_nz1550v2_idn['Region'].map(df_power_coal_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_nz1550v2_idn['Region'].map(df_power_coal_utilization), axis=0)
    )

df_totalcapacity_nz1550v2_ind.loc[df_totalcapacity_nz1550v2_ind['fuel_type'] == "Coal", years_columns] = ( 
    df_totalcapacity_nz1550v2_ind.loc[df_totalcapacity_nz1550v2_ind['fuel_type'] == "Coal", years_columns]
    .div(df_totalcapacity_nz1550v2_ind['Region'].map(df_power_coal_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_nz1550v2_ind['Region'].map(df_power_coal_utilization), axis=0)
    )

df_totalcapacity_nz1550v2_tur.loc[df_totalcapacity_nz1550v2_tur['fuel_type'] == "Coal", years_columns] = ( 
    df_totalcapacity_nz1550v2_tur.loc[df_totalcapacity_nz1550v2_tur['fuel_type'] == "Coal", years_columns]
    .div(df_totalcapacity_nz1550v2_tur['Region'].map(df_power_coal_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_nz1550v2_tur['Region'].map(df_power_coal_utilization), axis=0)
    )

df_totalcapacity_nz1550v2_usa.loc[df_totalcapacity_nz1550v2_usa['fuel_type'] == "Coal", years_columns] = ( 
    df_totalcapacity_nz1550v2_usa.loc[df_totalcapacity_nz1550v2_usa['fuel_type'] == "Coal", years_columns]
    .div(df_totalcapacity_nz1550v2_usa['Region'].map(df_power_coal_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_nz1550v2_usa['Region'].map(df_power_coal_utilization), axis=0)
    )

df_totalcapacity_nz1550v2_vnm.loc[df_totalcapacity_nz1550v2_vnm['fuel_type'] == "Coal", years_columns] = ( 
    df_totalcapacity_nz1550v2_vnm.loc[df_totalcapacity_nz1550v2_vnm['fuel_type'] == "Coal", years_columns]
    .div(df_totalcapacity_nz1550v2_vnm['Region'].map(df_power_coal_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_nz1550v2_vnm['Region'].map(df_power_coal_utilization), axis=0)
    )

df_totalcapacity_nz1550v2_pol.loc[df_totalcapacity_nz1550v2_pol['fuel_type'] == "Coal", years_columns] = ( 
    df_totalcapacity_nz1550v2_pol.loc[df_totalcapacity_nz1550v2_pol['fuel_type'] == "Coal", years_columns]
    .div(df_totalcapacity_nz1550v2_pol['Region'].map(df_power_coal_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_nz1550v2_pol['Region'].map(df_power_coal_utilization), axis=0)
    )

df_totalcapacity_nz1550v2_kaz.loc[df_totalcapacity_nz1550v2_kaz['fuel_type'] == "Coal", years_columns] = ( 
    df_totalcapacity_nz1550v2_kaz.loc[df_totalcapacity_nz1550v2_kaz['fuel_type'] == "Coal", years_columns]
    .div(df_totalcapacity_nz1550v2_kaz['Region'].map(df_power_coal_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_nz1550v2_kaz['Region'].map(df_power_coal_utilization), axis=0)
    )

df_totalcapacity_nz1550v2_zaf.loc[df_totalcapacity_nz1550v2_zaf['fuel_type'] == "Coal", years_columns] = ( 
    df_totalcapacity_nz1550v2_zaf.loc[df_totalcapacity_nz1550v2_zaf['fuel_type'] == "Coal", years_columns]
    .div(df_totalcapacity_nz1550v2_zaf['Region'].map(df_power_coal_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_nz1550v2_zaf['Region'].map(df_power_coal_utilization), axis=0)
    )

df_totalcapacity_nz1550v2_bgd.loc[df_totalcapacity_nz1550v2_bgd['fuel_type'] == "Coal", years_columns] = ( 
    df_totalcapacity_nz1550v2_bgd.loc[df_totalcapacity_nz1550v2_bgd['fuel_type'] == "Coal", years_columns]
    .div(df_totalcapacity_nz1550v2_bgd['Region'].map(df_power_coal_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_nz1550v2_bgd['Region'].map(df_power_coal_utilization), axis=0)
    )

df_totalcapacity_nz1550v2_emde.loc[df_totalcapacity_nz1550v2_emde['fuel_type'] == "Coal", years_columns] = ( 
    df_totalcapacity_nz1550v2_emde.loc[df_totalcapacity_nz1550v2_emde['fuel_type'] == "Coal", years_columns]
    .div(df_totalcapacity_nz1550v2_emde['Region'].map(df_power_coal_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_nz1550v2_emde['Region'].map(df_power_coal_utilization), axis=0)
    )

df_totalcapacity_nz1550v2_devunfccc.loc[df_totalcapacity_nz1550v2_devunfccc['fuel_type'] == "Coal", years_columns] = ( 
    df_totalcapacity_nz1550v2_devunfccc.loc[df_totalcapacity_nz1550v2_devunfccc['fuel_type'] == "Coal", years_columns]
    .div(df_totalcapacity_nz1550v2_devunfccc['Region'].map(df_power_coal_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_nz1550v2_devunfccc['Region'].map(df_power_coal_utilization), axis=0)
    )

df_totalcapacity_nz1550v2_global.loc[df_totalcapacity_nz1550v2_global['fuel_type'] == "Coal", years_columns] = ( 
    df_totalcapacity_nz1550v2_global.loc[df_totalcapacity_nz1550v2_global['fuel_type'] == "Coal", years_columns]
    .div(df_totalcapacity_nz1550v2_global['Region'].map(df_power_coal_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_nz1550v2_global['Region'].map(df_power_coal_utilization), axis=0)
    )



# 2 - gas
df_totalcapacity_nz1550v2_deu.loc[df_totalcapacity_nz1550v2_deu['fuel_type'] == "Gas", years_columns] = ( 
    df_totalcapacity_nz1550v2_deu.loc[df_totalcapacity_nz1550v2_deu['fuel_type'] == "Gas", years_columns]
    .div(df_totalcapacity_nz1550v2_deu['Region'].map(df_power_gas_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_nz1550v2_deu['Region'].map(df_power_gas_utilization), axis=0)
    )

df_totalcapacity_nz1550v2_idn.loc[df_totalcapacity_nz1550v2_idn['fuel_type'] == "Gas", years_columns] = ( 
    df_totalcapacity_nz1550v2_idn.loc[df_totalcapacity_nz1550v2_idn['fuel_type'] == "Gas", years_columns]
    .div(df_totalcapacity_nz1550v2_idn['Region'].map(df_power_gas_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_nz1550v2_idn['Region'].map(df_power_gas_utilization), axis=0)
    )

df_totalcapacity_nz1550v2_ind.loc[df_totalcapacity_nz1550v2_ind['fuel_type'] == "Gas", years_columns] = ( 
    df_totalcapacity_nz1550v2_ind.loc[df_totalcapacity_nz1550v2_ind['fuel_type'] == "Gas", years_columns]
    .div(df_totalcapacity_nz1550v2_ind['Region'].map(df_power_gas_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_nz1550v2_ind['Region'].map(df_power_gas_utilization), axis=0)
    )

df_totalcapacity_nz1550v2_tur.loc[df_totalcapacity_nz1550v2_tur['fuel_type'] == "Gas", years_columns] = ( 
    df_totalcapacity_nz1550v2_tur.loc[df_totalcapacity_nz1550v2_tur['fuel_type'] == "Gas", years_columns]
    .div(df_totalcapacity_nz1550v2_tur['Region'].map(df_power_gas_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_nz1550v2_tur['Region'].map(df_power_gas_utilization), axis=0)
    )

df_totalcapacity_nz1550v2_usa.loc[df_totalcapacity_nz1550v2_usa['fuel_type'] == "Gas", years_columns] = ( 
    df_totalcapacity_nz1550v2_usa.loc[df_totalcapacity_nz1550v2_usa['fuel_type'] == "Gas", years_columns]
    .div(df_totalcapacity_nz1550v2_usa['Region'].map(df_power_gas_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_nz1550v2_usa['Region'].map(df_power_gas_utilization), axis=0)
    )

df_totalcapacity_nz1550v2_vnm.loc[df_totalcapacity_nz1550v2_vnm['fuel_type'] == "Gas", years_columns] = ( 
    df_totalcapacity_nz1550v2_vnm.loc[df_totalcapacity_nz1550v2_vnm['fuel_type'] == "Gas", years_columns]
    .div(df_totalcapacity_nz1550v2_vnm['Region'].map(df_power_gas_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_nz1550v2_vnm['Region'].map(df_power_gas_utilization), axis=0)
    )

df_totalcapacity_nz1550v2_pol.loc[df_totalcapacity_nz1550v2_pol['fuel_type'] == "Gas", years_columns] = ( 
    df_totalcapacity_nz1550v2_pol.loc[df_totalcapacity_nz1550v2_pol['fuel_type'] == "Gas", years_columns]
    .div(df_totalcapacity_nz1550v2_pol['Region'].map(df_power_gas_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_nz1550v2_pol['Region'].map(df_power_gas_utilization), axis=0)
    )

df_totalcapacity_nz1550v2_kaz.loc[df_totalcapacity_nz1550v2_kaz['fuel_type'] == "Gas", years_columns] = ( 
    df_totalcapacity_nz1550v2_kaz.loc[df_totalcapacity_nz1550v2_kaz['fuel_type'] == "Gas", years_columns]
    .div(df_totalcapacity_nz1550v2_kaz['Region'].map(df_power_gas_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_nz1550v2_kaz['Region'].map(df_power_gas_utilization), axis=0)
    )

df_totalcapacity_nz1550v2_zaf.loc[df_totalcapacity_nz1550v2_zaf['fuel_type'] == "Gas", years_columns] = ( 
    df_totalcapacity_nz1550v2_zaf.loc[df_totalcapacity_nz1550v2_zaf['fuel_type'] == "Gas", years_columns]
    .div(df_totalcapacity_nz1550v2_zaf['Region'].map(df_power_gas_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_nz1550v2_zaf['Region'].map(df_power_gas_utilization), axis=0)
    )

df_totalcapacity_nz1550v2_bgd.loc[df_totalcapacity_nz1550v2_bgd['fuel_type'] == "Gas", years_columns] = ( 
    df_totalcapacity_nz1550v2_bgd.loc[df_totalcapacity_nz1550v2_bgd['fuel_type'] == "Gas", years_columns]
    .div(df_totalcapacity_nz1550v2_bgd['Region'].map(df_power_gas_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_nz1550v2_bgd['Region'].map(df_power_gas_utilization), axis=0)
    )

df_totalcapacity_nz1550v2_emde.loc[df_totalcapacity_nz1550v2_emde['fuel_type'] == "Gas", years_columns] = ( 
    df_totalcapacity_nz1550v2_emde.loc[df_totalcapacity_nz1550v2_emde['fuel_type'] == "Gas", years_columns]
    .div(df_totalcapacity_nz1550v2_emde['Region'].map(df_power_gas_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_nz1550v2_emde['Region'].map(df_power_gas_utilization), axis=0)
    )

df_totalcapacity_nz1550v2_devunfccc.loc[df_totalcapacity_nz1550v2_devunfccc['fuel_type'] == "Gas", years_columns] = ( 
    df_totalcapacity_nz1550v2_devunfccc.loc[df_totalcapacity_nz1550v2_devunfccc['fuel_type'] == "Gas", years_columns]
    .div(df_totalcapacity_nz1550v2_devunfccc['Region'].map(df_power_gas_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_nz1550v2_devunfccc['Region'].map(df_power_gas_utilization), axis=0)
    )

df_totalcapacity_nz1550v2_global.loc[df_totalcapacity_nz1550v2_global['fuel_type'] == "Gas", years_columns] = ( 
    df_totalcapacity_nz1550v2_global.loc[df_totalcapacity_nz1550v2_global['fuel_type'] == "Gas", years_columns]
    .div(df_totalcapacity_nz1550v2_global['Region'].map(df_power_gas_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_nz1550v2_global['Region'].map(df_power_gas_utilization), axis=0)
    )




# 3 - oil
df_totalcapacity_nz1550v2_deu.loc[df_totalcapacity_nz1550v2_deu['fuel_type'] == "Oil", years_columns] = ( 
    df_totalcapacity_nz1550v2_deu.loc[df_totalcapacity_nz1550v2_deu['fuel_type'] == "Oil", years_columns]
    .div(df_totalcapacity_nz1550v2_deu['Region'].map(df_power_oil_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_nz1550v2_deu['Region'].map(df_power_oil_utilization), axis=0)
    )

df_totalcapacity_nz1550v2_idn.loc[df_totalcapacity_nz1550v2_idn['fuel_type'] == "Oil", years_columns] = ( 
    df_totalcapacity_nz1550v2_idn.loc[df_totalcapacity_nz1550v2_idn['fuel_type'] == "Oil", years_columns]
    .div(df_totalcapacity_nz1550v2_idn['Region'].map(df_power_oil_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_nz1550v2_idn['Region'].map(df_power_oil_utilization), axis=0)
    )

df_totalcapacity_nz1550v2_ind.loc[df_totalcapacity_nz1550v2_ind['fuel_type'] == "Oil", years_columns] = ( 
    df_totalcapacity_nz1550v2_ind.loc[df_totalcapacity_nz1550v2_ind['fuel_type'] == "Oil", years_columns]
    .div(df_totalcapacity_nz1550v2_ind['Region'].map(df_power_oil_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_nz1550v2_ind['Region'].map(df_power_oil_utilization), axis=0)
    )

df_totalcapacity_nz1550v2_tur.loc[df_totalcapacity_nz1550v2_tur['fuel_type'] == "Oil", years_columns] = ( 
    df_totalcapacity_nz1550v2_tur.loc[df_totalcapacity_nz1550v2_tur['fuel_type'] == "Oil", years_columns]
    .div(df_totalcapacity_nz1550v2_tur['Region'].map(df_power_oil_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_nz1550v2_tur['Region'].map(df_power_oil_utilization), axis=0)
    )

df_totalcapacity_nz1550v2_usa.loc[df_totalcapacity_nz1550v2_usa['fuel_type'] == "Oil", years_columns] = ( 
    df_totalcapacity_nz1550v2_usa.loc[df_totalcapacity_nz1550v2_usa['fuel_type'] == "Oil", years_columns]
    .div(df_totalcapacity_nz1550v2_usa['Region'].map(df_power_oil_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_nz1550v2_usa['Region'].map(df_power_oil_utilization), axis=0)
    )

df_totalcapacity_nz1550v2_vnm.loc[df_totalcapacity_nz1550v2_vnm['fuel_type'] == "Oil", years_columns] = ( 
    df_totalcapacity_nz1550v2_vnm.loc[df_totalcapacity_nz1550v2_vnm['fuel_type'] == "Oil", years_columns]
    .div(df_totalcapacity_nz1550v2_vnm['Region'].map(df_power_oil_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_nz1550v2_vnm['Region'].map(df_power_oil_utilization), axis=0)
    )

df_totalcapacity_nz1550v2_pol.loc[df_totalcapacity_nz1550v2_pol['fuel_type'] == "Oil", years_columns] = ( 
    df_totalcapacity_nz1550v2_pol.loc[df_totalcapacity_nz1550v2_pol['fuel_type'] == "Oil", years_columns]
    .div(df_totalcapacity_nz1550v2_pol['Region'].map(df_power_oil_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_nz1550v2_pol['Region'].map(df_power_oil_utilization), axis=0)
    )

df_totalcapacity_nz1550v2_kaz.loc[df_totalcapacity_nz1550v2_kaz['fuel_type'] == "Oil", years_columns] = ( 
    df_totalcapacity_nz1550v2_kaz.loc[df_totalcapacity_nz1550v2_kaz['fuel_type'] == "Oil", years_columns]
    .div(df_totalcapacity_nz1550v2_kaz['Region'].map(df_power_oil_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_nz1550v2_kaz['Region'].map(df_power_oil_utilization), axis=0)
    )

df_totalcapacity_nz1550v2_zaf.loc[df_totalcapacity_nz1550v2_zaf['fuel_type'] == "Oil", years_columns] = ( 
    df_totalcapacity_nz1550v2_zaf.loc[df_totalcapacity_nz1550v2_zaf['fuel_type'] == "Oil", years_columns]
    .div(df_totalcapacity_nz1550v2_zaf['Region'].map(df_power_oil_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_nz1550v2_zaf['Region'].map(df_power_oil_utilization), axis=0)
    )

df_totalcapacity_nz1550v2_bgd.loc[df_totalcapacity_nz1550v2_bgd['fuel_type'] == "Oil", years_columns] = ( 
    df_totalcapacity_nz1550v2_bgd.loc[df_totalcapacity_nz1550v2_bgd['fuel_type'] == "Oil", years_columns]
    .div(df_totalcapacity_nz1550v2_bgd['Region'].map(df_power_oil_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_nz1550v2_bgd['Region'].map(df_power_oil_utilization), axis=0)
    )

df_totalcapacity_nz1550v2_emde.loc[df_totalcapacity_nz1550v2_emde['fuel_type'] == "Oil", years_columns] = ( 
    df_totalcapacity_nz1550v2_emde.loc[df_totalcapacity_nz1550v2_emde['fuel_type'] == "Oil", years_columns]
    .div(df_totalcapacity_nz1550v2_emde['Region'].map(df_power_oil_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_nz1550v2_emde['Region'].map(df_power_oil_utilization), axis=0)
    )
df_totalcapacity_nz1550v2_emde = df_totalcapacity_nz1550v2_emde.groupby('fuel_type')[years_columns].sum().reset_index()

df_totalcapacity_nz1550v2_devunfccc.loc[df_totalcapacity_nz1550v2_devunfccc['fuel_type'] == "Oil", years_columns] = ( 
    df_totalcapacity_nz1550v2_devunfccc.loc[df_totalcapacity_nz1550v2_devunfccc['fuel_type'] == "Oil", years_columns]
    .div(df_totalcapacity_nz1550v2_devunfccc['Region'].map(df_power_oil_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_nz1550v2_devunfccc['Region'].map(df_power_oil_utilization), axis=0)
    )
df_totalcapacity_nz1550v2_devunfccc = df_totalcapacity_nz1550v2_devunfccc.groupby('fuel_type')[years_columns].sum().reset_index()

df_totalcapacity_nz1550v2_global.loc[df_totalcapacity_nz1550v2_global['fuel_type'] == "Oil", years_columns] = ( 
    df_totalcapacity_nz1550v2_global.loc[df_totalcapacity_nz1550v2_global['fuel_type'] == "Oil", years_columns]
    .div(df_totalcapacity_nz1550v2_global['Region'].map(df_power_oil_intensity), axis=0)
    .div((24*365))
    .div(df_totalcapacity_nz1550v2_global['Region'].map(df_power_oil_utilization), axis=0)
    )
df_totalcapacity_nz1550v2_global = df_totalcapacity_nz1550v2_global.groupby('fuel_type')[years_columns].sum().reset_index()




# delete extras
del df_power_oil_intensity, df_power_gas_intensity, df_power_coal_intensity
del df_power_oil_utilization, df_power_gas_utilization, df_power_coal_utilization








# In[4]: ADD TOTAL ANNUAL & CUMULATIVE & AVOIDED --- EMISSIONS & CAPACITY FOR EACH COUNTRY
##########################################################################################

# --------------
# set some initial terms: column names, temporary variables to store data from the loops

# Define the columns names for the final DataFrames
new_column_names = ['ghg_annual_cp', 'ghg_annual_nz', 'ghg_annual_nznew', 'ghg_annaul_avoided',
                    'ghg_cumulative_cp', 'ghg_cumulative_nz', 'ghg_cumulative_nznew','ghg_cumulative_avoided',
                    'capacity_annual_cp', 'capacity_annual_nz', 'capacity_annual_nznew', 'capacity_annaul_avoided','capacity_cumulative_avoided']


# List of country codes to iterate over
temp_country_codes = ['deu', 'idn', 'ind', 'tur', 'usa', 'vnm','pol', 'kaz', 'zaf', 'bgd', 'emde', 'devunfccc', 'global']

# Dictionary to store each country's DataFrame
temp_country_dfs = {}





# --------------
# this loop goes through each coutnry and scenario (both emissions & capacity) and combines each country into a single dataframe

# Loop through each country code
for country_code in temp_country_codes:

    # this is to select each countrie's respective data to start with
    temp_emissions_currentpolicy = globals()[f'df_emissions_currentpolicy_{country_code}'].copy()
    temp_emissions_netzero = globals()[f'df_emissions_netzero_{country_code}'].copy()
    temp_emissions_nz1550v2 = globals()[f'df_emissions_nz1550v2_{country_code}'].copy()
    temp_totalcapacity_currentpolicy = globals()[f'df_totalcapacity_currentpolicy_{country_code}'].copy()
    temp_totalcapacity_netzero = globals()[f'df_totalcapacity_netzero_{country_code}'].copy()
    temp_totalcapacity_nz1550v2 = globals()[f'df_totalcapacity_nz1550v2_{country_code}'].copy()
    
    
    # Emissions calculations --- total emissions across all fuel types --- and get avoided CP vs NZ15 50%
    temp_emissions_currentpolicy_annual = temp_emissions_currentpolicy[years_columns].sum(axis=0)
    temp_emissions_netzero_annual = temp_emissions_netzero[years_columns].sum(axis=0)
    temp_emissions_nz1550v2_annual = temp_emissions_nz1550v2[years_columns].sum(axis=0)
    temp_emissions_avoided_annual = temp_emissions_currentpolicy_annual - temp_emissions_nz1550v2_annual   

    temp_emissions_currentpolicy_cumulative = temp_emissions_currentpolicy_annual.cumsum()
    temp_emissions_netzero_cumulative = temp_emissions_netzero_annual.cumsum()
    temp_emissions_nz1550v2_cumulative = temp_emissions_nz1550v2_annual.cumsum()
    temp_emissions_avoided_cumulative = temp_emissions_avoided_annual.cumsum()


    # Capacity calculations --- total capacity across all fuel types --- and get avoided CP vs NZ15 50%
    temp_totalcapacity_currentpolicy_annual = temp_totalcapacity_currentpolicy[years_columns].sum(axis=0)
    temp_totalcapacity_netzero_annual = temp_totalcapacity_netzero[years_columns].sum(axis=0)
    temp_totalcapacity_nz1550v2_annual = temp_totalcapacity_nz1550v2[years_columns].sum(axis=0)
    temp_totalcapacity_avoided_annual = temp_totalcapacity_nz1550v2_annual.diff()
    temp_totalcapacity_avoided_cumulative = temp_totalcapacity_avoided_annual.cumsum()


    # Combine into a single DataFrame for the current country
    temp_combined = pd.concat([temp_emissions_currentpolicy_annual, temp_emissions_netzero_annual, temp_emissions_nz1550v2_annual, temp_emissions_avoided_annual,
                             temp_emissions_currentpolicy_cumulative, temp_emissions_netzero_cumulative, temp_emissions_nz1550v2_cumulative, temp_emissions_avoided_cumulative,
                             temp_totalcapacity_currentpolicy_annual, temp_totalcapacity_netzero_annual, temp_totalcapacity_nz1550v2_annual, temp_totalcapacity_avoided_annual,
                             temp_totalcapacity_avoided_cumulative], axis=1)

    # Rename columns
    temp_combined.columns = new_column_names
    
    # Store the DataFrame in the dictionary using the country code as the key
    temp_country_dfs[country_code] = temp_combined



# Access the DataFrames for each country, e.g., df_deu, df_usa, etc.
df_country_deu = temp_country_dfs['deu']
df_country_idn = temp_country_dfs['idn']
df_country_ind = temp_country_dfs['ind']
df_country_tur = temp_country_dfs['tur']
df_country_usa = temp_country_dfs['usa']
df_country_vnm = temp_country_dfs['vnm']
df_country_pol = temp_country_dfs['pol']
df_country_kaz = temp_country_dfs['kaz']
df_country_zaf = temp_country_dfs['zaf']
df_country_bgd = temp_country_dfs['bgd']
df_country_emde = temp_country_dfs['emde']
df_country_devunfccc = temp_country_dfs['devunfccc']
df_country_global = temp_country_dfs['global']



# delete
del temp_combined, temp_country_codes, temp_country_dfs, country_code, new_column_names
del temp_emissions_avoided_annual, temp_emissions_avoided_cumulative, temp_emissions_currentpolicy_annual, temp_emissions_currentpolicy_cumulative, temp_emissions_netzero_annual, temp_emissions_netzero_cumulative, temp_emissions_nz1550v2_annual, temp_emissions_nz1550v2_cumulative
del temp_totalcapacity_avoided_annual, temp_totalcapacity_avoided_cumulative, temp_totalcapacity_currentpolicy_annual, temp_totalcapacity_netzero_annual, temp_totalcapacity_nz1550v2_annual
del temp_emissions_currentpolicy, temp_emissions_netzero, temp_emissions_nz1550v2, temp_totalcapacity_currentpolicy, temp_totalcapacity_netzero, temp_totalcapacity_nz1550v2










# In[4]: BY FUEL AVOIDED CAPACITY 
#######################################


# get annual total capacity avoided by country
df_byfuel_avoided_annual_deu = df_totalcapacity_nz1550v2_deu.assign(**df_totalcapacity_nz1550v2_deu[years_columns].diff(axis=1))
df_byfuel_avoided_annual_idn = df_totalcapacity_nz1550v2_idn.assign(**df_totalcapacity_nz1550v2_idn[years_columns].diff(axis=1))
df_byfuel_avoided_annual_ind = df_totalcapacity_nz1550v2_ind.assign(**df_totalcapacity_nz1550v2_ind[years_columns].diff(axis=1))
df_byfuel_avoided_annual_tur = df_totalcapacity_nz1550v2_tur.assign(**df_totalcapacity_nz1550v2_tur[years_columns].diff(axis=1))
df_byfuel_avoided_annual_usa = df_totalcapacity_nz1550v2_usa.assign(**df_totalcapacity_nz1550v2_usa[years_columns].diff(axis=1))
df_byfuel_avoided_annual_vnm = df_totalcapacity_nz1550v2_vnm.assign(**df_totalcapacity_nz1550v2_vnm[years_columns].diff(axis=1))
df_byfuel_avoided_annual_pol = df_totalcapacity_nz1550v2_pol.assign(**df_totalcapacity_nz1550v2_pol[years_columns].diff(axis=1))
df_byfuel_avoided_annual_kaz = df_totalcapacity_nz1550v2_kaz.assign(**df_totalcapacity_nz1550v2_kaz[years_columns].diff(axis=1))
df_byfuel_avoided_annual_zaf = df_totalcapacity_nz1550v2_zaf.assign(**df_totalcapacity_nz1550v2_zaf[years_columns].diff(axis=1))
df_byfuel_avoided_annual_bgd = df_totalcapacity_nz1550v2_bgd.assign(**df_totalcapacity_nz1550v2_bgd[years_columns].diff(axis=1))
df_byfuel_avoided_annual_emde = df_totalcapacity_nz1550v2_emde.assign(**df_totalcapacity_nz1550v2_emde[years_columns].diff(axis=1))
df_byfuel_avoided_annual_devunfccc = df_totalcapacity_nz1550v2_devunfccc.assign(**df_totalcapacity_nz1550v2_devunfccc[years_columns].diff(axis=1))
df_byfuel_avoided_annual_global = df_totalcapacity_nz1550v2_global.assign(**df_totalcapacity_nz1550v2_global[years_columns].diff(axis=1))


# now get total avoided capacity by country and fuel
df_byfuel_avoided_cumulative_deu = df_byfuel_avoided_annual_deu.copy().assign(**{col: df_byfuel_avoided_annual_deu[years_columns].cumsum(axis=1)[col] for col in years_columns})
df_byfuel_avoided_cumulative_idn = df_byfuel_avoided_annual_idn.copy().assign(**{col: df_byfuel_avoided_annual_idn[years_columns].cumsum(axis=1)[col] for col in years_columns})
df_byfuel_avoided_cumulative_ind = df_byfuel_avoided_annual_ind.copy().assign(**{col: df_byfuel_avoided_annual_ind[years_columns].cumsum(axis=1)[col] for col in years_columns})
df_byfuel_avoided_cumulative_tur = df_byfuel_avoided_annual_tur.copy().assign(**{col: df_byfuel_avoided_annual_tur[years_columns].cumsum(axis=1)[col] for col in years_columns})
df_byfuel_avoided_cumulative_usa = df_byfuel_avoided_annual_usa.copy().assign(**{col: df_byfuel_avoided_annual_usa[years_columns].cumsum(axis=1)[col] for col in years_columns})
df_byfuel_avoided_cumulative_vnm = df_byfuel_avoided_annual_vnm.copy().assign(**{col: df_byfuel_avoided_annual_vnm[years_columns].cumsum(axis=1)[col] for col in years_columns})
df_byfuel_avoided_cumulative_pol = df_byfuel_avoided_annual_pol.copy().assign(**{col: df_byfuel_avoided_annual_pol[years_columns].cumsum(axis=1)[col] for col in years_columns})
df_byfuel_avoided_cumulative_kaz = df_byfuel_avoided_annual_kaz.copy().assign(**{col: df_byfuel_avoided_annual_kaz[years_columns].cumsum(axis=1)[col] for col in years_columns})
df_byfuel_avoided_cumulative_zaf = df_byfuel_avoided_annual_zaf.copy().assign(**{col: df_byfuel_avoided_annual_zaf[years_columns].cumsum(axis=1)[col] for col in years_columns})
df_byfuel_avoided_cumulative_bgd = df_byfuel_avoided_annual_bgd.copy().assign(**{col: df_byfuel_avoided_annual_bgd[years_columns].cumsum(axis=1)[col] for col in years_columns})
df_byfuel_avoided_cumulative_emde = df_byfuel_avoided_annual_emde.copy().assign(**{col: df_byfuel_avoided_annual_emde[years_columns].cumsum(axis=1)[col] for col in years_columns})
df_byfuel_avoided_cumulative_devunfccc = df_byfuel_avoided_annual_devunfccc.copy().assign(**{col: df_byfuel_avoided_annual_devunfccc[years_columns].cumsum(axis=1)[col] for col in years_columns})
df_byfuel_avoided_cumulative_global = df_byfuel_avoided_annual_global.copy().assign(**{col: df_byfuel_avoided_annual_global[years_columns].cumsum(axis=1)[col] for col in years_columns})






# In[]

# export data

# --------------
# countries
df_country_deu.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/1.1 - country - DEU.xlsx', index = False)
df_country_idn.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/1.2 - country - IDN.xlsx', index = False)
df_country_ind.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/1.3 - country - IND.xlsx', index = False)
df_country_tur.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/1.4 - country - TUR.xlsx', index = False)
df_country_usa.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/1.5 - country - USA.xlsx', index = False)
df_country_vnm.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/1.6 - country - VNM.xlsx', index = False)
df_country_pol.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/1.7 - country - POL.xlsx', index = False)
df_country_kaz.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/1.8 - country - KAZ.xlsx', index = False)
df_country_emde.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/1.9 - country - EMDE.xlsx', index = False)
df_country_global.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/1.10 - country - GLOBAL.xlsx', index = False)
df_country_zaf.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/1.11 - country - ZAF.xlsx', index = False)
df_country_bgd.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/1.12 - country - BGD.xlsx', index = False)
df_country_devunfccc.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/1.13 - country - DEVUNFCCC.xlsx', index = False)


# --------------
# emissions  - current policy
df_emissions_currentpolicy_deu.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/2.1 - emissions - current policy - DEU.xlsx', index = False)
df_emissions_currentpolicy_idn.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/2.2 - emissions - current policy - IDN.xlsx', index = False)
df_emissions_currentpolicy_ind.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/2.3 - emissions - current policy - IND.xlsx', index = False)
df_emissions_currentpolicy_tur.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/2.4 - emissions - current policy - TUR.xlsx', index = False)
df_emissions_currentpolicy_usa.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/2.5 - emissions - current policy - USA.xlsx', index = False)
df_emissions_currentpolicy_vnm.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/2.6 - emissions - current policy - VNM.xlsx', index = False)
df_emissions_currentpolicy_pol.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/2.7 - emissions - current policy - POL.xlsx', index = False)
df_emissions_currentpolicy_kaz.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/2.8 - emissions - current policy - KAZ.xlsx', index = False)
df_emissions_currentpolicy_emde.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/2.9 - emissions - current policy - EMDE.xlsx', index = False)
df_emissions_currentpolicy_global.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/2.10 - emissions - current policy - GLOBAL.xlsx', index = False)
df_emissions_currentpolicy_zaf.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/2.11 - emissions - current policy - ZAF.xlsx', index = False)
df_emissions_currentpolicy_bgd.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/2.12 - emissions - current policy - BGD.xlsx', index = False)
df_emissions_currentpolicy_devunfccc.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/2.13 - emissions - current policy - DEVUNFCCC.xlsx', index = False)


# emissions  - netzero
df_emissions_netzero_deu.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/3.1 - emissions - netzero - DEU.xlsx', index = False)
df_emissions_netzero_idn.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/3.2 - emissions - netzero - IDN.xlsx', index = False)
df_emissions_netzero_ind.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/3.3 - emissions - netzero - IND.xlsx', index = False)
df_emissions_netzero_tur.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/3.4 - emissions - netzero - TUR.xlsx', index = False)
df_emissions_netzero_usa.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/3.5 - emissions - netzero - USA.xlsx', index = False)
df_emissions_netzero_vnm.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/3.6 - emissions - netzero - VNM.xlsx', index = False)
df_emissions_netzero_pol.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/3.7 - emissions - netzero - POL.xlsx', index = False)
df_emissions_netzero_kaz.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/3.8 - emissions - netzero - KAZ.xlsx', index = False)
df_emissions_netzero_emde.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/3.9 - emissions - netzero - EMDE.xlsx', index = False)
df_emissions_netzero_global.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/3.10 - emissions - netzero - GLOBAL.xlsx', index = False)
df_emissions_netzero_zaf.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/3.11 - emissions - netzero - ZAF.xlsx', index = False)
df_emissions_netzero_bgd.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/3.12 - emissions - netzero - BGD.xlsx', index = False)
df_emissions_netzero_devunfccc.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/3.13 - emissions - netzero - DEVUNFCCC.xlsx', index = False)

# emissions  - net zero 1.5C 50%
df_emissions_nz1550v2_deu.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/4.1 - emissions - net zero 15C 50% - DEU.xlsx', index = False)
df_emissions_nz1550v2_idn.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/4.2 - emissions - net zero 15C 50% - IDN.xlsx', index = False)
df_emissions_nz1550v2_ind.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/4.3 - emissions - net zero 15C 50% - IND.xlsx', index = False)
df_emissions_nz1550v2_tur.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/4.4 - emissions - net zero 15C 50% - TUR.xlsx', index = False)
df_emissions_nz1550v2_usa.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/4.5 - emissions - net zero 15C 50% - USA.xlsx', index = False)
df_emissions_nz1550v2_vnm.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/4.6 - emissions - net zero 15C 50% - VNM.xlsx', index = False)
df_emissions_nz1550v2_pol.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/4.7 - emissions - net zero 15C 50% - POL.xlsx', index = False)
df_emissions_nz1550v2_kaz.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/4.8 - emissions - net zero 15C 50% - KAZ.xlsx', index = False)
df_emissions_nz1550v2_emde.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/4.9 - emissions - net zero 15C 50% - EMDE.xlsx', index = False)
df_emissions_nz1550v2_global.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/4.10 - emissions - net zero 15C 50% - GLOBAL.xlsx', index = False)
df_emissions_nz1550v2_zaf.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/4.11 - emissions - net zero 15C 50% - ZAF.xlsx', index = False)
df_emissions_nz1550v2_bgd.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/4.12 - emissions - net zero 15C 50% - BGD.xlsx', index = False)
df_emissions_nz1550v2_devunfccc.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/4.13 - emissions - net zero 15C 50% - DEVUNFCCC.xlsx', index = False)

# --------------
# total capacity  - current policy
df_totalcapacity_currentpolicy_deu.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/5.1 - total capacity - current policy - DEU.xlsx', index = False)
df_totalcapacity_currentpolicy_idn.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/5.2 - total capacity - current policy - IDN.xlsx', index = False)
df_totalcapacity_currentpolicy_ind.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/5.3 - total capacity - current policy - IND.xlsx', index = False)
df_totalcapacity_currentpolicy_tur.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/5.4 - total capacity - current policy - TUR.xlsx', index = False)
df_totalcapacity_currentpolicy_usa.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/5.5 - total capacity - current policy - USA.xlsx', index = False)
df_totalcapacity_currentpolicy_vnm.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/5.6 - total capacity - current policy - VNM.xlsx', index = False)
df_totalcapacity_currentpolicy_pol.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/5.7 - total capacity - current policy - POL.xlsx', index = False)
df_totalcapacity_currentpolicy_kaz.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/5.8 - total capacity - current policy - KAZ.xlsx', index = False)
df_totalcapacity_currentpolicy_emde.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/5.9 - total capacity - current policy - EMDE.xlsx', index = False)
df_totalcapacity_currentpolicy_global.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/5.10 - total capacity - current policy - GLOBAL.xlsx', index = False)
df_totalcapacity_currentpolicy_zaf.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/5.11 - total capacity - current policy - ZAF.xlsx', index = False)
df_totalcapacity_currentpolicy_bgd.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/5.12 - total capacity - current policy - BGD.xlsx', index = False)
df_totalcapacity_currentpolicy_devunfccc.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/5.13 - total capacity - current policy - DEVUNFCCC.xlsx', index = False)


# total capacity   - netzero
df_totalcapacity_netzero_deu.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/6.1 - total capacity - netzero - DEU.xlsx', index = False)
df_totalcapacity_netzero_idn.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/6.2 - total capacity - netzero - IDN.xlsx', index = False)
df_totalcapacity_netzero_ind.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/6.3 - total capacity - netzero - IND.xlsx', index = False)
df_totalcapacity_netzero_tur.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/6.4 - total capacity - netzero - TUR.xlsx', index = False)
df_totalcapacity_netzero_usa.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/6.5 - total capacity - netzero - USA.xlsx', index = False)
df_totalcapacity_netzero_vnm.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/6.6 - total capacity - netzero - VNM.xlsx', index = False)
df_totalcapacity_netzero_pol.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/6.7 - total capacity - netzero - POL.xlsx', index = False)
df_totalcapacity_netzero_kaz.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/6.8 - total capacity - netzero - KAZ.xlsx', index = False)
df_totalcapacity_netzero_emde.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/6.9 - total capacity - netzero - EMDE.xlsx', index = False)
df_totalcapacity_netzero_global.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/6.10 - total capacity - netzero - GLOBAL.xlsx', index = False)
df_totalcapacity_netzero_zaf.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/6.11 - total capacity - netzero - ZAF.xlsx', index = False)
df_totalcapacity_netzero_bgd.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/6.12 - total capacity - netzero - BGD.xlsx', index = False)
df_totalcapacity_netzero_devunfccc.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/6.13 - total capacity - netzero - DEVUNFCCC.xlsx', index = False)


# total capacity   - net zero 1.5C 50%
df_totalcapacity_nz1550v2_deu.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/7.1 - total capacity - net zero 15C 50% - DEU.xlsx', index = False)
df_totalcapacity_nz1550v2_idn.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/7.2 - total capacity - net zero 15C 50% - IDN.xlsx', index = False)
df_totalcapacity_nz1550v2_ind.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/7.3 - total capacity - net zero 15C 50% - IND.xlsx', index = False)
df_totalcapacity_nz1550v2_tur.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/7.4 - total capacity - net zero 15C 50% - TUR.xlsx', index = False)
df_totalcapacity_nz1550v2_usa.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/7.5 - total capacity - net zero 15C 50% - USA.xlsx', index = False)
df_totalcapacity_nz1550v2_vnm.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/7.6 - total capacity - net zero 15C 50% - VNM.xlsx', index = False)
df_totalcapacity_nz1550v2_pol.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/7.7 - total capacity - net zero 15C 50% - POL.xlsx', index = False)
df_totalcapacity_nz1550v2_kaz.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/7.8 - total capacity - net zero 15C 50% - KAZ.xlsx', index = False)
df_totalcapacity_nz1550v2_emde.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/7.9 - total capacity - net zero 15C 50% - EMDE.xlsx', index = False)
df_totalcapacity_nz1550v2_global.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/7.10 - total capacity - net zero 15C 50% - GLOBAL.xlsx', index = False)
df_totalcapacity_nz1550v2_zaf.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/7.11 - total capacity - net zero 15C 50% - ZAF.xlsx', index = False)
df_totalcapacity_nz1550v2_bgd.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/7.12 - total capacity - net zero 15C 50% - BGD.xlsx', index = False)
df_totalcapacity_nz1550v2_devunfccc.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/7.13 - total capacity - net zero 15C 50% - DEVUNFCCC.xlsx', index = False)


# --------------
# by fuel --- annual avoided
df_byfuel_avoided_annual_deu.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/8.1 - avoided capacity - annual - DEU.xlsx', index = False)
df_byfuel_avoided_annual_idn.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/8.2 - avoided capacity - annual - IDN.xlsx', index = False)
df_byfuel_avoided_annual_ind.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/8.3 - avoided capacity - annual - IND.xlsx', index = False)
df_byfuel_avoided_annual_tur.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/8.4 - avoided capacity - annual - TUR.xlsx', index = False)
df_byfuel_avoided_annual_usa.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/8.5 - avoided capacity - annual - USA.xlsx', index = False)
df_byfuel_avoided_annual_vnm.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/8.6 - avoided capacity - annual - VNM.xlsx', index = False)
df_byfuel_avoided_annual_pol.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/8.7 - avoided capacity - annual - POL.xlsx', index = False)
df_byfuel_avoided_annual_kaz.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/8.8 - avoided capacity - annual - KAZ.xlsx', index = False)
df_byfuel_avoided_annual_emde.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/8.9 - avoided capacity - annual - EMDE.xlsx', index = False)
df_byfuel_avoided_annual_global.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/8.10 - avoided capacity - annual - GLOBAL.xlsx', index = False)
df_byfuel_avoided_annual_zaf.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/8.11 - avoided capacity - annual - ZAF.xlsx', index = False)
df_byfuel_avoided_annual_bgd.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/8.12 - avoided capacity - annual - BGD.xlsx', index = False)
df_byfuel_avoided_annual_devunfccc.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/8.13 - avoided capacity - annual - DEVUNFCCC.xlsx', index = False)

# by fuel --- cumulative avoided
df_byfuel_avoided_cumulative_deu.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/9.1 - avoided capacity - cumulative - DEU.xlsx', index = False)
df_byfuel_avoided_cumulative_idn.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/9.2 - avoided capacity - cumulative - IDN.xlsx', index = False)
df_byfuel_avoided_cumulative_ind.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/9.3 - avoided capacity - cumulative - IND.xlsx', index = False)
df_byfuel_avoided_cumulative_tur.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/9.4 - avoided capacity - cumulative - TUR.xlsx', index = False)
df_byfuel_avoided_cumulative_usa.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/9.5 - avoided capacity - cumulative - USA.xlsx', index = False)
df_byfuel_avoided_cumulative_vnm.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/9.6 - avoided capacity - cumulative - VNM.xlsx', index = False)
df_byfuel_avoided_cumulative_pol.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/9.7 - avoided capacity - cumulative - POL.xlsx', index = False)
df_byfuel_avoided_cumulative_kaz.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/9.8 - avoided capacity - cumulative - KAZ.xlsx', index = False)
df_byfuel_avoided_cumulative_emde.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/9.9 - avoided capacity - cumulative - EMDE.xlsx', index = False)
df_byfuel_avoided_cumulative_global.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/9.10 - avoided capacity - cumulative - GLOBAL.xlsx', index = False)
df_byfuel_avoided_cumulative_zaf.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/9.11 - avoided capacity - cumulative - ZAF.xlsx', index = False)
df_byfuel_avoided_cumulative_bgd.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/9.12 - avoided capacity - cumulative - BGD.xlsx', index = False)
df_byfuel_avoided_cumulative_devunfccc.to_excel('2 - output/script 6.1 - Power sector - By country - Emissions & Capacity - Annual Cumulative Avoided/9.13 - avoided capacity - cumulative - DEVUNFCCC.xlsx', index = False)














