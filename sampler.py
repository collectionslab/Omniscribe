from cv2 import *
from os import listdir
from os.path import isfile, isdir, join
import os
import numpy
import random
import argparse
'''
	Tool for extracting square samples from large images
'''

def processImg(files,color=1,px=32,number=10,ft=None,saveFile=None):
    flist=[]
    for f in files:
        if isfile(f):
            flist.append(f)
        elif isdir(f):
            for pf in listdir(f):
                if isfile(f=join(f, pf)):
                    flist.append(f)
        else:
            print("Invalid file/folder")
            
    for file in flist:        
        img=imread(f,color)
        r,c,j=("","","")
        if color==0:
            r,c =img.shape
        else:
            r,c,j = img.shape
        for i in range(1,number+1):
            f=file
            r1=random.randint(0,r-px)
            c1=random.randint(0,c-px)
            newimg=img[r1:r1+px,c1:c1+px]
            
            if(ft==None):
                ft=f.split('.')[1]
            f=f.split('.')[0].split(os.sep)[-1]
            if (saveFile!=None):
                f=saveFile + os.sep + f
            imwrite(f+'_'+str(i)+'.'+ft,newimg)

#Generate small samples from existing large images
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-g','--grey',action='store_const',const=0,default=1)
    parser.add_argument('-p','--pixels',action='store',default=32)
    parser.add_argument('-t','--filetype',action='store',default=None)
    parser.add_argument('-n','--number',action='store',default=10)
    parser.add_argument('-s','--save',action='store',default=None)
    parser.add_argument('files',nargs='+')
    
    args=parser.parse_args()
    print(args.filetype)
    processImg(args.files,args.grey,int(args.pixels),int(args.number),args.filetype,args.save)
