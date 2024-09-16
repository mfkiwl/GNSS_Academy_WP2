from InputOutput import LeoPosIdx, LeoQuatIdx, SatPosIdx, SatApoIdx, SatClkIdx, SatBiaIdx
import numpy as np

from COMMON import GnssConstants as Const
from COMMON.Misc import modulo
from COMMON.Dates import convertYearDoy2JulianDay

def computeLeoComPos(Sod, LeoPosInfo):

    xPos = yPos = zPos = None

    # try:      # If LeoPosInfo is a dictionary
    #     # First we ensure Sod index
    #     sod_index = LeoPosInfo.get("SOD").index(Sod)

    #     # Iterate the keys of a given dictionary to acquire x, y and z position
    #     for key in LeoPosInfo.keys():

    #         # In case of finding one of them, it takes a list (value associated to that key) and finds the correspondent value using sod_index
    #         if "x" in key:
    #             xPos = LeoPosInfo.get(key)[sod_index]

    #         elif "y" in key:
    #             yPos = LeoPosInfo.get(key)[sod_index]

    #         elif "z" in key:
    #             zPos = LeoPosInfo.get(key)[sod_index]

    # except:
    #     pass

    try:
        LeoPosInfo = LeoPosInfo.to_numpy()
        value_position = np.where(LeoPosInfo[:,LeoPosIdx["SOD"]] == Sod)[0][0]

        xPos = LeoPosInfo[value_position:, LeoPosIdx["xCM"]][0]
        yPos = LeoPosInfo[value_position:, LeoPosIdx["yCM"]][0]
        zPos = LeoPosInfo[value_position:, LeoPosIdx["zCM"]][0]
    except:
        pass

    return (xPos, yPos, zPos)


def computeSatClkBias(Sod, SatLabel, SatClkInfo):
    # Things to discuss, there are acases where the Sod is 20 but this clk uses jump of 30 seconds
    clock_bias = 0
    close_value_down = close_value_up = 0   # In case of not having any Sod similar, interpolate between the closest values

    # Setting decimal precision for flaots
    # np.set_printoptions(suppress=True, precision=32)    # Force pandas to work in complete notation and not scientific notation
    np.set_printoptions(precision=32)       # Set precision of np to 32 to use all decimals

    # First, filter by satellite
    SatClkInfo = SatClkInfo[SatClkInfo[SatClkIdx["CONST"]] == SatLabel[:1]]
    SatClkInfo = SatClkInfo[SatClkInfo[SatClkIdx["PRN"]] == SatLabel[1:]]

    # Converting SOD from object to int
    SatClkInfo[SatClkIdx["SOD"]] = SatClkInfo[SatClkIdx["SOD"]].astype(int)     # Convert SOD Column from object type to int type

    try:
        if Sod in SatClkInfo[SatClkIdx["SOD"]].unique():                     # SatClkInfo returns object type, not int or float type
            # Get values of SatClkInfo filtered
            SatClkInfo = SatClkInfo[SatClkInfo[SatClkIdx["SOD"]] == Sod].values

            # Get a value of np in the column SatClkIdx["CLK-BIAS"] and in every row and set it to np.float64
            # set to np.float64 and getting the first value of the given array
            clock_bias = SatClkInfo[:, SatClkIdx["CLK-BIAS"]].astype(np.float64)[0]


        else:
            # First, we acquire the last element for cases lower than Sod, because un case of having more than 1 option, 
            # the closer one is the last position of the array
            close_value_down = SatClkInfo[SatClkInfo[SatClkIdx["SOD"]] < Sod][-1:]     # Getting the last element for cases lower than Sod
            close_value_down = close_value_down.values

            close_value_up = SatClkInfo[SatClkInfo[SatClkIdx["SOD"]] > Sod][:1]        # Getting the first element for cases higher than Sod
            close_value_up = close_value_up.values

            # The idea is to compute first the differences to get the pendent of the line, but doing this we will love the offset
            # Then, we have to add this offset as a sum

            clock_bias = (\
                            (close_value_up[:, SatClkIdx["CLK-BIAS"]].astype(np.float64)[0] - close_value_down[:, SatClkIdx["CLK-BIAS"]].astype(np.float64)[0])/  \
                            (close_value_up[:, SatClkIdx["SOD"]][0] - close_value_down[:, SatClkIdx["SOD"]][0]) \
                        ) * Sod \
                        + close_value_down[:, SatClkIdx["CLK-BIAS"]].astype(np.float64)[0]      # Adding the offset removed by the last expression
    except:
        pass

    return clock_bias


def computeRcvrApo(Conf, Year, Doy, Sod, SatLabel, LeoQuatInfo):
    
    # Acquiring Center of Masses, Antenna Reference Frame and Phase Center Offset
    COM = Conf['LEO_COM_POS']
    ARP = Conf['LEO_ARP_POS']

    if SatLabel[0] == 'G':
        PCO = Conf['LEO_PCO_GPS']
    elif SatLabel[0] == 'E':
        PCO = Conf['LEO_PCO_GAL']
    # COM -> ARP -> APC
    APC = ARP - PCO     # Acquiring Antenna Phase Center (APC), as PCO is the difference between ARP and APC

    LeoQuatInfo = LeoQuatInfo[LeoQuatInfo[LeoQuatIdx["SOD"]] == Sod]

    # Converting SOD from object to int
    q0 = LeoQuatInfo[LeoQuatIdx["q0"]].iloc[0]
    q1 = LeoQuatInfo[LeoQuatIdx["q1"]].iloc[0]
    q2 = LeoQuatInfo[LeoQuatIdx["q2"]].iloc[0]
    q3 = LeoQuatInfo[LeoQuatIdx["q3"]].iloc[0]

    # Creating Rotation Matrix for later computation
    rotation_matrix = np.array([[  (1 - 2*q2**2 - 2*q3**2),  2*(q1*q2 - q0*q3),         2*(q0*q2 + q1*q3)],
                                [   2*(q1*q2 + q0*q3),       (1 - 2*q1**2 - 2*q3**2),   2*(q2*q3 - q0*q1)],
                                [   2*(q1*q3 - q0*q2),       2*(q0*q1 + q2*q3),         (1 - 2*q1**2 - 2*q2**2)]
                                ])

    # Acquiring Greenwich Siderial Time Reference, but need to obtain Jualian Day Number and fraction of the day first
    JDN = convertYearDoy2JulianDay(Year, Doy, Sod) - 2415020    # Julian Day Number
    fday = Sod / Const.S_IN_D                                   # fday is Fractional part of the day

    gstr = modulo(279.690983 + 0.9856473354*JDN + 360*fday + 180, 360)      # Convert o radians and rotate it over the third axis (Applying Earth Rotation)
    gstr = np.deg2rad(gstr)     # Corvert it from degree to radian

    # STILL IN PROCESS ( How to compute ECI to ECEF and acquire XYZ Position ???? )



def computeSatComPos(TransmissionTime, SatPosInfo):
    pass


def applySagnac(SatComPos, FlightTime):

    angle = Const.OMEGA_EARTH * FlightTime
    rot_matrix = np.array( [[np.cos(angle),    np.sin(angle),   0],
                            [-np.sin(angle),   np.cos(angle),   0],
                            [0,                0,               1]])

    sagnac = np.dot(rot_matrix, SatComPos)

    return sagnac


def computeSatApo(SatLabel, SatComPos, RcvrPos, SunPos, SatApoInfo):
    SatApoInfo = SatApoInfo[SatApoInfo[SatApoIdx["CONST"]] == SatLabel[:1]]
    SatApoInfo = SatApoInfo[SatApoInfo[SatApoIdx["PRN"]] == SatLabel[1:]]

    # From Center of Masses, Receiver Position, Sun Position and Antenna Phase Offset, compute Antenna Phase Offset position


def getSatBias(GammaF1F2, SatLabel, SatBiaInfo):

    SatBiaInfo = SatBiaInfo[SatBiaInfo[SatBiaIdx["CONST"]] == SatLabel[:1]]
    SatBiaInfo = SatBiaInfo[SatBiaInfo[SatBiaIdx["PRN"]] == SatLabel[1:]]

    CodeBias = (SatBiaInfo[SatBiaIdx["OBS_f1_C"]] + GammaF1F2 * SatBiaInfo[SatBiaIdx["OBS_f2_C"]]) / (1 + GammaF1F2)
    PhaseBias = (SatBiaInfo[SatBiaIdx["OBS_f1_P"]] + GammaF1F2 * SatBiaInfo[SatBiaIdx["OBS_f2_P"]]) / (1 + GammaF1F2)
    ClockBias = (SatBiaInfo[SatBiaIdx["CLK_f1_C"]] + GammaF1F2 * SatBiaInfo[SatBiaIdx["CLK_f2_C"]]) / (1 + GammaF1F2)

    return (CodeBias, PhaseBias, ClockBias)



def computeDtr(SatComPos_1, SatComPos, Sod, Sod_1):
    pass


def getUERE(Conf, SatLabel):
    sigmaUERE = 0

    if SatLabel[0] == 'G':
        sigmaUERE = Conf['GPS_UERE']

    elif SatLabel[0] == 'E':
        sigmaUERE = Conf['GAL_UERE']

    return sigmaUERE

def computeGeoRange(SatCopPos, RcvrPos):
    pass



def estimateRcvrClk(CodeResidual, SigmaUERE):
    pass