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

conda install -c conda-forge metpy=0.10.2

conda install -c conda-forge xarray=0.12.3

#https://unidata.github.io/MetPy/latest/api/generated/metpy.calc.html

"""

import matplotlib.pyplot as plt
from glob import glob
import os
import numpy as np
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import metpy.calc as mpcalc
#from metpy.cbook import get_test_data
#from metpy.plots import add_metpy_logo, SkewT
from metpy.plots import SkewT
from metpy.units import units

#%%
add_log = True
if add_log == True :
    log_file = 'metpy_python.log'
    err_log_file = 'metpy_python_err.log'
    
def write_log(log_file, log_str):
    with open(log_file, 'a') as log_f:
        log_f.write(log_str+'\n')
    return print (log_str)
#for checking time
cht_start_time = datetime.now()
def print_working_time():
    working_time = (datetime.now() - cht_start_time) #total days for downloading
    return print('working time ::: %s' % (working_time))

#%%
###########################################
# Upper air data can be obtained using the siphon package, but for this example we will use
# some of MetPy's sample data.
dir_name = '../47138/'

dir_names = ['../47090/', '../47012/', '../47104/', '../47122/', '../47138/', '../47155/', '../47158/', '../47169/', '../47185/', '../47186/']

for dir_name in dir_names:
        
    filename = 'UPPER_SONDE_47122_ALL_2018_2018_2019.csv'
    
    #%%
    for fullname in sorted(glob(os.path.join(dir_name, '*.csv'))):
        fullname_el = fullname.split('/')
        filename = fullname_el[-1]
        filename_el = filename.split('_')
        obs_year = int(filename_el[-3])
        
        save_dir_name = 'skew_T-log_P-diagram_{0}/'.format(obs_year)
    
        if not os.path.exists(dir_name+save_dir_name):
            os.makedirs(dir_name+save_dir_name)
            print ('*'*80)
            print (dir_name+save_dir_name, 'is created')
        else :
            print ('*'*80)
            print (dir_name+save_dir_name, 'is exist')
    
        #지점,일시(UTC),기압(hPa),고도(gpm),기온(°C),이슬점온도(°C),풍향(deg),풍속(knot),지상 FLAG(null),권계면 FLAG(null),최대풍 FLAG(null)
        df = pd.read_csv(dir_name+filename, skiprows=1, sep=',', header=None, index_col=0,
                           names = ['site', 'time', 'pressure', 'height', 'temperature', 'dewpoint', 'direction', 'speed', 'FLAG1', 'FLAG2', 'FLAG3'],
                           skipfooter=1, engine='python')
        
        df['u_wind'], df['v_wind'] = mpcalc.wind_components(df['speed'],
                                                            np.deg2rad(df['direction']))
        
        # Drop any rows with all NaN values for T, Td, winds
        #df = df.dropna(subset=('temperature', 'dewpoint', 'direction', 'speed', 'u_wind', 'v_wind'), how='all').reset_index(drop=True)
        df = df.dropna(subset=('temperature', 'dewpoint'), how='all').reset_index(drop=True)
        #df = df.dropna(subset=('temperature', 'dewpoint', 'height'), how='all').reset_index(drop=True)

        # Rows that do not meet the condition alpha + num are eliminated
        s_start_date = datetime(obs_year, 1, 1) #convert startdate to date type
        s_end_date = datetime(obs_year+1, 1, 1)
        
        date1 = s_start_date
        selected_times = []
        while date1 < s_end_date : 
            date1_strf = date1.strftime('%Y-%m-%d %H:%M')
            selected_times.append(date1_strf)
            date1 = date1 + relativedelta(hours=12)
        
        for selected_time in selected_times:
            print('site : {0}'.format(dir_name))
            print('selected_time.\n {0}'.format(selected_time))
            
            if os.path.isfile('{0}{1}{2}_{3}_solution.pdf'.format(dir_name, save_dir_name, filename_el[-5], selected_time[:13])) \
            and os.path.isfile('{0}{1}{2}_{3}_solution.png'.format(dir_name, save_dir_name, filename_el[-5], selected_time[:13])) \
            and os.path.isfile('{0}{1}{2}_{3}_student.csv'.format(dir_name, save_dir_name, filename_el[-5], selected_time[:13])) :
                write_log(log_file, '{4} ::: {0}{1}{2}_{3}_solution files are already exist'.format(dir_name, save_dir_name, filename_el[-5], selected_time[:13], datetime.now()))
            else : 
                try : 
                    f = lambda s: selected_time in s
                    ids  = df['time'].apply(f)
                    df_selected_time = df[ids]
                    
                    #df_selected_time = df_selected_time.dropna()
                    df_selected_time = df_selected_time.sort_values('pressure', ascending=False)
                    print('df_selected_time.\n{0}'.format(df_selected_time))
                    
                    df_selected_time.to_csv(r'{0}{1}{2}_{3}_student.csv'.format(dir_name, save_dir_name, filename_el[-5], selected_time[:13]))
                    ###########################################
                    # We will pull the data out of the example dataset into individual variables and
                    # assign units.
                    
                    p = df_selected_time['pressure'].values * units.hPa
                    T = df_selected_time['temperature'].values * units.degC
                    Td = df_selected_time['dewpoint'].values * units.degC
                    wind_speed = df_selected_time['speed'].values * units.knots
                    wind_dir = df_selected_time['direction'].values * units.degrees
                    u, v = mpcalc.wind_components(wind_speed, wind_dir)
        
                    # Calculate RH
                    #RH = mpcalc.relative_humidity_from_dewpoint(T[0], Td[0])
                    df_selected_time['RH'] = mpcalc.relative_humidity_from_dewpoint(T, Td)
                    
                    # Calculate potential temperature
                    #potential_T = mpcalc.potential_temperature(p[1], T[10])
                    df_selected_time['potential_T'] = mpcalc.potential_temperature(p, T)
                    print('df_selected_time after drop nan.\n{0}'.format(df_selected_time))
                                    
                    df_selected_time.to_csv(r'{0}{1}{2}_{3}_solution.csv'.format(dir_name, save_dir_name, filename_el[-5], selected_time[:13]))
                    
                    ###########################################
                    # Create a new figure. The dimensions here give a good aspect ratio.
                    fig = plt.figure(figsize=(12, 16))          
                    #add_metpy_logo(fig, 115, 100)
                    skew = SkewT(fig, rotation=45)
                    
                    skew.ax.set_title('skew T log p diagram\n', fontsize=24)            
                    skew.ax.set_xlabel(r'temperature ($ \degree C$)', fontsize=18)
                    skew.ax.set_ylabel(r'pressure ($ hPa $)', fontsize=18)
                    
        
                    # Plot the data using normal plotting functions, in this case using
                    # log scaling in Y, as dictated by the typical meteorological plot
                    skew.plot(p, T, 'r')
                    skew.plot(p, T, 'ro', markersize = 8, fillstyle='none', label='temperature')
                    skew.plot(p, Td, 'g', linestyle='--')
                    skew.plot(p, Td, 'g^', markersize = 8, fillstyle='none', label='dew point temperature')
                    skew.plot_barbs(p, u, v)
                    
                    skew.ax.set_ylim(1050, 100)
                    skew.ax.set_xlim(-50, 60)
                    skew.ax.tick_params(axis="x", labelsize=14, pad=10, rotation=45, labelcolor='cyan')
                    skew.ax.tick_params(axis="y", labelsize=14, pad=0.5)
                    
                    # Calculate full parcel profile and add to plot as black line
                    prof_0 = mpcalc.parcel_profile(p, T[0], Td[0]).to('degC')
                    skew.plot(p, prof_0, 'k', linewidth=1.5)
                    
                    # Shade areas of CAPE and CIN
                    '''
                    Calculate the convective available potential energy (CAPE) and convective inhibition (CIN) 
                    of a given upper air profile and most unstable parcel path. 
                    CIN is integrated between the surface and LFC, 
                    CAPE is integrated between the LFC and EL (or top of sounding). 
                    Intersection points of the measured temperature profile and parcel profile are linearly interpolated.
                    '''
                    skew.shade_cin(p, T, prof_0)
                    skew.shade_cape(p, T, prof_0)
                    
                    #prof = mpcalc.parcel_profile(p, T, Td).to('degC')
                    #skew.plot(p, prof, 'b', linewidth=1.5)
        
                    # Calculate LCL height and plot as black dot
                    lcl_pressure, lcl_temperature = mpcalc.lcl(p[0], T[0], Td[0])
                    skew.plot(lcl_pressure, lcl_temperature, 'ko', markersize = 8, fillstyle='none', label='LCL')
                    
                    # Calculate LCF height and plot as purple dot
                    LCF_pressure, LCF_temperature = mpcalc.lfc(p, T, Td, prof_0)
                    skew.plot(LCF_pressure, LCF_temperature, 'rx', markersize = 8, fillstyle='none', label='LCF')
                    
                    # Calculate EL height and plot as blue dot
                    EL_pressure, EL_temperature = mpcalc.el(p, T, Td, prof_0)
                    skew.plot(EL_pressure, EL_temperature, 'bo', markersize = 8, fillstyle='none', label='EL')
                    
                    # Calculate most_unstable_parcel
                    mup_pressure, mup_temperature, mup_dewTemperature, mup_index = mpcalc.most_unstable_parcel(p, T, Td, heights=prof_0, bottom=1050 * units.hPa, depth=650 * units.hPa)
                    skew.plot(p[mup_index-1:mup_index+1], T[mup_index-1:mup_index+1], 'b', label='the most unstable level')
                    #skew.plot(p[mup_index-1:mup_index+1], 'b', label='the most unstable parcel')
                                
                    # An example of a slanted line at constant T -- in this case the 0
                    # isotherm
                    skew.ax.axvline(0, color='c', linestyle='-', linewidth=1, label='isothermal')
                    for i in range(23) :
                        for j in range(2,11,2) :
                            skew.ax.axvline(i*10-160+j, color='c', linestyle='-', linewidth=0.3)
                        skew.ax.axvline(i*10-160, color='c', linestyle='-', linewidth=1)
                
                    # Add the relevant special lines
                    skew.plot_dry_adiabats(t0=np.arange(-50, 160, 2) * units.degC, color='green', linestyle='-', linewidth=0.3)
                    skew.plot_dry_adiabats(color='green', linestyle='-', linewidth=1.5, label='dry adiabat')
                    skew.plot_moist_adiabats(t0=np.arange(-50, 160, 2) * units.degC, color='brown', linestyle='-', linewidth=0.3)
                    skew.plot_moist_adiabats(color='brown', linestyle='-', linewidth=1.5, label='saturation adiabat')
                    mixing_ratio_ticks = np.array([0.0001, 0.0005, 0.001, 0.015, 0.002, 0.003, 0.005, 0.007, 0.010, 0.015, 0.020, 0.030, 0.040, 0.050]).reshape(-1, 1)
                    skew.plot_mixing_lines(w=mixing_ratio_ticks, color='blue', linestyle='--', linewidth=1.0, label='mixing ratio')
                    
                    #0.0001, 0.0005, 0.001, 0.015, 0.002, 0.003, 0.005, 0.007, 0.010, 0.015, 0.020, 0.030, 0.040, 0.050        
                    plt.text(-51, 1071, 'mixing ratio', horizontalalignment='left', verticalalignment='center', fontsize=9, color='blue')
                    plt.text(-42, 1071, '{0}'.format(mixing_ratio_ticks[0][0]), horizontalalignment='left', verticalalignment='center', fontsize=9, color='blue')
                    plt.text(-26, 1071, '{0}'.format(mixing_ratio_ticks[1][0]), horizontalalignment='left', verticalalignment='center', fontsize=9, color='blue')
                    plt.text(-17.5, 1071, '{0}'.format(mixing_ratio_ticks[2][0]), horizontalalignment='left', verticalalignment='center', fontsize=9, color='blue')
                    plt.text(-8.7, 1071, '{0}'.format(mixing_ratio_ticks[3][0]), horizontalalignment='left', verticalalignment='center', fontsize=9, color='blue')
                    plt.text(-3.2, 1071, '{0}'.format(mixing_ratio_ticks[4][0]), horizontalalignment='left', verticalalignment='center', fontsize=9, color='blue')
                    plt.text(3.5, 1071, '{0}'.format(mixing_ratio_ticks[5][0]), horizontalalignment='left', verticalalignment='center', fontsize=9, color='blue')
                    plt.text(8.5, 1071, '{0}'.format(mixing_ratio_ticks[6][0]), horizontalalignment='left', verticalalignment='center', fontsize=9, color='blue')
                    plt.text(13.5, 1071, '{0}'.format(mixing_ratio_ticks[7][0]), horizontalalignment='left', verticalalignment='center', fontsize=9, color='blue')
                    plt.text(20.2, 1071, '{0}'.format(mixing_ratio_ticks[8][0]), horizontalalignment='left', verticalalignment='center', fontsize=9, color='blue')
                    plt.text(24.7, 1071, '{0}'.format(mixing_ratio_ticks[9][0]), horizontalalignment='left', verticalalignment='center', fontsize=9, color='blue')
                    plt.text(32, 1071, '{0}'.format(mixing_ratio_ticks[10][0]), horizontalalignment='left', verticalalignment='center', fontsize=9, color='blue')
                    plt.text(36.8, 1071, '{0}'.format(mixing_ratio_ticks[11][0]), horizontalalignment='left', verticalalignment='center', fontsize=9, color='blue')
                    plt.text(40.8, 1071, '{0}'.format(mixing_ratio_ticks[12][0]), horizontalalignment='left', verticalalignment='center', fontsize=9, color='blue')
            
                    plt.text(-162.5, 93.5, '$ \cdotp $ site : {0}'.format(filename_el[-5]), horizontalalignment='left', verticalalignment='center', fontsize=10)
                    plt.text(-160.70, 97, '$ \cdotp $ time : {0} (UTC)'.format(selected_time[:16]), horizontalalignment='left', verticalalignment='center', fontsize=10)
                    
                    #for ubuntu
                    plt.text(-40, 1310, '$ \cdotp $ LCL (   ): {0:.1f}, {1:.1f}'.format(lcl_pressure, lcl_temperature), horizontalalignment='left', verticalalignment='center', fontsize=12)
                    plt.text(-38.15, 1360, '$ \cdotp $ LCF (   ): {0:.1f}, {1:.1f}'.format(LCF_pressure, LCF_temperature), horizontalalignment='left', verticalalignment='center', fontsize=12)
                    plt.text(-36.30, 1410, '$ \cdotp $ EL   (   ): {0:.1f}, {1:.1f}'.format(EL_pressure, EL_temperature), horizontalalignment='left', verticalalignment='center', fontsize=12)
                    plt.text(-33.0, 1310, 'o', horizontalalignment='left', verticalalignment='center', fontsize=12, color='black')
                    plt.text(-31.15, 1360, 'x', horizontalalignment='left', verticalalignment='center', fontsize=12, color='red')
                    plt.text(-29.30, 1410, 'o', horizontalalignment='left', verticalalignment='center', fontsize=12, color='blue')
                    #plt.text(30, 1310, '$ \cdotp $ the most unstable parcel index: {0}'.format(mup_index), horizontalalignment='left', verticalalignment='center', fontsize=12)
                    #plt.text(31.85, 1360, '     {0:.1f} ~ {1:.1f}'.format(p[mup_index-1], p[mup_index]), horizontalalignment='left', verticalalignment='center', fontsize=12)
                    plt.text(25.70, 1410, '$ \cdotp $ {0}'.format(filename), horizontalalignment='left', verticalalignment='center', fontsize=12)
                    
                    #for windows
                    #plt.text(-40, 1280, '$ \cdotp $ LCL (   ): {0:.1f}, {1:.1f}'.format(lcl_pressure, lcl_temperature), horizontalalignment='left', verticalalignment='center', fontsize=12)
                    #plt.text(-38.15, 1330, '$ \cdotp $ LCF (   ): {0:.1f}, {1:.1f}'.format(LCF_pressure, LCF_temperature), horizontalalignment='left', verticalalignment='center', fontsize=12)
                    #plt.text(-36.30, 1380, '$ \cdotp $ EL   (   ): {0:.1f}, {1:.1f}'.format(EL_pressure, EL_temperature), horizontalalignment='left', verticalalignment='center', fontsize=12)
                    #plt.text(-34.5, 1280, 'o', horizontalalignment='left', verticalalignment='center', fontsize=12, color='black')
                    #plt.text(-32.65, 1330, 'x', horizontalalignment='left', verticalalignment='center', fontsize=12, color='red')
                    #plt.text(-30.80, 1380, 'o', horizontalalignment='left', verticalalignment='center', fontsize=12, color='blue')
                    #plt.text(30, 1280, '$ \cdotp $ the most unstable parcel index: {0}'.format(mup_index), horizontalalignment='left', verticalalignment='center', fontsize=12)
                    #plt.text(31.85, 1330, '     {0:.1f} ~ {1:.1f}'.format(p[mup_index-1], p[mup_index]), horizontalalignment='left', verticalalignment='center', fontsize=12)
                    #plt.text(33.70, 1380, '$ \cdotp $ {0}'.format(filename), horizontalalignment='left', verticalalignment='center', fontsize=12)
                    
                    #plt.legend()
                    plt.legend(loc='upper left')
                    
                    plt.savefig('{0}{1}{2}_{3}_solution.png'.format(dir_name, save_dir_name, filename_el[-5], selected_time[:13]),
                        dpi=None, facecolor='w', edgecolor='w',
                        orientation='portrait', papertype=None, format=None,
                        transparent=False, bbox_inches=None, pad_inches=0.1,
                        frameon=None, metadata=None)
                    plt.savefig('{0}{1}{2}_{3}_solution.pdf'.format(dir_name, save_dir_name, filename_el[-5], selected_time[:13]),
                        dpi=None, facecolor='w', edgecolor='w',
                        orientation='portrait', papertype=None, format=None,
                        transparent=False, bbox_inches=None, pad_inches=0.1,
                        frameon=None, metadata=None)
                    write_log(log_file, '{4} ::: {0}{1}{2}_{3}_solution files are created'.format(dir_name, save_dir_name, filename_el[-5], selected_time[:13], datetime.now()))
                    # Show the plot
                    #plt.show()
                    plt.close(fig)
                
                except Exception as err :
                    write_log(err_log_file, '{4} ::: {0} with {1}{2} on {3}'.format(err, dir_name, filename, selected_time[:13], datetime.now()))