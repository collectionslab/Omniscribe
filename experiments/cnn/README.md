annotations-computervision/experiments/cnn/
=========================================== 

rawlogs

JQNet1-cross_val-500epochs
JQNet1-cross_val-lr_0.001-f1-100epochs
JQNet1-cross_val-lr_0.01-f1-100epochs

These consists of training accuracies and validation accuracies on the 
original 10 books in the dataset evaluated on the JQNet1 model found
in model_utils.py in .csv format. The format is as follows 

train_accs	val_accs
1. 0.813161875945537	0.8275862068965517
2. 0.8127836611195158	0.8275862068965517
3. 0.8044629349470499	0.8160919540229885
.
.
.
500. 0.8029500756429652 	0.45977011494252873

where every epoch (up to 500 in this case) has a recorded training and 
validation accuracy.
