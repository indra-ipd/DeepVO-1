# File to return the Deep VO model.
import torch
import torch.nn as nn
import torch.nn.functional as F


class Net_DeepVO(nn.Module):
    def __init__(self):
        super(Net_DeepVO, self).__init__()
        # CNN
        self.conv1   = nn.Conv2d(6,64,7,2,3,bias=False)
        self.conv2   = nn.Conv2d(64,128,5,2,2,bias = False)
        self.conv3   = nn.Conv2d(128,256,5,2,2,bias = False)
        self.conv3_1 = nn.Conv2d(256,256,3,1,1,bias = False)
        self.conv4   = nn.Conv2d(256,512,3,2,1,bias = False)
        self.conv4_1 = nn.Conv2d(512,512,3,1,1,bias= False)
        self.conv5   = nn.Conv2d(512,512,3,2,1,bias = False)
        self.conv5_1 = nn.Conv2d(512,512,3,1,1,bias = False)
        self.conv6   = nn.Conv2d(512,1024,3,2,1,bias = False)


        # LSTM
        self.LSTM1 = nn.LSTMCell(122880,1024)
        self.LSTM2 = nn.LSTMCell(1024,1024)

        # FC
        self.fc1 = nn.Linear(1024,128)
        #self.fc2 = nn.Linear(128,12)
        self.fc_r = nn.Linear(128,3)
        self.fc_t = nn.Linear(128,3)





    def forward(self, x):
        x = (F.relu(self.conv1(x)))
        x = (F.relu(self.conv2(x)))
        x = (F.relu(self.conv3(x)))
        x = (F.relu(self.conv3_1(x)))
        x = (F.relu(self.conv4(x)))
        x = (F.relu(self.conv4_1(x)))
        x = (F.relu(self.conv5(x)))
        x = (F.relu(self.conv5_1(x)))
        x = ((self.conv6(x))) # No relu at the last conv

        x = x.view(-1,20*6*1024);
        h_t1 = torch.cuda.FloatTensor(x.size(0),1024);
        c_t1 = torch.cuda.FloatTensor(x.size(0),1024);
        h_t2 = torch.cuda.FloatTensor(x.size(0),1024);
        c_t2 = torch.cuda.FloatTensor(x.size(0),1024);
        h_t1,c_t1 = self.LSTM1(x,(h_t1,c_t1))
        h_t2,c_t2 = self.LSTM2(h_t1,(h_t2,c_t2))
        output_fc1 = (F.relu(self.fc1(h_t2)))

        output_r = self.fc_r(output_fc1)
        output_t = self.fc_t(output_fc1)

        return output_r, output_t

class Net_CNN(nn.Module):
    def __init__(self):
        super(Net_CNN, self).__init__()

        self.conv1   = nn.Conv2d(6,64,7,2,3)
        self.conv2   = nn.Conv2d(64,128,5,2,2)
        self.conv3   = nn.Conv2d(128,256,5,2,2)
        self.conv3_1 = nn.Conv2d(256,256,3,1,1)
        self.conv4   = nn.Conv2d(256,512,3,2,1)
        self.conv4_1 = nn.Conv2d(512,512,3,1,1)
        self.conv5   = nn.Conv2d(512,512,3,2,1)
        self.conv5_1 = nn.Conv2d(512,512,3,1,1)
        self.conv6   = nn.Conv2d(512,1024,3,2,1)


    def forward(self, x):
        x = (F.relu(self.conv1(x)))
        x = (F.relu(self.conv2(x)))
        x = (F.relu(self.conv3(x)))
        x = (F.relu(self.conv3_1(x)))
        x = (F.relu(self.conv4(x)))
        x = (F.relu(self.conv4_1(x)))
        x = (F.relu(self.conv5(x)))
        x = (F.relu(self.conv5_1(x)))
        x = ((self.conv6(x))) # No relu at the last conv


        return x


class Net_CNN_BN(nn.Module):
    def __init__(self):
        super(Net_CNN_BN, self).__init__()

        self.conv1   = nn.Conv2d(6,64,7,2,3,bias=False)
        self.conv1_bn = nn.BatchNorm2d(64)

        self.conv2   = nn.Conv2d(64,128,5,2,2,bias=False)
        self.conv2_bn = nn.BatchNorm2d(128)

        self.conv3   = nn.Conv2d(128,256,5,2,2,bias=False)
        self.conv3_bn = nn.BatchNorm2d(256)

        self.conv3_1 = nn.Conv2d(256,256,3,1,1,bias=False)
        self.conv3_1_bn = nn.BatchNorm2d(256)

        self.conv4   = nn.Conv2d(256,512,3,2,1,bias=False)
        self.conv4_bn = nn.BatchNorm2d(512)

        self.conv4_1 = nn.Conv2d(512,512,3,1,1,bias=False)
        self.conv4_1_bn = nn.BatchNorm2d(512)

        self.conv5   = nn.Conv2d(512,512,3,2,1,bias=False)
        self.conv5_bn = nn.BatchNorm2d(512)

        self.conv5_1 = nn.Conv2d(512,512,3,1,1,bias=False)
        self.conv5_1_bn = nn.BatchNorm2d(512)

        self.conv6   = nn.Conv2d(512,1024,3,2,1,bias=False)
        self.conv6_bn = nn.BatchNorm2d(1024)


    def forward(self, x):
        x = (F.relu(self.conv1_bn(self.conv1(x))))
        x = (F.relu(self.conv2_bn(self.conv2(x))))
        x = (F.relu(self.conv3_bn(self.conv3(x))))
        x = (F.relu(self.conv3_1_bn(self.conv3_1(x))))
        x = (F.relu(self.conv4_bn(self.conv4(x))))
        x = (F.relu(self.conv4_1_bn(self.conv4_1(x))))
        x = (F.relu(self.conv5_bn(self.conv5(x))))
        x = (F.relu(self.conv5_1_bn(self.conv5_1(x))))
        x = ((self.conv6_bn(self.conv6(x)))) # No relu at the last conv

        return x



class Net_LSTM(nn.Module):
    def __init__(self):
        super(Net_LSTM, self).__init__()

        # LSTM
        self.LSTM1 = nn.LSTMCell(122880,1024)
        self.LSTM2 = nn.LSTMCell(1024,1024)

        # FC
        self.fc1 = nn.Linear(1024,128)
        #self.fc2 = nn.Linear(128,12)

        self.fc_r = nn.Linear(128,3)
        self.fc_t = nn.Linear(128,3)




    def forward(self, x):

        x = x.view(-1,20*6*1024);
        h_t1 = torch.cuda.FloatTensor(x.size(0),1024).fill_(0);
        c_t1 = torch.cuda.FloatTensor(x.size(0),1024).fill_(0);
        h_t2 = torch.cuda.FloatTensor(x.size(0),1024).fill_(0);
        c_t2 = torch.cuda.FloatTensor(x.size(0) ,1024).fill_(0);

        h_t1,c_t1 = self.LSTM1(x,(h_t1,c_t1))
        h_t2,c_t2 = self.LSTM2(h_t1,(h_t2,c_t2))
        
        output_fc1 = (F.relu(self.fc1(h_t2)))
        output_r = self.fc_r(output_fc1)
        output_t = self.fc_r(output_fc1)


        return output_r,output_t




def copyWeights(cnn,weights,flag):
    # copy caffe weight or the checkpoint ones without batchnorm
    if flag !='checkpoint_wb':
        cnn.conv1.weight.data = weights["conv1.0.weight"]
        cnn.conv1.bias.data = weights["conv1.0.bias"]

        cnn.conv2.weight.data = weights["conv2.0.weight"]
        cnn.conv2.bias.data = weights["conv2.0.bias"]

        cnn.conv3.weight.data = weights["conv3.0.weight"]
        cnn.conv3.bias.data = weights["conv3.0.bias"]

        cnn.conv3_1.weight.data = weights["conv3_1.0.weight"]
        cnn.conv3_1.bias.data = weights["conv3_1.0.bias"]

        cnn.conv4.weight.data = weights["conv4.0.weight"]
        cnn.conv4.bias.data = weights["conv4.0.bias"]

        cnn.conv4_1.weight.data = weights["conv4_1.0.weight"]
        cnn.conv4_1.bias.data = weights["conv4_1.0.bias"]

        cnn.conv5.weight.data = weights["conv5.0.weight"]
        cnn.conv5.bias.data = weights["conv5.0.bias"]

        cnn.conv5_1.weight.data = weights["conv5_1.0.weight"]
        cnn.conv5_1.bias.data = weights["conv5_1.0.bias"]

        cnn.conv6.weight.data = weights["conv6.0.weight"]
        cnn.conv6.bias.data = weights["conv6.0.bias"]

    else:
    	cnn.conv1.weight.data = weights["conv1.0.weight"]
    	cnn.conv1_bn.weight.data = weights["conv1.1.weight"]
    	cnn.conv1_bn.bias.data = weights["conv1.1.bias"]
    	cnn.conv1_bn.running_mean.data = weights["conv1.1.running_mean"]
    	cnn.conv1_bn.running_var.data = weights["conv1.1.running_var"]

    	cnn.conv2.weight.data = weights["conv2.0.weight"]
    	cnn.conv2_bn.weight.data = weights["conv2.1.weight"]
    	cnn.conv2_bn.bias.data = weights["conv2.1.bias"]
    	cnn.conv2_bn.running_mean.data = weights["conv2.1.running_mean"]
    	cnn.conv2_bn.running_var.data = weights["conv2.1.running_var"]

    	cnn.conv3.weight.data = weights["conv3.0.weight"]
    	cnn.conv3_bn.weight.data = weights["conv3.1.weight"]
    	cnn.conv3_bn.bias.data = weights["conv3.1.bias"]
    	cnn.conv3_bn.running_mean.data = weights["conv3.1.running_mean"]
    	cnn.conv3_bn.running_var.data = weights["conv3.1.running_var"]

    	cnn.conv3_1.weight.data = weights["conv3_1.0.weight"]
    	cnn.conv3_1_bn.weight.data = weights["conv3_1.1.weight"]
    	cnn.conv3_1_bn.bias.data = weights["conv3_1.1.bias"]
    	cnn.conv3_1_bn.running_mean.data = weights["conv3_1.1.running_mean"]
    	cnn.conv3_1_bn.running_var.data = weights["conv3_1.1.running_var"]

    	cnn.conv4.weight.data = weights["conv4.0.weight"]
    	cnn.conv4_bn.weight.data = weights["conv4.1.weight"]
    	cnn.conv4_bn.bias.data = weights["conv4.1.bias"]
    	cnn.conv4_bn.running_mean.data = weights["conv4.1.running_mean"]
    	cnn.conv4_bn.running_var.data = weights["conv4.1.running_var"]

    	cnn.conv4_1.weight.data = weights["conv4_1.0.weight"]
    	cnn.conv4_1_bn.weight.data = weights["conv4_1.1.weight"]
    	cnn.conv4_1_bn.bias.data = weights["conv4_1.1.bias"]
    	cnn.conv4_1_bn.running_mean.data = weights["conv4_1.1.running_mean"]
    	cnn.conv4_1_bn.running_var.data = weights["conv4_1.1.running_var"]

    	cnn.conv5.weight.data = weights["conv5.0.weight"]
    	cnn.conv5_bn.weight.data = weights["conv5.1.weight"]
    	cnn.conv5_bn.bias.data = weights["conv5.1.bias"]
    	cnn.conv5_bn.running_mean.data = weights["conv5.1.running_mean"]
    	cnn.conv5_bn.running_var.data = weights["conv5.1.running_var"]

    	cnn.conv5_1.weight.data = weights["conv5_1.0.weight"]
    	cnn.conv5_1_bn.weight.data = weights["conv5_1.1.weight"]
    	cnn.conv5_1_bn.bias.data = weights["conv5_1.1.bias"]
    	cnn.conv5_1_bn.running_mean.data = weights["conv5_1.1.running_mean"]
    	cnn.conv5_1_bn.running_var.data = weights["conv5_1.1.running_var"]

    	cnn.conv6.weight.data = weights["conv6.0.weight"]
    	cnn.conv6_bn.weight.data = weights["conv6.1.weight"]
    	cnn.conv6_bn.bias.data = weights["conv6.1.bias"]
    	cnn.conv6_bn.running_mean.data = weights["conv6.1.running_mean"]
    	cnn.conv6_bn.running_var.data = weights["conv6.1.running_var"]


    return cnn 
