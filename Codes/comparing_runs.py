# The unmodified run has fiure_atms = 1, and the modified file (run_2) has the fire_atms = 0, and has cyclic boundary conditions
# %% Importing libraries
print("importing libraries")
import pandas as pd
import netCDF4 as nc
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import wrf
import statistics as st
import glob
import pickle
import os.path as osp
# %% Assigning a pickle file so I don't have to run this later
out_path = 'fireflux_med_case_new_runs.pkl'
if not osp.exists(out_path):
    # %% Reading in the files
    print('Reading in the files')
    unmod = nc.Dataset('/home/jbenik/fireflux_med/open_boundary_condition_run/wrfout_d01_2013-01-30_15:00:00') #open boundary conditions
    mod = nc.Dataset('/home/jbenik/fireflux_med/cyclic_boundary_conditions/wrfout_d01_2013-01-30_15:00:00') #cyclic boundary conditions
    # %% Reading in variables

    #Setting some values to get a graph of the wind at a certain point
    # main tower
    y_main = int(190/2)
    x_main = int(93/2)

    # East tower
    y_east = int(158/2)
    x_east = int(117/2)

    # West tower
    y_west = int(151/2)
    x_west = int(94/2)

    # South tower
    y_south = int(119/2)
    x_south = int(115/2)

    #Getting u, v, and height from open boundary conditions
    print('Getting u wind from open boundary conditions fireflux_med run')
    u_unmod = wrf.getvar(unmod, "ua", None, units = "m/s")
    print('Getting v wind from open boundary conditions fireflux_med run')
    v_unmod = wrf.getvar(unmod, "va", None, units = "m/s")
    print('Getting w wind from open boundary conditions fireflux_med run')
    w_unmod = wrf.getvar(unmod, "wa", None, units = "m/s")
    print('Getting height from open boundary conditions fireflux_med run')
    ht_unmod = wrf.getvar(unmod, "z", units="m", msl = False)
    
    # Getting u, v, and height from cyclic boundary conditions
    u_mod = wrf.getvar(mod, "ua", None, units = "m/s")
    print('Getting u wind from cyclic boundary conditions fireflux_med run')
    v_mod = wrf.getvar(mod, "va", None, units = "m/s")
    print('Getting v wind from cyclic boundary conditions fireflux_med run')
    w_mod = wrf.getvar(mod, "wa", None, units = "m/s")
    print('Getting height from cyclic boundary conditions fireflux_med run')
    ht_mod = wrf.getvar(mod, "z", units="m", msl = False)

    print('Getting time')
    time_unmod = unmod.variables['XTIME'][:]
    time_mod = mod.variables['XTIME'][:]

    print("Reading in the data")
    print("Main tower data")
    main_tower1 = pd.read_csv('/home/jbenik/FireFlux2/Codes_and_Data/Data/Main_Tower_Data/Proc_FF2_10HzMTdespiked_rotated.csv', parse_dates=['TIMESTAMP'], skiprows = (0, 2, 3))

    main_tower = main_tower1.truncate(before= np.where(main_tower1['TIMESTAMP'] == '1/30/2013  15:00:00')[0][0], 
                        after=np.where(main_tower1['TIMESTAMP'] == '1/30/2013  15:17:00')[0][0])
    # Main tower variables
    print("Getting the variables from the main tower data")
    time_main_tower = main_tower['TIMESTAMP']
    time2 = np.arange(240, 420.01, .1)

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

    # Short tower data
    df_w1 = pd.read_csv('/home/jbenik/FireFlux2/Codes_and_Data/Data/Short_Tower_Data/Proc_FF2_1HzSTWdespikedrotated.csv')

    df_w = df_w1.truncate(before= np.where(df_w1['TIMESTAMP'] == '1/30/2013 15:00')[0][0], 
                        after=np.where(df_w1['TIMESTAMP'] == '1/30/2013 15:16')[0][0])

    df_e1 = pd.read_csv('/home/jbenik/FireFlux2/Codes_and_Data/Data/Short_Tower_Data/Proc_FF2_1HzSTEdespikedrotated.csv')

    df_e = df_e1.truncate(before= np.where(df_e1['TIMESTAMP'] == '1/30/2013 15:00')[0][0], 
                        after=np.where(df_e1['TIMESTAMP'] == '1/30/2013 15:16')[0][0])

    df_s1 = pd.read_csv('/home/jbenik/FireFlux2/Codes_and_Data/Data/Short_Tower_Data/Proc_FF2_1HzSTSdespikedrotated.csv')

    df_s = df_s1.truncate(before= np.where(df_s1['TIMESTAMP'] == '1/30/2013 15:00')[0][0], 
                        after=np.where(df_s1['TIMESTAMP'] == '1/30/2013 15:16')[0][0])

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

    # Tower Data
    # 20 meters open boundary conditions
    print("Interpolating heights")
    print("Interpolating U at 20 meters")
    U_h_20_unmod = wrf.interplevel(u_unmod, ht_unmod, 20)[:, y_main, x_main] # Run this for all time
    #save everything in the results dictionary, then with that we can analyze it some more since we will have all the data. 
    print("Interpolating V at 20 meters")
    V_h_20_unmod = wrf.interplevel(v_unmod, ht_unmod, 20)[:, y_main, x_main]
    print("Calculating Wind Speed")
    ws_h_20_unmod = np.sqrt((U_h_20_unmod ** 2) + (V_h_20_unmod ** 2))
    print("Interpolating W at 20 meters")
    W_h_20_unmod = wrf.interplevel(w_unmod, ht_unmod, 20)[:, y_main, x_main]

    # 10 meters open boundary conditions
    print("Interpolating heights")
    print("Interpolating U at 10 meters")
    U_h_10_unmod = wrf.interplevel(u_unmod, ht_unmod, 10)[:, y_main, x_main] # Run this for all time
    #save everything in the results dictionary, then with that we can analyze it some more since we will have all the data. 
    print("Interpolating V at 10 meters")
    V_h_10_unmod = wrf.interplevel(v_unmod, ht_unmod, 10)[:, y_main, x_main]
    print("Calculating Wind Speed")
    ws_h_10_unmod = np.sqrt((U_h_10_unmod ** 2) + (V_h_10_unmod ** 2))
    print("Interpolating W at 10 meters")
    W_h_10_unmod = wrf.interplevel(w_unmod, ht_unmod, 10)[:, y_main, x_main]

    # 5.77 meters open boundary conditions
    print("Interpolating heights")
    print("Interpolating U at 577 meters")
    U_h_577_unmod = wrf.interplevel(u_unmod, ht_unmod, 5.77)[:, y_main, x_main] # Run this for all time
    #save everything in the results dictionary, then with that we can analyze it some more since we will have all the data. 
    print("Interpolating V at 577 meters")
    V_h_577_unmod = wrf.interplevel(v_unmod, ht_unmod, 5.77)[:, y_main, x_main]
    print("Calculating Wind Speed")
    ws_h_577_unmod = np.sqrt((U_h_577_unmod ** 2) + (V_h_577_unmod ** 2))
    print("Interpolating W at 577 meters")
    W_h_577_unmod = wrf.interplevel(w_unmod, ht_unmod, 5.77)[:, y_main, x_main]

    # 5.33 meters West Tower
    print("Interpolating heights")
    print("Interpolating U at 533 meters")
    West_U_h_533_unmod = wrf.interplevel(u_unmod, ht_unmod, 5.33)[:, y_west, x_west] # Run this for all time
    #save everything in the results dictionary, then with that we can analyze it some more since we will have all the data. 
    print("Interpolating V at 533 meters")
    West_V_h_533_unmod = wrf.interplevel(v_unmod, ht_unmod, 5.33)[:, y_west, x_west]
    print("Calculating Wind Speed")
    West_ws_h_533_unmod = np.sqrt((West_U_h_533_unmod ** 2) + (West_V_h_533_unmod ** 2))
    print("Interpolating W at 533 meters")
    West_W_h_533_unmod = wrf.interplevel(w_unmod, ht_unmod, 5.33)[:, y_west, x_west]
    print("Interpolating U at 533 meters")

    #5.33 meters South Tower
    print("Interpolating heights")
    print("Interpolating U at 533 meters")
    south_U_h_533_unmod = wrf.interplevel(u_unmod, ht_unmod, 5.33)[:, y_south, x_south] # Run this for all time
    #save everything in the results dictionary, then with that we can analyze it some more since we will have all the data. 
    print("Interpolating V at 533 meters")
    south_V_h_533_unmod = wrf.interplevel(v_unmod, ht_unmod, 5.33)[:, y_south, x_south]
    print("Calculating Wind Speed")
    south_ws_h_533_unmod = np.sqrt((south_U_h_533_unmod ** 2) + (south_V_h_533_unmod ** 2))
    print("Interpolating W at 533 meters")
    south_W_h_533_unmod = wrf.interplevel(w_unmod, ht_unmod, 5.33)[:, y_south, x_south]
    print("Interpolating U at 533 meters")

    #5.28 meters east Tower
    print("Interpolating heights")
    print("Interpolating U at 528 meters")
    east_U_h_528_unmod = wrf.interplevel(u_unmod, ht_unmod, 5.28)[:, y_east, x_east] # Run this for all time
    #save everything in the results dictionary, then with that we can analyze it some more since we will have all the data. 
    print("Interpolating V at 528 meters")
    east_V_h_528_unmod = wrf.interplevel(v_unmod, ht_unmod, 5.28)[:, y_east, x_east]
    print("Calculating Wind Speed")
    east_ws_h_528_unmod = np.sqrt((east_U_h_528_unmod ** 2) + (east_V_h_528_unmod ** 2))
    print("Interpolating W at 528 meters")
    east_W_h_528_unmod = wrf.interplevel(w_unmod, ht_unmod, 5.28)[:, y_east, x_east]
    print("Interpolating U at 528 meters")

    #this is for the modified case now
    # 20 meters
    print("Interpolating heights")
    print("Interpolating U at 20 meters")
    U_h_20_mod = wrf.interplevel(u_mod, ht_mod, 20)[:, y_main, x_main] # Run this for all time
    #save everything in the results dictionary, then with that we can analyze it some more since we will have all the data. 
    print("Interpolating V at 20 meters")
    V_h_20_mod = wrf.interplevel(v_mod, ht_mod, 20)[:, y_main, x_main]
    print("Calculating Wind Speed")
    ws_h_20_mod = np.sqrt((U_h_20_mod ** 2) + (V_h_20_mod ** 2))
    print("Interpolating W at 20 meters")
    W_h_20_mod = wrf.interplevel(w_mod, ht_mod, 20)[:, y_main, x_main]

    # 10 meters
    print("Interpolating heights")
    print("Interpolating U at 10 meters")
    U_h_10_mod = wrf.interplevel(u_mod, ht_mod, 10)[:, y_main, x_main] # Run this for all time
    #save everything in the results dictionary, then with that we can analyze it some more since we will have all the data. 
    print("Interpolating V at 10 meters")
    V_h_10_mod = wrf.interplevel(v_mod, ht_mod, 10)[:, y_main, x_main]
    print("Calculating Wind Speed")
    ws_h_10_mod = np.sqrt((U_h_10_mod ** 2) + (V_h_10_mod ** 2))
    print("Interpolating W at 10 meters")
    W_h_10_mod = wrf.interplevel(w_mod, ht_mod, 10)[:, y_main, x_main]

    # 5.77 meters
    print("Interpolating heights")
    print("Interpolating U at 577 meters")
    U_h_577_mod = wrf.interplevel(u_mod, ht_mod, 5.77)[:, y_main, x_main] # Run this for all time
    #save everything in the results dictionary, then with that we can analyze it some more since we will have all the data. 
    print("Interpolating V at 577 meters")
    V_h_577_mod = wrf.interplevel(v_mod, ht_mod, 5.77)[:, y_main, x_main]
    print("Calculating Wind Speed")
    ws_h_577_mod = np.sqrt((U_h_577_mod ** 2) + (V_h_577_mod ** 2))
    print("Interpolating W at 577 meters")
    W_h_577_mod = wrf.interplevel(w_mod, ht_mod, 5.77)[:, y_main, x_main] 
    print("Interpolating U at 577 meters")

    # 5.33 meters West Tower
    print("Interpolating heights")
    print("Interpolating U at 533 meters")
    West_U_h_533_mod = wrf.interplevel(u_mod, ht_mod, 5.33)[:, y_west, x_west] # Run this for all time
    #save everything in the results dictionary, then with that we can analyze it some more since we will have all the data. 
    print("Interpolating V at 533 meters")
    West_V_h_533_mod = wrf.interplevel(v_mod, ht_mod, 5.33)[:, y_west, x_west]
    print("Calculating Wind Speed")
    West_ws_h_533_mod = np.sqrt((West_U_h_533_mod ** 2) + (West_V_h_533_mod ** 2))
    print("Interpolating W at 533 meters")
    West_W_h_533_mod = wrf.interplevel(w_mod, ht_mod, 5.33)[:, y_west, x_west]
    print("Interpolating U at 533 meters")

    #5.33 meters South Tower
    print("Interpolating heights")
    print("Interpolating U at 533 meters")
    south_U_h_533_mod = wrf.interplevel(u_mod, ht_mod, 5.33)[:, y_south, x_south] # Run this for all time
    #save everything in the results dictionary, then with that we can analyze it some more since we will have all the data. 
    print("Interpolating V at 533 meters")
    south_V_h_533_mod = wrf.interplevel(v_mod, ht_mod, 5.33)[:, y_south, x_south]
    print("Calculating Wind Speed")
    south_ws_h_533_mod = np.sqrt((south_U_h_533_mod ** 2) + (south_V_h_533_mod ** 2))
    print("Interpolating W at 533 meters")
    south_W_h_533_mod = wrf.interplevel(w_mod, ht_mod, 5.33)[:, y_south, x_south]
    print("Interpolating U at 533 meters")

    #5.28 meters east Tower
    print("Interpolating heights")
    print("Interpolating U at 528 meters")
    east_U_h_528_mod = wrf.interplevel(u_mod, ht_mod, 5.28)[:, y_east, x_east] # Run this for all time
    #save everything in the results dictionary, then with that we can analyze it some more since we will have all the data. 
    print("Interpolating V at 528 meters")
    east_V_h_528_mod = wrf.interplevel(v_mod, ht_mod, 5.28)[:, y_east, x_east]
    print("Calculating Wind Speed")
    east_ws_h_528_mod = np.sqrt((east_U_h_528_mod ** 2) + (east_V_h_528_mod ** 2))
    print("Interpolating W at 528 meters")
    east_W_h_528_mod = wrf.interplevel(w_mod, ht_mod, 5.28)[:, y_east, x_east]

    time_main = main_tower['TIMESTAMP']
    time_short = np.arange(0, 720)
    results = {'time_unmod':time_unmod, 'time_mod':time_mod,
    'ws_h_20_mod':ws_h_20_mod, 'W_h_20_mod':W_h_20_mod,
    'ws_h_10_mod':ws_h_10_mod, 'W_h_10_mod':W_h_10_mod,
    'ws_h_577_mod':ws_h_577_mod, 'W_h_577_mod':W_h_577_mod,
    'West_ws_h_533_mod':West_ws_h_533_mod, 'West_W_h_533_mod':West_W_h_533_mod,
    'south_ws_h_533_mod':south_ws_h_533_mod, 'south_W_h_533_mod':south_W_h_533_mod,
    'east_ws_h_528_mod':east_ws_h_528_mod, 'east_W_h_528_mod':east_W_h_528_mod,
    'ws_h_20_unmod':ws_h_20_unmod, 'W_h_20_unmod':W_h_20_unmod,
    'ws_h_10_unmod':ws_h_10_unmod, 'W_h_10_unmod':W_h_10_unmod,
    'ws_h_577_unmod':ws_h_577_unmod, 'W_h_577_unmod':W_h_577_unmod,
    'West_ws_h_533_unmod':West_ws_h_533_unmod, 'West_W_h_533_unmod':West_W_h_533_unmod,
    'south_ws_h_533_unmod':south_ws_h_533_unmod, 'south_W_h_533_unmod':south_W_h_533_unmod,
    'east_ws_h_528_unmod':east_ws_h_528_unmod, 'east_W_h_528_unmod':east_W_h_528_unmod,
    'ws_20':ws_20, 'ws_10':ws_10,'ws_6':ws_6, 'uz20':uz20, 'uz10':uz10, 'uz6':uz6,
    'wsw':wsw, 'ww':ww, 'wss':wss, 'ws':ws, 'wse':wse, 'we':we,
    'time_main':time_main, 'time_short':time_short} #put the other variables in here such as wsw and ww

    with open(out_path, 'wb') as f:
        pickle.dump(results, f)
else:
    with open(out_path, 'rb') as f:
        results = pickle.load(f)
    locals().update(results)
# %% Creating the figure
#time_main = np.arange(0, 1020.10, .1)
fig, ax = plt.subplots(3, figsize = (12, 8))

# Main tower

#20 meters
ax[0].plot(time_mod * 60, ws_h_20_mod, label = 'Cyclic Boundary Conditions', color = 'blue')
ax[0].plot(time_unmod * 60, ws_h_20_unmod, label = 'Open Boundary Conditions', color = 'red')
ax[0].plot(time_main, ws_20, label = 'Observation Winds', color = 'green')
ax[0].set_xlabel('Time (Seconds)', fontsize =12, fontweight = 'bold')
ax[0].set_ylabel('Wind Speed (m/s)', fontsize = 12, fontweight = 'bold')
ax[0].set_title('20m Wind Speeds (Open and Cyclic Boundary Conditions', fontsize = 18, fontweight = 'bold')
ax[0].legend()
ax[0].grid()
# 10 meters
ax[1].plot(time_mod * 60, ws_h_10_mod, label = 'Cyclic Boundary Conditions', color = 'blue')
ax[1].plot(time_unmod * 60, ws_h_10_unmod, label = 'Open Boundary Conditions', color = 'red')
ax[1].plot(time_main, ws_10, label = 'Observation Winds', color = 'green')
ax[1].set_xlabel('Time (Seconds)', fontsize =12, fontweight = 'bold')
ax[1].set_ylabel('Wind Speed (m/s)', fontsize = 12, fontweight = 'bold')
ax[1].set_title('10m Wind Speeds (Open and Cyclic Boundary Conditions', fontsize = 18, fontweight = 'bold')
ax[1].legend()
ax[1].grid()
# 5.77 meters
ax[2].plot(time_mod * 60, ws_h_577_mod, label = 'Cyclic Boundary Conditions', color = 'blue')
ax[2].plot(time_unmod * 60, ws_h_577_unmod, label = 'Open Boundary Conditions', color = 'red')
ax[2].plot(time_main, ws_6, label = 'Observation Winds', color = 'green')
ax[2].set_xlabel('Time (Seconds)', fontsize =12, fontweight = 'bold')
ax[2].set_ylabel('Wind Speed (m/s)', fontsize = 12, fontweight = 'bold')
ax[2].set_title('5.77m Wind Speeds (Open and Cyclic Boundary Conditions', fontsize = 18, fontweight = 'bold')
ax[2].legend()
ax[2].grid()
plt.tight_layout()
plt.show()

# %% this is plotting the main tower without any observation winds
fig, ax = plt.subplots(3, figsize = (12, 8))

# Main tower

#20 meters
ax[0].plot(time_mod * 60, ws_h_20_mod, label = 'Cyclic Boundary Conditions', color = 'blue')
ax[0].plot(time_unmod * 60, ws_h_20_unmod, label = 'Open Boundary Conditions', color = 'red', linestyle = '--')
ax[0].set_xlabel('Time (Seconds)', fontsize =12, fontweight = 'bold')
ax[0].set_ylabel('Wind Speed (m/s)', fontsize = 12, fontweight = 'bold')
ax[0].set_title('20m Wind Speeds (Open and Cyclic Boundary Conditions)', fontsize = 18, fontweight = 'bold')
ax[0].legend()
ax[0].grid()
ax[0].set_xlim(0, 1000)
# 10 meters
ax[1].plot(time_mod * 60, ws_h_10_mod, label = 'Cyclic Boundary Conditions', color = 'blue')
ax[1].plot(time_unmod * 60, ws_h_10_unmod, label = 'Open Boundary Conditions', color = 'red', linestyle = '--')
ax[1].set_xlabel('Time (Seconds)', fontsize =12, fontweight = 'bold')
ax[1].set_ylabel('Wind Speed (m/s)', fontsize = 12, fontweight = 'bold')
ax[1].set_title('10m Wind Speeds (Open and Cyclic Boundary Conditions)', fontsize = 18, fontweight = 'bold')
ax[1].legend()
ax[1].grid()
ax[1].set_xlim(0, 1000)
# 5.77 meters
ax[2].plot(time_mod * 60, ws_h_577_mod, label = 'Cyclic Boundary Conditions', color = 'blue')
ax[2].plot(time_unmod * 60, ws_h_577_unmod, label = 'Open Boundary Conditions', color = 'red', linestyle = '--')
ax[2].set_xlabel('Time (Seconds)', fontsize =12, fontweight = 'bold')
ax[2].set_ylabel('Wind Speed (m/s)', fontsize = 12, fontweight = 'bold')
ax[2].set_title('5.77m Wind Speeds (Open and Cyclic Boundary Conditions)', fontsize = 18, fontweight = 'bold')
ax[2].legend()
ax[2].grid()
ax[2].set_xlim(0, 1000)
plt.tight_layout()
plt.show()
# %% Creating the figure
fig, ax = plt.subplots(3, figsize = (12, 8))

# Short tower

# West 5.33 meters
ax[0].plot(time_mod * 60, West_ws_h_533_mod, label = 'Cyclic Boundary Conditions', color = 'blue')
ax[0].plot(time_unmod * 60, West_ws_h_533_unmod, label = 'Open Boundary Conditions', color = 'red', linestyle = '--')
ax[0].set_xlabel('Time (Seconds)', fontsize =12, fontweight = 'bold')
ax[0].set_ylabel('Wind Speed (m/s)', fontsize = 12, fontweight = 'bold')
ax[0].set_title('West Tower Wind Speeds (Open and Cyclic Boundary Conditions', fontsize = 18, fontweight = 'bold')
ax[0].grid()
ax[0].legend()
# South 5.33 meters
ax[1].plot(time_mod * 60, south_ws_h_533_mod, label = 'Cyclic Boundary Conditions', color = 'blue')
ax[1].plot(time_unmod * 60, south_ws_h_533_unmod, label = 'Open Boundary Conditions', color = 'red', linestyle = '--')
ax[1].set_xlabel('Time (Seconds)', fontsize =12, fontweight = 'bold')
ax[1].set_ylabel('Wind Speed (m/s)', fontsize = 12, fontweight = 'bold')
ax[1].set_title('South Tower Wind Speeds (Open and Cyclic Boundary Conditions', fontsize = 18, fontweight = 'bold')
ax[1].grid()
ax[1].legend()
# east 5.28 meters
ax[2].plot(time_mod * 60, east_ws_h_528_mod, label = 'Cyclic Boundary Conditions', color = 'blue')
ax[2].plot(time_unmod * 60, east_ws_h_528_unmod, label = 'Open Boundary Conditions', color = 'red', linestyle = '--')
ax[2].set_xlabel('Time (Seconds)', fontsize =12, fontweight = 'bold')
ax[2].set_ylabel('Wind Speed (m/s)', fontsize = 12, fontweight = 'bold')
ax[2].set_title('East Tower Wind Speeds (Open and Cyclic Boundary Conditions', fontsize = 18, fontweight = 'bold')
ax[2].grid()
ax[2].legend()
plt.tight_layout()
plt.show()
# %%
