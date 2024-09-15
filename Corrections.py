#!/usr/bin/env python

########################################################################
# PETRUS/SRC/Corrections.py:
# This is the Corrections Module of SENTUS tool
#
#  Project:        SENTUS
#  File:           Corrections.py
#  Date(YY/MM/DD): 14/07/24
#
#   Author: GNSS Academy
#   Copyright 2024 GNSS Academy
#
# -----------------------------------------------------------------
# Date       | Author             | Action
# -----------------------------------------------------------------
#
########################################################################

# Import External and Internal functions and Libraries
#----------------------------------------------------------------------
import sys, os
# Add path to find all modules
Common = os.path.dirname(os.path.dirname(
    os.path.abspath(sys.argv[0]))) + '/COMMON'
sys.path.insert(0, Common)
from collections import OrderedDict
from COMMON import GnssConstants as Const
from COMMON.Misc import findSun, crossProd
import numpy as np


from Correction_functions import computeLeoComPos, computeSatClkBias, computeRcvrApo, getUERE
from COMMON.Misc import findSun
from InputOutput import LeoPosIdx

STATUS_OK = 1

def runCorrectMeas(Year,
                    Doy,
                    Conf, 
                    PreproObsInfo, 
                    LeoPosInfo,
                    LeoQuatInfo,
                    SatPosInfo, 
                    SatApoInfo,
                    SatClkInfo,
                    SatBiaInfo,
                    # SatComPos_1,
                    # Sod_1
                    ):

    # Purpose: correct GNSS preprocessed measurements and compute the first
    #          pseudo range residuals

    #          More in detail, this function handles the following:
    #          tasks:

    #             *  Compute the Satellite Antenna Phase Center position at the transmission time and corrected from the Sagnac
    #                effect interpolating the SP3 file positions
    #             *  Compute the Satellite Clock Bias interpolating the biases coming from the RINEX CLK file and
    #                applying the Relativistic Correction (DTR)
    #             *  Correct the Pre-processed measurements from Geometrical Range, Satellite clock and Troposphere. 
    #             *  Build the Corrected Measurements and Measurement Residuals
    #             *  Build the Sigma UERE


    # Parameters
    # ==========
    # Conf: dict
    #         Configuration dictionary
    # Rcvr: list
    #         Receiver information: position, masking angle...
    # ObsInfo: list
    #         OBS info for current epoch
    #         ObsInfo[1][1] is the second field of the 
    #         second satellite
    # PreproObsInfo: dict
    #         Preprocessed observations for current epoch per sat
    #         PreproObsInfo["G01"]["C1"]
    # LeoPosInfo: dict
    #         containing the LEO reference positions
    # LeoQuatInfo: dict
    #         containing the LEO quaternions
    # SatPosInfo: dict
    #         containing the SP3 file info
    # SatApoInfo: dict
    #         containing the ANTEX file info
    # SatClkInfo: dict
    #         containing the RINEX CLK file info
    # SatBiaInfo: dict
    #         containing the BIA file info
    # SatComPos_1: dict
    #         containing the previous satellite positions
    # Sod_1: dict
    #         containing the time stamp of previous satellite positions

    # Returns
    # =======
    # CorrInfo: dict
    #         Corrected measurements for current epoch per sat
    #         CorrInfo["G01"]["CorrectedPsr"]

    # Initialize output
    CorrInfo = OrderedDict({})
    RcvrRefPosXyz = np.zeros(3)
    RcvrRefPosLlh = np.zeros(3)

    # Loop over satellites
    for SatLabel, SatPrepro in PreproObsInfo.items():
        # Get constellation
        Constel = SatLabel[0]
        
        Wave = {}
        # Get wavelengths
        if Constel == 'G':

            # L1 wavelength
            Wave["F1"] = Const.GPS_L1_WAVE

            # L2 wavelength
            Wave["F2"] = Const.GPS_L2_WAVE

            # Gamma GPS
            GammaF1F2 = Const.GPS_GAMMA_L1L2

        elif Constel == 'E':

            # E1 wavelength
            Wave["F1"] = Const.GAL_E1_WAVE

            # E5a wavelength
            Wave["F2"] = Const.GAL_E5A_WAVE

            # Gamma Galileo
            GammaF1F2 = Const.GAL_GAMMA_E1E5A

        # Initialize output info
        SatCorrInfo = {
            "Sod": 0.0,             # Second of day
            "Doy": 0,               # Day of year
            "Elevation": 0.0,       # Elevation
            "Azimuth": 0.0,         # Azimuth
            "Flag": 1,              # 0: Not Used 1: Used
            "LeoX": 0.0,            # X-Component of the Receiver CoP Position --> CoP (Center of Phases)
            "LeoY": 0.0,            # Y-Component of the Receiver CoP Position  
            "LeoZ": 0.0,            # Z-Component of the Receiver CoP Position  
            "LeoApoX": 0.0,         # X-Component of the Receiver APO in ECEF  --> APO (Antenna Phase Offset)
            "LeoApoY": 0.0,         # Y-Component of the Receiver APO in ECEF
            "LeoApoZ": 0.0,         # Z-Component of the Receiver APO in ECEF
            "SatX": 0.0,            # X-Component of the Satellite CoP Position 
                                    # at transmission time and corrected from Sagnac
            "SatY": 0.0,            # Y-Component of the Satellite CoP Position  
                                    # at transmission time and corrected from Sagnac
            "SatZ": 0.0,            # Z-Component of the Satellite CoP Position  
                                    # at transmission time and corrected from Sagnac
            "SatApoX": 0.0,         # X-Component of the Satellite APO in ECEF
            "SatApoY": 0.0,         # Y-Component of the Satellite APO in ECEF
            "SatApoZ": 0.0,         # Z-Component of the Satellite APO in ECEF
            "ApoProj": 0.0,         # Projection of the Satellite APO
            "SatClk": 0.0,          # Satellite Clock Bias
            "SatCodeBia": 0.0,      # Satellite Code Bias
            "SatPhaseBia": 0.0,     # Satellite Phase Bias
            "FlightTime": 0.0,      # Signal Flight Time
            "Dtr": 0.0,             # Relativistic correction
            "CorrCode": 0.0,        # Code corrected from delays
            "CorrPhase": 0.0,       # Phase corrected from delays
            "GeomRange": 0.0,       # Geometrical Range (distance between Satellite 
                                    # Position and Receiver Reference Position)
            "CodeResidual": 0.0,    # Code Residual
            "PhaseResidual": 0.0,   # Phase Residual
            "RcvrClk": 0.0,         # Receiver Clock estimation
            "SigmaUere": 0.0,       # Sigma User Equivalent Range Error (Sigma of 
                                    # the total residual error associated to the 
                                    # satellite)

        } # End of SatCorrInfo

    # ----------------------------------------------------------------------------------------------------------------------------

        Sod = SatPrepro["Sod"]
        SatCorrInfo["Doy"] = LeoPosInfo[LeoPosIdx["DOY"]]
        SatCorrInfo["Year"] = LeoPosInfo[LeoPosIdx["YEAR"]]

        RcvrRefPosXyzCom = computeLeoComPos(Sod, LeoPosInfo)    # Compute the Center of Masses (CoM)

        if SatPrepro["Status"] == STATUS_OK:

            SatClkBias = computeSatClkBias(Sod, SatLabel, SatClkInfo)     # Compute Satellite Clock Bias (Linear interpolation between closer inputs) 

            DeltaT = SatPrepro["C1"]/Const.SPEED_OF_LIGHT

            TransmissionTime = Sod - DeltaT - SatClkBias        # Compute Transmission Time

        #     RcvrPosXyz = computeRcvrApo(Conf, Year, Doy, Sod, SatLabel, LeoQuatInfo)



        #     RcvrRefPosXyz = RcvrRefPosXyzCom + RcvrPosXyz

        #     SatComPos = computeSatComPos(TransmissionTime, SatPosInfo)      # Compute Satellite Center of Masses Position at Tranmission Time, 10-point Langrange interpolation between closer inputs (SP3 positions)

        #     FlightTime = np.linalg.norm(SatComPos - RcvrPos) / Const.SPEED_OF_LIGHT    # Compute Flight Time

        #     SatComPos = applySagnac(SatComPos, FlightTime)                  # Apply Sagnac correction

        SubPos = findSun(SatCorrInfo["Year"], SatCorrInfo["Doy"], Sod)

        #     Apo = computeSatApo(SatLabel, SatComPos, RcvrPos, SunPos, SatApoInfo)   # Compute Antenna Phase Offset in ECEF from ANTEX APOs in satellite-body reference frame

        #     SatCopPos = SatComPos + Apo         # Apply APOs to the Satellite Position

        #     SatelliteBiases = getSatBias(GammaF1F2, SatLabel, SatBiaInfo)   #Get SAtellite Biases in meters

        #     Dtr = computeDtr(SatComPos_1, SatComPos, Sod, Sod_1)            # Compute relativistic correction

        #     SatClkBias += Dtr                   # Apply Dtr to Clock Bias

        SigmaUERE = getUERE(Conf, SatLabel)         # Get Sigma UERE from Conf


        #     CorrCode = SatPrepro["IF_C"] + SatClk + CodeSatBias         # Corrected measurements from previous information
        #     CorrPhase = SatPrepro["IF_P"] + SatClk + PhaseSatBias       # In the statement is miswritten (IF_L)

        #     GeomRange = computeGeoRange(SatCopPos, RcvrPos)             # COmpute Geometrical Range

        #     CodeResidual = CorrCode - GeomRange                         # Comute the first Residual removing the geometrical range (They include Recevier Clock Estimation)
        #     PhaseResidual = CorrPhase - GeomRange

        # RcvrClk = estimateRcvrClk(CodeResidual, SigmaUERE)      # Estimate the Receiver Clock first guess as a weighted average of the residuals  

        # CodeResidual -= RcvrClk     # Remove Receiver Clock from residuals
        # PhaseResidual -= RcvrClk


        # Assigning values
        SatCorrInfo["Sod"] = Sod
        SatCorrInfo["Elevation"] = SatPrepro["Elevation"]
        SatCorrInfo["Azimuth"] = SatPrepro["Azimuth"]

        if SatCorrInfo["Dtr"] == Const.NAN or SatCorrInfo["CORR-CODE"] == 0 or SatCorrInfo["CORR-PHASE"] == 0 or \
            SatCorrInfo["GEOM-RNGE"] == 0:
            SatCorrInfo["Status"] = 0

        try:
            SatCorrInfo["SigmaUere"] = SigmaUERE
        except:
            pass


        CorrInfo[SatLabel] = SatCorrInfo

    return CorrInfo, RcvrRefPosXyz, RcvrRefPosLlh
