# Copyright (c) 2016,2017 MetPy Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
"""
===========================
Upper Air Sounding Tutorial
===========================

Upper air analysis is a staple of many synoptic and mesoscale analysis
problems. In this tutorial we will gather weather balloon data, plot it,
perform a series of thermodynamic calculations, and summarize the results.
To learn more about the Skew-T diagram and its use in weather analysis and
forecasting, checkout `this <https://homes.comet.ucar.edu/~alanbol/aws-tr-79-006.pdf>`_
air weather service guide.
conda install xarray=0.12.1

#https://unidata.github.io/MetPy/latest/api/generated/metpy.calc.html

"""
from glob import glob
import os
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from dateutil.relativedelta import relativedelta
import numpy as np
import pandas as pd
from datetime import datetime
import metpy.calc as mpcalc
from metpy.plots import Hodograph, SkewT
from metpy.units import units


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
dir_name = '../rawin_data/47138/'
save_dir_name = 'skew_T-log_P-diagram/'

if not os.path.exists(dir_name+save_dir_name):
    os.makedirs(dir_name+save_dir_name)
    print ('*'*80)
    print (dir_name+save_dir_name, 'is created')
else :
    print ('*'*80)
    print (dir_name+save_dir_name, 'is exist')
    
filename = 'UPPER_SONDE_47138_ALL_2018_2018_2019.csv'

fullname = dir_name + filename
fullname =sorted(glob(os.path.join(dir_name, '*.csv')))[-1]
#%%
fullname_el = fullname.split('\\')
filename = fullname_el[-1]
filename_el = filename.split('_')
obs_year = int(filename_el[-3])

#지점,일시(UTC),기압(hPa),고도(gpm),기온(°C),이슬점온도(°C),풍향(deg),풍속(knot),지상 FLAG(null),권계면 FLAG(null),최대풍 FLAG(null)
df = pd.read_csv(dir_name+filename, skiprows=1, sep=',', header=None, index_col=0,
                   names = ['site', 'time', 'pressure', 'height', 'temperature', 'dewpoint', 'direction', 'speed', 'FLAG1', 'FLAG2', 'FLAG3'],
                   skipfooter=1, engine='python')

df['u_wind'], df['v_wind'] = mpcalc.wind_components(df['speed'],
                                                    np.deg2rad(df['direction']))
#%%
# Drop any rows with all NaN values for T, Td, winds
#df = df.dropna(subset=('temperature', 'dewpoint', 'direction', 'speed', 'u_wind', 'v_wind'), how='all').reset_index(drop=True)
df = df.dropna(subset=('temperature', 'dewpoint'), how='all').reset_index(drop=True)

#%%
# Rows that do not meet the condition alpha + num are eliminated
s_start_date = datetime(obs_year, 1, 1) #convert startdate to date type
s_end_date = datetime(obs_year, 12, 31)

date1 = s_start_date
selected_times = []
while date1 < s_end_date : 
    date1_strf = date1.strftime('%Y-%m-%d %H:%M')
    selected_times.append(date1_strf)
    date1 = date1 + relativedelta(hours=12)

#%%
#for selected_time in selected_times[0:10] :
selected_time  = selected_times[0]
print(selected_time)

f = lambda s: selected_time in s
ids  = df['time'].apply(f)
df_selected_time = df[ids]

#df_selected_time = df_selected_time.dropna()
df_selected_time = df_selected_time.sort_values('pressure', ascending=False)
print(df_selected_time)

df_selected_time.to_csv(r'{0}{1}{2}_{3}.csv'.format(dir_name, save_dir_name, filename_el[-5], selected_time[:13]))
###########################################
# We will pull the data out of the example dataset into individual variables and
# assign units.
            

##########################################################################
# We will pull the data out of the example dataset into individual variables and
# assign units.

p = df_selected_time['pressure'].values * units.hPa
T = df_selected_time['temperature'].values * units.degC
Td = df_selected_time['dewpoint'].values * units.degC
wind_speed = df_selected_time['speed'].values * units.knots
wind_dir = df_selected_time['direction'].values * units.degrees
u, v = mpcalc.wind_components(wind_speed, wind_dir)

##########################################################################
# Thermodynamic Calculations
# --------------------------
#
# Often times we will want to calculate some thermodynamic parameters of a
# sounding. The MetPy calc module has many such calculations already implemented!
#
# * **Lifting Condensation Level (LCL)** - The level at which an air parcel's
#   relative humidity becomes 100% when lifted along a dry adiabatic path.
# * **Parcel Path** - Path followed by a hypothetical parcel of air, beginning
#   at the surface temperature/pressure and rising dry adiabatically until
#   reaching the LCL, then rising moist adiabatially.

# Calculate the LCL
lcl_pressure, lcl_temperature = mpcalc.lcl(p[0], T[0], Td[0])

print(lcl_pressure, lcl_temperature)

# Calculate the parcel profile.
parcel_prof = mpcalc.parcel_profile(p, T[0], Td[0]).to('degC')

##########################################################################
# Basic Skew-T Plotting
# ---------------------
#
# The Skew-T (log-P) diagram is the standard way to view rawinsonde data. The
# y-axis is height in pressure coordinates and the x-axis is temperature. The
# y coordinates are plotted on a logarithmic scale and the x coordinate system
# is skewed. An explanation of skew-T interpretation is beyond the scope of this
# tutorial, but here we will plot one that can be used for analysis or
# publication.
#
# The most basic skew-T can be plotted with only five lines of Python.
# These lines perform the following tasks:
#
# 1. Create a ``Figure`` object and set the size of the figure.
#
# 2. Create a ``SkewT`` object
#
# 3. Plot the pressure and temperature (note that the pressure,
#    the independent variable, is first even though it is plotted on the y-axis).
#
# 4. Plot the pressure and dewpoint temperature.
#
# 5. Plot the wind barbs at the appropriate pressure using the u and v wind
#    components.

# Create a new figure. The dimensions here give a good aspect ratio
fig = plt.figure(figsize=(9, 9))
skew = SkewT(fig)

# Plot the data using normal plotting functions, in this case using
# log scaling in Y, as dictated by the typical meteorological plot
skew.plot(p, T, 'r', linewidth=2)
skew.plot(p, Td, 'g', linewidth=2)
skew.plot_barbs(p, u, v)

# Show the plot
plt.show()

##########################################################################
# Advanced Skew-T Plotting
# ------------------------
#
# Fiducial lines indicating dry adiabats, moist adiabats, and mixing ratio are
# useful when performing further analysis on the Skew-T diagram. Often the
# 0C isotherm is emphasized and areas of CAPE and CIN are shaded.

# Create a new figure. The dimensions here give a good aspect ratio
fig = plt.figure(figsize=(9, 9))
skew = SkewT(fig, rotation=30)

# Plot the data using normal plotting functions, in this case using
# log scaling in Y, as dictated by the typical meteorological plot
skew.plot(p, T, 'r')
skew.plot(p, Td, 'g')
skew.plot_barbs(p, u, v)
skew.ax.set_ylim(1050, 100)
skew.ax.set_xlim(-40, 60)

# Plot LCL temperature as black dot
skew.plot(lcl_pressure, lcl_temperature, 'ko', markerfacecolor='black')

# Plot the parcel profile as a black line
skew.plot(p, parcel_prof, 'k', linewidth=2)

# Shade areas of CAPE and CIN
skew.shade_cin(p, T, parcel_prof)
skew.shade_cape(p, T, parcel_prof)

# Plot a zero degree isotherm
skew.ax.axvline(0, color='c', linestyle='--', linewidth=2)

# Add the relevant special lines
skew.plot_dry_adiabats()
skew.plot_moist_adiabats()
skew.plot_mixing_lines()

# Show the plot
plt.show()

##########################################################################
# Adding a Hodograph
# ------------------
#
# A hodograph is a polar representation of the wind profile measured by the rawinsonde.
# Winds at different levels are plotted as vectors with their tails at the origin, the angle
# from the vertical axes representing the direction, and the length representing the speed.
# The line plotted on the hodograph is a line connecting the tips of these vectors,
# which are not drawn.

# Create a new figure. The dimensions here give a good aspect ratio
fig = plt.figure(figsize=(9, 9))
skew = SkewT(fig, rotation=30)

# Plot the data using normal plotting functions, in this case using
# log scaling in Y, as dictated by the typical meteorological plot
skew.plot(p, T, 'r')
skew.plot(p, Td, 'g')
skew.plot_barbs(p, u, v)
skew.ax.set_ylim(1050, 100)
skew.ax.set_xlim(-40, 60)

# Plot LCL as black dot
skew.plot(lcl_pressure, lcl_temperature, 'ko', markerfacecolor='black')

# Plot the parcel profile as a black line
skew.plot(p, parcel_prof, 'k', linewidth=2)

# Shade areas of CAPE and CIN
skew.shade_cin(p, T, parcel_prof)
skew.shade_cape(p, T, parcel_prof)

# Plot a zero degree isotherm
skew.ax.axvline(0, color='c', linestyle='--', linewidth=2)

# Add the relevant special lines
skew.plot_dry_adiabats()
skew.plot_moist_adiabats()
skew.plot_mixing_lines()

# Create a hodograph
# Create an inset axes object that is 40% width and height of the
# figure and put it in the upper right hand corner.
ax_hod = inset_axes(skew.ax, '40%', '40%', loc=1)
h = Hodograph(ax_hod, component_range=80.)
h.add_grid(increment=20)
h.plot_colormapped(u, v, wind_speed)  # Plot a line colored by wind speed

# Show the plot
plt.show()
