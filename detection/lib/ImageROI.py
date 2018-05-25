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
    def checkMerge(box1,box2,overlap):
        '''
        check if 2 ROIs overlap, with box edges increased by 'overlap'
        '''
        b1= (box1.x,box1.y,box1.w+box1.x,box1.h+box1.y)
        b2= (box2.x,box2.y,box2.w+box2.x,box2.h+box2.y)
        
        if ( b2[2] >= (b1[0] - overlap) 
	     and (b1[2] + overlap) >= b2[0] 
	     and b2[3] >= (b1[1] - overlap) 
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
    def CountourMerge(ROIs):
        #Given a List of ROIs, merges them based on their overlap.
        #Returns a List of ROIs.
        canvas =numpy.zeros(img.shape)
        for roi in ROIs:
            cv2.rectangle(canvas,(x,y),(x+w,y+h),255,1)
        oldBB=0
        newBB=1
        new_ROIs=[]
        countours=None
        while oldBB!=newBB :
	    bb=cv2.Canny(canvas.astype(numpy.uint8),200,225)
	    im2 ,countours, hr = cv2.findContours (bb,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	    oldBB=newBB
	    newBB=len(countours)
	    canvas = numpy.zeros(img.shape)
	    for cntr in countours :
		x,y,w,h=cv2.boundingRect(cntr)
		
		cv2.rectangle(canvas,(x,y),(x+w,y+h),255,-1)
        for cntr in countours :
	    x,y,w,h=cv2.boundingRect(cntr)
	    areas.append(ImageROI(x,y,w,h,None,None,None))
        return new_ROIs
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
        PC=0
        while count != length:
            for i in range(0,length):
                if not added[i]:
                    if base == None:
                        base=ROIs[i]
                        added[i]=True
                        changed=True
                        count+=1
                        PC=#calculate F1
                    else:	
			#TODO : finish F1 calculation
                        self.MergeROI(base,ROIs[i])
                        #calculate F1
                        if new F1 >= old F1:
                            base=#new ROI
                            added[i]=True
                            count+=1
                            changed=True
            if not changed:
                final.append(base)
                base=None
        return final
            
            

                            
                        
            


