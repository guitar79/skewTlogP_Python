# Copyright (c) 2015,2016,2017 MetPy Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
"""
conda install -c conda-forge metpy
created by guitar79@naver.com
"""

import matplotlib.pyplot as plt
from glob import glob
import os
import numpy as np
import pandas as pd
from datetime import datetime
import metpy.calc as mpcalc
#from metpy.cbook import get_test_data
#from metpy.plots import add_metpy_logo, SkewT
from metpy.plots import SkewT
from metpy.units import units

add_log = True
if add_log == True :
    log_file = 'drawing_SkewT-logP_using_1data.log'
    err_log_file = 'drawing_SkewT-logP_using_1data_err.log'
    
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


xxlim = [-50, 50]
yylim = [1050, 100]

base_dir_name = '../1data/'
            
for dir_names in sorted(os.listdir(base_dir_name))[0:1]:
    for dir_name in sorted(os.listdir('{0}{1}/'.format(base_dir_name, dir_names)))[0:1]:
        for fullname in sorted(glob(os.path.join('{0}{1}/{2}/'\
                 .format(base_dir_name, dir_names, dir_name), '*solution.csv')))[0:1]:
            fullname_el = fullname.split('/')
            #fullname_el = fullname.split('\\')
            filename = fullname_el[-1]
            
            #지점,일시(UTC),기압(hPa),고도(gpm),기온(°C),이슬점온도(°C),풍향(deg),풍속(knot),
            #지상 FLAG(null),권계면 FLAG(null),최대풍 FLAG(null)
            #idx,time,pressure,height,temperature,dewpoint,direction,speed,FLAG1,FLAG2,FLAG3,u_wind,v_wind,wet_bulb_T,potential_T,potential_T_C,saturation_vaper_pressure,vaper_pressure,saturation_mixing_ratio,mixing_ratio,relative_humidity_from_dewpoint,relative_humidity_from_mixing_ratio,virtual_temperature,virtual_potential_temperature
            df_selected_time = pd.read_csv(fullname, skiprows=1, sep=',', header=None, index_col=0,
                               names = ['index', 'time', 'pressure', 'height', 'temperature', 
                                        'dewpoint', 'direction', 'speed', 'FLAG1', 'FLAG2', 'FLAG3',
                                        'u_wind', 'v_wind', 'wet_bulb_T', 'potential_T', 'potential_T_C',
                                        'saturation_vaper_pressure', 'vaper_pressure', 
                                        'saturation_mixing_ratio', 'mixing_ratio',
                                        'relative_humidity_from_dewpoint', 'relative_humidity_from_mixing_ratio',
                                        'virtual_temperature', 'virtual_potential_temperature'],
                               skipfooter=0, engine='python')
        
            if os.path.isfile('{0}.png'.format(fullname[:-4])) \
                  and not os.path.isfile('{0}.pdf'.format(fullname[:-4])) :
                write_log(log_file, '{1} ::: {0} files are already exist'.format(fullname[:-4], datetime.now()))
            else : 
                try : 
                    print('filename : {0}'.format(fullname))
                    print('df_selected_time.\n{0}'.format(df_selected_time))
                    
                    ###########################################
                    # We will pull the data out of the example dataset into individual variables and
                    # assign units.
                    p = df_selected_time['pressure'].values * units.hPa
                    T = df_selected_time['temperature'].values * units.degC
                    Td = df_selected_time['dewpoint'].values * units.degC
                    wind_speed = df_selected_time['speed'].values * units.knots
                    wind_dir = df_selected_time['direction'].values * units.degrees
                    u, v = mpcalc.wind_components(wind_speed, wind_dir)
                    
                    ###########################################
                    # Create a new figure. The dimensions here give a good aspect ratio.
                    fig = plt.figure(figsize=(28, 24))          
                    #add_metpy_logo(fig, 115, 100)
                    skew = SkewT(fig, rotation=45)
                    
                    skew.ax.set_title('skew T log p diagram\n', fontsize=30)            
                    skew.ax.set_xlabel(r'temperature ($ \degree C$)', fontsize=24)
                    skew.ax.set_ylabel(r'pressure ($ hPa $)', fontsize=24)
                    
                    # isotherm
                    for i in range(1,12) :
                        skew.ax.axvline(i*20-155, color='green', linestyle='-', linewidth=112, alpha=0.1)
                    skew.ax.axvline(0, color='brown', linestyle='-', linewidth=1.5, label='isothermal')
                    for i in range(46) :
                        for j in range(1,10) :
                            skew.ax.axvline(i*5-160+j, color='brown', linestyle='-', linewidth=0.3)
                        skew.ax.axvline(i*5-160, color='brown', linestyle='-', linewidth=1.5)
                    for i in range(0, 10) :
                        plt.text(i*10-90.5, 300, '{0}'.format(i*10-90), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=14, rotation=45, color='brown', alpha=0.7)
                        
                    for i in range(3, 12) :
                        plt.text(i*10-90.5, 600, '{0}'.format(i*10-90), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=14, rotation=45, color='brown', alpha=0.7)
                
                    # Add the relevant special lines
                    skew.plot_dry_adiabats(t0=np.arange(-50, 260, 2) * units.degC, 
                                           color='orange', linestyle='-', linewidth=1.0)
                    #skew.plot_dry_adiabats(color='orange', linestyle='-', 
                    #                       linewidth=1.5, label='dry adiabat')
                    skew.plot_moist_adiabats(t0=np.arange(-50, 160, 2) * units.degC, 
                                             color='green', linestyle='-', linewidth=1.0)
                    #skew.plot_moist_adiabats(color='green', linestyle='-', 
                    #                         linewidth=1.5, label='saturation adiabat')
                    
                    mixing_ratio_ticks = np.array([0.0001, 0.0002, 0.0004, 0.0006, 0.0008, 
                                                   0.001, 0.0015, 0.002, 0.0025, 0.003, 
                                                   0.004, 0.005, 0.006, 0.007, 0.008, 
                                                   0.009, 0.010, 0.012, 0.014, 0.016, 
                                                   0.018, 0.020, 0.022, 0.024, 0.026, 
                                                   0.028, 0.030, 0.033, 0.036, 0.040, 
                                                   0.044, 0.048, 0.052, 0.056, 0.060, 
                                                   0.065, 0.070]).reshape(-1, 1)
                    skew.plot_mixing_lines(w=mixing_ratio_ticks, p=[1050, 400] * units.hPa, color='blue', 
                                           linestyle='--', linewidth=1.0, label='mixing ratio')
                    
                    ###########################################################
                    ### 400 hPa mixing ratio
                    ###########################################################
                    plt.text(15.5, 394, 'mixing ratio', 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(-50.8, 394, '{0}'.format(mixing_ratio_ticks[0][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(-44.7, 394, '{0}'.format(mixing_ratio_ticks[1][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(-38.0, 394, '{0}'.format(mixing_ratio_ticks[2][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(-34.0, 394, '{0}'.format(mixing_ratio_ticks[3][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(-30.9, 394, '{0}'.format(mixing_ratio_ticks[4][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(-28.4, 394, '{0}'.format(mixing_ratio_ticks[5][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(-24.0, 394, '{0}'.format(mixing_ratio_ticks[6][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(-21.0, 394, '{0}'.format(mixing_ratio_ticks[7][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(-18, 394, '{0}'.format(mixing_ratio_ticks[8][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(-16, 394, '{0}'.format(mixing_ratio_ticks[9][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(-12.5, 394, '{0}'.format(mixing_ratio_ticks[10][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(-9.8, 394, '{0}'.format(mixing_ratio_ticks[11][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(-7.2, 394, '{0}'.format(mixing_ratio_ticks[12][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(-5.3, 394, '{0}'.format(mixing_ratio_ticks[13][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(-3.5, 394, '{0}'.format(mixing_ratio_ticks[14][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(-2.0, 394, '{0}'.format(mixing_ratio_ticks[15][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(-0.4, 394, '{0:.0f}'.format(mixing_ratio_ticks[16][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(2.1, 394, '{0:.0f}'.format(mixing_ratio_ticks[17][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(4.2, 394, '{0:.0f}'.format(mixing_ratio_ticks[18][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(6.2, 394, '{0:.0f}'.format(mixing_ratio_ticks[19][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(8.0, 394, '{0:.0f}'.format(mixing_ratio_ticks[20][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(9.4, 394, '{0:.0f}'.format(mixing_ratio_ticks[21][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(10.8, 394, '{0:.0f}'.format(mixing_ratio_ticks[22][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(12.0, 394, '{0:.0f}'.format(mixing_ratio_ticks[23][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(13.2, 394, '{0:.0f}'.format(mixing_ratio_ticks[24][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(14.3, 394, '{0:.0f}'.format(mixing_ratio_ticks[25][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    #plt.text(32.2, 394, '{0:.0f}'.format(mixing_ratio_ticks[26][0]*1000), 
                    #         horizontalalignment='left', verticalalignment='center', 
                    #         fontsize=9, color='blue')
                    #plt.text(33.8, 1062, '{0:.0f}'.format(mixing_ratio_ticks[27][0]*1000), 
                    #         horizontalalignment='left', verticalalignment='center', 
                    #         fontsize=9, color='blue')
                    #plt.text(35.3, 1062, '{0:.0f}'.format(mixing_ratio_ticks[28][0]*1000), 
                    #         horizontalalignment='left', verticalalignment='center', 
                    #         fontsize=9, color='blue')
                    #plt.text(37.2, 1062, '{0:.0f}'.format(mixing_ratio_ticks[29][0]*1000), 
                    #         horizontalalignment='left', verticalalignment='center', 
                    #         fontsize=9, color='blue')
                    #plt.text(38.8, 1062, '{0:.0f}'.format(mixing_ratio_ticks[30][0]*1000), 
                    #         horizontalalignment='left', verticalalignment='center', 
                    #         fontsize=9, color='blue')
                    #plt.text(40.2, 1062, '{0:.0f}'.format(mixing_ratio_ticks[31][0]*1000), 
                    #         horizontalalignment='left', verticalalignment='center', 
                    #         fontsize=9, color='blue')
                    #plt.text(41.8, 1062, '{0:.0f}'.format(mixing_ratio_ticks[32][0]*1000), 
                    #         horizontalalignment='left', verticalalignment='center', 
                    #         fontsize=9, color='blue')
                    #plt.text(43.0, 1062, '{0:.0f}'.format(mixing_ratio_ticks[33][0]*1000), 
                    #         horizontalalignment='left', verticalalignment='center', 
                    #         fontsize=9, color='blue')
                    #plt.text(44.2, 1062, '{0:.0f}'.format(mixing_ratio_ticks[34][0]*1000), 
                    #         horizontalalignment='left', verticalalignment='center', 
                    #         fontsize=9, color='blue')
                    #plt.text(45.4, 1062, '{0:.0f}'.format(mixing_ratio_ticks[35][0]*1000), 
                    #         horizontalalignment='left', verticalalignment='center', 
                    #         fontsize=9, color='blue')
                    #plt.text(46.9, 1062, '{0:.0f}'.format(mixing_ratio_ticks[36][0]*1000), 
                    #         horizontalalignment='left', verticalalignment='center', 
                    #         fontsize=9, color='blue')
                    
                    
                    ###########################################################
                    ### bottom mixing ratio
                    ###########################################################
                    plt.text(-46.5, 1062, 'mixing ratio', 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(-41.2, 1062, '{0}'.format(mixing_ratio_ticks[0][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(-34.2, 1062, '{0}'.format(mixing_ratio_ticks[1][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(-27.2, 1062, '{0}'.format(mixing_ratio_ticks[2][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(-22.5, 1062, '{0}'.format(mixing_ratio_ticks[3][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(-19, 1062, '{0}'.format(mixing_ratio_ticks[4][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(-16.5, 1062, '{0}'.format(mixing_ratio_ticks[5][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(-11.5, 1062, '{0}'.format(mixing_ratio_ticks[6][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(-8.2, 1062, '{0}'.format(mixing_ratio_ticks[7][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(-5, 1062, '{0}'.format(mixing_ratio_ticks[8][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(-2.8, 1062, '{0}'.format(mixing_ratio_ticks[9][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(1.2, 1062, '{0}'.format(mixing_ratio_ticks[10][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(4.3, 1062, '{0}'.format(mixing_ratio_ticks[11][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(7.0, 1062, '{0}'.format(mixing_ratio_ticks[12][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(9.2, 1062, '{0}'.format(mixing_ratio_ticks[13][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(11.2, 1062, '{0}'.format(mixing_ratio_ticks[14][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(13.0, 1062, '{0}'.format(mixing_ratio_ticks[15][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(14.7, 1062, '{0:.0f}'.format(mixing_ratio_ticks[16][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(17.5, 1062, '{0:.0f}'.format(mixing_ratio_ticks[17][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(19.9, 1062, '{0:.0f}'.format(mixing_ratio_ticks[18][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(22.0, 1062, '{0:.0f}'.format(mixing_ratio_ticks[19][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(23.9, 1062, '{0:.0f}'.format(mixing_ratio_ticks[20][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(25.3, 1062, '{0:.0f}'.format(mixing_ratio_ticks[21][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(27.0, 1062, '{0:.0f}'.format(mixing_ratio_ticks[22][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(28.5, 1062, '{0:.0f}'.format(mixing_ratio_ticks[23][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(29.7, 1062, '{0:.0f}'.format(mixing_ratio_ticks[24][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(31.1, 1062, '{0:.0f}'.format(mixing_ratio_ticks[25][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(32.2, 1062, '{0:.0f}'.format(mixing_ratio_ticks[26][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(33.8, 1062, '{0:.0f}'.format(mixing_ratio_ticks[27][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(35.3, 1062, '{0:.0f}'.format(mixing_ratio_ticks[28][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(37.2, 1062, '{0:.0f}'.format(mixing_ratio_ticks[29][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(38.8, 1062, '{0:.0f}'.format(mixing_ratio_ticks[30][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(40.2, 1062, '{0:.0f}'.format(mixing_ratio_ticks[31][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(41.8, 1062, '{0:.0f}'.format(mixing_ratio_ticks[32][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(43.0, 1062, '{0:.0f}'.format(mixing_ratio_ticks[33][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(44.2, 1062, '{0:.0f}'.format(mixing_ratio_ticks[34][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(45.4, 1062, '{0:.0f}'.format(mixing_ratio_ticks[35][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    plt.text(46.9, 1062, '{0:.0f}'.format(mixing_ratio_ticks[36][0]*1000), 
                             horizontalalignment='left', verticalalignment='center', 
                             fontsize=9, color='blue')
                    
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
                    skew.plot(lcl_pressure, lcl_temperature, 'ko', 
                              markersize = 8, fillstyle='none', label='LCL')
                    
                    # Calculate LCF height and plot as purple dot
                    LCF_pressure, LCF_temperature = mpcalc.lfc(p, T, Td, prof_0)
                    skew.plot(LCF_pressure, LCF_temperature, 'rx', 
                              markersize = 8, fillstyle='none', label='LCF')
                    
                    # Calculate EL height and plot as blue dot
                    EL_pressure, EL_temperature = mpcalc.el(p, T, Td, prof_0)
                    skew.plot(EL_pressure, EL_temperature, 'bo', 
                              markersize = 8, fillstyle='none', label='EL')
                    
                    # Calculate most unstable parcel
                    mup_pressure, mup_temperature, mup_dewTemperature, mup_index \
                        = mpcalc.most_unstable_parcel(p, T, Td, heights=prof_0, bottom=1050 * units.hPa)
                    mup_pressure, mup_temperature, mup_dewTemperature, mup_index \
                        = mpcalc.most_unstable_parcel(p, T, Td)
                    skew.plot(p[mup_index-1:mup_index+1], T[mup_index-1:mup_index+1], 'b', 
                              label='the most unstable level')
                    
                    # Calculate precipitable water
                    precipitable_water = mpcalc.precipitable_water(Td, p)
                                        
                    plt.text(xxlim[0]+16, yylim[0]+150, '$ \cdotp $ LCL (   ): {0:.1f}, {1:.1f}'.format(lcl_pressure, lcl_temperature), \
                                 horizontalalignment='left', verticalalignment='center', fontsize=12)
                    plt.text(xxlim[0]+17.5, yylim[0]+200, '$ \cdotp $ LCF (   ): {0:.1f}, {1:.1f}'.format(LCF_pressure, LCF_temperature), \
                                 horizontalalignment='left', verticalalignment='center', fontsize=12)
                    plt.text(xxlim[0]+19, yylim[0]+260, '$ \cdotp $ EL   (   ): {0:.1f}, {1:.1f}'.format(EL_pressure, EL_temperature), \
                                 horizontalalignment='left', verticalalignment='center', fontsize=12)
                    plt.text(xxlim[0]+20.5, yylim[0]+320, '$ \cdotp $ precipitable_water : {0:.1f}'.format(precipitable_water), \
                                 horizontalalignment='left', verticalalignment='center', fontsize=12)
                    plt.text(xxlim[0]+22.0, yylim[0]+380, '$ \cdotp $ the most unstable parcel index: {0:.1f} ~ {1:.1f}'.format(p[mup_index-1], p[mup_index]), \
                                 horizontalalignment='left', verticalalignment='center', fontsize=12)
                    plt.text(xxlim[0]+18.6, yylim[0]+150, 'o', 
                             horizontalalignment='left', verticalalignment='center', fontsize=12, color='black')
                    plt.text(xxlim[0]+20.1, yylim[0]+200, 'x', 
                             horizontalalignment='left', verticalalignment='center', fontsize=12, color='red')
                    plt.text(xxlim[0]+21.6, yylim[0]+260, 'o', 
                             horizontalalignment='left', verticalalignment='center', fontsize=12, color='blue')
                              
                    plt.text(xxlim[0]+66, yylim[0]+150, '$ \cdotp $ filename : {0}'.format(fullname_el[-1]), 
                             horizontalalignment='left', verticalalignment='center', fontsize=12)
                    plt.text(xxlim[0]+67.5, yylim[0]+200, '$ \cdotp $ site : {0}'.format(fullname_el[-3]), 
                             horizontalalignment='left', verticalalignment='center', fontsize=10)
                    plt.text(xxlim[0]+69, yylim[0]+260, '$ \cdotp $ time : {0} (UTC)'.format(fullname_el[-1][:16]), 
                             horizontalalignment='left', verticalalignment='center', fontsize=10) 
                    
                    plt.legend(loc='upper left')
                    
                    plt.savefig('{0}.png'.format(fullname[:-4]),
                        dpi=None, facecolor='w', edgecolor='w',
                        orientation='portrait', papertype=None, format=None,
                        transparent=False, bbox_inches=None, pad_inches=0.1,
                        frameon=None, metadata=None)
                    plt.savefig('{0}.pdf'.format(fullname[:-4]),
                        dpi=None, facecolor='w', edgecolor='w',
                        orientation='portrait', papertype=None, format=None,
                        transparent=False, bbox_inches=None, pad_inches=0.1,
                        frameon=None, metadata=None)
                    write_log(log_file, '{1} ::: {0} files are created'.format(fullname[:-4], datetime.now()))
                    
                    # Show the plot
                    #plt.show()
                    # Close the plot
                    plt.close(fig)
                
                except Exception as err :
                    write_log(err_log_file, '{2} ::: {0} with {1}'.format(err, fullname, datetime.now()))