"""
Utility functions for ROI operations
"""

from lib.model.ImageROI import ImageROI
import cv2
import numpy
def df_to_ImageROI(df):
    """
    Convert a dataframe into a list of ImageROIs
    """
    imgROIs = []
    
    for index, row in df.iterrows():
        # create the roi object
        x = row['left']
        y = row['top']
        width = row['width']
        height = row['height']
        confidence = row['conf']
        text = row['text']
        level = row['level']        
        imgROI = ImageROI(x,y,width,height,confidence,text,level)
        #print(imgROI.toString())
        imgROIs.append(imgROI)
    return imgROIs


def checkMerge(box1,box2,overlap):
    '''
    check if 2 ROIs overlap, with box edges increased by 'overlap'
    '''
    b1= (box1.x,box1.y,box1.w+box1.x,box1.h+box1.y)
    b2= (box2.x,box2.y,box2.w+box2.x,box2.h+box2.y)

    if ( b2[2] >= (b1[0] - overlap) \
     and (b1[2] + overlap) >= b2[0] \
     and b2[3] >= (b1[1] - overlap) \
     and (b1[3] + overlap) >= b2[1]):
        return True
    else:
        return False


def mergeROI(box1,box2):
    '''
    merge 2 ROIs. Data about text, line number, and confidence will be lost.
    '''
    b1= (box1.x,box1.y,box1.w+box1.x,box1.h+box1.y)
    b2= (box2.x,box2.y,box2.w+box2.x,box2.h+box2.y)

    x = min(b1[0],b2[0])
    y = min(b1[1],b2[1])
    x1 = max(b1[2],b2[2])
    y1 = max(b1[3],b2[3])
    finBox=(x,y,x1,y1)

    return ImageROI(x,y,x1-x,y1-y,None,None,None)


def CountourMerge(img,ROIs):
    """
    Given a List of ROIs, merges them based on their overlap.
    img = tuple with image shape
    ROIs = List of ROIs
    Returns a List of ROIs.
    """
    canvas =numpy.zeros(img)
    for roi in ROIs:
        cv2.rectangle(canvas,(roi.x,roi.y),(roi.x+roi.width,roi.y+roi.height),255,-1)
    oldBB=0
    newBB=1
    new_ROIs=[]
    countours=None
    
    while oldBB!=newBB:
        bb=cv2.Canny(canvas.astype(numpy.uint8),200,225)
        im2 ,countours, hr = cv2.findContours(bb,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        oldBB=newBB
        newBB=len(countours)
        canvas = numpy.zeros(img)
        for cntr in countours :
            x,y,w,h=cv2.boundingRect(cntr)
            cv2.rectangle(canvas,(roi.x,roi.y),(roi.x+roi.width,roi.y+roi.height),255,-1)
    
            cv2.rectangle(canvas,(x,y),(x+w,y+h),255,-1)
    
    for cntr in countours :
        x,y,w,h=cv2.boundingRect(cntr)
        new_ROIs.append(ImageROI(x,y,w,h,None,None,None))
    return new_ROIs


def WhiteInCrop(img,ROI=None):
    '''
    Given an image and a corresponding crop, calculate the number of 
    nonzero/nonblack pixels. None calculates nonblack pixels in whole image
    '''
    crop=img
    if ROI == None:
        crop=img[ ROI.x : ROI.x+ ROI.width][ROI.y: ROI.y + ROI.height]
    pxnum= cv2.countNonZero(crop)
    return pxnum


def CalculateF1(img,ROI):
    '''
    Given an image and an ROI, calculates F1 score, recall and
    precision of ROI. image must be white on black background
    recall is fraction of white pixels in ROI
    precision is fraction of image cropped by ROI
    '''
                        
    imgpx= self.WhiteInCrop(img)
    croppx= self.WhiteInCrop(img,ROI)
    recall=croppx/imgpx
    precision = ROI.width*ROI.height / img.size

    F1 = 2 * (precision * recall) / (precision + recall)

    return (F1,recall,precision)         


def F1Merge(img, ROIs,elim):
    '''
    Given a set of ROIs for a binarized image, merges them by optimizing F1 score.
    elim is a number between zero and 1 that dictates whether to include a box in the final merge if it makes up at least elim of the image

    '''
    #sort ROIs by size:
    ROIs.sort(key=lambda ROI: ROI.h*ROI.y,reverse=True)

    length = len(ROIs)
    added = [False] * length
    count=0
    base=None
    final=[]
    changed=False
    base_F1=0
    imgpx=0
    while count != length:
        for i in range(0,length):
            if not added[i]:
                if base == None:
                    base=ROIs[i]
                    base_F1= self.CalculateF1(img,base)  
                    added[i]=True
                    changed=True
                    count+=1
                    base_F1= self.CalculateF1(img,base)
                    if base_F1[2] <elim:
                        #reset the base
                        base=None
                    else:
                        base_F1=base_F1[0]
                    
                else:	

                    new_ROI=self.MergeROI(base,ROIs[i])
                    new_F1= self.CalculateF1(img,new_ROI)
                    if new_F1[2] > elim and new_F1[0] >= base_F1:
                        base=new_ROI
                        base_F1=new_F1[0]
                        added[i]=True
                        count+=1
                        changed=True
        if not changed:
            final.append(base)
            base=None
    if base != None:
        final.append(base)
    return final




