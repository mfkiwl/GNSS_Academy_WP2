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
from InputOutput import CorrIdx
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

    PlotConf["Path"] = sys.argv[1] + '/CORR/figures/' + \
        '%s_%s_Y%sD%s.png' % (Label, Rcvr, Year, Doy)


# Function to convert 'G01', 'G02', etc. to 1, 2, etc.
def convert_satlabel_to_prn(value):
    return int(value[1:])


# Function to convert 'G01', 'G02', etc. to 'G'
def convert_satlabel_to_const(value):
    return value[0]


# Plot Satellite Tracks
def plotSatTracks(PreproObsFile, CorrData):
    # Use the Map
    pass



# Plot Flight Time
def plotFlightTime(PreproObsFile, CorrData):
    PlotConf = {}

    GPS_Data = CorrData[CorrData[CorrIdx["CONST"]] == 'G']
    GPS_Data = GPS_Data[GPS_Data[CorrIdx["FLAG"]] == 1]
    Galileo_Data = CorrData[CorrData[CorrIdx["CONST"]] == 'E']
    Galileo_Data = Galileo_Data[Galileo_Data[CorrIdx["FLAG"]] == 1]


    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (8.4,6.6)
    PlotConf["Title"] = "GPS Satellite Flight Time"

    PlotConf["yLabel"] = "Flight Time [miliseconds] "
    # PlotConf["yLim"] = [-1.6, 1.6]

    PlotConf["xLabel"] = "Hour of DoY 011"
    PlotConf["xTicks"] = range(0, 25)
    PlotConf["xLim"] = [0, 24]

    PlotConf["Grid"] = 1

    PlotConf["Marker"] = '.'
    PlotConf["MarkerSize"] = 1
    PlotConf["LineWidth"] = 1

    PlotConf["ColorBar"] = "gnuplot"
    PlotConf["ColorBarLabel"] = "Elevation [deg]"
    PlotConf["ColorBarMin"] = 0.
    PlotConf["ColorBarMax"] = 90.

    PlotConf["xData"] = {}
    PlotConf["yData"] = {}
    PlotConf["zData"] = {}

    for prn in sorted(unique(GPS_Data[CorrIdx["PRN"]])):

        FilterCond = GPS_Data[CorrIdx["PRN"]] == prn
        PlotConf["xData"][prn] = GPS_Data[CorrIdx["SOD"]][FilterCond] / GnssConstants.S_IN_H
        PlotConf["yData"][prn] = GPS_Data[CorrIdx["FLIGHT-TIME"]][FilterCond]
        PlotConf["zData"][prn] = GPS_Data[CorrIdx["ELEV"]][FilterCond]

    PlotConf["Path"] = sys.argv[1] + '/OUT/CORR/FIGURES/' + 'GPS_FLIGHT_TIME_D011Y24.png'

    generatePlot(PlotConf)

    # ----------------------------------------------------------------------------------------------


    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (8.4,6.6)
    PlotConf["Title"] = "Galileo Satellite Flight Time"

    PlotConf["yLabel"] = "Flight Time [miliseconds] "
    # PlotConf["yLim"] = [-1.6, 1.6]

    PlotConf["xLabel"] = "Hour of DoY 011"
    PlotConf["xTicks"] = range(0, 25)
    PlotConf["xLim"] = [0, 24]

    PlotConf["Grid"] = 1

    PlotConf["Marker"] = '.'
    PlotConf["MarkerSize"] = 1
    PlotConf["LineWidth"] = 1

    PlotConf["ColorBar"] = "gnuplot"
    PlotConf["ColorBarLabel"] = "Elevation [deg]"
    PlotConf["ColorBarMin"] = 0.
    PlotConf["ColorBarMax"] = 90.

    PlotConf["xData"] = {}
    PlotConf["yData"] = {}
    PlotConf["zData"] = {}

    for prn in sorted(unique(Galileo_Data[CorrIdx["PRN"]])):

        FilterCond = Galileo_Data[CorrIdx["PRN"]] == prn
        PlotConf["xData"][prn] = Galileo_Data[CorrIdx["SOD"]][FilterCond] / GnssConstants.S_IN_H
        PlotConf["yData"][prn] = Galileo_Data[CorrIdx["FLIGHT-TIME"]][FilterCond]
        PlotConf["zData"][prn] = Galileo_Data[CorrIdx["ELEV"]][FilterCond]

    PlotConf["Path"] = sys.argv[1] + '/OUT/CORR/FIGURES/' + 'Galileo_FLIGHT_TIME_D011Y24.png'

    generatePlot(PlotConf)

# Plot DTR
def plotDTR(PreproObsFile, CorrData):
    PlotConf = {}

    GPS_Data = CorrData[CorrData[CorrIdx["CONST"]] == 'G']
    GPS_Data = GPS_Data[GPS_Data[CorrIdx["FLAG"]] == 1]
    Galileo_Data = CorrData[CorrData[CorrIdx["CONST"]] == 'E']
    Galileo_Data = Galileo_Data[Galileo_Data[CorrIdx["FLAG"]] == 1]


    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (8.4,6.6)
    PlotConf["Title"] = "GPS Relativistic Correction (Dtr)"

    PlotConf["yLabel"] = "Relativistic Correction (Dtr) [m] "
    # PlotConf["yLim"] = [-1.6, 1.6]

    PlotConf["xLabel"] = "Hour of DoY 011"
    PlotConf["xTicks"] = range(0, 25)
    PlotConf["xLim"] = [0, 24]

    PlotConf["Grid"] = 1

    PlotConf["Marker"] = '.'
    PlotConf["MarkerSize"] = 1
    PlotConf["LineWidth"] = 1

    PlotConf["ColorBar"] = "gnuplot"
    PlotConf["ColorBarLabel"] = "Elevation [deg]"
    PlotConf["ColorBarMin"] = 0.
    PlotConf["ColorBarMax"] = 90.

    PlotConf["xData"] = {}
    PlotConf["yData"] = {}
    PlotConf["zData"] = {}

    for prn in sorted(unique(GPS_Data[CorrIdx["PRN"]])):

        FilterCond = GPS_Data[CorrIdx["PRN"]] == prn
        PlotConf["xData"][prn] = GPS_Data[CorrIdx["SOD"]][FilterCond] / GnssConstants.S_IN_H
        PlotConf["yData"][prn] = GPS_Data[CorrIdx["DTR"]][FilterCond]
        PlotConf["zData"][prn] = GPS_Data[CorrIdx["ELEV"]][FilterCond]

    PlotConf["Path"] = sys.argv[1] + '/OUT/CORR/FIGURES/' + 'GPS_DTR_D011Y24.png'

    generatePlot(PlotConf)

    # ----------------------------------------------------------------------------------------------


    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (8.4,6.6)
    PlotConf["Title"] = "Galileo Relativistic Correction (Dtr)"

    PlotConf["yLabel"] = "Relativistic Correction (Dtr) [m]"
    # PlotConf["yLim"] = [-1.6, 1.6]

    PlotConf["xLabel"] = "Hour of DoY 011"
    PlotConf["xTicks"] = range(0, 25)
    PlotConf["xLim"] = [0, 24]

    PlotConf["Grid"] = 1

    PlotConf["Marker"] = '.'
    PlotConf["MarkerSize"] = 1
    PlotConf["LineWidth"] = 1

    PlotConf["ColorBar"] = "gnuplot"
    PlotConf["ColorBarLabel"] = "Elevation [deg]"
    PlotConf["ColorBarMin"] = 0.
    PlotConf["ColorBarMax"] = 90.

    PlotConf["xData"] = {}
    PlotConf["yData"] = {}
    PlotConf["zData"] = {}

    for prn in sorted(unique(Galileo_Data[CorrIdx["PRN"]])):

        FilterCond = Galileo_Data[CorrIdx["PRN"]] == prn
        PlotConf["xData"][prn] = Galileo_Data[CorrIdx["SOD"]][FilterCond] / GnssConstants.S_IN_H
        PlotConf["yData"][prn] = Galileo_Data[CorrIdx["DTR"]][FilterCond]
        PlotConf["zData"][prn] = Galileo_Data[CorrIdx["ELEV"]][FilterCond]

    PlotConf["Path"] = sys.argv[1] + '/OUT/CORR/FIGURES/' + 'Galileo_DTR_D011Y24.png'

    generatePlot(PlotConf)





# Plot Code Residuals
def plotResidualsCode(PreproObsFile, CorrData):
    PlotConf = {}

    GPS_Data = CorrData[CorrData[CorrIdx["CONST"]] == 'G']
    GPS_Data = GPS_Data[GPS_Data[CorrIdx["FLAG"]] == 1]
    Galileo_Data = CorrData[CorrData[CorrIdx["CONST"]] == 'E']
    Galileo_Data = Galileo_Data[Galileo_Data[CorrIdx["FLAG"]] == 1]


    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (8.4,6.6)
    PlotConf["Title"] = "GPS Code Residuals"

    PlotConf["yLabel"] = "Code Residuals [m]"
    # PlotConf["yLim"] = [-1.6, 1.6]

    PlotConf["xLabel"] = "Hour of DoY 011"
    PlotConf["xTicks"] = range(0, 25)
    PlotConf["xLim"] = [0, 24]

    PlotConf["Grid"] = 1

    PlotConf["Marker"] = '.'
    PlotConf["MarkerSize"] = 1
    PlotConf["LineWidth"] = 1

    PlotConf["ColorBar"] = "gnuplot"
    PlotConf["ColorBarLabel"] = "PRN"
    PlotConf["ColorBarMin"] = 0.
    PlotConf["ColorBarMax"] = 36.

    PlotConf["xData"] = {}
    PlotConf["yData"] = {}
    PlotConf["zData"] = {}

    for prn in sorted(unique(GPS_Data[CorrIdx["PRN"]])):

        FilterCond = GPS_Data[CorrIdx["PRN"]] == prn
        PlotConf["xData"][prn] = GPS_Data[CorrIdx["SOD"]][FilterCond] / GnssConstants.S_IN_H
        PlotConf["yData"][prn] = GPS_Data[CorrIdx["CODE-RES"]][FilterCond]
        PlotConf["zData"][prn] = GPS_Data[CorrIdx["PRN"]][FilterCond]

    PlotConf["Path"] = sys.argv[1] + '/OUT/CORR/FIGURES/' + 'GPS_Code_Residuals_D011Y24.png'

    generatePlot(PlotConf)

    # ----------------------------------------------------------------------------------------------


    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (8.4,6.6)
    PlotConf["Title"] = "Galileo Code Residuals"

    PlotConf["yLabel"] = "Code Residuals [m]"
    # PlotConf["yLim"] = [-1.6, 1.6]

    PlotConf["xLabel"] = "Hour of DoY 011"
    PlotConf["xTicks"] = range(0, 25)
    PlotConf["xLim"] = [0, 24]

    PlotConf["Grid"] = 1

    PlotConf["Marker"] = '.'
    PlotConf["MarkerSize"] = 1
    PlotConf["LineWidth"] = 1

    PlotConf["ColorBar"] = "gnuplot"
    PlotConf["ColorBarLabel"] = "PRN"
    PlotConf["ColorBarMin"] = 0.
    PlotConf["ColorBarMax"] = 36.

    PlotConf["xData"] = {}
    PlotConf["yData"] = {}
    PlotConf["zData"] = {}

    for prn in sorted(unique(Galileo_Data[CorrIdx["PRN"]])):

        FilterCond = Galileo_Data[CorrIdx["PRN"]] == prn
        PlotConf["xData"][prn] = Galileo_Data[CorrIdx["SOD"]][FilterCond] / GnssConstants.S_IN_H
        PlotConf["yData"][prn] = Galileo_Data[CorrIdx["CODE-RES"]][FilterCond]
        PlotConf["zData"][prn] = Galileo_Data[CorrIdx["PRN"]][FilterCond]

    PlotConf["Path"] = sys.argv[1] + '/OUT/CORR/FIGURES/' + 'Galileo_Code_Residuals_D011Y24.png'

    generatePlot(PlotConf)



# Plot Phase Residuals
def plotResidualsPhase(PreproObsFile, CorrData):
    PlotConf = {}

    GPS_Data = CorrData[CorrData[CorrIdx["CONST"]] == 'G']
    GPS_Data = GPS_Data[GPS_Data[CorrIdx["FLAG"]] == 1]
    Galileo_Data = CorrData[CorrData[CorrIdx["CONST"]] == 'E']
    Galileo_Data = Galileo_Data[Galileo_Data[CorrIdx["FLAG"]] == 1]


    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (8.4,6.6)
    PlotConf["Title"] = "GPS Phase Residuals"

    PlotConf["yLabel"] = "Phase Residuals [m]"
    # PlotConf["yLim"] = [-1.6, 1.6]

    PlotConf["xLabel"] = "Hour of DoY 011"
    PlotConf["xTicks"] = range(0, 25)
    PlotConf["xLim"] = [0, 24]

    PlotConf["Grid"] = 1

    PlotConf["Marker"] = '.'
    PlotConf["MarkerSize"] = 1
    PlotConf["LineWidth"] = 1

    PlotConf["ColorBar"] = "gnuplot"
    PlotConf["ColorBarLabel"] = "PRN"
    PlotConf["ColorBarMin"] = 0.
    PlotConf["ColorBarMax"] = 36.

    PlotConf["xData"] = {}
    PlotConf["yData"] = {}
    PlotConf["zData"] = {}

    for prn in sorted(unique(GPS_Data[CorrIdx["PRN"]])):

        FilterCond = GPS_Data[CorrIdx["PRN"]] == prn
        PlotConf["xData"][prn] = GPS_Data[CorrIdx["SOD"]][FilterCond] / GnssConstants.S_IN_H
        PlotConf["yData"][prn] = GPS_Data[CorrIdx["PHASE-RES"]][FilterCond]
        PlotConf["zData"][prn] = GPS_Data[CorrIdx["PRN"]][FilterCond]

    PlotConf["Path"] = sys.argv[1] + '/OUT/CORR/FIGURES/' + 'GPS_Phase_Residuals_D011Y24.png'

    generatePlot(PlotConf)

    # ----------------------------------------------------------------------------------------------


    PlotConf["Type"] = "Lines"
    PlotConf["FigSize"] = (8.4,6.6)
    PlotConf["Title"] = "Galileo Phase Residuals"

    PlotConf["yLabel"] = "Phase Residuals [m]"
    # PlotConf["yLim"] = [-1.6, 1.6]

    PlotConf["xLabel"] = "Hour of DoY 011"
    PlotConf["xTicks"] = range(0, 25)
    PlotConf["xLim"] = [0, 24]

    PlotConf["Grid"] = 1

    PlotConf["Marker"] = '.'
    PlotConf["MarkerSize"] = 1
    PlotConf["LineWidth"] = 1

    PlotConf["ColorBar"] = "gnuplot"
    PlotConf["ColorBarLabel"] = "PRN"
    PlotConf["ColorBarMin"] = 0.
    PlotConf["ColorBarMax"] = 36.

    PlotConf["xData"] = {}
    PlotConf["yData"] = {}
    PlotConf["zData"] = {}

    for prn in sorted(unique(Galileo_Data[CorrIdx["PRN"]])):

        FilterCond = Galileo_Data[CorrIdx["PRN"]] == prn
        PlotConf["xData"][prn] = Galileo_Data[CorrIdx["SOD"]][FilterCond] / GnssConstants.S_IN_H
        PlotConf["yData"][prn] = Galileo_Data[CorrIdx["PHASE-RES"]][FilterCond]
        PlotConf["zData"][prn] = Galileo_Data[CorrIdx["PRN"]][FilterCond]

    PlotConf["Path"] = sys.argv[1] + '/OUT/CORR/FIGURES/' + 'Galileo_Phase_Residuals_D011Y24.png'

    generatePlot(PlotConf)




# Plot Receiver Clock
def plotReceiverClock(PreproObsFile, CorrData):
    pass




def generateCorrPlots(PreproObsFile):
    
    # Purpose: generate output plots regarding Correction results

    # Satellite Tracks
    # ----------------------------------------------------------
    # Read the cols we need from PREPRO OBS file
    CorrData = read_csv(PreproObsFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[CorrIdx["SAT-X"],CorrIdx["SAT-X"],CorrIdx["CONST"],CorrIdx["PRN"],CorrIdx["FLAG"],CorrIdx["ELEV"]])
    
    print('INFO: Plot Satellite Tracks ...')

    # Configure plot and call plot generation function
    plotSatTracks(PreproObsFile, CorrData)

    # Flight Time
    # ----------------------------------------------------------
    # Read the cols we need from PREPRO OBS file
    CorrData = read_csv(PreproObsFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[CorrIdx["SOD"],CorrIdx["CONST"],CorrIdx["PRN"],CorrIdx["FLAG"],CorrIdx["FLIGHT-TIME"], CorrIdx["ELEV"]])
    
    print('INFO: Plot Flight Time...')

    # Configure plot and call plot generation function
    plotFlightTime(PreproObsFile, CorrData)


    # DTR (Relativistic Effect)
    # ----------------------------------------------------------
    # Read the cols we need from PREPRO OBS file
    CorrData = read_csv(PreproObsFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[CorrIdx["SOD"],CorrIdx["CONST"],CorrIdx["PRN"],CorrIdx["FLAG"],CorrIdx["DTR"], CorrIdx["ELEV"]])
    
    print('INFO: Plot DTR...')

    # Configure plot and call plot generation function
    plotDTR(PreproObsFile, CorrData)


    # Code Residuals
    # ----------------------------------------------------------
    # Read the cols we need from PREPRO OBS file
    CorrData = read_csv(PreproObsFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[CorrIdx["SOD"],CorrIdx["CONST"],CorrIdx["PRN"],CorrIdx["FLAG"],CorrIdx["CODE-RES"]])
    
    print('INFO: Plot Code Residuals...')

    # Configure plot and call plot generation function
    plotResidualsCode(PreproObsFile, CorrData)


    # Phase Residuals
    # ----------------------------------------------------------
    # Read the cols we need from PREPRO OBS file
    CorrData = read_csv(PreproObsFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[CorrIdx["SOD"],CorrIdx["CONST"],CorrIdx["PRN"],CorrIdx["FLAG"],CorrIdx["PHASE-RES"]])
    
    print('INFO: Plot Phase Residuals...')

    # Configure plot and call plot generation function
    plotResidualsPhase(PreproObsFile, CorrData)


    # Clock Receiver
    # ----------------------------------------------------------
    # Read the cols we need from PREPRO OBS file
    CorrData = read_csv(PreproObsFile, delim_whitespace=True, skiprows=1, header=None,\
    usecols=[CorrIdx["SOD"],CorrIdx["CONST"],CorrIdx["PRN"],CorrIdx["RCVR-CLK"]])
    
    print('INFO: Plot Receiver Clock...')

    # Configure plot and call plot generation function
    plotReceiverClock(PreproObsFile, CorrData)