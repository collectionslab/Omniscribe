from .lib.ImageROI import ImageROI
class Verifier():
    def __init__(self):
        self.data={}
        
    def loadBoundingBoxesCSV(self,filename,skipTitle):
        """
        Load ROIs from manual CSV. skipTitle tells whether to skip first line
        Rows of csv are formatted as:
        ID,name,x1,x2,y1,y2,isAnnotated
        returns Dictionary of Images
        
        
        Note: May want to put this in some sort of image collection class.
        For bounding box: different class for verifiable human ones?
        Currently returns dictionary of IDs (as strings)  with corresponding list of bounding boxes
        """
        
        with open(filename) as f:
            for line in f:
                if skipTitle:
                    skipTitle = False
                    continue
                
                line=line.split(',')
                if not line[0] in self.data:
                    self.data[line[0]]=[]
           
                x1=int(line[2])
                y1=int(line[3])
                x2=int(line[4])
                y2=int(line[5])
                isAnnotated=int(line[6])
                self.data[line[0]].append(ImageROI(x1,y1,x2-x1,y2-y1))    
        
    def validate(self,id,imgROIs):
        """
        Given a list of ROIs, does verification using boxes of data[id]
        """
        TruePositive=0
        FalsePositive=0
        for roi in imgROIs:
            for groundTruth in data[id]:
                #if roi overlaps with a groundTruth, increment TruePositive
            



#sample use

v= verifier()
v.loadBoundingBoxesCSV("bb_data.csv")
