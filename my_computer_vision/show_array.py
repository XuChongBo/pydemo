# -*- coding:utf-8 -*-
from PIL import Image
from pylab import imshow,show,axis,array,zeros
from pylab import jet
import numpy as np
import sys

# load the image file
img = Image.open(sys.argv[1])

img=array(img) 

#invert image
im2 = 255 - img                 

im3 = zeros(im2.shape)

im3=np.zeros(shape=(100,200),dtype=np.int)
im3[15:15+10,15:15+10]=11
print im3[15:15+10,15:15+10]

imshow(im3)   # Warning,  when im3 has float type, it sometime can not be show.  You have to convert it to uinit8 type
#imshow(zeros(im2.shape)+190)

show()


# another way
import matplotlib.pyplot as plt
array_data =np.clip(np.random.randn(5,5),0,1) #生成随机数据,5行5列,最大值1,最小值0
print type(array_data), array_data.shape, array_data.size, array_data.ndim, array_data.dtype, array_data.itemsize, array_data.strides
plt.imshow(array_data,cmap=plt.cm.gray)  #only surport shape: H,W  or H,W,3.  not for H,W,1
plt.show()
