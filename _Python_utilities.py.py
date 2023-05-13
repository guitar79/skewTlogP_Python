# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 01:00:19 2018
@author: guitar79@naver.com

"""

#%%
from datetime import datetime, timedelta
import os
import shutil
from pathlib import Path
import numpy as np

#from astropy.io import fits

#%%
# =============================================================================
# mkdir
# =============================================================================

def mkdir(fpath, mode=0o777, exist_ok=True):
    ''' Convenience function for Path.mkdir()
    '''
    fpath = Path(fpath)
    Path.mkdir(fpath, mode=mode, exist_ok=exist_ok)


#%%
# =============================================================================
# creat log
# =============================================================================

def write_log(log_file, log_str):
    import time
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    msg = '[' + timestamp + '] ' + log_str
    print(msg)
    with open(log_file, 'a') as f:
        f.write(msg + '\n')

def write_log2(log_file, log_str):
    import os
    with open(log_file, 'a') as log_f:
        log_f.write("{}, {}\n".format(os.path.basename(__file__), log_str))
    return print ("{}, {}\n".format(os.path.basename(__file__), log_str))


#%%        
# =============================================================================
# for checking time
# =============================================================================
cht_start_time = datetime.now()
def print_working_time(cht_start_time):
    working_time = (datetime.now() - cht_start_time) #total days for downloading
    return print('working time ::: %s' % (working_time))

#%%
# =============================================================================
#     
# =============================================================================
def nearest_date(items, pivot) :
    nearest = min(items, 
                key=lambda x: abs(x - pivot))
    timedelta = abs(nearest - pivot)
    return nearest, timedelta

def nearest_ind(items, pivot) :
    time_diff = np.abs([date - pivot for date in items])
    return time_diff.argmin(0)

#%%
# =============================================================================
#     
# =============================================================================
def removeAllEmptyDirs(fpath):
    """
    Parameters
    ----------
    fullname : fpath
        The fullname of input directory...

    """
    
    del_N = 0
    for i in range(10) : 
        fullnames = getFullnameListOfallsubDirs(fpath)
        #print ("fullnames: {}".format(fullnames))
        print ("{} directories were found... ".format(len(fullnames)))
        
        for fullname in fullnames[:] :
            # Check is empty..
            print('Check directory {} is empty or not...'.format(fullname))
            if len(os.listdir(fullname)) == 0 :
                # Delete..
                shutil.rmtree(r"{}".format(fullname)) 
                del_N =+1
                print ("rmtree {}\n".format(fullname))
    
    return print("Total {} directories deleted...".format(del_N))

#%%
# =============================================================================
# getFullnameListOfallFiles
# =============================================================================
def getFullnameListOfallFiles(dirName):
    ##############################################3
    import os
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = sorted(os.listdir(dirName))
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getFullnameListOfallFiles(fullPath)
        else:
            allFiles.append(fullPath)
                
    return allFiles


# =============================================================================
# getFullnameListOfallFiles
# =============================================================================

def getFullnameListOfallsubDirs1(dirName):
    ##############################################3
    import os
    allFiles = list()
    for file in sorted(os.listdir(dirName)):
        d = os.path.join(dirName, file)
        allFiles.append(d)
        if os.path.isdir(d):
            allFiles.extend(getFullnameListOfallsubDirs1(d))

    return allFiles


# =============================================================================
# getFullnameListOfallsubDirs
# =============================================================================
def getFullnameListOfallsubDirs(dirName):
    ##############################################3
    import os
    allFiles = list()
    for it in os.scandir(dirName):
        if it.is_dir():
            allFiles.append(it.path)
            allFiles.extend(getFullnameListOfallsubDirs(it))
    allFiles = [w+"/" for w in allFiles]
    return allFiles

# =============================================================================
# getFullnameListOfsubDir
# =============================================================================
def getFullnameListOfsubDir(dirName):
    ##############################################3
    import os
    allFiles = list()
    for it in os.scandir(dirName):
        if it.is_dir():
            allFiles.append(it.path)
    allFiles = [w+"/" for w in allFiles]
    return allFiles
# %%
