"""
Image ROI data object that stores the information of the bounding boxes
"""

class ImageROI:
    def __init__(self, x=0, y=0, width=10, height=20, text='test', confidence=1.00, level=1,
                 isAnnotation=False
                ):
        """
        
        :params level: block(2), para(3), textline(4), word(5)   
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.confidence = confidence
        self.text = text
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
                  "isAnnotation:{7}".format(self.x, self.y, self.width, self.height, self.confidence, 
                                            self.text, self.level, self.isAnnotation))
        return content
              
        
        
        
   

            
            

                            
                        
            


