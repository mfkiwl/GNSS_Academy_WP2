
import sys, os
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import conda
CondaFileDir = conda.__file__
CondaDir = CondaFileDir.split('lib')[0]
ProjLib = os.path.join(os.path.join(CondaDir, 'share'), 'proj')
os.environ["PROJ_LIB"] = ProjLib
from mpl_toolkits.basemap import Basemap

import warnings
import matplotlib.cbook

from COMMON import GnssConstants

def createFigure(PlotConf):
    try:
        fig, ax = plt.subplots(1, 1, figsize = PlotConf["FigSize"])
    
    except:
        fig, ax = plt.subplots(1, 1)

    return fig, ax

def saveFigure(fig, Path):
    Dir = os.path.dirname(Path)
    try:
        os.makedirs(Dir)
    except: pass
    fig.savefig(Path, dpi=150., bbox_inches='tight')

def prepareAxis(PlotConf, ax):
    for key in PlotConf:
        if key == "Title":
            ax.set_title(PlotConf["Title"])

        for axis in ["x", "y"]:
            if axis == "x":
                if key == axis + "Label":
                    ax.set_xlabel(PlotConf[axis + "Label"])

                if key == axis + "Ticks":
                    ax.set_xticks(PlotConf[axis + "Ticks"])

                if key == axis + "TicksLabels":
                    ax.set_xticklabels(PlotConf[axis + "TicksLabels"])
                
                if key == axis + "Lim":
                    ax.set_xlim(PlotConf[axis + "Lim"])

            if axis == "y":
                if key == axis + "Label":
                    ax.set_ylabel(PlotConf[axis + "Label"])

                if key == axis + "Ticks":
                    ax.set_yticks(PlotConf[axis + "Ticks"])

                if key == axis + "TicksLabels":
                    ax.set_yticklabels(PlotConf[axis + "TicksLabels"], fontsize=8)
                
                if key == axis + "Lim":
                    ax.set_ylim(PlotConf[axis + "Lim"])

        if key == "Grid" and PlotConf[key] == True:
            ax.grid(linestyle='--', linewidth=0.5, which='both', alpha = 0.5)

def prepareColorBar(PlotConf, ax, Values):
    try:
        Min = PlotConf["ColorBarMin"]
    except:
        Mins = []
        for v in Values.values():
            Mins.append(min(v))
        Min = min(Mins)
    try:
        Max = PlotConf["ColorBarMax"]
    except:
        Maxs = []
        for v in Values.values():
            Maxs.append(max(v))
        Max = max(Maxs)
    normalize = mpl.cm.colors.Normalize(vmin=Min, vmax=Max)

    divider = make_axes_locatable(ax)
    # size size% of the plot and gap of pad% from the plot
    color_ax = divider.append_axes("right", size="3%", pad="2%")
    cmap = plt.cm.get_cmap(PlotConf["ColorBar"])

    if "ColorBarDiscrete" in PlotConf:

        list_label = [*range(Min, Max, 1)]        # Can be [*range(0, len(PlotConf["zData"].keys()), 1)], as well

        norm = mpl.colors.BoundaryNorm(list_label, cmap.N, extend = 'max')      # norm = mpl.colors.BoundaryNorm(list_label, cmap.N, extend = 'both')

        cbar = mpl.colorbar.ColorbarBase(color_ax, 
        cmap=cmap,
        norm=norm,
        label=PlotConf["ColorBarLabel"])

        cbar.set_ticks(list_label)
        cbar.set_ticklabels(PlotConf["zData"].keys())

        colors = [cmap(norm(value)) for value in list_label]

    else:

        cbar = mpl.colorbar.ColorbarBase(color_ax, 
        cmap=cmap,
        norm=mpl.colors.Normalize(vmin=Min, vmax=Max),
        label=PlotConf["ColorBarLabel"])

        colors = []

    return normalize, cmap, colors

def drawMap(PlotConf, ax,):
    Map = Basemap(projection = 'cyl',
    llcrnrlat  = PlotConf["LatMin"]-0,
    urcrnrlat  = PlotConf["LatMax"]+0,
    llcrnrlon  = PlotConf["LonMin"]-0,
    urcrnrlon  = PlotConf["LonMax"]+0,
    lat_ts     = 10,
    resolution = 'l',
    ax         = ax)

    # Draw map meridians
    Map.drawmeridians(
    np.arange(PlotConf["LonMin"],PlotConf["LonMax"]+1,PlotConf["LonStep"]),
    labels = [0,0,0,1],
    fontsize = 6,
    linewidth=0.2)
        
    # Draw map parallels
    Map.drawparallels(
    np.arange(PlotConf["LatMin"],PlotConf["LatMax"]+1,PlotConf["LatStep"]),
    labels = [1,0,0,0],
    fontsize = 6,
    linewidth=0.2)

    # Draw coastlines
    Map.drawcoastlines(linewidth=0.5)

    # Draw countries
    Map.drawcountries(linewidth=0.25)


def generateLinesPlot(PlotConf):
    LineWidth = 1.5

    fig, ax = createFigure(PlotConf)

    prepareAxis(PlotConf, ax)

    for key in PlotConf:
        if key == "LineWidth":
            LineWidth = PlotConf["LineWidth"]
        if key == "ColorBar" or key == "ColorBarDiscrete":
            normalize, cmap, colors = prepareColorBar(PlotConf, ax, PlotConf["zData"])

        if key == "Map" and PlotConf[key] == True:
            drawMap(PlotConf, ax)

    for Label in PlotConf["yData"].keys():

        if "ColorBarDiscrete" in PlotConf:
            z_data = np.array(PlotConf["zData"][Label].str.slice(1).astype(int))
            colorbar = cmap(normalize(z_data))
        else: 
            colorbar = cmap(normalize(np.array(PlotConf["zData"][Label])))


        if "ColorBar" in PlotConf:
            try:
                ax.scatter(PlotConf["xData"][Label], PlotConf["yData"][Label], 
                marker = PlotConf["Marker"],
                s = PlotConf["MarkerSize"],
                linewidth = LineWidth,
                c = colorbar)
                if "Annotation" in PlotConf:
                    x_data = np.array(PlotConf["xData"][Label])
                    y_data = np.array(PlotConf["yData"][Label])
                    annotations = np.array(PlotConf["zData"][Label])

                    prev_x_data_point = 0
                    first_x_data_point = True
                    pos = 7

                    try:

                        for i in range(0, len(annotations)):
                            if x_data[i] > prev_x_data_point + 700 / GnssConstants.S_IN_H and first_x_data_point == False:

                                color_used = colors[int(Label[1:]) - PlotConf["ColorBarMin"]]

                                # Reference: https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.annotate.html
                                ax.annotate(Label, (x_data[i], y_data[i]), fontsize = 5, color = color_used, xytext=(-10, pos), textcoords='offset points')

                                prev_x_data_point = x_data[i]
                                pos = -7 if pos == 7 else 7

                            elif first_x_data_point == True:

                                first_x_data_point = False
                                color_used = colors[int(Label[1:]) - PlotConf["ColorBarMin"]]

                                ax.annotate(Label, (x_data[i], y_data[i]), fontsize = 5, color = color_used, xytext=(7, pos), textcoords='offset points')

                                prev_x_data_point = x_data[i]
                                pos = -7 if pos == 7 else 7


                    except:
                        pass
            except:
                pass

            try:
                if PlotConf["AddPlot"] == 1:
                    ax.scatter(PlotConf["xData2"][Label], PlotConf["yData2"][Label], 
                        marker = PlotConf["Marker"], 
                        s = PlotConf["MarkerSize"],
                        linewidth = LineWidth,
                        c = "grey")
            except:
                pass
        else:
            ax.plot(PlotConf["xData"][Label], PlotConf["yData"][Label],
            PlotConf["Marker"],
            linewidth = LineWidth)



    saveFigure(fig, PlotConf["Path"])
    plt.close()

def generateStepPlot(PlotConf):

    plt.figure(figsize=PlotConf["FigSize"])

    plt.plot(PlotConf["xData"] , PlotConf["yData"], label = "Raw", c = PlotConf["colorData"])
    plt.plot(PlotConf["xData2"] , PlotConf["yData2"], label = "Smoothed", c = PlotConf["colorData2"] )

    plt.xlabel(PlotConf["yLabel"]) 
    plt.ylabel(PlotConf["yLabel"]) 
    plt.title(PlotConf["Title"]) 

    plt.xlim(left = min(PlotConf["xData"]), right = max(PlotConf["xData"]))
    plt.ylim(top = max(PlotConf["yLim"]), bottom = min(PlotConf["yLim"]))
    plt.yticks(PlotConf["yTicks"])

    plt.grid(visible = True, axis = 'both', linestyle = '--', linewidth = 1, alpha = 0.4)
    plt.legend()

    plt.savefig(PlotConf["Path"])
    plt.close()


# def generateScatterPlot(PlotConf):

#     plt.figure(figsize=PlotConf["FigSize"])

#     plot = plt.scatter(PlotConf["xData"].values , PlotConf["yData"].values, label = "Raw", c = PlotConf["zData"], cmap = "gnuplot", marker = ".", s = 2)
#     # plt.plot(PlotConf["xData2"] , PlotConf["yData2"], label = "Smoothed", c = PlotConf["colorData2"] )
#     plt.colorbar(plot)

#     plt.xlabel(PlotConf["yLabel"]) 
#     plt.ylabel(PlotConf["yLabel"]) 
#     plt.title(PlotConf["Title"]) 

#     plt.xlim(left = min(PlotConf["xData"]), right = max(PlotConf["xData"]))
#     plt.ylim(top = max(PlotConf["yLim"]), bottom = min(PlotConf["yLim"]))
#     plt.yticks(PlotConf["yTicks"])

#     plt.grid(visible = True, axis = 'both', linestyle = '--', linewidth = 1, alpha = 0.4)
#     plt.legend()

#     plt.savefig(PlotConf["Path"])



def generatePlot(PlotConf):
    if(PlotConf["Type"] == "Lines"):
        generateLinesPlot(PlotConf)

    elif (PlotConf["Type"] == "Step"):
        generateStepPlot(PlotConf)

    # elif (PlotConf["Type"] == "Scatter"):
    #     generateScatterPlot(PlotConf)
