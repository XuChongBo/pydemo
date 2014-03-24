#!/usr/bin/env python
# -*- coding:utf-8 -*-
from PIL import Image
from pylab import imshow,show,subplot,array,figure,gray,zeros,ones,uint8,jet
from skimage.filter import threshold_adaptive
from scipy.ndimage import filters,measurements

file_name='../../data/cv_data/empire.jpg'
# load the image file
img_gray = array(Image.open(file_name).convert('L'))

# binary the image
img_bin = threshold_adaptive(img_gray, block_size=15, offset=10)

#refers to http://docs.scipy.org/doc/scipy/reference/ndimage.html
#none-zero pixels are considered.
#label begin from 1.
#structure defines the connect condition.
s = array([[1,1,1],[1,1,1],[1,1,1]])
labeled_array, num_features = measurements.label(img_bin, structure=s)
print labeled_array
print num_features 

figure()
gray() # don't use colors 

subplot(1,2,1)   
imshow(img_gray)

subplot(1,2,2)

#imshow(labeled_array>173)
#print labeled_array==173
imshow(labeled_array)
jet()
show()

#print zeros(labeled_array.shape)+220
# starts the figure GUI and raises the figure windows
