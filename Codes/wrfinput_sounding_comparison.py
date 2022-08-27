print('this file will be used to compare the input_sounding file to the wrfinput file')
# %% Importing necessary libraries
import netCDF4 as nc
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import wrf
# %% Reading in the files
sounding = pd.read_csv('input_sounding.csv')
cyclic = nc.Dataset('base_runs/cyclic/wrfinput_d01')
open = nc.Dataset('base_runs/open/wrfinput_d01')
# %% Reading in the variables
u_sounding = sounding['u']
v_sounding = sounding['v']
ht_sounding = sounding['ht']
ws_sounding = sounding['ws']

y_main = int(190/2)
x_main = int(93/2)


u_cyclic = cyclic.variables['U'][0, :, y_main, x_main]
v_cyclic = cyclic.variables['V'][0, :, y_main, x_main]
ws_cyclic = np.sqrt((u_cyclic ** 2) + (v_cyclic ** 2))
ph_cyclic = cyclic.variables['PH'][0, :, y_main, x_main]
phb_cyclic = cyclic.variables['PHB'][0, :, y_main, x_main]
#ht_cyclic = (ph_cyclic + phb_cyclic) / 9.81
ht_cyclic = wrf.getvar(cyclic, "z", units = "m", msl = False)[:, y_main, x_main]


u_open = open.variables['U'][0, :, y_main, x_main]
v_open = open.variables['V'][0, :, y_main, x_main]
ws_open = np.sqrt((u_open ** 2) + (v_open ** 2))
ph_open = open.variables['PH'][0, :, y_main, x_main]
phb_open = open.variables['PHB'][0, :, y_main, x_main]
ht_open = wrf.getvar(open, "z", units = "m", msl = False)[:, y_main, x_main]
#ht_open = (ph_open + phb_open) / 9.81

# %% Creating the cyclic plot
fig, ax = plt.subplots(1, 3, figsize = (10, 12))
plt.suptitle('Cyclic Boundary Conditions wrfinput vs. input_sounding', fontsize = 18, fontweight = 'bold')
ax[0].plot(u_cyclic, ht_cyclic, color = 'red', label = 'Simulated U Wind')
ax[0].plot(u_sounding, ht_sounding, color = 'blue', label = 'Observed U Wind', linestyle = '--')
ax[0].set_xlabel('U Wind', fontsize = 12, fontweight = 'bold')
ax[0].set_ylabel('Height (m)', fontsize = 12, fontweight = 'bold')
ax[0].grid()
ax[0].legend()
ax[0].set_title('U Wind', fontsize = 12, fontweight = 'bold')

ax[1].plot(v_cyclic, ht_cyclic, color = 'red', label = 'Simulated V Wind')
ax[1].plot(v_sounding, ht_sounding, color = 'blue', label = 'Observed V Wind', linestyle = '--')
ax[1].set_xlabel('V Wind', fontsize = 12, fontweight = 'bold')
ax[1].set_ylabel('Height (m)', fontsize = 12, fontweight = 'bold')
ax[1].grid()
ax[1].legend()
ax[1].set_title('V Wind', fontsize = 12, fontweight = 'bold')

ax[2].plot(ws_cyclic, ht_cyclic, color = 'red', label = 'Simulated Wind Speed')
ax[2].plot(ws_sounding, ht_sounding, color = 'blue', label = 'Observed Wind Speed', linestyle = '--')
ax[2].set_xlabel('Wind Speed', fontsize = 12, fontweight = 'bold')
ax[2].set_ylabel('Height (m)', fontsize = 12, fontweight = 'bold')
ax[2].grid()
ax[2].legend(loc = 2)
ax[2].set_title('Wind Speed', fontsize = 12, fontweight = 'bold')

plt.tight_layout()
plt.show()
# %% Creating the open plot
fig, ax = plt.subplots(1, 3, figsize = (10, 12))
plt.suptitle('Open Boundary Conditions wrfinput vs. input_sounding', fontsize = 18, fontweight = 'bold')
ax[0].plot(u_open, ht_open, color = 'red', label = 'Simulated U Wind')
ax[0].plot(u_sounding, ht_sounding, color = 'blue', label = 'Observed U Wind', linestyle = '--')
ax[0].set_xlabel('U Wind', fontsize = 12, fontweight = 'bold')
ax[0].set_ylabel('Height (m)', fontsize = 12, fontweight = 'bold')
ax[0].grid()
ax[0].legend()
ax[0].set_title('U Wind', fontsize = 12, fontweight = 'bold')

ax[1].plot(v_open, ht_open, color = 'red', label = 'Simulated V Wind')
ax[1].plot(v_sounding, ht_sounding, color = 'blue', label = 'Observed V Wind', linestyle = '--')
ax[1].set_xlabel('V Wind', fontsize = 12, fontweight = 'bold')
ax[1].set_ylabel('Height (m)', fontsize = 12, fontweight = 'bold')
ax[1].grid()
ax[1].legend()
ax[1].set_title('V Wind', fontsize = 12, fontweight = 'bold')

ax[2].plot(ws_open, ht_open, color = 'red', label = 'Simulated Wind Speed')
ax[2].plot(ws_sounding, ht_sounding, color = 'blue', label = 'Observed Wind Speed', linestyle = '--')
ax[2].set_xlabel('Wind Speed', fontsize = 12, fontweight = 'bold')
ax[2].set_ylabel('Height (m)', fontsize = 12, fontweight = 'bold')
ax[2].grid()
ax[2].legend(loc = 2)
ax[2].set_title('Wind Speed', fontsize = 12, fontweight = 'bold')

plt.tight_layout()
plt.show()
# %%
