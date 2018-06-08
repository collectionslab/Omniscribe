###
# Contains utils for model architecture creation, etc.
###


###
# JQNet1 start
###

import torch.nn as nn
import torch.nn.functional as F
from torch.optim import lr_scheduler
# device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

#from https://github.com/pytorch/examples/blob/master/mnist/main.py
class JQNet1(nn.Module):
    def __init__(self, use_gpu):
        super(JQNet1, self).__init__()
        if use_gpu:
            self.conv1 = nn.Conv2d(1, 10, kernel_size=3, padding = 1).cuda()
            self.conv2 = nn.Conv2d(10, 20, kernel_size=3, padding = 1).cuda()
            self.conv3 = nn.Conv2d(20, 40, kernel_size=3, padding = 1).cuda()
            self.conv2_drop = nn.Dropout2d(p = 0.2)
            self.conv3_drop = nn.Dropout2d(p = 0.1)

            #assumes a batch size of 50
            self.fc1 = nn.Linear(31360,64).cuda()
            self.fc2 = nn.Linear(64, 25).cuda()
            self.fc3 = nn.Linear(25,2).cuda()
        else:
            self.conv1 = nn.Conv2d(1, 10, kernel_size=3, padding = 1).cpu()
            self.conv2 = nn.Conv2d(10, 20, kernel_size=3, padding = 1).cpu()
            self.conv3 = nn.Conv2d(20, 40, kernel_size=3, padding = 1).cpu()
            self.conv2_drop = nn.Dropout2d(p = 0.2)
            self.conv3_drop = nn.Dropout2d(p = 0.1)

            #assumes a batch size of 50
            self.fc1 = nn.Linear(31360,64).cpu()
            self.fc2 = nn.Linear(64, 25).cpu()
            self.fc3 = nn.Linear(25,2).cpu()

    def forward(self, x):
        x = F.relu(F.max_pool2d(self.conv1(x), 2))
        x = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
        x = F.relu(F.max_pool2d(self.conv3_drop(self.conv3(x)), 2))
        
        x = x.view(x.size(0),-1) #clutch line
        x = F.relu(self.fc1(x))
        x = F.dropout(x, training=self.training)
        
        
        x = x.view(x.size(0),-1) #clutch line
        x = F.relu(self.fc2(x))
        x = F.dropout(x, training=self.training)
        
        x = self.fc3(x)
        return F.log_softmax(x, dim=1)
    
###
# JQNet1 End
###
    
    
    
###
# Net1 Start
###

import torch.nn as nn
import torch.nn.functional as F
from torch.optim import lr_scheduler
import torch

class Net1(nn.Module):
    def __init__(self, use_gpu):
        super(Net1, self).__init__()
        device = torch.device('cuda' if use_gpu else 'cpu')
        
#         self.input_size = (32, 32)
        self.input_size = (64, 64)
        
        self.conv1 = nn.Conv2d(1, 10, kernel_size=4).to(device)
        self.maxpool1 = nn.MaxPool2d(2).to(device)
        
        self.conv2 = nn.Conv2d(10, 20, kernel_size=4).to(device)
        self.maxpool2 = nn.MaxPool2d(6).to(device)

        # Todo: check input size of this layer
#         self.fc1 = nn.Linear(8000, 100).to(device)
        self.fc1 = nn.Linear(320, 100).to(device)

        
        self.batchnorm1 = nn.BatchNorm1d(100).to(device)
        
        self.fc2 = nn.Linear(100, 2).to(device)
        
        # Only use this layer if self.training
        self.conv2_drop = nn.Dropout2d(p = 0.2).to(device)

    def forward(self, x):
        x = F.relu(self.maxpool1(self.conv1(x)))
        x = F.relu(self.maxpool2(self.conv2(x)))
        
#         print(x.size())
        # Expand x based on batch size (x.size(0))
        x = x.view(x.size(0), -1)
#         print(x.size())
        x = self.fc1(x)
        
        x = self.batchnorm1(x)
        
        x = self.fc2(x)
        
        if self.training:
            x = self.conv2_drop(x)
        
        return F.log_softmax(x, dim=1)

###
# Net1 End
###
    
    
# ========================================
# define model structure
# ========================================
from lib.playground.utee import selector
from lib.playground.mnist import model
import inspect

def create_model_architecture(model_type='mnist', use_gpu = False, **kwargs):
    """
    params model_type: the type of model, for now, support mnist and resnet18    
    """
    if model_type == 'mnist':
        print('using pretrained mnist model')
        
        # load the model from the playground library
        model_annotation, ds_fetcher, is_imagenet = selector.select('mnist')
        
        # remove last layer
        removed = list(model_annotation.model.children())[:-1]
        
        # add a front layer to account for new input
        # IMPORTANT, we need to update the self.input_dims of the MLP class
        removed = [nn.Linear(img_input_size*img_input_size,28*28), nn.ReLU()] + removed
        
        # formulate the layers
        model_annotation.model=torch.nn.Sequential(*removed)
        
        # add the new fc layer
        model_annotation.model.fc = torch.nn.Linear(256,2).cuda()
        
        # update the self.input_dims of the network
        model_annotation.input_dims = img_input_size * img_input_size                

    elif model_type == 'resnet18':    
        print("Transferring resnet18 and retraining with annotations dataset.")    
        model_annotation = models.resnet18(pretrained=True)
        num_params = sum(1 for i in model_annotation.parameters())

        # There are 10 layers (model_ft.children()) in resnet18
        # Freezing the first half of resnet18, freezing all params for layers 1-5
        max_layer = 5
        curr_layer = 1
        last_layer = None
        for child in model_annotation.children():
            if curr_layer <= max_layer:
                for param in child.parameters():
                    param.requires_grad = False
                last_layer = child
                curr_layer = curr_layer + 1
            else:
                break

        # Replace the final fully connected layer to perform binary classification
        num_ftrs = model_annotation.fc.in_features
        model_annotation.fc = nn.Linear(num_ftrs, 2)
        
    elif model_type == 'jq_net1':
        print("Creating JQ's net1.")
        argspec = inspect.getfullargspec(JQNet1).args
        args = {arg : kwargs[arg] for arg in argspec if arg in kwargs}
        model_annotation = JQNet1(use_gpu, **args)
        
    elif model_type == 'net1':
        print('Creating Net1.')
        argspec = inspect.getfullargspec(Net1).args
        args = {arg : kwargs[arg] for arg in argspec if arg in kwargs}
        model_annotation = Net1(use_gpu, **args)
        

    # return
    if use_gpu:
        return model_annotation.cuda()
    else:
        return model_annotation.cpu()
