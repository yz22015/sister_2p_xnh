## startup script, import modules, load datases

## IMPORTS ==========================================================================================================
import os
import random
import numpy as np
import pandas as pd
from copy import deepcopy
from scipy import stats

import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import colors

## append functions
from mf_analysis import *
from mf_plotting import *


## DIRECTORIES ======================================================================================================
workingDir = '/path_to_downloaded_datasets'

## LOAD VARIABLES ===================================================================================================
load_info = True
load_Ztrim_cell = True
load_Zglobal_cell = True
load_Ztrim_glom = True
load_sisD = True
sampleList = ['Y489', 'Y391', 'C432']

if load_info:
    info = {}
    info['Y489'] = np.load(os.path.join(workingDir, 'Y489_info.npy'), allow_pickle = 'True').item()
    info['Y391'] = np.load(os.path.join(workingDir, 'Y391_info.npy'), allow_pickle = 'True').item()
    info['C432'] = np.load(os.path.join(workingDir, 'C432a_info.npy'), allow_pickle = 'True').item()

if load_Ztrim_cell:
    # default is load neuropil corrected, subsampled to common freq - 10 Hz
    Ztrim_cell = {}
    Ztrim_cell['Y489'] = np.load(os.path.join(workingDir, 'Y489_Ztrim_cell_ss10.npy'), allow_pickle = 'True').item()
    Ztrim_cell['Y391'] = np.load(os.path.join(workingDir, 'Y391_Ztrim_cell_ss10.npy'), allow_pickle = 'True').item()
    Ztrim_cell['C432'] = np.load(os.path.join(workingDir, 'C432a_Ztrim_cell_ss10.npy'), allow_pickle = 'True').item() # default uses C432a

if load_Zglobal_cell:
    # default is load neuropil corrected, subsampled to common freq - 10 Hz
    Zglobal_cell = {}
    Zglobal_cell['Y489'] = np.load(os.path.join(workingDir, 'Y489_Zglobal_cell_ss10.npy'), allow_pickle = 'True').item()
    Zglobal_cell['Y391'] = np.load(os.path.join(workingDir, 'Y391_Zglobal_cell_ss10.npy'), allow_pickle = 'True').item()
    Zglobal_cell['C432'] = np.load(os.path.join(workingDir, 'C432a_Zglobal_cell_ss10.npy'), allow_pickle = 'True').item() # default uses C432a
    
if load_Ztrim_glom:
    # glom signal does not require neuropil correction
    Ztrim_glom = {}
    Ztrim_glom['Y489'] = np.load(os.path.join(workingDir, 'Y489_Ztrim_glom_ss10.npy'), allow_pickle = 'True').item()
    Ztrim_glom['Y391'] = np.load(os.path.join(workingDir, 'Y391_Ztrim_glom_ss10.npy'), allow_pickle = 'True').item()

if load_sisD:
    sisD_all = {}
    sisD_all['Y489'] = np.load(os.path.join(workingDir, 'Y489_sisD.npy'), allow_pickle = 'True').item()
    sisD_all['Y391'] = np.load(os.path.join(workingDir, 'Y391_sisD.npy'), allow_pickle = 'True').item()
    sisD_all['C432'] = np.load(os.path.join(workingDir, 'C432a_sisD.npy'), allow_pickle = 'True').item()

    
## CALCULATIONS - GENERAL ===========================================================================================
calculations = True
if calculations:
    sr10 = 10 # common sampling frequency for all glom, cell data
    
    moPairs = {}
    moPairs['Y489'] = info['Y489']['mo_clean']
    moPairs['Y391'] = list(info['Y391']['modd_odo_map'].keys())
    moPairs['C432'] = list(info['C432']['modd_odo_map'].keys())
    
    glomList_2P = {}
    for i in ['Y489', 'Y391']:
        glomList_2P[i] = info[i]['glom_list_2P']
