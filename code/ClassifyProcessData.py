import utils
import copy

def FormerProcessData(others_path, data_path, AVY_dprove_path=""):
    method_list = utils.method_list

    others_list = utils.ReadJson(others_path)
    others_dic = {}
    for i in range(len(others_list)):
        aig = others_list[i]
        aig_name = list(aig.keys())[0]
        run_times = aig[aig_name]
        temp_dic = {}
        for method_time_pair in run_times:
            method = list(method_time_pair.keys())[0]
            time = str(method_time_pair[method])
            temp_dic[method] = time
        others_dic[aig_name] = temp_dic
    others_name_list = list(others_dic.keys())
    # print(len(others_name_list))

    AVY_dprove_name_list = []
    AVY_dprove_dic = {}
    if AVY_dprove_path != "":
        AVY_dprove_dic = utils.ReadJson(AVY_dprove_path)
        AVY_dprove_name_list = list(AVY_dprove_dic.keys())
        # print(len(AVY_dprove_name_list))

    data_list = []
    if AVY_dprove_path != "":
        others_method_list = copy.deepcopy(method_list)
        others_method_list.remove("dprove")
        for name in AVY_dprove_name_list:
            if all(keyword in others_dic[name].keys() for keyword in others_method_list):
                temp_data = [name, AVY_dprove_dic[name]["dprove"]]
                for method in others_method_list:
                    temp_data.append(others_dic[name][method])
                mark = False
                for time in temp_data[1:]:
                    if time != "timeout" and time != "failed" and time != "0.0":
                        mark = True
                if mark == True:
                    data_list.append(temp_data)
    else:
        for name in others_name_list:
            if all(keyword in others_dic[name].keys() for keyword in method_list):
                temp_data = [name]
                for method in method_list:
                    temp_data.append(others_dic[name][method])
                mark = False
                for time in temp_data[1:]:
                    if time != "timeout" and time != "failed" and time != "0.0":
                        mark = True
                if mark == True:
                    data_list.append(temp_data)
    title = "filename"
    for method in method_list:
        title = title + "," + method
    with open(data_path, "w") as writer:
        writer.write(title + "\n")
        for line in data_list:
            writer.write(",".join(line) + "\n")

def ProcessData(AVY_dprove_path, pdr_IC3_path, others_path, data_path):
    method_list = utils.method_list

    AVY_dprove_dic = utils.ReadJson(AVY_dprove_path)

    pdr_IC3_dic = utils.ReadJson(pdr_IC3_path)
    pdr_IC3_name_list = list(pdr_IC3_dic.keys())

    others_list = utils.ReadJson(others_path)
    others_dic = {}
    for i in range(len(others_list)):
        aig = others_list[i]
        aig_name = list(aig.keys())[0]
        run_times = aig[aig_name]
        temp_dic = {}
        for method_time_pair in run_times:
            method = list(method_time_pair.keys())[0]
            time = str(method_time_pair[method])
            temp_dic[method] = time
        others_dic[aig_name] = temp_dic

    data_list = []
    for name in pdr_IC3_name_list:
        temp_data = [name]
        temp_data.append(AVY_dprove_dic[name]["dprove"])
        temp_data.append(pdr_IC3_dic[name]["pdr"])
        temp_data.append(others_dic[name]["iimc"])
        temp_data.append(pdr_IC3_dic[name]["IC3"])

        mark = False
        for time in temp_data[1:]:
            if time != "timeout" and time != "failed" and time != "0.0" and time != "0":
                mark = True
        if mark == True:
            data_list.append(temp_data)
    
    title = "filename"
    for method in method_list:
        title = title + "," + method
    with open(data_path, "w") as writer:
        writer.write(title + "\n")
        for line in data_list:
            writer.write(",".join(line) + "\n")

def ProcessDataForBenchmark(AVY_dprove_path, pdr_IC3_path, others_path, hwmcc_clean_path, train_path, test_path):
    AVY_dprove_dic = utils.ReadJson(AVY_dprove_path)

    pdr_IC3_dic = utils.ReadJson(pdr_IC3_path)
    train_name_list = list(pdr_IC3_dic.keys())

    others_list = utils.ReadJson(others_path)
    others_dic = {}
    for i in range(len(others_list)):
        aig = others_list[i]
        aig_name = list(aig.keys())[0]
        run_times = aig[aig_name]
        temp_dic = {}
        for method_time_pair in run_times:
            method = list(method_time_pair.keys())[0]
            time = str(method_time_pair[method])
            temp_dic[method] = time
        others_dic[aig_name] = temp_dic

    hwmcc_dic = utils.ReadJson(hwmcc_clean_path)
    test_name_list = list(hwmcc_dic.keys())
    print(len(train_name_list))
    print(len(test_name_list))
    train_name_list = list(set(train_name_list) - set(test_name_list))
    print(len(train_name_list))

    data_list = []
    for name in train_name_list:
        temp_data = [name]
        temp_data.append(AVY_dprove_dic[name]["dprove"])
        temp_data.append(pdr_IC3_dic[name]["pdr"])
        temp_data.append(others_dic[name]["iimc"])
        temp_data.append(pdr_IC3_dic[name]["IC3"])

        mark = False
        for time in temp_data[1:]:
            if time != "timeout" and time != "failed" and time != "0.0" and time != "0":
                mark = True
        if mark == True:
            data_list.append(temp_data)

    with open(train_path, "w") as writer:
        for line in data_list:
            writer.write(",".join(line) + "\n")

    data_list = []
    for name in test_name_list:
        temp_data = [name]
        temp_data.append(hwmcc_dic[name]["dprove"])
        temp_data.append(hwmcc_dic[name]["pdr"])
        temp_data.append(hwmcc_dic[name]["iimc"])
        temp_data.append(hwmcc_dic[name]["IC3"])

        mark = False
        for time in temp_data[1:]:
            if time != "timeout" and time != "failed" and time != "0.0" and time != "0":
                mark = True
        if mark == True:
            data_list.append(temp_data)

    with open(test_path, "w") as writer:
        for line in data_list:
            writer.write(",".join(line) + "\n")

def FinalProcessData(AVY_dprove_path, pdr_IC3_path, iimc_path, data_path):
    method_list = utils.method_list

    AVY_dprove_dic = utils.ReadJson(AVY_dprove_path)

    pdr_IC3_dic = utils.ReadJson(pdr_IC3_path)
    pdr_IC3_name_list = list(pdr_IC3_dic.keys())

    iimc_dic = utils.ReadJson(iimc_path)

    data_list = []
    for name in pdr_IC3_name_list:
        temp_data = [name]
        temp_data.append(AVY_dprove_dic[name]["dprove"])
        temp_data.append(pdr_IC3_dic[name]["pdr"])
        temp_data.append(iimc_dic[name]["iimc"])
        temp_data.append(pdr_IC3_dic[name]["IC3"])

        mark = False
        for time in temp_data[1:]:
            if time != "timeout" and time != "failed" and time != "0.0":
                mark = True
        if mark == True:
            data_list.append(temp_data)
    
    title = "filename"
    for method in method_list:
        title = title + "," + method
    with open(data_path, "w") as writer:
        writer.write(title + "\n")
        for line in data_list:
            writer.write(",".join(line) + "\n")

def ProcessiimcData(iimc_path, data_path):
    method_list = utils.method_list

    iimc_dic = utils.ReadJson(iimc_path)
    iimc_name_list = list(iimc_dic.keys())
    # print(len(iimc_name_list))

    data_list = []
    for name in iimc_name_list:
        if all(keyword in iimc_dic[name].keys() for keyword in method_list):
            time_list = []
            for method in method_list:
                time_list.append(iimc_dic[name][method])
            mark = False
            for time in time_list:
                if time != "timeout" and time != "failed" and time != "0.0" and time != "0":
                    mark = True
            if mark == True:
                temp_data = [name]
                for method in method_list:
                    temp_data.append(iimc_dic[name][method])
                data_list.append(temp_data)

    title = "filename"
    for method in method_list:
        title = title + "," + method
    with open(data_path, "w") as writer:
        writer.write(title + ",DeepChecker\n")
        for line in data_list:
            writer.write(",".join(line) + "\n")


if __name__ == '__main__':
    AVY_dprove_path = utils.AVY_dprove_path
    pdr_IC3_path = utils.pdr_IC3_path
    others_path = utils.others_path
    iimc_path = utils.iimc_path
    iimc_benchmark_path = utils.iimc_benchmark_path
    hwmcc_clean_path = utils.hwmcc_clean_path

    data_path = utils.classify_basic_data_path + "data.csv"
    # train_path = utils.classify_basic_data_path + "train_data.csv"
    # test_path = utils.classify_basic_data_path + "test_data.csv"

    if utils.use_all_methods:
        # ProcessDataForBenchmark(AVY_dprove_path, pdr_IC3_path, others_path, hwmcc_clean_path, train_path, test_path)
        ProcessData(AVY_dprove_path, pdr_IC3_path, others_path, data_path)
        # FinalProcessData(AVY_dprove_path, pdr_IC3_path, iimc_path, data_path)
    else:
        ProcessiimcData(iimc_benchmark_path, data_path)

    # ProcessData(AVY_dprove_path, pdr_IC3_path, others_path, data_path)
    # FinalProcessData(AVY_dprove_path, pdr_IC3_path, iimc_path, data_path)
    # FormerProcessData(others_path, data_path, AVY_dprove_path=AVY_dprove_path)
