import json
import pickle
import os

use_all_methods = True

if use_all_methods:
    method_list = ["dprove", "pdr", "iimc", "IC3"]
else:
    method_list = ["iimcbw", "iimcfw", "iimcic3", "iimcic3lr"]

encoding_layer_list = ["0-depth Encoding", "1-depth Encoding", "2-depth Encoding"]

choose_top_method_number_1 = 1
choose_top_method_number_2 = 2
sum_method_number = len(method_list)

date = "2021-1-26-best-classify"
# date = "2021-1-26-time"
# date = "2021-1-29"

root_path = "/mnt/hd0/DeepChecker/DataForNet/" + date + "/"
if not os.path.exists(root_path):
    os.mkdir(root_path)

tools_path = root_path + "tools/"
iimc_path = root_path + "iimc/"
if not os.path.exists(tools_path):
    os.mkdir(tools_path)
if not os.path.exists(iimc_path):
    os.mkdir(iimc_path)

if use_all_methods:
    basic_path = tools_path
else:
    basic_path = iimc_path

classify_task_path = basic_path + "classify/"
time_task_path = basic_path + "time/"
if not os.path.exists(classify_task_path):
    os.mkdir(classify_task_path)
if not os.path.exists(time_task_path):
    os.mkdir(time_task_path)

classify_model_path = classify_task_path + "classify_model/"
classify_predict_path = classify_task_path + "classify_predict/"
importance_message_path = classify_task_path + "importance_message/"
importance_fig_path = classify_task_path + "importance_figure/"
statistic_sample_distribution_path = classify_task_path + "statistic_sample_distribution/"
classify_basic_data_path = classify_task_path + "basic_data/"
classify_result_path = classify_task_path + "result/"

time_model_path = time_task_path + "time_model/"
time_predict_path = time_task_path + "time_predict/"
time_basic_data_path = time_task_path + "basic_data/"
time_result_path = time_task_path + "result/"

path_list = [classify_model_path, classify_predict_path, importance_message_path, importance_fig_path,
                    statistic_sample_distribution_path, classify_basic_data_path, classify_result_path,
                            time_model_path, time_predict_path, time_basic_data_path, time_result_path]
for temp_path in path_list:
    if not os.path.exists(temp_path):
        os.mkdir(temp_path)

# AVY_dprove_path = "/mnt/hd0/DeepChecker/dataset/2021-1-6/AVY_dprove_clean.json"
# AVY_dprove_path = "/mnt/hd0/DeepChecker/DataForNet/2021-1-10/data_clean.json"
AVY_dprove_path = "/mnt/hd0/DeepChecker/dataset/2020-1-18/AVY_dprove_clean.json"
pdr_IC3_path = "/mnt/hd0/DeepChecker/dataset/2020-1-18/pdr_IC3_clean.json"
# iimc_path = "/mnt/hd0/DeepChecker/dataset/2020-1-18/iimc_clean.json"
iimc_path = "/mnt/hd0/DeepChecker/dataset/2020-1-26/clean_iimc.json"
others_path = "/mnt/hd0/DeepChecker/dataset/2020-1-12/others.json"
hwmcc_clean_path = "/mnt/hd0/DeepChecker/dataset/2020-1-22/hwmcc_clean.json"

# iimc_benchmark_path = "/mnt/hd0/DeepChecker/dataset/2021-1-8/iimc_benchmark.json"
iimc_benchmark_path = "/mnt/hd0/DeepChecker/dataset/2021-1-19/iimc_benchmark.json"
new_format_json_path = "/mnt/hd0/DeepChecker/new_format.json"

encoding_log_path_0 = "/mnt/hd0/DeepChecker/StatisticAvgEncodingTime/embedding_0.log"
encoding_log_path_1 = "/mnt/hd0/DeepChecker/StatisticAvgEncodingTime/embedding_1.log"
encoding_log_path_2 = "/mnt/hd0/DeepChecker/StatisticAvgEncodingTime/embedding_2.log"
encoding_aig_path = "/mnt/hd0/DeepChecker/StatisticAvgEncodingTime/networks/"
encoding_aag_path = "/mnt/hd0/DeepChecker/networks_aag/"


embedding_date_0 = "2021-1-2_v0.1"
embedding_date_1 = "2020-12-24_v1.1"
# embedding_date_2 = "2021-1-2_v2.2"

embedding_date_2 = "2020-1-28_v2.2"

# embedding_date_0 = "2020-12-11_v0"
# embedding_date_1 = "2020-12-24_v1.1"
# embedding_date_2 = "2020-12-24_v2.1"

embedded_dir_0 = "/mnt/hd0/DeepChecker/embedding/embedded/" + embedding_date_0
embedded_dir_1 = "/mnt/hd0/DeepChecker/embedding/embedded/" + embedding_date_1
embedded_dir_2 = "/mnt/hd0/DeepChecker/embedding/embedded/" + embedding_date_2


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

def GetLabelList(name_list, label_dic):
    label_list = []
    for name in name_list:
        aig_label = label_dic[name]
        assert(aig_label in method_list)
        label = method_list.index(aig_label)
        label_list.append(label)
    return label_list

def NameMap(name):
    dic = {"pdr": "ABC-pdr", "dprove": "ABC-dprove", "iimc": "IImc", "IC3": "IC3ref"
        , "iimcbw": "bdd_bw_reach", "iimcfw": "bdd_fw_reach", "iimcic3": "ic3", "iimcic3lr": "ic3lr"}
    return dic[name]

