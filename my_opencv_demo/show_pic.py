# -*- coding: utf-8 -*-
#from opencv.highgui import *
import cv2
import sys

img = cv2.imread('demo2.jpg',0)
#img = cv2.imread(sys.argv[1])
print type(img), img.shape, img.dtype

cv2.imshow("Example1", img)
cv2.waitKey(0)

img = cv2.imread('demo2.jpg')
#img = cv2.imread(sys.argv[1])
print type(img), img.shape, img.dtype

cv2.imshow("Example1", img)
cv2.waitKey(0)
