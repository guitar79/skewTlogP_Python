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
BASEDIR = 'c:\RS_data\RAWIN_data'
<<<<<<< HEAD
BASEDIR = 'd:\RS_data\RAWIN_data'
=======
#BASEDIR = 'd:\RS_data\RAWIN_data'
>>>>>>> f7f3545b01e736ecb79eef8b97596f3678980a2c
BASEDIR = Path(BASEDIR)

SKEWTLOGPNDIR = BASEDIR / "SkewTlogP_image" 

if not SKEWTLOGPNDIR.exists():
    os.makedirs("{}".format(str(SKEWTLOGPNDIR)))
    print("{} is created...".format(str(SKEWTLOGPNDIR)))

#%%
O_code = "47090"

RAWINDAILYDIRCODE = BASEDIR / "Daily" / O_code
<<<<<<< HEAD

SKEWTLOGPNSITEDIR = BASEDIR / "SkewTlogP_image" / O_code

if not SKEWTLOGPNSITEDIR.exists():
    os.makedirs("{}".format(str(SKEWTLOGPNSITEDIR)))
print("{} is created...".format(str(SKEWTLOGPNSITEDIR)))
=======
SKEWTLOGPNSITEDIR = BASEDIR / "SkewTlogP_image" / O_code

if not SKEWTLOGPNSITEDIR.exists():
    os.makedirs("{}".format(str(RAWINDAILYDIRCODE)))
print("{} is created...".format(str(RAWINDAILYDIRCODE)))
>>>>>>> f7f3545b01e736ecb79eef8b97596f3678980a2c

fpaths = sorted(list(RAWINDAILYDIRCODE.glob("*.csv")))
print("fpaths: {}".format(fpaths))

#%%
<<<<<<< HEAD
for fpath in fpaths[:]:
=======
for fpath in fpaths[:200]:
>>>>>>> f7f3545b01e736ecb79eef8b97596f3678980a2c
    print("fpath: ", fpath)
    print("fpath.name: ", fpath.name)
    filename_el = fpath.name.split('_')
    O_code = filename_el[0]
    
<<<<<<< HEAD
    df = pd.read_csv(fpath, sep=',', 
                 encoding='utf8')
    #df = pd.read_csv(fpath, sep=',', skiprows=1,
    #                names = ['site', 'dt_str(UTC)', 'pressure(hPa)', 'height', 'temperature(°C)', 
    #                        'dewpoint(°C)', 'winddirection(deg)', 'windspeed(knot)', 'FLAG1', 'FLAG2', 'FLAG3'], 
    #                 encoding='euc-kr')
    #df = pd.read_csv(fpath, sep=',', 
    #                 encoding='euc-kr')
    df = df.dropna(subset=('winddirection(deg)', 
                    'windspeed(knot)'), 
                    ).reset_index(drop=True)
=======
    #df = pd.read_csv(fpath, sep=',', encoding='cp949')
    df = pd.read_csv(fpath, sep=',', skiprows=1,
                    names = ['site', 'dt_str(UTC)', 'pressure(hPa)', 'height', 'temperature(°C)', 
                            'dewpoint(°C)', 'winddirection(deg)', 'windspeed(knot)', 'FLAG1', 'FLAG2', 'FLAG3'], 
                     encoding='euc-kr')
    #df = pd.read_csv(fpath, sep=',', 
    #                 encoding='euc-kr')
    df = df.dropna(subset=('pressure(hPa)', 'temperature(°C)', 
                            'dewpoint(°C)', 'winddirection(deg)', 
                            'windspeed(knot)'), how='all'
               ).reset_index(drop=True)
    df = df.drop_duplicates()
    
    # Calculate wind vector
    df['u_wind'], df['v_wind'] = mpcalc.wind_components(df['windspeed(knot)'].values * u.knots, 
                            np.deg2rad(df['winddirection(deg)'].values * u.deg))

    df = df.dropna(subset=('pressure(hPa)', 'temperature(°C)', 
                            'dewpoint(°C)')#, how='all'
                    ).reset_index(drop=True)

    df = df.drop_duplicates()
    
    print("df:", df)
    print("len(df):", len(df))
    #%%
    #p = df['pressure(hPa)'].values * u.hPa
    #T = df['temperature(°C)'].values * u.degC
    #Td = df['dewpoint(°C)'].values * u.degC

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
    skew = SkewT(fig, rotation=45, subplot=gs[:, :2])
    #####################################################################
    # 기압에 따른 기온 값을 찍어보자.
    #####################################################################
    # 먼저 점을 찍고
    skew.plot(df['pressure(hPa)'].values * u.hPa,  #기압
            df['temperature(°C)'].values * u.degC,  #기온
            'ro', markersize = 8, fillstyle='none', 
            label = 'temperature(°C)')
    
    # 실선도 추가해 주자.
    skew.plot(df['pressure(hPa)'].values * u.hPa,   #기압
            df['temperature(°C)'].values * u.degC,  #기온
            'r')
    #####################################################################

    #####################################################################
    # 기압에 따른 이슬점 값을 찍어보자.
    #####################################################################
    # 먼저 점을 찍고
    skew.plot(df['pressure(hPa)'].values * u.hPa, #기압
            df['dewpoint(°C)'].values * u.degC, # 기온
            'g^', markersize = 8, fillstyle='none', 
            label = 'dew point temperature')
    # 실선도 추가해 주자.
    skew.plot(df['pressure(hPa)'].values * u.hPa, #기압
            df['dewpoint(°C)'].values * u.degC,  #이슬점
            'g', linestyle='--')
    #####################################################################

    #####################################################################
    # 기압에 따른 바람을 표시해 보자.
    #####################################################################
    skew.plot_barbs(df['pressure(hPa)'].values * u.hPa, #기압
            df['u_wind'], 
            df['v_wind'])
    #####################################################################


    #lcl_pressure, lcl_temperature = mpcalc.lcl(p[0], T[0], Td[0])
    #skew.plot(lcl_pressure, lcl_temperature, 'ko', markerfacecolor='black')

    skew.ax.set_title('단열선도', fontsize=18) 
    skew.ax.set_xlabel(r'기온 (${\degree \mathrm{C}}$)', fontsize=14)
    skew.ax.set_ylabel(r'기압 (${\mathrm{hPa}}$)', fontsize=14)

    # Add the relevant special lines
    skew.ax.axvline(0, label = '등온선')
    skew.plot_dry_adiabats(label = '건조 단열선')
    skew.plot_moist_adiabats(label = '포화 단열선')
    skew.plot_mixing_lines(label = '포화 혼합비선')

    # legend 추가
    plt.legend(loc='upper left')

    #####################################################################
    # 파일 이름과 해당 날짜를 넣어 주자.
    #####################################################################
    plt.annotate('$ \cdotp $ filename : {0}'.format(fpath.name), 
                fontsize=10, xy=(1, 0), xytext=(20, 150), va='top', ha='left',
                xycoords='axes fraction', textcoords='offset points')

    plt.annotate('$ \cdotp $ time : {0} {1}(UTC)'.format(filename_el[1][:10], filename_el[1][11:13]),
                fontsize=10, xy=(1, 0), xytext=(20, 130), va='top', ha='left',
                xycoords='axes fraction', textcoords='offset points')

    plt.annotate('Created by Kiehyun.Park@gmail.com\n using METPY', fontsize=10,
                xy=(1, 0), xytext=(0, -40), va='top', ha='right',
                xycoords='axes fraction', textcoords='offset points')
    ###########################################################
    ###########################################################

    # Create a hodograph

    ax = fig.add_subplot(gs[1:2, -1])
    h = Hodograph(ax, component_range=60.)
    h.add_grid(increment=20)
    h.plot(df['u_wind'], 
            df['v_wind'])
    ax.set_title("\n\n Wind hodograph", fontsize = 14)
    plt.savefig("{}/{}/{}_SKewTlogP_basic.png".format(str(SKEWTLOGPNDIR), 
                                                       O_code,
                                                       fpath.stem))
    #plt.show()
    #plt.close()
    # %%
