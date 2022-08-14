#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 13 13:16:24 2022

@author: jeremybenik
"""

# %% Importing necessary libraries
import matplotlib.pyplot as plt
import pandas as pd
# %% Reading in the data
df = pd.read_csv('/Users/jeremybenik/Research_Files/FireFlux_med/new_sounding_plotting.csv')

ht_old = df['ln_ht_old']
ht_new = df['ln_ht_new']

ws_old = df['ws_old']
ws_new = df['ws_new']

ws_adj = df['ws_adj']
fig, ax = plt.subplots(1, 3, figsize = (12, 10))

ax[0].plot(ws_old, ht_old, color = 'blue', label = 'Wind Speed')
ax[0].set_xlabel('Wind Speed (m/s)', fontsize = 12, fontweight = 'bold')
ax[0].set_ylabel('LN Height', fontsize = 12, fontweight = 'bold')
ax[0].set_title('Original Sounding', fontsize = 18, fontweight = 'bold')
ax[0].grid()

ax[1].plot(ws_new, ht_new, color = 'blue', label = 'Wind Speed')
ax[1].set_xlabel('Wind Speed (m/s)', fontsize = 12, fontweight = 'bold')
ax[1].set_ylabel('LN Height', fontsize = 12, fontweight = 'bold')
ax[1].set_title('New Sounding', fontsize = 18, fontweight = 'bold')
ax[1].grid()


ax[2].plot(ws_adj, ht_new, color = 'blue', label = 'Wind Speed')
ax[2].set_xlabel('Wind Speed (m/s)', fontsize = 12, fontweight = 'bold')
ax[2].set_ylabel('LN Height', fontsize = 12, fontweight = 'bold')
ax[2].set_title('Modified Winds Sounding', fontsize = 18, fontweight = 'bold')
ax[2].grid()