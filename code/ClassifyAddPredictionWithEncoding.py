import utils
import csv


def ClassifyAddPredictionWithEncoding(predict_data_path, predict_data_with_encoding_path,
                                     encoding_time_path_0, encoding_time_path_1, encoding_time_path_2):
    with open(predict_data_path, newline='') as csvfile:
        data = list(csv.reader(csvfile))
    title_list = data[0]
    data = data[1:]
    
    encoding_time_path_list = [encoding_time_path_0, encoding_time_path_1, encoding_time_path_2]
    for i in range(len(encoding_time_path_list)):
        encoding_time_path = encoding_time_path_list[i]
        encoding_time_dic = utils.ReadJson(encoding_time_path)
        for index in range(len(data)):
            name = data[index][0].split(".aig")[0]
            encoding_time = encoding_time_dic[name]
            predict_time = data[index][i + 5]            
            if predict_time != "timeout" and predict_time != "failed" and predict_time != "0.0" and predict_time != "0":
                total_time = str(encoding_time + float(predict_time))
            else:
                total_time = "timeout"
            data[index].append(total_time)


    title = ",".join(title_list)
    for encoding_layer in utils.encoding_layer_list:
        title = title + "," + "AddEncoding_" + encoding_layer
    with open(predict_data_with_encoding_path, "w") as writer:
        writer.write(title + "\n")
        for line in data:
            writer.write(",".join(line) + "\n")

if __name__ == '__main__':
    classify_basic_data_path = utils.classify_basic_data_path
    predict_data_path = classify_basic_data_path + "classify_predict_data.csv"
    predict_data_with_encoding_path = classify_basic_data_path + "classify_predict_data_with_encoding.csv"

    encoding_time_path_0 = utils.classify_basic_data_path + "encoding_time_0.json"
    encoding_time_path_1 = utils.classify_basic_data_path + "encoding_time_1.json"
    encoding_time_path_2 = utils.classify_basic_data_path + "encoding_time_2.json"

    ClassifyAddPredictionWithEncoding(predict_data_path, predict_data_with_encoding_path,
                                     encoding_time_path_0, encoding_time_path_1, encoding_time_path_2)