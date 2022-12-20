# Copyright (c) 2015,2016,2017 MetPy Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
"""
=================
Advanced Sounding
=================

Plot a sounding using MetPy with more advanced features.

https://unidata.github.io/MetPy/latest/examples/Advanced_Sounding.html#sphx-glr-examples-advanced-sounding-py

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

skew.ax.set_xlim(xxlim[0], xxlim[1])
skew.ax.set_ylim(yylim[0], yylim[1])

# An example of a slanted line at constant T -- in this case the 0
# isotherm
skew.ax.axvline(0, color='c', linestyle='--', linewidth=2)

# Add the relevant special lines
skew.plot_dry_adiabats()
skew.plot_moist_adiabats()
skew.plot_mixing_lines()

# Set title
skew.ax.set_title('Skew T Adiabatic Diagram\n', fontsize=42) 
skew.ax.set_xlabel(r'temperature (${\degree \mathrm{C}}$)', fontsize=24)
skew.ax.set_ylabel(r'pressure (${\mathrm{hPa}}$)', fontsize=24)

plt.save()

plt.savefig('{0}/SkewTlogP_{1}.pdf'.format(str(RAWINDIR), "empty"),
                facecolor='w', edgecolor='w',
                orientation='portrait')

# Show the plot
plt.show()

# %%
