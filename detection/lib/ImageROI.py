"""
Image ROI object that stores the information of the bounding boxes
"""

class ImageROI:
    def __init__(self, x, y, width, height, txt, confidence, line_number):
        """
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.confidence = confidence
        self.txt = txt
        self.line_number = line_number
        
        
    




