from InputOutput import LeoPosIdx, LeoQuatIdx, SatPosIdx, SatApoIdx, SatClkIdx, SatBiaIdx

def computeLeoComPos(Sod, LeoPosInfo):

    xPos = yPos = zPos = None

    try:
        # First we ensure Sod index
        sod_index = LeoPosInfo.get("SOD").index(Sod)

        # Iterate the keys of a given dictionary to acquire x, y and z position
        for key in LeoPosInfo.keys():

            # In case of finding one of them, it takes a list (value associated to that key) and finds the correspondent value using sod_index
            if "x" in key:
                xPos = LeoPosInfo.get(key)[sod_index]

            elif "y" in key:
                yPos = LeoPosInfo.get(key)[sod_index]

            elif "z" in key:
                zPos = LeoPosInfo.get(key)[sod_index]

    except:
        pass

    return (xPos, yPos, zPos)
