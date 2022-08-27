print('this file plots the basic sounding for open and cyclic boundary conditions ff_med runs')
# %% Importing necesary libraries
import matplotlib.pyplot as plt
import netCDF4 as nc
import pandas as pd
import numpy as np
import wrf
import pickle
import os.path as osp
# %% Getting the variables and storing them in a pickle file
out_path = 'fireflux_med_base_sounding_1.pkl'
if not osp.exists(out_path):
    y_main = int(190/2)
    x_main = int(93/2)
    # Cyclic
    cyclic_1 = nc.Dataset('base_runs/cyclic/wrfout_d01_2013-01-30_14:40:00')
    cyclic_2 = nc.Dataset('base_runs/cyclic/wrfout_d01_2013-01-30_14:56:40')
    # Take everything at 34 and beyond since they are the same times
    cyclic_3 = nc.Dataset('base_runs/cyclic/wrfout_d01_2013-01-30_15:01:01')

    # Open
    open_1 = nc.Dataset('base_runs/open/wrfout_d01_2013-01-30_14:40:00')
    open_2 = nc.Dataset('base_runs/open/wrfout_d01_2013-01-30_14:56:40')


    print('Getting u from all the wrfout files with corrected time stamp')
    print('Getting first u from cyclic')
    u_1_cyclic = wrf.getvar(cyclic_1, "ua", None, units = "m/s")[:, :, y_main, x_main]
    print('Getting second u from cyclic')
    u_2_cyclic = wrf.getvar(cyclic_2, "ua", None, units = "m/s")[:, :, y_main, x_main]
    print('Getting third u from cyclic')
    u_3_cyclic = wrf.getvar(cyclic_3, "ua", None, units = "m/s")[34::, :, y_main, x_main]
    print('Getting first u from open')
    u_1_open = wrf.getvar(open_1, "ua", None, units = "m/s")[:, :, y_main, x_main]
    print('Getting second u from open')
    u_2_open = wrf.getvar(open_2, "ua", None, units = "m/s")[:, :, y_main, x_main]
    print('Getting v from all the wrfovt files with corrected time stamp')

    v_1_cyclic = wrf.getvar(cyclic_1, "va", None, units = "m/s")[:, :, y_main, x_main]
    v_2_cyclic = wrf.getvar(cyclic_2, "va", None, units = "m/s")[:, :, y_main, x_main]
    v_3_cyclic = wrf.getvar(cyclic_3, "va", None, units = "m/s")[34::, :, y_main, x_main]
    v_1_open = wrf.getvar(open_1, "va", None, units = "m/s")[:, :, y_main, x_main]
    v_2_open = wrf.getvar(open_2, "va", None, units = "m/s")[:, :, y_main, x_main]
    
    
    ws_1_cyclic = np.sqrt((u_1_cyclic ** 2) + (v_1_cyclic ** 2)) 
    ws_2_cyclic = np.sqrt((u_2_cyclic ** 2) + (v_2_cyclic ** 2)) 
    ws_3_cyclic = np.sqrt((u_3_cyclic ** 2) + (v_3_cyclic ** 2))
    ws_1_open = np.sqrt((u_1_open ** 2) + (v_1_open ** 2)) 
    ws_2_open = np.sqrt((u_2_open ** 2) + (v_2_open ** 2)) 

    time_1_cyclic = cyclic_1.variables['XTIME'][:]
    time_2_cyclic = cyclic_2.variables['XTIME'][:]
    time_3_cyclic = cyclic_3.variables['XTIME'][34::]
    time_1_open = open_1.variables['XTIME'][:]
    time_2_open = open_2.variables['XTIME'][:]


    results = {'time_1_cyclic':time_1_cyclic, 'time_2_cyclic':time_2_cyclic,
    'time_3_cyclic':time_3_cyclic, 'time_1_open':time_1_open, 'time_2_open':time_2_open,
    'ws_1_cyclic':ws_1_cyclic, 'ws_2_cyclic':ws_2_cyclic, 'ws_3_cyclic':ws_3_cyclic,
    'ws_1_open':ws_1_open, 'ws_2_open':ws_2_open}
    with open(out_path, 'wb') as f:
        pickle.dump(results, f)
else:
    with open(out_path, 'rb') as f:
        results = pickle.load(f)
    locals().update(results)

# %% concatenating the data
'''1.02903414e+00, 3.13614893e+00, 5.34496069e+00, 7.66261530e+00,
       1.00967093e+01, 1.26556549e+01, 1.53481236e+01, 1.81820831e+01,
       2.11639767e+01, 2.42990532e+01, 2.75926247e+01, 3.10511303e+01,
       3.46819649e+01, 3.84929390e+01, 4.24925880e+01, 4.66908989e+01'''
ws_h_533_cyclic = np.concatenate((ws_1_cyclic[:, 2], ws_2_cyclic[:, 2], ws_3_cyclic[:, 2]), axis = 0)
ws_h_533_open = np.concatenate((ws_1_open[:, 2], ws_2_open[:, 2]), axis = 0)

ws_h_10_cyclic = np.concatenate((ws_1_cyclic[:, 4], ws_2_cyclic[:, 4], ws_3_cyclic[:, 4]), axis = 0)
ws_h_10_open = np.concatenate((ws_1_open[:, 4], ws_2_open[:, 4]), axis = 0)

ws_h_20_cyclic = np.concatenate((ws_1_cyclic[:, 8], ws_2_cyclic[:, 8], ws_3_cyclic[:, 8]), axis = 0)
ws_h_20_open = np.concatenate((ws_1_open[:, 8], ws_2_open[:, 8]), axis = 0)

time_cyclic = np.concatenate((time_1_cyclic[:], time_2_cyclic[:], time_3_cyclic[34::])) 
time_open = np.concatenate((time_1_open[:], time_2_open[:])) 
# %% Main tower data
main_tower1 = pd.read_csv('/home/jbenik/FireFlux2/Codes_and_Data/Data/Main_Tower_Data/Proc_FF2_10HzMTdespiked_rotated.csv', parse_dates=['TIMESTAMP'], skiprows = (0, 2, 3))

main_tower = main_tower1.truncate(before= np.where(main_tower1['TIMESTAMP'] == '1/30/2013  15:00:00')[0][0], 
                    after=np.where(main_tower1['TIMESTAMP'] == '1/30/2013  15:06:00')[0][0])
# Main tower variables
print("Getting the variables from the main tower data")
time_main_tower = main_tower['TIMESTAMP']
time_main = np.arange(1200, 1560.1, .1)
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
# %% Creating the plot
fig, ax = plt.subplots(3, figsize = (12, 10))
#cyclic
#open
#observations
ax[0].plot(time_cyclic[0:1520] * 60, ws_h_20_cyclic[0:1520], color = 'blue', label = 'Cyclic')
ax[0].plot(time_open[0:1520] * 60, ws_h_20_open[0:1520], color = 'red', label = 'Open')
ax[0].plot(time_main, ws_20, color = 'green', label = 'Observations')
ax[0].set_xlabel('Time (s)', fontsize = 12, fontweight = 'bold')
ax[0].set_ylabel('Wind Speed (m/s)', fontsize = 12, fontweight = 'bold')
ax[0].set_title('21.1m Winds with Obs. Winds', fontsize = 18, fontweight = 'bold')
ax[0].grid()
ax[0].legend()
#ax[0].set_xlim(1175, 1600)

ax[1].plot(time_cyclic[0:1520] * 60, ws_h_10_cyclic[0:1520], color = 'blue', label = 'Cyclic')
ax[1].plot(time_open[0:1520] * 60, ws_h_10_open[0:1520], color = 'red', label = 'Open')
ax[1].plot(time_main, ws_10, color = 'green', label = 'Observations')
ax[1].set_xlabel('Time (s)', fontsize = 12, fontweight = 'bold')
ax[1].set_ylabel('Wind Speed (m/s)', fontsize = 12, fontweight = 'bold')
ax[1].set_title('10m Winds with Obs. Winds', fontsize = 18, fontweight = 'bold')
ax[1].grid()
ax[1].legend()
#ax[1].set_xlim(1175, 1600)

ax[2].plot(time_cyclic[0:1520] * 60, ws_h_533_cyclic[0:1520], color = 'blue', label = 'Cyclic')
ax[2].plot(time_open[0:1520] * 60, ws_h_533_open[0:1520], color = 'red', label = 'Open')
ax[2].plot(time_main, ws_6, color = 'green', label = 'Observations')
ax[2].set_xlabel('Time (s)', fontsize = 12, fontweight = 'bold')
ax[2].set_ylabel('Wind Speed (m/s)', fontsize = 12, fontweight = 'bold')
ax[2].set_title('5.34m Winds with Obs. Winds', fontsize = 18, fontweight = 'bold')
ax[2].grid()
ax[2].legend()
#ax[2].set_xlim(1175, 1600)

plt.tight_layout()
plt.show()

# %%
