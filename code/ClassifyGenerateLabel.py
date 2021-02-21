import csv
import sys
import utils

def GenerateLabel(data_path, name_list_path, label_dic_path):
    with open(data_path, "r") as csvfile:
        data = list(csv.reader(csvfile))[1:]

    name_list = []
    label_dic = {}
    for line in data:
        method = "None"
        time = float(sys.maxsize)
        for index in range(len(utils.method_list)):
            if line[index + 1] != "timeout" and line[index + 1] != "failed" and line[index + 1] != "0.0" and float(line[index + 1]) < time:
                time = float(line[index + 1])
                method = utils.method_list[index]
        if method != "None":
            name_list.append(line[0])
            label_dic[line[0]] = method
        else:
            print(line[0])
    utils.WriteJson(name_list, name_list_path)
    utils.WriteJson(label_dic, label_dic_path)

def Statistic(train_label_dic_path, test_label_dic_path):
    train_label_dic = utils.ReadJson(train_label_dic_path)
    test_label_dic = utils.ReadJson(test_label_dic_path)
    statistic_dic = utils.Statistic([train_label_dic])
    print("train_data")
    print(statistic_dic)
    statistic_dic = utils.Statistic([test_label_dic])
    print("test_data")
    print(statistic_dic)
    statistic_dic = utils.Statistic([train_label_dic, test_label_dic])
    print("all_data")
    print(statistic_dic)

def StatisticSamples(test_label_dic_path, statistic_name_dic_path):
    test_label_dic = utils.ReadJson(test_label_dic_path)
    statistic_name_dic = {}
    for method in utils.method_list:
        statistic_name_dic[method] = []
    for name in test_label_dic.keys():
        statistic_name_dic[test_label_dic[name]].append(name)
    utils.WriteJson(statistic_name_dic, statistic_name_dic_path)
    
# def JudgeSituation15(test_name_list_path):
#     test_name_list = utils.ReadJson(test_name_list_path)
#     for name in test_name_list:
#         vec = utils.GetVec(utils.embedded_dir_1, name)
#         if vec[14] != 0:
#             print(name)
        

if __name__ == '__main__':
    classify_basic_data_path = utils.classify_basic_data_path
    
    train_data_path = classify_basic_data_path + "classify_train_data.csv"
    test_data_path = classify_basic_data_path + "classify_test_data.csv"
    train_name_list_path = classify_basic_data_path + "train_name_list.json"
    test_name_list_path = classify_basic_data_path + "test_name_list.json"
    train_label_dic_path = classify_basic_data_path + "train_label_dic.json"
    test_label_dic_path = classify_basic_data_path + "test_label_dic.json"

    statistic_name_dic_path = classify_basic_data_path + "statistic_name_dic.json"

    GenerateLabel(train_data_path, train_name_list_path, train_label_dic_path)
    GenerateLabel(test_data_path, test_name_list_path, test_label_dic_path)

    Statistic(train_label_dic_path, test_label_dic_path)

    StatisticSamples(test_label_dic_path, statistic_name_dic_path)
 
    # JudgeSituation15(train_name_list_path)
    # JudgeSituation15(test_name_list_path)


