#######################################################################################################################
#######################################################################################################################
# Title: Baseline NILM Architecture
# Topic: Non-intrusive load monitoring utilising machine learning, pattern matching and source separation
# File: main
# Date: 23.10.2021
# Author: Dr. Pascal A. Schirmer
# Version: V.0.0
# Copyright: University of Hertfordshire, Hatfield UK
#######################################################################################################################
#######################################################################################################################


#######################################################################################################################
# Import external libs
#######################################################################################################################
from lib.fnc.loadData import loadData
from lib.train import train
from lib.test import test


#######################################################################################################################
# Function
#######################################################################################################################
def main(setup_Exp, setup_Data, setup_Para, setup_Mdl, basePath, dataPath, mdlPath, resultPath, setup_Feat_One, setup_Feat_Mul):
    ####################################################################################################################
    # Welcome Message
    ####################################################################################################################
    print("-----------------------------------------------------------------------------------------------------------")
    print("-----------------------------------------------------------------------------------------------------------")
    print("Welcome to Base-NILM tool!")
    print("Author:     Dr. Pascal Alexander Schirmer")
    print("Copyright:  University of Hertfordshire")
    print("Date:       23.10.2021 \n \n")
    print("Running NILM tool: Conventional Mode")
    print("Algorithm:       " + str(setup_Para['algorithm']))
    print("Classifier:      " + setup_Para['classifier'])
    print("Dataset:         " + setup_Data['dataset'])
    print("House Train:     " + str(setup_Data['houseTrain']))
    print("House Test:      " + str(setup_Data['houseTest']))
    print("House Val:       " + str(setup_Data['houseVal']))
    print("Configuration:   " + setup_Exp['configuration_name'])
    print("Experiment name: " + setup_Exp['experiment_name'])
    print("Plotting:        " + str(setup_Exp['plotting']))
    print("-----------------------------------------------------------------------------------------------------------")
    print("-----------------------------------------------------------------------------------------------------------")

    ####################################################################################################################
    # Training
    ####################################################################################################################
    if setup_Exp['train'] == 1:
        # ------------------------------------------
        # Load data
        # ------------------------------------------
        [dataTrain, _, dataVal, _, _, _] = loadData(setup_Data, dataPath)

        # ------------------------------------------
        # Train
        # ------------------------------------------
        train(dataTrain, dataVal, setup_Exp, setup_Data, setup_Para, setup_Mdl, setup_Feat_One, setup_Feat_Mul,
              basePath, mdlPath)

    ####################################################################################################################
    # Testing
    ####################################################################################################################
    if setup_Exp['test'] == 1:
        # ------------------------------------------
        # Load data
        # ------------------------------------------
        [_, dataTest, _, _, _, _] = loadData(setup_Data, dataPath)

        # ------------------------------------------
        # Test
        # ------------------------------------------
        [_, _] = test(dataTest, setup_Exp, setup_Data, setup_Para, setup_Feat_One, setup_Feat_Mul, basePath, mdlPath,
                      resultPath)