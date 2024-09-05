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


def computeSatClkBias(Sod, SatClkInfo):
    # Things to discuss, there are acases where the Sod is 20 but this clk uses jump of 30 seconds



    SatClkInfo = SatClkInfo[SatClkInfo[SatClkIdx["SOD"]] == Sod]
    return float(SatClkInfo[SatClkIdx["CLK-BIAS"]])


def computeRcvrApo(Conf, Year, Doy, Sod, SatLabel, LeoQuatInfo):
    pass
