import csv
import utils
import sys

def GeneratePrediction(name_list_path, time_predict, layer, method):
    name_list = utils.ReadJson(name_list_path)
    title = "filename,predict"
    data = []
    for name in name_list:
        line = []
        line.append(name)
        line.append(str(time_predict[name_list.index(name)]))
        data.append(line)
    with open(utils.time_predict_path + "predict_" + method + "_" + str(layer) + ".csv", "w") as writer:
        writer.write(title + "\n")
        for line in data:
            writer.write(",".join(line) + "\n")




if __name__ == '__main__':
    time_predict_path = utils.time_predict_path
    time_predict_path_0 = time_predict_path + "time_predict_0.json"
    time_predict_path_1 = time_predict_path + "time_predict_1.json"
    time_predict_path_2 = time_predict_path + "time_predict_2.json"

    time_basic_data_path = utils.time_basic_data_path
    test_name_list_path = time_basic_data_path + "test_name_list.json"
    test_data_path = time_basic_data_path + "test_data.csv"
    predict_data_path = time_basic_data_path + "time_predict_data.csv"

    with open(test_data_path, newline='') as csvfile:
        data = list(csv.reader(csvfile))

    test_name_list = utils.ReadJson(test_name_list_path)
    method_list = utils.method_list
    for test_set_predict_path in [time_predict_path_0, time_predict_path_1, time_predict_path_2]:
        predict = utils.ReadJson(test_set_predict_path)
        for method in method_list:
            time_list = predict[method]
            for index in range(len(data)):        
                data[index].append(str(time_list[index]))

    for index in range(len(data)):
        predict_time = "timeout"
        for i in range(len(utils.method_list)):
            temp_point = i + 1
            temp_time = data[index][temp_point]
            if temp_time != "timeout" and temp_time != "failed" and temp_time != "0.0":
                if predict_time == "timeout":
                    predict_time = temp_time
                elif float(temp_time) < float(predict_time):
                    predict_time = temp_time
        data[index].append(predict_time)
        
    title = "filename"
    for method in method_list:
        title = title + "," + method
    for i in range(3):
        for method in method_list:
            title = title + "," + method + "_" + str(i)
    with open(predict_data_path, "w") as writer:
        writer.write(title + ",GroundTruth\n")
        for line in data:
            writer.write(",".join(line) + "\n")