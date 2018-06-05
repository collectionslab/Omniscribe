
from .model.ImageROI import ImageROI
from .utils.RoiUtils import *
import cv2
import numpy
#Based on http://www.danvk.org/2015/01/07/finding-blocks-of-text-in-an-image-using-python-opencv-and-numpy.html

#Class for detecting ROIs using Canny Image Detection

class CannyEngine:
        def __init__(self):
                pass
            
        def image_to_data(self, img):
                """
                Given an image as a numpy array (PIL or opencv image) 
                find ROIs using Canny Image Detection
                Returns a list of ImageROI objects denoting ROIs found.
                """
                #white if px >225 or near px that is >225. Black if below 200
                img = cv2.bilateralFilter(img,9,75,75)
                img=cv2.Canny(img,150,225)
                img = cv2.medianBlur(img,3)
                for i in range(1,7):
                        ker=cv2.getStructuringElement(cv2.MORPH_RECT,(i,i))
                        img=cv2.dilate(img,ker,i)
                        img = cv2.morphologyEx(img, cv2.MORPH_OPEN, ker)
                        
                ret,thresh=cv2.threshold(img,127,255,cv2.THRESH_BINARY)
                        
                im2 ,countours, hr = cv2.findContours (img,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                areas=[]
                canvas = numpy.zeros(img.shape)
                
                for cntr in countours :
                        x,y,w,h=cv2.boundingRect(cntr)
                        areas.append(ImageROI(x,y,w,h,level=3))
                return areas
           
        def image_to_data_easy(self, img):
                """ 
                Takes an image and returns basic bounding boxes
                with simple countour based merge.
                """
                preproc=CannyEngine.CannyBoxes(img)
                final=CountourMerge(img.shape,preproc)
                return final
