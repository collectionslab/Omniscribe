"""
Utility functions.
"""

import numpy as np
import matplotlib.pyplot as plt

def imshow(inp, title=None):
    """
    Imshow for Tensor
    """
    inp = inp.numpy().transpose((1, 2, 0))
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    inp = std * inp + mean
    inp = np.clip(inp, 0, 1)
    plt.imshow(inp)
    if title is not None:
        plt.title(title)
    plt.pause(0.001)  # pause a bit so that plots are updated
    
    
def valid_imshow_data(data):
    """
    Check if the imshow has correct data dimension
    """
    data = np.asarray(data)
    if data.ndim == 2:
        return True
    elif data.ndim == 3:
        if 3 <= data.shape[2] <= 4:
            return True
        else:
            print('The "data" has 3 dimensions but the last dimension '
                  'must have a length of 3 (RGB) or 4 (RGBA), not "{}".'
                  ''.format(data.shape[2]))
            return False
    else:
        print('To visualize an image the data must be 2 dimensional or '
              '3 dimensional, not "{}".'
              ''.format(data.ndim))
        return False


def safe_div(n1, n2):
    if n2 == 0:
        return 0
    return n1/n2

def compute_f1_score(tn, fp, fn, tp, class_type='pos'):
    if class_type == 'pos':
        prec   = safe_div(float(tp),(float(tp) + float(fp)))
        recall = safe_div(float(tp),(float(tp) + float(fn)))
    elif class_type == 'neg':
        prec   = safe_div(float(tn),(float(tn) + float(fn)))
        recall = safe_div(float(tn),(float(tn) + float(fp)))
        
    return safe_div(float(2) * (prec * recall), (prec + recall))


def write_metrics_to_csv(raw_metrics, metric_names, dirname, filename):
    import csv
    import os
    
    if not os.path.exists(dirname):
        os.makedirs(dirname)
        
    fileloc = os.path.join(dirname, filename)
    with open(fileloc, 'w') as outfile:
        filewriter = csv.writer(outfile, delimiter=',')
        filewriter.writerow(metric_names)
        for epoch in range(len(raw_metrics[metric_names[0]])):
            newrow = [raw_metrics[metric][epoch] for metric in metric_names]
            filewriter.writerow(newrow)
            
    print("Wrote metrics to '" + str(fileloc) + "'")
    return


def plot_values(train_values, val_values, title, ylabel='Loss'):
    plt.plot(train_values,label = "train")
    plt.plot(val_values,label = "validation")
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel("Epochs")
    plt.legend()
    plt.show()


    print("Average Training Score: " + str(np.mean(train_values)))
    print("Average Validation Score: " + str(np.mean(val_values)))
    
    
def write_metrics_to_csv(raw_metrics, metric_names, dirname, filename):
    import csv
    import os
    
    if not os.path.exists(dirname):
        os.makedirs(dirname)
        
    fileloc = os.path.join(dirname, filename)
    with open(fileloc, 'w') as outfile:
        filewriter = csv.writer(outfile, delimiter=',')
        filewriter.writerow(metric_names)
        for epoch in range(len(raw_metrics[metric_names[0]])):
            newrow = [raw_metrics[metric][epoch] for metric in metric_names]
            filewriter.writerow(newrow)
            
    print("Wrote metrics to '" + str(fileloc) + "'")
    return


