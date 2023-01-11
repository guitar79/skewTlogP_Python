# Copyright (c) 2015,2016,2017 MetPy Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
"""


"""

import os
from glob import glob
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime
import metpy.calc as mpcalc
from metpy.units import units

BASEDIR = 'c:\Rdata\RAWIN_data'
BASEDIR = 'd:\Rdata\RAWIN_data'
##BASEDIR ='/mnt/6TB1/RS_data/RAWIN_data'
BASEDIR = Path(BASEDIR)


class draw_skewT_logP():
    def __init__(self, skewed_graph):
        self.skew = skewed_graph
        self.xxlim = [-50, 50]
        self.yylim = [1050.1, 99.9]
        self.DA_Upper = 680
        self.UDA_list = [(-56.2, -30, -50), (-54.4, -28, -50), (-52.8, -26, -50), (-51.0, -24, -50), (-49.2, -22, -50),
                         (-47.4, -20, -50), (-45.6, -18, -50), (-43.8, -16, -50), (-42.0, -14, -50), (-40.2, -12, -50),
                         (-38.4, -10, -49), (-36.4, -8, -49), (-34.5, -6, -49), (-32.7, -4, -50), (-30.8, -2, -50),
                         (-29.1, 0, -49), (-27.4, 2, -49), (-25.6, 4, -51), (-23.8, 6, -52), (-22.0, 8, -52),
                         (-20.3, 10, -52), (-18.6, 12, -52), (-16.8, 14, -52), (-15.0, 16, -52), (-13.2, 18, -52),
                         (-11.4, 20, -52), (-9.6, 22, -52), (-7.8, 24, -52), (-6.0, 26, -52), (-4.2, 28, -52),
                         (-2.4, 30, -52), (-0.6, 32, -52), (1.1, 34, -52), (2.9, 36, -52), (4.8, 38, -52),
                         (6.6, 40, -52), (8.5, 42, -52), (10.3, 44, -52)]
        self.MA_Upper = 530
        self.UMA_list = [(-70.6, -30, -50), (-68.8, -28, -50), (-66.9, -26, -50), (-65.0, -24, -50), (-63.2, -22, -50),
                     (-61.3, -20, -50), (-59.3, -18, -50), (-57.3, -16, -50), (-55.2, -14, -50), (-53.1, -12, -50),
                     (-50.9, -10, -49), (-48.3, -8, -49), (-46.0, -6, -49), (-43.6, -4, -49), (-40.9, -2, -49),
                     (-38.3, -0, -49), (-35.5, 2, -50), (-32.5, 4, -51), (-29.5, 6, -54), (-26.5, 8, -58), (-23.2, 10, -61),
                     (-19.9, 12, -64), (-16.6, 14, -69), (-13.1, 16, -72), (-9.8, 18, -76), (-6.4, 20, -79),
                     (-3.1, 22, -82), (0.1, 24, -85), (3.1, 26, -88), (6.1, 28, -90), (9.1, 30, -92),
                     (11.9, 32, -94), (14.5, 34, -96), (17.2, 36, -98), (19.7, 38, -100)]
        self.mixing_ratio_ticks = np.array([0.0001, 0.0002, 0.0004, 0.0006, 0.0008,
                                       0.001, 0.0015, 0.002, 0.0025, 0.003,
                                       0.004, 0.005, 0.006, 0.007, 0.008,
                                       0.009, 0.010, 0.012, 0.014, 0.016,
                                       0.018, 0.020, 0.022, 0.024, 0.026,
                                       0.028, 0.030, 0.033, 0.036, 0.040,
                                       0.044, 0.048, 0.052, 0.056, 0.060,
                                       0.065, 0.070]).reshape(-1, 1)
        self.MRL_Upper = 396
        self.MRL_Upper_list = [-50.8, -44.6, -38.0, -33.8, -30.9,
                          -28.4, -23.8, -20.6, -18.0, -15.8,
                          -12.5, -9.4, -7.2, -5.3, -3.5,
                          -1.8, -0.2, 2.2, 4.3, 6.3,
                          8.0, 9.4, 10.8, 12.0, 13.2,
                          14.3, 15.5]
        self.MRL_Under = 1068
        self.MRL_Under_list = [-41.1, -34.2, -27.0, -22.5, -19.0,
                          -16.5, -11.5, -8.0, -5.0, -2.7,
                          1.2, 4.4, 7.0, 9.2, 11.3,
                          13.0, 14.7, 17.5, 19.9, 22.0,
                          23.9, 25.5, 27.2, 28.6, 29.9,
                          31.2, 32.3, 34.0, 35.4, 37.2,
                          38.9, 40.3, 41.8, 43.0, 44.2,
                          45.6, 47.0]
    def add_isobar(self):
        self.skew.ax.set_ylim(self.yylim[0], self.yylim[1])
        yts1 = list(np.arange(1050, 99, -10))
        self.skew.ax.set_yticks(yts1)

        yts2 = list(np.arange(1050, 99, -50))
        yticklabels = []
        i = 0
        for ytick in yts2:
            yticklabels.append(ytick)
            for j in range(4):
                yticklabels.append('')
            self.skew.plot([ytick, ytick], [-150, 100], 'k', linewidth=0.6)

            # 기온축이 기울어 지고, 기압축이 로그스케일이어서 텍스트 정렬이 흐트러지는 문제를 36기 유호혁 학생이 아래와 같이 해결함.
            # isobar text
            if ytick >= 200:
                plt.text(-20 - (np.log(1050) - np.log(1050 - i * 50)) * 35, ytick, '{0}'.format(ytick),
                         horizontalalignment='left', verticalalignment='center',
                         fontsize=14, color='black', alpha=.30)
            if ytick >= 500:
                plt.text(20 - (np.log(1050) - np.log(1050 - i * 50)) * 35, ytick, '{0}'.format(ytick),
                         horizontalalignment='left', verticalalignment='center',
                         fontsize=14, color='black', alpha=.30)
        self.skew.ax.set_yticklabels(yticklabels[:-4], minor=False)
        return self.skew

    def add_isothermal(self):
        for i in range(1, 12):
            self.skew.ax.axvline(i * 20 - 155, color='green', linestyle='-', linewidth=112, alpha=0.1)
        for i in range(46):
            for j in range(1, 10):
                self.skew.ax.axvline(i * 5 - 160 + j, color='brown', linestyle='-', linewidth=0.3)
            self.skew.ax.axvline(i * 5 - 160, color='brown', linestyle='-', linewidth=1.5)
        self.skew.ax.axvline(0, color='brown', linestyle='-', linewidth=1.5, label='isothermal')
        self.skew.ax.set_xlim(self.xxlim[0], self.xxlim[1])
        self.skew.ax.tick_params(axis="x", labelsize=14, pad=10, rotation=45, labelcolor='brown')
        self.skew.ax.tick_params(axis="y", labelsize=14, pad=0.5)

        # 기온축이 기울어 지고, 기압축이 로그스케일이어서 텍스트 정렬이 흐트러지는 문제를 36기 유호혁 학생이 아래와 같이 해결함.
        # isothermal text
        for i in range(36):
            if i < 16:
                plt.text(-i * 5 - 10.5, 1050 / 10 ** (i / 35), '{0}'.format(-i * 5 - 10),
                         horizontalalignment='left', verticalalignment='center',
                         fontsize=14, rotation=45, color='brown', alpha=0.7)
            if i < 30:
                plt.text(-i * 5 + 29.5, 1050 / 10 ** (i / 35), '{0}'.format(-i * 5 + 30),
                         horizontalalignment='left', verticalalignment='center',
                         fontsize=14, rotation=45, color='brown', alpha=0.7)
            if i > 7:
                plt.text(-i * 5 + 69.5, 1050 / 10 ** (i / 35), '{0}'.format(-i * 5 + 70),
                         horizontalalignment='left', verticalalignment='center',
                         fontsize=14, rotation=45, color='brown', alpha=0.7)
        return self.skew

    def add_dry_adiabats(self):
        self.skew.plot_dry_adiabats(t0=np.arange(-50, 260, 2) * units.degC,
                               color='orange', linestyle='-', linewidth=1.0, label='dry adiabat')

        for UDA in self.UDA_list:
            plt.text(UDA[0], self.DA_Upper, '{}'.format(UDA[1]),
                     horizontalalignment='left', verticalalignment='center',
                     fontsize=12, color='orange', rotation=UDA[2])
        return self.skew
    def add_moist_adiabats(self):
        self.skew.plot_moist_adiabats(t0=np.arange(-50, 160, 2) * units.degC,
                                 color='green', linestyle='-', linewidth=1.0, label='saturation adiabat')

        for UMA in self.UMA_list:
            plt.text(UMA[0], self.MA_Upper, '{}'.format(UMA[1]),
                     horizontalalignment='left', verticalalignment='center',
                     fontsize=12, color='green', rotation=UMA[2])
        return self.skew

    def add_mising_ratio(self):
        self.skew.plot_mixing_lines(self.mixing_ratio_ticks, [1050, 400] * units.hPa, color='blue',
                               linestyle='--', linewidth=1.0, label='mixing ratio')
        plt.text(16.5, self.MRL_Upper, 'mixing ratio',
                 horizontalalignment='left', verticalalignment='center',
                 fontsize=9, color='blue')
        for i in range(len(self.MRL_Upper_list)):
            plt.text(self.MRL_Upper_list[i], self.MRL_Upper, '{0}'.format(self.mixing_ratio_ticks[i][0] * 1000),
                     horizontalalignment='left', verticalalignment='center',
                     fontsize=9, color='blue')
        plt.text(-46.5, self.MRL_Under, 'mixing ratio',
                 horizontalalignment='left', verticalalignment='center',
                 fontsize=9, color='blue')
        for i in range(len(self.MRL_Under_list)):
            plt.text(self.MRL_Under_list[i], self.MRL_Under, '{0}'.format(self.mixing_ratio_ticks[i][0] * 1000),
                     horizontalalignment='left', verticalalignment='center',
                     fontsize=9, color='blue')

###########################################################
### 등온선(isothem) 그리는 함수 정의
###########################################################
def add_isothermal(plt, skew, xxlim, yylim) :
    # 등온선의 녹색 영역 표시
    for i in range(1,12) :
        skew.ax.axvline(i*20-155, color='green', linestyle='-', linewidth=112, alpha=0.1)

    # 갈색 등온선의 그리기 
    for i in range(46) :
        for j in range(1,10) :
            skew.ax.axvline(i*5-160+j, color='brown', linestyle='-', linewidth=0.3)
        skew.ax.axvline(i*5-160, color='brown', linestyle='-', linewidth=1.5)
    skew.ax.axvline(0, color='brown', linestyle='-', linewidth=1.5, label='isothermal')

    # 가로(기온)축 표시하기
    skew.ax.set_xlim(xxlim[0], xxlim[1])
    skew.ax.tick_params(axis="x", labelsize=14, pad=10, rotation=45, labelcolor='brown')
    skew.ax.tick_params(axis="y", labelsize=14, pad=0.5)

    # 기온축이 기울어 지고, 기압축이 로그스케일이어서 텍스트 정렬이 흐트러지는 문제를 36기 유호혁 학생이 아래와 같이 해결함.
    #isothermal text
    for i in range(36):    
        if i < 16:
            plt.text(-i*5-10.5, 1050 / 10**(i/35), '{0}'.format(-i*5-10), 
                horizontalalignment='left', verticalalignment='center', 
                fontsize=14, rotation=45, color='brown', alpha=0.7)
        if i < 30:
            plt.text(-i*5+29.5, 1050 / 10**(i/35), '{0}'.format(-i*5+30), 
                horizontalalignment='left', verticalalignment='center', 
                fontsize=14, rotation=45, color='brown', alpha=0.7)
        if i > 7 : 
            plt.text(-i*5+69.5, 1050 / 10**(i/35), '{0}'.format(-i*5+70), 
                horizontalalignment='left', verticalalignment='center', 
                fontsize=14, rotation=45, color='brown', alpha=0.7)    
    return skew    
###########################################################


###########################################################
### 등압선 그리는 함수 정의
###########################################################
def add_isobar(plt, skew, xxlim, yylim):
    skew.ax.set_ylim(yylim[0], yylim[1])
    yts1 = list(np.arange(1050, 99, -10))  # 10 hPa 간격 (가는 선) 표시
    skew.ax.set_yticks(yts1)

    # 50 hPa 간격
    yts2 = list(np.arange(1050, 99, -50))  # 50 hPa 간격 (굵은 선) 표시
    yticklabels=[]
    i=0
    for ytick in yts2 : 
        yticklabels.append(ytick)
        for j in range(4):
            yticklabels.append('')
        skew.plot([ytick, ytick], [-150,100], 'k', linewidth=0.6)
    
        # 기온축이 기울어 지고, 기압축이 로그스케일이어서 텍스트 정렬이 흐트러지는 문제를 36기 유호혁 학생이 아래와 같이 해결함.
        #isobar text
        if ytick >= 200 : 
            plt.text(-20-(np.log(1050)-np.log(1050-i*50))*35, ytick, '{0}'.format(ytick), 
                horizontalalignment='left', verticalalignment='center', 
                fontsize=14, color='black', alpha=.30)
        if ytick >= 500 : 
            plt.text(20-(np.log(1050)-np.log(1050-i*50))*35, ytick, '{0}'.format(ytick), 
                horizontalalignment='left', verticalalignment='center', 
                fontsize=14, color='black', alpha=.30)

    #print("yticklabels: {}".format(yticklabels))
    #print("len(yticklabels): {}".format(len(yticklabels)))

    skew.ax.set_yticklabels(yticklabels[:-4], minor=False)
    
    return skew
###########################################################


###########################################################
### 건조 단열선 그리는 함수 정의
###########################################################
def add_dry_adiabats(skew):
    skew.plot_dry_adiabats(t0=np.arange(-50, 260, 2) * units.degC, 
                            color='orange', linestyle='-', linewidth=1.0, label='dry adiabat')

    ### Upper dry adiabats text
    DA_Upper = 680

    UDA_list = [(-56.2, -30, -50), (-54.4, -28, -50), (-52.8, -26, -50), (-51.0, -24, -50), (-49.2, -22, -50), 
                    (-47.4, -20, -50), (-45.6, -18, -50), (-43.8, -16, -50), (-42.0, -14, -50), (-40.2, -12, -50), 
                    (-38.4, -10, -49), (-36.4, -8, -49), (-34.5, -6, -49), (-32.7, -4, -50), (-30.8, -2, -50), 
                    (-29.1, 0, -49), (-27.4, 2, -49), (-25.6, 4, -51), (-23.8, 6, -52), (-22.0, 8, -52),
                    (-20.3, 10, -52), (-18.6, 12, -52), (-16.8, 14, -52), (-15.0, 16, -52), (-13.2, 18, -52),
                    (-11.4, 20, -52), (-9.6, 22, -52), (-7.8, 24, -52), (-6.0, 26, -52), (-4.2, 28, -52),
                    (-2.4, 30, -52), (-0.6, 32, -52), (1.1, 34, -52), (2.9, 36, -52), (4.8, 38, -52),
                    (6.6, 40, -52), (8.5, 42, -52), (10.3, 44, -52)]

    for UDA in UDA_list :
        plt.text(UDA[0], DA_Upper, '{}'.format(UDA[1]), 
            horizontalalignment='left', verticalalignment='center', 
            fontsize=12, color='orange', rotation=UDA[2])
    return skew
###########################################################


###########################################################
### 습윤단열선 그리는 함수 정의
###########################################################
def add_moist_adiabats(skew) :
    skew.plot_moist_adiabats(t0=np.arange(-50, 160, 2) * units.degC, 
                            color='green', linestyle='-', linewidth=1.0, label='saturation adiabat')

    ### Upper moist adiabats text
    MA_Upper = 530
    UMA_list = [(-70.6, -30, -50), (-68.8, -28, -50), (-66.9, -26, -50), (-65.0, -24, -50), (-63.2, -22, -50), 
                (-61.3, -20, -50), (-59.3, -18, -50), (-57.3, -16, -50), (-55.2, -14, -50), (-53.1, -12, -50), 
                (-50.9, -10, -49), (-48.3, -8, -49), (-46.0, -6, -49), (-43.6, -4, -49), (-40.9, -2, -49), 
                (-38.3, -0, -49), (-35.5, 2, -50), (-32.5, 4, -51), (-29.5, 6, -54), (-26.5, 8, -58), (-23.2, 10, -61),
                (-19.9, 12, -64), (-16.6, 14, -69), (-13.1, 16, -72), (-9.8, 18, -76), (-6.4, 20, -79), 
                (-3.1, 22, -82), (0.1, 24, -85), (3.1, 26, -88), (6.1, 28, -90), (9.1, 30, -92), 
                (11.9, 32, -94), (14.5, 34, -96), (17.2, 36, -98), (19.7, 38, -100)]
    for UMA in UMA_list :
        plt.text(UMA[0], MA_Upper, '{}'.format(UMA[1]), 
            horizontalalignment='left', verticalalignment='center', 
            fontsize=12, color='green', rotation=UMA[2])  
    return skew
###########################################################


###########################################################
### 포화혼합비선 그리는 함수 정의
###########################################################

def add_mising_ratio(skew) :
    mixing_ratio_ticks = np.array([0.0001, 0.0002, 0.0004, 0.0006, 0.0008, 
                0.001, 0.0015, 0.002, 0.0025, 0.003, 
                0.004, 0.005, 0.006, 0.007, 0.008, 
                0.009, 0.010, 0.012, 0.014, 0.016, 
                0.018, 0.020, 0.022, 0.024, 0.026, 
                0.028, 0.030, 0.033, 0.036, 0.040, 
                0.044, 0.048, 0.052, 0.056, 0.060, 
                0.065, 0.070]).reshape(-1, 1)
    skew.plot_mixing_lines(mixing_ratio_ticks, [1050, 400] * units.hPa, color='blue', 
                            linestyle='--', linewidth=1.0, label='mixing ratio')

    ### Upper mixing ratio text
    MRL_Upper = 396

    plt.text(16.5, MRL_Upper, 'mixing ratio', 
            horizontalalignment='left', verticalalignment='center', 
            fontsize=9, color='blue')
    MRL_Upper_list = [-50.8, -44.6, -38.0, -33.8, -30.9,
                    -28.4, -23.8, -20.6, -18.0, -15.8, 
                    -12.5, -9.4, -7.2, -5.3, -3.5,
                    -1.8, -0.2, 2.2, 4.3, 6.3,
                    8.0, 9.4, 10.8, 12.0, 13.2,
                    14.3, 15.5]
    for i in range(len(MRL_Upper_list)) :
        plt.text(MRL_Upper_list[i], MRL_Upper, '{0}'.format(mixing_ratio_ticks[i][0]*1000), 
            horizontalalignment='left', verticalalignment='center', 
            fontsize=9, color='blue')  

    ### bottom mixing ratio text
    MRL_Under = 1068

    plt.text(-46.5, MRL_Under, 'mixing ratio', 
            horizontalalignment='left', verticalalignment='center', 
            fontsize=9, color='blue')

    MRL_Under_list = [-41.1, -34.2, -27.0, -22.5, -19.0,
                    -16.5, -11.5, -8.0, -5.0, -2.7, 
                    1.2, 4.4, 7.0, 9.2, 11.3,
                    13.0, 14.7, 17.5, 19.9, 22.0,
                    23.9, 25.5, 27.2, 28.6, 29.9,
                    31.2, 32.3, 34.0, 35.4, 37.2,
                    38.9, 40.3, 41.8, 43.0, 44.2,
                    45.6, 47.0]
    for i in range(len(MRL_Under_list)) :
        plt.text(MRL_Under_list[i], MRL_Under, '{0}'.format(mixing_ratio_ticks[i][0]*1000), 
            horizontalalignment='left', verticalalignment='center', 
            fontsize=9, color='blue') 
    return skew
###########################################################



def yearly_data_process_df_seleted_date(fullname, df, selected_time, save_dir_name, dir_name):
    fullname_el = fullname.split('/')
    #fullname_el = fullname.split('\\')
    filename = fullname_el[-1]
    filename_el = filename.split('_')
                
    print('site : {0}'.format(dir_name))
    
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
    print('Thread {0} is finished'.format(selected_time))
    return 0 # Return a dummy value
    # Putting large values in Queue was slow than expected(~10min)

#def yearly_data_process_df_seleted_date(fullname, df, selected_time, save_dir_name, dir_name):
def drawing_SkewT_logP_using1data(fullname, base_dir_name, dir_name):
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from datetime import datetime
    import metpy.calc as mpcalc
    #from metpy.cbook import get_test_data
    #from metpy.plots import add_metpy_logo, SkewT
    from metpy.plots import SkewT
    from metpy.units import units
    
    fullname_el = fullname.split('/')
    #fullname_el = fullname.split('\\')
    filename = fullname_el[-1]
    
    ###########################################
    ### idx,time,pressure,height,temperature,dewpoint,direction,speed,FLAG1,FLAG2,FLAG3,
    ### u_wind,v_wind,wet_bulb_T,potential_T,potential_T_C,
    ### saturation_vaper_pressure,vaper_pressure,saturation_mixing_ratio,mixing_ratio,
    ### relative_humidity_from_dewpoint,relative_humidity_from_mixing_ratio,
    ### virtual_temperature,virtual_potential_temperature
    ###########################################
    
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
        and os.path.isfile('{0}.pdf'.format(fullname[:-4])) :
        write_log(log_file, '{1} ::: {0} files are already exist'.format(fullname[:-4], datetime.now()))
    else : 
        try : 
            print('filename : {0}'.format(fullname))
                        
            ###########################################
            ### We will pull the data out of the example dataset into individual variables and
            ### assign units.
            ###########################################
            p = df_selected_time['pressure'].values * units.hPa
            T = df_selected_time['temperature'].values * units.degC
            Td = df_selected_time['dewpoint'].values * units.degC
            wind_speed = df_selected_time['speed'].values * units.knots
            wind_dir = df_selected_time['direction'].values * units.degrees
            u, v = mpcalc.wind_components(wind_speed, wind_dir)
            
            ###########################################
            ### Create a new figure. The dimensions here give a good aspect ratio.
            ###########################################
            
            xxlim = [-50, 50]
            yylim = [1050.1, 99.9]


            fig = plt.figure(figsize=(28, 24))          
            #add_metpy_logo(fig, 115, 100)
            skew = SkewT(fig, rotation=45)
            
            skew.ax.set_title('Skew T Adiabatic Diagram\n', fontsize=42) 
            skew.ax.set_xlabel(r'temperature (${\degree \mathrm{C}}$)', fontsize=24)
            skew.ax.set_ylabel(r'pressure (${\mathrm{hPa}}$)', fontsize=24)
            
            # isobar and isothermal
            for i in range(1,12) :
                skew.ax.axvline(i*20-155, color='green', linestyle='-', linewidth=112, alpha=0.1)
            skew.ax.axvline(0, color='brown', linestyle='-', linewidth=1.5, label='isothermal')
            for i in range(46) :
                for j in range(1,10) :
                    skew.ax.axvline(i*5-160+j, color='brown', linestyle='-', linewidth=0.3)
                skew.ax.axvline(i*5-160, color='brown', linestyle='-', linewidth=1.5)
        
            skew.ax.set_ylim(yylim[0], yylim[1])
            yts1 = list(np.arange(1050, 99, -10))
            skew.ax.set_yticks(yts1)
            
            yts2 = list(np.arange(1050, 99, -50))
            skew.plot([1000,1000], [-150,100], 'k', linewidth=0.6, label='isobar')                    
            yticklabels=[]
            i=0
            for ytick in yts2 : 
                yticklabels.append(ytick)
                for j in range(4):
                    yticklabels.append('')
                skew.plot([ytick,ytick], [-150,100], 'k', linewidth=0.6)
        
                #isothermal text
                plt.text(-i*5-20.5, ytick, '{0}'.format(-i*5-20), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=14, rotation=45, color='brown', alpha=0.7)
                plt.text(-i*5-0.5, ytick, '{0}'.format(-i*5), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=14, rotation=45, color='brown', alpha=0.7)
                plt.text(-i*5+19.5, ytick, '{0}'.format(-i*5+20), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=14, rotation=45, color='brown', alpha=0.7)
                plt.text(-i*5+39.5, ytick, '{0}'.format(-i*5+40), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=14, rotation=45, color='brown', alpha=0.7)
                if i > 3 : 
                    plt.text(-i*5+59.5, ytick, '{0}'.format(-i*5+60), 
                         horizontalalignment='left', verticalalignment='center', 
                         fontsize=14, rotation=45, color='brown', alpha=0.7)
                
                #isobar text
                plt.text(-40-np.log(50)*i/np.sqrt(2), ytick, '{0}'.format(ytick), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=14, color='black', alpha=30)
                plt.text(-10-np.log(50)*i/np.sqrt(2), ytick, '{0}'.format(ytick), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=14, color='black', alpha=30)
                if i < 19 : 
                    plt.text(20-np.log(50)*i/np.sqrt(2), ytick, '{0}'.format(ytick), 
                         horizontalalignment='left', verticalalignment='center', 
                         fontsize=14, color='black', alpha=30)
                
                i += 1
                continue
            skew.ax.set_yticklabels(yticklabels, minor=False)
            
            skew.ax.set_xlim(xxlim[0], xxlim[1])
            skew.ax.tick_params(axis="x", labelsize=14, pad=10, rotation=45, labelcolor='brown')
            skew.ax.tick_params(axis="y", labelsize=14, pad=0.5)
                            
            ###########################################################
            ### dry_adiabats
            ###########################################################
            skew.plot_dry_adiabats(t0=np.arange(-50, 260, 2) * units.degC, 
                                   color='orange', linestyle='-', linewidth=1.0, label='dry adiabat')
            
            ### Upper dry adiabats
            MA_Upper = 680
            plt.text(-56.2, MA_Upper, '-30', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='orange', rotation=-50)
            plt.text(-54.4, MA_Upper, '-28', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='orange', rotation=-50)
            plt.text(-52.8, MA_Upper, '-26', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='orange', rotation=-50)
            plt.text(-51.0, MA_Upper, '-24', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='orange', rotation=-50)
            plt.text(-49.2, MA_Upper, '-22', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='orange', rotation=-50)
            plt.text(-47.4, MA_Upper, '-20', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='orange', rotation=-50)
            plt.text(-45.6, MA_Upper, '-18', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='orange', rotation=-50)
            plt.text(-43.8, MA_Upper, '-16', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='orange', rotation=-50)
            plt.text(-42.0, MA_Upper, '-14', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='orange', rotation=-50)
            plt.text(-40.2, MA_Upper, '-12', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='orange', rotation=-50)
            plt.text(-38.4, MA_Upper, '-10', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='orange', rotation=-49)
            plt.text(-36.4, MA_Upper, '-8', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='orange', rotation=-49)
            plt.text(-34.5, MA_Upper, '-6', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='orange', rotation=-49)
            plt.text(-32.7, MA_Upper, '-4', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='orange', rotation=-49)
            plt.text(-30.8, MA_Upper, '-2', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='orange', rotation=-49)
            plt.text(-29.1, MA_Upper, '0', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='orange', rotation=-49)
            plt.text(-27.4, MA_Upper, '2', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='orange', rotation=-50)
            plt.text(-25.6, MA_Upper, '4', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='orange', rotation=-51)
            plt.text(-23.8, MA_Upper, '6', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='orange', rotation=-52)
            plt.text(-22.0, MA_Upper, '8', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='orange', rotation=-52)
            plt.text(-20.3, MA_Upper, '10', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='orange', rotation=-52)
            plt.text(-18.6, MA_Upper, '12', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='orange', rotation=-52)
            plt.text(-16.8, MA_Upper, '14', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='orange', rotation=-52)
            plt.text(-15.0, MA_Upper, '16', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='orange', rotation=-52)
            plt.text(-13.2, MA_Upper, '18', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='orange', rotation=-52)
            plt.text(-11.4, MA_Upper, '20', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='orange', rotation=-52)
            plt.text(-9.6, MA_Upper, '22', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='orange', rotation=-52)
            plt.text(-7.8, MA_Upper, '24', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='orange', rotation=-52)
            plt.text(-6.0, MA_Upper, '26', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='orange', rotation=-52)
            plt.text(-4.2, MA_Upper, '28', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='orange', rotation=-52)
            plt.text(-2.4, MA_Upper, '30', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='orange', rotation=-52)
            plt.text(-0.6, MA_Upper, '32', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='orange', rotation=-52)
            plt.text(1.1, MA_Upper, '34', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='orange', rotation=-52)
            plt.text(2.9, MA_Upper, '36', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='orange', rotation=-52)
            plt.text(4.8, MA_Upper, '38', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='orange', rotation=-52)
            plt.text(6.6, MA_Upper, '40', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='orange', rotation=-52)
            plt.text(8.5, MA_Upper, '42', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='orange', rotation=-52)
            plt.text(10.3, MA_Upper, '44', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='orange', rotation=-52)
            
            ###########################################################
            ### moist_adiabats
            ###########################################################
            skew.plot_moist_adiabats(t0=np.arange(-50, 160, 2) * units.degC, 
                                     color='green', linestyle='-', linewidth=1.0, label='saturation adiabat')
            
            ### Upper moist adiabats
            MA_Upper = 530
            plt.text(-70.6, MA_Upper, '-30', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='green', rotation=-50)
            plt.text(-68.8, MA_Upper, '-28', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='green', rotation=-50)
            plt.text(-66.9, MA_Upper, '-26', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='green', rotation=-50)
            plt.text(-65.0, MA_Upper, '-24', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='green', rotation=-50)
            plt.text(-63.2, MA_Upper, '-22', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='green', rotation=-50)
            plt.text(-61.3, MA_Upper, '-20', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='green', rotation=-50)
            plt.text(-59.3, MA_Upper, '-18', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='green', rotation=-50)
            plt.text(-57.3, MA_Upper, '-16', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='green', rotation=-50)
            plt.text(-55.2, MA_Upper, '-14', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='green', rotation=-50)
            plt.text(-53.1, MA_Upper, '-12', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='green', rotation=-50)
            plt.text(-50.9, MA_Upper, '-10', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='green', rotation=-49)
            plt.text(-48.3, MA_Upper, '-8', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='green', rotation=-49)
            plt.text(-46.0, MA_Upper, '-6', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='green', rotation=-49)
            plt.text(-43.6, MA_Upper, '-4', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='green', rotation=-49)
            plt.text(-40.9, MA_Upper, '-2', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='green', rotation=-49)
            plt.text(-38.3, MA_Upper, '0', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='green', rotation=-49)
            plt.text(-35.5, MA_Upper, '2', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='green', rotation=-50)
            plt.text(-32.5, MA_Upper, '4', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='green', rotation=-51)
            plt.text(-29.5, MA_Upper, '6', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='green', rotation=-54)
            plt.text(-26.5, MA_Upper, '8', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='green', rotation=-58)
            plt.text(-23.2, MA_Upper, '10', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='green', rotation=-61)
            plt.text(-19.9, MA_Upper, '12', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='green', rotation=-64)
            plt.text(-16.6, MA_Upper, '14', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='green', rotation=-69)
            plt.text(-13.1, MA_Upper, '16', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='green', rotation=-72)
            plt.text(-9.8, MA_Upper, '18', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='green', rotation=-76)
            plt.text(-6.4, MA_Upper, '20', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='green', rotation=-79)
            plt.text(-3.1, MA_Upper, '22', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='green', rotation=-82)
            plt.text(0.1, MA_Upper, '24', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='green', rotation=-85)
            plt.text(3.1, MA_Upper, '26', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='green', rotation=-88)
            plt.text(6.1, MA_Upper, '28', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='green', rotation=-90)
            plt.text(9.1, MA_Upper, '30', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='green', rotation=-92)
            plt.text(11.9, MA_Upper, '32', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='green', rotation=-94)
            plt.text(14.5, MA_Upper, '34', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='green', rotation=-96)
            plt.text(17.2, MA_Upper, '36', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='green', rotation=-98)
            plt.text(19.7, MA_Upper, '38', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=12, color='green', rotation=-100)
            
            
            ###########################################################
            ### mixing ratio
            ###########################################################
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
            
            ### Upper mixing ratio
            MRL_Upper = 396
            plt.text(16.5, MRL_Upper, 'mixing ratio', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(-50.8, MRL_Upper, '{0}'.format(mixing_ratio_ticks[0][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(-44.6, MRL_Upper, '{0}'.format(mixing_ratio_ticks[1][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(-38.0, MRL_Upper, '{0}'.format(mixing_ratio_ticks[2][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(-33.8, MRL_Upper, '{0}'.format(mixing_ratio_ticks[3][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(-30.9, MRL_Upper, '{0}'.format(mixing_ratio_ticks[4][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(-28.4, MRL_Upper, '{0}'.format(mixing_ratio_ticks[5][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(-23.8, MRL_Upper, '{0}'.format(mixing_ratio_ticks[6][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(-20.6, MRL_Upper, '{0}'.format(mixing_ratio_ticks[7][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(-18, MRL_Upper, '{0}'.format(mixing_ratio_ticks[8][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(-15.8, MRL_Upper, '{0}'.format(mixing_ratio_ticks[9][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(-12.5, MRL_Upper, '{0}'.format(mixing_ratio_ticks[10][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(-9.4, MRL_Upper, '{0}'.format(mixing_ratio_ticks[11][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(-7.2, MRL_Upper, '{0}'.format(mixing_ratio_ticks[12][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(-5.3, MRL_Upper, '{0}'.format(mixing_ratio_ticks[13][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(-3.5, MRL_Upper, '{0}'.format(mixing_ratio_ticks[14][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(-1.8, MRL_Upper, '{0}'.format(mixing_ratio_ticks[15][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(-0.2, MRL_Upper, '{0:.0f}'.format(mixing_ratio_ticks[16][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(2.2, MRL_Upper, '{0:.0f}'.format(mixing_ratio_ticks[17][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(4.3, MRL_Upper, '{0:.0f}'.format(mixing_ratio_ticks[18][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(6.3, MRL_Upper, '{0:.0f}'.format(mixing_ratio_ticks[19][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(8.0, MRL_Upper, '{0:.0f}'.format(mixing_ratio_ticks[20][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(9.4, MRL_Upper, '{0:.0f}'.format(mixing_ratio_ticks[21][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(10.8, MRL_Upper, '{0:.0f}'.format(mixing_ratio_ticks[22][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(12.0, MRL_Upper, '{0:.0f}'.format(mixing_ratio_ticks[23][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(13.2, MRL_Upper, '{0:.0f}'.format(mixing_ratio_ticks[24][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(14.3, MRL_Upper, '{0:.0f}'.format(mixing_ratio_ticks[25][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(15.5, MRL_Upper, '{0:.0f}'.format(mixing_ratio_ticks[26][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            #plt.text(33.8, MRL_Upper, '{0:.0f}'.format(mixing_ratio_ticks[27][0]*1000), 
            #         horizontalalignment='left', verticalalignment='center', 
            #         fontsize=9, color='blue')
            #plt.text(35.3, MRL_Upper, '{0:.0f}'.format(mixing_ratio_ticks[28][0]*1000), 
            #         horizontalalignment='left', verticalalignment='center', 
            #         fontsize=9, color='blue')
            #plt.text(37.2, MRL_Upper, '{0:.0f}'.format(mixing_ratio_ticks[29][0]*1000), 
            #         horizontalalignment='left', verticalalignment='center', 
            #         fontsize=9, color='blue')
            #plt.text(38.8, MRL_Upper, '{0:.0f}'.format(mixing_ratio_ticks[30][0]*1000), 
            #         horizontalalignment='left', verticalalignment='center', 
            #         fontsize=9, color='blue')
            #plt.text(40.2, MRL_Upper, '{0:.0f}'.format(mixing_ratio_ticks[31][0]*1000), 
            #         horizontalalignment='left', verticalalignment='center', 
            #         fontsize=9, color='blue')
            #plt.text(41.8, MRL_Upper, '{0:.0f}'.format(mixing_ratio_ticks[32][0]*1000), 
            #         horizontalalignment='left', verticalalignment='center', 
            #         fontsize=9, color='blue')
            #plt.text(43.0, MRL_Upper, '{0:.0f}'.format(mixing_ratio_ticks[33][0]*1000), 
            #         horizontalalignment='left', verticalalignment='center', 
            #         fontsize=9, color='blue')
            #plt.text(44.2, MRL_Upper, '{0:.0f}'.format(mixing_ratio_ticks[34][0]*1000), 
            #         horizontalalignment='left', verticalalignment='center', 
            #         fontsize=9, color='blue')
            #plt.text(45.4, MRL_Upper, '{0:.0f}'.format(mixing_ratio_ticks[35][0]*1000), 
            #         horizontalalignment='left', verticalalignment='center', 
            #         fontsize=9, color='blue')
            #plt.text(46.9, MRL_Upper, '{0:.0f}'.format(mixing_ratio_ticks[36][0]*1000), 
            #         horizontalalignment='left', verticalalignment='center', 
            #         fontsize=9, color='blue')
            
            ### bottom mixing ratio
            MRL_Under = 1068
            plt.text(-46.5, MRL_Under, 'mixing ratio', 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(-41.1, MRL_Under, '{0}'.format(mixing_ratio_ticks[0][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(-34.2, MRL_Under, '{0}'.format(mixing_ratio_ticks[1][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(-27.0, MRL_Under, '{0}'.format(mixing_ratio_ticks[2][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(-22.5, MRL_Under, '{0}'.format(mixing_ratio_ticks[3][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(-19, MRL_Under, '{0}'.format(mixing_ratio_ticks[4][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(-16.5, MRL_Under, '{0}'.format(mixing_ratio_ticks[5][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(-11.5, MRL_Under, '{0}'.format(mixing_ratio_ticks[6][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(-8.0, MRL_Under, '{0}'.format(mixing_ratio_ticks[7][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(-5, MRL_Under, '{0}'.format(mixing_ratio_ticks[8][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(-2.7, MRL_Under, '{0}'.format(mixing_ratio_ticks[9][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(1.2, MRL_Under, '{0}'.format(mixing_ratio_ticks[10][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(4.4, MRL_Under, '{0}'.format(mixing_ratio_ticks[11][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(7.0, MRL_Under, '{0}'.format(mixing_ratio_ticks[12][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(9.2, MRL_Under, '{0}'.format(mixing_ratio_ticks[13][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(11.3, MRL_Under, '{0}'.format(mixing_ratio_ticks[14][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(13.0, MRL_Under, '{0}'.format(mixing_ratio_ticks[15][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(14.7, MRL_Under, '{0:.0f}'.format(mixing_ratio_ticks[16][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(17.5, MRL_Under, '{0:.0f}'.format(mixing_ratio_ticks[17][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(19.9, MRL_Under, '{0:.0f}'.format(mixing_ratio_ticks[18][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(22.0, MRL_Under, '{0:.0f}'.format(mixing_ratio_ticks[19][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(23.9, MRL_Under, '{0:.0f}'.format(mixing_ratio_ticks[20][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(25.5, MRL_Under, '{0:.0f}'.format(mixing_ratio_ticks[21][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(27.2, MRL_Under, '{0:.0f}'.format(mixing_ratio_ticks[22][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(28.6, MRL_Under, '{0:.0f}'.format(mixing_ratio_ticks[23][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(29.9, MRL_Under, '{0:.0f}'.format(mixing_ratio_ticks[24][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(31.2, MRL_Under, '{0:.0f}'.format(mixing_ratio_ticks[25][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(32.3, MRL_Under, '{0:.0f}'.format(mixing_ratio_ticks[26][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(34.0, MRL_Under, '{0:.0f}'.format(mixing_ratio_ticks[27][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(35.4, MRL_Under, '{0:.0f}'.format(mixing_ratio_ticks[28][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(37.2, MRL_Under, '{0:.0f}'.format(mixing_ratio_ticks[29][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(38.9, MRL_Under, '{0:.0f}'.format(mixing_ratio_ticks[30][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(40.3, MRL_Under, '{0:.0f}'.format(mixing_ratio_ticks[31][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(41.8, MRL_Under, '{0:.0f}'.format(mixing_ratio_ticks[32][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(43.0, MRL_Under, '{0:.0f}'.format(mixing_ratio_ticks[33][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(44.2, MRL_Under, '{0:.0f}'.format(mixing_ratio_ticks[34][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(45.6, MRL_Under, '{0:.0f}'.format(mixing_ratio_ticks[35][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            plt.text(47.0, MRL_Under, '{0:.0f}'.format(mixing_ratio_ticks[36][0]*1000), 
                     horizontalalignment='left', verticalalignment='center', 
                     fontsize=9, color='blue')
            
            # Plot the data using normal plotting functions, in this case using
            # log scaling in Y, as dictated by the typical meteorological plot
            skew.plot(p, T, 'r')
            skew.plot(p, T, 'ro', markersize = 8, fillstyle='none', label='temperature')
            skew.plot(p, Td, 'g', linestyle='--')
            skew.plot(p, Td, 'g^', markersize = 8, fillstyle='none', label='dew point temperature')
            skew.plot_barbs(p, u, v)
                              
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
                      
            plt.text(xxlim[0]+76, yylim[0]+260, '$ \cdotp $ filename : {0}'.format(fullname_el[-1]), 
                     horizontalalignment='left', verticalalignment='center', fontsize=12)
            plt.text(xxlim[0]+77.5, yylim[0]+320, '$ \cdotp $ site : {0}'.format(fullname_el[-3]), 
                     horizontalalignment='left', verticalalignment='center', fontsize=10)
            plt.text(xxlim[0]+79, yylim[0]+380, '$ \cdotp $ time : {0} (UTC)'.format(fullname_el[-1][:16]), 
                     horizontalalignment='left', verticalalignment='center', fontsize=10) 
            
            plt.text(xxlim[0]+77.0, yylim[0]+110, 'Created by guitar79@naver.com using METPY', 
                     horizontalalignment='left', verticalalignment='center', fontsize=18, color='green', alpha=50)
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
            print('#'*60)
            write_log(log_file, '{1} ::: {0} files are created'.format(fullname[:-4], datetime.now()))
            
            # Show the plot
            #plt.show()
            # Close the plot
            plt.switch_backend('Agg'),
            plt.close(fig)
        
        except Exception as err :
            write_log(err_log_file, '{2} ::: {0} with {1}'.format(err, fullname, datetime.now()))
    print('Thread {0} is finished'.format(fullname))
    return 0 # Return a dummy value
    # Putting large values in Queue was slow than expected(~10min)


