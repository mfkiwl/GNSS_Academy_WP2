from InputOutput import LeoPosIdx, LeoQuatIdx, SatPosIdx, SatApoIdx, SatClkIdx, SatBiaIdx

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
        LeoPosInfo = LeoPosInfo[LeoPosInfo[LeoPosIdx["SOD"]] == Sod]

        xPos = float(LeoPosInfo[LeoPosIdx["xCM"]].unique())
        yPos = float(LeoPosInfo[LeoPosIdx["yCM"]].unique())
        zPos = float(LeoPosInfo[LeoPosIdx["zCM"]].unique())
    except:
        pass

    return (xPos, yPos, zPos)


def computeSatClkBias(Sod, SatLabel, SatClkInfo):
    # Things to discuss, there are acases where the Sod is 20 but this clk uses jump of 30 seconds
    clock_bias = None

    close_value_down = close_value_up = 0   # In case of not having any Sod similar, interpolate between the closest values

    # First, filter by satellite
    SatClkInfo = SatClkInfo[SatClkInfo[SatClkIdx["CONST"]] == SatLabel[:1]]
    SatClkInfo = SatClkInfo[SatClkInfo[SatClkIdx["PRN"]] == SatLabel[1:]]

    SatClkInfo[SatClkIdx["SOD"]] = SatClkInfo[SatClkIdx["SOD"]].astype(int)     # Convert SOD Column from object type to int type

    try:
        if Sod in SatClkInfo[SatClkIdx["SOD"]].unique():                     # SatClkInfo returns object type, not int or float type
            SatClkInfo = SatClkInfo[SatClkInfo[SatClkIdx["SOD"]] == Sod]
            clock_bias = float(SatClkInfo[SatClkIdx["CLK-BIAS"]])

        else:
            close_value_down = SatClkInfo[SatClkInfo[SatClkIdx["SOD"]] < Sod][-1:]     # Getting the last element for cases lower than Sod
            close_value_up = SatClkInfo[SatClkInfo[SatClkIdx["SOD"]] > Sod][:1]        # Getting the first element for cases higher than Sod

            # * We have a problem because by astyping, we pass from -4.114159919830e-04 to -0.000411
            # * Another problem is that I am using pandas, so clock_bias now is a pandas, TRY TO REVERT IT or CONVERT PANDAS INTO DICTIONARIES
            clock_bias = ((close_value_up[SatClkIdx["CLK-BIAS"]].astype(float) - close_value_down[SatClkIdx["CLK-BIAS"]].astype(float))  \
                            /(close_value_up[SatClkIdx["SOD"]].astype(int) - close_value_down[SatClkIdx["SOD"]].astype(int))   ) * Sod
    except:
        pass

    return clock_bias


def computeRcvrApo(Conf, Year, Doy, Sod, SatLabel, LeoQuatInfo):
    pass
