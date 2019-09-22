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

conda install xarray=0.12.1

"""
#%%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import metpy.calc as mpcalc
#from metpy.cbook import get_test_data
#from metpy.plots import add_metpy_logo, SkewT
from metpy.plots import SkewT
from metpy.units import units

#import shutil
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
dir_name = '../47090/'
file_name = 'UPPER_SONDE_47090_ALL_2011_2011_2015.csv'
file_name_el = file_name.split('_')

#지점,일시(UTC),기압(hPa),고도(gpm),기온(°C),이슬점온도(°C),풍향(deg),풍속(knot),지상 FLAG(null),권계면 FLAG(null),최대풍 FLAG(null)
df = pd.read_csv(dir_name+file_name, skiprows=1, sep=',', header=None, index_col=0,
                 names = ['site', 'time', 'pressure', 'height', 'temperature', 'dewpoint', 'direction', 'speed', 'FLAG1', 'FLAG2', 'FLAG3'],
                 skipfooter=1, engine='python')

df.drop_duplicates(keep = 'first', inplace = True) 

df.to_csv(r'{0}.csv'.format(file_name[:-4]))

f = open('{0}.csv'.format(file_name[:-4]), 'r', encoding = 'unicode_escape')
f = f.read()
rows = f.split("\n")
#%%
#df_new = df.drop_duplicates(subset = ['time', 'pressure', 'temperature', 'dewpoint'], keep='first')
#df_new.to_csv(r'{0}/{1}_subset.csv'.format(dir_name, file_name))
new_data = ""
previous_p = 0.0
tt = ' 00:00'
#for i in range(df_new.size) : 
for row in rows : 
    d = row.split(",")
    #if 'hPa' in d[2] :
    if 'pressure' in d[2] :
        continue
    elif previous_p > float(d[2]):
        if tt == ' 00:00' : tt = ' 06:00'
        elif tt == ' 06:00' : tt = ' 12:00'
        elif tt == ' 12:00' : tt = ' 18:00'
        elif tt == ' 18:00' : tt = ' 00:00'
    d[1] += tt
    for j in range(len(d)) : 
        new_data += d[j] + ","
    new_data += "\n"
    
    print(d[1] + tt, previous_p, d[2])

    previous_p = float(d[2])
#%%
with open("{0}.csv".format(file_name[:-4]), "w") as text_file:
    text_file.write(new_data)
        
        