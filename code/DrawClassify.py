import matplotlib.pyplot as plt
import csv
import utils
import copy
import numpy as np
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib.patches import ConnectionPatch

def Draw(index_list, predict_data_path, save_path):
    method_list = []
    method_list.append("2-depth Encoding")
    method_list.append("1-depth Encoding")
    method_list.append("0-depth Encoding")
    method_list.append("ABC-pdr")
    method_list.append("IImc")
    method_list.append("ABC-dprove")
    method_list.append("IC3ref")
    method_list.append("Ground Truth")
    method_list.append("Random")

    maxtime = 3600
    with open(predict_data_path, newline='') as csvfile:
        data = list(csv.reader(csvfile))

    xaxis = list(range(1, maxtime + 1))
    data = data[1:]
    
    fig, ax = plt.subplots()
    
    axins = ax.inset_axes((0.25, 0.024, 0.3, 0.55))

    for method in method_list:
        solved_num_list = [0] * maxtime
        for line in data:
            pointer = index_list[method_list.index(method)]
            if line[pointer] != "timeout" and line[pointer] != "failed" and line[pointer] != "0.0" and line[pointer] != "0":
                lowerbound = int(float(line[pointer]) + 1)
                for index in range(len(solved_num_list)):
                    if index >= lowerbound:
                        solved_num_list[index] += 1
        if method in utils.method_list:
            method = utils.NameMap(method)
        if method == "2-depth Encoding":
            color = "#004c6d"
        elif method == "1-depth Encoding":
            color = "#6996b3"
        elif method == "0-depth Encoding":
            color = "#9dc6e0"
        elif method == "ABC-pdr":
            color = "#D68910"
        elif method == "IImc":
            color = "#dd5756"
        elif method == "ABC-dprove":
            color = "#ab4a85"
        elif method == "IC3ref":
            color = "#58508d"
        elif method == "Ground Truth":
            color = "#C3C3C3"
        elif method == "Random":
            color = "#000000"
        else:
            color = None
        
        if method == "Ground Truth":
            linestyle = ':'
        elif method == "Random":
            linestyle = "--"
        else:
            linestyle = None
        plt.plot(xaxis, solved_num_list, label=method, color=color, linestyle=linestyle)        
        axins.plot(xaxis, solved_num_list, label=method, color=color, linestyle=linestyle)


    xlim0 = -50
    xlim1 = 550

    ylim0 = 500
    ylim1 = 800
    axins.set_xlim(xlim0, xlim1)
    axins.set_ylim(ylim0, ylim1)
    axins.set_xticks([])
    axins.set_yticks([])
    tx0 = xlim0
    tx1 = xlim1
    ty0 = ylim0
    ty1 = ylim1
    sx = [tx0,tx1,tx1,tx0,tx0]
    sy = [ty0,ty0,ty1,ty1,ty0]
    ax.plot(sx,sy,"black",linestyle="--",linewidth=0.7)

    xy = (xlim1,ylim0)
    xy2 = (xlim0,ylim0)
    con = ConnectionPatch(xyA=xy2,xyB=xy,coordsA="data",coordsB="data",
            axesA=axins,axesB=ax,linestyle="--",linewidth=0.7)
    axins.add_artist(con)

    xy = (xlim1,ylim1)
    xy2 = (xlim0,ylim1)
    con = ConnectionPatch(xyA=xy2,xyB=xy,coordsA="data",coordsB="data",
            axesA=axins,axesB=ax,linestyle="--",linewidth=0.7)
    axins.add_artist(con)

    plt.xticks(range(0, 4000, 900), size=17)
    plt.yticks(size=17)
    plt.legend(prop = {'size':13})
    plt.subplots_adjust(left=0.09, right=0.99, top=0.99, bottom=0.07)
    # plt.xlabel('Time (s)', size=17)
    # plt.ylabel('# Solved Benchmarks', size=17)
 
    plt.savefig(save_path)
    plt.show()

if __name__ == '__main__':
    root_path = utils.root_path
    
    index_list = [7, 6, 5, 2, 3, 1, 4, 11, 12]
    index_with_encoding_list = [16, 15, 14, 2, 3, 1, 4, 11, 12]

    classify_basic_data_path = utils.classify_basic_data_path
    predict_data_path = classify_basic_data_path + "classify_predict_data.csv"
    predict_data_with_encoding_path = classify_basic_data_path + "classify_predict_data_with_encoding.csv"

    save_path = utils.classify_result_path + "Classify.pdf"
    save_with_encoding_path = utils.classify_result_path + "ClassifyWithEncodingTime.pdf"
    
    Draw(index_list, predict_data_path, save_path)
    Draw(index_with_encoding_list, predict_data_with_encoding_path, save_with_encoding_path)





    

    