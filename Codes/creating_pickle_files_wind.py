# %% 
import netCDF4 as nc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import os.path as osp
import wrf
import statistics as st
# %% Gathering locations of the towers
# %%
y_main = int(190 / 2)
x_main = int(93 / 2)

# East tower
y_east = int(158 / 2)
x_east = int(117 / 2)

# West tower
y_west = int(151 / 2)
x_west = int(94 / 2)

# South tower
y_south = int(119 / 2)
x_south = int(115 / 2)


# %% Defining a function to read in the files and create pickle files from it
def pick(path1, path2, path3, path4, picklepath):
    # Reading in the variables
    file_1 = nc.Dataset(path1)
    file_2 = nc.Dataset(path2)
    file_3 = nc.Dataset(path3)
    file_4 = nc.Dataset(path4)

    # Finding where the file times match
    l = np.where(float(file_2.variables['XTIME'][-1]) == np.array(file_3.variables['XTIME'][:]))[0][0] + 1
    # finding the time where they match
    print('Running this here so I can get it all done in one run')
    print('Getting u from the first wrfout file')
    u_main_1 = wrf.getvar(file_1, "ua", None, units = "m/s")[:, :, :, :]
    print('Getting u from the second wrfout file')
    u_main_2 = wrf.getvar(file_2, "ua", None, units = "m/s")[:, :, :, :]
    print('Getting u from the third wrfout file')
    u_main_3 = wrf.getvar(file_3, "ua", None, units = "m/s")[l::, :, :, :]
    print('Getting u from the fourth wrfout file')
    u_main_4 = wrf.getvar(file_4, "ua", None, units = "m/s")[:, :, :, :]

    u_main = np.concatenate((u_main_1, u_main_2, u_main_3, u_main_4), axis = 0)
    print('Reading in height from file 1')
    ht_1 = wrf.getvar(file_1, "z", units="m", msl = False)[:, :, :]
    print('Getting v from the first wrfout file')
    v_main_1 = wrf.getvar(file_1, "va", None, units = "m/s")[:, :, :, :]
    print('Getting v from the second wrfout file')
    v_main_2 = wrf.getvar(file_2, "va", None, units = "m/s")[:, :, :, :]
    print('Getting v from the third wrfout file')
    v_main_3 = wrf.getvar(file_3, "va", None, units = "m/s")[l::, :, :, :]
    print('Getting v from the fourth wrfout file')
    v_main_4 = wrf.getvar(file_4, "va", None, units = "m/s")[:, :, :, :]
    print('Getting v from the fifth wrfout file')
    v_main = np.concatenate((v_main_1, v_main_2, v_main_3, v_main_4), axis = 0)

    out_path = picklepath + '/main_U.pkl'
    if not osp.exists(out_path):
        U_h_20 = wrf.interplevel(u_main, ht_1, 20)[:, y_main, x_main]
        U_h_10 = wrf.interplevel(u_main, ht_1, 10)[:, y_main, x_main]
        U_h_577 = wrf.interplevel(u_main, ht_1, 5.77)[:, y_main, x_main]
        results = {'U_h_20':U_h_20, 'U_h_10':U_h_10, 'U_h_577':U_h_577}
        with open(out_path, 'wb') as f:
            pickle.dump(results, f)
    else:
        with open(out_path, 'rb') as f:
            results = pickle.load(f)
        locals().update(results)


    out_path = picklepath + '/main_V.pkl'
    if not osp.exists(out_path):
        V_h_20 = wrf.interplevel(v_main, ht_1, 20)[:, y_main, x_main]
        V_h_10 = wrf.interplevel(v_main, ht_1, 10)[:, y_main, x_main]
        V_h_577 = wrf.interplevel(v_main, ht_1, 5.77)[:, y_main, x_main]
        results = {'V_h_20':V_h_20, 'V_h_10':V_h_10, 'V_h_577':V_h_577}
        with open(out_path, 'wb') as f:
            pickle.dump(results, f)
    else:
        with open(out_path, 'rb') as f:
            results = pickle.load(f)
        locals().update(results)


    out_path = picklepath + '/time.pkl'
    if not osp.exists(out_path):

        time_1 = file_1.variables['XTIME'][:]
        time_2 = file_2.variables['XTIME'][:]
        time_3 = file_3.variables['XTIME'][l::]
        time_4 = file_4.variables['XTIME'][:]

        time_sim = np.concatenate((time_1, time_2, time_3, time_4), axis = 0)
        results = {'time_sim':time_sim}

        with open(out_path, 'wb') as f:
            pickle.dump(results, f)
    else:
        with open(out_path, 'rb') as f:
            results = pickle.load(f)
        locals().update(results)

    out_path = picklepath + '/U_west.pkl'
    if not osp.exists(out_path):
        U_west_533 = wrf.interplevel(u_main, ht_1, 5.33)[:, y_west, x_west]
        results = {'U_west_533':U_west_533}
        with open(out_path, 'wb') as f:
            pickle.dump(results, f)
    else:
        with open(out_path, 'rb') as f:
            results = pickle.load(f)
        locals().update(results)


    out_path = picklepath + '/V_west.pkl'
    if not osp.exists(out_path):
        V_west_533 = wrf.interplevel(v_main, ht_1, 5.33)[:, y_west, x_west]
        results = {'V_west_533':V_west_533}
        with open(out_path, 'wb') as f:
            pickle.dump(results, f)
    else:
        with open(out_path, 'rb') as f:
            results = pickle.load(f)
        locals().update(results)
    

    out_path = picklepath + '/U_south.pkl'
    if not osp.exists(out_path):
        U_south_533 = wrf.interplevel(u_main, ht_1, 5.33)[:, y_south, x_south]
        results = {'U_south_533':U_south_533}
        with open(out_path, 'wb') as f:
            pickle.dump(results, f)
    else:
        with open(out_path, 'rb') as f:
            results = pickle.load(f)
        locals().update(results)


    out_path = picklepath + '/V_south.pkl'
    if not osp.exists(out_path):
        V_south_533 = wrf.interplevel(v_main, ht_1, 5.33)[:, y_south, x_south]
        results = {'V_south_533':V_south_533}
        with open(out_path, 'wb') as f:
            pickle.dump(results, f)
    else:
        with open(out_path, 'rb') as f:
            results = pickle.load(f)
        locals().update(results)


    out_path = picklepath + '/U_east.pkl'
    if not osp.exists(out_path):
        U_east_528 = wrf.interplevel(u_main, ht_1, 5.28)[:, y_east, x_east]
        results = {'U_east_528':U_east_528}
        with open(out_path, 'wb') as f:
            pickle.dump(results, f)
    else:
        with open(out_path, 'rb') as f:
            results = pickle.load(f)
        locals().update(results)


    out_path = picklepath + '/V_east.pkl'
    if not osp.exists(out_path):
        V_east_528 = wrf.interplevel(v_main, ht_1, 5.28)[:, y_east, x_east]
        results = {'V_east_528':V_east_528}
        with open(out_path, 'wb') as f:
            pickle.dump(results, f)
    else:
        with open(out_path, 'rb') as f:
            results = pickle.load(f)
        locals().update(results)

# %% Creating the program for 2 files
def pick2(path1, path2, picklepath):
    # Reading in the variables
    file_1 = nc.Dataset(path1)
    file_2 = nc.Dataset(path2)

    # finding the time where they match
    print('Running this here so I can get it all done in one run')
    print('Getting u from the first wrfout file')
    u_main_1 = wrf.getvar(file_1, "ua", None, units = "m/s")[:, :, :, :]
    print('Getting u from the second wrfout file')
    u_main_2 = wrf.getvar(file_2, "ua", None, units = "m/s")[:, :, :, :]

    u_main = np.concatenate((u_main_1, u_main_2), axis = 0)
    print('Reading in height from file 1')
    ht_1 = wrf.getvar(file_1, "z", units="m", msl = False)[:, :, :]
    print('Getting v from the first wrfout file')
    v_main_1 = wrf.getvar(file_1, "va", None, units = "m/s")[:, :, :, :]
    print('Getting v from the second wrfout file')
    v_main_2 = wrf.getvar(file_2, "va", None, units = "m/s")[:, :, :, :]
    v_main = np.concatenate((v_main_1, v_main_2), axis = 0)

    out_path = picklepath + '/main_U.pkl'
    if not osp.exists(out_path):
        U_h_20 = wrf.interplevel(u_main, ht_1, 20)[:, y_main, x_main]
        U_h_10 = wrf.interplevel(u_main, ht_1, 10)[:, y_main, x_main]
        U_h_577 = wrf.interplevel(u_main, ht_1, 5.77)[:, y_main, x_main]
        results = {'U_h_20':U_h_20, 'U_h_10':U_h_10, 'U_h_577':U_h_577}
        with open(out_path, 'wb') as f:
            pickle.dump(results, f)
    else:
        with open(out_path, 'rb') as f:
            results = pickle.load(f)
        locals().update(results)


    out_path = picklepath + '/main_V.pkl'
    if not osp.exists(out_path):
        V_h_20 = wrf.interplevel(v_main, ht_1, 20)[:, y_main, x_main]
        V_h_10 = wrf.interplevel(v_main, ht_1, 10)[:, y_main, x_main]
        V_h_577 = wrf.interplevel(v_main, ht_1, 5.77)[:, y_main, x_main]
        results = {'V_h_20':V_h_20, 'V_h_10':V_h_10, 'V_h_577':V_h_577}
        with open(out_path, 'wb') as f:
            pickle.dump(results, f)
    else:
        with open(out_path, 'rb') as f:
            results = pickle.load(f)
        locals().update(results)


    out_path = picklepath + '/time.pkl'
    if not osp.exists(out_path):

        time_1 = file_1.variables['XTIME'][:]
        time_2 = file_2.variables['XTIME'][:]

        time_sim = np.concatenate((time_1, time_2), axis = 0)
        results = {'time_sim':time_sim}

        with open(out_path, 'wb') as f:
            pickle.dump(results, f)
    else:
        with open(out_path, 'rb') as f:
            results = pickle.load(f)
        locals().update(results)

    out_path = picklepath + '/U_west.pkl'
    if not osp.exists(out_path):
        U_west_533 = wrf.interplevel(u_main, ht_1, 5.33)[:, y_west, x_west]
        results = {'U_west_533':U_west_533}
        with open(out_path, 'wb') as f:
            pickle.dump(results, f)
    else:
        with open(out_path, 'rb') as f:
            results = pickle.load(f)
        locals().update(results)


    out_path = picklepath + '/V_west.pkl'
    if not osp.exists(out_path):
        V_west_533 = wrf.interplevel(v_main, ht_1, 5.33)[:, y_west, x_west]
        results = {'V_west_533':V_west_533}
        with open(out_path, 'wb') as f:
            pickle.dump(results, f)
    else:
        with open(out_path, 'rb') as f:
            results = pickle.load(f)
        locals().update(results)
    

    out_path = picklepath + '/U_south.pkl'
    if not osp.exists(out_path):
        U_south_533 = wrf.interplevel(u_main, ht_1, 5.33)[:, y_south, x_south]
        results = {'U_south_533':U_south_533}
        with open(out_path, 'wb') as f:
            pickle.dump(results, f)
    else:
        with open(out_path, 'rb') as f:
            results = pickle.load(f)
        locals().update(results)


    out_path = picklepath + '/V_south.pkl'
    if not osp.exists(out_path):
        V_south_533 = wrf.interplevel(v_main, ht_1, 5.33)[:, y_south, x_south]
        results = {'V_south_533':V_south_533}
        with open(out_path, 'wb') as f:
            pickle.dump(results, f)
    else:
        with open(out_path, 'rb') as f:
            results = pickle.load(f)
        locals().update(results)


    out_path = picklepath + '/U_east.pkl'
    if not osp.exists(out_path):
        U_east_528 = wrf.interplevel(u_main, ht_1, 5.28)[:, y_east, x_east]
        results = {'U_east_528':U_east_528}
        with open(out_path, 'wb') as f:
            pickle.dump(results, f)
    else:
        with open(out_path, 'rb') as f:
            results = pickle.load(f)
        locals().update(results)


    out_path = picklepath + '/V_east.pkl'
    if not osp.exists(out_path):
        V_east_528 = wrf.interplevel(v_main, ht_1, 5.28)[:, y_east, x_east]
        results = {'V_east_528':V_east_528}
        with open(out_path, 'wb') as f:
            pickle.dump(results, f)
    else:
        with open(out_path, 'rb') as f:
            results = pickle.load(f)
        locals().update(results)
# %% 10_01 modified sounding
'''
pick('../simulations/10_01_22_smooth_sodar_modified_20_min_ws_averages_6m_ext_03_z0/wrfout_d01_2013-01-30_14:50:00',
'../simulations/10_01_22_smooth_sodar_modified_20_min_ws_averages_6m_ext_03_z0/wrfout_d01_2013-01-30_15:06:40',
'../simulations/10_01_22_smooth_sodar_modified_20_min_ws_averages_6m_ext_03_z0/wrfout_d01_2013-01-30_15:12:01',
'../simulations/10_01_22_smooth_sodar_modified_20_min_ws_averages_6m_ext_03_z0/wrfout_d01_2013-01-30_15:28:41',
'pickle_files/10_01_22_modified_sounding')
# %% 10_01 base sounding
pick('../simulations/10_01_22_smooth_sodar_20_min_ws_averages_6m_ext_03_z0/wrfout_d01_2013-01-30_14:50:00',
'../simulations/10_01_22_smooth_sodar_20_min_ws_averages_6m_ext_03_z0/wrfout_d01_2013-01-30_15:06:40',
'../simulations/10_01_22_smooth_sodar_20_min_ws_averages_6m_ext_03_z0/wrfout_d01_2013-01-30_15:10:01',
'../simulations/10_01_22_smooth_sodar_20_min_ws_averages_6m_ext_03_z0/wrfout_d01_2013-01-30_15:26:41',
'pickle_files/10_01_22_base_sounding')

# %% 10_01 match ff2
pick('../simulations/10_01_22_modified_20_min_averages_match_ff2_sim/wrfout_d01_2013-01-30_14:50:00',
'../simulations/10_01_22_modified_20_min_averages_match_ff2_sim/wrfout_d01_2013-01-30_15:06:40',
'../simulations/10_01_22_modified_20_min_averages_match_ff2_sim/wrfout_d01_2013-01-30_15:13:01',
'../simulations/10_01_22_modified_20_min_averages_match_ff2_sim/wrfout_d01_2013-01-30_15:29:41',
'pickle_files/10_01_22_match_ff2')
# %% 10_04 simulation

pick('../simulations/10_04_22_sim_attempt_to_match_obs_mod_sounding_1/wrfout_d01_2013-01-30_14:50:00',
'../simulations/10_04_22_sim_attempt_to_match_obs_mod_sounding_1/wrfout_d01_2013-01-30_15:06:40',
'../simulations/10_04_22_sim_attempt_to_match_obs_mod_sounding_1/wrfout_d01_2013-01-30_15:09:01',
'../simulations/10_04_22_sim_attempt_to_match_obs_mod_sounding_1/wrfout_d01_2013-01-30_15:25:41',
'pickle_files/10_04_22_sim_attempt_to_match_obs_mod_sounding_1')

# %% 10_05 simulation
pick('../simulations/10_05_22_sim_02_z0_modified_sounding_match_obs/wrfout_d01_2013-01-30_14:50:00',
'../simulations/10_05_22_sim_02_z0_modified_sounding_match_obs/wrfout_d01_2013-01-30_15:06:40',
'../simulations/10_05_22_sim_02_z0_modified_sounding_match_obs/wrfout_d01_2013-01-30_15:13:01',
'../simulations/10_05_22_sim_02_z0_modified_sounding_match_obs/wrfout_d01_2013-01-30_15:29:41',
'pickle_files/10_05_22_sim_attempt_to_match_obs_mod_sounding_1')

pick('../simulations/10_07_more_levels_in_sounding/wrfout_d01_2013-01-30_14:50:00',
'../simulations/10_07_more_levels_in_sounding/wrfout_d01_2013-01-30_15:06:40',
'../simulations/10_07_more_levels_in_sounding/wrfout_d01_2013-01-30_15:09:01',
'../simulations/10_07_more_levels_in_sounding/wrfout_d01_2013-01-30_15:25:41',
'pickle_files/10_07_pickle_files')

pick2('../simulations/10_10_modified_levels_in_sounding_03_z0/wrfout_d01_2013-01-30_14:50:00',
'../simulations/10_10_modified_levels_in_sounding_03_z0/wrfout_d01_2013-01-30_15:06:40',
'pickle_files/10_10_simulation')
'''
pick('../simulations/10_10_modified_levels_in_sounding_03_z0/wrfout_d01_2013-01-30_14:50:00',
'../simulations/10_10_modified_levels_in_sounding_03_z0/wrfout_d01_2013-01-30_15:06:40',
'../simulations/10_10_modified_levels_in_sounding_03_z0/wrfout_d01_2013-01-30_15:13:01',
'../simulations/10_10_modified_levels_in_sounding_03_z0/wrfout_d01_2013-01-30_15:29:41',
'pickle_files/10_10_simulation')

'''
pick2('../simulations/10_11_22_mod_sounding_03z0/wrfout_d01_2013-01-30_14:50:00', 
'../simulations/10_11_22_mod_sounding_03z0/wrfout_d01_2013-01-30_15:06:40',
'pickle_files/10_11_simulation')
'''