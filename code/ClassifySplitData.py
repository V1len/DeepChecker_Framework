import csv
from sklearn.model_selection import train_test_split
import utils

def SplitData(data_path, train_data_path, test_data_path):
    with open(data_path, "r") as csvfile:
        data = list(csv.reader(csvfile))
        print(len(data) - 1)
    title = data[0]
    new_data = data[1:]

    train_data, test_data = train_test_split(new_data, test_size=0.2)
    print(len(train_data))
    print(len(test_data))

    with open(train_data_path, 'w')as writer:
        writer.write(",".join(title) + "\n")
        for line in train_data:
            writer.write(",".join(line) + "\n")
    with open(test_data_path, 'w')as writer:
        writer.write(",".join(title) + "\n")
        for line in test_data:
            writer.write(",".join(line) + "\n")


if __name__ == '__main__':
    classify_basic_data_path = utils.classify_basic_data_path

    data_path = classify_basic_data_path + "data.csv"
    train_data_path = classify_basic_data_path + "train_data.csv"
    test_data_path = classify_basic_data_path + "test_data.csv"

    SplitData(data_path, train_data_path, test_data_path)