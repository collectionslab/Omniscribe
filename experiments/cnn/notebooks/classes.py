"""
Classes. The better way is to have a class with a file. In here, we don't do that
"""

# Creating a class to deal with early stopping criteria
# Important: minimizes a loss value
class EarlyStopping:
    def __init__(self, min_delta=0, patience=5):
        # The minimum delta in loss to be considered a change in loss
        self.min_delta = min_delta
        
        # number of epochs to wait for improvement before terminating
        self.patience = patience
        
        # number of epochs waited
        self.wait = 0
        
        # Set "best loss" to some large number
        self.best_loss = 1e15
        
    def checkStoppingCriteria(self, curr_loss):
        """ Returns whether the stopping criteria has been met. """
        if (curr_loss - self.best_loss) < -self.min_delta:
            self.best_loss = curr_loss
            self.wait = 1
        elif self.wait < self.patience:
            self.wait += 1
        else:
            return True
        return False
        


