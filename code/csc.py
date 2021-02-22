import argparse
import utils
import sys
import ClassifyGenerateLabel
import Classify

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
    parser.add_argument('--train_data_path', type=str, default="")
    parser.add_argument('--model_path', type=str, default=utils.classify_model_path + "model.pkl")
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
            if args.test_data_path == "":
                print("There is no path for test data!")
            elif not os.path.isfile(args.model_path):
                print("There is no path for model!")
            else:
                name_list, label_dic = ClassifyGenerateLabel.ClassifyGenerateLabel(args.train_data_path, args.stage)
            
        
    elif args.function == "time":
        utils.MakeTimeDir()
