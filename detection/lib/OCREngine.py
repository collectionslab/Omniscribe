"""
OCR engine that supports tesseract or opencv
"""
import pytesseract
import pandas as pd
from lib.utils.RoiUtils import *
from io import StringIO
from lib.CannyEngine import *


class OCREngine:
    
    def __init__(self, engine='tesseract', ocr_config=None):
        """
        :params engine: which engine we are using: tesseract, opencv2
        """        
        self.engine = engine
        self.ocr_config = ocr_config
        if self.engine == 'tesseract':
            self.ocr = pytesseract
            
            # configuration 
            if ocr_config is None:
                self.ocr_config = self._tess_ocr_config()
                
        elif self.engine == 'cv2':
            cannyEngine = CannyEngine()
            self.ocr = cannyEngine
        else:
            print('Did not initiate the ocr engine correctly. Error will occur.')
            self.ocr = None
            
    
    def image_to_data(self, img):
        """
        Extract rois using the ocr engine.
        """
        if self.engine == 'tesseract':
            imgROIs, data_df = self._tess_image_to_data(img)
        elif self.engine == 'cv2':
            imgROIs = self._opencv_image_to_data(img)
            data_df = None
        return imgROIs, data_df        
        
        
    def _tess_image_to_data(self, img):
        """
        Tesseract specific function. Convert the image into verbose data, including boxes, 
        confidences, line and page numbers
        
        return: list of imageROIs and the df for the original content
        """
        data = self.ocr.image_to_data(img, config = self.ocr_config)
        
        # convert the tabular data into pandas
        tmp = StringIO(data)
        data_df = pd.read_table(tmp)

        # convert the data_df into ImageROI object
        imgROIs = df_to_ImageROI(data_df)
        
        return imgROIs, data_df
    
    
    def _opencv_image_to_data(self, img):
        """
        Opencv specific function. Convert the image into verbose data, including boxes, 
        confidences, line and page numbers
        
        return: list of imageROIs 
        """
        imgROIs = self.ocr.image_to_data(img)
        
        return imgROIs
    
    
    def _tess_ocr_config(self):
        """
        Tessearct configuration. Best configuration identified so far.
        """
        language = 'eng' # language
        psm = '3' # page segmentation mode; 3 = fully automatic page segmentation, but no OSD
        oem = '2' # OCR engine, 0:original, 1: cube, 2: tesseract + cube
        config = '-l %s --psm %s --oem %s' %(language, psm, oem)
        return config
        
        
     
        






