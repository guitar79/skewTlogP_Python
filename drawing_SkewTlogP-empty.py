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
from metpy.units import units

import Python_utilities
import rawin_utilities

from metpy.plots import SkewT
from metpy.units import units

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
BASEDIR = 'd:\RS_data\RAWIN_data'
BASEDIR = Path(BASEDIR)

RAWINDIR = BASEDIR / "SkewT-logP_image"

if not RAWINDIR.exists():
    os.makedirs("{}".format(str(RAWINDIR)))
    print("{} is created...".format(str(RAWINDIR)))
#%%

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

skew.ax.set_title('Skew T Adiabatic Diagram\n', fontsize=42) 
skew.ax.set_xlabel(r'temperature (${\degree \mathrm{C}}$)', fontsize=24)
skew.ax.set_ylabel(r'pressure (${\mathrm{hPa}}$)', fontsize=24)

#등온선 그리는 함수
rawin_utilities.add_isothermal(plt, skew, xxlim, yylim)

#기압축 그리는 함수
rawin_utilities.add_isobar(plt, skew, xxlim, yylim)

#건조단열선 그리는 함수
rawin_utilities.add_dry_adiabats(plt, skew, xxlim, yylim)

#습윤단열선 그리는 함수
rawin_utilities.add_moist_adiabats(plt, skew, xxlim, yylim)

#포화혼합비선 그리는 함수
rawin_utilities.add_mising_ratio(plt, skew, xxlim, yylim)

###########################################################
#legend 추가
###########################################################
plt.legend(loc='upper left')

plt.show()
# %%
