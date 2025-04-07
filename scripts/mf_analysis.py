## analysis functions
#%% IMPORTS ----------------------------------------------------------------------------------------------------
import numpy as np
import pandas as pd



#%% OPERATIONS ON Ftrim ----------------------------------------------------------------------------------------------------
## get average over trials
def get_Favg(Ftrim, cellList, moPairs):
    """
    intro: trial average Ca trace for specified cells and odours
    Inputs:
        Ftrim: dictionary, keys are plane-roi pair, then modd - channel pair, e.g. Ftrim['TC_plane2_114']['mod01_odour1'].shape = (4, 40000)
        cellList: a list of cell names to get the average for e.g. info['TC_list']
        moPairs: a list of stimulus name to get the average for e.g. list(info['modd_odo_map'])
    """
    Favg = {}

    for i in cellList:
        Favg[i] = {}
        for j in moPairs:
            Favg[i][j] = np.mean(Ftrim[i][j], axis = 0)
    return Favg


## get the min max value of Ftrim for specified cell, odour, repeat and time window
def get_Ftrim_subset_min_max(Ftrim, cList, moList, rList, sampRate, start_s, end_s):
    """
    get the min and max value of Ftrim of specified cells, odours and repeats and specified time window
    rList: 1-indexing e.g. [1, 2, 3, 4]
    """
    rList = [i-1 for i in rList]
    dmin = []
    dmax = []
    start_dp = int(sampRate * start_s)
    end_dp = int(sampRate * end_s)
    for c in cList:
        for o in moList:
            dmin.append(np.min(Ftrim[c][o][rList, start_dp : end_dp]))
            dmax.append(np.max(Ftrim[c][o][rList, start_dp : end_dp]))
    dmin = np.min(dmin)
    dmax = np.max(dmax)
    
    return dmin, dmax


## get response integrals (specified repeats for Favg), for specified time window
def get_Fint_startEnd_selectedRepeats(Ftrim, cellList, moPairs, sampRate, start_s, end_s, repeatNames = [1, 2, 3, 4]):
    """
    intro: sum up responses within specified time window divided by sampling rate, also calculate the trial average
    Ftrim: dictionary, keys are plane-roi pair, then modd - channel pair, e.g. Ftrim['TC_plane2_114']['mod01_odour1'].shape = (4, 40000)
    cellList: a list of cell names to get the average for e.g. info['TC_list']
    moPairs: a list of stimulus name to get the average for e.g. list(info['modd_odo_map'])
    samRate: sampling rate of the Ca data e.g. 1000 Hz
    repeatIdx: a list of repeats to use for calculating Favg, 1-indexing
    """

    Fint = {}
    Fintavg = {}
    
    # slice index needs to be integers
    start_dp = int(start_s * sampRate)
    end_dp = int(end_s * sampRate)

    repeatIdx = [a - 1 for a in repeatNames]

    for i in cellList:
        Fint[i] = {}
        Fintavg[i] = {}

        for j in moPairs:
            d = Ftrim[i][j][:, start_dp:end_dp]

            Fint[i][j] = np.sum(d, axis = 1)/sampRate

            Fintavg[i][j] = np.mean(Fint[i][j][repeatIdx], axis = 0)

    return Fint, Fintavg


#%% OPERATIONS ON Fint ----------------------------------------------------------------------------------------------------
## normalise Fintavg
def get_Fintavg_norm(Fintavg, normMethod = 'byColStd', returnType = 'df'):
    """
    Normalises Fintavg.
    Fintavg: dict, e.g. Fintavg['glom01']['mod01_01'] = float
    Fintavg_df column = roi, row = odour
    normMethod:
        'byColStd': divide by cell's std of Fintavg i.e. preserving relative response sizes across odours, so to compare cells with diff. sizes of fluorescence response
        'byRowStd': divide by odours std of Fintavg i.e. preserving the relatibe response sizes across cells, so to compare odours
        can add more methods in the future
    returnType: 'df': output a pandas dataframe, 'dict': output a dict, 'np': numpy array, factor': outputs the factors used to normalise rows/columns
    """
    #output_df = True, output_factor = False

    Fintavg_df = pd.DataFrame.from_dict(Fintavg)
    # now row is odour, column is roi

    if normMethod == 'byRowStd':
        stim_std = Fintavg_df.std(axis = 1)
        Fintavg_norm_df = Fintavg_df.div(stim_std, axis = 0)
    
    if normMethod == 'byColStd':
        roi_std = Fintavg_df.std(axis = 0)
        Fintavg_norm_df = Fintavg_df.div(roi_std, axis = 1)
    

    if returnType == 'df':
        return Fintavg_norm_df
    elif returnType == 'dict':
        Fintavg_norm_dict = Fintavg_norm_df.to_dict()
        return Fintavg_norm_dict
    elif returnType == 'np':
        return Fintavg_norm_df.values
    elif returnType == 'factor':
        if normMethod == 'byRowStd':
            return stim_std
        elif normMethod == 'byColStd':
            return roi_std


#%% OPERATIONS ON CORRELATION MATRIX -----------------------------------------------------------------------------------
## calculate correlation between 2 dataframes (Pearson)
def get_corrM(df1, df2, method = 'byCol'):
    """
    df1, df2: dataframes, rows = odours, cols = rois
    method: 
        'byCol' requires df1 and df2 need to share the same index, but can have. diff. columns (e.g. correlating the odour vector among each roi pair)
        'byRow' requires df1 and df2 to share columns but can have diff. index
    """

    if method == 'byCol':
        # make sure the dataframes have the same index names
        if df1.index.to_list() != df2.index.to_list():
            raise ValueError('dataframes do not share index!')
    
        col1 = list(df1.columns)
        col2 = list(df2. columns)
        
        M = pd.DataFrame(index = col1, columns = col2, dtype = float)
        for i in col1:
            for j in col2:
                a = list(df1[i])
                b = list(df2[j])
                M[j][i] = np.corrcoef(a, b)[0,1]

    if method == 'byRow':
        # make sure the dataframes have the same column names
        if df1.columns.to_list() != df2.columns.to_list():
            raise ValueError('dataframes do not share columns!')
    
        index1 = list(df1.index)
        index2 = list(df2.index)
        
        M = pd.DataFrame(index = index1, columns = index2, dtype = float)
        for i in index1:
            for j in index2:
                a = list(df1.T[i])
                b = list(df2.T[j])
                M[j][i] = np.corrcoef(a, b)[0,1]
    return M


## get subset of corr values for self, sister and stranger
def get_corrM_subset_self_sis_stranger(corrM, sisD):
    """
    from a correlation matrix (needs to be a dataframe with cells as col and index names),
    subset out all self correlation, all sister correlation and all stranger correlation,
    differs from get_avgCorrM_xx series in that this does not contain any averageing per cell etc.
    only subsetting
    """
    cellList = sisD['cell_list']
    glomList = sisD['glom_list']
    
    corr_self = []
    corr_sis = []
    corr_stranger = []
    
    for idx1, c1 in enumerate(cellList):
        for idx2, c2 in enumerate(cellList):
            # this ensures that only count each cell pair once
            if idx2 >= idx1:
                g1 = glomList[idx1]
                g2 = glomList[idx2]
                
                # is it self
                if c1 == c2:
                    corr_self.append(corrM.loc[c1, c2])
                else:
                    # is it sister
                    if g1 == g2:
                        corr_sis.append(corrM.loc[c1, c2])
                    # is it stranger
                    else:
                        corr_stranger.append(corrM.loc[c1, c2])
                        
    corrDict = {'self': corr_self, 'sister': corr_sis, 'stranger': corr_stranger}
    return corrDict


## get avg values for each cell, save as a dataframe
def get_avgCorr_self_sis_stranger_perCell(corrM, sisD):
    """
    get a table of avg. correlation values, row = cell, column = self, sister, stranger
    corrM: pd dataframe, contains correlation of each cell against each other cell
    sisD: dict, contains cell list and glom list which is used to tell apart sister vs stranger cells
    """
    avgCorr_byCell = {}
    
    for idx1, c1 in enumerate(sisD['cell_list']):
        avgCorr_byCell[c1] = {}
        corr_self = []
        corr_sis = []
        corr_stranger = []

        for idx2, c2 in enumerate(sisD['cell_list']):
            g1 = sisD['glom_list'][idx1]
            g2 = sisD['glom_list'][idx2]

            if c1 == c2:
                corr_self = corrM.loc[c1, c2]
            else:
                if g1 == g2:
                    corr_sis.append(corrM.loc[c1, c2])
                else:
                    corr_stranger.append(corrM.loc[c1, c2])
        avgCorr_byCell[c1]['self'] = corr_self
        avgCorr_byCell[c1]['sister'] = np.mean(corr_sis)
        avgCorr_byCell[c1]['stranger'] = np.mean(corr_stranger)
    
    # convert to dataframe
    avgCorr_byCell_df = pd.DataFrame(avgCorr_byCell).T
    return avgCorr_byCell_df


#%% GENERAL -----------------------------------------------------------------------------------
## get x axis in seconds for a trial, for plotting
def get_trial_x_s(info):
    """
    intro: take trial length, Ca data resampling rate and odour onset from idct info, 
        writes an x-axis with unit seconds for plotting
    output:
        x_s: e.g. 4000 datapoints from -3 to 37s for a 40s trial with odour onset at 3s and sampling rate of 1kHz
    """

    # extract variables
    sampRate = info['resampleRate_Hz']
    trialL = info['trialTrim_s'] * sampRate
    baselineL = info['baselineL_trial_s'] * sampRate

    x_preOnset = np.arange(-baselineL, 0)
    x_postOnset = np.arange(0, trialL - baselineL)

    x = np.hstack((x_preOnset, x_postOnset))
    x_s = x/sampRate

    return x_s


## truncate and subsample x40, useful for plotting
def get_trial_x_trunc_subsample(x40, timeStart_s, timeEnd_s, old_sampRate, new_sampRate):
    """
    timeStart_s: time in seconds, start of x40 is 0 (though x40[0] = -3)
    timeEnd_s: time in seconds, end of x40 is 40 (though x40[-1] = -37)
    """
    timestart_dp = int(timeStart_s * old_sampRate)
    timeend_dp = int(timeEnd_s * old_sampRate)

    x40_trunc = x40[timestart_dp:timeend_dp]

    x_trunc_subsample = x40_trunc[::int(old_sampRate / new_sampRate)]

    return x_trunc_subsample