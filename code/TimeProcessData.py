import utils
import copy

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

    data_path = utils.time_basic_data_path + "data.csv"

    if utils.use_all_methods:
        ProcessData(AVY_dprove_path, pdr_IC3_path, others_path, data_path)
    else:
        ProcessiimcData(iimc_benchmark_path, data_path)

