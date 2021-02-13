import utils
from os.path import getsize

def ProcessNameList(train_name_list_path, test_name_list_path):
    train_name_list = utils.ReadJson(train_name_list_path)
    test_name_list = utils.ReadJson(test_name_list_path)
    total_name_list = list(set(train_name_list) | set(test_name_list))
    processed_name_list = []
    for name in total_name_list:
        processed_name_list.append(name.split(".aig")[0])
    return total_name_list, processed_name_list

def StatisticAvgEncodingTime(log_path, time_path):
    dic = {}
    with open(log_path, 'r') as file_obj:
        data = file_obj.read()
        file_obj.close()
    lines = data.split("\n")
    num = int(len(lines) / 2)
    for i in range(num):
        name_message = lines[2 * i]
        time_message = lines[2 * i + 1]
        name = name_message.split("../networks_aag/")[1].split(".aag")[0]
        temp_time = time_message.split("user\t")[1].split("s")[0]
        minute = float(temp_time.split("m")[0])
        second = float(temp_time.split("m")[1])
        time = minute * 60 + second
        dic[name] = time
    utils.WriteJson(dic, time_path)
    return dic

def GetEncodingSize(name):
    path = utils.encoding_aig_path + name
    size = getsize(path)
    return size

def StatisticAvgAag(name_list):
    sum_num = 0
    for name in processed_name_list:
        aag_path = utils.encoding_aag_path + name + ".aag"
        with open(aag_path, 'r') as file_obj:
            data = file_obj.read()
            file_obj.close()
        lines = data.split("\n")
        num = int(lines[0].split(" ")[1])
        sum_num += num
    avg_num = sum_num / len(processed_name_list)
    return avg_num


if __name__ == '__main__':
    train_name_list_path = utils.classify_basic_data_path + "train_name_list.json"
    test_name_list_path = utils.classify_basic_data_path + "test_name_list.json"
    total_name_list, processed_name_list = ProcessNameList(train_name_list_path, test_name_list_path)

    encoding_log_path_0 = utils.encoding_log_path_0
    encoding_log_path_1 = utils.encoding_log_path_1
    encoding_log_path_2 = utils.encoding_log_path_2
    encoding_log_path_list = [encoding_log_path_0, encoding_log_path_1, encoding_log_path_2]

    encoding_time_path_0 = utils.classify_basic_data_path + "encoding_time_0.json"
    encoding_time_path_1 = utils.classify_basic_data_path + "encoding_time_1.json"
    encoding_time_path_2 = utils.classify_basic_data_path + "encoding_time_2.json"
    encoding_time_path_list = [encoding_time_path_0, encoding_time_path_1, encoding_time_path_2]

    for i in range(len(encoding_log_path_list)):
        log_path = encoding_log_path_list[i]
        time_path = encoding_time_path_list[i]
        print("layer" + str(i))
        dic = StatisticAvgEncodingTime(log_path, time_path)
        sum_time = 0.0
        for name in processed_name_list:
            sum_time += dic[name]
        avg_time = sum_time / len(processed_name_list)
        print(avg_time)
        time_list = []
        for name in processed_name_list:
            time_list.append(dic[name])
        time_list = sorted(time_list)
        median_time = time_list[int(len(processed_name_list) / 2)]
        print(median_time)
    
    sum_size = 0    
    for name in total_name_list:
        temp_size = GetEncodingSize(name)
        sum_size += temp_size
    avg_size = sum_size / len(total_name_list)
    print(avg_size)

    # avg_aag = StatisticAvgAag(processed_name_list)
    # print(avg_aag)

