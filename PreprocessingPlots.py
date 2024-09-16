#!/usr/bin/env python

########################################################################
# PreprocessingPlots.py:
# This is the PreprocessingPlots Module of SENTUS tool
#
#  Project:        SENTUS
#  File:           PreprocessingPlots.py
#
#   Author: GNSS Academy
#   Copyright 2024 GNSS Academy
#
# -----------------------------------------------------------------
# Date       | Author             | Action
# -----------------------------------------------------------------
#
########################################################################

import sys, os
from pandas import unique
from pandas import read_csv
from InputOutput import PreproIdx
from InputOutput import REJECTION_CAUSE_DESC
sys.path.append(os.getcwd() + '/' + \
    os.path.dirname(sys.argv[0]) + '/' + 'COMMON')
from COMMON import GnssConstants
import numpy as np
from collections import OrderedDict

from COMMON.Plots import generatePlot
import matplotlib.pyplot as plt


def initPlot(PreproObsFile, PlotConf, Title, Label):
    PreproObsFileName = os.path.basename(PreproObsFile)
    PreproObsFileNameSplit = PreproObsFileName.split('_')
    Rcvr = PreproObsFileNameSplit[2]
    DatepDat = PreproObsFileNameSplit[3]
    Date = DatepDat.split('.')[0]
    Year = Date[1:3]
    Doy = Date[4:]

    PlotConf["xLabel"] = "Hour of Day %s" % Doy

    PlotConf["Title"] = "%s from %s on Year %s"\
        " DoY %s" % (Title, Rcvr, Year, Doy)

    PlotConf["Path"] = sys.argv[1] + '/OUT/PPVE/figures/' + \
        '%s_%s_Y%sD%s.png' % (Label, Rcvr, Year, Doy)


# Function to convert 'G01', 'G02', etc. to 1, 2, etc.
def convert_satlabel_to_prn(value):
    return int(value[1:])


# Function to convert 'G01', 'G02', etc. to 'G'
def convert_satlabel_to_const(value):
    return value[0]


# Plot Satellite Tracks
def plotSatTracks(PreproObsFile, PreproObsData):
    # Use the Map
    pass



# Plot Flight Time
def plotFlightTime(PreproObsFile, PreproObsData):
    pass



# Plot DTR
def plotDTR(PreproObsFile, PreproObsData):
    pass




# Plot Code Residuals
def plotResidualsCode(PreproObsFile, PreproObsData):
    pass



# Plot Phase Residuals
def plotResidualsPhase(PreproObsFile, PreproObsData):
    pass




# Plot Receiver Clock
def plotReceiverClock(PreproObsFile, PreproObsData):
    pass




def generatePreproPlots(PreproObsFile):
    
    # Purpose: generate output plots regarding Correction results

    # Satellite Tracks
    # ----------------------------------------------------------
    # Read the cols we need from PREPRO OBS file
    PreproObsData = read_csv(PreproObsFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[PreproIdx["SAT-X"],PreproIdx["SAT-X"],PreproIdx["CONST"],PreproIdx["FLAG"],PreproIdx["ELEV"]])
    
    print('INFO: Plot Satellite Tracks ...')

    # Configure plot and call plot generation function
    plotSatTracks(PreproObsFile, PreproObsData)

    # Flight Time
    # ----------------------------------------------------------
    # Read the cols we need from PREPRO OBS file
    PreproObsData = read_csv(PreproObsFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[PreproIdx["SOD"],PreproIdx["CONST"],PreproIdx["TOF"], PreproIdx["ELEV"]])
    
    print('INFO: Plot Flight Time...')

    # Configure plot and call plot generation function
    plotFlightTime(PreproObsFile, PreproObsData)


    # DTR (Relativistic Effect)
    # ----------------------------------------------------------
    # Read the cols we need from PREPRO OBS file
    PreproObsData = read_csv(PreproObsFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[PreproIdx["SOD"],PreproIdx["CONST"],PreproIdx["DTR"], PreproIdx["ELEV"]])
    
    print('INFO: Plot DTR...')

    # Configure plot and call plot generation function
    plotDTR(PreproObsFile, PreproObsData)


    # Code Residuals
    # ----------------------------------------------------------
    # Read the cols we need from PREPRO OBS file
    PreproObsData = read_csv(PreproObsFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[PreproIdx["SOD"],PreproIdx["CONST"],PreproIdx["CODE-RES"], PreproIdx["ELEV"]])
    
    print('INFO: Plot Code Residuals...')

    # Configure plot and call plot generation function
    plotResidualsCode(PreproObsFile, PreproObsData)


    # Phase Residuals
    # ----------------------------------------------------------
    # Read the cols we need from PREPRO OBS file
    PreproObsData = read_csv(PreproObsFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[PreproIdx["SOD"],PreproIdx["CONST"],PreproIdx["PHASE-RES"], PreproIdx["ELEV"]])
    
    print('INFO: Plot Phase Residuals...')

    # Configure plot and call plot generation function
    plotResidualsPhase(PreproObsFile, PreproObsData)


    # Clock Receiver
    # ----------------------------------------------------------
    # Read the cols we need from PREPRO OBS file
    PreproObsData = read_csv(PreproObsFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[PreproIdx["SOD"],PreproIdx["CONST"],PreproIdx["RCVR-CLK"]])
    
    print('INFO: Plot Receiver Clock...')

    # Configure plot and call plot generation function
    plotReceiverClock(PreproObsFile, PreproObsData)