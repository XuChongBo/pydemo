from PIL import Image
from pylab import imshow,show,axis,array,zeros
from pylab import jet
import numpy as np

# load the image file
img = Image.open('../../data/cv_data/empire.jpg')

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
print type(array_data), array_data.shape, array_data.size, array_data.ndim, array_data.dtype, array_data.itemsize, array_data.strides
plt.imshow(array_data)
plt.show()
