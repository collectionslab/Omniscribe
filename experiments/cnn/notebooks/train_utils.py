from __future__ import print_function

# import torch
# import torch.nn as nn
# import torch.optim as optim
# from torch.autograd import Variable
# import numpy as np
# import torchvision
# from torchvision import datasets, models, transforms
# import matplotlib.pyplot as plt
# import os
# import copy
# import csv
# import gc
# import torchnet as tnt
# from utils import *
# from classes import *
# from tqdm import tqdm_notebook # for-loop progress bar in notebook

# # plt setup and the gpu setup
# plt.ion()
# use_gpu = torch.cuda.is_available()

# load memory profiler
# %load_ext memory_profiler


def train(model, criterion, optimizer, train_data_loader, val_data_loader, num_epochs = 25, use_gpu = False):
    
    import time
    import torchnet as tnt
    import torch
    from torch.autograd import Variable
    from utils import compute_f1_score
    
    since = time.time()
    
    device_name = 'cuda' if use_gpu else 'cpu'
    
    # setup data_loaders
    data_loaders = {'train': train_data_loader, 'val': val_data_loader}
    num_samples = {p : len(data_loaders[p].dataset) for p in data_loaders}
    
    # accumulate metrics
    metric_names = [p+'-'+m for p in ['train', 'val'] for m in ['loss', 'tn', 'fp', 'fn', 'tp', 'f1_pos', 'f1_neg']]
    metrics_dict = {m : [] for m in metric_names}
    
    # start training
    for epoch in range(num_epochs):
        print()
        print('Epoch {}/{}'.format(epoch, num_epochs - 1))
        print('-' * 10)
        
        # perform both train and val in each epoch
        for phase in ['train', 'val']:
            # initialize variables for metrics per epoch
            running_loss = 0.0
            confusion_matrix = tnt.meter.ConfusionMeter(2)
            
            # set model into appropriate mode based on phase
            model.train(phase == 'train')
            
            # iterate over data in appropraite phase
            for data in data_loaders[phase]:
                inputs, labels = data
                inputs, labels = Variable(inputs.to(device_name)), Variable(labels.to(device_name))
                
                # zero optimizer gradients
                optimizer.zero_grad()
                
                # Perform forward pass
                with torch.set_grad_enabled(phase == 'train'):
                    # forward
                    outputs = model(inputs)
                    _, preds = torch.max(outputs.data, 1)
                    loss = criterion(outputs, labels)
                    
                    # back propagation if training
                    if phase == 'train':
                        loss.backward()
                        optimizer.step()
                   
                    # statistics

                    # add info to confusion matrix
                    confusion_matrix.add(outputs.data, labels.data)

                    # accumulate running_loss for epoch
                    running_loss += (loss.item() * inputs.size(0))
                    
            # outside of data loop
            # at end of phase in the epoch, calculate metrics
            
            # compute evaluation
            epoch_loss = float(running_loss) / float(num_samples[phase])
            conf_tn    = confusion_matrix.conf[0][0]
            conf_fp    = confusion_matrix.conf[0][1]
            conf_fn    = confusion_matrix.conf[1][0]
            conf_tp    = confusion_matrix.conf[1][1]
            epoch_f1_p = compute_f1_score(conf_tn, conf_fp, conf_fn, conf_tp, class_type='pos')
            epoch_f1_n = compute_f1_score(conf_tn, conf_fp, conf_fn, conf_tp, class_type='neg')
            
            # accumulate metrics
            metrics_dict[phase+'-loss'].append(epoch_loss)
            metrics_dict[phase+'-tn'].append(conf_tn)
            metrics_dict[phase+'-fp'].append(conf_fp)
            metrics_dict[phase+'-fn'].append(conf_fn)
            metrics_dict[phase+'-tp'].append(conf_tp)
            metrics_dict[phase+'-f1_pos'].append(epoch_f1_p)
            metrics_dict[phase+'-f1_neg'].append(epoch_f1_n)
            
            # report evaluation
            print('Phase:%s' %phase)
            print('average loss:', epoch_loss)
            print('f1_pos:', epoch_f1_p)
            print('f1_neg:', epoch_f1_n)
            print()
            
        # outside of phase in epoch loop
        
    # outside of epoch loop
    # training complete

    time_elapsed = time.time() - since
    print('Training complete in {:.0f}m {:.0f}s'.format(
        time_elapsed // 60, time_elapsed % 60))
    
    # return both the trained model and the metrics
    return model, metrics_dict
