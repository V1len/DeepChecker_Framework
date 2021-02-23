import json
import pickle
import os


method_list = ["dprove", "pdr", "iimc", "IC3"]


encoding_layer_list = ["0-depth Encoding", "1-depth Encoding", "2-depth Encoding"]

choose_top_method_number_1 = 1
choose_top_method_number_2 = 2
sum_method_number = len(method_list)


AVY_dprove_path = "/Users/zhujiayi/Desktop/dataset/2020-1-18/AVY_dprove_clean.json"
pdr_IC3_path = "/Users/zhujiayi/Desktop/dataset/2020-1-18/pdr_IC3_clean.json"
# iimc_path = "/mnt/hd0/DeepChecker/dataset/2020-1-26/clean_iimc.json"
others_path = "/Users/zhujiayi/Desktop/dataset/2020-1-12/others.json"
# hwmcc_clean_path = "/mnt/hd0/DeepChecker/dataset/2020-1-22/hwmcc_clean.json"

# iimc_benchmark_path = "/mnt/hd0/DeepChecker/dataset/2021-1-19/iimc_benchmark.json"

encoding_log_path_0 = "/Users/zhujiayi/Desktop/embedding/embedding_0.log"
encoding_log_path_1 = "/Users/zhujiayi/Desktop/embedding/embedding_1.log"
encoding_log_path_2 = "/Users/zhujiayi/Desktop/embedding/embedding_2.log"
# encoding_aig_path = "/mnt/hd0/DeepChecker/StatisticAvgEncodingTime/networks/"
# encoding_aag_path = "/mnt/hd0/DeepChecker/networks_aag/"

encoding_dir = "/Users/zhujiayi/Desktop/embedding/"
encoding_dir_0 = "/Users/zhujiayi/Desktop/embedding/embedding/2021-1-2_v0.1"
encoding_dir_1 = "/Users/zhujiayi/Desktop/embedding/embedding/2020-12-24_v1.1"
encoding_dir_2 = "/Users/zhujiayi/Desktop/embedding/embedding/2021-1-2_v2.2"
encoding_dic_dir_0 = "/Users/zhujiayi/Desktop/embedding/embedding/encoding_dic_0"
encoding_dic_dir_1 = "/Users/zhujiayi/Desktop/embedding/embedding/encoding_dic_1"
encoding_dic_dir_2 = "/Users/zhujiayi/Desktop/embedding/embedding/encoding_dic_2"

classify_task_path = "../classify/"
classify_model_path = classify_task_path + "classify_model/"
classify_predict_path = classify_task_path + "classify_predict/"
importance_message_path = classify_task_path + "importance_message/"
importance_fig_path = classify_task_path + "importance_figure/"
statistic_sample_distribution_path = classify_task_path + "statistic_sample_distribution/"
classify_basic_data_path = classify_task_path + "basic_data/"
classify_result_path = classify_task_path + "result/"

def MakeClassifyDir():
    if not os.path.exists(classify_task_path):
        os.mkdir(classify_task_path)   
    path_list = [classify_model_path, classify_predict_path, importance_message_path, importance_fig_path,
                    statistic_sample_distribution_path, classify_basic_data_path, classify_result_path]
    for temp_path in path_list:
        if not os.path.exists(temp_path):
            os.mkdir(temp_path)

time_task_path = "../time/"
time_model_path = time_task_path + "time_model/"
time_predict_path = time_task_path + "time_predict/"
time_basic_data_path = time_task_path + "basic_data/"
time_result_path = time_task_path + "result/"

def MakeTimeDir():    
    if not os.path.exists(time_task_path):
        os.mkdir(time_task_path)
    path_list = [time_model_path, time_predict_path, time_basic_data_path, time_result_path]
    for temp_path in path_list:
        if not os.path.exists(temp_path):
            os.mkdir(temp_path)

def WriteJson(my_json, json_path):
    with open(json_path, 'w')as file_obj:
        json.dump(my_json, file_obj)
        file_obj.close()

def ReadJson(json_path):
    with open(json_path, 'r') as load_f:
        load_json = json.load(load_f)
        load_f.close()
    return load_json

def Save_pkl(obj, pkl_name):
    with open(pkl_name, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def Load_pkl(pkl_name):
    with open(pkl_name, 'rb') as f:
        return pickle.load(f)

def InitialDic():
    statistic_dic = {}
    for method in method_list:
        statistic_dic[method] = 0
    return statistic_dic

def Statistic(dic_list):
    statistic_dic = InitialDic()
    for dic in dic_list:
        for key in dic.keys():
            value = dic[key]
            statistic_dic[value] += 1
    return statistic_dic

def GetVec(dir, name):
    aig_name = name + ".vector"
    aig_path = os.path.join(dir, aig_name)
    assert(os.path.isfile(aig_path))
    vector = []
    with open(aig_path, encoding='utf-8') as fp:
        line = fp.readlines()[0].split("[")[1].split("]")[0]
        items = line.split(", ")
        for item in items:
            vector.append(int(item))
        fp.close()
    return vector

def GetVecList(dir, name_list):
    vec_list = []
    for name in name_list:
        vector = GetVec(dir, name)
        vec_list.append(vector)
    return vec_list

def GetVecListFromDic(dir, name_list):
    vec_list = []
    for name in name_list:
        vector = ReadJson(dir)[name]
        vec_list.append(vector)
    return vec_list

def GetLabelList(name_list, label_dic):
    label_list = []
    for name in name_list:
        aig_label = label_dic[name]
        assert(aig_label in method_list)
        label = method_list.index(aig_label)
        label_list.append(label)
    return label_list

def GetTimeList(name_list, label_dic):
    time_list = []
    for name in name_list:
        time = label_dic[name]
        time_list.append(time)
    return time_list

def NameMap(name):
    dic = {"pdr": "ABC-pdr", "dprove": "ABC-dprove", "iimc": "IImc", "IC3": "IC3ref"
        , "iimcbw": "bdd_bw_reach", "iimcfw": "bdd_fw_reach", "iimcic3": "ic3", "iimcic3lr": "ic3lr"}
    return dic[name]

