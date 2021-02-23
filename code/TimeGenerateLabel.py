import csv
import sys
import utils

def GenerateLabel(data_path, name_list_path, time_message_dic_path, timeout_message_dic_path):
    with open(data_path, "r") as csvfile:
        data = list(csv.reader(csvfile))[1:]

    name_list = []
    time_message_dic = {}
    timeout_message_dic = {}
    for line in data:
        name_list.append(line[0])
        time_dic = {}
        timeout_dic = {}
        for index in range(len(utils.method_list)):
            if line[index + 1] == "timeout" or line[index + 1] == "failed" or line[index + 1] == "0.0" or line[index + 1] == "0":
                time_dic[utils.method_list[index]] = 3600.0
                timeout_dic[utils.method_list[index]] = True
            else:
                time_dic[utils.method_list[index]] = float(line[index + 1])
                timeout_dic[utils.method_list[index]] = False
        time_message_dic[line[0]] = time_dic
        timeout_message_dic[line[0]] = timeout_dic

    utils.WriteJson(name_list, name_list_path)
    utils.WriteJson(time_message_dic, time_message_dic_path)
    utils.WriteJson(timeout_message_dic, timeout_message_dic_path)
    return name_list, time_message_dic, timeout_message_dic

def GenerateLabelForOneMethod(data_path, name_list_path, time_dic_path, timeout_dic_path, method):
    method_list = utils.method_list    
    with open(data_path, "r") as csvfile:
        data = list(csv.reader(csvfile))[1:]

    name_list = []
    time_dic = {}
    timeout_dic = {}
    for line in data:
        name = line[0]
        name_list.append(name)
        index = method_list.index(method) + 1
        if line[index] == "timeout" or line[index] == "failed" or line[index] == "0.0" or line[index] == "0":
            time_dic[name] = 3600.0
            timeout_dic[name] = True
        else:
            time_dic[name] = float(line[index])
            timeout_dic[name] = False

    utils.WriteJson(name_list, name_list_path)
    utils.WriteJson(time_dic, time_dic_path)
    utils.WriteJson(timeout_dic, timeout_dic_path)
    return name_list, time_dic, timeout_dic

def TimeGenerateLabel(data_path, stage, method):
    if stage == "train":
        name_list_path = utils.time_basic_data_path + "train_name_list.json"
        time_dic_path = utils.time_basic_data_path + "train_time_dic_" + method + ".json"
        timeout_dic_path = utils.time_basic_data_path + "train_timeout_dic_" + method + ".json"
    elif stage == "test":
        name_list_path = utils.time_basic_data_path + "test_name_list.json"
        time_dic_path = utils.time_basic_data_path + "test_time_dic_" + method + ".json"
        timeout_dic_path = utils.time_basic_data_path + "test_timeout_dic_" + method + ".json"
    name_list, time_dic, timeout_dic = GenerateLabelForOneMethod(data_path, name_list_path, time_dic_path, timeout_dic_path, method)
    return name_list, time_dic, timeout_dic

if __name__ == '__main__':
    time_basic_data_path = utils.time_basic_data_path
    
    train_data_path = time_basic_data_path + "train_data.csv"
    test_data_path = time_basic_data_path + "test_data.csv"
    train_name_list_path = time_basic_data_path + "train_name_list.json"
    test_name_list_path = time_basic_data_path + "test_name_list.json"
    train_time_message_path = time_basic_data_path + "train_time_message.json"
    test_time_message_path = time_basic_data_path + "test_time_message.json"
    train_timeout_message_path = time_basic_data_path + "train_timeout_message.json"
    test_timeout_message_path = time_basic_data_path + "test_timeout_message.json"

    GenerateLabel(train_data_path, train_name_list_path, train_time_message_path, train_timeout_message_path)
    GenerateLabel(test_data_path, test_name_list_path, test_time_message_path, test_timeout_message_path)




