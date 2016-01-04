# -*- coding: utf-8 -*-
#from opencv.highgui import *
from PIL import Image
from pylab import imshow,show,axis,array,zeros
from pylab import jet
import numpy as np
###############
#  pil surpport array shape: (h,w)   (h,w,3)    NOT (h,w,1) 

# load the image file
img = Image.open('demo2.jpg')
print type(img)
print img.mode
img.show()
img = np.array(img)
print type(img)
print img.shape, img.dtype, 


######################
img = np.zeros((500,200), np.uint8)
img[50:100,50:100] = 255
#img = np.array([[2,5,9,100,255],[2,5,9,100,255],[2,5,9,100,255],[2,5,9,100,255]])
print type(img), img.shape, img.dtype
pil_image= Image.fromarray(img)   #the input array must be type of 'uinit8' 
print pil_image.mode
pil_image.show()

##################
img[80:150,80:140] = 155
img = img[:,:,np.newaxis]  #not surpport  shape
if img.shape[2]==1:
    img = img.reshape(img.shape[0:2])
print type(img), img.shape, img.dtype
pil_image= Image.fromarray(img)   #the input array must be type of 'uinit8' 
print pil_image.mode
pil_image.show()

