# -*- coding: utf-8 -*-
#from opencv.highgui import *
import cv2
import sys
import numpy as np

img = cv2.imread(sys.argv[1])
#img = cv2.imread(sys.argv[1])
print type(img), img.shape, img.dtype

b = img[:,:,0]
g = img[:,:,1]
r = img[:,:,2]
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#im_gray = ( r*0.3 + 0.59*g + 0.11*b ).astype(np.uint8)
#img_gray = ( r*0.3 + 0.59*g + 0.11*b ).astype(np.uint8)
cv2.imshow("Example1", img_gray)
cv2.imwrite("xxgray.png", img_gray)
cv2.waitKey(0)
