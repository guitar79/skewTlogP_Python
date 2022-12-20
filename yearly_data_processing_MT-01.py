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

from glob import glob
from pathlib import Path
import numpy as np
import os
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import metpy.calc as mpcalc
#from metpy.cbook import get_test_data
#from metpy.plots import add_metpy_logo, SkewT
from metpy.units import units
import rawin_utilities


################################################
### Multiprocessing instead of multithreading
################################################
import multiprocessing as proc
myQueue = proc.Manager().Queue()

# I love the OOP way.(Custom class for multiprocessing)
class Multiprocessor():
    def __init__(self):
        self.processes = []
        self.queue = proc.Queue()

    @staticmethod
    def _wrapper(func, args, kwargs):
        ret = func(*args, **kwargs)
        myQueue.put(ret)

    def restart(self):
        self.processes = []
        self.queue = proc.Queue()

    def run(self, func, *args, **kwargs):
        args2 = [func, args, kwargs]
        p = proc.Process(target=self._wrapper, args=args2)
        self.processes.append(p)
        p.start()

    def wait(self):
        for p in self.processes:
            p.join()
        rets = []
        for p in self.processes:
            ret = myQueue.get_nowait()

            rets.append(ret)
        for p in self.processes:
            p.terminate()
        return rets


myMP = Multiprocessor()
num_cpu = 4

base_dir_name = '../yearly_data/'

save_base_dir_name = '../1data/'
if not os.path.exists('{0}'.format(save_base_dir_name)):
    os.makedirs('{0}'.format(save_base_dir_name))
    print ('*'*80)
    print ('{0} is created'.format(save_base_dir_name))
else :
    print ('*'*80)
    print ('{0} is exist'.format(save_base_dir_name))
            

dir_names = ['47090/', '47102/', '47104/', '47122/', '47138/', 
             '47155/', '47158/', '47169/', '47185/', '47186/']

for dir_name in dir_names:
        
    #filename = 'UPPER_SONDE_47122_ALL_2018_2018_2019.csv'
    
    for fullname in sorted(glob(os.path.join(base_dir_name+dir_name, '*.csv'))):
        
        fullname_el = fullname.split('/')
        #fullname_el = fullname.split('\\')
        filename = fullname_el[-1]
        filename_el = filename.split('_')
        obs_year = int(filename_el[-3])
        
        save_dir_name = '{0}{1}/'.format(save_base_dir_name+dir_name,obs_year)
            
        if not os.path.exists('{0}'.format(save_dir_name)):
            os.makedirs('{0}'.format(save_dir_name))
            print ('*'*80)
            print ('{0} is created'.format(save_dir_name))
        else :
            print ('*'*80)
            print ('{0} is exist'.format(save_dir_name))

        ###########################################
        ### Upper air data can be obtained using the siphon package, but for this example we will use
        ### some of MetPy's sample data.
            
        #######################################################################################
        ###지점,일시(UTC),기압(hPa),고도(gpm),기온(°C),이슬점온도(°C),풍향(deg),풍속(knot),
        ###지상 FLAG(null),권계면 FLAG(null),최대풍 FLAG(null)
        df = pd.read_csv(base_dir_name+dir_name+filename, skiprows=1, sep=',', header=None, index_col=0,
                           names = ['site', 'time', 'pressure', 'height', 'temperature', 
                                    'dewpoint', 'direction', 'speed', 'FLAG1', 'FLAG2', 'FLAG3'],
                           skipfooter=0, engine='python')
        
        df['u_wind'], df['v_wind'] = mpcalc.wind_components(df['speed'].values * units.knots, 
                                            np.deg2rad(df['direction'].values * units.deg))
        
        # Drop any rows with all NaN values for T, Td
        df = df.dropna(subset=('temperature', 'dewpoint'), how='all').reset_index(drop=True)
        # Rows that do not meet the condition alpha + num are eliminated
        s_start_date = datetime(obs_year, 1, 1) #convert startdate to date type
        s_end_date = datetime(obs_year+1, 1, 1)
        
        selected_times = []
        while s_start_date < s_end_date : 
            date1_strf = s_start_date.strftime('%Y-%m-%d %H:%M')
            selected_times.append(date1_strf)
            s_start_date = s_start_date + relativedelta(hours=6)
    
        values = []
        num_batches = len(selected_times) // num_cpu + 1
        for batch in range(num_batches):
            myMP.restart()
            for selected_time in selected_times[batch*num_cpu:(batch+1)*num_cpu]:
                print('selected_time.\n {0}'.format(selected_time))
                #myMP.run(f, fullname, selected_time)
                myMP.run(rawin_utilities.yearly_data_process_df_seleted_date, fullname, df, selected_time, save_dir_name, dir_name)

        print("Batch " + str(batch))
        myMP.wait()
        #values.append(myMP.wait())
        print("OK batch" + str(batch))