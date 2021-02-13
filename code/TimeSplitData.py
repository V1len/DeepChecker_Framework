import csv
from sklearn.model_selection import train_test_split
import utils

def SplitData(data_path, train_data_path, test_data_path, new_format_json_path, remove_mark=False):
    with open(data_path, "r") as csvfile:
        data = list(csv.reader(csvfile))
        print(len(data))

    new_format = utils.ReadJson(new_format_json_path)
    new_data = []
    if remove_mark:
        for item in data[1:]:
            if item[0] not in new_format:
                new_data.append(item)
    else:
        new_data = data[1:]

    train_data, test_data = train_test_split(new_data, test_size=0.2)
    print(len(train_data))
    print(len(test_data))

    with open(train_data_path, 'w')as writer:
        for line in train_data:
            writer.write(",".join(line) + "\n")
    with open(test_data_path, 'w')as writer:
        for line in test_data:
            writer.write(",".join(line) + "\n")


if __name__ == '__main__':
    time_basic_data_path = utils.time_basic_data_path

    data_path = time_basic_data_path + "data.csv"
    train_data_path = time_basic_data_path + "train_data.csv"
    test_data_path = time_basic_data_path + "test_data.csv"
    new_format_json_path = utils.new_format_json_path

    SplitData(data_path, train_data_path, test_data_path, new_format_json_path, remove_mark=True)