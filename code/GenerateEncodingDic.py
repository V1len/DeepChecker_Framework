import utils
import os

def GenerateEncodingDic(encoding_dir, encoding_dic_dir):
    encoding_dic ={}
    file_name_list = os.listdir(encoding_dir)
    for file_name in file_name_list:
        aig_name = file_name.split(".vector")[0]
        file_path = os.path.join(encoding_dir, file_name)
        assert(os.path.isfile(file_path))
        vector = []
        with open(file_path, encoding='utf-8') as fp:
            line = fp.readlines()[0].split("[")[1].split("]")[0]
            items = line.split(", ")
            for item in items:
                vector.append(int(item))
            fp.close()
        encoding_dic[aig_name] = vector
    utils.WriteJson(encoding_dic, encoding_dic_dir)
    

if __name__ == '__main__':
    encoding_dir_0 = utils.encoding_dir_0
    encoding_dir_1 = utils.encoding_dir_1
    encoding_dir_2 = utils.encoding_dir_2
    encoding_dic_dir_0 = utils.encoding_dic_dir_0
    encoding_dic_dir_1 = utils.encoding_dic_dir_1
    encoding_dic_dir_2 = utils.encoding_dic_dir_2

    GenerateEncodingDic(encoding_dir_0, encoding_dic_dir_0)
    GenerateEncodingDic(encoding_dir_1, encoding_dic_dir_1)
    GenerateEncodingDic(encoding_dir_2, encoding_dic_dir_2)

