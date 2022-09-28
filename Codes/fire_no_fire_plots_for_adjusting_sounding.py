# %% Importing necessary libraries
print('Importing necessary libraries')
import netCDF4 as nc
import pandas as pd
import matplotlib.pyplot as plt
import wrf
import numpy as np
import pickle
import os.path as osp
# %% It looks like interpolating height doesn't work, so to get the height, I will input a value manually
'''Here are the indices I can use
0:0
1:2.6736931800842285, 
2:5.1978759765625,
3:7.557523727416992, 
4:10.023331642150879,
5:12.606412887573242, 
6:15.322469711303711,
7:18.178232192993164, 
8:21.18073844909668,
9:24.336769104003906, 
10:27.653553009033203,
11:31.13888168334961, 
12:34.80120086669922,
13:38.648963928222656, 
14:42.691436767578125,
15:46.93775177001953, 
16:51.39803695678711,
17:56.08224868774414, 
18:61.00136184692383,
...
'''
# %% Reading in all the files
#Structure
# Fire_atms = 1
# Fire_atms = 0
out_path = 'fireflux_med_sounding_vars_1.pkl'
if not osp.exists(out_path):
    # Reading in the files
    print('Reading in the files')
    open_fire = nc.Dataset('/home/jbenik/fireflux_med/fire_atms_1/open/ff_med_wrfout_open_fire_atms_1')
    cyclic_fire = nc.Dataset('/home/jbenik/fireflux_med/fire_atms_1/cyclic/ff_med_wrfout_cyclic_fire_atms_1')
    # Open and cyclic for fire_atms = 0
    open_no_fire = nc.Dataset('/home/jbenik/fireflux_med/fire_atms_0/open_boundary_conditions/ff_med_wrfout_fire_atms_0')
    cyclic_no_fire = nc.Dataset('/home/jbenik/fireflux_med/fire_atms_0/cyclic_boundary_conditions/wrfout_merged')
    # Reading in variables
    print('Reading in time')
    time_open_fire = open_fire.variables['XTIME'][:]
    time_cyclic_fire = cyclic_fire.variables['XTIME'][:]
    time_open_no_fire = open_no_fire.variables['XTIME'][:]
    time_cyclic_no_fire = cyclic_no_fire.variables['XTIME'][:]

    #Setting some values to get a graph of the wind at a certain point
    # main tower
    y_main = int(190/2)
    x_main = int(93/2)
    
    print('Getting variables from fire runs')
    #Getting u, v, and height from open boundary conditions with fire
    print('Getting u wind from open boundary conditions fireflux_med run')
    u_open_fire = wrf.getvar(open_fire, "ua", None, units = "m/s")
    print('Getting v wind from open boundary conditions fireflux_med run')
    v_open_fire = wrf.getvar(open_fire, "va", None, units = "m/s")
    print('Getting w wind from open boundary conditions fireflux_med run')
    #w_open_fire = wrf.getvar(open_fire, "wa", None, units = "m/s")
    print('Getting height from open boundary conditions fireflux_med run')
    ht_open_fire = wrf.getvar(open_fire, "z", units="m", msl = False)[:, y_main, x_main]
    print('Getting time')
    time_open_fire = open_fire.variables['XTIME'][:]

    #Getting u, v, and height from cyclic boundary conditions with fire
    print('Getting u wind from cyclic boundary conditions fireflux_med run')
    u_cyclic_fire = wrf.getvar(cyclic_fire, "ua", None, units = "m/s")[:, :, y_main, x_main]
    print('Getting v wind from cyclic boundary conditions fireflux_med run')
    v_cyclic_fire = wrf.getvar(cyclic_fire, "va", None, units = "m/s")[:, :, y_main, x_main]
    print('Getting w wind from cyclic boundary conditions fireflux_med run')
    #w_cyclic_fire = wrf.getvar(cyclic_fire, "wa", None, units = "m/s")[:, :, y_main, x_main]
    print('Getting height from cyclic boundary conditions fireflux_med run')
    ht_cyclic_fire = wrf.getvar(cyclic_fire, "z", units="m", msl = False)[:, y_main, x_main]
    time_cyclic_fire = cyclic_fire.variables['XTIME'][:]

    print('Getting variables from no fire runs')
    #Getting u, v, and height from open boundary conditions with fire
    print('Getting u wind from open boundary conditions fireflux_med run')
    u_open_no_fire = wrf.getvar(open_no_fire, "ua", None, units = "m/s")[:, :, y_main, x_main]
    print('Getting v wind from open boundary conditions fireflux_med run')
    v_open_no_fire = wrf.getvar(open_no_fire, "va", None, units = "m/s")[:, :, y_main, x_main]
    print('Getting w wind from open boundary conditions fireflux_med run')
    #w_open_no_fire = wrf.getvar(open_no_fire, "wa", None, units = "m/s")[:, :, y_main, x_main]
    print('Getting height from open boundary conditions fireflux_med run')
    #ht_open_no_fire = wrf.getvar(open_no_fire, "z", units="m", msl = False)[:, y_main, x_main]
    time_open_no_fire = open_no_fire.variables['XTIME'][:]
    
    #Getting u, v, and height from cyclic boundary conditions with fire
    print('Getting u wind from cyclic boundary conditions fireflux_med run')
    u_cyclic_no_fire = wrf.getvar(cyclic_no_fire, "ua", None, units = "m/s")[:, :, y_main, x_main]
    print('Getting v wind from cyclic boundary conditions fireflux_med run')
    v_cyclic_no_fire = wrf.getvar(cyclic_no_fire, "va", None, units = "m/s")[:, :, y_main, x_main]
    print('Getting w wind from cyclic boundary conditions fireflux_med run')
    #w_cyclic_no_fire = wrf.getvar(cyclic_no_fire, "wa", None, units = "m/s")[:, :, y_main, x_main]
    print('Getting height from cyclic boundary conditions fireflux_med run')
    #ht_cyclic_no_fire = wrf.getvar(cyclic_no_fire, "z", units="m", msl = False)[:, y_main, x_main]
    time_cyclic_no_fire = cyclic_no_fire.variables['XTIME'][:]

    print("Reading in the data")
    print("Main tower data")
    main_tower1 = pd.read_csv('/home/jbenik/FireFlux2/Codes_and_Data/Data/Main_Tower_Data/Proc_FF2_10HzMTdespiked_rotated.csv', parse_dates=['TIMESTAMP'], skiprows = (0, 2, 3))

    main_tower = main_tower1.truncate(before= np.where(main_tower1['TIMESTAMP'] == '1/30/2013  15:00:00')[0][0], 
                        after=np.where(main_tower1['TIMESTAMP'] == '1/30/2013  15:17:00')[0][0])
    # Main tower variables
    print("Getting the variables from the main tower data")
    time_main_tower = main_tower['TIMESTAMP']

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

    print("Interpolating all the variables to the main tower heights")
    # U for open fire with set values
    U_20_open_fire = wrf.interplevel(u_open_fire, ht_open_fire, 20)[:, y_main, x_main]
    U_10_open_fire = wrf.interplevel(u_open_fire, ht_open_fire, 10)[:, y_main, x_main]
    U_577_open_fire = wrf.interplevel(u_open_fire, ht_open_fire, 5.77)[:, y_main, x_main]
    # V for open fire with set values
    V_20_open_fire = wrf.interplevel(v_open_fire, ht_open_fire, 20)[:, y_main, x_main]
    V_10_open_fire = wrf.interplevel(v_open_fire, ht_open_fire, 10)[:, y_main, x_main]
    V_577_open_fire = wrf.interplevel(v_open_fire, ht_open_fire, 5.77)[:, y_main, x_main]

    # U for cyclic fire with set values
    U_20_cyclic_fire = wrf.interplevel(u_cyclic_fire, ht_cyclic_fire, 20)[:, y_main, x_main]
    U_10_cyclic_fire = wrf.interplevel(u_cyclic_fire, ht_cyclic_fire, 10)[:, y_main, x_main]
    U_577_cyclic_fire = wrf.interplevel(u_cyclic_fire, ht_cyclic_fire, 5.77)[:, y_main, x_main]
    # V for cyclic fire with set values
    V_20_cyclic_fire = wrf.interplevel(v_cyclic_fire, ht_cyclic_fire, 20)[:, y_main, x_main]
    V_10_cyclic_fire = wrf.interplevel(v_cyclic_fire, ht_cyclic_fire, 10)[:, y_main, x_main]
    V_577_cyclic_fire = wrf.interplevel(v_cyclic_fire, ht_cyclic_fire, 5.77)[:, y_main, x_main]


    # U for open no fire with set values
    U_20_open_no_fire = wrf.interplevel(u_open_no_fire, ht_open_fire, 20)[:, y_main, x_main]
    U_10_open_no_fire = wrf.interplevel(u_open_no_fire, ht_open_fire, 10)[:, y_main, x_main]
    U_577_open_no_fire = wrf.interplevel(u_open_no_fire, ht_open_fire, 5.77)[:, y_main, x_main]
    # V for open no fire with set values
    V_20_open_no_fire = wrf.interplevel(v_open_no_fire, ht_open_fire, 20)[:, y_main, x_main]
    V_10_open_no_fire = wrf.interplevel(v_open_no_fire, ht_open_fire, 10)[:, y_main, x_main]
    V_577_open_no_fire = wrf.interplevel(v_open_no_fire, ht_open_fire, 5.77)[:, y_main, x_main]

    # U for cyclic no fire with set values
    U_20_cyclic_no_fire = wrf.interplevel(u_cyclic_no_fire, ht_cyclic_fire, 20)[:, y_main, x_main]
    U_10_cyclic_no_fire = wrf.interplevel(u_cyclic_no_fire, ht_cyclic_fire, 10)[:, y_main, x_main]
    U_577_cyclic_no_fire = wrf.interplevel(u_cyclic_no_fire, ht_cyclic_fire, 5.77)[:, y_main, x_main]
    # V for cyclic no fire with set values
    V_20_cyclic_no_fire = wrf.interplevel(v_cyclic_no_fire, ht_cyclic_fire, 20)[:, y_main, x_main]
    V_10_cyclic_no_fire = wrf.interplevel(v_cyclic_no_fire, ht_cyclic_fire, 10)[:, y_main, x_main]
    V_577_cyclic_no_fire = wrf.interplevel(v_cyclic_no_fire, ht_cyclic_fire, 5.77)[:, y_main, x_main]



    ws_20_open_fire = np.sqrt((U_20_open_fire ** 2) + (V_20_open_fire ** 2))
    ws_20_cyclic_fire = np.sqrt((U_20_cyclic_fire ** 2) + (V_20_cyclic_fire ** 2))

    ws_20_open_no_fire = np.sqrt((U_20_open_no_fire ** 2) + (V_20_open_no_fire ** 2))
    ws_20_cyclic_no_fire = np.sqrt((U_20_cyclic_no_fire ** 2) + (V_20_cyclic_no_fire ** 2))

    ws_10_open_fire = np.sqrt((U_10_open_fire ** 2) + (V_10_open_fire ** 2))
    ws_10_cyclic_fire = np.sqrt((U_10_cyclic_fire ** 2) + (V_10_cyclic_fire ** 2))

    ws_10_open_no_fire = np.sqrt((U_10_open_no_fire ** 2) + (V_10_open_no_fire ** 2))
    ws_10_cyclic_no_fire = np.sqrt((U_10_cyclic_no_fire ** 2) + (V_10_cyclic_no_fire ** 2))
    
    ws_577_open_fire = np.sqrt((U_577_open_fire ** 2) + (V_577_open_fire ** 2))
    ws_577_cyclic_fire = np.sqrt((U_577_cyclic_fire ** 2) + (V_577_cyclic_fire ** 2))

    ws_577_open_no_fire = np.sqrt((U_577_open_no_fire ** 2) + (V_577_open_no_fire ** 2))
    ws_577_cyclic_no_fire = np.sqrt((U_577_cyclic_no_fire ** 2) + (V_577_cyclic_no_fire ** 2))
    time_main = main_tower['TIMESTAMP']
    time_short = np.arange(0, 720)
    results = {'time_open_fire':time_open_fire, 'time_cyclic_fire':time_cyclic_fire, 
    'time_open_no_fire':time_open_no_fire,'time_cyclic_no_fire':time_cyclic_no_fire,

    'U_20_open_fire':U_20_open_fire,'U_20_open_no_fire':U_20_open_no_fire,
    'U_20_cyclic_fire':U_20_cyclic_fire,'U_20_cyclic_no_fire':U_20_cyclic_no_fire,

    'V_20_open_fire':V_20_open_fire,'V_20_open_no_fire':V_20_open_no_fire,
    'V_20_cyclic_fire':V_20_cyclic_fire,'V_20_cyclic_no_fire':V_20_cyclic_no_fire, 

    'ws_20_open_fire':ws_20_open_fire, 'ws_20_open_no_fire':ws_20_open_no_fire,
    'ws_20_cyclic_fire':ws_20_cyclic_fire, 'ws_20_cyclic_no_fire':ws_20_cyclic_no_fire,
    
    'U_10_open_fire':U_10_open_fire,'U_10_open_no_fire':U_10_open_no_fire,
    'U_10_cyclic_fire':U_10_cyclic_fire,'U_10_cyclic_no_fire':U_10_cyclic_no_fire,

    'V_10_open_fire':V_10_open_fire,'V_10_open_no_fire':V_10_open_no_fire,
    'V_10_cyclic_fire':V_10_cyclic_fire,'V_10_cyclic_no_fire':V_10_cyclic_no_fire, 

    'ws_10_open_fire':ws_10_open_fire, 'ws_10_open_no_fire':ws_10_open_no_fire,
    'ws_10_cyclic_fire':ws_10_cyclic_fire, 'ws_10_cyclic_no_fire':ws_10_cyclic_no_fire,

    'U_577_open_fire':U_577_open_fire,'U_577_open_no_fire':U_577_open_no_fire,
    'U_577_cyclic_fire':U_577_cyclic_fire,'U_577_cyclic_no_fire':U_577_cyclic_no_fire,

    'V_577_open_fire':V_577_open_fire,'V_577_open_no_fire':V_577_open_no_fire,
    'V_577_cyclic_fire':V_577_cyclic_fire,'V_577_cyclic_no_fire':V_577_cyclic_no_fire,

    'ws_577_open_fire':ws_577_open_fire, 'ws_577_open_no_fire':ws_577_open_no_fire,
    'ws_577_cyclic_fire':ws_577_cyclic_fire, 'ws_577_cyclic_no_fire':ws_577_cyclic_no_fire,


    'time_main':time_main} #put the other variables in here such as wsw and ww

    with open(out_path, 'wb') as f:
        pickle.dump(results, f)
else:
    with open(out_path, 'rb') as f:
        results = pickle.load(f)
    locals().update(results)
# %% Short towers
y_east = int(158/2)
x_east = int(117/2)

# West tower
y_west = int(151/2)
x_west = int(94/2)

# South tower
y_south = int(119/2)
x_south = int(115/2)
# %% Main tower data
main_tower1 = pd.read_csv('/home/jbenik/FireFlux2/Codes_and_Data/Data/Main_Tower_Data/Proc_FF2_10HzMTdespiked_rotated.csv', parse_dates=['TIMESTAMP'], skiprows = (0, 2, 3))

main_tower = main_tower1.truncate(before= np.where(main_tower1['TIMESTAMP'] == '1/30/2013  15:00:00')[0][0], 
                    after=np.where(main_tower1['TIMESTAMP'] == '1/30/2013  15:29:00')[0][0])
# Main tower variables
print("Getting the variables from the main tower data")
time_main_tower = main_tower['TIMESTAMP']
time_main = np.arange(0, 1740.1, .1)
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

# %% Creating plots

# Plotting the U winds from open boundary run
fig, ax = plt.subplots(3, figsize = (12, 10))
plt.suptitle('Simulated Main Tower U Winds From Open Boundary Fire Run', fontsize = 18, fontweight = 'bold')
ax[0].plot(time_open_fire * 60, U_20_open_fire, color = 'red', label = 'U Wind')
ax[0].set_title('Simulated U Wind at 21.18m', fontsize = 18, fontweight = 'bold')
ax[0].set_xlabel('Time (S)', fontsize = 12, fontweight = 'bold')
ax[0].set_ylabel('Wind Speed (m/s)', fontsize = 12, fontweight = 'bold')
ax[0].legend()
ax[0].grid()

ax[1].plot(time_open_fire * 60, U_10_open_fire, color = 'red', label = 'U Wind')
ax[1].set_title('Simulated U Wind at 10m', fontsize = 18, fontweight = 'bold')
ax[1].set_xlabel('Time (S)', fontsize = 12, fontweight = 'bold')
ax[1].set_ylabel('Wind Speed (m/s)', fontsize = 12, fontweight = 'bold')
ax[1].legend()
ax[1].grid()

ax[2].plot(time_open_fire * 60, U_577_open_fire, color = 'red', label = 'U Wind')
ax[2].set_title('Simulated U Wind at 5.19m', fontsize = 18, fontweight = 'bold')
ax[2].set_xlabel('Time (S)', fontsize = 12, fontweight = 'bold')
ax[2].set_ylabel('Wind Speed (m/s)', fontsize = 12, fontweight = 'bold')
ax[2].legend()
ax[2].grid()

plt.tight_layout()
#plt.savefig('/home/jbenik/fireflux_med/images/u_open_fire.png')
plt.show()
# %% V winds from open boundary run
# Plotting the V winds from open boundary run 
fig, ax = plt.subplots(3, figsize = (12, 10))
plt.suptitle('Simulated Main Tower V Winds From Open Boundary Fire Run', fontsize = 18, fontweight = 'bold')
ax[0].plot(time_open_fire * 60, V_20_open_fire, color = 'red', label = 'V Wind')
ax[0].set_title('Simulated V Wind at 21.18m', fontsize = 18, fontweight = 'bold')
ax[0].set_xlabel('Time (S)', fontsize = 12, fontweight = 'bold')
ax[0].set_ylabel('Wind Speed (m/s)', fontsize = 12, fontweight = 'bold')
ax[0].legend()
ax[0].grid()

ax[1].plot(time_open_fire * 60, V_10_open_fire, color = 'red', label = 'V Wind')
ax[1].set_title('Simulated V Wind at 10m', fontsize = 18, fontweight = 'bold')
ax[1].set_xlabel('Time (S)', fontsize = 12, fontweight = 'bold')
ax[1].set_ylabel('Wind Speed (m/s)', fontsize = 12, fontweight = 'bold')
ax[1].legend()
ax[1].grid()

ax[2].plot(time_open_fire * 60, V_577_open_fire, color = 'red', label = 'V Wind')
ax[2].set_title('Simulated V Wind at 5.19m', fontsize = 18, fontweight = 'bold')
ax[2].set_xlabel('Time (S)', fontsize = 12, fontweight = 'bold')
ax[2].set_ylabel('Wind Speed (m/s)', fontsize = 12, fontweight = 'bold')
ax[2].legend()
ax[2].grid()

plt.tight_layout()
#plt.savefig('/home/jbenik/fireflux_med/images/v_open_fire.png')
plt.show()
# %% U winds from cyclic boundary run
# Plotting the U winds from cyclic boundary run 
fig, ax = plt.subplots(3, figsize = (12, 10))
plt.suptitle('Simulated Main Tower U Winds From cyclic Boundary Fire Run', fontsize = 18, fontweight = 'bold')
ax[0].plot(time_cyclic_fire * 60, U_20_cyclic_fire, color = 'red', label = 'U Wind')
ax[0].set_title('Simulated U Wind at 21.18m', fontsize = 18, fontweight = 'bold')
ax[0].set_xlabel('Time (S)', fontsize = 12, fontweight = 'bold')
ax[0].set_ylabel('Wind Speed (m/s)', fontsize = 12, fontweight = 'bold')
ax[0].legend()
ax[0].grid()

ax[1].plot(time_cyclic_fire * 60, U_10_cyclic_fire, color = 'red', label = 'U Wind')
ax[1].set_title('Simulated U Wind at 10m', fontsize = 18, fontweight = 'bold')
ax[1].set_xlabel('Time (S)', fontsize = 12, fontweight = 'bold')
ax[1].set_ylabel('Wind Speed (m/s)', fontsize = 12, fontweight = 'bold')
ax[1].legend()
ax[1].grid()

ax[2].plot(time_cyclic_fire * 60, U_577_cyclic_fire, color = 'red', label = 'U Wind')
ax[2].set_title('Simulated U Wind at 5.19m', fontsize = 18, fontweight = 'bold')
ax[2].set_xlabel('Time (S)', fontsize = 12, fontweight = 'bold')
ax[2].set_ylabel('Wind Speed (m/s)', fontsize = 12, fontweight = 'bold')
ax[2].legend()
ax[2].grid()

plt.tight_layout()
#plt.savefig('/home/jbenik/fireflux_med/images/u_cyclic_fire.png')
plt.show()
# %% V winds from cyclic boundary run
# Plotting the V winds from cyclic boundary run 
fig, ax = plt.subplots(3, figsize = (12, 10))
plt.suptitle('Simulated Main Tower V Winds From cyclic Boundary Fire Run', fontsize = 18, fontweight = 'bold')
ax[0].plot(time_cyclic_fire * 60, V_20_cyclic_fire, color = 'red', label = 'V Wind')
ax[0].set_title('Simulated V Wind at 21.18m', fontsize = 18, fontweight = 'bold')
ax[0].set_xlabel('Time (S)', fontsize = 12, fontweight = 'bold')
ax[0].set_ylabel('Wind Speed (m/s)', fontsize = 12, fontweight = 'bold')
ax[0].legend()
ax[0].grid()

ax[1].plot(time_cyclic_fire * 60, V_10_cyclic_fire, color = 'red', label = 'V Wind')
ax[1].set_title('Simulated V Wind at 10m', fontsize = 18, fontweight = 'bold')
ax[1].set_xlabel('Time (S)', fontsize = 12, fontweight = 'bold')
ax[1].set_ylabel('Wind Speed (m/s)', fontsize = 12, fontweight = 'bold')
ax[1].legend()
ax[1].grid()

ax[2].plot(time_cyclic_fire * 60, V_577_cyclic_fire, color = 'red', label = 'V Wind')
ax[2].set_title('Simulated V Wind at 5.19m', fontsize = 18, fontweight = 'bold')
ax[2].set_xlabel('Time (S)', fontsize = 12, fontweight = 'bold')
ax[2].set_ylabel('Wind Speed (m/s)', fontsize = 12, fontweight = 'bold')
ax[2].legend()
ax[2].grid()

plt.tight_layout()
#plt.savefig('/home/jbenik/fireflux_med/images/v_cyclic_fire.png')
plt.show()
# %% U and V winds from the fire_atms = 0 runs

# Open Boundary conditions
fig, ax = plt.subplots(3, figsize = (12, 10))
ax2 = ax[0].twinx()
plt.suptitle('Simulated Main Tower V Winds From Open Boundary No Fire Run', fontsize = 18, fontweight = 'bold')
ax1 = ax[0].plot(time_open_no_fire * 60, U_20_open_no_fire, color = 'red', label = 'U Wind')
ax3 = ax2.plot(time_open_no_fire * 60, V_20_open_no_fire, color = 'blue', label = 'V Wind')
ax2.set_ylabel('V Wind (m/s)', fontsize = 12, fontweight = 'bold')
ax[0].set_title('Simulated U and V Wind at 21.18m', fontsize = 18, fontweight = 'bold')
ax[0].set_xlabel('Time (S)', fontsize = 12, fontweight = 'bold')
ax[0].set_ylabel('U Wind (m/s)', fontsize = 12, fontweight = 'bold')
label = ax1 + ax3
labels = [i.get_label() for i in label]
ax[0].legend(label, labels, prop={'size': 12})
ax[0].grid()

ax2 = ax[1].twinx()
ax1 = ax[1].plot(time_open_no_fire * 60, U_10_open_no_fire, color = 'red', label = 'U Wind')
ax3 = ax2.plot(time_open_no_fire * 60, V_10_open_no_fire, color = 'blue', label = 'V Wind')
ax[1].set_title('Simulated U and V Wind at 10m', fontsize = 18, fontweight = 'bold')
ax2.set_ylabel('V Wind (m/s)', fontsize = 12, fontweight = 'bold')
ax[1].set_xlabel('Time (S)', fontsize = 12, fontweight = 'bold')
ax[1].set_ylabel('U Wind (m/s)', fontsize = 12, fontweight = 'bold')
label = ax1 + ax3
labels = [i.get_label() for i in label]
ax[1].legend(label, labels, prop={'size': 12})
ax[1].grid()

ax2 = ax[2].twinx()
ax1 = ax[2].plot(time_open_no_fire * 60, U_577_open_no_fire, color = 'red', label = 'U Wind')
ax3 = ax2.plot(time_open_no_fire * 60, V_577_open_no_fire, color = 'blue', label = 'V Wind')
ax[2].set_title('Simulated U and V Wind at 5.19m', fontsize = 18, fontweight = 'bold')
ax2.set_ylabel('V Wind (m/s)', fontsize = 12, fontweight = 'bold')
ax[2].set_xlabel('Time (S)', fontsize = 12, fontweight = 'bold')
ax[2].set_ylabel('U Wind (m/s)', fontsize = 12, fontweight = 'bold')
label = ax1 + ax3
labels = [i.get_label() for i in label]
ax[2].legend(label, labels, prop={'size': 12})
ax[2].grid()

plt.tight_layout()
#plt.savefig('/home/jbenik/fireflux_med/images/u_and_v_open_no_fire.png')
plt.show()

# %% Cyclic Boundary conditions

# Cyclic Boundary conditions
fig, ax = plt.subplots(3, figsize = (12, 10))
ax2 = ax[0].twinx()
plt.suptitle('Simulated Main Tower V Winds From cyclic Boundary No Fire Run', fontsize = 18, fontweight = 'bold')
ax1 = ax[0].plot(time_cyclic_no_fire * 60, U_20_cyclic_no_fire, color = 'red', label = 'U Wind')
ax3 = ax2.plot(time_cyclic_no_fire * 60, V_20_cyclic_no_fire, color = 'blue', label = 'V Wind')
ax2.set_ylabel('V Wind (m/s)', fontsize = 12, fontweight = 'bold')
ax[0].set_title('Simulated U and V Wind at 21.18m', fontsize = 18, fontweight = 'bold')
ax[0].set_xlabel('Time (S)', fontsize = 12, fontweight = 'bold')
ax[0].set_ylabel('U Wind (m/s)', fontsize = 12, fontweight = 'bold')
label = ax1 + ax3
labels = [i.get_label() for i in label]
ax[0].legend(label, labels, prop={'size': 12})
ax[0].grid()

ax2 = ax[1].twinx()
ax1 = ax[1].plot(time_cyclic_no_fire * 60, U_10_cyclic_no_fire, color = 'red', label = 'U Wind')
ax3 = ax2.plot(time_cyclic_no_fire * 60, V_10_cyclic_no_fire, color = 'blue', label = 'V Wind')
ax[1].set_title('Simulated U and V Wind at 10m', fontsize = 18, fontweight = 'bold')
ax2.set_ylabel('V Wind (m/s)', fontsize = 12, fontweight = 'bold')
ax[1].set_xlabel('Time (S)', fontsize = 12, fontweight = 'bold')
ax[1].set_ylabel('U Wind (m/s)', fontsize = 12, fontweight = 'bold')
label = ax1 + ax3
labels = [i.get_label() for i in label]
ax[1].legend(label, labels, prop={'size': 12})
ax[1].grid()

ax2 = ax[2].twinx()
ax1 = ax[2].plot(time_cyclic_no_fire * 60, U_577_cyclic_no_fire, color = 'red', label = 'U Wind')
ax3 = ax2.plot(time_cyclic_no_fire * 60, V_577_cyclic_no_fire, color = 'blue', label = 'V Wind')
ax[2].set_title('Simulated U and V Wind at 5.19m', fontsize = 18, fontweight = 'bold')
ax2.set_ylabel('V Wind (m/s)', fontsize = 12, fontweight = 'bold')
ax[2].set_xlabel('Time (S)', fontsize = 12, fontweight = 'bold')
ax[2].set_ylabel('U Wind (m/s)', fontsize = 12, fontweight = 'bold')
label = ax1 + ax3
labels = [i.get_label() for i in label]
ax[2].legend(label, labels, prop={'size': 12})
ax[2].grid()

plt.tight_layout()
#plt.savefig('/home/jbenik/fireflux_med/images/u_and_v_cyclic_no_fire.png')
plt.show()
# %% Wind Speeds Cyclic
# Plotting the Winds from cyclic boundary run 
fig, ax = plt.subplots(3, figsize = (12, 10))
plt.suptitle('Simulated Main Tower Winds From Cyclic Boundary Fire Run', fontsize = 18, fontweight = 'bold')
ax[0].plot(time_cyclic_fire * 60, ws_20_cyclic_fire, color = 'red', label = 'V Wind')
ax[0].set_title('Simulated V Wind at 21.18m', fontsize = 18, fontweight = 'bold')
ax[0].set_xlabel('Time (S)', fontsize = 12, fontweight = 'bold')
ax[0].set_ylabel('Wind Speed (m/s)', fontsize = 12, fontweight = 'bold')
ax[0].legend()
ax[0].grid()

ax[1].plot(time_cyclic_fire * 60, ws_10_cyclic_fire, color = 'red', label = 'V Wind')
ax[1].set_title('Simulated Wind at 10m', fontsize = 18, fontweight = 'bold')
ax[1].set_xlabel('Time (S)', fontsize = 12, fontweight = 'bold')
ax[1].set_ylabel('Wind Speed (m/s)', fontsize = 12, fontweight = 'bold')
ax[1].legend()
ax[1].grid()

ax[2].plot(time_cyclic_fire * 60, ws_577_cyclic_fire, color = 'red', label = 'V Wind')
ax[2].set_title('Simulated Wind at 5.19m', fontsize = 18, fontweight = 'bold')
ax[2].set_xlabel('Time (S)', fontsize = 12, fontweight = 'bold')
ax[2].set_ylabel('Wind Speed (m/s)', fontsize = 12, fontweight = 'bold')
ax[2].legend()
ax[2].grid()

plt.tight_layout()
#plt.savefig('/home/jbenik/fireflux_med/images/v_cyclic_fire.png')
plt.show()
# %% Wind Speeds Open
# Plotting the Winds from open boundary run 
fig, ax = plt.subplots(3, figsize = (12, 10))
plt.suptitle('Simulated Main Tower Winds From open Boundary Fire Run', fontsize = 18, fontweight = 'bold')
ax[0].plot(time_open_fire * 60, ws_20_open_fire, color = 'red', label = 'V Wind')
ax[0].set_title('Simulated V Wind at 21.18m', fontsize = 18, fontweight = 'bold')
ax[0].set_xlabel('Time (S)', fontsize = 12, fontweight = 'bold')
ax[0].set_ylabel('Wind Speed (m/s)', fontsize = 12, fontweight = 'bold')
ax[0].legend()
ax[0].grid()

ax[1].plot(time_open_fire * 60, ws_10_open_fire, color = 'red', label = 'V Wind')
ax[1].set_title('Simulated Wind at 10m', fontsize = 18, fontweight = 'bold')
ax[1].set_xlabel('Time (S)', fontsize = 12, fontweight = 'bold')
ax[1].set_ylabel('Wind Speed (m/s)', fontsize = 12, fontweight = 'bold')
ax[1].legend()
ax[1].grid()

ax[2].plot(time_open_fire * 60, ws_577_open_fire, color = 'red', label = 'V Wind')
ax[2].set_title('Simulated Wind at 5.19m', fontsize = 18, fontweight = 'bold')
ax[2].set_xlabel('Time (S)', fontsize = 12, fontweight = 'bold')
ax[2].set_ylabel('Wind Speed (m/s)', fontsize = 12, fontweight = 'bold')
ax[2].legend()
ax[2].grid()

plt.tight_layout()
#plt.savefig('/home/jbenik/fireflux_med/images/v_open_fire.png')
plt.show()

# %% Plotting both

# Cyclic and Open Boundary conditions
fig, ax = plt.subplots(3, figsize = (12, 10))
ax2 = ax[0].twinx()
plt.suptitle('Simulated Main Tower Winds From Cyclic and Open Boundary Fire Run', fontsize = 18, fontweight = 'bold')
ax1 = ax[0].plot(time_cyclic_fire * 60, ws_20_cyclic_fire, color = 'red', label = 'Cyclic Winds')
ax3 = ax2.plot(time_open_fire * 60, ws_20_open_fire, color = 'blue', label = 'Open Winds')
ax2.set_ylabel('Cyclic Wind (m/s)', fontsize = 12, fontweight = 'bold')
ax[0].set_title('Simulated Winds at 21.18m', fontsize = 18, fontweight = 'bold')
ax[0].set_xlabel('Time (S)', fontsize = 12, fontweight = 'bold')
ax[0].set_ylabel('Open Wind (m/s)', fontsize = 12, fontweight = 'bold')
label = ax1 + ax3
labels = [i.get_label() for i in label]
ax[0].legend(label, labels, prop={'size': 12})
ax[0].grid()

ax2 = ax[1].twinx()
ax1 = ax[1].plot(time_cyclic_fire * 60, ws_10_cyclic_fire, color = 'red', label = 'Cyclic Winds')
ax3 = ax2.plot(time_open_fire * 60, ws_10_open_fire, color = 'blue', label = 'Open Winds')
ax[1].set_title('Simulated Winds at 10m', fontsize = 18, fontweight = 'bold')
ax2.set_ylabel('Cyclic Wind (m/s)', fontsize = 12, fontweight = 'bold')
ax[1].set_xlabel('Time (S)', fontsize = 12, fontweight = 'bold')
ax[1].set_ylabel('Open Wind (m/s)', fontsize = 12, fontweight = 'bold')
label = ax1 + ax3
labels = [i.get_label() for i in label]
ax[1].legend(label, labels, prop={'size': 12})
ax[1].grid()

ax2 = ax[2].twinx()
ax1 = ax[2].plot(time_cyclic_fire * 60, ws_577_cyclic_fire, color = 'red', label = 'Cyclic Wind')
ax3 = ax2.plot(time_open_fire * 60, ws_577_open_fire, color = 'blue', label = 'Open Wind')
ax[2].set_title('Simulated Winds at 5.19m', fontsize = 18, fontweight = 'bold')
ax2.set_ylabel('Cyclic Wind (m/s)', fontsize = 12, fontweight = 'bold')
ax[2].set_xlabel('Time (S)', fontsize = 12, fontweight = 'bold')
ax[2].set_ylabel('Open Wind (m/s)', fontsize = 12, fontweight = 'bold')
label = ax1 + ax3
labels = [i.get_label() for i in label]
ax[2].legend(label, labels, prop={'size': 12})
ax[2].grid()

plt.tight_layout()
#plt.savefig('/home/jbenik/fireflux_med/images/u_and_v_cyclic_fire.png')
plt.show()


# %% plotting both on the same plot

# Cyclic and Open Boundary conditions
fig, ax = plt.subplots(3, figsize = (12, 10))
plt.suptitle('Simulated Main Tower Winds From Cyclic and Open Boundary Fire Run', fontsize = 18, fontweight = 'bold')
ax[0].plot(time_cyclic_fire * 60, ws_20_cyclic_fire, color = 'red', label = 'Cyclic Winds')
ax[0].plot(time_open_fire * 60, ws_20_open_fire, color = 'blue', label = 'Open Winds', linestyle = '--')
ax[0].set_ylabel('Wind Speeds (m/s)', fontsize = 12, fontweight = 'bold')
ax[0].set_title('Simulated Winds at 21.18m', fontsize = 18, fontweight = 'bold')
ax[0].set_xlabel('Time (S)', fontsize = 12, fontweight = 'bold')
ax[0].legend()
ax[0].grid()


ax[1].plot(time_cyclic_fire * 60, ws_10_cyclic_fire, color = 'red', label = 'Cyclic Winds')
ax[1].plot(time_open_fire * 60, ws_10_open_fire, color = 'blue', label = 'Open Winds', linestyle = '--')
ax[1].set_title('Simulated Winds at 10m', fontsize = 18, fontweight = 'bold')
ax[1].set_xlabel('Time (S)', fontsize = 12, fontweight = 'bold')
ax[1].set_ylabel('Wind Speeds (m/s)', fontsize = 12, fontweight = 'bold')
ax[1].legend()
ax[1].grid()

ax[2].plot(time_cyclic_fire * 60, ws_577_cyclic_fire, color = 'red', label = 'Cyclic Wind')
ax[2].plot(time_open_fire * 60, ws_577_open_fire, color = 'blue', label = 'Open Wind', linestyle = '--')
ax[2].set_title('Simulated Winds at 5.19m', fontsize = 18, fontweight = 'bold')
ax[2].set_xlabel('Time (S)', fontsize = 12, fontweight = 'bold')
ax[2].set_ylabel('Winds (m/s)', fontsize = 12, fontweight = 'bold')
ax[2].legend()
ax[2].grid()

plt.tight_layout()
#plt.savefig('/home/jbenik/fireflux_med/images/u_and_v_cyclic_fire.png')
plt.show()

# %% No fire

# Cyclic and Open Boundary conditions
fig, ax = plt.subplots(3, figsize = (12, 10))
plt.suptitle('Simulated Main Tower Winds From Cyclic and Open Boundary No Fire Run', fontsize = 18, fontweight = 'bold')
ax[0].plot(time_cyclic_no_fire * 60, ws_20_cyclic_no_fire, color = 'red', label = 'Cyclic Winds')
ax[0].plot(time_open_no_fire * 60, ws_20_open_no_fire, color = 'blue', label = 'Open Winds', linestyle = '--')
ax[0].set_ylabel('Wind Speeds (m/s)', fontsize = 12, fontweight = 'bold')
ax[0].set_title('Simulated Winds at 21.18m', fontsize = 18, fontweight = 'bold')
ax[0].set_xlabel('Time (S)', fontsize = 12, fontweight = 'bold')
ax[0].legend()
ax[0].grid()


ax[1].plot(time_cyclic_no_fire * 60, ws_10_cyclic_no_fire, color = 'red', label = 'Cyclic Winds')
ax[1].plot(time_open_no_fire * 60, ws_10_open_no_fire, color = 'blue', label = 'Open Winds', linestyle = '--')
ax[1].set_title('Simulated Winds at 10m', fontsize = 18, fontweight = 'bold')
ax[1].set_xlabel('Time (S)', fontsize = 12, fontweight = 'bold')
ax[1].set_ylabel('Wind Speeds (m/s)', fontsize = 12, fontweight = 'bold')
ax[1].legend()
ax[1].grid()

ax[2].plot(time_cyclic_no_fire * 60, ws_577_cyclic_no_fire, color = 'red', label = 'Cyclic Wind')
ax[2].plot(time_open_no_fire * 60, ws_577_open_no_fire, color = 'blue', label = 'Open Wind', linestyle = '--')
ax[2].set_title('Simulated Winds at 5.19m', fontsize = 18, fontweight = 'bold')
ax[2].set_xlabel('Time (S)', fontsize = 12, fontweight = 'bold')
ax[2].set_ylabel('Winds (m/s)', fontsize = 12, fontweight = 'bold')
ax[2].legend()
ax[2].grid()

plt.tight_layout()
#plt.savefig('/home/jbenik/fireflux_med/images/u_and_v_cyclic_no_fire.png')
plt.show()

# %% Main tower data included
fig, ax = plt.subplots(3, figsize = (12, 10))
plt.suptitle('Simulated Main Tower Winds From Cyclic and Open Boundary No Fire Run', fontsize = 18, fontweight = 'bold')
ax[0].plot(time_cyclic_no_fire * 60, ws_20_cyclic_no_fire, color = 'red', label = 'Cyclic Winds')
ax[0].plot(time_open_no_fire * 60, ws_20_open_no_fire, color = 'blue', label = 'Open Winds', linestyle = '--')
ax[0].plot(time_main, ws_20, color = 'green', label = 'Main Tower Winds')
ax[0].set_ylabel('Wind Speeds (m/s)', fontsize = 12, fontweight = 'bold')
ax[0].set_title('Simulated Winds at 21.18m', fontsize = 18, fontweight = 'bold')
ax[0].set_xlabel('Time (S)', fontsize = 12, fontweight = 'bold')
ax[0].legend()
ax[0].grid()
ax[0].set_xlim(1100, 1300)


ax[1].plot(time_cyclic_no_fire * 60, ws_10_cyclic_no_fire, color = 'red', label = 'Cyclic Winds')
ax[1].plot(time_open_no_fire * 60, ws_10_open_no_fire, color = 'blue', label = 'Open Winds', linestyle = '--')
ax[1].plot(time_main, ws_10, color = 'green', label = 'Main Tower Winds')
ax[1].set_title('Simulated Winds at 10m', fontsize = 18, fontweight = 'bold')
ax[1].set_xlabel('Time (S)', fontsize = 12, fontweight = 'bold')
ax[1].set_ylabel('Wind Speeds (m/s)', fontsize = 12, fontweight = 'bold')
ax[1].legend()
ax[1].grid()
ax[1].set_xlim(1100, 1300)

ax[2].plot(time_cyclic_no_fire * 60, ws_577_cyclic_no_fire, color = 'red', label = 'Cyclic Wind')
ax[2].plot(time_open_no_fire * 60, ws_577_open_no_fire, color = 'blue', label = 'Open Wind', linestyle = '--')
ax[2].plot(time_main, ws_6, color = 'green', label = 'Main Tower Winds')
ax[2].set_title('Simulated Winds at 5.19m', fontsize = 18, fontweight = 'bold')
ax[2].set_xlabel('Time (S)', fontsize = 12, fontweight = 'bold')
ax[2].set_ylabel('Winds (m/s)', fontsize = 12, fontweight = 'bold')
ax[2].legend()
ax[2].grid()
ax[2].set_xlim(1100, 1300)

plt.tight_layout()
#plt.savefig('/home/jbenik/fireflux_med/images/u_and_v_cyclic_no_fire.png')
plt.show()

# %%
