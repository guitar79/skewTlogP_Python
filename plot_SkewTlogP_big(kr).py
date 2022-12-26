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

from datetime import datetime
from dateutil.relativedelta import relativedelta
import metpy.calc as mpcalc
from metpy.units import units as u

import Python_utilities
import rawin_utilities

from metpy.plots import SkewT

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
#BASEDIR = 'd:\RS_data\RAWIN_data'
BASEDIR = Path(BASEDIR)

SKEWTLOGPNDIR = BASEDIR / "SkewTlogP_image" 

if not SKEWTLOGPNDIR.exists():
    os.makedirs("{}".format(str(SKEWTLOGPNDIR)))
    print("{} is created...".format(str(SKEWTLOGPNDIR)))

#%%
O_code = "47090"

RAWINDAILYDIRCODE = BASEDIR / "Daily" / O_code
SKEWTLOGPNSITEDIR = BASEDIR / "SkewTlogP_image" / O_code

if not SKEWTLOGPNSITEDIR.exists():
    os.makedirs("{}".format(str(RAWINDAILYDIRCODE)))
print("{} is created...".format(str(RAWINDAILYDIRCODE)))

fpaths = sorted(list(RAWINDAILYDIRCODE.glob("*.csv")))
print("fpaths: {}".format(fpaths))

#%%
for fpath in fpaths[:2]:
    print("fpath: ", fpath)
    print("fpath.name: ", fpath.name)
    filename_el = fpath.name.split('_')
    O_code = filename_el[0]
    
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
    print("df:", df)
    print("len(df):", len(df))
    #%%
    p = df['pressure(hPa)'].values * u.hPa
    T = df['temperature(°C)'].values * u.degC
    Td = df['dewpoint(°C)'].values * u.degC
    wind_speed = df['windspeed(knot)'].values * u.knots
    wind_dir = df['winddirection(deg)'].values * u.degrees
    u, v = mpcalc.wind_components(wind_speed, wind_dir)
    
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
    fig = plt.figure(figsize=(28, 24)) 

    # 온도축과 기압축의 범위를 지정해 주자.
    xxlim = [-50, 50] #온도축
    yylim = [1050.1, 99.9] #기압축

    #온도 축의 기울기를 지정한다.
    skew = SkewT(fig, rotation=45)

    skew.ax.set_title('단열선도', fontsize=42) 
    skew.ax.set_xlabel(r'기온 (${\degree \mathrm{C}}$)', fontsize=24)
    skew.ax.set_ylabel(r'기압 (${\mathrm{hPa}}$)', fontsize=24)


    graph = rawin_utilities.draw_skewT_logP(skew)
    # 등온선 그리는 함수
    graph.add_isothermal()

    # 기압축 그리는 함수
    graph.add_isobar()

    # 건조단열선 그리는 함수
    graph.add_dry_adiabats()

    # 습윤단열선 그리는 함수
    graph.add_moist_adiabats()

    # 포화혼합비선 그리는 함수
    graph.add_mising_ratio()

    # legend 추가
    plt.legend(loc='upper left')

    ###########################################################
    #####아래에 코딩을 완성하시오...
    ###########################################################
    # input some text for explaination.
    plt.annotate('$ \cdotp $ LCL ( {} ): \n$ \cdotp $ LCF ( {} ):\n$ \cdotp $ EL  ( {} ): ' \
                .format('o', 'x', 'o'), fontsize=14,
                xy=(0, 0), xytext=(0, -12), va='top', ha='left',
                xycoords='axes fraction', textcoords='offset points')

    plt.annotate('$ \cdotp $ filename :\n$ \cdotp $ time :' \
                .format('o', 'x', 'o'), fontsize=14,
                xy=(0, 1), xytext=(0, 32), va='top', ha='left',
                xycoords='axes fraction', textcoords='offset points')

    plt.annotate('Created by Kiehyun.Park@gmail.com using METPY', fontsize=20,
                xy=(1, 0), xytext=(0, -50), va='top', ha='right',
                xycoords='axes fraction', textcoords='offset points')
    ###########################################################
    ###########################################################

    plt.savefig("{}/SKewTlogP_big_(kr).png".format(str(SKEWTLOGPNDIR)))

    plt.show()
    # %%
