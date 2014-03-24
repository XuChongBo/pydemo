#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
=====================
Global Thresholding
=====================

Thresholding is the simplest way to classify the pixels to forground OR background. If that background is relatively uniform, then you can use a global threshold value to binarize the image by pixel-intensity. 

=====================
Adaptive Thresholding
=====================
If there's large variation in the background intensity, however, adaptive thresholding (a.k.a. local or dynamic thresholding) may produce better results.

"""

import matplotlib.pyplot as plt
from PIL import Image
from pylab import imshow,show,subplot,array,figure,gray
from skimage import data
from skimage.filter import threshold_otsu, threshold_adaptive

file_name='../../data/cv_data/empire.jpg'
# load the image file
img = Image.open(file_name)
print img

# convert to gray
img_gray = img.convert('L')    # not inplace operator
print img_gray

# the input for threshold method must be ndarray.  can be color or gray 
image=array(img)

#image = data.page()
#print type(image)

global_thresh = threshold_otsu(image)
binary_global = image > global_thresh

block_size = 40


"""
threshold_adaptive calculates thresholds in regions of size `block_size` surrounding each pixel (i.e. local neighborhoods). 
Each threshold value is the weighted mean of the local neighborhood minus an offset value.
refer to http://scikit-image.org/docs/dev/api/skimage.filter.html
"""
#Bydefaultthe ‘gaussian’ method is used.  #Default offset is 0 #Default is ‘reflect’ #input image:  (N, M) ndarray #skimage.filter.threshold_adaptive(image, block_size, method='gaussian', offset=0, mode='reflect', param=None)
binary_adaptive = threshold_adaptive(image, block_size, offset=10)

fig, axes = plt.subplots(nrows=3, figsize=(7, 8))
ax0, ax1, ax2 = axes
plt.gray()

ax0.imshow(image)
ax0.set_title('Image')

ax1.imshow(binary_global)
ax1.set_title('Global thresholding')

ax2.imshow(binary_adaptive)
ax2.set_title('Adaptive thresholding')

for ax in axes:
    ax.axis('off')

plt.show()
