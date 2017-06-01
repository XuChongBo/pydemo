# -*- coding: utf-8 -*-
#from opencv.highgui import *
import cv2
import sys
from PIL import Image
import PIL
from numpy import array


def get_statistic(img_gray):
    """
    assume the shape of img array is (height, width).
    """
    t = array(img_gray)
    h = array([0]*256)
    print t.shape
    assert(t.ndim==2)
    for i in range(t.shape[0]):
        for j in range(t.shape[1]):
            h[t[i,j]]+=1
    #print h
    return h

def print_hist(filename):
    img = Image.open(filename)
    print img
    img_gray = img
    h = get_statistic(img_gray)    
    for i, e in enumerate(h):
       if e != 0:
        print i, e


filename = sys.argv[1]
img = Image.open(filename)
#img = cv2.imread(sys.argv[1])
print img
print_hist(filename)
#cv2.imshow("Example1", img)
#cv2.waitKey(-1)

img = img.resize((200,51),  PIL.Image.ANTIALIAS)
print img
outname = 'outres.png'
img.save(outname)
print_hist(outname)
#cv2.imshow("Example2", img)
#cv2.waitKey(-1)


