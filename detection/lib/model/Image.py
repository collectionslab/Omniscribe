'''
Image object that stores images and relevant data

'''
from .ImageROI import ImageROI

class Image:
    def __init__(self,ID,ROIs):
        self.ID=ID
        self.ROIs=ROIs
        
            
