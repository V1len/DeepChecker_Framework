import torch
import torch.nn as nn
from torch.nn import init
from torch.utils.data import Dataset
import utils

class BaseBlock(nn.Module):
    def __init__(self, in_features, out_features):
        super(BaseBlock, self).__init__()
        self.Dense = nn.Linear(in_features, out_features)
        self.dropout = nn.Dropout(p=0.5)
        self.relu = nn.ReLU()

    def forward(self, x):
        out = self.Dense(x)
        out = self.dropout(out)
        out = self.relu(out)
        return out

class ClassifyNet(nn.Module):
    def __init__(self, input_length):
        super(ClassifyNet, self).__init__()
        self.Dense0 = BaseBlock(input_length, 512)
        self.Dense1 = BaseBlock(512, 1024)
        self.Dense2 = BaseBlock(1024, 2048)
        self.Dense3 = BaseBlock(2048, 2048)
        self.Dense4 = BaseBlock(2048, 1024)
        self.Dense5 = BaseBlock(1024, 512)
        self.Dense6 = BaseBlock(512, 128)
        self.Dense7 = BaseBlock(128, 32)
        self.Dense8 = nn.Linear(32, 4)
        self.Softmax = nn.Softmax(dim=1)

    def forward(self, x, use_dropout=False):
        output = self.Dense0(x)
        output = self.Dense1(output)
        output = self.Dense2(output)
        output = self.Dense3(output)
        output = self.Dense4(output)
        output = self.Dense5(output)
        output = self.Dense6(output)
        output = self.Dense7(output)
        output = self.Dense8(output)
        output = self.Softmax(output)
        return output

def initNetParams(net):
    for m in net.modules():
        if isinstance(m, nn.Conv2d):
            init.xavier_uniform_(m.weight.data)
            init.constant_(m.bias.data, 0.1)
        elif isinstance(m, nn.BatchNorm2d):
            m.weight.data.fill_(1)
            m.bias.data.zero_()
        elif isinstance(m, nn.Linear):
            m.weight.data.normal_(0, 0.01)
            m.bias.data.zero_()


class MyDataSet(Dataset):
    def __init__(self, name_list, vec_list, label_list):
        self.name_list = name_list
        self.vec_list = vec_list
        self.label_list = label_list

    def __len__(self):
        return len(self.name_list)

    def __getitem__(self, index):
        name = self.name_list[index]
        vec = self.vec_list[index]
        label = utils.method_list.index(self.label_list[index])
        return name, vec, label