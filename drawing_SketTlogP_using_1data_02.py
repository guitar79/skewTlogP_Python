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

log_dir = "logs/"
log_file = "{}{}.log".format(log_dir, os.path.basename(__file__)[:-3])
err_log_file = "{}{}_err.log".format(log_dir, os.path.basename(__file__)[:-3])
print ("log_file: {}".format(log_file))
print ("err_log_file: {}".format(err_log_file))
    

base_dr = '../1data/'

for dir_names in sorted(os.listdir(base_dr)):
    for dir_name in sorted(os.listdir('{0}{1}/'.format(base_dr, dir_names))):
        fullnames = sorted(glob(os.path.join('{0}{1}/{2}/'\
                 .format(base_dr, dir_names, dir_name), '*solution.csv')))
        
        for fullname in fullnames :
            print('filename.\n {0}'.format(fullname))
            _rawin_utilities.drawing_SkewT_logP_using1data(fullname, base_dr, dir_name)