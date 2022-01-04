#######################################################################################################################
#######################################################################################################################
# Title: Baseline NILM Architecture
# Topic: Non-intrusive load monitoring utilising machine learning, pattern matching and source separation
# File: start
# Date: 23.11.2021
# Author: Dr. Pascal A. Schirmer
# Version: V.0.0
# Copyright: University of Hertfordshire, Hatfield UK
#######################################################################################################################
#######################################################################################################################


#######################################################################################################################
# Import external libs
#######################################################################################################################
from os.path import dirname, join as pjoin
import os
from main import main
from trans import trans
from kfold import kfold
import warnings


#######################################################################################################################
# Format
#######################################################################################################################
warnings.filterwarnings('ignore')                                                                                        # suppressing all warning

#######################################################################################################################
# Paths
#######################################################################################################################
basePath = pjoin(dirname(os.getcwd()), '02_Base_NILM')
dataPath = pjoin(dirname(os.getcwd()), '02_Base_NILM', 'data')
mdlPath = pjoin(dirname(os.getcwd()), '02_Base_NILM', 'mdl')
libPath = pjoin(dirname(os.getcwd()), '02_Base_NILM', 'lib')
resultPath = pjoin(dirname(os.getcwd()), '02_Base_NILM', 'results')

#######################################################################################################################
# Configuration
#######################################################################################################################

# Experiment
setup_Exp = {'experiment_name': "redd4Def",                                                                              # name of the experiment (name of files that will be saved)
             'author': "Pascal",                                                                                         # name of the person running the experiment
             'configuration_name': "baseNILM",                                                                           # name of the experiment configuration
             'train': 1,                                                                                                 # if 1 training will be performed (if 'experiment_name' exist the mdl will be retrained)
             'test': 1,                                                                                                  # if 1 testing will be performed
             'plotting': 0,                                                                                              # if 1 results will be plotted
             'saveResults': 0}                                                                                           # if 1 results will be saved

# Dataset
setup_Data = {'dataset': "reddTrans",                                                                                         # name of the dataset: 1) redd, 2) ampds, 3) refit, 4)...
              'shape': 2,                                                                                                # if 2 shape is 2-dimensional (Tx[2+M], with T samples and M devices), if 3 shape is 3-dimensional (Tx[2+M]xF, where F is the number of features)
              'granularity': 3,                                                                                          # granularity of the data in Hz
              'downsample': 3,                                                                                           # down-samples the data with a integer value, use 1 for base sample rate
              'houseTrain': [1, 3],                                                                                      # houses used for training, e.g. [1, 3, 4, 5, 6]
              'houseTest': 4,                                                                                            # house used for testing, e.g. 2
              'houseVal': 5,                                                                                             # house used for validation, e.g. 2
              'testRatio': 0.1,                                                                                          # if only one house is used 'testRatio' defines the split of 'houseTrain'
              'kfold': 10,                                                                                                # if 1 'testRatio' is used for data splitting, otherwise k-fold cross validation (tbi)
              'selApp': [],                                                                               # appliances to be evaluated (note first appliance is '0')
              'ghost': 1,                                                                                                # if 0) ghost data will not be used, 1) ghost data will be treated as own appliance, 2) ideal data will be used
              'normData': 2,                                                                                             # normalize data, if 0) none, 1) min-max (in this case meanX/meanY are interpreted as max values), 2) min/max one common value (meanX), 3) mean-std, 4) min/max using train-data
              'meanX': 5000,                                                                                             # normalization value (mean) for the aggregated signal
              'meanY': [500, 200, 700, 400],                                                                             # normalization values (mean) for the appliance signals
              'stdX': 814,                                                                                               # normalization value (std) for the aggregated signal
              'stdY': [800, 400, 1000, 700],                                                                             # normalization values (std) for the aggregated signals
              'neg': 0,                                                                                                  # if 1 negative data will be removed during pre-processing
              'filt': "none",                                                                                            # if 'none' no filtering of data is applied, if 'median' median filtering is applied
              'filt_len': 21}                                                                                            # length of the filter (must be an odd number)

# Architecture Parameters
setup_Para = {'algorithm': 1,                                                                                            # if 0 classification is used, if 1 regression is used
              'classifier': "CNN",                                                                                       # possible classifier: 1) ML: RF, CNN, LSTM \ 2) PM: DTW, MVM \ 3) SS: NMF, SCA
              'trans': 0,                                                                                                # if 1 transfer learning is applied, e.g. 'houseTrain' are used for training and 'houseTest' and 'houseVal' for testing and validation respectively
              'framelength': 10,                                                                                         # frame-length of the time-frames
              'overlap': 9,                                                                                              # overlap between two consecutive time frames
              'p_Threshold': 50,                                                                                         # threshold for binary distinction of On/Off states
              'multiClass': 1,                                                                                           # if 0 one model per appliance is used, if 1 one model for all appliances is used
              'seq2seq': 0,                                                                                              # if 0) seq2point is used, if 1) seq2seq is used (only if multiClass=0 and overlap=0)
              'feat': 0}                                                                                                 # if 0) raw values are used, if 1) 1D features are calculated, if 2) 2D feature are calculated (only for shape 3 data)

# Mdl Parameters
setup_Mdl = {'batch_size': 1000,                                                                                         # batch size for DNN based approaches
             'epochs': 50,                                                                                               # number of epochs for training
             'valsteps': 50,                                                                                             # number of validation steps
             'shuffle': "False",                                                                                         # either True or False for shuffling data
             'verbose': 2,                                                                                               # settings for displaying mdl progress
             'n_neighbors': 5,                                                                                           # number of nearest neighbors for KNN
             'max_depth': 10,                                                                                            # maximum depth for RF
             'random_state': 0,                                                                                          # random state parameter for RF
             'n_estimators': 32,                                                                                         # number of estimators for RF
             'kernel': "rbf",                                                                                            # kernel for SVM
             'C': 100,                                                                                                   # regularization parameter SVM
             'epsilon': 0.1,                                                                                             # epsilon parameter SVM
             'gamma': 0.1}                                                                                               # scale parameter SVM

#######################################################################################################################
# Select Features
#######################################################################################################################
# One-Dimensional Features (sel multiple)
setup_Feat_One = {'Mean':      1,                                                                                        # Mean value of the frame
                  'Std':       1,                                                                                        # standard deviation of the frame
                  'RMS':       1,                                                                                        # rms value of the frame
                  'Peak2Rms':  1,                                                                                        # peak-to-RMS value of the frame
                  'Median':    1,                                                                                        # median value of the frame
                  'MIN':       1,                                                                                        # minimum value of the frame
                  'MAX':       1,                                                                                        # maximum value of the frame
                  'Per25':     1,                                                                                        # 25 percentile of the frame
                  'Per75':     1,                                                                                        # 75 percentile of the frame
                  'Energy':    1,                                                                                        # energy in the frame
                  'Var':       1,                                                                                        # variance of the frame
                  'Range':     1,                                                                                        # range of values in the frame
                  '3rdMoment': 0,                                                                                        # 3rd statistical moment of the frame
                  '4thMoment': 0,                                                                                        # 4th statistical moment of the frame
                  'Diff':      0,                                                                                        # first derivative
                  'DiffDiff':  0}                                                                                        # second derivative

# Multi-Dimensional Features (select one)
setup_Feat_Mul = {'FFT': 0,                                                                                              # if 1) using amplitudes, 2) using phase angles, 3) use both (concatenated same dimension) 4) use both (concatenated new dimension)
                  'PQ': 2}                                                                                               # if 1) raw values, 2) FFT amplitudes, 3) FFT phases (only for shape 3 data with P/Q as features)

#######################################################################################################################
# Non Transfer
#######################################################################################################################
if setup_Para['trans'] == 0 and setup_Data['kfold'] <= 1:
    main(setup_Exp, setup_Data, setup_Para, setup_Mdl, basePath, dataPath, mdlPath, resultPath, setup_Feat_One,
         setup_Feat_Mul)
else:
    kfold(setup_Exp, setup_Data, setup_Para, setup_Mdl, basePath, dataPath, mdlPath, resultPath, setup_Feat_One,
          setup_Feat_Mul)

#######################################################################################################################
# Transfer
#######################################################################################################################
if setup_Para['trans'] == 1:
    trans(setup_Exp, setup_Data, setup_Para, setup_Mdl, basePath, dataPath, mdlPath, resultPath, setup_Feat_One,
          setup_Feat_Mul)