import utils
import numpy as np

if __name__ == '__main__':
    embedded_dir_2 = utils.embedded_dir_2

    train_name_list_path = utils.classify_basic_data_path + "train_name_list.json"
    test_name_list_path = utils.classify_basic_data_path + "test_name_list.json"
    train_name_list = utils.ReadJson(train_name_list_path)
    test_name_list = utils.ReadJson(test_name_list_path)

    train_vec_list = utils.GetVecList(embedded_dir_2, train_name_list)
    test_vec_list = utils.GetVecList(embedded_dir_2, test_name_list)

    train_statistic_vec = np.array(train_vec_list).sum(axis=0)
    test_statistic_vec = np.array(test_vec_list).sum(axis=0)
    print(train_statistic_vec)
    print(test_statistic_vec)
    for index in range(133, 161):
        if train_statistic_vec[index] != 0:
            print("train")
            print(index)
        if test_statistic_vec[index] != 0:
            print("test")
            print(index)