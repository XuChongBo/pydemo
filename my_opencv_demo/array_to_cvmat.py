# -*- coding: utf-8 -*-
#from opencv.highgui import *
import cv2
import sys
import numpy as np

###
#OpenCV  cvmat must have 1, 3 or 4 channels
#valid shape is (h,w)  (h,w,1)  (h,w,3)  (h,w,4)

######################
img = np.zeros((500,200), np.uint8)
img[50:100,50:100] = 255
#img = np.array([[2,5,9,100,255],[2,5,9,100,255],[2,5,9,100,255],[2,5,9,100,255]])
print type(img), img.shape, img.dtype
cv2.imshow("Example1", img)
cv2.waitKey(0)
##################
img = img = img[:,:,np.newaxis]
print type(img), img.shape, img.dtype
cv2.imshow("Example1", img)
cv2.waitKey(0)

#############################################
img = cv2.imread('demo2.jpg')
print type(img), img.shape, img.dtype
cv2.imshow("Example1", img)
cv2.waitKey(0)


