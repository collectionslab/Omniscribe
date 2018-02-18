
try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract
import matplotlib.pyplot as plt
import numpy
import cv2
import argparse



#https://stackoverflow.com/questions/32125281/removing-watermark-out-of-an-image-using-opencv

def HighlightDark(img):
	ker=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(10,10))
	img=cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, ker)
	return img

def NoiseFilter(img):
	img =cv2.bilateralFilter(img,3,75,75)
	return img

def threshold(img,factor=None):
	#If you decide to manual threshhold, the magic number is 30
	#Please ensure that images are greyscale
	ret, bh = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	if(factor != None):
		#reperform thresholding with otsu's threshold modified by factor
		ret, bh =cv2.threshold(img,ret * factor,255,cv2.THRESH_BINARY)
	return bh	
	
def ExtractArea(img,mask):
	#Extracts Dark areas of an image that are in the white areas of the mask
	#Background is made to be white.
	#image and mask must be of same number of channels
	cv2.bitwise_not(img, img)
	fin=cv2.bitwise_and(img,mask)
	fin=cv2.bitwise_not(fin,fin)
	return fin

def CleanMask(img):
	ker=cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
	
	img=cv2.morphologyEx(img, cv2.MORPH_CLOSE, ker)
	
	return img

def QuickPreprocess(img):
	mask = HighlightDark(img)
	mask = NoiseFilter(mask)
	mask = threshold(mask)
	return mask

#for running as a command line script
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('files',nargs=1)
    
	args=parser.parse_args()
	img = cv2.imread(args.files[0],0)
	cv2.imwrite("h.jpg",QuickPreprocess(img))
