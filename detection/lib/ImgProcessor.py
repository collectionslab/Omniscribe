"""
05/15/18 This object is created to perform variety of image processing.

It is based on the git repo root directory preproc.py

Reference: 
#https://stackoverflow.com/questions/32125281/removing-watermark-out-of-an-image-using-opencv

by
Johnny Ho
Emily Chen
Morgan Madjukie

"""


try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract
import matplotlib.pyplot as plt
import numpy as np
import cv2
import argparse

from os import listdir, makedirs
from os.path import isfile, join, exists


class ImgProcessor:
    
    def __init__(self):
        pass

    def HighlightDark(self,img):
        ker=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(10,10))
        img=cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, ker)
        return img

    def NoiseFilter(self,img):
        img =cv2.bilateralFilter(img,3,75,75)
        return img

    def threshold(self, img,factor=None):
        #If you decide to manual threshhold, the magic number is 30
        #Please ensure that images are greyscale
        ret, bh = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        if(factor != None):
            #reperform thresholding with otsu's threshold modified by factor
            ret, bh =cv2.threshold(img,ret * factor,255,cv2.THRESH_BINARY)
        return bh

    def thresholdMagic(self, img):
        #Threshold by magic number = 30
        ret, res = cv2.threshold(img,30,255,cv2.THRESH_BINARY)
        return res

    def ExtractArea(self, img, mask):
        #Extracts Dark areas of an image that are in the white areas of the mask
        #Background is made to be white.
        #image and mask must be of same number of channels
        cv2.bitwise_not(img, img)
        fin=cv2.bitwise_and(img,mask)
        fin=cv2.bitwise_not(fin,fin)
        return fin

    def CleanMask(self, img):
        ker=cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))

        img=cv2.morphologyEx(img, cv2.MORPH_CLOSE, ker)

        return img

    def quickPreprocess(self, img):
        """
        A quick complete image preprocessing step
        """
        mask = self.HighlightDark(img)
        mask = self.NoiseFilter(mask)
        mask = self.threshold(mask)

        mask = np.bitwise_not(mask, mask)
        return mask

    def loadImage(self, inFilename):
        """
        Load and return an image numpy array
        
        :params inFilename: input file name (with path)
        """
        img = cv2.imread(inFilename, 0)
        return img

    def PreprocessImageFile(self, inFilename, outFilename):
        img = cv2.imread(inFilename, 0)
        cv2.imwrite(outFilename, QuickPreprocess(img))


    def PreprocessImageFolder(self, inFoldername, outFoldername):
        if not exists(outFoldername):
            makedirs(outFoldername)

        for f in listdir(inFoldername):
            fname = join(inFoldername, f)
            if isfile(fname):
                PreprocessImageFile(fname, join(outFoldername, str(f)))



