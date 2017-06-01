"""
    open an image file and show it.
"""
import sys
from PIL import Image
from pylab import imshow,show,axis
import numpy as np

# load the image file

img = Image.open(sys.argv[1])
#img = Image.open('../../data/cv_data/empire.jpg')
print img.width, img.height
print img
print dir(img)
arr = np.array(img)
#arr =np.zeros(shape=(100,200,3),dtype=np.int)
print arr.shape, arr.dtype
noise = 4*np.random.standard_normal(arr.shape[0:2])
noise = np.dstack((noise,)*arr.shape[2])
print noise
arr = np.clip(arr + noise, 0, 255)
print arr.shape, arr.dtype
arr = np.uint8(arr)
print arr
img = Image.fromarray(arr)
img.show()
