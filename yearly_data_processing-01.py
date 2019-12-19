# Copyright (c) 2015,2016,2017 MetPy Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
"""
=================
Advanced Sounding
=================

Plot a sounding using MetPy with more advanced features.

Beyond just plotting data, this uses calculations from `metpy.calc` to find the lifted
condensation level (LCL) and the profile of a surface-based parcel. The area between the
ambient profile and the parcel profile is colored as well.

conda install -c conda-forge metpy

#https://unidata.github.io/MetPy/latest/api/generated/metpy.calc.html

"""

from glob import glob
import os
import numpy as np
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import metpy.calc as mpcalc
#from metpy.cbook import get_test_data
#from metpy.plots import add_metpy_logo, SkewT
from metpy.units import units

add_log = True
if add_log == True :
    log_file = 'yearly_data_processing.log'
    err_log_file = 'yearly_data_processing_err.log'
    
def write_log(log_file, log_str):
    with open(log_file, 'a') as log_f:
        log_f.write(log_str+'\n')
    return print (log_str)
#for checking time
cht_start_time = datetime.now()
def print_working_time():
    working_time = (datetime.now() - cht_start_time) #total days for downloading
    return print('working time ::: %s' % (working_time))

###########################################
# Upper air data can be obtained using the siphon package, but for this example we will use
# some of MetPy's sample data.

base_dir_name = '../yearly_data/'

save_base_dir_name = '../1data/'
if not os.path.exists('{0}'.format(save_base_dir_name)):
    os.makedirs('{0}'.format(save_base_dir_name))
    print ('*'*80)
    print ('{0} is created'.format(save_base_dir_name))
else :
    print ('*'*80)
    print ('{0} is exist'.format(save_base_dir_name))
            

dir_names = ['47090/', '47102/', '47104/', '47122/', '47138/', 
             '47155/', '47158/', '47169/', '47185/', '47186/']


for dir_name in dir_names:
        
    #filename = 'UPPER_SONDE_47122_ALL_2018_2018_2019.csv'
    
    for fullname in sorted(glob(os.path.join(base_dir_name+dir_name, '*.csv'))):
        fullname_el = fullname.split('/')
        #fullname_el = fullname.split('\\')
        filename = fullname_el[-1]
        filename_el = filename.split('_')
        obs_year = int(filename_el[-3])
        
        save_dir_name = '{0}{1}/'.format(save_base_dir_name+dir_name,obs_year)
    
        if not os.path.exists('{0}'.format(save_dir_name)):
            os.makedirs('{0}'.format(save_dir_name))
            print ('*'*80)
            print ('{0} is created'.format(save_dir_name))
        else :
            print ('*'*80)
            print ('{0} is exist'.format(save_dir_name))
            
        #######################################################################################
        ###지점,일시(UTC),기압(hPa),고도(gpm),기온(°C),이슬점온도(°C),풍향(deg),풍속(knot),
        ###지상 FLAG(null),권계면 FLAG(null),최대풍 FLAG(null)
        df = pd.read_csv(base_dir_name+dir_name+filename, skiprows=1, sep=',', header=None, index_col=0,
                           names = ['site', 'time', 'pressure', 'height', 'temperature', 
                                    'dewpoint', 'direction', 'speed', 'FLAG1', 'FLAG2', 'FLAG3'],
                           skipfooter=0, engine='python')
        
        df['u_wind'], df['v_wind'] = mpcalc.wind_components(df['speed'].values * units.knots, 
                                            np.deg2rad(df['direction'].values * units.deg))
        
        # Drop any rows with all NaN values for T, Td
        df = df.dropna(subset=('temperature', 'dewpoint'), how='all').reset_index(drop=True)

        # Rows that do not meet the condition alpha + num are eliminated
        s_start_date = datetime(obs_year, 1, 1) #convert startdate to date type
        s_end_date = datetime(obs_year+1, 1, 1)
        
        selected_times = []
        while s_start_date < s_end_date : 
            date1_strf = s_start_date.strftime('%Y-%m-%d %H:%M')
            selected_times.append(date1_strf)
            s_start_date = s_start_date + relativedelta(hours=6)
        
        for selected_time in selected_times:
            print('site : {0}'.format(dir_name))
            print('selected_time.\n {0}'.format(selected_time))
            
            if os.path.isfile('{0}{1}_{2}_student.csv'\
                      .format(save_dir_name, filename_el[-5], selected_time[:13]))\
                and os.path.isfile('{0}{1}_{2}_solution.csv'\
                      .format(save_dir_name, filename_el[-5], selected_time[:13])):
                write_log(log_file, '{3} ::: {0}{1}_{2} files are already exist'\
                      .format(save_dir_name, filename_el[-5], selected_time[:13], datetime.now()))
            else : 
                try : 
                    f = lambda s: selected_time in s
                    ids  = df['time'].apply(f)
                    df_selected_time = df[ids]
                    df_selected_time = df_selected_time.sort_values('pressure', ascending=False)
                    
                    print('filename : {0}'.format(fullname))
                    print('df_selected_time.\n{0}'.format(df_selected_time))
                    
                    df_selected_time.to_csv(r'{0}{1}_{2}_student.csv'\
                              .format(save_dir_name, filename_el[-5], selected_time[:13]))
                    
                    #################################################################################
                    ### We will pull the data out of the example dataset into individual variables and
                    ### assign units.
                    #################################################################################
                    
                    p = df_selected_time['pressure'].values * units.hPa
                    T = df_selected_time['temperature'].values * units.degC
                    Td = df_selected_time['dewpoint'].values * units.degC
                    wind_speed = df_selected_time['speed'].values * units.knots
                    wind_dir = df_selected_time['direction'].values * units.degrees
                    u, v = mpcalc.wind_components(wind_speed, wind_dir)
                                        
                    # Calculate web bulb temperature
                    df_selected_time['wet_bulb_T'] = mpcalc.wet_bulb_temperature(p, T, Td)
                    
                    # Calculate potential temperature
                    df_selected_time['potential_T'] = mpcalc.potential_temperature(p, T)
                    df_selected_time['potential_T_C'] = df_selected_time['potential_T'].values - 273.15
                    
                    # Calculate saturation vaper pressure
                    df_selected_time['saturation_vaper_pressure'] = mpcalc.saturation_vapor_pressure(T)
                    df_selected_time['vaper_pressure']  = mpcalc.saturation_vapor_pressure(Td)
                    SVP = df_selected_time['saturation_vaper_pressure'].values * units.hPa
                    VP = df_selected_time['vaper_pressure'].values * units.hPa
                    
                    # Calculate mixing ratio
                    df_selected_time['saturation_mixing_ratio'] = mpcalc.mixing_ratio(SVP, p)
                    df_selected_time['mixing_ratio'] = mpcalc.mixing_ratio(VP, p)
                    SMR = df_selected_time['saturation_mixing_ratio'].values * units('g/kg')
                    MR = df_selected_time['mixing_ratio'].values * units('g/kg')
                    
                    # Calculate relative humidity
                    df_selected_time['relative_humidity_from_dewpoint'] \
                        = mpcalc.relative_humidity_from_dewpoint(T, Td)
                    df_selected_time['relative_humidity_from_mixing_ratio'] \
                        = mpcalc.relative_humidity_from_mixing_ratio(MR, T, p) 
                    
                    # Calculate virtual temperature
                    df_selected_time['virtual_temperature'] \
                        = mpcalc.virtual_temperature(T, MR)
                        
                    # Calculate virtual potential temperature
                    df_selected_time['virtual_potential_temperature'] \
                        = mpcalc.virtual_potential_temperature(p, T, MR)
                                 
                    print('df_selected_time after drop nan.\n{0}'.format(df_selected_time))
                            
                    df_selected_time.to_csv(r'{0}{1}_{2}_solution.csv'\
                            .format(save_dir_name, filename_el[-5], selected_time[:13]))
        
                except Exception as err :
                    write_log(err_log_file, '{4} ::: {0} with {1}{2} on {3}'\
                              .format(err, dir_name, filename, selected_time[:13], datetime.now()))