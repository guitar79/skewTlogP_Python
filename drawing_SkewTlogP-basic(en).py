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

O_code = "47155"

SKEWTLOGPNSITEDIR = BASEDIR / "SkewTlogP_image" / O_code

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

#온도 축의 기울기를 지정한다.
skew = SkewT(fig, rotation=45)

skew.ax.set_title('Skew T Adiabatic Diagram', fontsize=18) 
skew.ax.set_xlabel(r'temperature (${\degree \mathrm{C}}$)', fontsize=14)
skew.ax.set_ylabel(r'pressure (${\mathrm{hPa}}$)', fontsize=14)

# Add the relevant special lines
skew.ax.axvline(0, label = 'isothermal')
skew.plot_dry_adiabats(label = 'dry adiabats')
skew.plot_moist_adiabats(label = 'satutation adiabat')
skew.plot_mixing_lines(label = 'saturation mising ratio')

# legend 추가
plt.legend(loc='upper left')

###########################################################
#####아래에 코딩을 완성하시오...
###########################################################

plt.annotate('Created by Kiehyun.Park@gmail.com\n using METPY', fontsize=10,
             xy=(1, 0), xytext=(0, -40), va='top', ha='right',
             xycoords='axes fraction', textcoords='offset points')
###########################################################
###########################################################

plt.savefig("{}/SKewTlogP_basic(en).png".format(str(SKEWTLOGPNDIR)))
plt.show()
plt.close()
# %%
