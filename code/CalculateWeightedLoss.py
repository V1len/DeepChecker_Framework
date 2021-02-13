import utils
import csv

def CalculateWeightedLoss(predict_data_path):
    with open(predict_data_path, newline='') as csvfile:
        data = list(csv.reader(csvfile))
    titles = data[0]
    index_list = [5, 6, 7, 8, 9, 10, 12, 13]
    data = data[1:]
    test_num = len(data)
    for index in index_list:
        title = titles[index]
        print(title)
        sum_weighted_loss = 0.0
        for line in data:
            predict_time = line[index]
            truth_time = line[11]
            if predict_time == "failed" or predict_time == "timeout" or predict_time == "0.0":
                sum_weighted_loss += (3600.0 - float(truth_time))
            else:
                sum_weighted_loss += (float(predict_time)- float(truth_time))
        print(sum_weighted_loss / test_num)


if __name__ == '__main__':
    classify_basic_data_path = utils.classify_basic_data_path
    # train_predict_data_path = classify_basic_data_path + "classify_train_predict_data.csv"
    predict_data_path = classify_basic_data_path + "classify_predict_data.csv"

    # print("train")
    # CalculateWeightedLoss(train_predict_data_path)
    # print("test")
    CalculateWeightedLoss(predict_data_path)
    



    

                
