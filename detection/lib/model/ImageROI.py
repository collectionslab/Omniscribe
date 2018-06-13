"""
Image ROI data object that stores the information of the bounding boxes
"""

class ImageROI:
    def __init__(self, x=0, y=0, width=10, height=20, text='', confidence=1.00, level=2,
                 isAnnotation=False
                ):
        """
        
        :params level: block(2), para(3), textline(4), word(5)   
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.confidence = confidence
        self.level = level
        
        # for annoation classification labeling
        self.isAnnotation = isAnnotation
        
        
    def toString(self):
        """
        Print the content of the object
        """
        content = ("x:{0}\t"
                  "y:{1}\t"
                  "width:{2}\t"
                  "height:{3}\t"
                  "text:{4}\t"
                  "confidence:{5}\t"
                  "level:{6}\t"
                  "isAnnotation:{7}".format(self.x, self.y, self.width, self.height, self.text,
                                            self.confidence, self.level, self.isAnnotation))
        return content
    
def roi_to_csv(rois, outfilename):
    import csv
    if isinstance(rois, ImageROI):
        rois = [rois]
    with open(outfilename, 'w') as outfile:
        writer = csv.writer(outfile, delimiter = ',', quoting = csv.QUOTE_NONNUMERIC)
        for roi in rois:
            all_data = [roi.x, roi.y, roi.width, roi.height, roi.text, roi.confidence, roi.level, 1 if roi.isAnnotation else 0]
            writer.writerow(all_data)
    return

def csv_to_roi(infilename):
    import csv
    rois = []
    with open(infilename, 'r') as infile:
        reader = csv.reader(infile, delimiter = ',', quoting = csv.QUOTE_NONNUMERIC)
        for row in reader:
            rois.append(ImageROI(x=int(row[0]),
                                 y=int(row[1]),
                                 width=int(row[2]),
                                 height=int(row[3]),
                                 text=str(row[4]),
                                 confidence=float(row[5]),
                                 level=int(row[6]),
                                 isAnnotation= (int(row[7]) == 1)  ))
    return rois
