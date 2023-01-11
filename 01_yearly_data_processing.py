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

conda install -c conda-forge metpy

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

import rawin_utilities
import Python_utilities


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
BASEDIR = Path(rawin_utilities.BASEDIR)

SONDEDIR = BASEDIR / "UPPER_Sonde"
if not SONDEDIR.exists():
    os.makedirs("{}".format(str(SONDEDIR)))
    print("{} is created...".format(str(SONDEDIR)))

#%%
fpaths = sorted(list(SONDEDIR.glob("*.csv")))
print("fpaths: {}".format(fpaths))

#%%
for fpath in fpaths[1:]:
    print("fpath: ", fpath)
    print("fpath.name: ", fpath.name)
    filename_el = fpath.name.split('_')
    O_code = filename_el[2]
    
    RAWINDAILYDIRCODE = BASEDIR / "Daily" / O_code
    
    if not RAWINDAILYDIRCODE.exists():
        os.makedirs("{}".format(str(RAWINDAILYDIRCODE)))
    print("{} is created...".format(str(RAWINDAILYDIRCODE)))
    with open(fpath) as f:
        print("f:", f)
        print("f.encoding:", f.encoding)
        encoding = f.encoding
    
    df = pd.read_csv(fpath, sep=',', skiprows=1,
                    encoding = encoding,
                    names = ['site', 'dt_str(UTC)', 'pressure(hPa)', 'height', 'temperature(°C)', 
                            'dewpoint(°C)', 'winddirection(deg)', 'windspeed(knot)', 'FLAG1', 'FLAG2', 'FLAG3']
                            )
    df = df.drop_duplicates()
    print("df:", df)

    # %%
    df['dt_YmdH(UTC)'] = pd.to_datetime(df['dt_str(UTC)'])
    df = df.sort_values(by=['dt_YmdH(UTC)', 'pressure(hPa)'],
                        ascending = False)
    print("df[['dt_YmdH(UTC)','pressure(hPa)']]:", df[['dt_YmdH(UTC)', 'pressure(hPa)']])
    # %%
    print("df['dt_YmdH(UTC)'].unique():\n {}".format(df['dt_YmdH(UTC)'].unique()))
    print("type(df['dt_YmdH(UTC)'].unique()):\n {}".format(type(df['dt_YmdH(UTC)'].unique())))
    # %%
    for specific_time in df['dt_YmdH(UTC)'].unique():
        try:
            #print("specific_time.astype(str): ", specific_time.astype(str))
            #specific_time.dt.strftime('%Y-%m-%d %H')
            #%% 
            df_one = df[(df['dt_YmdH(UTC)'] == specific_time)]
            print("df_one:", df_one)
            print("len(df_one):", len(df_one))
            
            #%%
            df_one.to_csv("{}/{}_{}.csv".format(str(RAWINDAILYDIRCODE), 
                                            O_code,
                                            specific_time.astype(str)[:13]))
        except Exception as err :
            print("X"*60)
            print('{0}'.format(err))