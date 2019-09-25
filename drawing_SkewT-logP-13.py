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
#dir_name = '../47138/'

dir_names = ['../47090/', '../47102/', '../47104/', '../47122/', '../47138/', '../47155/', '../47158/', '../47169/', '../47185/', '../47186/']

#dir_names = ['../47104/', '../47122/', '../47138/']
#dir_names = ['../47155/', '../47158/', '../47169/']
#dir_names = ['../47185/', '../47186/']
xxlim = [-20, 40]
yylim = [1050, 400]
for dir_name in dir_names:
        
    filename = 'UPPER_SONDE_47122_ALL_2018_2018_2019.csv'
    
    #%%
    for fullname in sorted(glob(os.path.join(dir_name, '*.csv'))):
        fullname_el = fullname.split('/')
        #fullname_el = fullname.split('\\')
        filename = fullname_el[-1]
        filename_el = filename.split('_')
        obs_year = int(filename_el[-3])
        
        save_dir_name = '../SkewT_LogP/{0}skew_T-log_P_{2}C_{3}C_{4}_{5}hPa_{1}/'.format(dir_name[3:],obs_year, xxlim[0], xxlim[1], yylim[0], yylim[1])
    
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
            and not os.path.isfile('{0}{1}{2}_{3}_student.csv'.format(dir_name, save_dir_name, filename_el[-5], selected_time[:13])) :
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
                                        
                    # Calculate potential temperature
                    #potential_T = mpcalc.potential_temperature(p[1], T[10])
                    df_selected_time['potential_T'] = mpcalc.potential_temperature(p, T)
                    df_selected_time['potential_T_C'] = df_selected_time['potential_T'].values - 273.15
                    
                    df_selected_time['saturation_vaper_pressure'] = mpcalc.saturation_vapor_pressure(T)
                    df_selected_time['vaper_pressure']  = mpcalc.saturation_vapor_pressure(Td)
                    VPS = df_selected_time['saturation_vaper_pressure'].values * units.hPa
                    VP = df_selected_time['vaper_pressure'].values * units.hPa
                    
                    df_selected_time['saturation_mixing_ratio'] = mpcalc.mixing_ratio(VPS, p)
                    df_selected_time['mixing_ratio'] = mpcalc.mixing_ratio(VP, p)
                    MRS = df_selected_time['saturation_mixing_ratio'].values * units('g/kg')
                    MR = df_selected_time['mixing_ratio'].values * units('g/kg')
                    
                    # Calculate RH
                    #RH = mpcalc.relative_humidity_from_dewpoint(T[0], Td[0])
                    df_selected_time['RH'] = mpcalc.relative_humidity_from_dewpoint(T, Td)
                    df_selected_time['RH_MR'] = mpcalc.relative_humidity_from_mixing_ratio(MR, T, p) 
                                        
                    print('df_selected_time after drop nan.\n{0}'.format(df_selected_time))
                                    
                    df_selected_time.to_csv(r'{0}{1}{2}_{3}_solution.csv'.format(dir_name, save_dir_name, filename_el[-5], selected_time[:13]))
                    
                    p = df_selected_time['pressure'].values * units.hPa
                    T = df_selected_time['temperature'].values * units.degC
                    Td = df_selected_time['dewpoint'].values * units.degC
                    wind_speed = df_selected_time['speed'].values * units.knots
                    wind_dir = df_selected_time['direction'].values * units.degrees
                    u, v = mpcalc.wind_components(wind_speed, wind_dir)
                    
                    ###########################################
                    # Create a new figure. The dimensions here give a good aspect ratio.
                    fig = plt.figure(figsize=(24, 12))          
                    #add_metpy_logo(fig, 115, 100)
                    skew = SkewT(fig, rotation=30)
                    
                    skew.ax.set_title('skew T log p diagram\n', fontsize=30)            
                    skew.ax.set_xlabel(r'temperature ($ \degree C$)', fontsize=24)
                    skew.ax.set_ylabel(r'pressure ($ hPa $)', fontsize=24)
                    
        
                    # Plot the data using normal plotting functions, in this case using
                    # log scaling in Y, as dictated by the typical meteorological plot
                    skew.plot(p, T, 'r')
                    skew.plot(p, T, 'ro', markersize = 8, fillstyle='none', label='temperature')
                    skew.plot(p, Td, 'g', linestyle='--')
                    skew.plot(p, Td, 'g^', markersize = 8, fillstyle='none', label='dew point temperature')
                    skew.plot_barbs(p, u, v)
                    
                    skew.ax.set_ylim(yylim[0], yylim[1])
                    skew.ax.set_xlim(xxlim[0], xxlim[1])
                    skew.ax.tick_params(axis="x", labelsize=14, pad=10, rotation=45, labelcolor='brown')
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
                    skew.ax.axvline(0, color='brown', linestyle='-', linewidth=1, label='isothermal')
                    for i in range(46) :
                        for j in range(1,10) :
                            skew.ax.axvline(i*5-160+j, color='brown', linestyle='-', linewidth=0.3)
                        skew.ax.axvline(i*5-160, color='brown', linestyle='-', linewidth=1)
                
                    # Add the relevant special lines
                    skew.plot_dry_adiabats(t0=np.arange(-50, 260, 2) * units.degC, color='green', linestyle='-', linewidth=0.3)
                    skew.plot_dry_adiabats(color='green', linestyle='-', linewidth=1.5, label='dry adiabat')
                    skew.plot_moist_adiabats(t0=np.arange(-50, 160, 2) * units.degC, color='orange', linestyle='-', linewidth=0.3)
                    skew.plot_moist_adiabats(color='orange', linestyle='-', linewidth=1.5, label='saturation adiabat')
                    
                    mixing_ratio_ticks = np.array([0.0001, 0.0002, 0.0004, 0.0006, 0.0008, 0.001, 0.0015, 0.002, 0.0025, 0.003, 0.004, 0.005, 0.006, 0.007, 0.008, 0.009, 0.010, 0.012, 0.014, 0.016, 0.018, 0.020, 0.022, 0.024, 0.026, 0.028, 0.030, 0.033, 0.036, 0.040]).reshape(-1, 1)
                    skew.plot_mixing_lines(w=mixing_ratio_ticks, color='blue', linestyle='--', linewidth=1.0, label='mixing ratio')
                    
                    plt.text(-21.0, 1062, 'mixing ratio', horizontalalignment='left', verticalalignment='center', fontsize=9, color='blue')
                    #plt.text(-27.2, 1062, '{0}'.format(mixing_ratio_ticks[2][0]*1000), horizontalalignment='left', verticalalignment='center', fontsize=9, color='blue')
                    #plt.text(-22.5, 1062, '{0}'.format(mixing_ratio_ticks[3][0]*1000), horizontalalignment='left', verticalalignment='center', fontsize=9, color='blue')
                    #plt.text(-19, 1062, '{0}'.format(mixing_ratio_ticks[4][0]*1000), horizontalalignment='left', verticalalignment='center', fontsize=9, color='blue')
                    plt.text(-16.5, 1062, '{0}'.format(mixing_ratio_ticks[5][0]*1000), horizontalalignment='left', verticalalignment='center', fontsize=9, color='blue')
                    plt.text(-11.5, 1062, '{0}'.format(mixing_ratio_ticks[6][0]*1000), horizontalalignment='left', verticalalignment='center', fontsize=9, color='blue')
                    plt.text(-8.2, 1062, '{0}'.format(mixing_ratio_ticks[7][0]*1000), horizontalalignment='left', verticalalignment='center', fontsize=9, color='blue')
                    plt.text(-5, 1062, '{0}'.format(mixing_ratio_ticks[8][0]*1000), horizontalalignment='left', verticalalignment='center', fontsize=9, color='blue')
                    plt.text(-2.8, 1062, '{0}'.format(mixing_ratio_ticks[9][0]*1000), horizontalalignment='left', verticalalignment='center', fontsize=9, color='blue')
                    plt.text(1.2, 1062, '{0}'.format(mixing_ratio_ticks[10][0]*1000), horizontalalignment='left', verticalalignment='center', fontsize=9, color='blue')
                    plt.text(4.3, 1062, '{0}'.format(mixing_ratio_ticks[11][0]*1000), horizontalalignment='left', verticalalignment='center', fontsize=9, color='blue')
                    plt.text(7.0, 1062, '{0}'.format(mixing_ratio_ticks[12][0]*1000), horizontalalignment='left', verticalalignment='center', fontsize=9, color='blue')
                    plt.text(9.2, 1062, '{0}'.format(mixing_ratio_ticks[13][0]*1000), horizontalalignment='left', verticalalignment='center', fontsize=9, color='blue')
                    plt.text(11.2, 1062, '{0}'.format(mixing_ratio_ticks[14][0]*1000), horizontalalignment='left', verticalalignment='center', fontsize=9, color='blue')
                    plt.text(13.0, 1062, '{0}'.format(mixing_ratio_ticks[15][0]*1000), horizontalalignment='left', verticalalignment='center', fontsize=9, color='blue')
                    plt.text(14.7, 1062, '{0:.0f}'.format(mixing_ratio_ticks[16][0]*1000), horizontalalignment='left', verticalalignment='center', fontsize=9, color='blue')
                    plt.text(17.5, 1062, '{0:.0f}'.format(mixing_ratio_ticks[17][0]*1000), horizontalalignment='left', verticalalignment='center', fontsize=9, color='blue')
                    plt.text(19.9, 1062, '{0:.0f}'.format(mixing_ratio_ticks[18][0]*1000), horizontalalignment='left', verticalalignment='center', fontsize=9, color='blue')
                    plt.text(22.0, 1062, '{0:.0f}'.format(mixing_ratio_ticks[19][0]*1000), horizontalalignment='left', verticalalignment='center', fontsize=9, color='blue')
                    plt.text(23.9, 1062, '{0:.0f}'.format(mixing_ratio_ticks[20][0]*1000), horizontalalignment='left', verticalalignment='center', fontsize=9, color='blue')
                    plt.text(25.3, 1062, '{0:.0f}'.format(mixing_ratio_ticks[21][0]*1000), horizontalalignment='left', verticalalignment='center', fontsize=9, color='blue')
                    plt.text(27.0, 1062, '{0:.0f}'.format(mixing_ratio_ticks[22][0]*1000), horizontalalignment='left', verticalalignment='center', fontsize=9, color='blue')
                    plt.text(28.5, 1062, '{0:.0f}'.format(mixing_ratio_ticks[23][0]*1000), horizontalalignment='left', verticalalignment='center', fontsize=9, color='blue')
                    plt.text(29.7, 1062, '{0:.0f}'.format(mixing_ratio_ticks[24][0]*1000), horizontalalignment='left', verticalalignment='center', fontsize=9, color='blue')
                    plt.text(31.1, 1062, '{0:.0f}'.format(mixing_ratio_ticks[25][0]*1000), horizontalalignment='left', verticalalignment='center', fontsize=9, color='blue')
                    plt.text(32.2, 1062, '{0:.0f}'.format(mixing_ratio_ticks[26][0]*1000), horizontalalignment='left', verticalalignment='center', fontsize=9, color='blue')
                    plt.text(33.8, 1062, '{0:.0f}'.format(mixing_ratio_ticks[27][0]*1000), horizontalalignment='left', verticalalignment='center', fontsize=9, color='blue')
                    plt.text(35.3, 1062, '{0:.0f}'.format(mixing_ratio_ticks[28][0]*1000), horizontalalignment='left', verticalalignment='center', fontsize=9, color='blue')
                    plt.text(37.2, 1062, '{0:.0f}'.format(mixing_ratio_ticks[29][0]*1000), horizontalalignment='left', verticalalignment='center', fontsize=9, color='blue')
                    
                    plt.text(-70.0, 393.5, '$ \cdotp $ site : {0}'.format(filename_el[-5]), horizontalalignment='left', verticalalignment='center', fontsize=10)
                    plt.text(-70.0, 397, '$ \cdotp $ time : {0} (UTC)'.format(selected_time[:16]), horizontalalignment='left', verticalalignment='center', fontsize=10)
                    
                    #for ubuntu
                    plt.text(-17, 1130, '$ \cdotp $ LCL (   ): {0:.1f}, {1:.1f}'.format(lcl_pressure, lcl_temperature), horizontalalignment='left', verticalalignment='center', fontsize=12)
                    plt.text(-16, 1150, '$ \cdotp $ LCF (   ): {0:.1f}, {1:.1f}'.format(LCF_pressure, LCF_temperature), horizontalalignment='left', verticalalignment='center', fontsize=12)
                    plt.text(-15, 1170, '$ \cdotp $ EL   (   ): {0:.1f}, {1:.1f}'.format(EL_pressure, EL_temperature), horizontalalignment='left', verticalalignment='center', fontsize=12)
                    plt.text(-15.0, 1130, 'o', horizontalalignment='left', verticalalignment='center', fontsize=12, color='black')
                    plt.text(-14.0, 1150, 'x', horizontalalignment='left', verticalalignment='center', fontsize=12, color='red')
                    plt.text(-13.0, 1170, 'o', horizontalalignment='left', verticalalignment='center', fontsize=12, color='blue')
                    #plt.text(30, 1310, '$ \cdotp $ the most unstable parcel index: {0}'.format(mup_index), horizontalalignment='left', verticalalignment='center', fontsize=12)
                    #plt.text(31.85, 1360, '     {0:.1f} ~ {1:.1f}'.format(p[mup_index-1], p[mup_index]), horizontalalignment='left', verticalalignment='center', fontsize=12)
                    plt.text(22.70, 1170, '$ \cdotp $ {0}'.format(filename), horizontalalignment='left', verticalalignment='center', fontsize=12)
                    
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