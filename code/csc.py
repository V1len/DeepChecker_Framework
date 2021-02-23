import argparse
import utils
import sys
import os
import ClassifyGenerateLabel
import Classify
import ClassifyAddPrediction
import TimeGenerateLabel
import TimePredict
import TimeAddPrediction

def ArgParse():
    parser = argparse.ArgumentParser() 
    parser.add_argument('-f', '--function', type=str, choices=['classify', 'time'], help='choose function')
    parser.add_argument('-s', '--stage', type=str, choices=['train', 'test'], help='choose stage')
    parser.add_argument('-l', '--layer', type=int, choices=[0,1,2], default=1, help='layer of encoding')
    parser.add_argument('--n_estimators', type=int, default=100, help='num of estimators for random forest')
    parser.add_argument('--max_depth', type=int, default=None, help='max depth for random forest')
    parser.add_argument('--max_leaf_nodes', type=int, default=None, help='max number of leaf nodes for random forest')
    parser.add_argument('--min_samples_split', type=int, default=2, help='min number of samples for split for random forest')
    parser.add_argument('--min_samples_leaf', type=int, default=1, help='min number of samples in a leaf for random forest')
    parser.add_argument('--train_data_path', type=str, default='')
    parser.add_argument('--test_name_list_path', type=str, default='')
    parser.add_argument('--model_path', type=str, default='')
    parser.add_argument('-m', '--method', type=str, choices=['dprove', 'pdr', 'iimc', 'IC3'], help='method for time predict')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = ArgParse()

    # print(args.stage)
    # print(args.function)
    if args.function == "classify":
        utils.MakeClassifyDir()
        if args.stage == "train":
            if args.train_data_path == "":
                print("There is no path for train data!")
            # elif args.model_path == "":
            #     print("There is no path for model!")
            else:
                name_list, label_dic = ClassifyGenerateLabel.ClassifyGenerateLabel(args.train_data_path, args.stage)
                Classify.Classify(name_list, label_dic, args.layer, args.n_estimators,
                                 args.max_depth, args.max_leaf_nodes, args.min_samples_split, args.min_samples_leaf)

        elif args.stage == "test":
            if args.test_name_list_path == "":
                print("There is no path for test name list!")
            elif args.model_path == "" and not os.path.isfile(utils.classify_model_path + "model_" + str(args.layer) + ".pkl"):
                print("There is no model!")
            elif args.model_path != "" and not os.path.isfile(args.model_path):    
                print("There is no model!")
            else:
                if args.model_path == "":
                    model_path = utils.classify_model_path + "model_" + str(args.layer) + ".pkl"
                else:
                    model_path = args.model_path
                classify_predict = Classify.Predict(args.test_name_list_path, model_path, args.layer)
                ClassifyAddPrediction.GeneratePrediction(args.test_name_list_path, classify_predict, args.layer)

                
        
    elif args.function == "time":
        utils.MakeTimeDir()
        if args.stage == "train":
            if args.train_data_path == "":
                print("There is no path for train data!")
            elif args.method == None:
                print("There is no method!")
            else:
                name_list, time_dic, timeout_dic = TimeGenerateLabel.TimeGenerateLabel(args.train_data_path, args.stage, args.method)
                TimePredict.TimePredict(name_list, time_dic, args.layer, args.n_estimators,
                                 args.max_depth, args.max_leaf_nodes, args.min_samples_split, args.min_samples_leaf, args.method)

        elif args.stage == "test":
            if args.test_name_list_path == "":
                print("There is no path for test name list!")
            elif args.model_path == "" and not os.path.isfile(utils.time_model_path + "model_" + args.method + "_" + str(args.layer) + ".pkl"):
                print("There is no model!")
            elif args.model_path != "" and not os.path.isfile(args.model_path):    
                print("There is no model!")
            else:
                if args.model_path == "":
                    model_path = utils.time_model_path + "model_" + args.method + "_" + str(args.layer) + ".pkl"
                else:
                    model_path = args.model_path
                time_predict = TimePredict.Predict(args.test_name_list_path, model_path, args.layer, args.method)
                TimeAddPrediction.GeneratePrediction(args.test_name_list_path, time_predict, args.layer, args.method)
