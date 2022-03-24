#######################################################################################################################
#######################################################################################################################
# Title: Baseline NILM Architecture
# Topic: Non-intrusive load monitoring utilising machine learning, pattern matching and source separation
# File: testMdlPM
# Date: 23.10.2021
# Author: Dr. Pascal A. Schirmer
# Version: V.0.0
# Copyright: Pascal A. Schirmer
#######################################################################################################################
#######################################################################################################################


#######################################################################################################################
# Import external libs
#######################################################################################################################
import os
import numpy as np
from numpy import load
from tslearn import metrics


#######################################################################################################################
# Function
#######################################################################################################################
def testMdlPM(XTest, YTest, setup_Data, setup_Para, setup_Exp, path, mdlPath):
    # ------------------------------------------
    # Load Mdl
    # ------------------------------------------
    mdlName = './mdl_' + setup_Para['classifier'] + '_' + setup_Exp['experiment_name'] + '.npz'
    os.chdir(mdlPath)
    mdl = load(mdlName)
    mdl = mdl['arr_0']
    os.chdir(path)

    # ------------------------------------------
    # Init Variables
    # ------------------------------------------
    YPred = np.zeros((XTest.shape[0], XTest.shape[1], setup_Data['numApp']))
    dist = np.zeros((XTest.shape[0], mdl.shape[0]))

    # ------------------------------------------
    # Find Matching Signatures
    # ------------------------------------------
    for i in range(0, XTest.shape[0]):
        for ii in range(0, mdl.shape[0]):
            dist[i, ii] = metrics.dtw(XTest[i, :], np.squeeze(mdl[ii, :, 0]))
        sel = np.argmin(dist[i, :])
        YPred[i, :, :] = mdl[sel, :, 1:mdl.shape[2]]

    # ------------------------------------------
    # Post-Processing
    # ------------------------------------------
    XPred = np.sum(YPred, axis=2)

    return [XPred, YPred]