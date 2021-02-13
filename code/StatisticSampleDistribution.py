import utils
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    classify_basic_data_path = utils.classify_basic_data_path

    embedded_dir_0 = utils.embedded_dir_0
    embedded_dir_1 = utils.embedded_dir_1
    embedded_dir_2 = utils.embedded_dir_2

    statistic_name_dic_path = classify_basic_data_path + "statistic_name_dic.json"
    statistic_name_dic = utils.ReadJson(statistic_name_dic_path)

    statistic_sample_distribution_path = utils.statistic_sample_distribution_path

    for i in range(len(utils.encoding_layer_list)):
        dir = [embedded_dir_0, embedded_dir_1, embedded_dir_2][i]
        for method in utils.method_list:
            temp_path = statistic_sample_distribution_path + method + "_distribution_" + str(i) + ".pdf"
            plt.figure()
            index = utils.method_list.index(method)
            name_list = statistic_name_dic[method]
            vec_list = utils.GetVecList(dir, name_list)
            statistic_vec = np.log(np.array(vec_list).sum(axis=0) + 1.0).tolist()
            # print(statistic_vec)
            # plt.subplot(2,2,index + 1)
            if i == 0:
                width = 0.3
                x = range(0,len(vec_list[0]),1)
            elif i == 1:
                width = 0.5
                x = range(0,len(vec_list[0]),4)
            else:
                width = 0.5
                x = range(0,len(vec_list[0]),30)
            plt.bar(range(len(statistic_vec)),statistic_vec, width=width, color="k")
            plt.title(utils.NameMap(method), size=30)
            y = range(0, 17, 4)
            plt.xticks(x, size=30)
            plt.yticks(y, size=30)
            # plt.xlabel('Features')
            # plt.ylabel('ln(# Total)')
            if i == 0:
                plt.subplots_adjust(left=0.1, right=0.99, top=0.9, bottom=0.10)
            elif i == 1:
                plt.subplots_adjust(left=0.1, right=0.99, top=0.9, bottom=0.10)
            else:
                plt.subplots_adjust(left=0.1, right=0.99, top=0.9, bottom=0.10)
            plt.savefig(temp_path)
            plt.show()


