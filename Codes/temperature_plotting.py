# %% Importing necessary libraries
import netCDF4 as nc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import os.path as osp
import wrf
import statistics as st
# %% Reading in the files
file_1 = nc.Dataset('/home/jbenik/fireflux_med/simulations/modified_heat_extinction_input_sounding/wrfout_d01_2013-01-30_14:50:00')
file_2 = nc.Dataset('/home/jbenik/fireflux_med/simulations/modified_heat_extinction_input_sounding/wrfout_d01_2013-01-30_15:06:40')
file_3 = nc.Dataset('/home/jbenik/fireflux_med/simulations/modified_heat_extinction_input_sounding/wrfout_d01_2013-01-30_15:13:01')
file_4 = nc.Dataset('/home/jbenik/fireflux_med/simulations/modified_heat_extinction_input_sounding/wrfout_d01_2013-01-30_15:29:41')

# %% Importing the files
print('Running this here so I can get it all done in one run')
print('Getting u from the first wrfout file')
t_main_1 = wrf.getvar(file_1, "tc", None)[:, :, :, :]
print('Getting u from the second wrfout file')
t_main_2 = wrf.getvar(file_2, "tc", None)[:, :, :, :]
print('Getting u from the third wrfout file')
t_main_3 = wrf.getvar(file_3, "tc", None)[54::, :, :, :]
print('Getting u from the fourth wrfout file')
t_main_4 = wrf.getvar(file_4, "tc", None)[:, :, :, :]
# %%
t_main = np.concatenate((t_main_1, t_main_2, t_main_3, t_main_4), axis = 0)
print('Reading in height from file 1')
ht_1 = wrf.getvar(file_1, "z", units="m", msl = False)[:, :, :]

# %%
y_main = int(190 / 2)
x_main = int(93 / 2)

# %% Getting the variables and storing them in a pickle file
out_path = 'main_tower_T_new_extinction_new_sounding'
if not osp.exists(out_path):
    
    T_h_20 = wrf.interplevel(t_main, ht_1, 20)[:, y_main, x_main]
    T_h_10 = wrf.interplevel(t_main, ht_1, 10)[:, y_main, x_main]
    T_h_577 = wrf.interplevel(t_main, ht_1, 5.77)[:, y_main, x_main]

    results = {'T_h_20':T_h_20, 'T_h_10':T_h_10, 'T_h_577':T_h_577}
    with open(out_path, 'wb') as f:
        pickle.dump(results, f)
else:
    with open(out_path, 'rb') as f:
        results = pickle.load(f)
    locals().update(results)

# %% time
out_path = 'time_V_new_extinction_new_sounding'
if not osp.exists(out_path):

    time_1 = file_1.variables['XTIME'][:]
    time_2 = file_2.variables['XTIME'][:]
    time_3 = file_3.variables['XTIME'][54::]
    time_4 = file_4.variables['XTIME'][:]

    time_sim = np.concatenate((time_1, time_2, time_3, time_4), axis = 0)
    results = {'time_sim':time_sim}

    with open(out_path, 'wb') as f:
        pickle.dump(results, f)
else:
    with open(out_path, 'rb') as f:
        results = pickle.load(f)
    locals().update(results)

# %% Creating the plots
main_tower1 = pd.read_csv('/home/jbenik/FireFlux2/Codes_and_Data/Data/Main_Tower_Data/Proc_FF2_10HzMTdespiked_rotated.csv', parse_dates=['TIMESTAMP'], skiprows = (0, 2, 3))

main_tower = main_tower1.truncate(before= np.where(main_tower1['TIMESTAMP'] == '1/30/2013  15:00:00')[0][0], 
                    after=np.where(main_tower1['TIMESTAMP'] == '1/30/2013  15:30:00')[0][0])
# Main tower variables
print("Getting the variables from the main tower data")
time_main_tower = main_tower['TIMESTAMP']
time_main = np.arange(600, 2400.1, .1)
print('20 meter variables')
ts20 = main_tower['Ts_20m']

print('10 meter variables')
ts10 = main_tower['Ts_10m']

print('5.77 meter variable')
ts6 = main_tower['Ts_6m']

# %%

fig, ax = plt.subplots(3, figsize = (12,10))
n = 50

# 5.33 Meter plot
#plt.suptitle('Simulated Main Tower Temperatures From Open Boundary Fire Run', fontsize = 18, fontweight = 'bold')
#ax[0].plot(time_main, ws_20, color = 'green', label = 'Main Tower Temperatures')
ax[0].plot(time_main, ts20.rolling(window = n).mean(), color = 'green', label = '5s Avg. Main Tower Temperatures')
ax[0].plot(time_sim * 60, T_h_20, color = 'red', label = 'Simulated Temperatures')
ax[0].axvline(x = 848, color = 'black', label = 'Ignition')
ax[0].set_ylabel('Temperature (C)', fontsize = 12, fontweight = 'bold')
ax[0].set_title('Simulated Temperatures at 20m', fontsize = 18, fontweight = 'bold')
ax[0].set_xlabel('Time (S)', fontsize = 12, fontweight = 'bold')
#ax[0].set_xlim(800, 1500)
ax[0].legend()
ax[0].grid()
#ax[0].set_xlim(1150, 1400)

#ax[1].plot(time_main, ws_10, color = 'green', label = 'Main Tower Temperatures')
ax[1].plot(time_main, ts10.rolling(window = n).mean(), color = 'green', label = '5s Avg. Main Tower Temperatures')
ax[1].plot(time_sim * 60, T_h_10, color = 'red', label = 'Simulated Temperatures')
ax[1].axvline(x = 848, color = 'black', label = 'Ignition')
ax[1].set_ylabel('Temperature (C)', fontsize = 12, fontweight = 'bold')
ax[1].set_title('Simulated Temperature at 10m', fontsize = 18, fontweight = 'bold')
ax[1].set_xlabel('Time (S)', fontsize = 12, fontweight = 'bold')
#ax[1].set_xlim(800, 1500)
ax[1].legend()
ax[1].grid()
#ax[1].set_xlim(1150, 1400)

ax[2].plot(time_main, ts6.rolling(window = n).mean(), color = 'green', label = '5s Avg. Main Tower Temperatures')
#ax[2].plot(time_main, ws_6, color = 'green', label = 'Main Tower Temperatures')
ax[2].plot(time_sim * 60, T_h_577, color = 'red', label = 'Simulated Temperatures')
ax[2].axvline(x = 848, color = 'black', label = 'Ignition')
ax[2].set_ylabel('Temperature (C)', fontsize = 12, fontweight = 'bold')
ax[2].set_title('Simulated Temperature at 5.77m', fontsize = 18, fontweight = 'bold')
ax[2].set_xlabel('Time (S)', fontsize = 12, fontweight = 'bold')
#ax[2].set_xlim(800, 1500)
ax[2].legend()
ax[2].grid()
#ax[2].set_xlim(1150, 1400)

plt.tight_layout()
#plt.savefig('/home/jbenik/fireflux_med/images/u_and_v_cyclic_no_fire.png')
plt.show()

# %%
