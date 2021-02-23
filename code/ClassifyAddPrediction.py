import csv
import utils
import sys
import random

def ClassifyAddCol(data, name_list, classify_predict_path, choose_top_method_number):
    method_list = utils.method_list
    predict = utils.ReadJson(classify_predict_path)
    statistic_dic = utils.InitialDic()
    for index in range(len(data)):
        target_method_list = predict[name_list[index]]
        predict_time = "None"
        point = 0
        for i in range(choose_top_method_number):
            target_method = target_method_list[i]
            assert(target_method in method_list)
            temp_point = method_list.index(target_method) + 1
            temp_time = data[index][temp_point]
            if predict_time == "None":
                predict_time = temp_time
                point = temp_point
            elif temp_time != "timeout" and temp_time != "failed" and temp_time != "0.0" and temp_time != "0":
                if predict_time == "timeout" or predict_time == "failed" or predict_time == "0.0" or predict_time == "0":
                    predict_time = temp_time
                    point = temp_point
                elif float(temp_time) < float(predict_time):
                    predict_time = temp_time
                    point = temp_point                
        data[index].append(predict_time)
        statistic_dic[method_list[point - 1]] += 1
    return data

def ClassifyAddPrediction(data_path, name_list_path, predict_data_path, 
                        classify_predict_path_0, classify_predict_path_1, classify_predict_path_2):
    with open(data_path, newline='') as csvfile:
        data = list(csv.reader(csvfile))

    method_list = utils.method_list
    name_list = utils.ReadJson(name_list_path)
    for set_predict_path in [classify_predict_path_0, classify_predict_path_1, classify_predict_path_2]:
        data = ClassifyAddCol(data, name_list, set_predict_path, utils.choose_top_method_number_1)
    for set_predict_path in [classify_predict_path_0, classify_predict_path_1, classify_predict_path_2]:
        data = ClassifyAddCol(data, name_list, set_predict_path, utils.choose_top_method_number_2)    

    for index in range(len(data)):
        predict_time = "timeout"
        for method in method_list:
            temp_point = method_list.index(method) + 1
            temp_time = data[index][temp_point]
            if temp_time != "timeout" and temp_time != "failed" and temp_time != "0.0" and temp_time != "0":
                if predict_time == "timeout":
                    predict_time = temp_time
                elif float(temp_time) < float(predict_time):
                    predict_time = temp_time
        data[index].append(predict_time)

    correct_num = 0
    for index in range(len(data)):
        random_point = random.randint(1, len(utils.method_list))
        random_predict = data[index][random_point]
        if random_predict == data[index][-1]:
            correct_num += 1
        data[index].append(random_predict)
    print("Random Acc top1")
    print(correct_num / len(data))

    correct_num = 0
    for index in range(len(data)):
        point_candidate = [1, 2, 3, 4]
        random_point_list = random.sample(point_candidate, utils.choose_top_method_number_2)
        random_predict = "timeout"
        for point in random_point_list:
            temp_time = data[index][point]
            if temp_time != "timeout" and temp_time != "failed" and temp_time != "0.0" and temp_time != "0":
                if random_predict == "timeout":
                    random_predict = temp_time
                elif float(temp_time) < float(random_predict):
                    random_predict = temp_time
        if random_predict == data[index][-2]:
            correct_num += 1
        data[index].append(random_predict)
    print("Random Acc top2")
    print(correct_num / len(data))

    title = "filename"
    for method in method_list:
        title = title + "," + method
    for encoding_layer in utils.encoding_layer_list:
        title = title + "," + "top1_" + encoding_layer
    for encoding_layer in utils.encoding_layer_list:
        title = title + "," + "top2_" + encoding_layer
    title = title + ",Ground Truth,Random Top1,Random Top2"
    with open(predict_data_path, "w") as writer:
        writer.write(title + "\n")
        for line in data:
            writer.write(",".join(line) + "\n")

def GeneratePrediction(name_list_path, classify_predict, layer):
    name_list = utils.ReadJson(name_list_path)
    title = "filename,predict"
    data = []
    for name in name_list:
        line = []
        line.append(name)
        line.append(classify_predict[name][0])
        data.append(line)
    with open(utils.classify_predict_path + "predict_" + str(layer) + ".csv", "w") as writer:
        writer.write(title + "\n")
        for line in data:
            writer.write(",".join(line) + "\n")



if __name__ == '__main__':
    classify_predict_path = utils.classify_predict_path
    classify_predict_path_0 = classify_predict_path + "classify_predict_0.json"
    classify_predict_path_1 = classify_predict_path + "classify_predict_1.json"
    classify_predict_path_2 = classify_predict_path + "classify_predict_2.json"
    # classify_train_predict_path_0 = classify_predict_path + "classify_train_predict_0.json"
    # classify_train_predict_path_1 = classify_predict_path + "classify_train_predict_1.json"
    # classify_train_predict_path_2 = classify_predict_path + "classify_train_predict_2.json"
    

    classify_basic_data_path = utils.classify_basic_data_path
    test_name_list_path = classify_basic_data_path + "test_name_list.json"
    test_data_path = classify_basic_data_path + "test_data.csv"
    predict_data_path = classify_basic_data_path + "classify_predict_data.csv"
    # train_name_list_path = classify_basic_data_path + "train_name_list.json"
    # train_data_path = classify_basic_data_path + "train_data.csv"
    # train_predict_data_path = classify_basic_data_path + "classify_train_predict_data.csv"

    # print("train")
    # ClassifyAddPrediction(train_data_path, train_name_list_path, train_predict_data_path, 
    #                         classify_train_predict_path_0, classify_train_predict_path_1, classify_train_predict_path_2)
    # print("test")
    ClassifyAddPrediction(test_data_path, test_name_list_path, predict_data_path, 
                            classify_predict_path_0, classify_predict_path_1, classify_predict_path_2)


