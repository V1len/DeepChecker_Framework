import utils
import DNNStructure
import torch
from torch import optim
import time
from torch.utils.data import DataLoader

if __name__ == '__main__':
    use_all_methods = utils.use_all_methods

    embedded_dir_0 = utils.embedded_dir_0
    embedded_dir_1 = utils.embedded_dir_1
    embedded_dir_2 = utils.embedded_dir_2
    embedded_dir_list = [embedded_dir_0, embedded_dir_1, embedded_dir_2]

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
    classify_predict_path_0 = classify_predict_path + "DNN_predict_0.json"
    classify_predict_path_1 = classify_predict_path + "DNN_predict_1.json"
    classify_predict_path_2 = classify_predict_path + "DNN_predict_2.json"

    classify_model_path = utils.classify_model_path
    classify_model_path_0 = classify_model_path + "DNN_model_0.pkl"
    classify_model_path_1 = classify_model_path + "DNN_model_1.pkl"
    classify_model_path_2 = classify_model_path + "DNN_model_2.pkl"

    for i in range(len(utils.encoding_layer_list)):
        train_vec_list = utils.GetVecList(embedded_dir_list[i], train_name_list)
        test_vec_list = utils.GetVecList(embedded_dir_list[i], test_name_list)
        input_length = len(train_vec_list[0])

        epochs = 500
        loss_func = torch.nn.CrossEntropyLoss().cuda()
        net = DNNStructure.ClassifyNet(input_length).cuda()
        lr = 1e-4
        optimizer = optim.Adam(net.parameters(), lr=lr, betas=(0.9, 0.999), eps=1e-7, weight_decay=0)
        DNNStructure.initNetParams(net)
        net.eval()

        prev_time = time.time()
        best_acc = 0
        best_epoch = 0
        for epoch in range(epochs):
            net.train()
            for i, (_, vector, label) in enumerate(train_loader):
                net.train()
                vector = vector.cuda()
                label = label.cuda()
                pred = net(vector)
                loss = loss_func(pred, label)
                # print(loss)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
            net.eval()