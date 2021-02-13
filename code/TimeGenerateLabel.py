import csv
import sys
import utils

def GenerateLabel(data_path, name_list_path, time_message_path, timeout_message_path):
    with open(data_path, "r") as csvfile:
        data = list(csv.reader(csvfile))

    name_list = []
    time_message = {}
    timeout_message = {}
    for line in data:
        name_list.append(line[0])
        time_dic = {}
        timeout_dic = {}
        for index in range(len(utils.method_list)):
            if line[index + 1] == "timeout" or line[index + 1] == "failed" or line[index + 1] == "0.0":
                time_dic[utils.method_list[index]] = 3600.0
                timeout_dic[utils.method_list[index]] = True
            else:
                time_dic[utils.method_list[index]] = float(line[index + 1])
                timeout_dic[utils.method_list[index]] = False
        time_message[line[0]] = time_dic
        timeout_message[line[0]] = timeout_dic

    utils.WriteJson(name_list, name_list_path)
    utils.WriteJson(time_message, time_message_path)
    utils.WriteJson(timeout_message, timeout_message_path)
         

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




