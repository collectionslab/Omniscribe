=================================================================================================

annotations-computervision/experiments/baseline_cnn/notebooks/

=================================================================================================

cifar10_model.ipynb

The very first model to be trained on our dataset with an accuracy of 70%

resnet18_half_frozen_1epochs_transfer-state.pt
resnet18_half_frozen_2epochs_transfer-state.pt

These are weights of a sub-model of Resnet-18 CNN architecture, consisting of
only half of its depth. They are pre-trained models that are to be loaded in.

testing-datasets.ipynb
testing-transfer_resnet18.ipynb

This verifies that the weights found in 
resnet18_half_frozen_1epochs_transfer-state.pt and
resnet18_half_frozen_2epochs_transfer-state.pt are saved successfully
and evaluates the model on our dataset
