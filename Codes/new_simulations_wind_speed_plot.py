#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 16:31:45 2022

@author: jeremybenik
"""

# %% Importing necessary libraries
import netCDF4 as nc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import os.path as osp
import wrf
import statistics as st
<<<<<<< HEAD
# %% Reading in the files
file_1 = nc.Dataset('/home/jbenik/fireflux_med/simulations/Mod_SODAR_smoothed_out_input_sounding_9_7_22/wrfout_d01_2013-01-30_14:40:00')
file_2 = nc.Dataset('/home/jbenik/fireflux_med/simulations/Mod_SODAR_smoothed_out_input_sounding_9_7_22/wrfout_d01_2013-01-30_14:56:40')
file_3 = nc.Dataset('/home/jbenik/fireflux_med/simulations/Mod_SODAR_smoothed_out_input_sounding_9_7_22/wrfout_d01_2013-01-30_15:04:01')
#file_3 = nc.Dataset('/home/jbenik/fireflux_med/simulations/modified_heat_extinction_input_sounding/wrfout_d01_2013-01-30_15:13:01')
#file_4 = nc.Dataset('/home/jbenik/fireflux_med/simulations/modified_heat_extinction_input_sounding/wrfout_d01_2013-01-30_15:29:41')

# %% Importing the files
print('Running this here so I can get it all done in one run')
print('Getting u from the first wrfout file')
u_main_1 = wrf.getvar(file_1, "ua", None, units = "m/s")[:, :, :, :]
print('Getting u from the second wrfout file')
u_main_2 = wrf.getvar(file_2, "ua", None, units = "m/s")[:, :, :, :]
#print('Getting u from the third wrfout file')
u_main_3 = wrf.getvar(file_3, "ua", None, units = "m/s")[36::, :, :, :]
#print('Getting u from the fourth wrfout file')
#u_main_4 = wrf.getvar(file_4, "ua", None, units = "m/s")[:, :, :, :]

u_main = np.concatenate((u_main_1, u_main_2, u_main_3), axis = 0)
print('Reading in height from file 1')
ht_1 = wrf.getvar(file_1, "z", units="m", msl = False)[:, :, :]
print('Getting v from the first wrfout file')
v_main_1 = wrf.getvar(file_1, "va", None, units = "m/s")[:, :, :, :]
print('Getting v from the second wrfout file')
v_main_2 = wrf.getvar(file_2, "va", None, units = "m/s")[:, :, :, :]
print('Getting v from the third wrfout file')
v_main_3 = wrf.getvar(file_3, "va", None, units = "m/s")[36::, :, :, :]
# print('Getting v from the fourth wrfout file')
# v_main_4 = wrf.getvar(file_4, "va", None, units = "m/s")[:, :, :, :]
# print('Getting v from the fifth wrfout file')
v_main = np.concatenate((v_main_1, v_main_2, v_main_3), axis = 0)
# %%
y_main = int(190 / 2)
x_main = int(93 / 2)

# East tower
y_east = 158
x_east = 117

# West tower
y_west = 151
x_west = 94

# South tower
y_south = 119
x_south = 115
# %% Main Tower
out_path = 'pickle_files/main_tower_U_smoothed_sodar.pkl'
if not osp.exists(out_path):
    print('Interpolating U to 20m')
    U_h_20 = wrf.interplevel(u_main, ht_1, 20)[:, y_main, x_main]
    print('Interpolating U to 10m')
    U_h_10 = wrf.interplevel(u_main, ht_1, 10)[:, y_main, x_main]
    print('Interpolating U to 5.77m')
    U_h_577 = wrf.interplevel(u_main, ht_1, 5.77)[:, y_main, x_main]

    results = {'U_h_20':U_h_20, 'U_h_10':U_h_10, 'U_h_577':U_h_577}
    with open(out_path, 'wb') as f:
        pickle.dump(results, f)
else:
    with open(out_path, 'rb') as f:
        results = pickle.load(f)
    locals().update(results)

out_path = 'pickle_files/main_tower_V_smooth_sodar.pkl'
if not osp.exists(out_path):

    print('Interpolating V to 20m')
    V_h_20 = wrf.interplevel(v_main, ht_1, 20)[:, y_main, x_main]
    print('Interpolating V to 10m')
    V_h_10 = wrf.interplevel(v_main, ht_1, 10)[:, y_main, x_main]
    print('Interpolating V to 5.77m')
    V_h_577 = wrf.interplevel(v_main, ht_1, 5.77)[:, y_main, x_main]

    results = {'V_h_20':V_h_20, 'V_h_10':V_h_10, 'V_h_577':V_h_577}

    with open(out_path, 'wb') as f:
        pickle.dump(results, f)
else:
    with open(out_path, 'rb') as f:
        results = pickle.load(f)
    locals().update(results)
# %% West Tower
out_path = 'pickle_files/west_tower_U_smoothed_sodar.pkl'
if not osp.exists(out_path):
    print('Interpolating U to 5.33m')
    U_h_533_West = wrf.interplevel(u_main, ht_1, 5.33)[:, y_west, x_west]


    results = {'U_h_533_West':U_h_533_West}
    with open(out_path, 'wb') as f:
        pickle.dump(results, f)
else:
    with open(out_path, 'rb') as f:
        results = pickle.load(f)
    locals().update(results)

out_path = 'pickle_files/west_tower_V_smoothed_sodar.pkl'
if not osp.exists(out_path):
    print('Interpolating V to 5.33m')
    V_h_533_West = wrf.interplevel(v_main, ht_1, 5.33)[:, y_west, x_west]


    results = {'V_h_533_West':V_h_533_West}
    with open(out_path, 'wb') as f:
        pickle.dump(results, f)
else:
    with open(out_path, 'rb') as f:
        results = pickle.load(f)
    locals().update(results)

# %% South
out_path = 'pickle_files/south_tower_U_smoothed_sodar.pkl'
if not osp.exists(out_path):
    print('Interpolating U to 5.33m')
    U_h_533_south = wrf.interplevel(u_main, ht_1, 5.33)[:, y_south, x_south]


    results = {'U_h_533_south':U_h_533_south}
    with open(out_path, 'wb') as f:
        pickle.dump(results, f)
else:
    with open(out_path, 'rb') as f:
        results = pickle.load(f)
    locals().update(results)

out_path = 'pickle_files/south_tower_V_smoothed_sodar.pkl'
if not osp.exists(out_path):
    print('Interpolating V to 5.33m')
    V_h_533_south = wrf.interplevel(v_main, ht_1, 5.33)[:, y_south, x_south]


    results = {'V_h_533_south':V_h_533_south}
    with open(out_path, 'wb') as f:
        pickle.dump(results, f)
else:
    with open(out_path, 'rb') as f:
        results = pickle.load(f)
    locals().update(results)
# %% East
out_path = 'pickle_files/east_tower_U_smoothed_sodar.pkl'
if not osp.exists(out_path):
    print('Interpolating U to 5.33m')
    U_h_528_east = wrf.interplevel(u_main, ht_1, 5.28)[:, y_east, x_east]


    results = {'U_h_528_east':U_h_528_east}
    with open(out_path, 'wb') as f:
        pickle.dump(results, f)
else:
    with open(out_path, 'rb') as f:
        results = pickle.load(f)
    locals().update(results)

out_path = 'pickle_files/east_tower_V_smoothed_sodar.pkl'
if not osp.exists(out_path):
    print('Interpolating V to 5.33m')
    V_h_528_east = wrf.interplevel(v_main, ht_1, 5.28)[:, y_east, x_east]


    results = {'V_h_528_east':V_h_528_east}
    with open(out_path, 'wb') as f:
        pickle.dump(results, f)
else:
    with open(out_path, 'rb') as f:
        results = pickle.load(f)
    locals().update(results)

# %% time
out_path = 'pickle_files/time_smooth_sodar.pkl'
if not osp.exists(out_path):

    time_1 = file_1.variables['XTIME'][:]
    time_2 = file_2.variables['XTIME'][:]
    time_3 = file_3.variables['XTIME'][36::]
    #time_4 = file_4.variables['XTIME'][:]

    time_sim = np.concatenate((time_1, time_2, time_3), axis = 0)
    results = {'time_sim':time_sim}

    with open(out_path, 'wb') as f:
        pickle.dump(results, f)
else:
    with open(out_path, 'rb') as f:
        results = pickle.load(f)
    locals().update(results)

# %% Calculating wind speed
ws_h_20 = np.sqrt((U_h_20 ** 2) + (V_h_20 ** 2))
ws_h_10 = np.sqrt((U_h_10 ** 2) + (V_h_10 ** 2))
ws_h_577 = np.sqrt((U_h_577 ** 2) + (V_h_577 ** 2))
ws_h_533_west = np.sqrt((U_h_533_West ** 2) + (V_h_533_West ** 2))
ws_h_533_south = np.sqrt((U_h_533_south ** 2) + (V_h_533_south ** 2))
ws_h_528_east = np.sqrt((U_h_528_east ** 2) + (V_h_528_east ** 2))
=======
import glob
# %% test case
path = 'pickle_files/10_10_simulation/'
files = glob.iglob(path + '*.pkl', recursive= True)
for x in files:
    with open(x, 'rb') as f:
        results = pickle.load(f)
    locals().update(results) 
ws_h_20 = np.sqrt((U_h_20 ** 2) + (V_h_20 ** 2))
ws_h_10 = np.sqrt((U_h_10 ** 2) + (V_h_10 ** 2))
ws_h_577 = np.sqrt((U_h_577 ** 2) + (V_h_577 ** 2))
ws_east = np.sqrt((U_east_528 ** 2) + (V_east_528 ** 2))
ws_south = np.sqrt((U_south_533 ** 2) + (V_south_533 ** 2))
ws_west = np.sqrt((U_west_533 ** 2) + (V_west_533 ** 2))
        
# %% 0.1z0
path = 'pickle_files/10_06_22_01_z0_9ms/'
files = glob.iglob(path + '*.pkl', recursive= True)
for x in files:
    with open(x, 'rb') as f:
        results = pickle.load(f)
    locals().update(results)
ws_h_20 = np.sqrt((U_h_20 ** 2) + (V_h_20 ** 2))
ws_h_10 = np.sqrt((U_h_10 ** 2) + (V_h_10 ** 2))
ws_h_577 = np.sqrt((U_h_577 ** 2) + (V_h_577 ** 2))
ws_east = np.sqrt((U_east_528 ** 2) + (V_east_528 ** 2))
ws_south = np.sqrt((U_south_533 ** 2) + (V_south_533 ** 2))
ws_west = np.sqrt((U_west_533 ** 2) + (V_west_533 ** 2))
# %% 0.1z0 base winds
path = 'pickle_files/10_06_22_01z0_base_winds/'
files = glob.iglob(path + '*.pkl', recursive= True)
for x in files:
    with open(x, 'rb') as f:
        results = pickle.load(f)
    locals().update(results)
ws_h_20 = np.sqrt((U_h_20 ** 2) + (V_h_20 ** 2))
ws_h_10 = np.sqrt((U_h_10 ** 2) + (V_h_10 ** 2))
ws_h_577 = np.sqrt((U_h_577 ** 2) + (V_h_577 ** 2))
ws_east = np.sqrt((U_east_528 ** 2) + (V_east_528 ** 2))
ws_south = np.sqrt((U_south_533 ** 2) + (V_south_533 ** 2))
ws_west = np.sqrt((U_west_533 ** 2) + (V_west_533 ** 2))
# %% 10_06_run

path = 'pickle_files/10_06_22_sim_attempt_to_match_obs_mod_sounding_1/'
files = glob.iglob(path + '*.pkl', recursive= True)
for x in files:
    with open(x, 'rb') as f:
        results = pickle.load(f)
    locals().update(results)
ws_h_20 = np.sqrt((U_h_20 ** 2) + (V_h_20 ** 2))
ws_h_10 = np.sqrt((U_h_10 ** 2) + (V_h_10 ** 2))
ws_h_577 = np.sqrt((U_h_577 ** 2) + (V_h_577 ** 2))
ws_east = np.sqrt((U_east_528 ** 2) + (V_east_528 ** 2))
ws_south = np.sqrt((U_south_533 ** 2) + (V_south_533 ** 2))
ws_west = np.sqrt((U_west_533 ** 2) + (V_west_533 ** 2))
# %% 10_05 run
path = 'pickle_files/10_05_22_sim_attempt_to_match_obs_mod_sounding_1/'
files = glob.iglob(path + '*.pkl', recursive= True)
for x in files:
    with open(x, 'rb') as f:
        results = pickle.load(f)
    locals().update(results)
ws_h_20 = np.sqrt((U_h_20 ** 2) + (V_h_20 ** 2))
ws_h_10 = np.sqrt((U_h_10 ** 2) + (V_h_10 ** 2))
ws_h_577 = np.sqrt((U_h_577 ** 2) + (V_h_577 ** 2))
ws_east = np.sqrt((U_east_528 ** 2) + (V_east_528 ** 2))
ws_south = np.sqrt((U_south_533 ** 2) + (V_south_533 ** 2))
ws_west = np.sqrt((U_west_533 ** 2) + (V_west_533 ** 2))
# %% 10_04 run
path = 'pickle_files/10_04_22_sim_attempt_to_match_obs_mod_sounding_1/'
files = glob.iglob(path + '*.pkl', recursive= True)
for x in files:
    with open(x, 'rb') as f:
        results = pickle.load(f)
    locals().update(results)
ws_h_20 = np.sqrt((U_h_20 ** 2) + (V_h_20 ** 2))
ws_h_10 = np.sqrt((U_h_10 ** 2) + (V_h_10 ** 2))
ws_h_577 = np.sqrt((U_h_577 ** 2) + (V_h_577 ** 2))
ws_east = np.sqrt((U_east_528 ** 2) + (V_east_528 ** 2))
ws_south = np.sqrt((U_south_533 ** 2) + (V_south_533 ** 2))
ws_west = np.sqrt((U_west_533 ** 2) + (V_west_533 ** 2))
# %% 10_05 run
path = 'pickle_files/10_05_22_sim_attempt_to_match_obs_mod_sounding_1/'
files = glob.iglob(path + '*.pkl', recursive= True)
for x in files:
    with open(x, 'rb') as f:
        results = pickle.load(f)
    locals().update(results)
ws_h_20 = np.sqrt((U_h_20 ** 2) + (V_h_20 ** 2))
ws_h_10 = np.sqrt((U_h_10 ** 2) + (V_h_10 ** 2))
ws_h_577 = np.sqrt((U_h_577 ** 2) + (V_h_577 ** 2))
ws_east = np.sqrt((U_east_528 ** 2) + (V_east_528 ** 2))
ws_south = np.sqrt((U_south_533 ** 2) + (V_south_533 ** 2))
ws_west = np.sqrt((U_west_533 ** 2) + (V_west_533 ** 2))
# %% modified Sounding
path = 'pickle_files/modified_sounding_pickle_files/'
files = glob.iglob(path + '*.pkl', recursive= True)
for x in files:
    with open(x, 'rb') as f:
        results = pickle.load(f)
    locals().update(results)
ws_h_20 = np.sqrt((U_h_20 ** 2) + (V_h_20 ** 2))
ws_h_10 = np.sqrt((U_h_10 ** 2) + (V_h_10 ** 2))
ws_h_577 = np.sqrt((U_h_577 ** 2) + (V_h_577 ** 2))
ws_east = np.sqrt((U_east_528 ** 2) + (V_east_528 ** 2))
ws_south = np.sqrt((U_south_533 ** 2) + (V_south_533 ** 2))
ws_west = np.sqrt((U_west_533 ** 2) + (V_west_533 ** 2))

# %% unmodified Sounding
path = 'pickle_files/modified_sounding_pickle_files/'

files = glob.iglob(path + '*.pkl', recursive= True)
for x in files:
    with open(x, 'rb') as f:
        results = pickle.load(f)
    locals().update(results)
ws_h_20 = np.sqrt((U_h_20 ** 2) + (V_h_20 ** 2))
ws_h_10 = np.sqrt((U_h_10 ** 2) + (V_h_10 ** 2))
ws_h_577 = np.sqrt((U_h_577 ** 2) + (V_h_577 ** 2))
ws_east = np.sqrt((U_east_528 ** 2) + (V_east_528 ** 2))
ws_south = np.sqrt((U_south_533 ** 2) + (V_south_533 ** 2))
ws_west = np.sqrt((U_west_533 ** 2) + (V_west_533 ** 2))

# %% modified Sounding match ff2_sim
path = 'pickle_files/modified_sounding_pickle_files/'
files = glob.iglob(path + '*.pkl', recursive= True)
for x in files:
    with open(x, 'rb') as f:
        results = pickle.load(f)
    locals().update(results)
ws_h_20 = np.sqrt((U_h_20 ** 2) + (V_h_20 ** 2))
ws_h_10 = np.sqrt((U_h_10 ** 2) + (V_h_10 ** 2))
ws_h_577 = np.sqrt((U_h_577 ** 2) + (V_h_577 ** 2))
ws_east = np.sqrt((U_east_528 ** 2) + (V_east_528 ** 2))
ws_south = np.sqrt((U_south_533 ** 2) + (V_south_533 ** 2))
ws_west = np.sqrt((U_west_533 ** 2) + (V_west_533 ** 2))
# %% 10_07 run
path = 'pickle_files/10_07_pickle_files/'
files = glob.iglob(path + '*.pkl', recursive= True)
for x in files:
    #print(x)
    with open(x, 'rb') as f:
        results = pickle.load(f)
    locals().update(results)
ws_h_20 = np.sqrt((U_h_20 ** 2) + (V_h_20 ** 2))
ws_h_10 = np.sqrt((U_h_10 ** 2) + (V_h_10 ** 2))
ws_h_577 = np.sqrt((U_h_577 ** 2) + (V_h_577 ** 2))
ws_east = np.sqrt((U_east_528 ** 2) + (V_east_528 ** 2))
ws_south = np.sqrt((U_south_533 ** 2) + (V_south_533 ** 2))
ws_west = np.sqrt((U_west_533 ** 2) + (V_west_533 ** 2))
ws_h_20 = np.sqrt((U_h_20 ** 2) + (V_h_20 ** 2))
ws_h_10 = np.sqrt((U_h_10 ** 2) + (V_h_10 ** 2))
ws_h_577 = np.sqrt((U_h_577 ** 2) + (V_h_577 ** 2))
ws_east = np.sqrt((U_east_528 ** 2) + (V_east_528 ** 2))
ws_south = np.sqrt((U_south_533 ** 2) + (V_south_533 ** 2))
ws_west = np.sqrt((U_west_533 ** 2) + (V_west_533 ** 2))

# %% 10 10 simulation
path = 'pickle_files/10_10_simulation/'
files = glob.iglob(path + '*.pkl', recursive= True)
for x in files:
   # print(x)
    with open(x, 'rb') as f:
        results = pickle.load(f)
    locals().update(results)
ws_h_20 = np.sqrt((U_h_20 ** 2) + (V_h_20 ** 2))
ws_h_10 = np.sqrt((U_h_10 ** 2) + (V_h_10 ** 2))
ws_h_577 = np.sqrt((U_h_577 ** 2) + (V_h_577 ** 2))
ws_east = np.sqrt((U_east_528 ** 2) + (V_east_528 ** 2))
ws_south = np.sqrt((U_south_533 ** 2) + (V_south_533 ** 2))
ws_west = np.sqrt((U_west_533 ** 2) + (V_west_533 ** 2))
# %% 10 10 simulation
path = 'pickle_files/10_11_simulation/'
files = glob.iglob(path + '*.pkl', recursive= True)
for x in files:
   # print(x)
    with open(x, 'rb') as f:
        results = pickle.load(f)
    locals().update(results)
ws_h_20 = np.sqrt((U_h_20 ** 2) + (V_h_20 ** 2))
ws_h_10 = np.sqrt((U_h_10 ** 2) + (V_h_10 ** 2))
ws_h_577 = np.sqrt((U_h_577 ** 2) + (V_h_577 ** 2))
ws_east = np.sqrt((U_east_528 ** 2) + (V_east_528 ** 2))
ws_south = np.sqrt((U_south_533 ** 2) + (V_south_533 ** 2))
ws_west = np.sqrt((U_west_533 ** 2) + (V_west_533 ** 2))
>>>>>>> ember_files
# %% Creating the plots
main_tower1 = pd.read_csv('/home/jbenik/FireFlux2/Codes_and_Data/Data/Main_Tower_Data/Proc_FF2_10HzMTdespiked_rotated.csv', parse_dates=['TIMESTAMP'], skiprows = (0, 2, 3))

main_tower = main_tower1.truncate(before= np.where(main_tower1['TIMESTAMP'] == '1/30/2013  15:00:00')[0][0], 
                    after=np.where(main_tower1['TIMESTAMP'] == '1/30/2013  15:30:00')[0][0])
# Main tower variables
print("Getting the variables from the main tower data")
time_main_tower = main_tower['TIMESTAMP']
time_main = np.arange(600, 2400.1, .1)
print('20 meter variables')
ux20 = main_tower['Ux_20m']
uy20 = main_tower['Uy_20m']
ws_20 = np.sqrt((ux20 ** 2) + (uy20 ** 2))
uz20 = main_tower['Uz_20m']
ts20 = main_tower['Ts_20m']

print('10 meter variables')
ux10 = main_tower['Ux_10m']
uy10 = main_tower['Uy_10m']
ws_10 = np.sqrt((ux10 ** 2) + (uy10 ** 2))
uz10 = main_tower['Uz_10m']
ts10 = main_tower['Ts_10m']

print('5.77 meter variable')
ux6 = main_tower['Ux_6m']
uy6 = main_tower['Uy_6m']
ws_6 = np.sqrt((ux6 ** 2) + (uy6 ** 2))
uz6 = main_tower['Uz_6m']
ts6 = main_tower['Ts_6m']

df_w1 = pd.read_csv('/home/jbenik/FireFlux2/Codes_and_Data/Data/Short_Tower_Data/Proc_FF2_1HzSTWdespikedrotated.csv')

<<<<<<< HEAD
# %% Plotting
fig, ax = plt.subplots(3, figsize = (12,10))
n = 600

=======
df_w = df_w1.truncate(before= np.where(df_w1['TIMESTAMP'] == '1/30/2013 15:00')[0][0], 
                    after=np.where(df_w1['TIMESTAMP'] == '1/30/2013 15:30')[0][0])

df_e1 = pd.read_csv('/home/jbenik/FireFlux2/Codes_and_Data/Data/Short_Tower_Data/Proc_FF2_1HzSTEdespikedrotated.csv')

df_e = df_e1.truncate(before= np.where(df_e1['TIMESTAMP'] == '1/30/2013 15:00')[0][0], 
                    after=np.where(df_e1['TIMESTAMP'] == '1/30/2013 15:30')[0][0])

df_s1 = pd.read_csv('/home/jbenik/FireFlux2/Codes_and_Data/Data/Short_Tower_Data/Proc_FF2_1HzSTSdespikedrotated.csv')

df_s = df_s1.truncate(before= np.where(df_s1['TIMESTAMP'] == '1/30/2013 15:00')[0][0], 
                    after=np.where(df_s1['TIMESTAMP'] == '1/30/2013 15:30')[0][0])

# defining vars

#west tower
print("Reading variables from west tower")
time_short_tower_w = df_w['TIMESTAMP']
uw = df_w['u']
vw = df_w['v']
ww = df_w['w']
tw = df_w['t']
wsw = np.sqrt((uw ** 2) + (vw ** 2))
#east tower
print("Reading in variables from east tower")
time_short_tower_e = df_e['TIMESTAMP']
ue = df_e['u']
ve = df_e['v']
we = df_e['w']
te = df_e['t']
wse = np.sqrt((ue ** 2) + (ve ** 2))
#south tower
print("reading in variables from south tower")
time_short_tower_s = df_s['TIMESTAMP']
us = df_s['u']
vs = df_s['v']
ws = df_s['w']
ts = df_s['t']
wss = np.sqrt((us ** 2) + (vs ** 2))

short_tower_time = np.arange(600, 2400)

# %% Plotting
fig, ax = plt.subplots(3, figsize = (12,10))
n = 600
plt.suptitle('10_11 0.3z0 run more levels', fontsize = 10, fontweight = 'bold')
>>>>>>> ember_files
# 5.33 Meter plot
#plt.suptitle('Simulated Main Tower Winds From Open Boundary Fire Run', fontsize = 18, fontweight = 'bold')
#ax[0].plot(time_main, ws_20, color = 'green', label = 'Main Tower Winds')
ax[0].plot(time_main, ws_20.rolling(window = n).mean(), color = 'green', label = '1m Avg. Main Tower Winds')
ax[0].plot(time_sim * 60, ws_h_20, color = 'red', label = 'Simulated Winds')
ax[0].axvline(x = 848, color = 'black', label = 'Ignition')
ax[0].set_ylabel('Wind Speeds (m/s)', fontsize = 12, fontweight = 'bold')
ax[0].set_title('Simulated Winds at 20m', fontsize = 18, fontweight = 'bold')
ax[0].set_xlabel('Time (S)', fontsize = 12, fontweight = 'bold')
#ax[0].set_xlim(800, 1500)
ax[0].legend()
ax[0].grid()
#ax[0].set_xlim(1150, 1400)

#ax[1].plot(time_main, ws_10, color = 'green', label = 'Main Tower Winds')
ax[1].plot(time_main, ws_10.rolling(window = n).mean(), color = 'green', label = '1m Avg. Main Tower Winds')
ax[1].plot(time_sim * 60, ws_h_10, color = 'red', label = 'Simulated Winds')
ax[1].axvline(x = 848, color = 'black', label = 'Ignition')
ax[1].set_ylabel('Wind Speeds (m/s)', fontsize = 12, fontweight = 'bold')
ax[1].set_title('Simulated Winds at 10m', fontsize = 18, fontweight = 'bold')
ax[1].set_xlabel('Time (S)', fontsize = 12, fontweight = 'bold')
#ax[1].set_xlim(800, 1500)
ax[1].legend()
ax[1].grid()
# ax[1].set_xlim(1150, 1400)

ax[2].plot(time_main, ws_6.rolling(window = n).mean(), color = 'green', label = '1m Avg. Main Tower Winds')
#ax[2].plot(time_main, ws_6, color = 'green', label = 'Main Tower Winds')
ax[2].plot(time_sim * 60, ws_h_577, color = 'red', label = 'Simulated Winds')
ax[2].axvline(x = 848, color = 'black', label = 'Ignition')
ax[2].set_ylabel('Wind Speeds (m/s)', fontsize = 12, fontweight = 'bold')
ax[2].set_title('Simulated Winds at 5.77m', fontsize = 18, fontweight = 'bold')
ax[2].set_xlabel('Time (S)', fontsize = 12, fontweight = 'bold')
#ax[2].set_xlim(800, 1500)
ax[2].legend()
ax[2].grid()
# ax[2].set_xlim(1150, 1400)
<<<<<<< HEAD
=======

plt.tight_layout()
#plt.savefig('/home/jbenik/fireflux_med/images/u_and_v_cyclic_no_fire.png')
plt.show()

# %% Short towers
fig, ax = plt.subplots(3, figsize = (12,10))
n = 60
plt.suptitle('10_06 0.2z0 run', fontsize = 10, fontweight = 'bold')
# 5.33 Meter plot
#plt.suptitle('Simulated Main Tower Winds From Open Boundary Fire Run', fontsize = 18, fontweight = 'bold')
#ax[0].plot(time_main, ws_20, color = 'green', label = 'Main Tower Winds')
ax[0].plot(short_tower_time, wsw[0:1800].rolling(window = n).mean(), color = 'green', label = '1m Avg. West Tower Winds')
ax[0].plot(time_sim * 60, ws_west, color = 'red', label = 'Simulated Winds')
ax[0].axvline(x = 848, color = 'black', label = 'Ignition')
ax[0].set_ylabel('Wind Speeds (m/s)', fontsize = 12, fontweight = 'bold')
ax[0].set_title('Simulated Winds at West Tower', fontsize = 18, fontweight = 'bold')
ax[0].set_xlabel('Time (S)', fontsize = 12, fontweight = 'bold')
#ax[0].set_xlim(800, 1500)
ax[0].legend()
ax[0].grid()
#ax[0].set_xlim(1150, 1400)

#ax[1].plot(time_main, ws_10, color = 'green', label = 'Main Tower Winds')
ax[1].plot(short_tower_time[0:1751], wss.rolling(window = n).mean(), color = 'green', label = '1m Avg. South Tower Winds')
ax[1].plot(time_sim * 60, ws_south, color = 'red', label = 'Simulated Winds')
ax[1].axvline(x = 848, color = 'black', label = 'Ignition')
ax[1].set_ylabel('Wind Speeds (m/s)', fontsize = 12, fontweight = 'bold')
ax[1].set_title('Simulated Winds at South Tower', fontsize = 18, fontweight = 'bold')
ax[1].set_xlabel('Time (S)', fontsize = 12, fontweight = 'bold')
#ax[1].set_xlim(800, 1500)
ax[1].legend()
ax[1].grid()
# ax[1].set_xlim(1150, 1400)

ax[2].plot(short_tower_time, wse.rolling(window = n).mean(), color = 'green', label = '1m Avg. East Tower Winds')
#ax[2].plot(time_main, ws_6, color = 'green', label = 'Main Tower Winds')
ax[2].plot(time_sim * 60, ws_east, color = 'red', label = 'Simulated Winds')
ax[2].axvline(x = 848, color = 'black', label = 'Ignition')
ax[2].set_ylabel('Wind Speeds (m/s)', fontsize = 12, fontweight = 'bold')
ax[2].set_title('Simulated Winds at East Tower', fontsize = 18, fontweight = 'bold')
ax[2].set_xlabel('Time (S)', fontsize = 12, fontweight = 'bold')
#ax[2].set_xlim(800, 1500)
ax[2].legend()
ax[2].grid()
# ax[2].set_xlim(1150, 1400)
>>>>>>> ember_files

plt.tight_layout()
#plt.savefig('/home/jbenik/fireflux_med/images/u_and_v_cyclic_no_fire.png')
plt.show()