# %% Importing necessary libraries
import netCDF4 as nc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import os.path as osp
import wrf
import os.path as osp
# %% Reading in the files
wrfout_1 = nc.Dataset('new_sounding/wrfout_d01_2013-01-30_14:40:00')
wrfout_2 = nc.Dataset('new_sounding/wrfout_d01_2013-01-30_14:56:40')
wrfout_3 = nc.Dataset('new_sounding/wrfout_d01_2013-01-30_15:03:01')
wrfout_4 = nc.Dataset('new_sounding/wrfout_d01_2013-01-30_15:19:41')
wrfout_5 = nc.Dataset('new_sounding/wrfout_d01_2013-01-30_15:27:01')
# %% Reading in variables
# Times I need to truncate the files to
# File 1 OK
# File 2 OK
# File 3 Time 53 + OK
# File 4 take last 10 out
# File 5 OK
# %% Checking timestamps to make sure they are correct with this config
time_1 = wrfout_1.variables['XTIME'][:]
time_2 = wrfout_2.variables['XTIME'][:]
time_3 = wrfout_3.variables['XTIME'][32::]
time_4 = wrfout_4.variables['XTIME'][:]
time_5 = wrfout_5.variables['XTIME'][9::]

y_main = int(190/2)
x_main = int(93/2)
out_path = 'fireflux_med_new_sounding_vars_2.pkl'
if not osp.exists(out_path):
    # Getting variables
    print('Getting u from all the wrfout files with corrected time stamp')
    print('Getting first u')
    u_1 = wrf.getvar(wrfout_1, "ua", None, units = "m/s")[:, :, y_main, x_main]
    print('Getting second u')
    u_2 = wrf.getvar(wrfout_2, "ua", None, units = "m/s")[:, :, y_main, x_main]
    print('Getting third u')
    u_3 = wrf.getvar(wrfout_3, "ua", None, units = "m/s")[32::, :, y_main, x_main]
    print('Getting fourth u')
    u_4 = wrf.getvar(wrfout_4, "ua", None, units = "m/s")[:, :, y_main, x_main]
    print('Getting fifth u')
    u_5 = wrf.getvar(wrfout_5, "ua", None, units = "m/s")[9::, :, y_main, x_main]
    print('Getting v from all the wrfovt files with corrected time stamp')
    v_1 = wrf.getvar(wrfout_1, "va", None, units = "m/s")[:, :, y_main, x_main]
    v_2 = wrf.getvar(wrfout_2, "va", None, units = "m/s")[:, :, y_main, x_main]
    v_3 = wrf.getvar(wrfout_3, "va", None, units = "m/s")[32::, :, y_main, x_main]
    v_4 = wrf.getvar(wrfout_4, "va", None, units = "m/s")[:, :, y_main, x_main]
    v_5 = wrf.getvar(wrfout_5, "va", None, units = "m/s")[9::, :, y_main, x_main]

    ws_1 = np.sqrt((u_1 ** 2) + (v_1 ** 2))
    ws_2 = np.sqrt((u_2 ** 2) + (v_2 ** 2))
    ws_3 = np.sqrt((u_3 ** 2) + (v_3 ** 2))
    ws_4 = np.sqrt((u_4 ** 2) + (v_4 ** 2))
    ws_5 = np.sqrt((u_5 ** 2) + (v_5 ** 2))

    time_1 = wrfout_1.variables['XTIME'][:]
    time_2 = wrfout_2.variables['XTIME'][:]
    time_3 = wrfout_3.variables['XTIME'][32::]
    time_4 = wrfout_4.variables['XTIME'][:]
    time_5 = wrfout_5.variables['XTIME'][9::]


    results = {'time_1':time_1, 'time_2':time_2, 'time_3':time_3, 'time_4':time_4,
    'time_5':time_5, 'ws_1':ws_1, 'ws_2':ws_2, 'ws_3':ws_3, 'ws_4':ws_4, 'ws_5':ws_5}
    with open(out_path, 'wb') as f:
        pickle.dump(results, f)
else:
    with open(out_path, 'rb') as f:
        results = pickle.load(f)
    locals().update(results)
# %% Making the arrays
ws_h_533 = np.concatenate((ws_1[:, 2], ws_2[:, 2], ws_3[:, 2], ws_4[:, 2], ws_5[:, 2]), axis = 0)
ws_h_10 = np.concatenate((ws_1[:, 4], ws_2[:, 4], ws_3[:, 4], ws_4[:, 4], ws_5[:, 4]), axis = 0)
ws_h_20 = np.concatenate((ws_1[:, 7], ws_2[:, 7], ws_3[:, 7], ws_4[:, 7], ws_5[:, 7]), axis = 0)
time = np.concatenate((time_1[:], time_2[:], time_3[:], time_4[:], time_5[:]), axis = 0)
time *= 60

# %% Creating the plots
main_tower1 = pd.read_csv('/home/jbenik/FireFlux2/Codes_and_Data/Data/Main_Tower_Data/Proc_FF2_10HzMTdespiked_rotated.csv', parse_dates=['TIMESTAMP'], skiprows = (0, 2, 3))

main_tower = main_tower1.truncate(before= np.where(main_tower1['TIMESTAMP'] == '1/30/2013  15:00:00')[0][0], 
                    after=np.where(main_tower1['TIMESTAMP'] == '1/30/2013  15:30:00')[0][0])
# Main tower variables
print("Getting the variables from the main tower data")
time_main_tower = main_tower['TIMESTAMP']
time_main = np.arange(1200, 3000.1, .1)
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



fig, ax = plt.subplots(3, figsize = (12,10))

# 5.33 Meter plot
plt.suptitle('Simulated Main Tower Winds From Open Boundary Fire Run', fontsize = 18, fontweight = 'bold')
ax[0].plot(time, ws_h_20, color = 'red', label = 'Simulated Winds')
#ax[0].plot(time_main, ws_20, color = 'green', label = 'Main Tower Winds')
ax[0].set_ylabel('Wind Speeds (m/s)', fontsize = 12, fontweight = 'bold')
ax[0].set_title('Simulated Winds at 19.30m', fontsize = 18, fontweight = 'bold')
ax[0].set_xlabel('Time (S)', fontsize = 12, fontweight = 'bold')
ax[0].legend()
ax[0].grid()
#ax[0].set_xlim(1150, 1400)

ax[1].plot(time, ws_h_10, color = 'red', label = 'Simulated Winds')
#ax[1].plot(time_main, ws_10, color = 'green', label = 'Main Tower Winds')
ax[1].set_ylabel('Wind Speeds (m/s)', fontsize = 12, fontweight = 'bold')
ax[1].set_title('Simulated Winds at 10.76m', fontsize = 18, fontweight = 'bold')
ax[1].set_xlabel('Time (S)', fontsize = 12, fontweight = 'bold')
ax[1].legend()
ax[1].grid()
#ax[1].set_xlim(1150, 1400)

ax[2].plot(time, ws_h_533, color = 'red', label = 'Simulated Winds')
#ax[2].plot(time_main, ws_6, color = 'green', label = 'Main Tower Winds')
ax[2].set_ylabel('Wind Speeds (m/s)', fontsize = 12, fontweight = 'bold')
ax[2].set_title('Simulated Winds at 5.70m', fontsize = 18, fontweight = 'bold')
ax[2].set_xlabel('Time (S)', fontsize = 12, fontweight = 'bold')
ax[2].legend()
ax[2].grid()
#ax[2].set_xlim(1150, 1400)

plt.tight_layout()
#plt.savefig('/home/jbenik/fireflux_med/images/u_and_v_cyclic_no_fire.png')
plt.show()

# %%
