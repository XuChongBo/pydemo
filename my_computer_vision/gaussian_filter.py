#!/usr/bin/env python
# -*- coding:utf-8 -*-
from PIL import Image
from pylab import imshow,show,subplot,array,figure,gray,zeros
from scipy.ndimage import filters

file_name='../../data/cv_data/empire.jpg'
# load the image file
img = array(Image.open(file_name))
print img.shape

#refers to http://docs.scipy.org/doc/scipy/reference/ndimage.html
img2 = zeros(img.shape)
for i in range(3):
    img2[:,:,i] = filters.gaussian_filter(img[:,:,i],7) 

# if the img is gray.  use the following 
#im = array(Image.open(’empire.jpg’).convert(’L’)) 
#im2 = filters.gaussian_filter(im,5)

figure()
gray() # don't use colors 

# show the two pics  on 1*2 frame
subplot(1,4,1)   
imshow(img)
subplot(1,4,2)
imshow(img2[:,:,0])
subplot(1,4,3)
imshow(img2[:,:,1])
subplot(1,4,4)
imshow(img2[:,:,2])
#subplot(1,2,2)
#imshow(img_gray)

# starts the figure GUI and raises the figure windows
show()
