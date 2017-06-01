# -*- coding: utf-8 -*-
#from opencv.highgui import *
import cv2
import sys
from PIL import Image
import numpy as np


def printMid(img):
    height = img.shape[0]
    width = img.shape[1]

    print img[height/2:height/2+50, width/2:width/2+50]

# read origin pixel data
img = Image.open('label-example.png')
print "pil img:", img
arr = np.asarray(img)
print "pil arr shape: ", arr.shape
print "pil arr: ", arr
printMid(arr)

# opencv will replace the pixel data using the palette automately
img = cv2.imread('label-example.png')
#img = cv2.imread(sys.argv[1])
print "----- cv image ------"
print type(img), img.shape, img.dtype
printMid(img)
cv2.imshow("Example1", img)
cv2.waitKey(0)

