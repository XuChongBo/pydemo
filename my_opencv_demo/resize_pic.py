# -*- coding: utf-8 -*-
#from opencv.highgui import *
import cv2
import sys

img = cv2.imread('demo2.jpg',0)
#img = cv2.imread(sys.argv[1])
print type(img), img.shape, img.dtype

cv2.imshow("Example1", img)
cv2.waitKey(0)
### method 1
img = cv2.resize(img,(500,400))
### method 2
img = cv2.resize(img,(0,0),fx=0.5,fy=0.5)
print type(img), img.shape, img.dtype
cv2.imshow("Example1", img)
cv2.waitKey(0)
