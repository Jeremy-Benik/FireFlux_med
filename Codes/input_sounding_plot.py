#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 16:08:08 2022

@author: jeremybenik
"""
# %% Importing necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# %% Reading in the data
df = pd.read_excel('/Users/jeremybenik/Desktop/fireflux_med_input_sounding.xlsx')
# %% Creating the plot
fig = plt.figure(figsize = (10, 12))
plt.plot(df['x'], df['ht'], color = 'blue')
plt.xlabel('Wind Speed (m/s)', fontsize = 12, fontweight = 'bold')
plt.ylabel('Height (m)', fontsize = 12, fontweight = 'bold')
plt.title('FireFlux_med input_sounding', fontsize = 18, fontweight = 'bold')
plt.legend()
plt.grid()
plt.show()