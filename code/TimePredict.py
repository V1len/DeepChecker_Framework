from sklearn.ensemble import RandomForestRegressor
import utils
import os
import numpy as np
from sklearn import tree
np.seterr(divide='ignore',invalid='ignore')

from sklearn.model_selection import GridSearchCV
from sklearn import metrics

def GetTimeList(name_list, time_message_dic, method):
    time_list = []
    for name in name_list:
        time = time_message_dic[name][method]
        time_list.append(time)
    return time_list

def RandomForest(embedded_dir, train_name_list, test_name_list, train_time_message, test_time_message,
                time_predict_path, layer, max_depth, min_samples_split=2, min_samples_leaf=1):
    time_model_path = utils.time_model_path
    train_vec_list = utils.GetVecList(embedded_dir, train_name_list)
    test_vec_list = utils.GetVecList(embedded_dir, test_name_list)
    time_predict_message = {}
    for method in utils.method_list:
        whole_time_model_path = time_model_path + method + "_model_" + layer + ".pkl"
        train_time_list = GetTimeList(train_name_list, train_time_message, method)
        test_time_list = GetTimeList(test_name_list, test_time_message, method)
        model = RandomForestRegressor(n_estimators=100, criterion="mae", max_depth=max_depth, min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf)
        model.fit(train_vec_list, train_time_list)
        utils.Save_pkl(model, whole_time_model_path)
        predict_time_list = model.predict(test_vec_list)
        time_predict_message[method] = predict_time_list.tolist()

        print("Traing Score:%f" % model.score(train_vec_list, train_time_list))
        print("Testing Score:%f" % model.score(test_vec_list, test_time_list))

    utils.WriteJson(time_predict_message, time_predict_path)

def TimePredict(name_list, time_dic, layer, n_estimators, max_depth, max_leaf_nodes, min_samples_split, min_samples_leaf, method):
    if layer == 0:
        encoding_dic_dir = utils.encoding_dic_dir_0
        model_path = utils.time_model_path + "model_" + method + "_0.pkl"
    elif layer == 1:
        encoding_dic_dir = utils.encoding_dic_dir_1
        model_path = utils.time_model_path + "model_" + method + "_1.pkl"
    elif layer == 2:
        encoding_dic_dir = utils.encoding_dic_dir_2
        model_path = utils.time_model_path + "model_" + method + "_2.pkl"
    vec_list = utils.GetVecListFromDic(encoding_dic_dir, name_list)
    model = RandomForestRegressor(n_estimators=n_estimators, criterion="mae", max_depth=max_depth, min_samples_split=min_samples_split,
                                    min_samples_leaf=min_samples_leaf, max_leaf_nodes=max_leaf_nodes, max_features=None)

    time_list = utils.GetTimeList(name_list, time_dic)
    classifier = model.fit(vec_list, time_list)
    utils.Save_pkl(classifier, model_path)

def Predict(name_list_path, model_path, layer, method):
    name_list = utils.ReadJson(name_list_path)
    if layer == 0:
        encoding_dic_dir = utils.encoding_dic_dir_0
    elif layer == 1:
        encoding_dic_dir = utils.encoding_dic_dir_1
    elif layer == 2:
        encoding_dic_dir = utils.encoding_dic_dir_2
    vec_list = utils.GetVecListFromDic(encoding_dic_dir, name_list)
    model = utils.Load_pkl(model_path)
    predict_time_list = model.predict(vec_list)
    time_predict = predict_time_list.tolist()
    time_predict_path = utils.time_predict_path + "predict_" + method + "_" + str(layer) + ".json"
    utils.WriteJson(time_predict, time_predict_path)
    return time_predict


if __name__ == '__main__':
    use_all_methods = utils.use_all_methods

    embedded_dir_0 = utils.embedded_dir_0
    embedded_dir_1 = utils.embedded_dir_1
    embedded_dir_2 = utils.embedded_dir_2

    time_basic_data_path = utils.time_basic_data_path
    train_name_list_path = time_basic_data_path + "train_name_list.json"
    train_time_message_path = time_basic_data_path + "train_time_message.json"
    test_name_list_path = time_basic_data_path + "test_name_list.json"
    test_time_message_path = time_basic_data_path + "test_time_message.json"

    train_name_list = utils.ReadJson(train_name_list_path)
    train_time_message = utils.ReadJson(train_time_message_path)
    test_name_list = utils.ReadJson(test_name_list_path)
    test_time_message = utils.ReadJson(test_time_message_path)

    time_predict_path = utils.time_predict_path
    time_predict_path_0 = time_predict_path + "time_predict_0.json"
    time_predict_path_1 = time_predict_path + "time_predict_1.json"
    time_predict_path_2 = time_predict_path + "time_predict_2.json"

    layer_0 = "0"
    layer_1 = "1"
    layer_2 = "2"

    if use_all_methods:
        print("0")
        RandomForest(embedded_dir_0, train_name_list, test_name_list, train_time_message, 
                    test_time_message, time_predict_path_0, layer_0, 
                    max_depth=None, min_samples_split=2, min_samples_leaf=1)
        print("1")
        RandomForest(embedded_dir_1, train_name_list, test_name_list, train_time_message, 
                    test_time_message, time_predict_path_1, layer_1, 
                    max_depth=None, min_samples_split=2, min_samples_leaf=1)
        print("2")
        RandomForest(embedded_dir_2, train_name_list, test_name_list, train_time_message, 
                    test_time_message, time_predict_path_2, layer_2, 
                    max_depth=None, min_samples_split=2, min_samples_leaf=1)
    else:
        RandomForest(embedded_dir_0, train_name_list, test_name_list, train_time_message, test_time_message, time_predict_path_0, layer_0, max_depth=3, min_samples_split=3, min_samples_leaf=1)
        RandomForest(embedded_dir_1, train_name_list, test_name_list, train_time_message, test_time_message, time_predict_path_1, layer_1, max_depth=4, min_samples_split=3, min_samples_leaf=1)
        RandomForest(embedded_dir_2, train_name_list, test_name_list, train_time_message, test_time_message, time_predict_path_2, layer_2, max_depth=None, min_samples_split=3, min_samples_leaf=1)
