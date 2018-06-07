'''
Image object that stores images and relevant data

'''
from .ImageROI import ImageROI

class Image:
    def __init__(self,ID,ROIs):
        self.ID=ID
        self.ROIs=ROIs
        
    def loadBoundingBoxesCSV(filename,skipTitle):
        '''
        Load ROIs from manual CSV. skipTitle tells whether to skip first line
        Rows of csv are formatted as:
        ID,name,x1,x2,y1,y2,isAnnotated
        returns Dictionary of Images


        Note: May want to put this in some sort of image collection class.
        For bounding box: different class for verifiable human ones?
        Currently returns dictionary of ID with corresponding list of bounding boxes
        '''
        collection={}
        with open(filename) as f:
            for line in f:
                if skipTitle:
                    skipTitle = False
                    continue
                
                line=line.split(',')
                if not line[0] in collection:
                    collection[line[0]]=[]
           
                x1=int(line[2])
                y1=int(line[3])
                x2=int(line[4])
                y2=int(line[5])
                isAnnotated=int(line[6])
                collection[line[0]].append(ImageROI(x1,y1,x2-x1,y2-y1))    
        return collection
            
