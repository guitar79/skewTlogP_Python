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
import rawin_utility

add_log = True
if add_log == True :
    log_file = 'drawing_SkewT-logP_using_1data.log'
    err_log_file = 'drawing_SkewT-logP_using_1data_err.log'
    

base_dir_name = '../1data/'

for dir_names in sorted(os.listdir(base_dir_name)):
    for dir_name in sorted(os.listdir('{0}{1}/'.format(base_dir_name, dir_names))):
        fullnames = sorted(glob(os.path.join('{0}{1}/{2}/'\
                 .format(base_dir_name, dir_names, dir_name), '*solution.csv')))
        
        for fullname in fullnames :
            print('filename.\n {0}'.format(fullname))
            rawin_utility.drawing_SkewT_logP_using1data(fullname, base_dir_name, dir_name)