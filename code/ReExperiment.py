import utils
import numpy as np
import ClassifyGenerateLabel
import Classify
import matplotlib.pyplot as plt

def ReExperiment(layer, model_path, test_vec_list, test_name_list, test_label_list):
    model = utils.Load_pkl(model_path)
    predictions = model.predict_proba(test_vec_list)
    predict_label_list = np.argsort(-predictions, axis=1)
    print("layer " + layer)
    sum_acc = Classify.GetAcc(predict_label_list, test_label_list, utils.choose_top_method_number_1)
    print(sum_acc)
    sum_acc = Classify.GetAcc(predict_label_list, test_label_list, utils.choose_top_method_number_2)
    print(sum_acc)

if __name__ == '__main__':
    model_path_0 = utils.classify_model_path + "model_0.pkl"
    model_path_1 = utils.classify_model_path + "model_1.pkl"
    model_path_2 = utils.classify_model_path + "model_2.pkl"
    embedded_dir_0 = utils.embedded_dir_0
    embedded_dir_1 = utils.embedded_dir_1
    embedded_dir_2 = utils.embedded_dir_2
    test_name_list_path = utils.classify_basic_data_path + "test_name_list.json"
    test_label_dic_path = utils.classify_basic_data_path + "test_label_dic.json"
    test_name_list = utils.ReadJson(test_name_list_path)
    test_label_dic = utils.ReadJson(test_label_dic_path)
    test_vec_list_0 = utils.GetVecList(embedded_dir_0, test_name_list)
    test_vec_list_1 = utils.GetVecList(embedded_dir_1, test_name_list)
    test_vec_list_2 = utils.GetVecList(embedded_dir_2, test_name_list)

    test_label_list = utils.GetLabelList(test_name_list, test_label_dic)

    layer_0 = "0"
    layer_1 = "1"
    layer_2 = "2"

    ReExperiment(layer_0, model_path_0, test_vec_list_0, test_name_list, test_label_list)
    ReExperiment(layer_1, model_path_1, test_vec_list_1, test_name_list, test_label_list)
    ReExperiment(layer_2, model_path_2, test_vec_list_2, test_name_list, test_label_list)


    
    
