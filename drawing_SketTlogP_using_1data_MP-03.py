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

#https://unidata.github.io/MetPy/latest/api/generated/metpy.calc.html

"""

from glob import glob
import os
import _rawin_utilities

add_log = True
if add_log == True :
    log_file = 'drawing_SkewT-logP_using_1data.log'
    err_log_file = 'drawing_SkewT-logP_using_1data_err.log'
    
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
 

###########################################
    
myMP = Multiprocessor()
num_cpu = 18

base_dr = '../1data/'

for dir_names in sorted(os.listdir(base_dr)):
    for dir_name in sorted(os.listdir('{0}{1}/'.format(base_dr, dir_names))):
        fullnames = sorted(glob(os.path.join('{0}{1}/{2}/'\
                 .format(base_dr, dir_names, dir_name), '*solution.csv')))
        values = []
        num_batches = len(fullnames) // num_cpu + 1
        for batch in range(num_batches):
            myMP.restart()
            for fullname in fullnames[batch*num_cpu:(batch+1)*num_cpu] :
                print('filename.\n {0}'.format(fullname))
                #myMP.run(f, fullname)
                myMP.run(_rawin_utilities.drawing_SkewT_logP_using1data, fullname, base_dr, dir_name)
            print("Batch " + str(batch))
            myMP.wait()
            #values.append(myMP.wait())
            print("OK batch" + str(batch))