"""
Data Loader to load the labeled data (ground truth)
"""


from lib.model.ImageROI import ImageROI



class GroudTruthDataLoader():
    def __init__(self):
        pass
        
    def loadBoundingBoxesCSV(self,filename,skipFirstLine=True):
        """
        Load ROIs from manual CSV (ground truth). skipTitle tells whether to skip first line
        Rows of csv are formatted as:
        ID,name,x1,x2,y1,y2,isAnnotated
        returns Dictionary of Images
        
        :params skipFirstLine: skip the first line of the file becaise it can be the row header
        """
        data = {}
        
        with open(filename) as f:
            for line in f:
                if skipFirstLine:
                    skipFirstLine = False
                    continue
                
                line=line.split(',')
                if not line[0] in data:
                    data[line[0]]=[]
                x1=int(line[2])
                y1=int(line[3])
                x2=int(line[4])
                y2=int(line[5])
                isAnnotated=int(line[6])
                data[line[0]].append(ImageROI(x1,y1,x2-x1,y2-y1))    
        return data


