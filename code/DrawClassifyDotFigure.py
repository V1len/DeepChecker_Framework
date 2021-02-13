import csv
import utils
import sys
import random
import numpy as np
import matplotlib.pyplot as plt

def ChangeData(data):
    if data != "timeout" and data != "failed" and data != "0.0" and data != "0":
        changed_data = float(data)
    else:
        changed_data = 3600.00
    return changed_data

if __name__ == '__main__':
    classify_basic_data_path = utils.classify_basic_data_path
    predict_data_path = classify_basic_data_path + "classify_predict_data.csv"

    with open(predict_data_path, newline='') as csvfile:
        data = list(csv.reader(csvfile))

    data = data[1:]
    
    truth_data_list = []
    random_data_list = []
    predict_data_list_0 = []
    predict_data_list_1 = []
    predict_data_list_2 = []
    for line in data:
        truth_data_list.append(ChangeData(line[len(utils.method_list) + len(utils.encoding_layer_list) + 1]))
        random_data_list.append(ChangeData(line[len(utils.method_list) + len(utils.encoding_layer_list) + 2]))
        predict_data_list_0.append(ChangeData(line[len(utils.method_list) + 1]))
        predict_data_list_1.append(ChangeData(line[len(utils.method_list) + 2]))
        predict_data_list_2.append(ChangeData(line[len(utils.method_list) + 3]))


    all_data_list = [random_data_list, predict_data_list_0, predict_data_list_1, predict_data_list_2]
    figure_label_list = ["Random", "0-depth Encoding", "1-depth Encoding", "2-depth Encoding"]
    for i in range(len(all_data_list)):
        temp_data_list = all_data_list[i]
        label = figure_label_list[i]
        save_path = utils.classify_result_path + figure_label_list[i] + ".pdf"
        for layer in utils.encoding_layer_list:
            fig, ax = plt.subplots()
            ax.set_title(label)
            # for j in range(len(data)):
            #     plt.scatter(temp_data_list[j], truth_data_list[j])
            ax.scatter(temp_data_list, truth_data_list)
            ax.set_xlabel('Predict Time (s)')
            ax.set_ylabel('Truth Time (s)')
            # ax.set_xlim(0, 3600)
            # ax.set_ylim(0, 3600)
            ax.set_xscale('log')
            ax.set_yscale('log')
            plt.savefig(save_path)