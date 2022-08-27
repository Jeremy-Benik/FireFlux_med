print('This program will read in the z_0 and ZNT value to check if they\
    are the same as the LANDUSE.TBL')
# %% Importing neccessary libraries
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import netCDF4 as nc
# %% Reading in the files
open_fire = nc.Dataset('/home/jbenik/fireflux_med/base_runs/open/wrfout_d01_2013-01-30_14:40:00')
cyclic_fire = nc.Dataset('/home/jbenik/fireflux_med/base_runs/cyclic/wrfout_d01_2013-01-30_14:40:00')
# %% Reading in the variables
y_main = int(190/2)
x_main = int(93/2)
open_z0 = open_fire.variables['Z0'][:, y_main, x_main]
open_znt = open_fire.variables['ZNT'][:, y_main, x_main]

cyclic_z0 = cyclic_fire.variables['Z0'][:, y_main, x_main]
cyclic_znt = cyclic_fire.variables['ZNT'][:, y_main, x_main]
# %% Plotting them
fig = plt.figure(figsize = (8, 8))
plt.plot(open_z0, label = 'Roughness Length')
plt.xlabel('Time (Seconds)', fontsize = 12, fontweight = 'bold')
plt.ylabel('Roughness Length (Z_0)', fontsize = 12, fontweight = 'bold')
plt.title('Roughness Length (Z_0) In The FF Med Simulation', fontsize = 18, fontweight = 'bold')
plt.legend()

plt.tight_layout()
plt.show()
#plt.plot(open_znt)
# %%
plt.plot(cyclic_z0)
plt.plot(cyclic_znt)

# %%
