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

#https://unidata.github.io/MetPy/latest/api/generated/metpy.calc.html

"""

#%%
import os
from glob import glob
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from datetime import datetime
from dateutil.relativedelta import relativedelta
import metpy.calc as mpcalc
from metpy.units import units as u

import Python_utilities
import rawin_utilities

from metpy.plots import Hodograph, SkewT

#%%
#######################################################
# for log file
log_dir = "logs/"
log_file = "{}{}.log".format(log_dir, os.path.basename(__file__)[:-3])
err_log_file = "{}{}_err.log".format(log_dir, os.path.basename(__file__)[:-3])
print ("log_file: {}".format(log_file))
print ("err_log_file: {}".format(err_log_file))
if not os.path.exists('{0}'.format(log_dir)):
    os.makedirs('{0}'.format(log_dir))
#######################################################

#%%
#######################################################
# read all files in base directory for processing

O_code = "47090"
O_codes = ["47090", "47102", "47104", "47122", "47138", 
        "47155", "47158", "47169", "47185", "47186"]
for O_code in O_codes[:]:
    RAWINDAILYCODEDIR = rawin_utilities.BASEDIR / "Daily" / O_code
    SKEWTLOGPCODEDIR = rawin_utilities.BASEDIR / "SkewTlogP_basic" / O_code

    if not SKEWTLOGPCODEDIR.exists():
        os.makedirs("{}".format(str(SKEWTLOGPCODEDIR)))
        print("{} is created...".format(str(SKEWTLOGPCODEDIR)))


    fpaths = sorted(list(RAWINDAILYCODEDIR.glob("*.csv")))
    print("fpaths: {}".format(fpaths))

    #%%
    for fpath in fpaths[:]:
        print("fpath: ", fpath)
        print("fpath.name: ", fpath.name)
        filename_el = fpath.name.split('_')
        O_code = filename_el[0]
        try:
            with open(fpath) as f:
                print("f:", f)
                print("f.encoding:", f.encoding)
                encoding = f.encoding
        
            df = pd.read_csv(fpath, 
                            #encoding = encoding,
                            encoding = "utf8",
                            sep=',')
            print("df:", df)
            print("df.columns:", df.columns)

            df = df.dropna(subset=('pressure(hPa)', 
                                    'temperature(°C)',
                                    'dewpoint(°C)', 
                                    'windspeed(knot)',
                                    'winddirection(deg)')).reset_index(drop=True)
            df = df.drop_duplicates()

            print("df:", df)
            print("df.columns:", df.columns)
            print("len(df):", len(df))
            # Calculate wind vector
            #%%
            p = df['pressure(hPa)'].values * u.hPa
            T = df['temperature(°C)'].values * u.degC
            Td = df['dewpoint(°C)'].values * u.degC
            u_wind, v_wind = mpcalc.wind_components(df['windspeed(knot)'].values * u.knots, 
                                    np.deg2rad(df['winddirection(deg)'].values * u.deg))

            #%%
            # 한글 폰트 사용을 위해서 세팅
            from matplotlib import font_manager, rc
            font_path = "C:/Windows/Fonts/NGULIM.TTF"
            font = font_manager.FontProperties(fname=font_path).get_name()
            rc('font', family=font)
            ###########################################
            ### Create a new figure. The dimensions here give a good aspect ratio.
            ### Skew T - log P diagram은 가로, 세로 비율이 적절해야 건조단열선, 습윤단열선의 기울기가 적절하게 그려진다.
            ###########################################
            fig = plt.figure(figsize=(12, 8)) 

            # 온도축과 기압축의 범위를 지정해 주자.
            xxlim = [-50, 50] #온도축
            yylim = [1050.1, 99.9] #기압축

            # Grid for plots
            gs = gridspec.GridSpec(4, 3)
            skew = SkewT(fig, rotation=45, subplot=gs[:, :])
            skew.ax.set_xlim(xxlim[0], xxlim[1])
            skew.ax.set_ylim(yylim[0], yylim[1])
            
            #####################################################################
            # 기압에 따른 기온 값을 찍어보자.
            #####################################################################
            # 먼저 점을 찍고
            skew.plot(p, T,
                    'ro', markersize = 8, fillstyle='none', 
                    label = '기온(°C)')
            # 실선도 추가해 주자.
            skew.plot(p, T,
                    'r')
            #####################################################################

            #####################################################################
            # 기압에 따른 이슬점 값을 찍어보자.
            #####################################################################
            # 먼저 점을 찍고
            skew.plot(p, Td,
                    'g^', markersize = 8, fillstyle='none', 
                    label = '이슬점(°C)')
            # 실선도 추가해 주자.
            skew.plot(p, Td,
                    'g', linestyle='--')
            #####################################################################

            #####################################################################
            # 기압에 따른 바람을 표시해 보자.
            #####################################################################
            skew.plot_barbs(p, u_wind, v_wind)
            #####################################################################

            # Calculate LCL height and plot as black dot. Because `p`'s first value is
            # ~1000 mb and its last value is ~250 mb, the `0` index is selected for
            # `p`, `T`, and `Td` to lift the parcel from the surface. If `p` was inverted,
            # i.e. start from low value, 250 mb, to a high value, 1000 mb, the `-1` index
            # should be selected.
            lcl_pressure, lcl_temperature = mpcalc.lcl(p[0], T[0], Td[0])
            skew.plot(lcl_pressure, lcl_temperature, 'ko', markerfacecolor='black')

            # Calculate full parcel profile and add to plot as black line
            prof = mpcalc.parcel_profile(p, T[0], Td[0]).to('degC')
            skew.plot(p, prof, 'k', linewidth=2)

            # Shade areas of CAPE and CIN
            skew.shade_cin(p, T, prof, Td)
            skew.shade_cape(p, T, prof)

            skew.ax.set_title('단열선도', fontsize=18,
                            y = 1.05, pad = 10) 
            skew.ax.set_xlabel(r'기온 (${\degree \mathrm{C}}$)', fontsize=14)
            skew.ax.set_ylabel(r'기압 (${\mathrm{hPa}}$)', fontsize=14)

            # Add the relevant special lines
            skew.ax.axvline(0, label = '등온선')
            skew.plot_dry_adiabats(label = '건조 단열선')
            skew.plot_moist_adiabats(label = '포화 단열선')
            skew.plot_mixing_lines(label = '포화 혼합비선')

            # Put a legend to the right of the current axis
            plt.legend(loc='upper left')
            
            #####################################################################
            # 파일 이름과 해당 날짜를 넣어 주자.
            #####################################################################
            plt.annotate('$ \cdotp $ filename : {0}'.format(fpath.name), 
                            fontsize=7, xy=(0, 1), xytext=(0, 22), va='top', ha='left',
                            xycoords='axes fraction', textcoords='offset points')

            plt.annotate('$ \cdotp $ time : {0} {1}(UTC)'.format(filename_el[1][:10], filename_el[1][11:13]),
                            fontsize=7, xy=(0, 1), xytext=(0, 15), va='top', ha='left',
                            xycoords='axes fraction', textcoords='offset points')

            # plt.annotate('Created by Kiehyun.Park@gmail.com\n using METPY', 
            #                 fontsize=10, xy=(1, 0), xytext=(0, -40), va='top', ha='right',
            #                 xycoords='axes fraction', textcoords='offset points')
            ###########################################################
            ###########################################################

            # # Create a hodograph
            # ax = fig.add_subplot(gs[1:2, -1])
            # #ax.margins(x = 1000, y = 100)
            # ax.set_title("호도 그래프 (바람)", fontsize = 12,
            #                 y = 1.0, pad = 10)
            # h = Hodograph(ax, component_range=100.)
            # h.add_grid(increment=20)
            # h.plot(-u_wind, -v_wind)
            
            # plt.subplots_adjust(left=None, bottom=None, 
            #                         right=None, top=None, wspace=.05, hspace=.05)
            
            plt.savefig("{}/{}_SKewTlogP_basic.png".format(str(SKEWTLOGPCODEDIR), 
                                                            fpath.stem))
            #plt.show()
            plt.close()
        
        except Exception as err :
            print("X"*60)
            print('{0}'.format(err))
