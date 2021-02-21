from sklearn.ensemble import RandomForestClassifier
import utils
import os
import numpy as np
import pydotplus
from sklearn import tree
from sklearn.model_selection import GridSearchCV

np.seterr(divide='ignore',invalid='ignore')

from sklearn.model_selection import GridSearchCV
from sklearn import metrics

def GeneratePredictResult(test_name_list, predict_label_list, classify_predict_path):
    classify_predict = {}
    method_list = utils.method_list
    for i in range(len(test_name_list)):
        test_name = test_name_list[i]
        temp_predict = []
        for predict in predict_label_list[i]:
            temp_predict.append(method_list[predict])
        classify_predict[test_name] = temp_predict
    utils.WriteJson(classify_predict, classify_predict_path)


    method_list = utils.method_list
    choose_top_method_number = utils.choose_top_method_number_1
    for i in range(choose_top_method_number):
        top_i_method_dic = {}
        for j in range(len(test_name_list)):
            test_name = test_name_list[j]
            top_i_method_dic[test_name] = classify_predict[test_name][i]
        statistic_dic = utils.Statistic([top_i_method_dic])
        print(statistic_dic)

    return classify_predict

def GetAcc(predict_label_list, test_label_list, choose_top_method_number):
    sum_acc = 0
    for i in range(choose_top_method_number):
        acc = (predict_label_list[:, i] == test_label_list).sum() / len(test_label_list)
        sum_acc += acc
    return sum_acc
    
def RandomForest(layer, embedded_dir, train_name_list, test_name_list, train_label_list, test_label_list, classify_predict_path,
                 classify_train_predict_path, model_path, importance_path, 
                 max_depth, max_leaf_nodes, min_samples_split=2, min_samples_leaf=1):
    train_vec_list = utils.GetVecList(embedded_dir, train_name_list)
    test_vec_list = utils.GetVecList(embedded_dir, test_name_list)

    model = RandomForestClassifier(n_estimators=100, criterion="entropy", max_depth=None, min_samples_split=min_samples_split, 
                                    min_samples_leaf=min_samples_leaf, max_leaf_nodes=max_leaf_nodes, max_features=None)
    classifier = model.fit(train_vec_list, train_label_list)
    utils.Save_pkl(classifier, model_path)
    

    predictions = classifier.predict_proba(test_vec_list)
    predict_label_list = np.argsort(-predictions, axis=1)
    importance = model.feature_importances_
    utils.WriteJson(importance.tolist(), importance_path)
    print("layer " + layer)
    sum_acc = GetAcc(predict_label_list, test_label_list, utils.choose_top_method_number_1)
    print(sum_acc)
    sum_acc = GetAcc(predict_label_list, test_label_list, utils.choose_top_method_number_2)
    print(sum_acc)
    classify_predict = GeneratePredictResult(test_name_list, predict_label_list, classify_predict_path)



if __name__ == '__main__':
    use_all_methods = utils.use_all_methods

    embedded_dir_0 = utils.embedded_dir_0
    embedded_dir_1 = utils.embedded_dir_1
    embedded_dir_2 = utils.embedded_dir_2

    classify_basic_data_path = utils.classify_basic_data_path
    train_name_list_path = classify_basic_data_path + "train_name_list.json"
    train_label_dic_path = classify_basic_data_path + "train_label_dic.json"
    test_name_list_path = classify_basic_data_path + "test_name_list.json"
    test_label_dic_path = classify_basic_data_path + "test_label_dic.json"

    train_name_list = utils.ReadJson(train_name_list_path)
    train_label_dic = utils.ReadJson(train_label_dic_path)
    test_name_list = utils.ReadJson(test_name_list_path)
    test_label_dic = utils.ReadJson(test_label_dic_path)

    train_label_list = utils.GetLabelList(train_name_list, train_label_dic)
    test_label_list = utils.GetLabelList(test_name_list, test_label_dic)

    classify_predict_path = utils.classify_predict_path
    classify_predict_path_0 = classify_predict_path + "classify_predict_0.json"
    classify_predict_path_1 = classify_predict_path + "classify_predict_1.json"
    classify_predict_path_2 = classify_predict_path + "classify_predict_2.json"
    classify_train_predict_path_0 = classify_predict_path + "classify_train_predict_0.json"
    classify_train_predict_path_1 = classify_predict_path + "classify_train_predict_1.json"
    classify_train_predict_path_2 = classify_predict_path + "classify_train_predict_2.json"

    classify_model_path = utils.classify_model_path
    classify_model_path_0 = classify_model_path + "model_0.pkl"
    classify_model_path_1 = classify_model_path + "model_1.pkl"
    classify_model_path_2 = classify_model_path + "model_2.pkl"
    
    importance_message_path = utils.importance_message_path
    importance_path_0 = importance_message_path + "importance_0.json"
    importance_path_1 = importance_message_path + "importance_1.json"
    importance_path_2 = importance_message_path + "importance_2.json"

    layer_0 = "0"
    layer_1 = "1"
    layer_2 = "2"

    if use_all_methods:
        RandomForest(layer_0, embedded_dir_0, train_name_list, test_name_list, train_label_list, test_label_list, 
                    classify_predict_path_0, classify_train_predict_path_0, classify_model_path_0, importance_path_0, 
                    max_depth=None, max_leaf_nodes=40, min_samples_split=40, min_samples_leaf=1)
        RandomForest(layer_1, embedded_dir_1, train_name_list, test_name_list, train_label_list, test_label_list, 
                    classify_predict_path_1, classify_train_predict_path_1, classify_model_path_1, importance_path_1, 
                    max_depth=None, max_leaf_nodes=80, min_samples_split=20, min_samples_leaf=1)
        RandomForest(layer_2, embedded_dir_2, train_name_list, test_name_list, train_label_list, test_label_list, 
                    classify_predict_path_2, classify_train_predict_path_2, classify_model_path_2, importance_path_2, 
                    max_depth=None, max_leaf_nodes=120, min_samples_split=10, min_samples_leaf=1)
    else:
        RandomForest(layer_0, embedded_dir_0, train_name_list, test_name_list, train_label_list, test_label_list, classify_predict_path_0, classify_train_predict_path_0, classify_model_path_0, importance_path_0, max_depth=3, max_leaf_nodes=30, min_samples_split=3, min_samples_leaf=1)
        RandomForest(layer_1, embedded_dir_1, train_name_list, test_name_list, train_label_list, test_label_list, classify_predict_path_1, classify_train_predict_path_1, classify_model_path_1, importance_path_1, max_depth=4, max_leaf_nodes=30, min_samples_split=3, min_samples_leaf=1)
        RandomForest(layer_2, embedded_dir_2, train_name_list, test_name_list, train_label_list, test_label_list, classify_predict_path_2, classify_train_predict_path_2, classify_model_path_2, importance_path_2, max_depth=None, max_leaf_nodes=30, min_samples_split=3, min_samples_leaf=1)
 
